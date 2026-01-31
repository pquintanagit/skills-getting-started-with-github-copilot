import copy
import pytest


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from src.app import app

    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Ensure activities are reset between tests to avoid cross-test pollution
    from src import app as app_module
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Soccer" in data
    assert isinstance(data["Soccer"].get("participants"), list)


def test_signup_success(client):
    email = "testuser@example.com"
    resp = client.post(f"/activities/Soccer/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")


def test_signup_duplicate(client):
    # alex@mergington.edu is already a participant in Soccer per default data
    resp = client.post("/activities/Soccer/signup?email=alex@mergington.edu")
    assert resp.status_code == 400


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert resp.status_code == 404
