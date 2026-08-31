"""Shared pytest fixtures for test isolation and configuration."""

import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for making requests to the app."""
    return TestClient(app)


@pytest.fixture
def initial_activities_state():
    """Provide the initial state of activities for reference in tests."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball practice and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis lessons and match play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn and perform in the school band",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["alexander@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore experiments and scientific research",
            "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["charlotte@mergington.edu", "benjamin@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(initial_activities_state):
    """
    Automatically reset activities to initial state before each test.
    This ensures test isolation and prevents state leakage between tests.
    """
    # Deep copy to reset all nested lists
    activities.clear()
    activities.update(copy.deepcopy(initial_activities_state))
    yield
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(copy.deepcopy(initial_activities_state))
