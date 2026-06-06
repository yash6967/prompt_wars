import pytest
from backend.services import ai_service

@pytest.fixture
def auth_headers(client):
    reg_payload = {
        "name": "Student User",
        "email": "student@saathi.com",
        "password": "SecurePass123!",
        "exam_target": "Boards"
    }
    reg_res = client.post("/auth/register", json=reg_payload)
    token = reg_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_invite_ally(client, auth_headers):
    payload = {
        "ally_name": "Parent Name",
        "ally_email": "parent@saathi.com",
        "role": "Parent"
    }
    response = client.post("/ally/invite", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["ally_name"] == "Parent Name"
    assert data["ally_email"] == "parent@saathi.com"
    assert data["role"] == "Parent"
    assert data["is_verified"] is True

def test_get_ally_connections(client, auth_headers):
    # Invite an ally first
    payload = {
        "ally_name": "Teacher Name",
        "ally_email": "teacher@saathi.com",
        "role": "Teacher"
    }
    client.post("/ally/invite", json=payload, headers=auth_headers)
    
    response = client.get("/ally/connections", headers=auth_headers)
    assert response.status_code == 200
    connections = response.json()
    assert len(connections) >= 1
    assert connections[0]["ally_name"] == "Teacher Name"

def test_get_ally_nudges_with_mocked_llm(client, auth_headers, monkeypatch):
    # Mock the AI service call to return structured text
    mock_nudge = "Elevated stress detected Actionable Tips: Encourage regular breaks and water."
    monkeypatch.setattr(ai_service, "generate_subtle_ally_nudge", lambda *args, **kwargs: mock_nudge)
    
    # Connect an ally
    payload = {
        "ally_name": "Educator Guide",
        "ally_email": "guide@saathi.com",
        "role": "Mentor"
    }
    client.post("/ally/invite", json=payload, headers=auth_headers)
    
    # Fetch nudges (which triggers the mocked generator)
    response = client.get("/ally/nudges", headers=auth_headers)
    assert response.status_code == 200
    nudges = response.json()
    assert len(nudges) >= 1
    assert nudges[0]["insight_summary"] == "Elevated stress detected"
    assert nudges[0]["actionable_tip"] == "Encourage regular breaks and water."
