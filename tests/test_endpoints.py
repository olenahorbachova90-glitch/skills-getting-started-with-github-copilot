"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        AAA Test: Verify GET /activities returns all available activities.
        Arrange: No setup needed (uses fixture client)
        Act: Make GET request to /activities
        Assert: Status 200 and all 9 activities present
        """
        # Arrange
        expected_activity_count = 9
        expected_activity_names = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Club",
            "Science Club",
        }

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert set(activities.keys()) == expected_activity_names

    def test_get_activities_response_structure(self, client):
        """
        AAA Test: Verify each activity has required fields.
        Arrange: Define required fields
        Act: Get activities and inspect structure
        Assert: Each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in activities.items():
            assert set(activity_details.keys()) == required_fields
            assert isinstance(activity_details["description"], str)
            assert isinstance(activity_details["schedule"], str)
            assert isinstance(activity_details["max_participants"], int)
            assert isinstance(activity_details["participants"], list)
            # All participants should be strings (emails)
            for participant in activity_details["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_initial_participants_correct(self, client):
        """
        AAA Test: Verify initial participant counts match expected state.
        Arrange: Define expected initial participants
        Act: Fetch activities
        Assert: Participants match initial state
        """
        # Arrange
        expected_participants = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
            "Basketball Team": 1,
            "Tennis Club": 2,
            "Art Studio": 1,
            "Music Band": 2,
            "Debate Club": 1,
            "Science Club": 2,
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, expected_count in expected_participants.items():
            assert activity_name in activities
            assert len(activities[activity_name]["participants"]) == expected_count
