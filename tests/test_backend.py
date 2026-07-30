def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12
    assert "participants" in payload["Chess Club"]


def test_signup_for_activity(client):
    email = "newstudent@example.com"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "duplicate@example.com"

    first_response = client.post(f"/activities/Chess Club/signup?email={email}")
    second_response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant(client):
    email = "remove@example.com"
    client.post(f"/activities/Chess Club/signup?email={email}")

    response = client.delete(f"/activities/Chess Club/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
