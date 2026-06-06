import streamlit as st
import datetime
from frontend.utils import session, api_client, theme

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
    st.subheader("Your Empathetic Exam Companion & Wellness Tracker")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", use_container_width=True):
            if session.login(email, password):
                st.success("Successfully logged in! Head over to the Dashboard.")
                st.rerun()
            else:
                st.error("Incorrect email or password.")
                
    with tab2:
        st.markdown("### Register New Student Account")
        name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email Address", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        exam_target = st.selectbox("Target Exam", ["JEE Main", "NEET UG", "CUET UG", "CAT", "GATE", "UPSC", "Boards", "Other"])
        exam_date = st.date_input("Exam Date", datetime.date.today() + datetime.timedelta(days=120))
        
        if st.button("Register", use_container_width=True):
            exam_datetime = datetime.datetime.combine(exam_date, datetime.time.min).isoformat()
            if session.register(name, reg_email, reg_password, exam_target, exam_datetime):
                st.success("Successfully registered and logged in!")
                st.rerun()
            else:
                st.error("Failed to register. Email may already be in use.")
else:
    user = st.session_state["user"]
    st.title(f"🧠 Welcome to Saathi, {user['name']}!")
    
    st.markdown(
        f"""
        <div class="card-lavender">
            <h4>Your Target: <b>{user['exam_target']}</b></h4>
            <p>Your preparation helper is active. Head to the sidebar navigation to access all features:</p>
            <ul>
                <li>📊 <b>Dashboard</b>: View analytics, study/wellness balance, and alerts</li>
                <li>📝 <b>Mood Check-In</b>: Log daily emotions, energy levels, sleep & study hours</li>
                <li>📋 <b>Assessment</b>: Take PHQ-9, GAD-7, and PSS-4 wellness surveys</li>
                <li>📖 <b>AI Story</b>: Read relatable stories custom-tailored to your journey</li>
                <li>💬 <b>AI Chat</b>: Talk to Saathi, your empathetic co-pilot</li>
                <li>📅 <b>Exam Calendar</b>: Track target exams and registration checkpoints</li>
                <li>⏳ <b>Activity Break</b>: Log recovery breaks & exercise timers</li>
                <li>🤝 <b>Subtle Ally</b>: Connect parent/educator guides with privacy-first nudges</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    tip_res = api_client.request("GET", "ai/tip")
    if tip_res and tip_res.status_code == 200:
        st.info(f"💡 **Daily Tip:** {tip_res.json().get('tip')}")
        
    if st.button("Logout"):
        session.logout()
        st.rerun()
