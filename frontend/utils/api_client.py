import os
import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

def get_headers():
    headers = {}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def request(method: str, path: str, json_data: dict = None, params: dict = None, data: dict = None):
    url = f"{BACKEND_URL}/{path.lstrip('/')}"
    headers = get_headers()
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == "POST":
            if json_data is not None:
                response = requests.post(url, headers=headers, json=json_data, params=params, timeout=10)
            else:
                response = requests.post(url, headers=headers, data=data, params=params, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json_data, params=params, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, params=params, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Network error connecting to backend: {e}")
        return None
