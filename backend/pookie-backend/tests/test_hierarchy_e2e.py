"""
End-to-end tests for hierarchy: Something → Intention → Action (Story MVP-3).

Tests the complete flow of creating and linking entities across the hierarchy.
"""
import pytest
from fastapi import status


class TestHierarchyE2E:
    def test_full_hierarchy_flow(self, client, mock_auth_headers, test_user):
        """
        Test complete hierarchy flow:
        1. Create something (capture)
        2. Create intention (goal)
        3. Link something to intention (what I care about)
        4. Create action (what I did)
        5. Link action to intention (fulfillment)
        6. Verify hierarchy in detail views
        """
        # 1. Create something
        something_response = client.post(
            "/api/v1/somethings",
            json={"content": "I want to be healthy", "contentType": "text"},
            headers=mock_auth_headers
        )
        assert something_response.status_code == status.HTTP_201_CREATED
        something_id = something_response.json()["id"]

        # 2. Create intention
        intention_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Exercise 3x per week"},
            headers=mock_auth_headers
        )
        assert intention_response.status_code == status.HTTP_201_CREATED
        intention_id = intention_response.json()["id"]

        # 3. Link something to intention
        link_care_response = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )
        assert link_care_response.status_code == status.HTTP_204_NO_CONTENT

        # 4. Create action
        action_response = client.post(
            "/api/v1/actions",
            json={"actionText": "Went to gym", "timeElapsed": 60},
            headers=mock_auth_headers
        )
        assert action_response.status_code == status.HTTP_201_CREATED
        action_id = action_response.json()["id"]

        # 5. Link action to intention
        link_action_response = client.post(
            f"/api/v1/actions/{action_id}/link-intention/{intention_id}",
            headers=mock_auth_headers
        )
        assert link_action_response.status_code == status.HTTP_204_NO_CONTENT

        # 6. Verify hierarchy in intention detail view
        intention_detail_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        assert intention_detail_response.status_code == status.HTTP_200_OK
        intention_data = intention_detail_response.json()

        # Verify linked something
        assert len(intention_data["linkedSomethings"]) == 1
        assert intention_data["linkedSomethings"][0]["id"] == something_id
        assert intention_data["linkedSomethings"][0]["content"] == "I want to be healthy"

        # Verify linked action
        assert len(intention_data["linkedActions"]) == 1
        assert intention_data["linkedActions"][0]["id"] == action_id
        assert intention_data["linkedActions"][0]["actionText"] == "Went to gym"
        assert intention_data["linkedActions"][0]["timeElapsed"] == 60

    def test_create_action_with_intention_link_in_one_call(self, client, mock_auth_headers, test_user):
        """
        Test creating action with intention link in a single API call.
        """
        # 1. Create intention
        intention_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Learn to code"},
            headers=mock_auth_headers
        )
        assert intention_response.status_code == status.HTTP_201_CREATED
        intention_id = intention_response.json()["id"]

        # 2. Create action with intention link
        action_response = client.post(
            "/api/v1/actions",
            json={
                "actionText": "Completed tutorial",
                "timeElapsed": 90,
                "intentionIds": [intention_id]
            },
            headers=mock_auth_headers
        )
        assert action_response.status_code == status.HTTP_201_CREATED
        action_id = action_response.json()["id"]

        # 3. Verify link exists
        intention_detail_response = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        intention_data = intention_detail_response.json()
        assert len(intention_data["linkedActions"]) == 1
        assert intention_data["linkedActions"][0]["id"] == action_id

    def test_action_fulfills_multiple_intentions(self, client, mock_auth_headers, test_user):
        """
        Test that one action can fulfill multiple intentions.
        """
        # Create two intentions
        intention1_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Get fit"},
            headers=mock_auth_headers
        )
        intention1_id = intention1_response.json()["id"]

        intention2_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Train for marathon"},
            headers=mock_auth_headers
        )
        intention2_id = intention2_response.json()["id"]

        # Create action linked to both intentions
        action_response = client.post(
            "/api/v1/actions",
            json={
                "actionText": "30 minute run",
                "timeElapsed": 30,
                "intentionIds": [intention1_id, intention2_id]
            },
            headers=mock_auth_headers
        )
        assert action_response.status_code == status.HTTP_201_CREATED
        action_id = action_response.json()["id"]

        # Verify action appears in both intentions
        intention1_detail = client.get(
            f"/api/v1/intentions/{intention1_id}",
            headers=mock_auth_headers
        ).json()
        assert any(a["id"] == action_id for a in intention1_detail["linkedActions"])

        intention2_detail = client.get(
            f"/api/v1/intentions/{intention2_id}",
            headers=mock_auth_headers
        ).json()
        assert any(a["id"] == action_id for a in intention2_detail["linkedActions"])

    def test_intention_linked_to_multiple_somethings(self, client, mock_auth_headers, test_user):
        """
        Test that one intention can be linked to multiple somethings.
        """
        # Create multiple somethings
        something1_response = client.post(
            "/api/v1/somethings",
            json={"content": "I want abs", "contentType": "text"},
            headers=mock_auth_headers
        )
        something1_id = something1_response.json()["id"]

        something2_response = client.post(
            "/api/v1/somethings",
            json={"content": "Gym motivation", "contentType": "text"},
            headers=mock_auth_headers
        )
        something2_id = something2_response.json()["id"]

        # Create intention
        intention_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Get fit"},
            headers=mock_auth_headers
        )
        intention_id = intention_response.json()["id"]

        # Link both somethings to intention
        link_response = client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something1_id, something2_id]},
            headers=mock_auth_headers
        )
        assert link_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify both somethings linked
        intention_detail = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        ).json()
        assert len(intention_detail["linkedSomethings"]) == 2
        linked_ids = {s["id"] for s in intention_detail["linkedSomethings"]}
        assert something1_id in linked_ids
        assert something2_id in linked_ids

    def test_cascade_delete_intention_preserves_somethings_and_actions(self, client, mock_auth_headers, test_user):
        """
        Test that deleting intention removes links but preserves somethings and actions.
        """
        # Create something
        something_response = client.post(
            "/api/v1/somethings",
            json={"content": "Test something", "contentType": "text"},
            headers=mock_auth_headers
        )
        something_id = something_response.json()["id"]

        # Create intention
        intention_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Test intention"},
            headers=mock_auth_headers
        )
        intention_id = intention_response.json()["id"]

        # Link something to intention
        client.post(
            f"/api/v1/intentions/{intention_id}/link-cares",
            json={"somethingIds": [something_id]},
            headers=mock_auth_headers
        )

        # Create action linked to intention
        action_response = client.post(
            "/api/v1/actions",
            json={
                "actionText": "Test action",
                "timeElapsed": 15,
                "intentionIds": [intention_id]
            },
            headers=mock_auth_headers
        )
        action_id = action_response.json()["id"]

        # Delete intention
        delete_response = client.delete(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify something still exists
        something_check = client.get(
            f"/api/v1/somethings/{something_id}",
            headers=mock_auth_headers
        )
        assert something_check.status_code == status.HTTP_200_OK

        # Verify action still exists
        action_check = client.get(
            f"/api/v1/actions/{action_id}",
            headers=mock_auth_headers
        )
        assert action_check.status_code == status.HTTP_200_OK

    def test_cascade_delete_action_preserves_intentions(self, client, mock_auth_headers, test_user):
        """
        Test that deleting action removes links but preserves intentions.
        """
        # Create intention
        intention_response = client.post(
            "/api/v1/intentions",
            json={"intentionText": "Test intention"},
            headers=mock_auth_headers
        )
        intention_id = intention_response.json()["id"]

        # Create action linked to intention
        action_response = client.post(
            "/api/v1/actions",
            json={
                "actionText": "Test action",
                "timeElapsed": 20,
                "intentionIds": [intention_id]
            },
            headers=mock_auth_headers
        )
        action_id = action_response.json()["id"]

        # Delete action
        delete_response = client.delete(
            f"/api/v1/actions/{action_id}",
            headers=mock_auth_headers
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify intention still exists
        intention_check = client.get(
            f"/api/v1/intentions/{intention_id}",
            headers=mock_auth_headers
        )
        assert intention_check.status_code == status.HTTP_200_OK

        # Verify action link removed from intention
        intention_detail = intention_check.json()
        assert len(intention_detail["linkedActions"]) == 0
