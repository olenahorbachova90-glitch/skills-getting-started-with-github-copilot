"""Tests for DELETE /activities/{activity_name}/participants endpoint."""

import pytest


class TestUnregister:
    """Test suite for unregistering participants from activities."""

    def test_unregister_successful(self, client):
        """
        AAA Test: Verify successful unregistration removes participant.
        Arrange: Select existing participant
        Act: DELETE request to unregister
        Assert: Status 200, participant removed from list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert email not in result["participants"]
        assert "message" in result
        assert email in result["message"]

    def test_unregister_activity_not_found(self, client):
        """
        AAA Test: Verify unregister fails with 404 when activity doesn't exist.
        Arrange: Use non-existent activity name
        Act: DELETE request
        Assert: Status 404, error detail
        """
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert result["detail"] == "Activity not found"

    def test_unregister_not_registered(self, client):
        """
        AAA Test: Verify unregister fails with 404 when student not registered.
        Arrange: Use email not in participants list
        Act: DELETE request
        Assert: Status 404, error detail
        """
        # Arrange
        activity_name = "Debate Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert result["detail"] == "Student is not registered for this activity"

    def test_unregister_frees_spot(self, client):
        """
        AAA Test: Verify unregistration frees up a spot for new signup.
        Arrange: Unregister someone, then sign up a new student
        Act: Sign up after unregistering
        Assert: New signup succeeds (spot was freed)
        """
        # Arrange
        activity_name = "Basketball Team"
        max_participants = 15
        existing_participants = 1

        # Fill the activity
        for i in range(max_participants - existing_participants):
            email = f"filler{i}@mergington.edu"
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Get activities to know who we can unregister
        activities_response = client.get("/activities")
        current_participants = activities_response.json()[activity_name]["participants"]
        unregister_email = current_participants[0]  # Unregister first participant

        # Act - Unregister someone
        unregister_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": unregister_email}
        )

        # Act - Try to sign up new student (should succeed now)
        new_student_email = "newstudent@mergington.edu"
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student_email}
        )

        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        assert unregister_email not in unregister_response.json()["participants"]

    def test_unregister_from_multiple_activities_independent(self, client):
        """
        AAA Test: Verify unregistering from one activity doesn't affect others.
        Arrange: Sign up for two activities, unregister from one
        Act: Unregister from first activity
        Assert: Removed from first, still in second
        """
        # Arrange
        email = "dual@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Music Band"

        # Sign up for both
        client.post(f"/activities/{activity1}/signup", params={"email": email})
        client.post(f"/activities/{activity2}/signup", params={"email": email})

        # Act - Unregister from first activity
        response = client.delete(
            f"/activities/{activity1}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email not in response.json()["participants"]

        # Verify still registered for second activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_unregister_decreases_participant_count(self, client):
        """
        AAA Test: Verify participant count decreases after unregistration.
        Arrange: Get initial participant count
        Act: Unregister someone
        Assert: Count decreased by 1
        """
        # Arrange
        activity_name = "Science Club"
        email = "charlotte@mergington.edu"

        activities_response = client.get("/activities")
        initial_count = len(activities_response.json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        new_count = len(response.json()["participants"])
        assert new_count == initial_count - 1

    def test_unregister_cannot_unregister_twice(self, client):
        """
        AAA Test: Verify cannot unregister same participant twice.
        Arrange: Unregister someone
        Act: Try to unregister same person again
        Assert: Second unregister fails with 404
        """
        # Arrange
        activity_name = "Music Band"
        email = "noah@mergington.edu"

        # First unregister should succeed
        response1 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Act - Try to unregister again
        response2 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404
        assert response2.json()["detail"] == "Student is not registered for this activity"
