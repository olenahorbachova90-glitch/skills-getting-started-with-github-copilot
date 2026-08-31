"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for activity signup functionality."""

    def test_signup_successful(self, client):
        """
        AAA Test: Verify successful signup adds participant to activity.
        Arrange: Prepare email and activity name
        Act: POST signup request
        Assert: Status 200, success message, participant added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

        # Verify participant was actually added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """
        AAA Test: Verify signup fails with 404 when activity doesn't exist.
        Arrange: Use non-existent activity name
        Act: POST signup request
        Assert: Status 404, error detail
        """
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert result["detail"] == "Activity not found"

    def test_signup_already_registered(self, client):
        """
        AAA Test: Verify signup fails with 400 when student already registered.
        Arrange: Use email already in participants
        Act: POST signup request
        Assert: Status 400, error detail
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert result["detail"] == "Student is already signed up for this activity"

    def test_signup_activity_full(self, client):
        """
        AAA Test: Verify signup fails with 400 when activity is at max capacity.
        Arrange: Fill activity to max by signing up until full
        Act: Attempt one more signup
        Assert: Status 400, error detail
        """
        # Arrange
        # Basketball Team has max_participants=15 and 1 current participant
        activity_name = "Basketball Team"
        max_participants = 15
        base_participants_count = 1

        # Sign up enough students to fill the activity
        for i in range(max_participants - base_participants_count):
            email = f"fillstudent{i}@mergington.edu"
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Act - try to signup when full
        overflow_email = "overflow@mergington.edu"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": overflow_email}
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert result["detail"] == "Activity is full"

    def test_signup_updates_spots_left(self, client):
        """
        AAA Test: Verify signup decrements available spots correctly.
        Arrange: Get initial participant count
        Act: Sign up one student, check updated count
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Art Studio"
        email = "newartist@mergington.edu"

        activities_response = client.get("/activities")
        initial_participants = activities_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

        # Verify new count
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count + 1
        assert email in updated_participants

    def test_signup_multiple_different_activities(self, client):
        """
        AAA Test: Verify same student can signup for different activities.
        Arrange: Prepare email and multiple activity names
        Act: Sign up for first activity, then second
        Assert: Both signups succeed, student in both activities
        """
        # Arrange
        email = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Music Band"

        # Act - Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )

        # Act - Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify student is in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
