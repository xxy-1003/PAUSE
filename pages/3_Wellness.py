import streamlit as st
import random

st.title("Wellness")

# Page configuration for Wellness page
st.set_page_config(
    page_title="PAUSE - Wellness",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern purple/white theme (same as main app)
st.markdown("""
<style>
    /* Modern purple theme */
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
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #F9F5FF 0%, #FFFFFF 100%);
        padding: 2rem;
    }
    
    /* Title styling */
    .main-title {
        font-size: 4rem;
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
        font-size: 1.5rem;
        color: var(--text-light);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Modern card design */
    .stat-card {
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
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(138, 43, 226, 0.12);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-purple), var(--dark-purple));
        border-radius: 20px 20px 0 0;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--dark-purple);
        margin: 10px 0 5px 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .metric-change {
        font-size: 0.85rem;
        padding: 4px 10px;
        border-radius: 15px;
        display: inline-block;
        font-weight: 500;
    }
    
    .positive {
        background-color: rgba(76, 175, 80, 0.1);
        color: #4CAF50;
    }
    
    .negative {
        background-color: rgba(244, 67, 54, 0.1);
        color: #F44336;
    }
    
    /* Quote card */
    .quote-card {
        background: linear-gradient(135deg, var(--lighter-purple), var(--white));
        border-radius: 20px;
        padding: 30px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .quote-card::before {
        content: '"';
        position: absolute;
        top: 10px;
        left: 20px;
        font-size: 6rem;
        color: rgba(138, 43, 226, 0.1);
        font-family: Georgia, serif;
        line-height: 1;
    }
    
    .quote-text {
        font-size: 1.2rem;
        font-style: italic;
        color: var(--text-dark);
        line-height: 1.6;
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }
    
    .quote-author {
        text-align: right;
        color: var(--primary-purple);
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Chart container */
    .chart-container {
        background: var(--white);
        border-radius: 20px;
        padding: 25px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
    }
    
    /* Wellness gauge styling */
    .gauge-container {
        text-align: center;
        padding: 20px;
    }
    
    .gauge-value {
        font-size: 3rem;
        font-weight: 800;
        color: var(--dark-purple);
        margin: 10px 0;
    }
    
    .gauge-label {
        font-size: 1rem;
        color: var(--text-light);
        margin-bottom: 20px;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 3rem;
        }
        .subtitle {
            font-size: 1.2rem;
        }
        .metric-value {
            font-size: 2.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Wellness data functions
def get_motivational_quote():
    """Return a random motivational quote"""
    quotes = [
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
            "text": "The time to relax is when you don't have time for it.",
            "author": "Sydney J. Harris"
        },
        {
            "text": "Balance is not something you find, it's something you create.",
            "author": "Jana Kingsford"
        },
        {
            "text": "Focus on being productive instead of busy.",
            "author": "Tim Ferriss"
        },
        {
            "text": "Your mind is for having ideas, not holding them.",
            "author": "David Allen"
        },
        {
            "text": "Self-care is not selfish. You cannot serve from an empty vessel.",
            "author": "Eleanor Brown"
        },
        {
            "text": "Almost everything will work again if you unplug it for a few minutes, including you.",
            "author": "Anne Lamott"
        },
        {
            "text": "The greatest wealth is health.",
            "author": "Virgil"
        }
    ]
    return random.choice(quotes)

def get_wellness_tips():
    """Return wellness tips"""
    tips = [
        "💧 Drink a glass of water - hydration improves focus by 15%",
        "👀 Follow the 20-20-20 rule: Every 20 minutes, look at something 20 feet away for 20 seconds",
        "🧘 Try a 5-minute meditation to reset your mind",
        "🌿 Take a short walk outside - natural light boosts mood and energy",
        "📝 Write down 3 things you're grateful for today",
        "🎵 Listen to calming music or nature sounds for 10 minutes",
        "💆‍♂️ Do some gentle neck and shoulder stretches",
        "🌱 Practice deep breathing: 4 seconds in, hold 4, 4 seconds out",
        "📱 Take a 30-minute digital detox - no screens!",
        "🍎 Have a healthy snack - nuts, fruits, or yogurt"
    ]
    return random.sample(tips, 3)

# Page title
st.markdown("<h1 class='main-title'>PAUSE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Wellness & Mindfulness 🧘</p>", unsafe_allow_html=True)

# Navigation back to Dashboard
col_nav, col_empty = st.columns([1, 3])
with col_nav:
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.switch_page("app.py")

# Fallback Navigation Section
st.markdown("<br>")
st.markdown("### 🔗 Quick Navigation")
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("⏱️ Timer", use_container_width=True):
        st.switch_page("pages/1_Timer.py")
with nav_col2:
    if st.button("📊 Analytics", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")
with nav_col3:
    if st.button("🧘 Wellness", use_container_width=True, disabled=True):
        pass  # Current page, so disabled

st.markdown("<br>", unsafe_allow_html=True)

# Wellness Overview Cards
st.markdown("### 🌿 Your Wellness Dashboard")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Mindfulness Score</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">85%</div>', unsafe_allow_html=True)
    st.markdown('<span class="metric-change positive">🎯 Excellent</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Sleep Quality</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">7.2h</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">avg per night</div>', unsafe_allow_html=True)
    st.markdown('<span class="metric-change positive">+0.5h this week</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Stress Level</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">Low</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">on a scale of 1-10: 3</div>', unsafe_allow_html=True)
    st.markdown('<span class="metric-change positive">↓ 2 points</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Energy Level</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">8/10</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">feeling energized</div>', unsafe_allow_html=True)
    st.markdown('<span class="metric-change positive">↑ 15% today</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Wellness Content
col_quote, col_burnout = st.columns([1, 1])

with col_quote:
    st.markdown('<div class="quote-card">', unsafe_allow_html=True)
    st.markdown("### 💭 Daily Inspiration")
    
    # Get and display motivational quote
    quote = get_motivational_quote()
    st.markdown(f'<div class="quote-text">{quote["text"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quote-author">— {quote["author"]}</div>', unsafe_allow_html=True)
    
    # Refresh quote button
    if st.button("🔄 New Quote", use_container_width=True):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick wellness actions
    st.markdown("<br>")
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Wellness Actions")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🧘 5-min Meditation", use_container_width=True):
            st.success("Starting 5-minute meditation... Find a quiet space.")
    with col_btn2:
        if st.button("🌿 Nature Break", use_container_width=True):
            st.info("Step outside for 10 minutes of fresh air")
    
    if st.button("💆‍♀️ Stretch Session", use_container_width=True):
        st.info("Follow along with gentle stretching exercises")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_burnout:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 🔥 Burnout Risk Assessment")
    
    # Burnout risk gauge
    burnout_risk = 25  # Low risk
    
    st.markdown(f"""
    <div class="gauge-container">
        <div class="gauge-label">Current Burnout Risk</div>
        <div class="gauge-value">{burnout_risk}%</div>
        <div style="background: #E6E6FA; height: 20px; border-radius: 10px; overflow: hidden; margin: 20px 0;">
            <div style="background: linear-gradient(90deg, #4CAF50, #FFC107, #F44336); 
                        width: 100%; height: 100%; position: relative;">
                <div style="position: absolute; left: {burnout_risk}%; top: -5px; width: 4px; height: 30px; 
                            background: #4B0082; border-radius: 2px;"></div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #666666;">
            <div>Low</div>
            <div>Moderate</div>
            <div>High</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Burnout factors
    st.markdown("#### Factors contributing to your score:")
    
    factors = [
        {"name": "Work-Life Balance", "score": 85, "status": "Good"},
        {"name": "Sleep Quality", "score": 72, "status": "Fair"},
        {"name": "Stress Management", "score": 90, "status": "Excellent"},
        {"name": "Social Connection", "score": 65, "status": "Needs attention"},
        {"name": "Physical Activity", "score": 80, "status": "Good"}
    ]
    
    for factor in factors:
        color = "#4CAF50" if factor["score"] >= 80 else "#FFC107" if factor["score"] >= 60 else "#F44336"
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-weight: 600;">{factor['name']}</span>
                <span style="color: {color}; font-weight: 600;">{factor['status']}</span>
            </div>
            <div style="background: #E6E6FA; height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: {color}; width: {factor['score']}%; height: 100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.caption("Monitor these factors regularly to maintain healthy work-life balance")
    st.markdown('</div>', unsafe_allow_html=True)

# Wellness Tips Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 🌱 Personalized Wellness Tips")

tips = get_wellness_tips()
for i, tip in enumerate(tips, 1):
    st.markdown(f"**{i}.** {tip}")

st.markdown("<br>")
col_tip1, col_tip2, col_tip3 = st.columns(3)
with col_tip1:
    if st.button("💧 Hydration Reminder", use_container_width=True):
        st.toast("💧 Time to drink water! Staying hydrated improves cognitive function.")
with col_tip2:
    if st.button("👀 Eye Rest", use_container_width=True):
        st.toast("👀 Look away from your screen for 20 seconds at something 20 feet away.")
with col_tip3:
    if st.button("🌬️ Breathing Exercise", use_container_width=True):
        st.toast("🌬️ Inhale for 4 seconds, hold for 4, exhale for 4. Repeat 5 times.")

st.markdown('</div>', unsafe_allow_html=True)

# Mindfulness Resources
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="stat-card">', unsafe_allow_html=True)
st.markdown("### 📚 Mindfulness Resources")

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.markdown("**Guided Meditations**")
    st.markdown("- 5-minute focus meditation")
    st.markdown("- 10-minute stress relief")
    st.markdown("- Sleep meditation")
with col_res2:
    st.markdown("**Wellness Articles**")
    st.markdown("- The science of breaks")
    st.markdown("- Digital detox guide")
    st.markdown("- Nutrition for focus")
with col_res3:
    st.markdown("**Tools & Apps**")
    st.markdown("- Nature sound player")
    st.markdown("- Breathing exercise timer")
    st.markdown("- Gratitude journal")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**PAUSE Wellness** • Nurture your mind and body • 🧘")