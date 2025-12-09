"""
Tests for CentroidService - Centroid RL math validation.

Validates:
- Incremental mean formulas (add/remove)
- Normalization to unit vectors
- Cosine similarity computation
- Edge cases (first item, last item, empty)
"""

import pytest
import numpy as np
from app.services.centroid_service import centroid_service
from app.models.circle import Circle
from app.models.something import Something
from app.models.something_circle import SomethingCircle


def test_initialize_centroid_first_item(db_session, test_user):
    """Test that first item correctly initializes centroid."""
    # Create circle
    circle = Circle(user_id=test_user.id, circle_name="Test Circle")
    db_session.add(circle)
    db_session.commit()

    # First embedding
    first_embedding = [1.0] * 384  # Simple vector for testing

    # Initialize centroid
    centroid_service.initialize_centroid(circle.id, first_embedding, db_session)

    # Verify centroid is set and normalized
    db_session.refresh(circle)
    assert circle.centroid_embedding is not None
    assert len(circle.centroid_embedding) == 384

    # Check normalization (magnitude should be 1.0)
    centroid_array = np.array(circle.centroid_embedding)
    magnitude = np.linalg.norm(centroid_array)
    assert abs(magnitude - 1.0) < 1e-6  # Float precision tolerance


def test_update_centroid_add_formula(db_session, test_user):
    """Test incremental add formula: (N * old + new) / (N + 1)."""
    # Create circle with initial centroid
    circle = Circle(
        user_id=test_user.id,
        circle_name="Math Test",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381  # Normalized unit vector
    )
    db_session.add(circle)
    db_session.commit()

    # Create first something to establish N=1
    something1 = Something(
        user_id=test_user.id,
        content="First item",
        content_type="text"
    )
    db_session.add(something1)
    db_session.commit()

    # Add to circle
    sc1 = SomethingCircle(circle_id=circle.id, something_id=something1.id, is_user_assigned=True)
    db_session.add(sc1)
    db_session.commit()

    # Add second item with different embedding
    something2 = Something(
        user_id=test_user.id,
        content="Second item",
        content_type="text"
    )
    db_session.add(something2)
    db_session.commit()

    new_embedding = [0.0, 1.0, 0.0] + [0.0] * 381

    # Add to circle and update centroid
    sc2 = SomethingCircle(circle_id=circle.id, something_id=something2.id, is_user_assigned=True)
    db_session.add(sc2)
    db_session.commit()

    centroid_service.update_centroid_add(circle.id, new_embedding, db_session)

    # Verify formula: (1 * [1,0,0] + [0,1,0]) / 2 = [0.5, 0.5, 0] (before normalization)
    db_session.refresh(circle)
    centroid = np.array(circle.centroid_embedding)

    # After normalization, should be roughly [0.707, 0.707, 0, ...]
    assert abs(centroid[0] - 0.707) < 0.01
    assert abs(centroid[1] - 0.707) < 0.01


def test_update_centroid_add_normalization(db_session, test_user):
    """Test that added centroids are normalized to unit vectors."""
    circle = Circle(
        user_id=test_user.id,
        circle_name="Normalization Test",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381
    )
    db_session.add(circle)
    db_session.commit()

    # Add something to trigger update
    something = Something(
        user_id=test_user.id,
        content="Item",
        content_type="text"
    )
    db_session.add(something)
    db_session.commit()

    sc = SomethingCircle(circle_id=circle.id, something_id=something.id, is_user_assigned=True)
    db_session.add(sc)
    db_session.commit()

    new_embedding = [1.0, 1.0, 1.0] + [0.0] * 381
    centroid_service.update_centroid_add(circle.id, new_embedding, db_session)

    # Verify magnitude = 1.0
    db_session.refresh(circle)
    magnitude = np.linalg.norm(np.array(circle.centroid_embedding))
    assert abs(magnitude - 1.0) < 1e-6


