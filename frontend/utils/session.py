import streamlit as st
from frontend.utils import api_client

def init_session():
    if "access_token" not in st.session_state:
        st.session_state["access_token"] = None
    if "user" not in st.session_state:
        st.session_state["user"] = None

def login(email: str, password: str) -> bool:
    response = api_client.request("POST", "auth/login", data={"username": email, "password": password})
    if response and response.status_code == 200:
        token_data = response.json()
        st.session_state["access_token"] = token_data["access_token"]
        me_resp = api_client.request("GET", "auth/me")
        if me_resp and me_resp.status_code == 200:
            st.session_state["user"] = me_resp.json()
            return True
    return False

def register(name: str, email: str, password: str, exam_target: str = None, exam_date: str = None) -> bool:
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "exam_target": exam_target,
        "exam_date": exam_date
    }
    response = api_client.request("POST", "auth/register", json_data=payload)
    if response and response.status_code == 200:
        token_data = response.json()
        st.session_state["access_token"] = token_data["access_token"]
        me_resp = api_client.request("GET", "auth/me")
        if me_resp and me_resp.status_code == 200:
            st.session_state["user"] = me_resp.json()
            return True
    return False

def logout():
    st.session_state["access_token"] = None
    st.session_state["user"] = None

def is_logged_in() -> bool:
    return st.session_state.get("access_token") is not None
