import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime, timedelta
import calendar
import sys
import os

# Add parent directory to path to import data_storage
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_storage import session_storage

# Import top navigation component
from components.navigation import create_top_navigation

# Page configuration for Analytics page
st.set_page_config(
    page_title="PAUSE - Analytics",
    page_icon="📊",
    layout="wide"
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
    
    /* Insight card styling */
    .insight-card {
        background: var(--white);
        border-radius: 15px;
        padding: 20px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(138, 43, 226, 0.1);
        margin-bottom: 15px;
    }
    
    .insight-icon {
        font-size: 1.5rem;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    .insight-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--dark-purple);
        margin-bottom: 5px;
    }
    
    .insight-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary-purple);
        margin: 5px 0;
    }
    
    .insight-description {
        font-size: 0.9rem;
        color: var(--text-light);
        margin-top: 5px;
    }
    
    /* KPI card styling for daily performance */
    .kpi-card {
        background: var(--white);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(138, 43, 226, 0.08);
        border: 1px solid rgba(138, 43, 226, 0.1);
        transition: all 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(138, 43, 226, 0.12);
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--dark-purple);
        margin: 5px 0;
        line-height: 1;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 3px;
    }
    
    .kpi-subtext {
        font-size: 0.75rem;
        color: #888;
        margin-top: 3px;
    }
    
    /* Burnout level indicator */
    .burnout-low {
        background-color: rgba(76, 175, 80, 0.1);
        color: #4CAF50;
        border-left: 4px solid #4CAF50;
    }
    
    .burnout-medium {
        background-color: rgba(255, 193, 7, 0.1);
        color: #FF9800;
        border-left: 4px solid #FF9800;
    }
    
    .burnout-high {
        background-color: rgba(244, 67, 54, 0.1);
        color: #F44336;
        border-left: 4px solid #F44336;
    }
    
    .burnout-indicator {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-weight: 600;
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

# Sidebar navigation has been removed and replaced with top navigation
# Date range selector moved to main page for better accessibility

# Initialize days_to_show in session state if not exists
if 'days_to_show' not in st.session_state:
    st.session_state.days_to_show = 30

# Date range selector will be added to main page layout

# Helper functions for data analysis
def calculate_weekly_trend(current, previous):
    """Calculate weekly trend percentage"""
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 1)

