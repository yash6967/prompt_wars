import os
import sys
import datetime
import streamlit as st

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from frontend.utils import session, api_client, theme
from frontend.utils.translations import t

st.set_page_config(
    page_title="Saathi — Student Mental Wellness Tracker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

theme.setup_page_theme()

session.init_session()

if not session.is_logged_in():
    st.title("🧠 SAATHI")
    sub_title = "आपका सहानुभूतिपूर्ण परीक्षा साथी और कल्याण ट्रैकर" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Your Empathetic Exam Companion & Wellness Tracker"
    st.subheader(sub_title)
    
    tab1, tab2 = st.tabs([t("login"), t("register")])
    
    with tab1:
        login_header = "अपने खाते में लॉगिन करें" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Login to Your Account"
        st.markdown(f"### {login_header}")
        email = st.text_input(t("email"), key="login_email", help="Enter your registered email address.")
        password = st.text_input(t("password"), type="password", key="login_password", help="Enter your account password.")
        if st.button(t("login"), use_container_width=True):
            if session.login(email, password):
                success_msg = "सफलतापूर्वक लॉगिन हो गया! डैशबोर्ड पर जाएं।" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Successfully logged in! Head over to the Dashboard."
                st.success(success_msg)
                st.rerun()
            else:
                err_msg = "गलत ईमेल या पासवर्ड।" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Incorrect email or password."
                st.error(err_msg)
                
    with tab2:
        reg_header = "नया छात्र खाता पंजीकृत करें" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Register New Student Account"
        st.markdown(f"### {reg_header}")
        name = st.text_input(t("name"), key="reg_name", help="Enter your full name.")
        reg_email = st.text_input(t("email"), key="reg_email", help="Enter a valid email address.")
        reg_password = st.text_input(t("password"), type="password", key="reg_password", help="Create a secure password.")
        exam_target = st.selectbox(t("exam_target"), ["JEE Main", "NEET UG", "CUET UG", "CAT", "GATE", "UPSC", "Boards", "Other"], help="Select the target examination you are preparing for.")
        exam_date = st.date_input(t("exam_date"), datetime.date.today() + datetime.timedelta(days=120), help="Select the scheduled or expected date of the examination.")
        
        if st.button(t("register"), use_container_width=True):
            exam_datetime = datetime.datetime.combine(exam_date, datetime.time.min).isoformat()
            if session.register(name, reg_email, reg_password, exam_target, exam_datetime):
                success_reg = "सफलतापूर्वक पंजीकृत और लॉग इन किया गया!" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Successfully registered and logged in!"
                st.success(success_reg)
                st.rerun()
            else:
                err_reg = "पंजीकरण विफल रहा। ईमेल पहले से उपयोग में हो सकता है।" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Failed to register. Email may already be in use."
                st.error(err_reg)
else:
    user = st.session_state["user"]
    welcome_msg = f"🧠 साथी में आपका स्वागत है, {user['name']}!" if st.session_state.get("language") == "Hindi (हिन्दी)" else f"🧠 Welcome to Saathi, {user['name']}!"
    st.title(welcome_msg)
    
    target_exam_lbl = f"आपका लक्ष्य: <b>{user['exam_target']}</b>" if st.session_state.get("language") == "Hindi (हिन्दी)" else f"Your Target: <b>{user['exam_target']}</b>"
    prep_helper_lbl = "आपका तैयारी सहायक सक्रिय है। सभी सुविधाओं तक पहुँचने के लिए साइडबार नेविगेशन पर जाएँ:" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Your preparation helper is active. Head to the sidebar navigation to access all features:"
    
    features_html = f"""
        <div class="card-lavender" role="region" aria-label="Target Exam & Features Directory">
            <h4>{target_exam_lbl}</h4>
            <p>{prep_helper_lbl}</p>
            <ul>
                <li>📊 <b>{t('nav_dashboard')}</b></li>
                <li>📝 <b>{t('nav_mood')}</b></li>
                <li>📋 <b>{t('nav_assessment')}</b></li>
                <li>📖 <b>{t('nav_ai_story')}</b></li>
                <li>💬 <b>{t('nav_ai_chat')}</b></li>
                <li>📅 <b>{t('nav_calendar')}</b></li>
                <li>⏳ <b>{t('nav_activity')}</b></li>
                <li>🤝 <b>{t('nav_subtle_ally')}</b></li>
            </ul>
        </div>
    """
    st.markdown(features_html, unsafe_allow_html=True)
    
    tip_res = api_client.request("GET", "ai/tip")
    if tip_res and tip_res.status_code == 200:
        tip_lbl = "दैनिक सलाह" if st.session_state.get("language") == "Hindi (हिन्दी)" else "Daily Tip"
        st.info(f"💡 **{tip_lbl}:** {tip_res.json().get('tip')}")
        
    if st.button(t("logout")):
        session.logout()
        st.rerun()
