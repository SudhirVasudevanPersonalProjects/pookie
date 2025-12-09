"""
Tests for PersonalizedRetrievalService - Hybrid RAG retrieval with centroid re-ranking.

RED phase: These tests will fail until PersonalizedRetrievalService is implemented.
"""

import pytest
from app.services.personalized_retrieval_service import PersonalizedRetrievalService
from unittest.mock import Mock, patch


@pytest.fixture
def service():
    return PersonalizedRetrievalService()


@pytest.fixture
def mock_filter_by_user(service):
    """Auto-patch _filter_by_user to pass through results"""
    with patch.object(service, '_filter_by_user', side_effect=lambda results, *args: results):
        yield


def test_hybrid_scoring_weights_add_to_one():
    """Verify hybrid scoring formula weights sum to 1.0"""
    # Weights: 40% base + 40% centroid + 15% user boost + 5% confidence penalty
    weights = [0.40, 0.40, 0.15, 0.05]
    assert sum(weights) == 1.0


def test_retrieve_and_rerank_basic(service, mock_filter_by_user):
    """Test retrieve_and_rerank returns re-ranked results"""
    # Mock FAISS results (something_id, base_similarity)
    faiss_results = [
        (1, 0.9),  # High base similarity
        (2, 0.8),
        (3, 0.7),
    ]

    # Mock centroid similarities
    # something 1: low centroid match (0.5)
    # something 2: high centroid match (0.95) - should boost to top
    # something 3: medium centroid match (0.6)
    mock_db = Mock()

    with patch.object(service, '_get_centroid_similarities') as mock_centroids:
        mock_centroids.return_value = {
            1: 0.5,
            2: 0.95,  # This should push something 2 to top
            3: 0.6,
        }

        with patch.object(service, '_get_learning_signals') as mock_signals:
            mock_signals.return_value = {
                1: {"is_user_assigned": False, "confidence_score": 0.8},
                2: {"is_user_assigned": False, "confidence_score": 0.8},
                3: {"is_user_assigned": False, "confidence_score": 0.8},
            }

            results = service.retrieve_and_rerank(
                query_embedding=[0.1] * 384,
                user_id="user-123",
                faiss_results=faiss_results,
                db=mock_db,
                top_k=3
            )

    # Something 2 should be first due to high centroid match
    assert len(results) == 3
    assert results[0]["something_id"] == 2  # Centroid boost pushed it to top
    assert "final_score" in results[0]
    assert "base_similarity" in results[0]
    assert "centroid_similarity" in results[0]


def test_user_assignment_boost_applied(service, mock_filter_by_user):
    """Test +0.15 boost when is_user_assigned=True"""
    faiss_results = [(1, 0.7), (2, 0.7)]  # Same base similarity

    mock_db = Mock()

    with patch.object(service, '_get_centroid_similarities') as mock_centroids:
        mock_centroids.return_value = {1: 0.6, 2: 0.6}  # Same centroid similarity

        with patch.object(service, '_get_learning_signals') as mock_signals:
            mock_signals.return_value = {
                1: {"is_user_assigned": True, "confidence_score": None},  # User assigned
                2: {"is_user_assigned": False, "confidence_score": 0.8},
            }

            results = service.retrieve_and_rerank(
                query_embedding=[0.1] * 384,
                user_id="user-123",
                faiss_results=faiss_results,
                db=mock_db,
                top_k=2
            )

    # Something 1 should be first due to user assignment boost
    assert results[0]["something_id"] == 1
    assert results[0]["final_score"] > results[1]["final_score"]


def test_confidence_penalty_applied(service, mock_filter_by_user):
    """Test -0.05 penalty when confidence_score < 0.5"""
    faiss_results = [(1, 0.7), (2, 0.7)]

    mock_db = Mock()

    with patch.object(service, '_get_centroid_similarities') as mock_centroids:
        mock_centroids.return_value = {1: 0.6, 2: 0.6}

        with patch.object(service, '_get_learning_signals') as mock_signals:
            mock_signals.return_value = {
                1: {"is_user_assigned": False, "confidence_score": 0.3},  # Low confidence
                2: {"is_user_assigned": False, "confidence_score": 0.8},  # High confidence
            }

            results = service.retrieve_and_rerank(
                query_embedding=[0.1] * 384,
                user_id="user-123",
                faiss_results=faiss_results,
                db=mock_db,
                top_k=2
            )

    # Something 2 should be first due to confidence penalty on something 1
    assert results[0]["something_id"] == 2