def format_time(minutes):
    """Format minutes into hours and minutes"""
    minutes = int(round(minutes))
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def get_day_name(date_str):
    """Get day name from date string"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%a")

def calculate_burnout_level(daily_summary, insights):
    """Calculate burnout level based on focus patterns with more meaningful metrics"""
    if daily_summary.empty:
        return "Low", 15
    
    # Get last 7 days data
    last_7_days = daily_summary.head(7)
    
    if last_7_days.empty:
        return "Low", 15
    
    # Calculate meaningful metrics
    total_focus_hours = last_7_days['total_focus_hours'].sum()
    avg_daily_focus = total_focus_hours / 7
    
    # Factor 1: Daily focus intensity (hours per day)
    # Healthy range: 2-4 hours/day, Risk: >6 hours/day
    if avg_daily_focus <= 2:
        focus_factor = 20  # Low intensity
    elif avg_daily_focus <= 4:
        focus_factor = 40  # Healthy range
    elif avg_daily_focus <= 6:
        focus_factor = 60  # High intensity
    else:
        focus_factor = 80  # Very high intensity
    
    # Factor 2: Streak length with rest days consideration
    # Healthy: 5-6 days/week with 1-2 rest days
    current_streak = insights.get('current_streak', 0)
    if current_streak <= 3:
        streak_factor = 20  # Short streak, low risk
    elif current_streak <= 7:
        streak_factor = 40  # Moderate streak
    elif current_streak <= 14:
        streak_factor = 60  # Long streak, moderate risk
    else:
        streak_factor = 80  # Very long streak, high risk
    
    # Factor 3: Session length distribution
    # Healthy: 25-45 minute sessions with breaks
    if 'avg_focus_duration' in last_7_days.columns and not last_7_days['avg_focus_duration'].isna().all():
        avg_session_length = last_7_days['avg_focus_duration'].mean()
        if avg_session_length <= 25:
            intensity_factor = 30  # Short sessions
        elif avg_session_length <= 45:
            intensity_factor = 40  # Optimal session length
        elif avg_session_length <= 60:
            intensity_factor = 60  # Long sessions
        else:
            intensity_factor = 80  # Very long sessions
    else:
        intensity_factor = 30
    
    # Factor 4: Rest day frequency
    # Healthy: 1-2 rest days per week
    days_with_sessions = len(last_7_days[last_7_days['session_count'] > 0])
    rest_days = 7 - days_with_sessions
    if rest_days >= 2:
        rest_factor = 20  # Good rest frequency
    elif rest_days == 1:
        rest_factor = 40  # Moderate rest
    else:
        rest_factor = 70  # No rest days, high risk
    
    # Factor 5: Focus consistency (working at consistent times)
    consistency = insights.get('focus_consistency', 0)
    if consistency <= 50:
        consistency_factor = 30  # Irregular schedule
    elif consistency <= 75:
        consistency_factor = 50  # Moderately consistent
    else:
        consistency_factor = 70  # Very consistent (potentially rigid)
    
    # Calculate burnout score (weighted average with improved weights)
    burnout_score = (
        focus_factor * 0.25 +      # Daily intensity
        streak_factor * 0.20 +     # Streak length
        intensity_factor * 0.20 +  # Session length
        rest_factor * 0.20 +       # Rest days
        consistency_factor * 0.15  # Schedule consistency
    )
    
    # Determine level with clearer thresholds
    if burnout_score < 35:
        return "Low", int(burnout_score)
    elif burnout_score < 55:
        return "Moderate", int(burnout_score)
    elif burnout_score < 70:
        return "High", int(burnout_score)
    else:
        return "Very High", int(burnout_score)

def generate_sample_data_if_empty():
    """Generate sample data if database is empty (for demo purposes)"""
    # Check if sample data has already been generated in this session
    if 'sample_data_generated' not in st.session_state:
        st.session_state.sample_data_generated = False
    
    if not st.session_state.sample_data_generated:
        sessions_df = session_storage.get_sessions()
        
        if sessions_df.empty:
            # Generate realistic sample data for the last 30 days
            today = datetime.now()
            for i in range(30):
                date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                
                # Realistic number of sessions per day (1-3, with some days having 0)
                # 70% chance of having sessions, 30% chance of no sessions (rest days)
                if np.random.random() < 0.7:
                    num_sessions = np.random.randint(1, 4)  # 1-3 sessions per day
                else:
                    num_sessions = 0  # Rest day
                
                for _ in range(num_sessions):
                    # Realistic focus durations: 20-45 minutes
                    focus_duration = np.random.randint(20, 46) * 60  # 20-45 minutes in seconds
                    # Realistic break durations: 3-10 minutes
                    break_duration = np.random.randint(3, 11) * 60   # 3-10 minutes in seconds
                    # Realistic productivity scores: 65-95
                    productivity_score = np.random.randint(65, 96)
                    
                    session_storage.save_session(
                        focus_duration=focus_duration,
                        break_duration=break_duration,
                        completed=True,
                        productivity_score=productivity_score,
                        session_type="focus",
                        notes=f"Sample session {_+1}",
                        session_date=date
                    )
            
            st.session_state.sample_data_generated = True
            st.info("📊 Realistic sample data generated for demonstration. Complete your own focus sessions to see real analytics!")

# Create top navigation (Analytics is current page)
create_top_navigation(current_page="Analytics")

# Page title
st.markdown("<h1 class='main-title'>PAUSE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Analytics Dashboard 📊</p>", unsafe_allow_html=True)

# Analytics Settings Section
st.markdown("### 📊 Analytics Settings")

col_set1, col_set2 = st.columns(2)

with col_set1:
    # Date range selector
    days_to_show = st.slider(
        "Show data for last (days):",
        min_value=7,
        max_value=90,
        value=st.session_state.days_to_show,
        help="Select how many days of data to display",
        key="analytics_days_slider"
    )
    st.session_state.days_to_show = days_to_show

with col_set2:
    st.markdown("**Data Range**")
    st.markdown(f"### {days_to_show} days")
    st.caption(f"Showing analytics for the last {days_to_show} days")

st.markdown("---")

# Generate sample data if database is empty
generate_sample_data_if_empty()

# Get real data from database using the selected date range
daily_summary = session_storage.get_daily_summary(days=days_to_show)
weekly_summary = session_storage.get_weekly_summary(weeks=8)
insights = session_storage.get_advanced_insights()
today_summary = session_storage.get_today_summary()

# Calculate current week vs last week
if not daily_summary.empty:
    # Get this week's data (last 7 days)
    this_week = daily_summary.head(7)
    last_week = daily_summary.iloc[7:14] if len(daily_summary) >= 14 else pd.DataFrame()
    
    this_week_focus = this_week['total_focus_hours'].sum() if not this_week.empty else 0
    last_week_focus = last_week['total_focus_hours'].sum() if not last_week.empty else 0
    
    this_week_sessions = this_week['session_count'].sum() if not this_week.empty else 0
    last_week_sessions = last_week['session_count'].sum() if not last_week.empty else 0
    
    this_week_avg_session = this_week['avg_focus_duration'].mean() if not this_week.empty and 'avg_focus_duration' in this_week.columns else 0
    last_week_avg_session = last_week['avg_focus_duration'].mean() if not last_week.empty and 'avg_focus_duration' in last_week.columns else 0
else:
    this_week_focus = 0
    last_week_focus = 0
    this_week_sessions = 0
    last_week_sessions = 0
    this_week_avg_session = 0
    last_week_avg_session = 0

# Calculate today's completion rate
if not today_summary.empty:
    total_sessions_today = today_summary.iloc[0]['session_count']
    completed_sessions_today = today_summary.iloc[0]['completed_sessions']
    completion_rate_today = (completed_sessions_today / total_sessions_today * 100) if total_sessions_today > 0 else 0
else:
    total_sessions_today = 0
    completed_sessions_today = 0
    completion_rate_today = 0

# ============================================
# SECTION 1: KPI OVERVIEW (TOP SECTION)
# ============================================
st.markdown("### 📈 KPI Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Weekly Focus Time
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Weekly Focus Time</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_focus:.1f}h</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(this_week_focus, last_week_focus)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% vs last week</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% vs last week</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Average Focus Session
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Average Focus Session</div>', unsafe_allow_html=True)
    avg_session_display = format_time(this_week_avg_session)
    st.markdown(f'<div class="metric-value">{avg_session_display}</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(this_week_avg_session, last_week_avg_session)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% longer</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% shorter</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    # Sessions Completed
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Sessions Completed</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_sessions}</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(this_week_sessions, last_week_sessions)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% more</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% fewer</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # Streak
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Focus Streak</div>', unsafe_allow_html=True)
    streak = insights.get('current_streak', 0)
    st.markdown(f'<div class="metric-value">{streak}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">days</div>', unsafe_allow_html=True)
    if streak >= 7:
        st.markdown('<span class="metric-change positive">🔥 Personal best!</span>', unsafe_allow_html=True)
    elif streak >= 3:
        st.markdown('<span class="metric-change positive">📈 Keep it up!</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="metric-change">Start a streak!</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# SECTION 2: PRODUCTIVITY TREND (ONE CHART ONLY)
# ============================================
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 📈 Weekly Focus Time Trend")

if not daily_summary.empty and len(daily_summary) >= 7:
    # Get last 7 days of data
    weekly_data = daily_summary.head(7).copy()
    weekly_data = weekly_data.sort_values('date')  # Sort by date
    
    # Create day names
    weekly_data['Day'] = weekly_data['date'].apply(get_day_name)
    
    # Create a clean line chart for focus hours only
    fig = go.Figure()
    
    # Add focus hours line
    fig.add_trace(go.Scatter(
        x=weekly_data['Day'],
        y=weekly_data['total_focus_hours'].fillna(0),
        name='Focus Hours',
        mode='lines+markers',
        line=dict(color='#8A2BE2', width=4),
        marker=dict(size=10, color='#8A2BE2'),
        fill='tozeroy',
        fillcolor='rgba(138, 43, 226, 0.1)'
    ))
    
    # Update layout for modern look
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        yaxis=dict(
            title=dict(text='Focus Hours', font=dict(color='#8A2BE2', size=12)),
            tickfont=dict(color='#8A2BE2'),
            gridcolor='rgba(138, 43, 226, 0.1)',
            showgrid=True
        ),
        xaxis=dict(
            gridcolor='rgba(138, 43, 226, 0.1)',
            showgrid=True
        ),
        height=400,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Your weekly focus time trend - aim for consistent daily focus")
else:
    st.info("📊 Not enough data yet. Complete more focus sessions to see your weekly trends!")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# SECTION 3: FOCUS BEHAVIOR INSIGHTS
# ============================================
st.markdown("### 🧠 Focus Behavior Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    # Most Productive Day
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">🏆</span> <span class="insight-title">Most Productive Day</span>', unsafe_allow_html=True)
    if insights['most_productive_day']['date']:
        date_obj = datetime.strptime(insights['most_productive_day']['date'], "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
        st.markdown(f'<div class="insight-value">{day_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-description">{insights["most_productive_day"]["session_count"]} sessions on {insights["most_productive_day"]["date"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-value">--</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-description">Complete more sessions to see your best day</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with insight_col2:
    # Focus Consistency Score
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">📅</span> <span class="insight-title">Focus Consistency</span>', unsafe_allow_html=True)
    consistency = insights.get('focus_consistency', 0)
    st.markdown(f'<div class="insight-value">{consistency:.0f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-description">Days with focus sessions in last 30 days</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with insight_col3:
    # Energy Pattern (simplified)
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">⚡</span> <span class="insight-title">Energy Pattern</span>', unsafe_allow_html=True)
    if not daily_summary.empty and len(daily_summary) >= 7:
        # Calculate average focus time by day of week
        daily_summary['date_obj'] = pd.to_datetime(daily_summary['date'])
        daily_summary['day_of_week'] = daily_summary['date_obj'].dt.day_name()
        avg_by_day = daily_summary.groupby('day_of_week')['total_focus_hours'].mean()
        
        if not avg_by_day.empty:
            best_day = avg_by_day.idxmax()
            best_hours = avg_by_day.max()
            st.markdown(f'<div class="insight-value">{best_day}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-description">{best_hours:.1f}h average focus</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="insight-value">--</div>', unsafe_allow_html=True)
            st.markdown('<div class="insight-description">Not enough data</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-value">--</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-description">Complete sessions to see pattern</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# SECTION 4: DAILY SNAPSHOT (LIGHTWEIGHT)
# ============================================
st.markdown("### 📅 Daily Snapshot")

if not today_summary.empty:
    today_data = today_summary.iloc[0]
    
    col_daily1, col_daily2 = st.columns(2)
    
    with col_daily1:
        # Simple KPI cards for today
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Today\'s Focus Time</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{today_data["total_focus_hours"]:.1f}h</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Sessions Completed</div>', unsafe_allow_html=True)
        completed = int(today_data['completed_sessions'])
        total = int(today_data['session_count'])
        st.markdown(f'<div class="metric-value">{completed}/{total}</div>', unsafe_allow_html=True)
        completion_rate = (completed / total * 100) if total > 0 else 0
        if completion_rate >= 80:
            st.markdown('<span class="metric-change positive">🎯 On track</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="metric-change negative">⚠️ Needs improvement</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_daily2:
        # Simple donut chart for focus vs break ratio
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Focus vs Break Ratio</div>', unsafe_allow_html=True)
        
        focus_hours = today_data['total_focus_hours']
        break_hours = today_data['total_break_hours'] if 'total_break_hours' in today_data else 0
        
        if focus_hours + break_hours > 0:
            # Create simple donut chart
            labels = ['Focus', 'Break']
            values = [focus_hours, break_hours]
            colors = ['#8A2BE2', '#9370DB']
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(colors=colors),
                textinfo='label+percent',
                hoverinfo='label+value',
                direction='clockwise',
                sort=False
            )])
            
            fig_donut.update_layout(
                height=250,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No sessions completed today")
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📅 No sessions completed today. Start your first focus session to see daily metrics!")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# SECTION 5: BURNOUT LEVEL (NEW FEATURE)
# ============================================
st.markdown("### 🔥 Burnout Level Assessment")

burnout_level, burnout_score = calculate_burnout_level(daily_summary, insights)

col_burnout1, col_burnout2 = st.columns([1, 2])

with col_burnout1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Burnout Risk</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{burnout_level}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Score: {burnout_score}/100</div>', unsafe_allow_html=True)
    
    # Color-coded indicator
    if burnout_level == "Low":
        st.markdown('<div class="burnout-indicator burnout-low">✅ Healthy balance</div>', unsafe_allow_html=True)
    elif burnout_level == "Moderate":
        st.markdown('<div class="burnout-indicator burnout-medium">⚠️ Monitor workload</div>', unsafe_allow_html=True)
    elif burnout_level == "High":
        st.markdown('<div class="burnout-indicator burnout-high">🚨 Take a break</div>', unsafe_allow_html=True)
    else:  # Very High
        st.markdown('<div class="burnout-indicator burnout-high">🔥 Critical - Rest needed</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_burnout2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Factors Considered</div>', unsafe_allow_html=True)
    
    factors = [
        "Daily focus intensity (hours per day)",
        "Current streak length & rest days", 
        "Average session duration",
        "Rest day frequency (per week)",
        "Schedule consistency"
    ]
    
    for factor in factors:
        st.markdown(f'<div style="margin-bottom: 8px;">• {factor}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>")
    
    # Recommendations based on burnout level
    if burnout_level == "Low":
        st.markdown("**Recommendations:**")
        st.markdown("- Maintain your current healthy balance")
        st.markdown("- Continue regular breaks between sessions")
        st.markdown("- Keep tracking your progress")
    elif burnout_level == "Moderate":
        st.markdown("**Recommendations:**")
        st.markdown("- Consider taking more frequent breaks")
        st.markdown("- Schedule at least 1 rest day per week")
        st.markdown("- Monitor your energy levels daily")
    elif burnout_level == "High":
        st.markdown("**Recommendations:**")
        st.markdown("- Take a complete day off from focused work")
        st.markdown("- Engage in non-work activities")
        st.markdown("- Reduce daily focus targets by 25%")
    else:  # Very High
        st.markdown("**Recommendations:**")
        st.markdown("- **Take 2-3 days completely off work**")
        st.markdown("- Seek support if feeling overwhelmed")
        st.markdown("- Reevaluate your work-life balance")
        st.markdown("- Consider professional help if needed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**PAUSE Analytics Dashboard** • Data-driven insights for better focus • 📊")