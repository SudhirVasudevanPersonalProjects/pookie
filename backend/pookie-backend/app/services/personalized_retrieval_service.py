"""
PersonalizedRetrievalService - Hybrid RAG with centroid re-ranking.

Implements the personalized retrieval layer from docs/pookie-semantic-architecture.md.
Re-ranks FAISS results using circle centroids to personalize semantic similarity.
"""

import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from functools import lru_cache
from app.models.something_circle import SomethingCircle
from app.models.circle import Circle
from app.services.centroid_service import centroid_service


class PersonalizedRetrievalService:
    """
    Hybrid retrieval service combining FAISS and circle centroids.

    Scoring formula:
    final_score = (
        0.40 * base_similarity +           # FAISS cosine similarity
        0.40 * max_centroid_similarity +   # Best matching circle centroid
        0.15 * user_assignment_boost +     # +0.15 if manually assigned
        0.05 * (1 - confidence_penalty)    # -0.05 if confidence < 0.5
    )
    """

    def __init__(self):
        # Simple in-memory cache for centroid similarities
        # Key: (user_id, query_embedding_hash) -> Dict[int, float]
        self._centroid_cache: Dict[Tuple[str, int], Dict[int, float]] = {}
        self._cache_max_size = 100

    def retrieve_and_rerank(
        self,
        query_embedding: List[float],
        user_id: str,
        faiss_results: List[Tuple[int, float]],
        db: Session,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Re-rank FAISS results using hybrid scoring.

        Args:
            query_embedding: 384-dim query vector
            user_id: User UUID for filtering
            faiss_results: List of (something_id, base_similarity) from FAISS
            db: Database session
            top_k: Return top K results after re-ranking

        Returns:
            List of dicts with something_id, final_score, base_similarity, centroid_similarity
        """
        # Filter FAISS results to only include user's somethings (data isolation)
        faiss_results = self._filter_by_user(faiss_results, user_id, db)

        if not faiss_results:
            return []

        # Get centroid similarities for query
        centroid_sims = self._get_centroid_similarities(query_embedding, user_id, db)

        # Get learning signals for each something
        learning_signals = self._get_learning_signals(
            [sid for sid, _ in faiss_results],
            db
        )

        # Calculate hybrid scores
        scored_results = []
        for something_id, base_similarity in faiss_results:
            # Get max centroid similarity for this something's circles
            max_centroid_sim = centroid_sims.get(something_id, 0.0)

            # Get learning signals
            signals = learning_signals.get(something_id, {
                "is_user_assigned": False,
                "confidence_score": None
            })

            # Calculate boosts/penalties
            user_boost = 0.15 if signals["is_user_assigned"] else 0.0

            confidence_penalty = 0.0
            if not signals["is_user_assigned"] and signals["confidence_score"] is not None:
                if signals["confidence_score"] < 0.5:
                    confidence_penalty = 0.05

            # Hybrid scoring formula
            # Weights: 40% base + 40% centroid + 15% user boost + 5% confidence
            # When penalty applies: subtract 5% instead of add
            final_score = (
                0.40 * base_similarity +
                0.40 * max_centroid_sim +
                user_boost -
                confidence_penalty  # Subtract penalty (0.05 for low confidence, 0.00 otherwise)
            )

            scored_results.append({
                "something_id": something_id,
                "final_score": final_score,
                "base_similarity": base_similarity,
                "centroid_similarity": max_centroid_sim
            })

        # Sort by final score descending
        scored_results.sort(key=lambda x: x["final_score"], reverse=True)

        return scored_results[:top_k]

    def _get_centroid_similarities(
        self,
        query_embedding: List[float],
        user_id: str,
        db: Session
    ) -> Dict[int, float]:
        """
        Get centroid similarities for all somethings via their circles.
        Uses simple caching to avoid repeated centroid calculations.

        Returns:
            Dict mapping something_id -> max_centroid_similarity
        """
        # Simple cache key based on query embedding hash
        query_hash = hash(tuple(query_embedding[:10]))  # Hash first 10 dims for speed
        cache_key = (user_id, query_hash)

        # Check cache
        if cache_key in self._centroid_cache:
            return self._centroid_cache[cache_key]

        # Get circle similarities for query
        circle_sims = centroid_service.compute_circle_similarities(
            query_embedding,
            user_id,
            db,
            top_k=100  # Get all circles
        )

        if not circle_sims:
            return {}

        # Build mapping: circle_id -> similarity
        circle_sim_map = {circle_id: sim for circle_id, _, sim in circle_sims}

        # Get all somethings in these circles
        circle_ids = [cid for cid, _, _ in circle_sims]
        something_circles = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id.in_(circle_ids)
        ).all()

        # Build mapping: something_id -> max_centroid_similarity
        something_max_sims = {}
        for sc in something_circles:
            circle_sim = circle_sim_map.get(sc.circle_id, 0.0)
            current_max = something_max_sims.get(sc.something_id, 0.0)
            something_max_sims[sc.something_id] = max(current_max, circle_sim)

        # Cache the result (with simple size limit)
        if len(self._centroid_cache) >= self._cache_max_size:
            # Simple eviction: remove oldest (first) entry
            self._centroid_cache.pop(next(iter(self._centroid_cache)))
        self._centroid_cache[cache_key] = something_max_sims

        return something_max_sims

    def _get_learning_signals(
        self,
        something_ids: List[int],
        db: Session
    ) -> Dict[int, Dict]:
        """
        Get learning signals (user assignment, confidence) for somethings.

        Returns:
            Dict mapping something_id -> {"is_user_assigned": bool, "confidence_score": float}
        """
        # Get all circle assignments for these somethings
        assignments = db.query(SomethingCircle).filter(
            SomethingCircle.something_id.in_(something_ids)
        ).all()

        # Build signal map - use max signal if multiple circles
        signals = {}
        for assignment in assignments:
            sid = assignment.something_id

            # If any circle is user-assigned, mark as user-assigned
            if sid not in signals or assignment.is_user_assigned:
                signals[sid] = {
                    "is_user_assigned": assignment.is_user_assigned,
                    "confidence_score": assignment.confidence_score
                }

        return signals

    def _filter_by_user(
        self,
        faiss_results: List[Tuple[int, float]],
        user_id: str,
        db: Session
    ) -> List[Tuple[int, float]]:
        """
        Filter FAISS results to only include somethings owned by user.

        Args:
            faiss_results: List of (something_id, base_similarity)
            user_id: User UUID
            db: Database session

        Returns:
            Filtered list containing only user's somethings
        """
        from app.models.something import Something

        something_ids = [sid for sid, _ in faiss_results]

        # Query to get somethings owned by this user
        user_something_ids = db.query(Something.id).filter(
            Something.id.in_(something_ids),
            Something.user_id == user_id
        ).all()

        user_ids_set = {sid[0] for sid in user_something_ids}

        # Filter results to only include user's somethings
        return [(sid, score) for sid, score in faiss_results if sid in user_ids_set]

    def format_rag_context(
        self,
        something_ids: List[int],
        db: Session,
        max_tokens: int = 1000
    ) -> str:
        """
        Format retrieved somethings as RAG context for LLM.

        Args:
            something_ids: List of something IDs to format
            db: Database session
            max_tokens: Maximum tokens for context (default 1000)

        Returns:
            Formatted context string with content, meanings, and circle names
        """
        from app.models.something import Something

        # Fetch somethings with circle relationships
        somethings = db.query(Something).filter(
            Something.id.in_(something_ids)
        ).all()

        if not somethings:
            return ""

        # Build context with token limiting
        lines = ["From your saved somethings:\n"]
        token_count = 10  # Approximate for header

        for i, something in enumerate(somethings, 1):
            # Get circle names
            circle_names = [sc.circle.circle_name for sc in something.circles]
            circle_str = ", ".join(circle_names) if circle_names else "Uncategorized"

            # Format entry
            meaning_str = f" (meaning: {something.meaning})" if something.meaning else ""
            entry = f"{i}. \"{something.content}\"{meaning_str} [Circle: {circle_str}]"

            # Rough token estimate: ~1 token per 4 chars
            entry_tokens = len(entry) // 4

            # Stop if we'd exceed max_tokens
            if token_count + entry_tokens > max_tokens:
                break

            lines.append(entry)
            token_count += entry_tokens

        # Add circle context summary
        all_circles = set()
        for something in somethings:
            all_circles.update(sc.circle.circle_name for sc in something.circles)

        if all_circles:
            circles_list = ", ".join(sorted(all_circles))
            lines.append(f"\nBased on your circles, you care about {circles_list}.")

        return "\n".join(lines)


# Singleton instance
personalized_retrieval_service = PersonalizedRetrievalService()
