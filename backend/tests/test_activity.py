import pytest

@pytest.fixture
def auth_headers(client):
    reg_payload = {
        "name": "Activity Tester",
        "email": "active@saathi.com",
        "password": "SecurePass123!",
        "exam_target": "CAT"
    }
    reg_res = client.post("/auth/register", json=reg_payload)
    token = reg_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_activity_advice(client, auth_headers):
    response = client.get("/activity/advice", headers=auth_headers)
    assert response.status_code == 200
    advice = response.json()
    assert "exercise" in advice
    assert "hydration" in advice

def test_log_activity_and_fetch_today(client, auth_headers):
    # Log 1st activity
    act1 = {
        "activity_type": "exercise",
        "duration_minutes": 15,
        "description": "Jogged in the garden"
    }
    res1 = client.post("/activity/log", json=act1, headers=auth_headers)
    assert res1.status_code == 200
    
    # Log 2nd activity
    act2 = {
        "activity_type": "meditation",
        "duration_minutes": 10,
        "description": "Mindfulness breathing"
    }
    res2 = client.post("/activity/log", json=act2, headers=auth_headers)
    assert res2.status_code == 200
    
    # Fetch today's aggregate summary
    response = client.get("/activity/today", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["total_duration_minutes"] == 25
    assert len(data["activities"]) == 2
    assert data["activities"][0]["activity_type"] == "exercise"
