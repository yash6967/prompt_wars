import streamlit as st
import time
from datetime import datetime
from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Active Break Tracker — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title("⏳ Active Recovery & Breaks")
st.markdown("Taking regular breaks improves memory retention and keeps burnout at bay. Track your restoration activities here.")

# Fetch active advice
advice_res = api_client.request("GET", "activity/advice")
if advice_res and advice_res.status_code == 200:
    advice = advice_res.json()
    st.subheader("💡 Why Breaks Matter")
    col1, col2, col3 = st.columns(3)
    
    advice_items = list(advice.items())
    with col1:
        st.markdown(f"**🏃‍♂️ Active Exercise:**\n{advice.get('exercise')}")
        st.markdown(f"**💤 Power Naps:**\n{advice.get('nap')}")
    with col2:
        st.markdown(f"**🧘 Meditation:**\n{advice.get('meditation')}")
        st.markdown(f"**🎨 Hobbies:**\n{advice.get('hobbies')}")
    with col3:
        st.markdown(f"**🤝 Social Connection:**\n{advice.get('social')}")
        st.markdown(f"**💧 Hydration:**\n{advice.get('hydration')}")

st.markdown("---")

# Split page into timer and manual logger
col_timer, col_log = st.columns(2)

with col_timer:
    st.subheader("⏱️ Quick Break Timer")
    timer_type = st.selectbox("Choose break type:", ["Hydration Break (2 min)", "Breathing Exercise (5 min)", "Short Walk (10 min)", "Meditation (15 min)"])
    
    duration_map = {
        "Hydration Break (2 min)": 2,
        "Breathing Exercise (5 min)": 5,
        "Short Walk (10 min)": 10,
        "Meditation (15 min)": 15
    }
    target_minutes = duration_map[timer_type]
    
    # State flags to handle active running timer
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
        
    start_btn = st.button("Start Timer")
    
    if start_btn:
        st.session_state.timer_running = True
        progress_bar = st.progress(0.0)
        timer_text = st.empty()
        
        total_seconds = target_minutes * 60
        for remaining in range(total_seconds, -1, -1):
            if not st.session_state.timer_running:
                break
            mins, secs = divmod(remaining, 60)
            timer_text.markdown(f"### ⏳ Remaining Time: **{mins:02d}:{secs:02d}**")
            progress_bar.progress(1.0 - (remaining / total_seconds))
            time.sleep(1)
            
        if st.session_state.timer_running:
            st.balloons()
            st.success("🎉 Break completed! Let's log it to save your progress.")
            st.session_state.timer_running = False
            
            # Auto-log break
            act_type = timer_type.split(" ")[0].lower()
            if "walk" in act_type:
                act_type = "exercise"
            elif "breathing" in act_type:
                act_type = "meditation"
                
            payload = {
                "activity_type": act_type,
                "duration_minutes": target_minutes,
                "description": f"Completed interactive {timer_type} timer."
            }
            api_client.request("POST", "activity/log", json_data=payload)
            st.rerun()

with col_log:
    st.subheader("📝 Log a Break Manually")
    with st.form("manual_break_form"):
        activity_type = st.selectbox(
            "What activity did you do?",
            ["exercise", "meditation", "social", "hydration", "nap", "hobbies"]
        )
        duration = st.number_input("Duration (minutes):", min_value=1, max_value=120, value=10)
        description = st.text_input("Short Description:", placeholder="E.g., Walked in park, drank 2 glasses of water")
        
        submitted = st.form_submit_button("Save Entry")
        if submitted:
            payload = {
                "activity_type": activity_type,
                "duration_minutes": duration,
                "description": description
            }
            res = api_client.request("POST", "activity/log", json_data=payload)
            if res and res.status_code == 200:
                st.success("Activity logged successfully!")
                st.rerun()
            else:
                st.error("Failed to log activity.")

st.markdown("---")

# Retrieve and show today's activity stats
today_res = api_client.request("GET", "activity/today")
if today_res and today_res.status_code == 200:
    today_data = today_res.json()
    st.subheader(f"📊 Your Recovery Statistics for Today")
    st.markdown(f"⚡ **Total Recovery Time:** {today_data.get('total_duration_minutes', 0)} minutes across **{today_data.get('count', 0)}** breaks.")
    
    if today_data.get("activities"):
        # Format for displaying
        for act in today_data["activities"]:
            logged_time = datetime.fromisoformat(act["logged_at"]).strftime("%I:%M %p")
            st.markdown(
                f"""
                <div class="card-sage">
                    <b>{act['activity_type'].capitalize()}</b> ({act['duration_minutes']} mins) at {logged_time}
                    <br><span style="font-size: 0.9rem;">{act['description'] or 'No description provided'}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
