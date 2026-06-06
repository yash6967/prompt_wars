import streamlit as st

def setup_page_theme():
    # Initialize session state for theme
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Light"
        
    # Render toggle in sidebar
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        theme_mode = st.radio(
            "🌓 Theme Mode",
            ["Light", "Dark"],
            index=0 if st.session_state["theme_mode"] == "Light" else 1,
            help="Switch between soft cream light mode and high contrast dark mode."
        )
        if theme_mode != st.session_state["theme_mode"]:
            st.session_state["theme_mode"] = theme_mode
            st.rerun()
            
    is_dark = st.session_state["theme_mode"] == "Dark"
    
    if is_dark:
        bg_color = "#1F1A17"
        text_color = "#FAF4EE"
        sidebar_bg = "#2C2724"
        card_lavender = "#2B2D42"
        card_gold = "#3F3D2F"
        card_sage = "#2A3530"
        card_rose = "#3B2B28"
        btn_bg = "#FAF4EE"
        btn_text = "#1F1A17"
        btn_hover = "#EBE5DF"
        metric_label = "rgba(250, 244, 238, 0.7)"
        border_color = "rgba(250, 244, 238, 0.15)"
        input_bg = "#2C2724"
        popover_bg = "#3F3935"
    else:
        bg_color = "#FAF4EE"
        text_color = "#2C2724"
        sidebar_bg = "#F3EBE3"
        card_lavender = "#E3E5F8"
        card_gold = "#F7ECCB"
        card_sage = "#E1ECE6"
        card_rose = "#F7E5E1"
        btn_bg = "#FFFFFF"
        btn_text = "#2C2724"
        btn_hover = "#F3EBE3"
        metric_label = "rgba(44, 39, 36, 0.7)"
        border_color = "rgba(44, 39, 36, 0.15)"
        input_bg = "#FFFFFF"
        popover_bg = "#FFFFFF"

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Global Page Background & Text Styling */
        html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }}
        
        /* Sidebar Styling Override */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {border_color};
        }}
        
        [data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        
        /* Typography overrides */
        h1, h2, h3, h4, h5, h6, .title-text, p, span, li, label, div {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: {text_color} !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
        }}
        
        /* Custom Modern Pastel Cards */
        .card-lavender {{
            background-color: {card_lavender} !important;
            color: {text_color} !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }}
        
        .card-gold {{
            background-color: {card_gold} !important;
            color: {text_color} !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }}
        
        .card-sage {{
            background-color: {card_sage} !important;
            color: {text_color} !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }}
        
        .card-rose {{
            background-color: {card_rose} !important;
            color: {text_color} !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }}
        
        /* General Streamlit button customization */
        div.stButton > button {{
            background-color: {btn_bg} !important;
            color: {btn_text} !important;
            border-radius: 12px !important;
            border: 1px solid {border_color} !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.15);
            background-color: {btn_hover} !important;
        }}
        
        /* Metric block styling override */
        [data-testid="stMetricValue"] {{
            color: {text_color} !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {metric_label} !important;
        }}
        
        /* Input overrides for absolute styling control in Light/Dark modes */
        .stTextInput input, .stPasswordInput input, .stNumberInput input, .stTextArea textarea, 
        div[data-baseweb="select"], div[data-baseweb="input"] input, textarea[data-baseweb="textarea"] {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px !important;
        }}
        
        /* Form borders customization */
        div[data-testid="stForm"] {{
            border: 1px solid {border_color} !important;
            border-radius: 24px !important;
            padding: 24px !important;
            background-color: transparent !important;
        }}
        
        /* Dropdown options popover text and background overrides */
        div[data-baseweb="popover"] *, ul[role="listbox"] *, [data-testid="stSelectbox"] * {{
            background-color: {popover_bg} !important;
            color: {text_color} !important;
        }}
        
        /* Multi-select tag item chips styling */
        div[data-baseweb="tag"] {{
            background-color: {card_lavender} !important;
            color: {text_color} !important;
            border-radius: 8px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
