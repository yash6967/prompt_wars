import os
import sys
import streamlit as st

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, theme

st.set_page_config(page_title="Helplines & Resources — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title("📚 Lifelines & Wellness Resources")
st.markdown("You do not have to navigate the stress of preparation alone. Keep these resources and wellness guides handy.")

# Critical Helplines Section
st.header("🚨 Emergency Mental Health Support")
st.markdown("If you are feeling extremely overwhelmed, anxious, or hopeless, please connect with a counselor immediately. They are confidential, free, and available 24/7.")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="card-rose">
            <h3 style="margin: 0; font-size: 1.25rem;">🇮🇳 AASRA Helpline</h3>
            <p style="margin: 10px 0 0 0; font-size: 1.1rem;">📞 <b>+91-9820466726</b></p>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem;">24/7 Free & Confidential Professional Support</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class="card-rose">
            <h3 style="margin: 0; font-size: 1.25rem;">🇮🇳 Kiran Mental Health Helpline</h3>
            <p style="margin: 10px 0 0 0; font-size: 1.1rem;">📞 <b>1800-599-0019</b></p>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Government of India - 24/7 Mental Health Care Line</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Prep Wellness habits Section
st.header("💡 Healthy preparation habits")

col_habit1, col_habit2, col_habit3 = st.columns(3)

with col_habit1:
    st.markdown(
        """
        <div class="card-lavender">
            <h3 style="font-size: 1.25rem; margin-top: 0;">🧠 Study Smart (Pomodoro)</h3>
            <p>Don't sit for hours without rising. Divide study times into blocks:</p>
            <ul>
                <li>Study without distractions for 25 minutes.</li>
                <li>Take a 5-minute break to drink water or walk.</li>
                <li>Repeat 4 times, then take a longer 20-minute break.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_habit2:
    st.markdown(
        """
        <div class="card-gold">
            <h3 style="font-size: 1.25rem; margin-top: 0;">💤 Sleep is Memory consolidation</h3>
            <p>Sacrificing sleep for studying reduces retention performance:</p>
            <ul>
                <li>Aim for 7 to 8 hours of sleep per night.</li>
                <li>Avoid blue light devices 30 minutes before sleep.</li>
                <li>A 15-20 min afternoon power nap can restore alertness.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_habit3:
    st.markdown(
        """
        <div class="card-sage">
            <h3 style="font-size: 1.25rem; margin-top: 0;">💬 Share the Load</h3>
            <p>Do not isolate yourself during your preparation weeks:</p>
            <ul>
                <li>Spend 15-20 minutes daily talking to a trusted sibling, parent, or friend.</li>
                <li>Focus the chat on topics unrelated to exam scores or rankings.</li>
                <li>Join peer study groups that prioritize support over competition.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.header("📚 External Wellness Articles")
st.markdown("- [Dealing with Exam Stress and Anxiety](https://www.unicef.org/india/stories/dealing-exam-stress-and-anxiety)")
st.markdown("- [The Science of Taking Breaks](https://www.psychologytoday.com/us/blog/the-brain-and-behavior/202111/the-science-taking-breaks)")
st.markdown("- [Healthy Eating and Hydration Guides for Students](https://www.nutrition.org.uk/healthy-sustainable-diets/life-stages/students/)")