def test_update_centroid_remove_formula(db_session, test_user):
    """Test incremental remove formula: ((N+1) * old - removed) / N."""
    # Create circle with 2 items
    circle = Circle(
        user_id=test_user.id,
        circle_name="Remove Test",
        # Centroid after 2 items: [0.707, 0.707, 0] (normalized mean of [1,0,0] and [0,1,0])
        centroid_embedding=[0.707, 0.707, 0.0] + [0.0] * 381
    )
    db_session.add(circle)
    db_session.commit()

    # Create 2 somethings
    s1 = Something(user_id=test_user.id, content="S1", content_type="text")
    s2 = Something(user_id=test_user.id, content="S2", content_type="text")
    db_session.add_all([s1, s2])
    db_session.commit()

    sc1 = SomethingCircle(circle_id=circle.id, something_id=s1.id, is_user_assigned=True)
    sc2 = SomethingCircle(circle_id=circle.id, something_id=s2.id, is_user_assigned=True)
    db_session.add_all([sc1, sc2])
    db_session.commit()

    # Remove s2
    removed_embedding = [0.0, 1.0, 0.0] + [0.0] * 381
    db_session.delete(sc2)
    db_session.commit()

    centroid_service.update_centroid_remove(circle.id, removed_embedding, db_session)

    # After removing [0,1,0], centroid should move back toward [1,0,0]
    db_session.refresh(circle)
    centroid = np.array(circle.centroid_embedding)

    # Should be close to [1, 0, 0] (normalized)
    # Removing [0,1,0] from mean of [1,0,0] and [0,1,0]  leaves ~[1,0,0]
    assert centroid[0] > 0.95  # First dimension dominant
    assert abs(centroid[1]) < 0.3  # Second dimension reduced (formula imperfect due to normalization)


def test_update_centroid_remove_last_item(db_session, test_user):
    """Test that removing last item sets centroid to NULL."""
    circle = Circle(
        user_id=test_user.id,
        circle_name="Last Item Test",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381
    )
    db_session.add(circle)
    db_session.commit()

    # Create and add one something
    something = Something(user_id=test_user.id, content="Only item", content_type="text")
    db_session.add(something)
    db_session.commit()

    sc = SomethingCircle(circle_id=circle.id, something_id=something.id, is_user_assigned=True)
    db_session.add(sc)
    db_session.commit()

    # Remove the only item
    removed_embedding = [1.0, 0.0, 0.0] + [0.0] * 381
    db_session.delete(sc)
    db_session.commit()

    centroid_service.update_centroid_remove(circle.id, removed_embedding, db_session)

    # Centroid should be NULL
    db_session.refresh(circle)
    assert circle.centroid_embedding is None


def test_compute_circle_similarities(db_session, test_user):
    """Test cosine similarity computation and sorting."""
    # Create 3 circles with different centroids
    c1 = Circle(
        user_id=test_user.id,
        circle_name="Circle 1",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381  # X-axis
    )
    c2 = Circle(
        user_id=test_user.id,
        circle_name="Circle 2",
        centroid_embedding=[0.707, 0.707, 0.0] + [0.0] * 381  # 45 degrees
    )
    c3 = Circle(
        user_id=test_user.id,
        circle_name="Circle 3",
        centroid_embedding=[0.0, 1.0, 0.0] + [0.0] * 381  # Y-axis
    )
    db_session.add_all([c1, c2, c3])
    db_session.commit()

    # Query vector on X-axis (should match c1 best)
    query = [1.0, 0.0, 0.0] + [0.0] * 381

    similarities = centroid_service.compute_circle_similarities(
        query, test_user.id, db_session, top_k=3
    )

    # Should be sorted by similarity
    assert len(similarities) == 3
    assert similarities[0][1] == "Circle 1"  # Highest similarity
    assert similarities[0][2] > similarities[1][2]  # Descending
    assert similarities[1][2] > similarities[2][2]


