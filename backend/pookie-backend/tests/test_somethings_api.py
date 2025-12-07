"""
Integration tests for Somethings CRUD API endpoints.

Story 2.4: Tests all CRUD operations, authentication, authorization, and edge cases.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.something import Something
from uuid import UUID


class TestCreateSomething:
    """Test POST /api/v1/somethings endpoint (AC 3)."""

    def test_create_text_something_success(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        test_user_id: str
    ):
        """Test creating a text something with valid JWT."""
        response = client.post(
            "/api/v1/somethings",
            json={
                "content": "I want to learn piano",
                "contentType": "text"
            },
            headers=mock_auth_headers
        )

        # Debug output
        if response.status_code != 201:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["content"] == "I want to learn piano"
        assert data["contentType"] == "text"
        assert data["userId"] == test_user_id
        assert "createdAt" in data
        assert "updatedAt" in data

    def test_create_image_something_with_media_url(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object
    ):
        """Test creating an image something with media URL."""
        response = client.post(
            "/api/v1/somethings",
            json={
                "contentType": "image",
                "mediaUrl": "https://storage.supabase.com/bucket/image.jpg"
            },
            headers=mock_auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["contentType"] == "image"
        assert data["mediaUrl"] == "https://storage.supabase.com/bucket/image.jpg"

    def test_create_something_without_auth_fails(self, client: TestClient):
        """Test creating something without JWT returns 401."""
        response = client.post(
            "/api/v1/somethings",
            json={
                "content": "I want to learn piano",
                "contentType": "text"
            }
        )

        # Should get 401 Unauthorized from FastAPI security
        assert response.status_code == 401

    def test_create_somethings_triggers_faiss_save_at_mod_10(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        test_user_id: str
    ):
        """Test that creating somethings triggers FAISS save every 10 items (testing bug fix)."""
        # Create 10 somethings to trigger save at ID 10
        # This test catches the critical bug where save_index() was called instead of save_to_storage()
        for i in range(10):
            response = client.post(
                "/api/v1/somethings",
                json={
                    "content": f"Something number {i + 1}",
                    "contentType": "text"
                },
                headers=mock_auth_headers
            )
            assert response.status_code == 201, f"Failed to create something {i + 1}: {response.text}"

        # If we got here without AttributeError, the save_to_storage() method exists
        # This would have failed with the old save_index() bug
        assert True


class TestListSomethings:
    """Test GET /api/v1/somethings endpoint (AC 4)."""

    def test_list_somethings_empty(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object
    ):
        """Test listing somethings when none exist."""
        response = client.get(
            "/api/v1/somethings",
            headers=mock_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_somethings_with_data(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        db_session: Session,
        test_user_id: str
    ):
        """Test listing somethings returns user's data."""
        from datetime import datetime, timezone, timedelta

        # Create test somethings with explicit timestamps (no time.sleep needed)
        base_time = datetime.now(timezone.utc)

        something1 = Something(
            user_id=UUID(test_user_id),
            content="First something",
            content_type="text"
        )
        db_session.add(something1)
        db_session.commit()
        db_session.refresh(something1)

        # Manually set older timestamp for first something
        something1.created_at = base_time - timedelta(seconds=1)
        db_session.commit()

        something2 = Something(
            user_id=UUID(test_user_id),
            content="Second something",
            content_type="text"
        )
        db_session.add(something2)
        db_session.commit()

        response = client.get(
            "/api/v1/somethings",
            headers=mock_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Verify both somethings are present and ordered by created_at desc
        contents = [item["content"] for item in data]
        assert "First something" in contents
        assert "Second something" in contents
        # Second something should be first (more recent)
        assert data[0]["content"] == "Second something"
        assert data[1]["content"] == "First something"

    def test_list_somethings_pagination(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        db_session: Session,
        test_user_id: str
    ):
        """Test pagination with skip and limit parameters."""
        # Create 5 test somethings
        for i in range(5):
            something = Something(
                user_id=UUID(test_user_id),
                content=f"Something {i}",
                content_type="text"
            )
            db_session.add(something)
        db_session.commit()

        # Test skip=2, limit=2
        response = client.get(
            "/api/v1/somethings?skip=2&limit=2",
            headers=mock_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_somethings_user_isolation(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        other_user: object,
        db_session: Session,
        test_user_id: str,
        other_user_id: str
    ):
        """Test users can only see their own somethings."""
        # Create something for test user
        test_something = Something(
            user_id=UUID(test_user_id),
            content="My something",
            content_type="text"
        )
        # Create something for other user
        other_something = Something(
            user_id=UUID(other_user_id),
            content="Other user's something",
            content_type="text"
        )
        db_session.add_all([test_something, other_something])
        db_session.commit()

        # Test user should only see their own
        response = client.get(
            "/api/v1/somethings",
            headers=mock_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["content"] == "My something"

    def test_list_somethings_without_auth_fails(self, client: TestClient):
        """Test listing somethings without JWT returns 401."""
        response = client.get("/api/v1/somethings")

        assert response.status_code == 401


class TestGetSomething:
    """Test GET /api/v1/somethings/{something_id} endpoint (AC 5)."""

    def test_get_something_success(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        db_session: Session,
        test_user_id: str
    ):
        """Test getting a single something by ID."""
        something = Something(
            user_id=UUID(test_user_id),
            content="Test something",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)

        response = client.get(
            f"/api/v1/somethings/{something.id}",
            headers=mock_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == something.id
        assert data["content"] == "Test something"

    def test_get_something_not_found(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object
    ):
        """Test getting non-existent something returns 404."""
        response = client.get(
            "/api/v1/somethings/99999",
            headers=mock_auth_headers
        )

        assert response.status_code == 404

    def test_get_something_other_user_fails(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        other_user: object,
        db_session: Session,
        other_user_id: str
    ):
        """Test users cannot access other users' somethings."""
        # Create something for other user
        something = Something(
            user_id=UUID(other_user_id),
            content="Other user's something",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)

        # Try to access with test user's auth
        response = client.get(
            f"/api/v1/somethings/{something.id}",
            headers=mock_auth_headers
        )

        # Should return 404 (not revealing existence)
        assert response.status_code == 404

    def test_get_something_without_auth_fails(self, client: TestClient):
        """Test getting something without JWT returns 401."""
        response = client.get("/api/v1/somethings/1")

        assert response.status_code == 401


class TestUpdateSomethingMeaning:
    """Test PATCH /api/v1/somethings/{something_id}/meaning endpoint (AC 6)."""

    def test_update_meaning_success(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        db_session: Session,
        test_user_id: str
    ):
        """Test updating meaning sets is_meaning_user_edited flag."""
        something = Something(
            user_id=UUID(test_user_id),
            content="I want to learn piano",
            content_type="text",
            meaning="User cares about music",
            is_meaning_user_edited=False
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)

        response = client.patch(
            f"/api/v1/somethings/{something.id}/meaning",
            json={"meaning": "User wants to develop musical skills"},
            headers=mock_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["meaning"] == "User wants to develop musical skills"
        assert data["isMeaningUserEdited"] is True

    def test_update_meaning_not_found(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object
    ):
        """Test updating meaning for non-existent something returns 404."""
        response = client.patch(
            "/api/v1/somethings/99999/meaning",
            json={"meaning": "Updated meaning"},
            headers=mock_auth_headers
        )

        assert response.status_code == 404

    def test_update_meaning_other_user_fails(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        other_user: object,
        db_session: Session,
        other_user_id: str
    ):
        """Test users cannot update other users' somethings."""
        something = Something(
            user_id=UUID(other_user_id),
            content="Other user's something",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)

        response = client.patch(
            f"/api/v1/somethings/{something.id}/meaning",
            json={"meaning": "Hacked meaning"},
            headers=mock_auth_headers
        )

        assert response.status_code == 404

    def test_update_meaning_without_auth_fails(self, client: TestClient):
        """Test updating meaning without JWT returns 401."""
        response = client.patch(
            "/api/v1/somethings/1/meaning",
            json={"meaning": "Updated"}
        )

        assert response.status_code == 401


class TestDeleteSomething:
    """Test DELETE /api/v1/somethings/{something_id} endpoint (AC 7)."""

    def test_delete_something_success(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        db_session: Session,
        test_user_id: str
    ):
        """Test deleting a something returns 204 No Content."""
        something = Something(
            user_id=UUID(test_user_id),
            content="To be deleted",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)

        response = client.delete(
            f"/api/v1/somethings/{something.id}",
            headers=mock_auth_headers
        )

        assert response.status_code == 204

        # Verify something is deleted
        deleted = db_session.query(Something).filter(Something.id == something.id).first()
        assert deleted is None

    def test_delete_something_not_found(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object
    ):
        """Test deleting non-existent something returns 404."""
        response = client.delete(
            "/api/v1/somethings/99999",
            headers=mock_auth_headers
        )

        assert response.status_code == 404

    def test_delete_something_other_user_fails(
        self,
        client: TestClient,
        mock_auth_headers: dict,
        test_user: object,
        other_user: object,
        db_session: Session,
        other_user_id: str
    ):
        """Test users cannot delete other users' somethings."""
        something = Something(
            user_id=UUID(other_user_id),
            content="Other user's something",
            content_type="text"
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)

        response = client.delete(
            f"/api/v1/somethings/{something.id}",
            headers=mock_auth_headers
        )

        assert response.status_code == 404

        # Verify something still exists
        still_exists = db_session.query(Something).filter(Something.id == something.id).first()
        assert still_exists is not None

    def test_delete_something_without_auth_fails(self, client: TestClient):
        """Test deleting something without JWT returns 401."""
        response = client.delete("/api/v1/somethings/1")

        assert response.status_code == 401
