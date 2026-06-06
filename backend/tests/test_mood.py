import pytest

@pytest.fixture
def auth_headers(client):
    reg_payload = {
        "name": "Mood Tester",
        "email": "moody@saathi.com",
        "password": "SecurePass123!",
        "exam_target": "NEET UG"
    }
    reg_res = client.post("/auth/register", json=reg_payload)
    token = reg_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_mood_entry(client, auth_headers):
    payload = {
        "mood_score": 8,
        "energy_level": 7,
        "sleep_hours": 7.5,
        "study_hours": 6.0,
        "emotion_tags": "Focused,Motivated",
        "note": "Had a highly productive study session today."
    }
    response = client.post("/mood/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["mood_score"] == 8
    assert data["energy_level"] == 7
    assert data["sleep_hours"] == 7.5
    assert data["study_hours"] == 6.0
    assert data["emotion_tags"] == "Focused,Motivated"
    assert data["note"] == "Had a highly productive study session today."
    assert "logged_at" in data

def test_get_mood_history(client, auth_headers):
    # Log two distinct mood entries
    client.post("/mood/", json={"mood_score": 6, "energy_level": 5}, headers=auth_headers)
    client.post("/mood/", json={"mood_score": 9, "energy_level": 8}, headers=auth_headers)
    
    # Retrieve history
    response = client.get("/mood/history", headers=auth_headers)
    assert response.status_code == 200
    history = response.json()
    assert len(history) >= 2
    assert history[0]["mood_score"] == 9
    assert history[1]["mood_score"] == 6