def test_fallback_no_circles(service, mock_filter_by_user):
    """Test graceful fallback when user has no circles"""
    faiss_results = [(1, 0.9), (2, 0.8), (3, 0.7)]

    mock_db = Mock()

    with patch.object(service, '_get_centroid_similarities') as mock_centroids:
        mock_centroids.return_value = {}  # No circles

        with patch.object(service, '_get_learning_signals') as mock_signals:
            mock_signals.return_value = {}

            results = service.retrieve_and_rerank(
                query_embedding=[0.1] * 384,
                user_id="user-123",
                faiss_results=faiss_results,
                db=mock_db,
                top_k=3
            )

    # Should fall back to FAISS ordering
    # Formula with no circles: 0.40 * base + 0.40 * 0 + 0 - 0 = 0.40*base
    assert len(results) == 3
    assert results[0]["something_id"] == 1  # Highest FAISS score
    # Expected: 0.40 * 0.9 = 0.36
    assert abs(results[0]["final_score"] - 0.36) < 0.01


def test_top_k_limit_respected(service, mock_filter_by_user):
    """Test top_k parameter limits results"""
    faiss_results = [(i, 0.9 - i * 0.1) for i in range(1, 11)]  # 10 results

    mock_db = Mock()

    with patch.object(service, '_get_centroid_similarities') as mock_centroids:
        mock_centroids.return_value = {i: 0.5 for i in range(1, 11)}

        with patch.object(service, '_get_learning_signals') as mock_signals:
            mock_signals.return_value = {
                i: {"is_user_assigned": False, "confidence_score": 0.8}
                for i in range(1, 11)
            }

            results = service.retrieve_and_rerank(
                query_embedding=[0.1] * 384,
                user_id="user-123",
                faiss_results=faiss_results,
                db=mock_db,
                top_k=5
            )

    assert len(results) == 5


def test_format_rag_context_with_circles(service):
    """Test RAG context formatting includes somethings, meanings, and circles"""
    from app.models.something import Something
    from app.models.circle import Circle

    # Create mock somethings with circles
    mock_circle1 = Mock()
    mock_circle1.circle_name = "Fitness"

    mock_circle2 = Mock()
    mock_circle2.circle_name = "Career"

    mock_sc1 = Mock()
    mock_sc1.circle = mock_circle1

    mock_sc2 = Mock()
    mock_sc2.circle = mock_circle2

    mock_something1 = Mock()
    mock_something1.id = 1
    mock_something1.content = "I want to get stronger"
    mock_something1.meaning = "Desire for physical fitness"
    mock_something1.circles = [mock_sc1]

    mock_something2 = Mock()
    mock_something2.id = 2
    mock_something2.content = "Need to practice presentation"
    mock_something2.meaning = "Career development goal"
    mock_something2.circles = [mock_sc2]

    mock_db = Mock()
    mock_query = Mock()
    mock_query.filter.return_value.all.return_value = [mock_something1, mock_something2]
    mock_db.query.return_value = mock_query

    context = service.format_rag_context([1, 2], mock_db)

    assert "From your saved somethings" in context
    assert "I want to get stronger" in context
    assert "Desire for physical fitness" in context
    assert "[Circle: Fitness]" in context
    assert "Need to practice presentation" in context
    assert "[Circle: Career]" in context
    assert "you care about" in context.lower()


def test_format_rag_context_no_circles(service):
    """Test RAG context formatting handles somethings without circles"""
    mock_something = Mock()
    mock_something.id = 1
    mock_something.content = "Random thought"
    mock_something.meaning = None
    mock_something.circles = []

    mock_db = Mock()
    mock_query = Mock()
    mock_query.filter.return_value.all.return_value = [mock_something]
    mock_db.query.return_value = mock_query

    context = service.format_rag_context([1], mock_db)

    assert "Random thought" in context
    assert "[Circle: Uncategorized]" in context