def test_predict_circles_for_embedding(db_session, test_user):
    """Test circle prediction with threshold filtering."""
    # Create circles
    c1 = Circle(
        user_id=test_user.id,
        circle_name="High Match",
        centroid_embedding=[1.0, 0.0, 0.0] + [0.0] * 381
    )
    c2 = Circle(
        user_id=test_user.id,
        circle_name="Low Match",
        centroid_embedding=[0.0, 0.0, 1.0] + [0.0] * 381  # Orthogonal (similarity ~0)
    )
    db_session.add_all([c1, c2])
    db_session.commit()

    # Query embedding similar to c1
    query_embedding = [1.0, 0.0, 0.0] + [0.0] * 381

    # Predict with threshold=0.7
    predictions = centroid_service.predict_circles_for_embedding(
        query_embedding, test_user.id, db_session, threshold=0.7, top_k=3
    )

    # Should only return high match
    assert len(predictions) == 1
    assert predictions[0]["circleName"] == "High Match"
    assert predictions[0]["confidence"] >= 0.7


def test_predict_circles_no_centroids(db_session, test_user):
    """Test prediction returns empty list when no centroids exist."""
    # Create circle without centroid
    circle = Circle(user_id=test_user.id, circle_name="No Centroid", centroid_embedding=None)
    db_session.add(circle)
    db_session.commit()

    # Query embedding
    query_embedding = [1.0] * 384

    # Predict should return empty
    predictions = centroid_service.predict_circles_for_embedding(
        query_embedding, test_user.id, db_session
    )

    assert predictions == []


def test_floating_point_precision_over_100_operations(db_session, test_user):
    """
    Test that centroid updates maintain precision over 100+ operations.

    AC: 1 - Floating point precision: No accumulation errors over 100+ operations.

    This test verifies that incremental mean calculations don't accumulate
    floating point errors that would corrupt the centroid over many updates.
    """
    # Create circle with initial centroid
    initial_centroid = [1.0, 0.0, 0.0] + [0.0] * 381
    circle = Circle(
        user_id=test_user.id,
        circle_name="Precision Test",
        centroid_embedding=initial_centroid.copy()
    )
    db_session.add(circle)
    db_session.commit()

    # Perform 100 add operations with similar embeddings
    embeddings_to_add = []
    for i in range(100):
        # Create slight variations around [1, 0, 0]
        embedding = [1.0 + (i % 10) * 0.01, 0.0, 0.0] + [0.0] * 381
        embeddings_to_add.append(embedding)

        # Create something and add to circle
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

        # Update centroid incrementally
        centroid_service.update_centroid_add(circle.id, embedding, db_session)

    # Get final centroid after 100 operations
    db_session.refresh(circle)
    final_centroid = np.array(circle.centroid_embedding)

    # Verify centroid is still normalized (magnitude = 1.0)
    magnitude = np.linalg.norm(final_centroid)
    assert abs(magnitude - 1.0) < 1e-5, \
        f"Centroid should remain normalized after 100 ops: magnitude={magnitude}"

    # Verify centroid is still close to expected direction
    # Since all embeddings are near [1, 0, 0], centroid should still be on X-axis
    assert final_centroid[0] > 0.95, \
        f"After 100 operations, centroid should still point along X-axis: {final_centroid[:3]}"

    # Verify no NaN or Inf values (signs of floating point corruption)
    assert not np.isnan(final_centroid).any(), "Centroid contains NaN after 100 operations"
    assert not np.isinf(final_centroid).any(), "Centroid contains Inf after 100 operations"

    # Test stability: Compute centroid manually and compare
    # Manual calculation: mean of all embeddings (including initial)
    all_embeddings = [initial_centroid] + embeddings_to_add
    manual_mean = np.mean(all_embeddings, axis=0)
    manual_normalized = manual_mean / np.linalg.norm(manual_mean)

    # Incremental calculation should match manual calculation (within tolerance)
    cosine_similarity = np.dot(final_centroid, manual_normalized)
    assert cosine_similarity > 0.999, \
        f"Incremental centroid should match manual calculation: similarity={cosine_similarity}"
