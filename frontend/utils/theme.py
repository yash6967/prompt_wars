import streamlit as st

def setup_page_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Global Page Background & Text Styling */
        html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
            background-color: #FAF4EE !important;
            color: #2C2724 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Sidebar Styling Override */
        [data-testid="stSidebar"] {
            background-color: #F3EBE3 !important;
            border-right: 1px solid rgba(44, 39, 36, 0.05);
        }
        
        [data-testid="stSidebar"] * {
            color: #2C2724 !important;
        }
        
        /* Typography overrides */
        h1, h2, h3, h4, h5, h6, .title-text {
            font-family: 'Outfit', sans-serif !important;
            color: #2C2724 !important;
            font-weight: 800 !important;
        }
        
        /* Custom Modern Pastel Cards */
        .card-lavender {
            background-color: #E3E5F8 !important;
            color: #2C2724 !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }
        
        .card-gold {
            background-color: #F7ECCB !important;
            color: #2C2724 !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }
        
        .card-sage {
            background-color: #E1ECE6 !important;
            color: #2C2724 !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }
        
        .card-rose {
            background-color: #F7E5E1 !important;
            color: #2C2724 !important;
            padding: 24px;
            border-radius: 24px;
            border: none;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.02);
        }
        
        /* General Streamlit button customization */
        div.stButton > button {
            background-color: #2C2724 !important;
            color: #FAF4EE !important;
            border-radius: 12px !important;
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(44, 39, 36, 0.15);
            background-color: #403A36 !important;
        }
        
        /* Metric block styling override */
        [data-testid="stMetricValue"] {
            color: #2C2724 !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: rgba(44, 39, 36, 0.7) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
