import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme
from frontend.utils.translations import t

st.set_page_config(page_title="Dashboard — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

user = st.session_state["user"]
st.title(t("dash_title"))
student_lbl = "छात्र" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Student"
target_exam_lbl = "लक्षित परीक्षा" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Target Exam"
st.markdown(f"**{student_lbl}:** {user['name']} | **{target_exam_lbl}:** {user['exam_target']}")

escalation_res = api_client.request("GET", "analytics/escalation-check")
if escalation_res and escalation_res.status_code == 200:
    escalation_data = escalation_res.json()
    if escalation_data.get("escalation_required"):
        st.markdown(
            f"""
            <div class="card-rose" role="alert" aria-live="assertive" aria-atomic="true" aria-label="Student Safety Escalation Alert">
                <h3 style="color: inherit; margin-top: 0;">{t("urgent_escalation")}</h3>
                <p>{t("escalation_p1")}</p>
                <p><b>{t("flagged_reasons")}</b></p>
                <ul>
            """
            + "".join([f"<li>{r}</li>" for r in escalation_data.get("reasons", [])])
            + f"""
                </ul>
                <p>{t("support_helplines")}</p>
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
        st.metric(label=t("avg_mood"), value=f"{summary['avg_mood_14d']}/10")
    with col2:
        st.metric(label=t("avg_energy"), value=f"{summary['avg_energy_14d']}/10")
    with col3:
        sleep_suffix = " घंटे" if st.session_state.get("language") == "Hindi (हिन्दी)" else " hrs"
        st.metric(label=t("avg_sleep"), value=f"{summary['avg_sleep_14d']}{sleep_suffix}")
    with col4:
        study_suffix = " घंटे" if st.session_state.get("language") == "Hindi (हिन्दी)" else " hrs"
        st.metric(label=t("avg_study"), value=f"{summary['avg_study_14d']}{study_suffix}")
        
    st.markdown("---")
    
history_res = api_client.request("GET", "mood/history")
if history_res and history_res.status_code == 200:
    history_data = history_res.json()
    if history_data:
        df = pd.DataFrame(history_data)
        df["logged_at"] = pd.to_datetime(df["logged_at"])
        df = df.sort_values(by="logged_at")
        
        st.header(t("trends_title"))
        
        is_dark = st.session_state.get("theme_mode", "Light") == "Dark"
        chart_template = "plotly_dark" if is_dark else "simple_white"
        chart_font = "#FAF4EE" if is_dark else "#2C2724"

        value_lbl = "स्कोर (1-10)" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Score (1-10)"
        date_lbl = "लॉग तिथि" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Logged Date"
        trajectory_title = "मनोदशा और ऊर्जा प्रक्षेपवक्र" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Mood & Energy Trajectory"
        mood_legend = "मनोदशा स्कोर" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Mood Score"
        energy_legend = "ऊर्जा स्तर" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Energy Level"

        df_renamed = df.rename(columns={"mood_score": mood_legend, "energy_level": energy_legend})

        fig = px.line(
            df_renamed, 
            x="logged_at", 
            y=[mood_legend, energy_legend], 
            labels={"value": value_lbl, "logged_at": date_lbl, "variable": "Metric"},
            title=trajectory_title,
            color_discrete_sequence=["#8E95D3", "#94B5A6"]
        )
        fig.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font)
        st.plotly_chart(fig, use_container_width=True)
        
        col_left, col_right = st.columns(2)
        with col_left:
            sleep_chart_title = "प्रति दिन नींद के घंटे" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Sleep Hours per Day"
            fig_sleep = px.bar(
                df,
                x="logged_at",
                y="sleep_hours",
                title=sleep_chart_title,
                labels={"sleep_hours": "Hours" if st.session_state.get("language") != "Hindi (हिन्दी)" else "घंटे", "logged_at": date_lbl},
                color_discrete_sequence=["#E5C672"]
            )
            fig_sleep.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font)
            st.plotly_chart(fig_sleep, use_container_width=True)
            
        with col_right:
            study_chart_title = "प्रति दिन पढ़ाई के घंटे" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Study Hours per Day"
            fig_study = px.bar(
                df,
                x="logged_at",
                y="study_hours",
                title=study_chart_title,
                labels={"study_hours": "Hours" if st.session_state.get("language") != "Hindi (हिन्दी)" else "घंटे", "logged_at": date_lbl},
                color_discrete_sequence=["#94B5A6"]
            )
            fig_study.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font)
            st.plotly_chart(fig_study, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(t("screen_reader_alt")):
            st.markdown(f"### {t('summary_table')}")
            summary_df = df[["logged_at", "mood_score", "energy_level", "sleep_hours", "study_hours"]].copy()
            summary_df["logged_at"] = summary_df["logged_at"].dt.strftime("%Y-%m-%d")
            st.dataframe(summary_df.rename(columns={
                "logged_at": "Logged Date" if st.session_state.get("language") != "Hindi (हिन्दी)" else "लॉग तिथि",
                "mood_score": "Mood Score (1-10)" if st.session_state.get("language") != "Hindi (हिन्दी)" else "मनोदशा स्कोर (1-10)",
                "energy_level": "Energy Level (1-10)" if st.session_state.get("language") != "Hindi (हिन्दी)" else "ऊर्जा स्तर (1-10)",
                "sleep_hours": "Sleep (Hours)" if st.session_state.get("language") != "Hindi (हिन्दी)" else "नींद (घंटे)",
                "study_hours": "Study (Hours)" if st.session_state.get("language") != "Hindi (हिन्दी)" else "अध्ययन (घंटे)"
            }), use_container_width=True, hide_index=True)
            
    else:
        st.info(t("no_logs"))
