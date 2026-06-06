import pytest

def test_register_user(client):
    payload = {
        "name": "Test User",
        "email": "test@saathi.com",
        "password": "testpassword123",
        "exam_target": "JEE Main"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client):
    payload = {
        "name": "Test User 1",
        "email": "dup@saathi.com",
        "password": "testpassword123",
        "exam_target": "NEET UG"
    }
    # First registration
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    
    # Duplicate registration
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user(client):
    # Register user first
    reg_payload = {
        "name": "Login Tester",
        "email": "log@saathi.com",
        "password": "mypassword",
        "exam_target": "CAT"
    }
    client.post("/auth/register", json=reg_payload)
    
    # Login payload
    login_data = {
        "username": "log@saathi.com",
        "password": "mypassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    
def test_login_invalid_credentials(client):
    login_data = {
        "username": "nonexistent@saathi.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_get_current_user_profile(client):
    reg_payload = {
        "name": "Profile Tester",
        "email": "prof@saathi.com",
        "password": "mypassword",
        "exam_target": "GATE"
    }
    reg_res = client.post("/auth/register", json=reg_payload)
    token = reg_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "prof@saathi.com"
    assert data["name"] == "Profile Tester"
    assert data["exam_target"] == "GATE"
