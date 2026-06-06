import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Dashboard — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

user = st.session_state["user"]
st.title("📊 Student Wellness Dashboard")
st.markdown(f"**Student:** {user['name']} | **Target Exam:** {user['exam_target']}")

escalation_res = api_client.request("GET", "analytics/escalation-check")
if escalation_res and escalation_res.status_code == 200:
    escalation_data = escalation_res.json()
    if escalation_data.get("escalation_required"):
        st.markdown(
            """
            <div class="card-rose">
                <h3 style="color: inherit; margin-top: 0;">🚨 Urgent: Student Safety Escalation Active</h3>
                <p>Recent self-reports or stress indicators suggest you are experiencing extremely high pressure or distress.</p>
                <p><b>Reasons flagged:</b></p>
                <ul>
            """
            + "".join([f"<li>{r}</li>" for r in escalation_data.get("reasons", [])])
            + """
                </ul>
                <p>You do not have to walk this path alone. Please reach out to one of the following confidential support resources immediately:</p>
                <ul>
            """
            + "".join([f"<li><b>{h['name']}:</b> {h['contact']}</li>" for h in escalation_data.get("support_helplines", [])])
            + """
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

summary_res = api_client.request("GET", "analytics/summary")
if summary_res and summary_res.status_code == 200:
    summary = summary_res.json()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Average Mood (14d)", value=f"{summary['avg_mood_14d']}/10")
    with col2:
        st.metric(label="Average Energy (14d)", value=f"{summary['avg_energy_14d']}/10")
    with col3:
        st.metric(label="Average Sleep (14d)", value=f"{summary['avg_sleep_14d']} hrs")
    with col4:
        st.metric(label="Average Study (14d)", value=f"{summary['avg_study_14d']} hrs")
        
    st.markdown("---")
    
history_res = api_client.request("GET", "mood/history")
if history_res and history_res.status_code == 200:
    history_data = history_res.json()
    if history_data:
        df = pd.DataFrame(history_data)
        df["logged_at"] = pd.to_datetime(df["logged_at"])
        df = df.sort_values(by="logged_at")
        
        st.header("📈 Wellness Trends Over Time")
        
        is_dark = st.session_state.get("theme_mode", "Light") == "Dark"
        chart_template = "plotly_dark" if is_dark else "simple_white"
        chart_font = "#FAF4EE" if is_dark else "#2C2724"

        fig = px.line(
            df, 
            x="logged_at", 
            y=["mood_score", "energy_level"], 
            labels={"value": "Score (1-10)", "logged_at": "Logged Date"},
            title="Mood & Energy Trajectory",
            color_discrete_sequence=["#8E95D3", "#94B5A6"]
        )
        fig.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font)
        st.plotly_chart(fig, use_container_width=True)
        
        col_left, col_right = st.columns(2)
        with col_left:
            fig_sleep = px.bar(
                df,
                x="logged_at",
                y="sleep_hours",
                title="Sleep Hours per Day",
                color_discrete_sequence=["#E5C672"]
            )
            fig_sleep.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font)
            st.plotly_chart(fig_sleep, use_container_width=True)
            
        with col_right:
            fig_study = px.bar(
                df,
                x="logged_at",
                y="study_hours",
                title="Study Hours per Day",
                color_discrete_sequence=["#94B5A6"]
            )
            fig_study.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font)
            st.plotly_chart(fig_study, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("👁️ View Text Alternative for Screen Readers & Low Bandwidth"):
            st.markdown("### Daily Wellness Logs Summary Table")
            summary_df = df[["logged_at", "mood_score", "energy_level", "sleep_hours", "study_hours"]].copy()
            summary_df["logged_at"] = summary_df["logged_at"].dt.strftime("%Y-%m-%d")
            st.dataframe(summary_df.rename(columns={
                "logged_at": "Logged Date",
                "mood_score": "Mood Score (1-10)",
                "energy_level": "Energy Level (1-10)",
                "sleep_hours": "Sleep (Hours)",
                "study_hours": "Study (Hours)"
            }), use_container_width=True, hide_index=True)
            
    else:
        st.info("Log your daily mood check-in to see wellness charts!")
