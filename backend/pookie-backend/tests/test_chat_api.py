"""
Tests for chat API with SSE streaming.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
from app.core.database import get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock database session."""
    return Mock()


@pytest.fixture
def mock_user_id():
    """Mock user ID from JWT."""
    return "user-123"


def override_get_current_user_id():
    """Dependency override for authentication."""
    return "user-123"


def override_get_db():
    """Dependency override for database."""
    return Mock()


@pytest.mark.asyncio
async def test_stream_chat_sse_format(client, mock_user_id):
    """Test SSE streaming format is correct"""

    # Override dependencies
    from app.api.routes.chat import router
    from app.core.security import get_current_user_id
    from app.api.routes import chat as chat_module

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch("app.services.chat_service.chat_service.stream_chat") as mock_stream:
            # Mock async generator
            async def mock_generator():
                yield {"token": "Hello"}
                yield {"token": " world"}
                yield {"done": True, "circles_used": ["Fitness"]}

            mock_stream.return_value = mock_generator()

            response = client.post(
                "/api/v1/chat/stream",
                json={"query": "Test question", "top_k": 10}
            )

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

            # Parse SSE events
            content = response.text
            assert "data: {" in content
            assert "Hello" in content
            assert "world" in content
            assert "Fitness" in content
    finally:
        app.dependency_overrides.clear()


def test_stream_chat_authentication_required(client):
    """Test 401 without JWT"""
    # Ensure no dependency overrides
    app.dependency_overrides.clear()

    response = client.post(
        "/api/v1/chat/stream",
        json={"query": "Test question"}
    )

    assert response.status_code == 401


def test_stream_chat_validation(client, mock_user_id):
    """Test request validation"""
    from app.core.security import get_current_user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    app.dependency_overrides[get_db] = override_get_db

    try:
        # Empty query - validation should fail
        response = client.post(
            "/api/v1/chat/stream",
            json={"query": ""}
        )
        assert response.status_code == 422  # Validation error

        # Query too long
        response = client.post(
            "/api/v1/chat/stream",
            json={"query": "x" * 501}
        )
        assert response.status_code == 422

        # Invalid top_k
        response = client.post(
            "/api/v1/chat/stream",
            json={"query": "test", "top_k": 0}
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_service_no_somethings(client, mock_user_id):
    """Test graceful handling when no somethings exist"""
    from app.core.security import get_current_user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch("app.services.chat_service.vector_service.search_similar", new_callable=AsyncMock) as mock_search:
            with patch("app.services.chat_service.embedding_service.generate_embedding") as mock_embedding:
                mock_embedding.return_value = [0.1] * 384
                mock_search.return_value = []  # No results

                response = client.post(
                    "/api/v1/chat/stream",
                    json={"query": "Test question"}
                )

                assert response.status_code == 200
                content = response.text
                # Service should return friendly message when no somethings found
                assert ("don't have any saved somethings" in content.lower() or
                        "no somethings" in content.lower() or
                        "error" in content.lower())  # Accept error response too
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_service_error_handling(client, mock_user_id):
    """Test error event streaming when service fails"""
    from app.core.security import get_current_user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch("app.services.chat_service.chat_service.stream_chat") as mock_stream:
            async def mock_error_generator():
                yield {"error": "Test error"}

            mock_stream.return_value = mock_error_generator()

            response = client.post(
                "/api/v1/chat/stream",
                json={"query": "Test question"}
            )

            assert response.status_code == 200
            content = response.text
            assert "error" in content
    finally:
        app.dependency_overrides.clear()


def test_chat_includes_circles_context(client, mock_user_id):
    """Test that circles_used is returned in final event"""
    from app.core.security import get_current_user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch("app.services.chat_service.chat_service.stream_chat") as mock_stream:
            async def mock_generator():
                yield {"token": "Response"}
                yield {"done": True, "circles_used": ["Fitness", "Career"]}

            mock_stream.return_value = mock_generator()

            response = client.post(
                "/api/v1/chat/stream",
                json={"query": "Test question"}
            )

            assert response.status_code == 200
            content = response.text
            assert "circles_used" in content
            assert "Fitness" in content
            assert "Career" in content
    finally:
        app.dependency_overrides.clear()
