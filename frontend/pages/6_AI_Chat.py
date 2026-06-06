import os
import sys
import streamlit as st

# Resolve project root path for remote environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frontend.utils import session, api_client, theme

st.set_page_config(page_title="Saathi Co-Pilot Chat", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

user = st.session_state["user"]
st.title("💬 Talk to Saathi")
st.markdown("Your empathetic exam preparation companion. Share whatever is on your mind — preparation doubts, stress, or wins.")

# Initialize chat history from backend if not already done
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
    with st.spinner("Retrieving chat logs..."):
        res = api_client.request("GET", "ai/chat/history")
        if res and res.status_code == 200:
            st.session_state.chat_messages = res.json()
        else:
            st.error("Failed to load message history from backend.")

# Display chat messages
for msg in st.session_state.chat_messages:
    role = msg["role"]
    avatar = "🧠" if role == "assistant" else "🧑‍🎓"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

# Accept user input
user_input = st.chat_input("Message Saathi...")
if user_input:
    # Render user message
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    
    # Get reply
    with st.chat_message("assistant", avatar="🧠"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Saathi is listening...*")
        
        res = api_client.request("POST", "ai/chat", json_data={"message": user_input})
        if res and res.status_code == 200:
            reply = res.json().get("reply", "I'm here for you, but I couldn't generate a reply right now.")
            message_placeholder.markdown(reply)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            
            # Auto-rerun if safety notice might require UI refresh or just keep state
            # No rerun needed as st.chat_input does it or we append.
        else:
            message_placeholder.markdown("⚠️ Sorry, I had trouble connecting to the server. Please try again.")
