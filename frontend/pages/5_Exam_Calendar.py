import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Exam Calendar — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

user = st.session_state["user"]
st.title("📅 Exam Timelines & Deadlines")
st.markdown("Track registration timelines and final countdowns for major competitive and board examinations.")

# User's target exam highlight
target_exam = user.get("exam_target")
if target_exam:
    st.info(f"💡 Your selected target exam is **{target_exam}**. Focus on its milestone boundaries below.")

# Filtering input
days_filter = st.slider("Filter upcoming exams within the next (days):", min_value=30, max_value=365, value=120, step=30, help="Drag to adjust the time window (in days) for displaying upcoming national examinations.")

with st.spinner("Fetching calendar dates..."):
    # Fetch upcoming exams
    upcoming_res = api_client.request("GET", f"calendar/upcoming?days={days_filter}")
    # Fetch all exams
    all_res = api_client.request("GET", "calendar/exams")
    
if all_res and all_res.status_code == 200:
    all_exams = all_res.json()
    upcoming_exams = upcoming_res.json() if upcoming_res and upcoming_res.status_code == 200 else []
    
    # Render Upcoming Exams List
    st.subheader(f"⏳ Upcoming Exams in next {days_filter} days")
    if upcoming_exams:
        card_styles = ["card-lavender", "card-sage"]
        for idx, exam in enumerate(upcoming_exams):
            is_target = target_exam and target_exam.lower() in exam["name"].lower()
            card_class = "card-gold" if is_target else card_styles[idx % len(card_styles)]
            
            # Formatted dates
            exam_date = datetime.fromisoformat(exam["date"]).strftime("%B %d, %Y - %I:%M %p")
            reg_start = datetime.fromisoformat(exam["registration_start"]).strftime("%b %d, %Y")
            reg_end = datetime.fromisoformat(exam["registration_end"]).strftime("%b %d, %Y")
            
            st.markdown(
                f"""
                <div class="{card_class}">
                    <h4 style="margin: 0;">{exam['name']} {'⭐ (Your Target)' if is_target else ''}</h4>
                    <p style="margin: 5px 0;">📅 <b>Exam Date:</b> {exam_date}</p>
                    <p style="margin: 5px 0; font-size: 0.9rem;">📝 <b>Registration Window:</b> {reg_start} to {reg_end}</p>
                    <a href="{exam['info_link']}" target="_blank" style="color: #2C2724; text-decoration: underline; font-weight: bold;">Official Registration Link ↗</a>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No exams found within the selected timeframe.")
        
    st.markdown("---")
    
    # Render all exams in a comprehensive Table
    st.subheader("📊 Complete Exam Directory")
    df_data = []
    for exam in all_exams:
        df_data.append({
            "Exam Name": exam["name"],
            "Exam Date": datetime.fromisoformat(exam["date"]).strftime("%Y-%m-%d"),
            "Registration Starts": datetime.fromisoformat(exam["registration_start"]).strftime("%Y-%m-%d"),
            "Registration Deadline": datetime.fromisoformat(exam["registration_end"]).strftime("%Y-%m-%d"),
            "Official Portal": exam["info_link"]
        })
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error("Failed to retrieve exams database.")
