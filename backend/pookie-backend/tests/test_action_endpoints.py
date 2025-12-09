"""
Tests for Action API endpoints (Story MVP-3).

Tests CRUD operations, linking to intentions, auth, and user isolation.
"""
import pytest
from fastapi import status


@pytest.fixture
def test_action_data():
    """Sample action data for testing."""
    return {
        "actionText": "Went to gym",
        "timeElapsed": 60
    }


@pytest.fixture
def create_test_action(client, mock_auth_headers, test_user, test_action_data):
    """Create a test action and return its data."""
    response = client.post(
        "/api/v1/actions",
        json=test_action_data,
        headers=mock_auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_test_intention_for_action(client, mock_auth_headers, test_user):
    """Create a test intention for action linking."""
    response = client.post(
        "/api/v1/intentions",
        json={"intentionText": "Get fit"},
        headers=mock_auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


class TestCreateAction:
    def test_create_action_success(self, client, mock_auth_headers, test_user, test_action_data):
        """Create action successfully."""
        response = client.post(
            "/api/v1/actions",
            json=test_action_data,
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["actionText"] == test_action_data["actionText"]
        assert data["timeElapsed"] == test_action_data["timeElapsed"]
        assert "id" in data
        assert "userId" in data
        assert "completedAt" in data
        assert "createdAt" in data

    def test_create_action_with_intentions(self, client, mock_auth_headers, test_user, test_action_data, create_test_intention_for_action):
        """Create action linked to intentions."""
        intention_id = create_test_intention_for_action["id"]
        action_data_with_intentions = {
            **test_action_data,
            "intentionIds": [intention_id]
        }

        response = client.post(
            "/api/v1/actions",
            json=action_data_with_intentions,
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["actionText"] == test_action_data["actionText"]

    def test_create_action_without_auth(self, client, test_action_data):
        """Reject creation without authentication."""
        response = client.post(
            "/api/v1/actions",
            json=test_action_data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_action_empty_text(self, client, mock_auth_headers, test_user):
        """Reject empty action text."""
        response = client.post(
            "/api/v1/actions",
            json={"actionText": "", "timeElapsed": 30},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_action_missing_time(self, client, mock_auth_headers, test_user):
        """Reject action without timeElapsed."""
        response = client.post(
            "/api/v1/actions",
            json={"actionText": "Did something"},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_action_time_negative(self, client, mock_auth_headers, test_user):
        """Reject negative time."""
        response = client.post(
            "/api/v1/actions",
            json={"actionText": "Test", "timeElapsed": -10},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_action_time_too_large(self, client, mock_auth_headers, test_user):
        """Reject time > 360 minutes."""
        response = client.post(
            "/api/v1/actions",
            json={"actionText": "Test", "timeElapsed": 361},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_action_time_boundary_values(self, client, mock_auth_headers, test_user):
        """Accept boundary values 0 and 360."""
        # Min value
        response_min = client.post(
            "/api/v1/actions",
            json={"actionText": "Quick action", "timeElapsed": 0},
            headers=mock_auth_headers
        )
        assert response_min.status_code == status.HTTP_201_CREATED

        # Max value
        response_max = client.post(
            "/api/v1/actions",
            json={"actionText": "Long action", "timeElapsed": 360},
            headers=mock_auth_headers
        )
        assert response_max.status_code == status.HTTP_201_CREATED

    def test_create_action_intention_not_found(self, client, mock_auth_headers, test_user, test_action_data):
        """Reject creation with non-existent intention."""
        action_data_with_intentions = {
            **test_action_data,
            "intentionIds": [999999]
        }

        response = client.post(
            "/api/v1/actions",
            json=action_data_with_intentions,
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestListActions:
    def test_list_actions_empty(self, client, mock_auth_headers, test_user):
        """List actions when none exist."""
        response = client.get(
            "/api/v1/actions",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_actions_with_data(self, client, mock_auth_headers, test_user, create_test_action):
        """List actions with existing data."""
        response = client.get(
            "/api/v1/actions",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(a["id"] == create_test_action["id"] for a in data)

    def test_list_actions_ordered_by_date(self, client, mock_auth_headers, test_user):
        """Actions ordered by completed_at DESC."""
        # Create multiple actions
        action1 = client.post(
            "/api/v1/actions",
            json={"actionText": "First action", "timeElapsed": 10},
            headers=mock_auth_headers
        ).json()

        action2 = client.post(
            "/api/v1/actions",
            json={"actionText": "Second action", "timeElapsed": 20},
            headers=mock_auth_headers
        ).json()

        # List actions
        response = client.get(
            "/api/v1/actions",
            headers=mock_auth_headers
        )

        data = response.json()
        # Most recent should be first (action2 created after action1)
        recent_ids = [a["id"] for a in data[:2]]
        assert action2["id"] in recent_ids

    def test_list_actions_user_isolation(self, client, test_user_token, mock_other_auth_headers, other_user):
        """Users only see their own actions."""
        # User 1 creates action
        response1 = client.post(
            "/api/v1/actions",
            json={"actionText": "User 1 action", "timeElapsed": 30},
            headers=mock_auth_headers
        )
        assert response1.status_code == status.HTTP_201_CREATED

        # User 2 lists actions
        response2 = client.get(
            "/api/v1/actions",
            headers=mock_other_auth_headers
        )
        assert response2.status_code == status.HTTP_200_OK
        data2 = response2.json()
        # User 2 should not see User 1's action
        assert not any(a["actionText"] == "User 1 action" for a in data2)


class TestGetActionDetail:
    def test_get_action_detail_success(self, client, mock_auth_headers, test_user, create_test_action):
        """Get action detail successfully."""
        action_id = create_test_action["id"]

        response = client.get(
            f"/api/v1/actions/{action_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == action_id
        assert data["actionText"] == create_test_action["actionText"]

    def test_get_action_detail_not_found(self, client, mock_auth_headers, test_user):
        """Return 404 for non-existent action."""
        response = client.get(
            "/api/v1/actions/999999",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_action_detail_wrong_user(self, client, test_user_token, mock_other_auth_headers, other_user):
        """Return 404 when accessing another user's action."""
        # User 1 creates action
        response1 = client.post(
            "/api/v1/actions",
            json={"actionText": "User 1 action", "timeElapsed": 45},
            headers=mock_auth_headers
        )
        assert response1.status_code == status.HTTP_201_CREATED
        action_id = response1.json()["id"]

        # User 2 tries to access it
        response2 = client.get(
            f"/api/v1/actions/{action_id}",
            headers=mock_other_auth_headers
        )

        assert response2.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteAction:
    def test_delete_action_success(self, client, mock_auth_headers, test_user, create_test_action):
        """Delete action successfully."""
        action_id = create_test_action["id"]

        response = client.delete(
            f"/api/v1/actions/{action_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        get_response = client.get(
            f"/api/v1/actions/{action_id}",
            headers=mock_auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_action_not_found(self, client, mock_auth_headers, test_user):
        """Return 404 for non-existent action."""
        response = client.delete(
            "/api/v1/actions/999999",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestLinkActionToIntention:
    def test_link_action_to_intention_success(self, client, mock_auth_headers, test_user, create_test_action, create_test_intention_for_action):
        """Link action to intention successfully."""
        action_id = create_test_action["id"]
        intention_id = create_test_intention_for_action["id"]

        response = client.post(
            f"/api/v1/actions/{action_id}/link-intention/{intention_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify link in intention detail view
        intention_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        assert intention_response.status_code == status.HTTP_200_OK
        data = intention_response.json()
        assert len(data["linkedActions"]) >= 1
        assert any(a["id"] == action_id for a in data["linkedActions"])

    def test_link_action_to_intention_duplicate(self, client, mock_auth_headers, test_user, create_test_action, create_test_intention_for_action):
        """Linking same action-intention twice doesn't create duplicate."""
        action_id = create_test_action["id"]
        intention_id = create_test_intention_for_action["id"]

        # Link once
        response1 = client.post(
            f"/api/v1/actions/{action_id}/link-intention/{intention_id}",
            headers=mock_auth_headers
        )
        assert response1.status_code == status.HTTP_204_NO_CONTENT

        # Link again
        response2 = client.post(
            f"/api/v1/actions/{action_id}/link-intention/{intention_id}",
            headers=mock_auth_headers
        )
        assert response2.status_code == status.HTTP_204_NO_CONTENT

        # Verify only one link exists
        intention_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        data = intention_response.json()
        linked_action_ids = [a["id"] for a in data["linkedActions"]]
        assert linked_action_ids.count(action_id) == 1

    def test_link_action_not_found(self, client, mock_auth_headers, test_user, create_test_intention_for_action):
        """Return 404 for non-existent action."""
        intention_id = create_test_intention_for_action["id"]

        response = client.post(
            f"/api/v1/actions/999999/link-intention/{intention_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_link_intention_not_found(self, client, mock_auth_headers, test_user, create_test_action):
        """Return 404 for non-existent intention."""
        action_id = create_test_action["id"]

        response = client.post(
            f"/api/v1/actions/{action_id}/link-intention/999999",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
