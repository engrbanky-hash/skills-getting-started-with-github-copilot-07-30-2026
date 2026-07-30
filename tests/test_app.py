from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_and_unregister_participant():
    email = "newstudent@example.com"

    signup_response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert signup_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email in activities_response.json()["Chess Club"]["participants"]

    unregister_response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )
    assert unregister_response.status_code == 200

    updated_response = client.get("/activities")
    assert email not in updated_response.json()["Chess Club"]["participants"]
