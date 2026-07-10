import copy
from fastapi.testclient import TestClient
from urllib.parse import quote
import src.app as app_module

# Keep an original snapshot of activities so tests can reset state
_original_activities = copy.deepcopy(app_module.activities)


def setup_function():
    app_module.activities = copy.deepcopy(_original_activities)


def test_get_activities():
    with TestClient(app_module.app) as client:
        r = client.get("/activities")
        assert r.status_code == 200
        data = r.json()
        assert "Chess Club" in data


def test_signup_success():
    with TestClient(app_module.app) as client:
        payload = {"email": "newstudent@mergington.edu"}
        r = client.post(f"/activities/{quote('Chess Club')}/signup", json=payload)
        assert r.status_code in (200, 201)
        assert "Signed up newstudent@mergington.edu for Chess Club" in r.json()["message"]


def test_signup_duplicate():
    with TestClient(app_module.app) as client:
        payload = {"email": "michael@mergington.edu"}
        r = client.post(f"/activities/{quote('Chess Club')}/signup", json=payload)
        assert r.status_code == 400


def test_signup_not_found():
    with TestClient(app_module.app) as client:
        payload = {"email": "someone@x.com"}
        r = client.post(f"/activities/{quote('Nonexistent')}/signup", json=payload)
        assert r.status_code == 404


def test_signup_full():
    # create an activity that is already full
    app_module.activities["Tiny Club"] = {
        "description": "x",
        "schedule": "now",
        "max_participants": 0,
        "participants": [],
    }
    with TestClient(app_module.app) as client:
        payload = {"email": "a@b.com"}
        r = client.post(f"/activities/{quote('Tiny Club')}/signup", json=payload)
        assert r.status_code == 400
