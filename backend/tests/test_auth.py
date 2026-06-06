import pytest

def test_register_user(client):
    payload = {
        "name": "Test User",
        "email": "test@saathi.com",
        "password": "SecurePass123!",
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
        "password": "SecurePass123!",
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
        "password": "SecurePass123!",
        "exam_target": "CAT"
    }
    client.post("/auth/register", json=reg_payload)
    
    # Login payload
    login_data = {
        "username": "log@saathi.com",
        "password": "SecurePass123!"
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
        "password": "SecurePass123!",
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

def test_register_weak_password_length(client):
    payload = {
        "name": "Weak User",
        "email": "weaklen@saathi.com",
        "password": "S1!",
        "exam_target": "Other"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "at least 8 characters" in response.json()["detail"]

def test_register_weak_password_no_digit(client):
    payload = {
        "name": "Weak User",
        "email": "weaknodig@saathi.com",
        "password": "SecurePass!",
        "exam_target": "Other"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "at least one digit" in response.json()["detail"]

def test_register_weak_password_no_special(client):
    payload = {
        "name": "Weak User",
        "email": "weaknospec@saathi.com",
        "password": "SecurePass123",
        "exam_target": "Other"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "at least one special character" in response.json()["detail"]

def test_register_empty_name(client):
    payload = {
        "name": "   ",
        "email": "emptyname@saathi.com",
        "password": "SecurePass123!",
        "exam_target": "Other"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "Name cannot be empty" in response.json()["detail"]
