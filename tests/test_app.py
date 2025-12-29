import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "successfully signed up" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_unregister_from_activity():
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "has been unregistered" in response.json()["message"]
    # Unregister again should fail
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]
