import streamlit as st
import random
from datetime import datetime
from data_storage import session_storage
from PIL import Image

icon = Image.open("assets/logo.png")

# Page configuration
st.set_page_config(
    page_title="PAUSE - Focus Smart. Live Well.",
    page_icon=icon,
    layout="wide"
)

# Custom CSS for modern purple/white theme - REDESIGNED
st.markdown("""
<style>
    /* Modern purple theme - Enhanced for Control Center */
    :root {
        --primary-purple: #8A2BE2;
        --light-purple: #E6E6FA;
        --lighter-purple: #F5F0FF;
        --dark-purple: #4B0082;
        --white: #FFFFFF;
        --light-gray: #F8F9FA;
        --text-dark: #333333;
        --text-light: #666666;
        --card-shadow: 0 10px 30px rgba(138, 43, 226, 0.08);
        --hero-gradient: linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%);
        --card-hover-shadow: 0 20px 40px rgba(138, 43, 226, 0.15);
    }
    
    /* Main container - Cleaner */
    .main {
        background: linear-gradient(135deg, #F9F5FF 0%, #FFFFFF 100%);
        padding: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* App Title/Branding Styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: var(--text-light);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Hero Section Styling - REDESIGNED */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        margin-bottom: 2rem;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.08) 0%, rgba(75, 0, 130, 0.08) 100%);
        border: 1px solid rgba(138, 43, 226, 0.15);
        box-shadow: 0 20px 60px rgba(138, 43, 226, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, var(--primary-purple), var(--dark-purple));
        border-radius: 28px 28px 0 0;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.8rem;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: var(--text-dark);
        margin-bottom: 2.5rem;
        font-weight: 400;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }
    

    
    /* Hero CTA Button */
    .hero-cta-button {
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        color: white;
        border: none;
        border-radius: 18px;
        padding: 20px 50px;
        font-size: 1.4rem;
        font-weight: 700;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 15px 35px rgba(138, 43, 226, 0.25);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .hero-cta-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, var(--dark-purple), var(--primary-purple));
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }
    
    .hero-cta-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(138, 43, 226, 0.35);
    }
    
    .hero-cta-button:hover::before {
        opacity: 1;
    }
    
    .hero-cta-button:active {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(138, 43, 226, 0.3);
    }
    
    /* Primary CTA Button */
    .primary-cta {
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        color: white;
        border: none;
        border-radius: 16px;
        padding: 18px 40px;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 10px 20px rgba(138, 43, 226, 0.2);
    }
    
    .primary-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(138, 43, 226, 0.3);
    }
    
    /* Modern card design - Cleaner */
    .control-card {
        background: var(--white);
        border-radius: 20px;
        padding: 25px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .control-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--card-hover-shadow);
    }
    
    .control-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-purple), var(--dark-purple));
        border-radius: 20px 20px 0 0;
    }
    
    /* KPI Cards - Minimal */
    .kpi-card {
        background: var(--white);
        border-radius: 16px;
        padding: 20px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(138, 43, 226, 0.12);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--dark-purple);
        margin: 10px 0 5px 0;
        line-height: 1;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    /* Navigation Cards */
    .nav-card {
        background: var(--white);
        border-radius: 20px;
        padding: 25px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        text-align: center;
        cursor: pointer;
    }
    
    .nav-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--card-hover-shadow);
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.02), rgba(75, 0, 130, 0.02));
    }
    
    .nav-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .nav-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--dark-purple);
        margin-bottom: 10px;
    }
    
    .nav-description {
        font-size: 0.9rem;
        color: var(--text-light);
        line-height: 1.4;
    }
    
    /* Quote card - Minimal */
    .quote-card-minimal {
        background: linear-gradient(135deg, var(--lighter-purple), var(--white));
        border-radius: 20px;
        padding: 25px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .quote-text-minimal {
        font-size: 1.1rem;
        font-style: italic;
        color: var(--text-dark);
        line-height: 1.6;
        margin-bottom: 10px;
        position: relative;
        z-index: 1;
    }
    
    .quote-author-minimal {
        text-align: right;
        color: var(--primary-purple);
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--dark-purple);
        margin: 2rem 0 1rem 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(138, 43, 226, 0.1);
    }
    
    /* Secondary button */
    .secondary-button {
        background: transparent;
        color: var(--primary-purple);
        border: 2px solid var(--primary-purple);
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .secondary-button:hover {
        background: var(--primary-purple);
        color: white;
        transform: translateY(-2px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Streamlit button overrides */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
    }
    
    /* Hero CTA Button specific styling */
    .hero-cta-button {
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        color: white;
        border: none;
        border-radius: 18px;
        padding: 20px 50px;
        font-size: 1.4rem;
        font-weight: 700;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 15px 35px rgba(138, 43, 226, 0.25);
        position: relative;
        overflow: hidden;
        z-index: 1;
        width: auto;
        margin: 0 auto;
    }
    
    .hero-cta-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, var(--dark-purple), var(--primary-purple));
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }
    
    .hero-cta-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(138, 43, 226, 0.35);
    }
    
    .hero-cta-button:hover::before {
        opacity: 1;
    }
    
    .hero-cta-button:active {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(138, 43, 226, 0.3);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.8rem;
        }
        .subtitle {
            font-size: 1.1rem;
        }
        .hero-title {
            font-size: 2.8rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
        .hero-section {
            padding: 2.5rem 1.5rem;
        }

        .kpi-value {
            font-size: 2rem;
        }
        .main {
            padding: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-title {
            font-size: 2.2rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        .hero-title {
            font-size: 2.2rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .hero-section {
            padding: 2rem 1rem;
        }

    }
    
    /* Animation for focus */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation has been removed
# Daily target setting moved to Timer page for better context

# Import pandas for data handling
import pandas as pd

# Main app layout - REDESIGNED CONTROL CENTER

# RESTORE PAUSE BRANDING
st.markdown('<h1 class="main-title">PAUSE</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Focus smart. Live well.</p>', unsafe_allow_html=True)

# ============================================
# SECTION 1: INTRODUCTION CARD
# ============================================

# Create introduction card using Streamlit container
with st.container():
    st.markdown("""
    <div style="
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.08);
        border: 1px solid rgba(138, 43, 226, 0.1);
        margin-bottom: 20px;
    ">
        <h1 style="color: #4B0082; margin-top: 0; font-size: 2.5rem;">PAUSE</h1>
        <h3 style="color: #666; margin-top: 0; font-weight: 400;">Focus smarter. Build healthier study habits.</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #333;">
            PAUSE is an AI-powered productivity assistant that helps students manage focus sessions, 
            build productive routines, track performance trends, and prevent burnout through intelligent analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SECTION 2: PRIMARY CTA BUTTON
