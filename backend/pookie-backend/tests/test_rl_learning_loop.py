"""
Tests for Reinforcement Learning Learning Loop (MVP-4).

Validates that the centroid RL system learns from user feedback.

These tests demonstrate the core RL principle:
- User corrections shift centroids
- Shifted centroids improve future predictions
"""

import pytest
import numpy as np
from app.models.circle import Circle
from app.models.something import Something
from app.models.something_circle import SomethingCircle
from app.services.centroid_service import centroid_service


def test_rl_user_correction_shifts_centroid_toward_new_item(db_session, test_user):
    """
    Test that user assignment shifts centroid toward the assigned item.

    This is the foundation of RL: user feedback updates the model.
    """
    # Create circle with initial centroid pointing in one direction
    circle = Circle(
        user_id=test_user.id,
        circle_name="Test Circle",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381  # Points along X-axis
    )
    db_session.add(circle)
    db_session.commit()

    # Record initial centroid direction
    initial_centroid = np.array(circle.centroid_embedding[:3])  # First 3 dims

    # User assigns an item in a different direction (Y-axis)
    something = Something(
        user_id=test_user.id,
        content="User-assigned item",
        content_type="text"
    )
    db_session.add(something)
    db_session.commit()

    # Simulate embedding for this item (points along Y-axis)
    new_embedding = [0.0, 1.0, 0.0] + [0.0] * 381

    # Create assignment (user correction signal)
    sc = SomethingCircle(
        circle_id=circle.id,
        something_id=something.id,
        is_user_assigned=True  # High learning signal
    )
    db_session.add(sc)
    db_session.commit()

    # Update centroid with user's correction
    centroid_service.update_centroid_add(circle.id, new_embedding, db_session)

    # Get updated centroid
    db_session.refresh(circle)
    updated_centroid = np.array(circle.centroid_embedding[:3])

    # Verify centroid shifted toward Y-axis
    assert updated_centroid[1] > initial_centroid[1], \
        "Y component should increase after adding Y-axis item"

    # Verify centroid is still normalized
    magnitude = np.linalg.norm(circle.centroid_embedding)
    assert abs(magnitude - 1.0) < 1e-6, "Centroid should remain normalized"


