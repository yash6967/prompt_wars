import streamlit as st
import json
from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Wellness Assessment — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title("📋 Wellness Assessment")
st.markdown(
    """
    This non-clinical assessment combined of validated scales helps track your levels of:
    - **PHQ-9** (Depression symptoms)
    - **GAD-7** (Anxiety symptoms)
    - **PSS-4** (Perceived stress scale)
    
    *Your answers are confidential. Take your time.*
    """
)

# Fetch questions from backend
with st.spinner("Loading questionnaire..."):
    response = api_client.request("GET", "assessment/questions")
    if not response or response.status_code != 200:
        st.error("Failed to load questions from backend. Please ensure the backend server is running.")
        st.stop()
    questions = response.json()

options_map = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

# Perceived Stress Scale questions have slightly different standard frequencies, but 0-3 scales map directly.
# Let's show a user-friendly translation.
pss_options_map = {
    "Never": 0,
    "Almost Never": 1,
    "Sometimes": 2,
    "Fairly Often": 3
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
        st.subheader("Section 1: General Mood & Wellness (PHQ-9)")
        st.caption("Over the last 2 weeks, how often have you been bothered by any of the following problems?")
        for q in phq_questions:
            ans = st.radio(
                f"**{q['id']}. {q['text']}**",
                options=list(options_map.keys()),
                index=0,
                key=f"q_{q['id']}"
            )
            answers[str(q["id"])] = options_map[ans]
            st.markdown("<br>", unsafe_allow_html=True)
            
    if gad_questions:
        st.markdown("---")
        st.subheader("Section 2: Anxiety & Stress Response (GAD-7)")
        st.caption("Over the last 2 weeks, how often have you been bothered by any of the following problems?")
        for q in gad_questions:
            ans = st.radio(
                f"**{q['id']}. {q['text']}**",
                options=list(options_map.keys()),
                index=0,
                key=f"q_{q['id']}"
            )
            answers[str(q["id"])] = options_map[ans]
            st.markdown("<br>", unsafe_allow_html=True)

    if pss_questions:
        st.markdown("---")
        st.subheader("Section 3: Perceived Coping & Pressures (PSS-4)")
        st.caption("In the last month, how often have you felt...")
        for q in pss_questions:
            ans = st.radio(
                f"**{q['id']}. {q['text']}**",
                options=list(pss_options_map.keys()),
                index=0,
                key=f"q_{q['id']}"
            )
            answers[str(q["id"])] = pss_options_map[ans]
            st.markdown("<br>", unsafe_allow_html=True)
            
    st.markdown("---")
    submitted = st.form_submit_button("Submit Assessment & Calculate Results", use_container_width=True)
    
    if submitted:
        payload = {
            "answers_json": json.dumps(answers)
        }
        res = api_client.request("POST", "assessment/", json_data=payload)
        if res and res.status_code == 200:
            result = res.json()
            st.success("Assessment submitted successfully!")
            
            # Show stress analysis breakdown card
            level = result["overall_level"].upper()
            card_classes = {
                "MILD": "card-sage",
                "MODERATE": "card-gold",
                "SEVERE": "card-rose"
            }
            card_class = card_classes.get(level, "card-lavender")
            
            st.markdown(
                f"""
                <div class="{card_class}">
                    <h3>Assessment Result: <span>{level} Pressure Level</span></h3>
                    <p>Below is your wellness index breakdown:</p>
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
                st.warning("⚠️ Your results suggest severe pressure. We highly encourage talking to one of our listed advisors, or visiting the **Resources** and **Subtle Ally** sections.")
            elif level == "MODERATE":
                st.info("💡 You are experiencing moderate stress. Consider scheduling regular activity breaks via the **Activity Break** page.")
            else:
                st.info("✨ Great job maintaining a low stress preparation routine! Continue logging your moods to track ongoing trends.")
        else:
            st.error("Failed to submit assessment. Please check backend log errors.")
