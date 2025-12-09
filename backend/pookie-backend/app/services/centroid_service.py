"""
Centroid Service for Circle Reinforcement Learning.

Implements incremental centroid updates using vector math for personalized semantic learning.
Key innovation: Layering custom semantics (centroids) on top of base embeddings for real-time personalization.
"""

import numpy as np
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.circle import Circle
from app.models.something import Something
from app.models.something_circle import SomethingCircle


class CentroidService:
    """
    Service for managing circle centroids with incremental RL updates.

    Architecture:
    - Layer 1: Base embeddings (sentence-transformers) = universal language
    - Layer 2: Circle centroids = personalized semantic categories
    - Learning: Incremental mean updates from user feedback (<50ms per update)

    Why Centroids:
    - Real-time: Update in <50ms (vs hours for fine-tuning)
    - Interpretable: See exactly how circles shift
    - Free tier compatible: No GPU/API costs
    - No catastrophic forgetting
    """

    def initialize_centroid(
        self,
        circle_id: int,
        first_embedding: List[float],
        db: Session
    ) -> None:
        """
        Initialize centroid with first something's embedding.

        Args:
            circle_id: Circle to initialize
            first_embedding: 384-dim embedding vector
            db: Database session
        """
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        if not circle:
            raise ValueError(f"Circle {circle_id} not found")

        # Normalize to unit vector for cosine similarity
        embedding_array = np.array(first_embedding)
        normalized = embedding_array / np.linalg.norm(embedding_array)

        circle.centroid_embedding = normalized.tolist()
        db.commit()

    def update_centroid_add(
        self,
        circle_id: int,
        new_embedding: List[float],
        db: Session
    ) -> None:
        """
        Incrementally update centroid when something is added.

        Formula: new_centroid = (N * old_centroid + new_embedding) / (N + 1)
        Where N = current count of somethings in circle

        Args:
            circle_id: Circle to update
            new_embedding: 384-dim embedding of newly added something
            db: Database session
        """
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        if not circle:
            raise ValueError(f"Circle {circle_id} not found")

        # Count current items in circle
        n_items = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        new_emb = np.array(new_embedding)

        if circle.centroid_embedding is None:
            # First item - initialize
            normalized = new_emb / np.linalg.norm(new_emb)
            circle.centroid_embedding = normalized.tolist()
        else:
            # Incremental update
            old_centroid = np.array(circle.centroid_embedding)

            # Formula: (N * old + new) / (N + 1)
            # N includes the item we just added, so use (n_items - 1)
            if n_items == 1:
                # Just added first item
                updated = new_emb
            else:
                updated = ((n_items - 1) * old_centroid + new_emb) / n_items

            # Normalize to unit vector
            normalized = updated / np.linalg.norm(updated)
            circle.centroid_embedding = normalized.tolist()

        db.commit()

    def update_centroid_remove(
        self,
        circle_id: int,
        removed_embedding: List[float],
        db: Session
    ) -> None:
        """
        Incrementally update centroid when something is removed.

        Formula: new_centroid = ((N + 1) * old_centroid - removed_embedding) / N
        Where N = new count after removal

        Special case: If removing last item, set centroid to NULL

        Args:
            circle_id: Circle to update
            removed_embedding: 384-dim embedding of removed something
            db: Database session
        """
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        if not circle:
            raise ValueError(f"Circle {circle_id} not found")

        # Count remaining items after removal
        n_remaining = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        if n_remaining == 0:
            # Last item removed - clear centroid
            circle.centroid_embedding = None
        elif circle.centroid_embedding is not None:
            # Reverse the add operation
            old_centroid = np.array(circle.centroid_embedding)
            removed_emb = np.array(removed_embedding)

            # Formula: ((N + 1) * old - removed) / N
            # n_remaining is already the count AFTER removal
            updated = ((n_remaining + 1) * old_centroid - removed_emb) / n_remaining

            # Normalize to unit vector
            normalized = updated / np.linalg.norm(updated)
            circle.centroid_embedding = normalized.tolist()

        db.commit()

    def compute_circle_similarities(
        self,
        query_embedding: List[float],
        user_id: str,
        db: Session,
        top_k: int = 5
    ) -> List[Tuple[int, str, float]]:
        """
        Find circles most similar to query embedding using cosine similarity.

        Args:
            query_embedding: 384-dim query vector
            user_id: User UUID for filtering
            db: Database session
            top_k: Return top K matches

        Returns:
            List of (circle_id, circle_name, similarity_score) sorted by similarity desc
        """
        # Get all circles with centroids for this user
        circles = db.query(Circle).filter(
            Circle.user_id == user_id,
            Circle.centroid_embedding.isnot(None)
        ).all()

        if not circles:
            return []

        query = np.array(query_embedding)
        query_normalized = query / np.linalg.norm(query)

        similarities = []
        for circle in circles:
            centroid = np.array(circle.centroid_embedding)
            # Cosine similarity = dot product of normalized vectors
            similarity = np.dot(query_normalized, centroid)
            similarities.append((circle.id, circle.circle_name, float(similarity)))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[2], reverse=True)

        return similarities[:top_k]

    def predict_circles_for_embedding(
        self,
        embedding: List[float],
        user_id: str,
        db: Session,
        threshold: float = 0.7,
        top_k: int = 3
    ) -> List[dict]:
        """
        Predict which circles an embedding belongs to.

        Uses centroid similarity with confidence threshold.

        Args:
            embedding: 384-dim embedding vector to predict circles for
            user_id: User UUID for filtering
            db: Database session
            threshold: Minimum similarity score (0-1) to include
            top_k: Maximum predictions to return

        Returns:
            List of dicts with circleId, circleName, confidence
            Example: [{"circleId": 5, "circleName": "Fitness", "confidence": 0.89}]
        """
        # Find similar circles
        similarities = self.compute_circle_similarities(
            embedding,
            user_id,
            db,
            top_k=top_k
        )

        # Filter by threshold and format
        predictions = []
        for circle_id, circle_name, score in similarities:
            if score >= threshold:
                predictions.append({
                    "circleId": circle_id,
                    "circleName": circle_name,
                    "confidence": round(score, 2)
                })

        return predictions

    def predict_circles_for_something(
        self,
        something_id: int,
        user_id: str,
        db: Session,
        threshold: float = 0.7,
        top_k: int = 3
    ) -> List[dict]:
        """
        Predict which circles a something belongs to (convenience wrapper).

        Fetches something's embedding and calls predict_circles_for_embedding.

        Args:
            something_id: Something to predict circles for
            user_id: User UUID for filtering
            db: Database session
            threshold: Minimum similarity score (0-1) to include
            top_k: Maximum predictions to return

        Returns:
            List of dicts with circleId, circleName, confidence
            Empty list if something not found or has no content
        """
        # Import here to avoid circular dependency
        from app.services.embedding_service import embedding_service

        something = db.query(Something).filter(
            Something.id == something_id,
            Something.user_id == user_id
        ).first()

        if not something or not something.content or not something.content.strip():
            return []

        # Generate embedding
        embedding = embedding_service.generate_embedding(something.content)

        # Predict using embedding
        return self.predict_circles_for_embedding(
            embedding,
            user_id,
            db,
            threshold,
            top_k
        )


# Singleton instance
centroid_service = CentroidService()