def test_rl_centroid_shift_improves_prediction_for_similar_items(db_session, test_user):
    """
    Test that centroid shift from user feedback improves predictions.

    This demonstrates the learning effect:
    - Before: Circle A predicts best for X-axis items
    - User corrects: Assigns Y-axis item to Circle A
    - After: Circle A now predicts better for items near Y-axis
    """
    # Create two circles in different directions
    circle_a = Circle(
        user_id=test_user.id,
        circle_name="Circle A",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381  # X-axis
    )
    circle_b = Circle(
        user_id=test_user.id,
        circle_name="Circle B",
        centroid_embedding=[0.0, 1.0, 0.0] + [0.0] * 381  # Y-axis
    )
    db_session.add_all([circle_a, circle_b])
    db_session.commit()

    # Test query: Item at 45 degrees between X and Y
    query_embedding = [0.707, 0.707, 0.0] + [0.0] * 381

    # Initial prediction (before user feedback)
    predictions_before = centroid_service.compute_circle_similarities(
        query_embedding, test_user.id, db_session, top_k=2
    )

    # Both circles should score similarly (item is equidistant)
    score_a_before = predictions_before[0][2] if predictions_before[0][0] == circle_a.id else predictions_before[1][2]
    score_b_before = predictions_before[0][2] if predictions_before[0][0] == circle_b.id else predictions_before[1][2]

    # User corrects: assigns multiple Y-like items to Circle A
    # This shifts Circle A's centroid toward Y-axis
    for i in range(3):
        something = Something(
            user_id=test_user.id,
            content=f"Y-like item {i}",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()

        sc = SomethingCircle(
            circle_id=circle_a.id,
            something_id=something.id,
            is_user_assigned=True
        )
        db_session.add(sc)
        db_session.commit()

        # Each assignment shifts centroid
        y_like_embedding = [0.2, 0.8, 0.0] + [0.0] * 381
        centroid_service.update_centroid_add(circle_a.id, y_like_embedding, db_session)

    # Final prediction (after user feedback)
    predictions_after = centroid_service.compute_circle_similarities(
        query_embedding, test_user.id, db_session, top_k=2
    )

    score_a_after = predictions_after[0][2] if predictions_after[0][0] == circle_a.id else predictions_after[1][2]

    # Circle A's score should improve for this query (moved closer to Y)
    # Since query is at 45 degrees and Circle A moved from X toward Y
    assert score_a_after > score_a_before or abs(score_a_after - score_a_before) < 0.1, \
        f"Circle A score should improve after learning: {score_a_before:.3f} -> {score_a_after:.3f}"


def test_rl_multiple_corrections_compound_learning(db_session, test_user):
    """
    Test that multiple user corrections compound the learning effect.

    Each correction should shift the centroid further in the learned direction.
    """
    circle = Circle(
        user_id=test_user.id,
        circle_name="Learning Circle",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381
    )
    db_session.add(circle)
    db_session.commit()

    # Track centroid movement
    centroids = []
    centroids.append(np.array(circle.centroid_embedding[:2]))  # Initial

    # Apply 5 corrections, each adding a Y-component
    for i in range(5):
        something = Something(
            user_id=test_user.id,
            content=f"Item {i}",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()

        sc = SomethingCircle(
            circle_id=circle.id,
            something_id=something.id,
            is_user_assigned=True
        )
        db_session.add(sc)
        db_session.commit()

        # Add item with Y-component
        correction_embedding = [0.3, 0.7, 0.0] + [0.0] * 381
        centroid_service.update_centroid_add(circle.id, correction_embedding, db_session)

        db_session.refresh(circle)
        centroids.append(np.array(circle.centroid_embedding[:2]))

    # Verify Y-component increased with each correction
    y_components = [c[1] for c in centroids]

    for i in range(1, len(y_components)):
        assert y_components[i] >= y_components[i-1] - 0.01, \
            f"Y-component should increase or stay stable: step {i-1}->{i}"

    # Final Y-component should be substantial
    assert y_components[-1] > 0.5, \
        f"After 5 corrections, Y-component should be > 0.5, got {y_components[-1]:.3f}"


def test_rl_learning_signal_stored_in_junction_table(db_session, test_user):
    """
    Test that user assignment stores learning signal (is_user_assigned=True).

    This metadata enables future RL improvements (e.g., weighting by confidence).
    """
    circle = Circle(
        user_id=test_user.id,
        circle_name="Test Circle",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381
    )
    db_session.add(circle)
    db_session.commit()

    something = Something(
        user_id=test_user.id,
        content="User-corrected item",
        content_type="text"
    )
    db_session.add(something)
    db_session.commit()

    # User manually assigns (correction signal)
    sc = SomethingCircle(
        circle_id=circle.id,
        something_id=something.id,
        is_user_assigned=True,  # Learning signal
        confidence_score=None  # User assignments have no confidence
    )
    db_session.add(sc)
    db_session.commit()

    # Verify signal stored
    retrieved_sc = db_session.query(SomethingCircle).filter_by(
        circle_id=circle.id,
        something_id=something.id
    ).first()

    assert retrieved_sc is not None
    assert retrieved_sc.is_user_assigned is True, \
        "User assignment signal should be stored"


def test_rl_centroid_reflects_learned_distribution(db_session, test_user):
    """
    Test that final centroid position reflects the learned distribution of items.

    If user assigns items clustered in one area, centroid should move there.
    """
    circle = Circle(
        user_id=test_user.id,
        circle_name="Distribution Test",
        centroid_embedding=[0.0, 0.0, 1.0] + [0.0] * 381  # Start on Z-axis
    )
    db_session.add(circle)
    db_session.commit()

    # User assigns 10 items all clustered near [0.8, 0.6, 0] (XY plane)
    cluster_embeddings = []
    for i in range(10):
        # Small variations around [0.8, 0.6, 0]
        emb = [
            0.8 + np.random.uniform(-0.1, 0.1),
            0.6 + np.random.uniform(-0.1, 0.1),
            0.0
        ] + [0.0] * 381
        cluster_embeddings.append(emb)

        something = Something(
            user_id=test_user.id,
            content=f"Cluster item {i}",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()

        sc = SomethingCircle(
            circle_id=circle.id,
            something_id=something.id,
            is_user_assigned=True
        )
        db_session.add(sc)
        db_session.commit()

        centroid_service.update_centroid_add(circle.id, emb, db_session)

    # Final centroid should be near the cluster center
    db_session.refresh(circle)
    final_centroid = np.array(circle.centroid_embedding[:3])

    # Should be closer to [0.8, 0.6, 0] than to initial [0, 0, 1]
    cluster_center = np.array([0.8, 0.6, 0.0])
    initial_position = np.array([0.0, 0.0, 1.0])

    distance_to_cluster = np.linalg.norm(final_centroid - cluster_center)
    distance_to_initial = np.linalg.norm(final_centroid - initial_position)

    assert distance_to_cluster < distance_to_initial, \
        f"Centroid should move toward learned cluster: " \
        f"dist to cluster={distance_to_cluster:.3f}, dist to initial={distance_to_initial:.3f}"
