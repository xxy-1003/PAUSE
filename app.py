import streamlit as st
import random

def calculate_weekly_trend(current, previous):
    return round(((current - previous) / previous) * 100, 1)

from PIL import Image

icon = Image.open("assets/logo.png")

# Page configuration
st.set_page_config(
    page_title="PAUSE - Focus Smart. Live Well.",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern purple/white theme
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
    
    /* Timer specific styling */
    .timer-container {
        background: var(--white);
        border-radius: 20px;
        padding: 25px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
    }
    
    .timer-circle {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }
    
    .timer-progress {
        transform: rotate(-90deg);
        transform-origin: 50% 50%;
    }
    
    .timer-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    
    .timer-minutes {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--dark-purple);
        line-height: 1;
    }
    
    .timer-seconds {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-purple);
        line-height: 1;
    }
    
    .timer-label {
        font-size: 0.9rem;
        color: var(--text-light);
        margin-top: 5px;
    }
    
    /* Timer button styling */
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
    
    /* Streamlit metric styling */
    .stMetric {
        margin-bottom: 15px;
    }
    
    .stMetric > div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: var(--dark-purple) !important;
    }
    
    .stMetric > div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: var(--text-light) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .stMetric > div[data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        font-weight: 500;
    }
    
    /* Positive delta (green) */
    .stMetric > div[data-testid="stMetricDelta"] > svg {
        color: #4CAF50 !important;
    }
    
    /* Negative delta (red) */
    .stMetric > div[data-testid="stMetricDelta"][data-delta-type="decrease"] > svg {
        color: #F44336 !important;
    }
    
    /* Container spacing */
    .stContainer {
        padding: 15px 0;
        border-bottom: 1px solid rgba(138, 43, 226, 0.1);
    }
    
    .stContainer:last-child {
        border-bottom: none;
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
        .timer-circle {
            width: 150px;
            height: 150px;
        }
        .timer-minutes {
            font-size: 2rem;
        }
        .timer-seconds {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for dashboard
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
        }
    ]
    return random.choice(quotes)

# Main app layout
st.markdown("<h1 class='main-title'>PAUSE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Focus smart. Live well.</p>", unsafe_allow_html=True)

# Statistics cards - 4 cards in a row
col1, col2, col3, col4 = st.columns(4)

with col1:
    trend = calculate_weekly_trend(3.8, 3.3)
    trend_html = f'<span class="metric-change positive">+{trend}% this week</span>' if trend >= 0 else f'<span class="metric-change negative">{trend}% this week</span>'
    st.markdown(f'''
    <div class="stat-card">
        <div class="metric-label">Daily Focus Time</div>
        <div class="metric-value">3.8h</div>
        {trend_html}
    </div>
    ''', unsafe_allow_html=True)

