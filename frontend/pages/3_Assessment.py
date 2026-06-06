import os
import sys
import streamlit as st
import json

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme
from frontend.utils.translations import t

st.set_page_config(page_title="Wellness Assessment — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title(t("assess_title"))
st.markdown(t("assess_desc"))

# Fetch questions from backend
with st.spinner("Loading questionnaire..."):
    response = api_client.request("GET", "assessment/questions")
    if not response or response.status_code != 200:
        st.error("Failed to load questions from backend. Please ensure the backend server is running.")
        st.stop()
    questions = response.json()

options_map = {
    t("opt_not_at_all"): 0,
    t("opt_several_days"): 1,
    t("opt_more_than_half"): 2,
    t("opt_nearly_every_day"): 3
}

# Perceived Stress Scale questions have slightly different standard frequencies, but 0-3 scales map directly.
pss_options_map = {
    t("opt_never"): 0,
    t("opt_almost_never"): 1,
    t("opt_sometimes"): 2,
    t("opt_fairly_often"): 3
}

# Form for assessment input
st.markdown("---")
with st.form("assessment_form"):
    answers = {}
    
    # Group questions by category for better UX
    phq_questions = [q for q in questions if q["category"] == "PHQ"]
    gad_questions = [q for q in questions if q["category"] == "GAD"]
    pss_questions = [q for q in questions if q["category"] == "PSS"]
    
    if phq_questions:
        st.header(t("assess_sec1"))
        st.caption(t("assess_caption_2weeks"))
        for q in phq_questions:
            q_text = t(f"q{q['id']}")
            ans = st.radio(
                f"**{q['id']}. {q_text}**",
                options=list(options_map.keys()),
                index=0,
                key=f"q_{q['id']}",
                help="Select the frequency matching your mood over the past two weeks."
            )
            answers[str(q["id"])] = options_map[ans]
            st.markdown("<br>", unsafe_allow_html=True)
            
    if gad_questions:
        st.markdown("---")
        st.header(t("assess_sec2"))
        st.caption(t("assess_caption_2weeks"))
        for q in gad_questions:
            q_text = t(f"q{q['id']}")
            ans = st.radio(
                f"**{q['id']}. {q_text}**",
                options=list(options_map.keys()),
                index=0,
                key=f"q_{q['id']}",
                help="Select the frequency matching your stress response over the past two weeks."
            )
            answers[str(q["id"])] = options_map[ans]
            st.markdown("<br>", unsafe_allow_html=True)

    if pss_questions:
        st.markdown("---")
        st.header(t("assess_sec3"))
        st.caption(t("assess_caption_month"))
        for q in pss_questions:
            q_text = t(f"q{q['id']}")
            ans = st.radio(
                f"**{q['id']}. {q_text}**",
                options=list(pss_options_map.keys()),
                index=0,
                key=f"q_{q['id']}",
                help="Select the frequency matching your perceived coping capability over the past month."
            )
            answers[str(q["id"])] = pss_options_map[ans]
            st.markdown("<br>", unsafe_allow_html=True)
            
    st.markdown("---")
    submitted = st.form_submit_button(t("assess_submit"), use_container_width=True, help="Calculate your mood, anxiety, and perceived stress score index.")
    
    if submitted:
        payload = {
            "answers_json": json.dumps(answers)
        }
        res = api_client.request("POST", "assessment/", json_data=payload)
        if res and res.status_code == 200:
            result = res.json()
            st.success(t("assess_success"))
            
            # Show stress analysis breakdown card
            level = result["overall_level"].upper()
            card_classes = {
                "MILD": "card-sage",
                "MODERATE": "card-gold",
                "SEVERE": "card-rose"
            }
            card_class = card_classes.get(level, "card-lavender")
            
            res_hdr = t("assess_result_hdr")
            pressure_lbl = t("assess_pressure_lvl")
            breakdown_lbl = t("assess_breakdown_lbl")
            
            st.markdown(
                f"""
                <div class="{card_class}">
                    <h3>{res_hdr}: <span>{level} {pressure_lbl}</span></h3>
                    <p>{breakdown_lbl}</p>
                    <ul>
                        <li><b>PHQ-9 Score (Mood):</b> {result['phq_score']} / 27</li>
                        <li><b>GAD-7 Score (Anxiety):</b> {result['gad_score']} / 21</li>
                        <li><b>PSS-4 Score (Perceived Stress):</b> {result['pss_score']} / 12</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if level == "SEVERE":
                st.warning(t("assess_severe_warn"))
            elif level == "MODERATE":
                st.info(t("assess_moderate_info"))
            else:
                st.info(t("assess_mild_info"))
        else:
            st.error("Failed to submit assessment. Please check backend log errors.")
