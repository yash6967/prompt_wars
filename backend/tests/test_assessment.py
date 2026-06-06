import pytest
import json

@pytest.fixture
def auth_headers(client):
    reg_payload = {
        "name": "Assessment Tester",
        "email": "assessment@saathi.com",
        "password": "SecurePass123!",
        "exam_target": "JEE Main"
    }
    reg_res = client.post("/auth/register", json=reg_payload)
    token = reg_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_assessment_questions(client, auth_headers):
    response = client.get("/assessment/questions", headers=auth_headers)
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) == 20
    assert questions[0]["category"] == "PHQ"

def test_submit_assessment_mild(client, auth_headers):
    # Construct mild score answers (all 0s)
    answers = {str(i): 0 for i in range(1, 21)}
    payload = {
        "answers_json": json.dumps(answers)
    }
    response = client.post("/assessment/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["phq_score"] == 0
    assert data["gad_score"] == 0
    assert data["pss_score"] == 6  # PSS has 2 reverse questions: 3-0 + 3-0 = 6
    assert data["overall_level"] == "mild"

def test_submit_assessment_severe(client, auth_headers):
    # Construct severe score answers (all 3s)
    answers = {str(i): 3 for i in range(1, 21)}
    payload = {
        "answers_json": json.dumps(answers)
    }
    response = client.post("/assessment/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["phq_score"] == 27
    assert data["gad_score"] == 21
    assert data["overall_level"] == "severe"
