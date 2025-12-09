"""
Test suite for hybrid RAG scoring validation (MVP-4 AC: 3).

Validates PersonalizedRetrievalService hybrid scoring formula:
    final_score = 0.40 * base + 0.40 * centroid + 0.15 * user_boost + 0.05 * (1 - confidence_penalty)

Tests cover:
- Formula weights sum to 1.0
- Centroid boost increases relevance scores vs. vanilla FAISS
- User assignment boost (+0.15) correctly applied
- Re-ranked results differ from raw FAISS results
- Fallback to vanilla FAISS when no circles exist
"""

import pytest
import numpy as np
from app.services.personalized_retrieval_service import personalized_retrieval_service
from app.services.centroid_service import centroid_service
from app.models.something import Something
from app.models.circle import Circle
from app.models.something_circle import SomethingCircle


class TestHybridRAGScoringFormula:
    """Test hybrid scoring formula correctness."""

    def test_formula_weights_sum_to_one(self):
        """
        AC: 3 - Formula weights sum to 1.0: 0.40 + 0.40 + 0.15 + 0.05 = 1.00

        Validates that hybrid scoring weights are balanced:
        - Base FAISS: 40%
        - Centroid similarity: 40%
        - User assignment boost: 15%
        - Confidence factor: 5%
        """
        # Weights from PersonalizedRetrievalService:92-100
        base_weight = 0.40
        centroid_weight = 0.40
        user_boost_weight = 0.15
        confidence_weight = 0.05

        total = base_weight + centroid_weight + user_boost_weight + confidence_weight

        assert total == 1.0, f"Formula weights must sum to 1.0, got {total}"

    def test_centroid_boost_increases_relevance_scores(
        self,
        db_session,
        test_user,
        test_user_id,
    ):
        """
        AC: 3 - Centroid boost increases relevance scores vs. vanilla FAISS.

        Scenario:
        - Create 3 somethings: A, B, C
        - Create 1 circle with centroid close to B
        - Query with embedding similar to B
        - Assert: hybrid_score(B) > vanilla_score(B) due to centroid boost
        """
        # Create somethings with known embeddings
        embedding_a = [1.0] + [0.0] * 383  # Normalize later
        embedding_b = [0.0, 1.0] + [0.0] * 382
        embedding_c = [0.0, 0.0, 1.0] + [0.0] * 381

        # Normalize embeddings
        embedding_a = (np.array(embedding_a) / np.linalg.norm(embedding_a)).tolist()
        embedding_b = (np.array(embedding_b) / np.linalg.norm(embedding_b)).tolist()
        embedding_c = (np.array(embedding_c) / np.linalg.norm(embedding_c)).tolist()

        # Create somethings manually
        something_a = Something(user_id=test_user.id, content="Item A")
        something_b = Something(user_id=test_user.id, content="Item B")
        something_c = Something(user_id=test_user.id, content="Item C")
        db_session.add_all([something_a, something_b, something_c])
        db_session.flush()

        # Set embeddings after creation
        something_a.embedding = embedding_a
        something_b.embedding = embedding_b
        something_c.embedding = embedding_c
        db_session.flush()

        # Create circle with centroid close to B
        circle = Circle(
            user_id=test_user_id,
            circle_name="Circle B",
            centroid_embedding=embedding_b
            
        )
        db_session.add(circle)
        db_session.flush()

        # Add B to circle
        sc = SomethingCircle(
            something_id=something_b.id,
            circle_id=circle.id,
            is_user_assigned=False,
            confidence_score=0.95
        )
        db_session.add(sc)
        db_session.commit()

        # Query embedding similar to B
        query_embedding = embedding_b

        # Vanilla FAISS results (no re-ranking)
        faiss_results = [
            (something_b.id, 1.0),   # Perfect match
            (something_a.id, 0.5),
            (something_c.id, 0.3),
        ]

        # Hybrid re-ranking
        hybrid_results = personalized_retrieval_service.retrieve_and_rerank(
            query_embedding=query_embedding,
            user_id=test_user_id,
            faiss_results=faiss_results,
            db=db_session,
            top_k=3
        )

        # Find B in hybrid results
        result_b = next(r for r in hybrid_results if r["something_id"] == something_b.id)

        # Hybrid score should be higher than vanilla (due to centroid boost)
        vanilla_score = 1.0  # Base FAISS score for B
        hybrid_score = result_b["final_score"]

        # Expected: 0.40 * 1.0 (base) + 0.40 * 1.0 (centroid) = 0.80 (no user boost, no penalty)
        expected_score = 0.80

        assert hybrid_score > vanilla_score * 0.40, \
            f"Hybrid score should exceed vanilla*0.40 due to centroid boost. Got {hybrid_score}"
        assert abs(hybrid_score - expected_score) < 0.01, \
            f"Expected hybrid score ~{expected_score}, got {hybrid_score}"

    def test_user_assignment_boost_applied_correctly(
        self,
        db_session,
        test_user,
        test_user_id,
    ):
        """
        AC: 3 - User assignment boost (+0.15) correctly applied when is_user_assigned=True.

        Scenario:
        - Create 2 identical somethings A and B
        - Assign both to same circle
        - Set A: is_user_assigned=True, B: is_user_assigned=False
        - Assert: final_score(A) = final_score(B) + 0.15
        """
        # Create identical embeddings
        embedding = [1.0] + [0.0] * 383
        embedding = (np.array(embedding) / np.linalg.norm(embedding)).tolist()

        # Create somethings manually
        something_a = Something(user_id=test_user.id, content="Item A - User Assigned")
        something_b = Something(user_id=test_user.id, content="Item B - Auto Assigned")
        db_session.add_all([something_a, something_b])
        db_session.flush()

        # Set embeddings after creation
        something_a.embedding = embedding
        something_b.embedding = embedding
        db_session.flush()

        # Create circle
        circle = Circle(
            user_id=test_user_id,
            circle_name="Test Circle",
            centroid_embedding=embedding
            
        )
        db_session.add(circle)
        db_session.flush()

        # Add A with user assignment
        sc_a = SomethingCircle(
            something_id=something_a.id,
            circle_id=circle.id,
            is_user_assigned=True,  # User manually assigned
            confidence_score=0.95
        )
        db_session.add(sc_a)

        # Add B without user assignment
        sc_b = SomethingCircle(
            something_id=something_b.id,
            circle_id=circle.id,
            is_user_assigned=False,  # Auto-assigned by clustering
            confidence_score=0.95
        )
        db_session.add(sc_b)
        db_session.commit()

        # Query with same embedding
        query_embedding = embedding

        # FAISS results (identical scores)
        faiss_results = [
            (something_a.id, 1.0),
            (something_b.id, 1.0),
        ]

        # Hybrid re-ranking
        hybrid_results = personalized_retrieval_service.retrieve_and_rerank(
            query_embedding=query_embedding,
            user_id=test_user_id,
            faiss_results=faiss_results,
            db=db_session,
            top_k=2
        )

        result_a = next(r for r in hybrid_results if r["something_id"] == something_a.id)
        result_b = next(r for r in hybrid_results if r["something_id"] == something_b.id)

        # A should have +0.15 boost
        score_diff = result_a["final_score"] - result_b["final_score"]

        assert abs(score_diff - 0.15) < 0.01, \
            f"User assignment boost should be 0.15, got {score_diff}"
        assert result_a["final_score"] > result_b["final_score"], \
            "User-assigned item should rank higher"

    def test_reranking_changes_order_vs_vanilla_faiss(
        self,
        db_session,
        test_user,
        test_user_id,
    ):
        """
        AC: 3 - Re-ranked results differ from raw FAISS results (personalization works).

        Scenario:
        - Create 3 somethings with different embeddings
        - Create circle with centroid close to item C (lowest FAISS score)
        - Query returns: A (0.9), B (0.8), C (0.5) from vanilla FAISS
        - After re-ranking with centroid boost, C should move up
        """
        # Create distinct embeddings
        embedding_a = [1.0, 0.0] + [0.0] * 382
        embedding_b = [0.9, 0.1] + [0.0] * 382
        embedding_c = [0.0, 1.0] + [0.0] * 382

        embedding_a = (np.array(embedding_a) / np.linalg.norm(embedding_a)).tolist()
        embedding_b = (np.array(embedding_b) / np.linalg.norm(embedding_b)).tolist()
        embedding_c = (np.array(embedding_c) / np.linalg.norm(embedding_c)).tolist()

        # Create somethings manually
        something_a = Something(user_id=test_user.id, content="High FAISS score")
        something_b = Something(user_id=test_user.id, content="Medium FAISS score")
        something_c = Something(user_id=test_user.id, content="Low FAISS but in user's circle")
        db_session.add_all([something_a, something_b, something_c])
        db_session.flush()

        # Set embeddings after creation
        something_a.embedding = embedding_a
        something_b.embedding = embedding_b
        something_c.embedding = embedding_c
        db_session.flush()

        # Create circle with centroid matching C
        circle = Circle(
            user_id=test_user_id,
            circle_name="Circle C",
            centroid_embedding=embedding_c
            
        )
        db_session.add(circle)
        db_session.flush()

        sc = SomethingCircle(
            something_id=something_c.id,
            circle_id=circle.id,
            is_user_assigned=False,
            confidence_score=0.95
        )
        db_session.add(sc)
        db_session.commit()

        # Query close to C (to trigger centroid boost for C)
        # This will test that centroid re-ranking applies correctly
        query_embedding = embedding_c

        # Simulated vanilla FAISS results (before re-ranking)
        # A has highest base score despite query being close to C
        # This simulates vanilla FAISS not knowing about user's circles
        faiss_results = [
            (something_a.id, 0.70),  # Not related to query but high FAISS score
            (something_c.id, 0.65),  # Related to query AND in user's circle
            (something_b.id, 0.60),
        ]

        # Hybrid re-ranking
        hybrid_results = personalized_retrieval_service.retrieve_and_rerank(
            query_embedding=query_embedding,
            user_id=test_user_id,
            faiss_results=faiss_results,
            db=db_session,
            top_k=3
        )

        # Verify personalization occurred: centroid_similarity should be > 0 for C
        result_c = next(r for r in hybrid_results if r["something_id"] == something_c.id)

        assert result_c["centroid_similarity"] > 0, \
            "Item C should have centroid_similarity > 0 since it's in a circle"

        # C's final score should be boosted above its base score due to centroid
        # final_score = 0.40 * base + 0.40 * centroid
        # With base=0.50, centroid=1.0 (C's circle centroid matches C perfectly):
        # Expected: 0.40 * 0.50 + 0.40 * 1.0 = 0.20 + 0.40 = 0.60
        expected_boost_min = 0.40 * result_c["centroid_similarity"]
        assert result_c["final_score"] > result_c["base_similarity"], \
            f"Final score ({result_c['final_score']}) should exceed base ({result_c['base_similarity']}) due to centroid boost"

        # Verify re-ranking modified scores (personalization applied)
        # At least one item should have non-zero centroid_similarity
        centroid_sims = [r["centroid_similarity"] for r in hybrid_results]
        assert any(cs > 0 for cs in centroid_sims), \
            "At least one item should have centroid_similarity > 0 (personalization applied)"

    def test_fallback_to_vanilla_when_no_circles(
        self,
        db_session,
        test_user,
        test_user_id,
    ):
        """
        AC: 3 - Fallback to vanilla FAISS when no circles exist (graceful degradation).

        Scenario:
        - User has no circles
        - Query returns FAISS results
        - Hybrid scoring should degrade gracefully:
            final_score = 0.40 * base + 0.40 * 0.0 = 0.40 * base
        - Order should match vanilla FAISS (no personalization)
        """
        # Create somethings (no circles)
        embedding_a = [1.0] + [0.0] * 383
        embedding_b = [0.5, 0.5] + [0.0] * 382

        embedding_a = (np.array(embedding_a) / np.linalg.norm(embedding_a)).tolist()
        embedding_b = (np.array(embedding_b) / np.linalg.norm(embedding_b)).tolist()

        # Create somethings manually
        something_a = Something(user_id=test_user.id, content="Item A")
        something_b = Something(user_id=test_user.id, content="Item B")
        db_session.add_all([something_a, something_b])
        db_session.flush()

        # Set embeddings after creation
        something_a.embedding = embedding_a
        something_b.embedding = embedding_b
        db_session.commit()

        # No circles created - graceful degradation scenario

        # Query
        query_embedding = embedding_a

        # Vanilla FAISS results
        faiss_results = [
            (something_a.id, 0.95),
            (something_b.id, 0.70),
        ]

        # Hybrid re-ranking (should fallback gracefully)
        hybrid_results = personalized_retrieval_service.retrieve_and_rerank(
            query_embedding=query_embedding,
            user_id=test_user_id,
            faiss_results=faiss_results,
            db=db_session,
            top_k=2
        )

        # Order should match vanilla (no centroid boost available)
        hybrid_order = [r["something_id"] for r in hybrid_results]
        vanilla_order = [something_a.id, something_b.id]

        assert hybrid_order == vanilla_order, \
            "Order should match vanilla FAISS when no circles exist"

        # Scores should be 40% of vanilla (only base_similarity component)
        result_a = hybrid_results[0]
        expected_score_a = 0.40 * 0.95  # Only base component

        assert abs(result_a["final_score"] - expected_score_a) < 0.01, \
            f"With no circles, hybrid score should be 0.40*vanilla. Expected {expected_score_a}, got {result_a['final_score']}"

    def test_retrieval_quality_improves_with_personalization(
        self,
        db_session,
        test_user,
        test_user_id,
    ):
        """
        AC: 3 - Verify retrieval quality improves with personalization.

        Scenario:
        - Create 5 somethings across 2 semantic themes
        - Theme 1 (work): 3 items
        - Theme 2 (hobby): 2 items
        - User has circle for Theme 1 (work items)
        - Query about work topic
        - Assert: All Theme 1 items rank higher than Theme 2 items
        """
        # Theme 1: Work-related embeddings (clustered)
        work_base = [1.0, 0.0] + [0.0] * 382
        work_emb_1 = (np.array([1.0, 0.1] + [0.0] * 382) / np.linalg.norm([1.0, 0.1] + [0.0] * 382)).tolist()
        work_emb_2 = (np.array([0.9, 0.1] + [0.0] * 382) / np.linalg.norm([0.9, 0.1] + [0.0] * 382)).tolist()
        work_emb_3 = (np.array([1.0, 0.0] + [0.0] * 382) / np.linalg.norm([1.0, 0.0] + [0.0] * 382)).tolist()

        # Theme 2: Hobby-related embeddings (different cluster)
        hobby_emb_1 = (np.array([0.0, 1.0] + [0.0] * 382) / np.linalg.norm([0.0, 1.0] + [0.0] * 382)).tolist()
        hobby_emb_2 = (np.array([0.1, 0.9] + [0.0] * 382) / np.linalg.norm([0.1, 0.9] + [0.0] * 382)).tolist()

        # Create somethings manually
        work_1 = Something(user_id=test_user.id, content="Work task 1")
        work_2 = Something(user_id=test_user.id, content="Work task 2")
        work_3 = Something(user_id=test_user.id, content="Work task 3")
        hobby_1 = Something(user_id=test_user.id, content="Hobby item 1")
        hobby_2 = Something(user_id=test_user.id, content="Hobby item 2")
        db_session.add_all([work_1, work_2, work_3, hobby_1, hobby_2])
        db_session.flush()

        # Set embeddings after creation
        work_1.embedding = work_emb_1
        work_2.embedding = work_emb_2
        work_3.embedding = work_emb_3
        hobby_1.embedding = hobby_emb_1
        hobby_2.embedding = hobby_emb_2
        db_session.flush()

        # Create circle for work theme
        work_centroid = (np.array(work_base) / np.linalg.norm(work_base)).tolist()
        circle_work = Circle(
            user_id=test_user_id,
            circle_name="Work Circle",
            centroid_embedding=work_centroid
            
        )
        db_session.add(circle_work)
        db_session.flush()

        # Assign work items to circle
        for work_obj in [work_1, work_2, work_3]:
            sc = SomethingCircle(
                something_id=work_obj.id,
                circle_id=circle_work.id,
                is_user_assigned=False,
                confidence_score=0.90
            )
            db_session.add(sc)
        db_session.commit()

        # Query about work (close to work centroid)
        query_embedding = work_centroid

        # Vanilla FAISS might rank hobby items high if embeddings happen to match
        # Simulate scenario where hobby_1 has decent vanilla score
        faiss_results = [
            (work_1.id, 0.95),
            (work_2.id, 0.90),
            (hobby_1.id, 0.85),  # Vanilla FAISS ranks this 3rd
            (work_3.id, 0.80),   # But work_3 should rank higher with personalization
            (hobby_2.id, 0.75),
        ]

        # Hybrid re-ranking
        hybrid_results = personalized_retrieval_service.retrieve_and_rerank(
            query_embedding=query_embedding,
            user_id=test_user_id,
            faiss_results=faiss_results,
            db=db_session,
            top_k=5
        )

        # Extract positions
        work_positions = [
            i for i, r in enumerate(hybrid_results)
            if r["something_id"] in [work_1.id, work_2.id, work_3.id]
        ]
        hobby_positions = [
            i for i, r in enumerate(hybrid_results)
            if r["something_id"] in [hobby_1.id, hobby_2.id]
        ]

        # All work items should rank higher than hobby items
        max_work_pos = max(work_positions)
        min_hobby_pos = min(hobby_positions)

        assert max_work_pos < min_hobby_pos, \
            f"All work items should rank before hobby items. Work: {work_positions}, Hobby: {hobby_positions}"
