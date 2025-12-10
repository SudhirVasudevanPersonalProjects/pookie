"""
Tests for Intention API endpoints (Story MVP-3).

Tests CRUD operations, linking/unlinking somethings, auth, and user isolation.
"""
import pytest
from fastapi import status
from uuid import UUID


@pytest.fixture
def test_intention_data():
    """Sample intention data for testing."""
    return {"intentionText": "Exercise 3x per week"}


@pytest.fixture
def create_test_intention_via_api(client, mock_auth_headers, test_user, test_intention_data):
    """Create a test intention via API and return its JSON data."""
    response = client.post(
        "/api/v1/intentions",
        json=test_intention_data,
        headers=mock_auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_test_something(client, mock_auth_headers, test_user):
    """Create a test something and return its data."""
    response = client.post(
        "/api/v1/somethings",
        json={"content": "I want to be healthy", "contentType": "text"},
        headers=mock_auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


class TestCreateIntention:
    def test_create_intention_success(self, client, mock_auth_headers, test_user, test_intention_data):
        """Create intention successfully."""
        response = client.post(
            "/api/v1/intentions",
            json=test_intention_data,
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["intentionText"] == test_intention_data["intentionText"]
        assert data["status"] == "active"
        assert "id" in data
        assert "userId" in data
        assert "createdAt" in data
        assert "updatedAt" in data

    def test_create_intention_without_auth(self, client, test_intention_data):
        """Reject creation without authentication."""
        response = client.post(
            "/api/v1/intentions",
            json=test_intention_data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_intention_empty_text(self, client, mock_auth_headers, test_user):
        """Reject empty intention text."""
        response = client.post(
            "/api/v1/intentions",
            json={"intentionText": ""},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_intention_text_too_long(self, client, mock_auth_headers, test_user):
        """Reject intention text > 500 chars."""
        long_text = "x" * 501
        response = client.post(
            "/api/v1/intentions",
            json={"intentionText": long_text},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListIntentions:
    def test_list_intentions_empty(self, client, mock_auth_headers, test_user):
        """List intentions when none exist."""
        response = client.get(
            "/api/v1/intentions",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_intentions_with_data(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """List intentions with existing data."""
        response = client.get(
            "/api/v1/intentions",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(i["id"] == create_test_intention_via_api["id"] for i in data)

    def test_list_intentions_user_isolation(self, client, test_user, create_test_intention, mock_other_auth_headers, other_user):
        """Users only see their own intentions."""
        # User 1 has an intention (created directly in DB)
        test_user_intention = create_test_intention(
            user_id=test_user.id,
            intention_text="User 1 intention"
        )

        # User 2 lists their intentions
        response = client.get(
            "/api/v1/intentions",
            headers=mock_other_auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # User 2 should not see User 1's intention
        assert not any(i["intentionText"] == "User 1 intention" for i in data)


class TestGetIntentionDetail:
    def test_get_intention_detail_success(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """Get intention detail successfully."""
        intention_id = create_test_intention_via_api["id"]

        response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == intention_id
        assert "linkedSomethings" in data
        assert "linkedActions" in data
        assert isinstance(data["linkedSomethings"], list)
        assert isinstance(data["linkedActions"], list)

    def test_get_intention_detail_not_found(self, client, mock_auth_headers, test_user):
        """Return 404 for non-existent intention."""
        response = client.get(
            "/api/v1/intentions/999999",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_intention_detail_wrong_user(self, client, test_user, create_test_intention, mock_other_auth_headers, other_user):
        """Return 404 when accessing another user's intention."""
        # User 1 has an intention (created directly in DB)
        test_user_intention = create_test_intention(
            user_id=test_user.id,
            intention_text="User 1 intention"
        )

        # User 2 tries to access it
        response = client.get(
            f"/api/v1/intentions/{test_user_intention.id}",
            headers=mock_other_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateIntention:
    def test_update_intention_text(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """Update intention text."""
        intention_id = create_test_intention_via_api["id"]

        response = client.put(
            f"/api/v1/intentions/{intention_id}",
            json={"intentionText": "Updated text"},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["intentionText"] == "Updated text"

    def test_update_intention_status(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """Update intention status."""
        intention_id = create_test_intention_via_api["id"]

        response = client.put(
            f"/api/v1/intentions/{intention_id}",
            json={"status": "completed"},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "completed"

    def test_update_intention_both(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """Update both text and status."""
        intention_id = create_test_intention_via_api["id"]

        response = client.put(
            f"/api/v1/intentions/{intention_id}",
            json={"intentionText": "New text", "status": "archived"},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["intentionText"] == "New text"
        assert data["status"] == "archived"

    def test_update_intention_not_found(self, client, mock_auth_headers, test_user):
        """Return 404 for non-existent intention."""
        response = client.put(
            "/api/v1/intentions/999999",
            json={"intentionText": "New text"},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteIntention:
    def test_delete_intention_success(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """Delete intention successfully."""
        intention_id = create_test_intention_via_api["id"]

        response = client.delete(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        get_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_intention_not_found(self, client, mock_auth_headers, test_user):
        """Return 404 for non-existent intention."""
        response = client.delete(
            "/api/v1/intentions/999999",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestLinkCaresToIntention:
    def test_link_cares_success(self, client, mock_auth_headers, test_user, create_test_intention_via_api, create_test_something):
        """Link somethings to intention successfully."""
        intention_id = create_test_intention_via_api["id"]
        something_id = create_test_something["id"]

        response = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify link in detail view
        detail_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        assert detail_response.status_code == status.HTTP_200_OK
        data = detail_response.json()
        assert len(data["linkedSomethings"]) == 1
        assert data["linkedSomethings"][0]["id"] == something_id

    def test_link_cares_duplicate(self, client, mock_auth_headers, test_user, create_test_intention_via_api, create_test_something):
        """Linking same something twice doesn't create duplicate."""
        intention_id = create_test_intention_via_api["id"]
        something_id = create_test_something["id"]

        # Link once
        response1 = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )
        assert response1.status_code == status.HTTP_204_NO_CONTENT

        # Link again
        response2 = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )
        assert response2.status_code == status.HTTP_204_NO_CONTENT

        # Verify only one link exists
        detail_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        data = detail_response.json()
        assert len(data["linkedSomethings"]) == 1

    def test_link_cares_not_found_intention(self, client, mock_auth_headers, test_user, create_test_something):
        """Return 404 for non-existent intention."""
        something_id = create_test_something["id"]

        response = client.post(
            "/api/v1/intentions/999999/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_link_cares_not_found_something(self, client, mock_auth_headers, test_user, create_test_intention_via_api):
        """Return 404 for non-existent something."""
        intention_id = create_test_intention_via_api["id"]

        response = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [999999]},
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUnlinkCareFromIntention:
    def test_unlink_care_success(self, client, mock_auth_headers, test_user, create_test_intention_via_api, create_test_something):
        """Unlink something from intention successfully."""
        intention_id = create_test_intention_via_api["id"]
        something_id = create_test_something["id"]

        # Link first
        link_response = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )
        assert link_response.status_code == status.HTTP_204_NO_CONTENT

        # Unlink
        unlink_response = client.delete(
            f"/api/v1/intentions/{intention_id}/unlink-care/{something_id}",
            headers=mock_auth_headers
        )
        assert unlink_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify unlinked
        detail_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        data = detail_response.json()
        assert len(data["linkedSomethings"]) == 0

    def test_unlink_care_idempotent(self, client, mock_auth_headers, test_user, create_test_intention_via_api, create_test_something):
        """Unlinking non-existent link is idempotent."""
        intention_id = create_test_intention_via_api["id"]
        something_id = create_test_something["id"]

        # Unlink without linking first (should succeed)
        response = client.delete(
            f"/api/v1/intentions/{intention_id}/unlink-care/{something_id}",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_unlink_care_intention_not_found(self, client, mock_auth_headers, test_user):
        """Return 404 for non-existent intention."""
        response = client.delete(
            "/api/v1/intentions/999999/unlink-care/1",
            headers=mock_auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
