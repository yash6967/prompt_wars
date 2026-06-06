import streamlit as st
from frontend.utils import session, api_client, theme

st.set_page_config(page_title="AI Wellness Mirror — Saathi", layout="wide")
theme.setup_page_theme()

if not session.is_logged_in():
    st.warning("⚠️ Please login from the Home page first.")
    st.stop()

st.title("📖 Relatable Narrative Mirror")
st.markdown("We generate unique, perspective-shifting stories tailored to your exact target exam goals and recent mood self-reports.")

if st.button("Generate My Preparation Journey Story", use_container_width=True):
    with st.spinner("Generating your story..."):
        res = api_client.request("GET", "ai/story")
        if res and res.status_code == 200:
            story_data = res.json()
            story_text = story_data.get("story", "")
            
            st.markdown("---")
            # Present chapters neatly
            chapters = story_text.split("\n\n")
            card_styles = ["card-lavender", "card-gold", "card-sage"]
            for idx, chapter in enumerate(chapters):
                if chapter.strip():
                    card_class = card_styles[idx % len(card_styles)]
                    # Parse out title if present
                    lines = chapter.strip().split("\n")
                    title = lines[0]
                    content = "\n".join(lines[1:]) if len(lines) > 1 else ""
                    
                    if "chapter" in title.lower() or ":" in title:
                        st.markdown(
                            f"""
                            <div class="{card_class}">
                                <h3>{title}</h3>
                                <p style="font-size: 1.1rem; line-height: 1.6;">{content}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="{card_class}">
                                <p style="font-size: 1.1rem; line-height: 1.6;">{chapter}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            
            # Simple interaction feedback
            st.markdown("---")
            st.write("Does this story mirror any of your current feelings?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes, this feels relatable"):
                    st.success("Thank you for sharing. Recognizing these patterns is a huge step in wellness.")
            with col2:
                if st.button("👎 Not quite like my day today"):
                    st.info("No worries! Stories adapt dynamically to your daily mood logs. Try checking in tomorrow.")
        else:
            st.error("Failed to generate story. Make sure you have checked in your mood today first.")