with col2:
    trend = calculate_weekly_trend(82, 77)
    trend_html = f'<span class="metric-change positive">+{trend}% this week</span>' if trend >= 0 else f'<span class="metric-change negative">{trend}% this week</span>'
    st.markdown(f'''
    <div class="stat-card">
        <div class="metric-label">Productivity Score</div>
        <div class="metric-value">82%</div>
        {trend_html}
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown('''
    <div class="stat-card">
        <div class="metric-label">Breaks Taken</div>
        <div class="metric-value">4</div>
        <span class="metric-label">Target: 5</span>
        <span class="metric-change negative">-1 from target</span>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown('''
    <div class="stat-card">
        <div class="metric-label">Mindfulness Minutes</div>
        <div class="metric-value">15</div>
        <span class="metric-label">Daily Goal: 10min</span>
        <span class="metric-change positive">🎯 Goal achieved</span>
    </div>
    ''', unsafe_allow_html=True)

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards to Other Pages
st.markdown("### 🚀 Explore PAUSE Features")
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    st.markdown('''
    <div class="stat-card">
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-size: 3rem;">⏱️</span>
        </div>
        <div class="metric-label">Focus Timer</div>
        <div style="font-size: 1.2rem; color: var(--text-dark); margin: 15px 0; line-height: 1.4;">
            Pomodoro-style timer with start, pause, reset controls and session streak tracking
        </div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("Go to Timer →", key="nav_timer", use_container_width=True):
        st.switch_page("pages/1_Timer.py")

with col_nav2:
    st.markdown('''
    <div class="stat-card">
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-size: 3rem;">📊</span>
        </div>
        <div class="metric-label">Analytics & Insights</div>
        <div style="font-size: 1.2rem; color: var(--text-dark); margin: 15px 0; line-height: 1.4;">
            Detailed productivity charts, performance metrics, and data-driven insights
        </div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("Go to Analytics →", key="nav_analytics", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")

with col_nav3:
    st.markdown('''
    <div class="stat-card">
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-size: 3rem;">🧘</span>
        </div>
        <div class="metric-label">Wellness & Mindfulness</div>
        <div style="font-size: 1.2rem; color: var(--text-dark); margin: 15px 0; line-height: 1.4;">
            Motivational quotes, burnout risk assessment, and wellness tips
        </div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("Go to Wellness →", key="nav_wellness", use_container_width=True):
        st.switch_page("pages/3_Wellness.py")

# Quick Overview Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📋 Quick Overview")

col_overview1, col_overview2 = st.columns(2)

with col_overview1:
    # Create a container for the Today's Summary section
    with st.container():
        # Add title with emoji
        st.markdown("#### 📋 Today's Summary")
        
        # Create a styled container using custom CSS class
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Create 2x2 grid for summary metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Focus Sessions Completed
            with st.container():
                st.write("**Focus Sessions Completed**")
                st.metric(
                    label="",
                    value="2",
                    delta="2/4 sessions",
                    delta_color="off"
                )
                st.caption("Target: 4 sessions")
            
            # Productivity Score  
            with st.container():
                st.write("**Productivity Score**")
                st.metric(
                    label="",
                    value="85%",
                    delta="+5%",
                    delta_color="normal"
                )
                st.caption("Daily performance")
        
        with col2:
            # Mindfulness Minutes
            with st.container():
                st.write("**Mindfulness Minutes**")
                st.metric(
                    label="",
                    value="15",
                    delta="🎯 Goal achieved",
                    delta_color="normal"
                )
                st.caption("Daily goal: 10min")
            
            # Breaks Taken
            with st.container():
                st.write("**Breaks Taken**")
                st.metric(
                    label="",
                    value="3",
                    delta="-2 from target",
                    delta_color="inverse"
                )
                st.caption("Target: 5 breaks")
        
        st.markdown('</div>', unsafe_allow_html=True)

with col_overview2:
    # Get and display motivational quote
    quote = get_motivational_quote()
    st.markdown(f'''
    <div class="quote-card">
        <h4>💭 Daily Inspiration</h4>
        <div class="quote-text">{quote["text"]}</div>
        <div class="quote-author">— {quote["author"]}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Refresh quote button
    if st.button("🔄 New Quote", key="home_quote", use_container_width=True):
        st.rerun()



# Footer with app info
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    st.markdown("**PAUSE Dashboard**")
    st.caption("Your central hub for focus and wellness")
with col_footer2:
    st.markdown("**Last Updated**")
    st.caption("Today, 10:30 AM")
with col_footer3:
    st.markdown("**Status**")
    st.caption("🟢 All systems operational")

# Run instructions in expander
with st.expander("🚀 How to run this app"):
    st.code("pip install streamlit plotly pandas numpy", language="bash")
    st.code("streamlit run app.py", language="bash")
    st.caption("Make sure you have Python installed on your system")

print("✅ PAUSE Dashboard loaded successfully!")
print("🎨 Modern purple/white UI with navigation cards and quick overview")
print("🚀 Run with: streamlit run app.py")