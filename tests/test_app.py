from fastapi.testclient import TestClient

from src.app import app, activities


def setup_function():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu"],
            }
        }
    )


def test_duplicate_signup_is_rejected():
    client = TestClient(app)

    first_response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )

    assert second_response.status_code == 400
    assert second_response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_participant_can_be_removed_from_activity():
    client = TestClient(app)

    response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
