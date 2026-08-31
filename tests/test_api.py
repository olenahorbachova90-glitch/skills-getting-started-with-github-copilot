"""Legacy integration tests using AAA pattern."""

import pytest


class TestAPIIntegration:
    """Integration tests for API endpoints."""

    def test_unregister_participant_from_activity(self, client):
        """
        AAA Test: Verify unregister endpoint removes participant correctly.
        Arrange: Select existing participant from Chess Club
        Act: DELETE request to unregister participant
        Assert: Status 200, participant removed, confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert email not in result["participants"]
        assert email in result["message"]
