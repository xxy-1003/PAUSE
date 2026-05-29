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
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    /* Hero Quote Container */
    .hero-quote-container {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 2rem;
        margin: 2.5rem auto 3rem auto;
        max-width: 800px;
        border: 1px solid rgba(138, 43, 226, 0.1);
        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.05);
        position: relative;
    }
    
    .hero-quote-container::before {
        content: '💭';
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        padding: 0 15px;
        font-size: 1.5rem;
    }
    
    .hero-quote-text {
        font-size: 1.4rem;
        font-style: italic;
        color: var(--text-dark);
        line-height: 1.6;
        margin-bottom: 1rem;
        position: relative;
        padding: 0 1rem;
    }
    
    .hero-quote-text::before {
        content: '"';
        position: absolute;
        left: -5px;
        top: -10px;
        font-size: 3rem;
        color: rgba(138, 43, 226, 0.2);
        font-family: Georgia, serif;
    }
    
    .hero-quote-text::after {
        content: '"';
        position: absolute;
        right: -5px;
        bottom: -20px;
        font-size: 3rem;
        color: rgba(138, 43, 226, 0.2);
        font-family: Georgia, serif;
    }
    
    .hero-quote-author {
        text-align: center;
        color: var(--primary-purple);
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
        font-style: normal;
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
        .hero-quote-container {
            padding: 1.5rem;
            margin: 2rem auto 2.5rem auto;
        }
        .hero-quote-text {
            font-size: 1.2rem;
            padding: 0 0.5rem;
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
        .hero-quote-container {
            padding: 1.2rem;
        }
        .hero-quote-text {
            font-size: 1.1rem;
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

# Helper functions for Control Center
def get_motivational_quote():
    """Return a random motivational quote - UPDATED with modern productivity quotes"""
    quotes = [
        {
            "text": "Small progress is still progress.",
            "author": "Productivity Principle"
        },
        {
            "text": "Focus on being productive, not busy.",
            "author": "Tim Ferriss"
        },
        {
            "text": "Discipline creates freedom.",
            "author": "Productivity Wisdom"
        },
        {
            "text": "Done is better than perfect.",
            "author": "Sheryl Sandberg"
        },
        {
            "text": "The key is not to prioritize what's on your schedule, but to schedule your priorities.",
            "author": "Stephen Covey"
        },
        {
            "text": "Productivity is never an accident. It is always the result of a commitment to excellence, intelligent planning, and focused effort.",
            "author": "Paul J. Meyer"
        },
        {
            "text": "Rest when you're weary. Refresh and renew yourself, your body, your mind, your spirit. Then get back to work.",
            "author": "Ralph Marston"
        },
        {
            "text": "Your mind is for having ideas, not holding them.",
            "author": "David Allen"
        },
        {
            "text": "Start where you are. Use what you have. Do what you can.",
            "author": "Arthur Ashe"
        },
        {
            "text": "The secret of getting ahead is getting started.",
            "author": "Mark Twain"
        },
        {
            "text": "Don't watch the clock; do what it does. Keep going.",
            "author": "Sam Levenson"
        },
        {
            "text": "The time to relax is when you don't have time for it.",
            "author": "Sydney J. Harris"
        },
        {
            "text": "Balance is not something you find, it's something you create.",
            "author": "Jana Kingsford"
        },
        {
            "text": "One hour of focused work is worth four hours of distracted work.",
            "author": "Deep Work Principle"
        },
        {
            "text": "The quality of your focus determines the quality of your results.",
            "author": "Focus Philosophy"
        },
        {
            "text": "Momentum builds with consistent action.",
            "author": "Productivity Insight"
        },
        {
            "text": "Clear goals lead to clear results.",
            "author": "Goal Setting Wisdom"
        },
        {
            "text": "The best time to start was yesterday. The next best time is now.",
            "author": "Proverb"
        },
        {
            "text": "Progress over perfection.",
            "author": "Modern Mantra"
        },
        {
            "text": "Your future self will thank you for starting today.",
            "author": "Self-Motivation"
        }
    ]
    return random.choice(quotes)

def get_todays_focus_time():
    """Get today's focus time from database"""
    try:
        today_summary = session_storage.get_today_summary()
        if not today_summary.empty:
            focus_hours = today_summary['total_focus_hours'].iloc[0]
            return round(focus_hours, 1) if pd.notna(focus_hours) else 0.0
    except Exception as e:
        print(f"Error getting today's focus time: {e}")
    return 0.0

def get_current_streak():
    """Get current streak from database"""
    try:
        insights = session_storage.get_advanced_insights()
        return insights.get('current_streak', 0)
    except Exception as e:
        print(f"Error getting current streak: {e}")
    return 0

# Import pandas for data handling
import pandas as pd

# Main app layout - REDESIGNED CONTROL CENTER

# RESTORE PAUSE BRANDING
st.markdown('<h1 class="main-title">PAUSE</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Focus smart. Live well.</p>', unsafe_allow_html=True)

# Get a random quote for the hero section
hero_quote = get_motivational_quote()
quote_text = hero_quote["text"]
quote_author = hero_quote["author"]

# Hero Section - FIXED with proper Streamlit structure
st.markdown('''
<div class="hero-section">
    <h1 class="hero-title">Ready to Focus?</h1>
    <p class="hero-subtitle">Build momentum. Reduce distractions. Make today meaningful.</p>
    
    <div class="hero-quote-container">
        <div class="hero-quote-text">{quote_text}</div>
        <div class="hero-quote-author">— {quote_author}</div>
    </div>
</div>
'''.format(quote_text=quote_text, quote_author=quote_author), unsafe_allow_html=True)

# Hero CTA Button - Streamlit compatible (NO raw HTML button)
col_hero1, col_hero2, col_hero3 = st.columns([1, 2, 1])
with col_hero2:
    # Add custom CSS for the hero CTA button
    st.markdown('''
    <style>
        .hero-cta-container {
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        /* Custom styling specifically for the hero CTA button */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
            color: white;
            border: none;
            border-radius: 18px;
            padding: 20px 50px;
            font-size: 1.4rem;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 15px 35px rgba(138, 43, 226, 0.25);
            width: 100%;
            max-width: 400px;
            margin: 0 auto;
            display: block;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(138, 43, 226, 0.35);
            background: linear-gradient(135deg, var(--dark-purple), var(--primary-purple));
        }
    </style>
    <div class="hero-cta-container">
    ''', unsafe_allow_html=True)
    
    # Hero CTA Button
    if st.button("🚀 Start Focus Session", key="hero_cta", type="primary"):
        st.switch_page("pages/1_Timer.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# SECTION 1: Minimal KPI Cards (Only 2 important KPIs)
st.markdown('<div class="section-header">📊 Today\'s Progress</div>', unsafe_allow_html=True)

# Get real data from database
today_focus_time = get_todays_focus_time()
current_streak = get_current_streak()

col_kpi1, col_kpi2 = st.columns(2)

with col_kpi1:
    message = "" if today_focus_time > 0 else "Start your first session!"
    if message:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Today's Focus Time</div>
            <div class="kpi-value">{today_focus_time}h</div>
            <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 5px;">
                {message}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Today's Focus Time</div>
            <div class="kpi-value">{today_focus_time}h</div>
        </div>
        ''', unsafe_allow_html=True)

with col_kpi2:
    streak_emoji = "🔥" if current_streak >= 7 else "⚡" if current_streak >= 3 else "📈"
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Current Streak</div>
        <div class="kpi-value">{current_streak} days</div>
        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 5px;">
            {streak_emoji} Keep it going!
        </div>
    </div>
    ''', unsafe_allow_html=True)

# SECTION 2: Quick Access Navigation
st.markdown('<div class="section-header">🚀 Quick Access</div>', unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    st.markdown('''
    <div class="nav-card">
        <div class="nav-icon">⏱️</div>
        <div class="nav-title">Focus Timer</div>
        <div class="nav-description">Pomodoro timer with session tracking</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("Start Timer →", key="nav_timer", use_container_width=True):
        st.switch_page("pages/1_Timer.py")

with col_nav2:
    st.markdown('''
    <div class="nav-card">
        <div class="nav-icon">📊</div>
        <div class="nav-title">Analytics</div>
        <div class="nav-description">Detailed insights & charts</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("View Analytics →", key="nav_analytics", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")

with col_nav3:
    st.markdown('''
    <div class="nav-card">
        <div class="nav-icon">🧘</div>
        <div class="nav-title">Wellness</div>
        <div class="nav-description">Mindfulness & balance tools</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("Go to Wellness →", key="nav_wellness", use_container_width=True):
        st.switch_page("pages/3_Wellness.py")

with col_nav4:
    st.markdown('''
    <div class="nav-card">
        <div class="nav-icon">📝</div>
        <div class="nav-title">Tasks</div>
        <div class="nav-description">Coming soon</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("Explore →", key="nav_tasks", use_container_width=True, disabled=True):
        pass

# SECTION 3: Quick Actions (Optional)
st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)

col_action1, col_action2, col_action3 = st.columns(3)

with col_action1:
    if st.button("🎯 Set Daily Goal", key="set_goal", use_container_width=True):
        st.info("Daily goal setting feature coming soon!")

with col_action2:
    if st.button("📈 View Weekly Report", key="weekly_report", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")

with col_action3:
    if st.button("🧠 Take a Break", key="take_break", use_container_width=True):
        st.info("Break timer feature coming soon!")

# Minimal Footer
st.markdown("---")
col_footer1, col_footer2 = st.columns(2)
with col_footer1:
    st.markdown("**PAUSE Control Center**")
    st.caption("Your modern productivity hub")
with col_footer2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"**Last updated**")
    st.caption(f"Today, {current_time}")

# Run instructions in expander (minimal)
with st.expander("ℹ️ Getting Started"):
    st.code("streamlit run app.py", language="bash")
    st.caption("Start your productivity journey with PAUSE")

print("✅ PAUSE Control Center loaded successfully!")
print("🎨 Modern, clean UI with action-oriented design")
print("🚀 Run with: streamlit run app.py")