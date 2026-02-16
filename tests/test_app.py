from fastapi.testclient import TestClient
from src import app as app_mod

client = TestClient(app_mod.app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect at least one known activity
    assert "Tennis Club" in data


def test_signup_and_unregister_flow():
    activity = "Tennis Club"
    email = "pytest-user@example.com"

    # Ensure the test email is not registered
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]

    # Sign up the test user
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify the user was added
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Signing up again should fail (duplicate)
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Unregister the test user
    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify the user was removed
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]
