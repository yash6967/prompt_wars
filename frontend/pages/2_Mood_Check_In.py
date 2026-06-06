import streamlit as st
from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Check-In — Saathi")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title("📝 Daily Mood Check-In")
st.markdown("Taking a moment to log how you feel helps visualize patterns and keeps you grounded.")

with st.form("check_in_form"):
    mood_score = st.slider("How is your mood today?", min_value=1, max_value=10, value=6, help="1 = Extremely low, 10 = Feeling amazing")
    energy_level = st.slider("What is your current energy level?", min_value=1, max_value=10, value=6, help="1 = Fully exhausted, 10 = Hyperactive & ready")
    sleep_hours = st.number_input("How many hours did you sleep last night?", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    study_hours = st.number_input("How many hours did you study today?", min_value=0.0, max_value=24.0, value=4.0, step=0.5)
    
    st.markdown("##### Emotion Tags")
    options = ["Anxious", "Stressed", "Calm", "Tired", "Motivated", "Bored", "Focused", "Happy", "Overwhelmed", "Excited"]
    selected_tags = st.multiselect("Select emotions matching your current state:", options)
    
    note = st.text_area("Write down any thoughts or journal notes:", placeholder="What is causing stress or helping you study today?")
    
    submitted = st.form_submit_button("Submit Entry", use_container_width=True)
    if submitted:
        emotion_tags_str = ",".join(selected_tags) if selected_tags else ""
        payload = {
            "mood_score": mood_score,
            "energy_level": energy_level,
            "sleep_hours": sleep_hours,
            "study_hours": study_hours,
            "emotion_tags": emotion_tags_str,
            "note": note
        }
        res = api_client.request("POST", "mood/", json_data=payload)
        if res and res.status_code == 200:
            st.success("Mood logged successfully! Check the Dashboard to see your trends.")
        else:
            st.error("Failed to log mood. Please try again.")
