import os
import sys
import streamlit as st
from datetime import datetime

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Subtle Ally Connections — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title("🤝 Subtle Ally Co-Pilot View")
st.markdown(
    """
    Empower parents, teachers, or mentors to be a part of your support circle.
    
    **Privacy First:** Allies do not receive your raw exam scores, mood numbers, or journal details. 
    They only receive **translated care cards** offering general, non-alarmist action tips when preparation stress is detected.
    """
)

tab1, tab2 = st.tabs(["Link Trusted Ally", "Care Cards & Insights"])

with tab1:
    st.header("Add a Supportive Guide")
    st.markdown("Invite a mentor, guardian, or parent to receive wellness indicators.")
    
    with st.form("invite_ally_form"):
        ally_name = st.text_input("Ally Full Name:", help="Enter the full name of the trusted guardian or educator you want to link.")
        ally_email = st.text_input("Ally Email Address:", help="Enter the email address of the guide to send notifications.")
        role = st.selectbox("Role / Relationship:", ["Parent", "Teacher", "Mentor", "Sibling", "Friend", "Other"], help="Select the relationship role of the guide.")
        
        submitted = st.form_submit_button("Link Ally")
        if submitted:
            if not ally_name or not ally_email:
                st.error("Please fill in all the details.")
            else:
                payload = {
                    "ally_name": ally_name,
                    "ally_email": ally_email,
                    "role": role
                }
                res = api_client.request("POST", "ally/invite", json_data=payload)
                if res and res.status_code == 200:
                    st.success("Successfully linked your helper guide!")
                    st.rerun()
                else:
                    st.error("Failed to link ally connection.")

    st.markdown("---")
    st.header("👥 Your Linked Allies")
    with st.spinner("Loading connections..."):
        conn_res = api_client.request("GET", "ally/connections")
        if conn_res and conn_res.status_code == 200:
            connections = conn_res.json()
            if connections:
                for conn in connections:
                    st.markdown(
                        f"""
                        <div class="card-lavender">
                            <b>{conn['ally_name']}</b> ({conn['role']}) — <span>{conn['ally_email']}</span>
                            <br><span style="font-weight: bold; font-size: 0.85rem;">✔ Connection active (Privacy-first alerts enabled)</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("You haven't linked any helpers yet. Add one above to create a support circle!")

with tab2:
    st.header("📋 Sent Care Cards Preview")
    st.markdown("Here are the privacy-first care cards generated for your allies based on your wellness trends:")
    
    with st.spinner("Retrieving nudges..."):
        nudge_res = api_client.request("GET", "ally/nudges")
        if nudge_res and nudge_res.status_code == 200:
            nudges = nudge_res.json()
            if nudges:
                for nudge in nudges:
                    nudge_time = datetime.fromisoformat(nudge["generated_at"]).strftime("%B %d, %Y - %I:%M %p")
                    st.markdown(
                        f"""
                        <div class="card-gold">
                            <h3 style="margin-top: 0; font-size: 1.25rem;">Care Card (Sent {nudge_time})</h3>
                            <p><b>Insight Summary:</b> {nudge['insight_summary']}</p>
                            <p style="background: rgba(255,255,255,0.4); padding: 12px; border-radius: 12px; border: 1px dashed rgba(44, 39, 36, 0.2);">
                                💡 <b>Actionable Tip for Ally:</b> {nudge['actionable_tip']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No care cards generated yet. Complete your first daily **Mood Check-In** to generate wellness insights.")
        else:
            st.error("Failed to load care card logs.")
