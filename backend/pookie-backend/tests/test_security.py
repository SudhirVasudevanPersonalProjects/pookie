"""
Tests for JWT authentication and security middleware.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_supabase():
    """Fixture to mock Supabase client."""
    with patch('app.core.security.get_supabase_client') as mock:
        yield mock


def test_health_check_no_auth_required():
    """Test that basic health check endpoint doesn't require authentication."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_protected_endpoint_without_auth():
    """Test that protected endpoint returns 401 without Authorization header."""
    response = client.get("/api/v1/protected")
    assert response.status_code == 401
    assert "detail" in response.json()


def test_protected_endpoint_with_invalid_token():
    """Test that invalid token returns 401."""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/api/v1/protected", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_protected_endpoint_with_valid_token(mock_supabase):
    """Test that valid token returns 200 with user data."""
    # Mock Supabase client and auth response
    mock_client = Mock()
    mock_user_obj = MagicMock()
    mock_user_obj.id = "test-uuid-123"
    mock_user_obj.email = "test@example.com"

    mock_client.auth.get_user.return_value = mock_user_obj
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer valid_test_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Authenticated"
    assert response.json()["user_id"] == "test-uuid-123"

    # Verify Supabase was called with the token
    mock_client.auth.get_user.assert_called_once_with("valid_test_token")


def test_protected_endpoint_with_dict_user_response(mock_supabase):
    """Test handling of dict-format user response from Supabase SDK."""
    # Mock Supabase client
    mock_client = Mock()
    mock_user_dict = {
        "id": "dict-uuid-456",
        "email": "dictuser@example.com",
        "aud": "authenticated"
    }

    mock_client.auth.get_user.return_value = mock_user_dict
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer valid_dict_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 200
    assert response.json()["user_id"] == "dict-uuid-456"


def test_protected_endpoint_with_nested_user_response(mock_supabase):
    """Test handling of nested user object (user.user.id pattern)."""
    # Mock Supabase client
    mock_client = Mock()
    mock_response = {
        "user": {
            "id": "nested-uuid-789",
            "email": "nested@example.com"
        }
    }

    mock_client.auth.get_user.return_value = mock_response
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer valid_nested_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 200
    assert response.json()["user_id"] == "nested-uuid-789"


def test_protected_endpoint_supabase_error(mock_supabase):
    """Test that Supabase errors are properly handled and return 401."""
    # Mock Supabase client
    mock_client = Mock()
    mock_client.auth.get_user.side_effect = Exception("JWT verification failed")
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer error_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_protected_endpoint_malformed_auth_header():
    """Test that malformed Authorization header returns 401."""
    # Missing "Bearer" prefix
    headers = {"Authorization": "just_a_token"}
    response = client.get("/api/v1/protected", headers=headers)
    assert response.status_code == 401

    # Empty Authorization header
    headers = {"Authorization": ""}
    response = client.get("/api/v1/protected", headers=headers)
    assert response.status_code == 401


def test_protected_endpoint_attribute_error(mock_supabase):
    """Test that AttributeError (config issue) returns 500."""
    # Mock Supabase client
    mock_client = Mock()
    mock_client.auth.get_user.side_effect = AttributeError("'NoneType' object has no attribute 'auth'")
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer config_error_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 500
    assert "configuration error" in response.json()["detail"].lower()


def test_protected_endpoint_value_error(mock_supabase):
    """Test that ValueError (invalid token format) returns 401."""
    # Mock Supabase client
    mock_client = Mock()
    mock_client.auth.get_user.side_effect = ValueError("Invalid token format")
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer malformed_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_extract_user_id_failure(mock_supabase):
    """Test that failure to extract user ID returns 500."""
    # Mock Supabase client with invalid user object (empty dict, no id)
    mock_client = Mock()
    mock_client.auth.get_user.return_value = {}  # Empty dict, no id
    mock_supabase.return_value = mock_client

    headers = {"Authorization": "Bearer no_id_token"}
    response = client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 500
    assert "extract user information" in response.json()["detail"].lower()
