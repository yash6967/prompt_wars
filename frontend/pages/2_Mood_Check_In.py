import os
import sys
import streamlit as st

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme
from frontend.utils.translations import t

st.set_page_config(page_title="Check-In — Saathi")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title(t("mood_title"))
st.markdown(t("mood_desc"))

with st.form("check_in_form"):
    mood_score = st.slider(t("mood_q"), min_value=1, max_value=10, value=6, help="1 = Extremely low, 10 = Feeling amazing")
    energy_level = st.slider(t("energy_q"), min_value=1, max_value=10, value=6, help="1 = Fully exhausted, 10 = Hyperactive & ready")
    sleep_hours = st.number_input(t("sleep_q"), min_value=0.0, max_value=24.0, value=7.0, step=0.5, help="Enter the approximate number of hours of sleep you had last night.")
    study_hours = st.number_input(t("study_q"), min_value=0.0, max_value=24.0, value=4.0, step=0.5, help="Enter the total hours spent studying today.")
    
    st.markdown(f"### {t('emotion_tags')}")
    options = ["Anxious", "Stressed", "Calm", "Tired", "Motivated", "Bored", "Focused", "Happy", "Overwhelmed", "Excited"]
    options_trans = {
        "Anxious": "चिंतित (Anxious)",
        "Stressed": "तनावग्रस्त (Stressed)",
        "Calm": "शांत (Calm)",
        "Tired": "थका हुआ (Tired)",
        "Motivated": "प्रेरित (Motivated)",
        "Bored": "उबा हुआ (Bored)",
        "Focused": "एकाग्र (Focused)",
        "Happy": "खुश (Happy)",
        "Overwhelmed": "अभिभूत (Overwhelmed)",
        "Excited": "उत्साहित (Excited)"
    }
    display_options = [options_trans[o] for o in options] if st.session_state.get("language") == "Hindi (हिन्दी)" else options
    selected_tags_trans = st.multiselect(t("select_emotions"), display_options, help="Select one or more emotion tags that describe your mood.")
    
    # Map back to English tag strings for database compatibility
    if st.session_state.get("language") == "Hindi (हिन्दी)":
        rev_map = {v: k for k, v in options_trans.items()}
        selected_tags = [rev_map[tag] for tag in selected_tags_trans]
    else:
        selected_tags = selected_tags_trans
        
    note = st.text_area(t("journal_notes"), placeholder=t("journal_placeholder"), help="Write any voluntary journal thoughts or daily updates to track stress causes.")
    
    submitted = st.form_submit_button(t("submit_entry"), use_container_width=True)
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
            st.success(t("mood_success"))
        else:
            st.error(t("mood_fail"))