# ============================================

# Start Focus Session Button - Full width, prominent
st.markdown("""
<style>
    .primary-cta-button {
        width: 100%;
        margin: 0 auto 30px auto;
        display: block;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #8A2BE2, #4B0082);
        color: white;
        border: none;
        border-radius: 18px;
        padding: 25px 30px;
        font-size: 1.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 15px 35px rgba(138, 43, 226, 0.25);
        width: 100%;
        margin: 0 auto;
        display: block;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(138, 43, 226, 0.35);
        background: linear-gradient(135deg, #4B0082, #8A2BE2);
    }
</style>
""", unsafe_allow_html=True)

# Primary CTA Button
if st.button("🚀 Start Focus Session", key="hero_cta", type="primary", use_container_width=True):
    st.switch_page("pages/1_Timer.py")

# ============================================
# SECTION 3: QUICK ACCESS CARDS
# ============================================

st.markdown("""
<div style="
    font-size: 1.5rem;
    font-weight: 700;
    color: #4B0082;
    margin: 2rem 0 1rem 0;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(138, 43, 226, 0.1);
">
    🚀 Quick Access
</div>
""", unsafe_allow_html=True)

# Create Quick Access cards in 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    # Timer Card
    with st.container():
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(138, 43, 226, 0.08);
            border: 1px solid rgba(138, 43, 226, 0.1);
            transition: all 0.3s ease;
            height: 100%;
            text-align: center;
        ">
            <div style="font-size: 3rem; margin-bottom: 15px;">⏱️</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #4B0082; margin-bottom: 10px;">
                Timer
            </div>
            <div style="font-size: 0.9rem; color: #666; line-height: 1.4; margin-bottom: 20px;">
                Start and manage focus sessions.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Timer button that actually navigates
        if st.button("Open Timer", key="timer_quick_access", use_container_width=True):
            st.switch_page("pages/1_Timer.py")

with col2:
    # Analytics Card
    with st.container():
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(138, 43, 226, 0.08);
            border: 1px solid rgba(138, 43, 226, 0.1);
            transition: all 0.3s ease;
            height: 100%;
            text-align: center;
        ">
            <div style="font-size: 3rem; margin-bottom: 15px;">📊</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #4B0082; margin-bottom: 10px;">
                Analytics
            </div>
            <div style="font-size: 0.9rem; color: #666; line-height: 1.4; margin-bottom: 20px;">
                View productivity insights and performance trends.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Analytics button that actually navigates
        if st.button("View Analytics", key="analytics_quick_access", use_container_width=True):
            st.switch_page("pages/2_Analytics.py")

with col3:
    # Focus Room Card
    with st.container():
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(138, 43, 226, 0.08);
            border: 1px solid rgba(138, 43, 226, 0.1);
            transition: all 0.3s ease;
            height: 100%;
            text-align: center;
        ">
            <div style="font-size: 3rem; margin-bottom: 15px;">👥</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #4B0082; margin-bottom: 10px;">
                Focus Rooms
            </div>
            <div style="font-size: 0.9rem; color: #666; line-height: 1.4; margin-bottom: 20px;">
                Study together with friends in virtual focus rooms.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Focus Room button that actually navigates
        if st.button("Join Rooms", key="focus_room_quick_access", use_container_width=True):
            st.switch_page("pages/4_Focus_Room.py")

# Minimal Footer
st.markdown("---")
col_footer1, col_footer2 = st.columns(2)
with col_footer1:
    st.markdown("**PAUSE Control Center**")
    st.caption("Your modern productivity hub")
with col_footer2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown("**Last updated**")
    st.caption("Today, {}".format(current_time))

# Run instructions in expander (minimal)
with st.expander("ℹ️ Getting Started"):
    st.code("streamlit run app.py", language="bash")
    st.caption("Start your productivity journey with PAUSE")

print("✅ PAUSE Control Center loaded successfully!")
print("🎨 Modern, clean UI with action-oriented design")
print("🚀 Run with: streamlit run app.py")