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
    
    /* Progress bar styling */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        position: relative;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-top: 5px;
        font-size: 12px;
        color: #666;
    }
    
    /* Metric progress bars */
    .metric-progress {
        margin-bottom: 12px;
    }
    
    .metric-progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    
    .metric-progress-bar {
        background: #f0f0f0;
        border-radius: 5px;
        height: 8px;
        overflow: hidden;
    }
    
    .metric-progress-fill {
        height: 100%;
        border-radius: 5px;
    }
    
    .metric-progress-desc {
        font-size: 11px;
        color: #666;
        margin-top: 2px;
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

# Use default 30 days for analytics data
days_to_show = 30

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
        return "Low", 15, {
            'focus_intensity': 0,
            'streak_length': 0,
            'session_length': 0,
            'rest_frequency': 0,
            'consistency': 0,
            'completion_rate': 0,
            'distractions': 0
        }
    
    # Get last 7 days data
    last_7_days = daily_summary.head(7)
    
    if last_7_days.empty:
        return "Low", 15, {
            'focus_intensity': 0,
            'streak_length': 0,
            'session_length': 0,
            'rest_frequency': 0,
            'consistency': 0,
            'completion_rate': 0,
            'distractions': 0
        }
    
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
    
    # Factor 6: Completion rate
    completion_rate = insights.get('completion_rate', 0)
    if completion_rate >= 90:
        completion_factor = 20  # High completion, low risk
    elif completion_rate >= 70:
        completion_factor = 40  # Good completion
    elif completion_rate >= 50:
        completion_factor = 60  # Moderate completion
    else:
        completion_factor = 80  # Low completion, high risk
    
    # Factor 7: Distractions (incomplete sessions)
    incomplete_sessions = insights.get('incomplete_sessions', 0)
    total_sessions = insights.get('sessions_in_range', 0) + incomplete_sessions
    if total_sessions > 0:
        distraction_rate = (incomplete_sessions / total_sessions * 100)
        if distraction_rate <= 10:
            distraction_factor = 20  # Low distractions
        elif distraction_rate <= 25:
            distraction_factor = 40  # Moderate distractions
        elif distraction_rate <= 50:
            distraction_factor = 60  # High distractions
        else:
            distraction_factor = 80  # Very high distractions
    else:
        distraction_factor = 20  # No sessions, low risk
    
    # Calculate burnout score (weighted average with improved weights)
    burnout_score = (
        focus_factor * 0.20 +      # Daily intensity
        streak_factor * 0.15 +     # Streak length
        intensity_factor * 0.15 +  # Session length
        rest_factor * 0.15 +       # Rest days
        consistency_factor * 0.15 + # Schedule consistency
        completion_factor * 0.10 + # Completion rate
        distraction_factor * 0.10  # Distractions
    )
    
    # Determine level with clearer thresholds
    if burnout_score < 35:
        level = "Low"
    elif burnout_score < 55:
        level = "Moderate"
    elif burnout_score < 70:
        level = "High"
    else:
        level = "Very High"
    
    # Return supporting metrics
    supporting_metrics = {
        'focus_intensity': focus_factor,
        'streak_length': streak_factor,
        'session_length': intensity_factor,
        'rest_frequency': rest_factor,
        'consistency': consistency_factor,
        'completion_rate': completion_factor,
        'distractions': distraction_factor
    }
    
    return level, int(burnout_score), supporting_metrics

def get_today_sessions_by_hour():
    """Get today's sessions grouped by hour for hourly activity chart"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get today's sessions
    today_sessions = session_storage.get_sessions(start_date=today, end_date=today)
    
    if today_sessions.empty:
        return pd.DataFrame()
    
    # Convert created_at to datetime and extract hour
    today_sessions['created_at_dt'] = pd.to_datetime(today_sessions['created_at'])
    today_sessions['hour'] = today_sessions['created_at_dt'].dt.hour
    
    # Group by hour
    hourly_data = today_sessions.groupby('hour').agg({
        'focus_duration': 'sum',  # Total focus seconds per hour
        'session_id': 'count'     # Number of sessions per hour
    }).reset_index()
    
    # Rename columns
    hourly_data = hourly_data.rename(columns={
        'focus_duration': 'total_focus_seconds',
        'session_id': 'session_count'
    })
    
    # Convert seconds to minutes
    hourly_data['focus_minutes'] = hourly_data['total_focus_seconds'] / 60
    
    # Sort by hour
    hourly_data = hourly_data.sort_values('hour')
    
    return hourly_data

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

# Generate sample data if database is empty
generate_sample_data_if_empty()

# Get real data from database using the selected date range
daily_summary = session_storage.get_daily_summary(days=days_to_show)
weekly_summary = session_storage.get_weekly_summary(weeks=days_to_show//7 if days_to_show >= 7 else 1)
insights = session_storage.get_advanced_insights(days=days_to_show)
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
# TODAY SECTION
# ============================================
st.markdown("### 📅 Today")

today_col1, today_col2, today_col3 = st.columns(3)

with today_col1:
    # Today's Focus Time
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Focus Time</div>', unsafe_allow_html=True)
    if not today_summary.empty:
        today_focus = today_summary.iloc[0]['total_focus_hours']
        st.markdown(f'<div class="metric-value">{today_focus:.1f}h</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-value">0h</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with today_col2:
    # Today's Sessions
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Sessions</div>', unsafe_allow_html=True)
    if not today_summary.empty:
        total_sessions = int(today_summary.iloc[0]['session_count'])
        completed_sessions = int(today_summary.iloc[0]['completed_sessions'])
        st.markdown(f'<div class="metric-value">{completed_sessions}/{total_sessions}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-value">0/0</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with today_col3:
    # Today's Completion Rate
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Completion Rate</div>', unsafe_allow_html=True)
    if not today_summary.empty and total_sessions_today > 0:
        completion_rate = (completed_sessions_today / total_sessions_today * 100)
        st.markdown(f'<div class="metric-value">{completion_rate:.0f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-value">0%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TODAY HOURLY ACTIVITY HEATMAP
# ============================================
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### ⏰ Today's Hourly Focus Activity")

import pandas as pd
import plotly.graph_objects as go

# =========================
# 1️⃣ MOCK DATA (for testing)
# =========================
mock_hourly_data = pd.DataFrame([
    {"hour": 6, "focus_minutes": 0,  "session_count": 0},
    {"hour": 7, "focus_minutes": 20, "session_count": 1},
    {"hour": 8, "focus_minutes": 45, "session_count": 2},
    {"hour": 9, "focus_minutes": 60, "session_count": 3},
    {"hour": 10, "focus_minutes": 30, "session_count": 1},
    {"hour": 11, "focus_minutes": 0,  "session_count": 0},
    {"hour": 12, "focus_minutes": 25, "session_count": 1},
    {"hour": 13, "focus_minutes": 10, "session_count": 1},
    {"hour": 14, "focus_minutes": 55, "session_count": 2},
    {"hour": 15, "focus_minutes": 70, "session_count": 3},
    {"hour": 16, "focus_minutes": 40, "session_count": 2},
    {"hour": 17, "focus_minutes": 15, "session_count": 1},
    {"hour": 18, "focus_minutes": 0,  "session_count": 0},
    {"hour": 19, "focus_minutes": 35, "session_count": 2},
    {"hour": 20, "focus_minutes": 50, "session_count": 2},
    {"hour": 21, "focus_minutes": 20, "session_count": 1},
    {"hour": 22, "focus_minutes": 0,  "session_count": 0},
])

# =========================
# 2️⃣ SWITCH MODE
# =========================
USE_MOCK = True  # 👉 改 False 就会用真实数据

if USE_MOCK:
    hourly_data = mock_hourly_data
else:
    hourly_data = get_today_sessions_by_hour()

# =========================
# 3️⃣ CLEAN + AGGREGATE (REAL ONLY SAFE)
# =========================
if not hourly_data.empty:
    hourly_data = (
        hourly_data
        .groupby('hour', as_index=False)
        .agg({
            'focus_minutes': 'sum',
            'session_count': 'sum'
        })
    )

    # fill missing hours (0–23)
    all_hours = pd.DataFrame({"hour": list(range(24))})
    hourly_data = all_hours.merge(hourly_data, on="hour", how="left")
    hourly_data = hourly_data.fillna(0)

    # =========================
    # 4️⃣ HEATMAP DATA
    # =========================
    heatmap_data = [hourly_data["focus_minutes"].values]

    # =========================
    # 5️⃣ PLOTLY HEATMAP
    # =========================
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data,
            x=list(range(24)),
            y=["Today"],
            colorscale=[
                [0.0, "#F5F0FF"],
                [0.2, "#D6B3FF"],
                [0.4, "#B57CFF"],
                [0.6, "#8A2BE2"],
                [1.0, "#4B0082"]
            ],
            hovertemplate=
                "<b>Hour %{x}:00</b><br>" +
                "Focus: %{z:.1f} min<br>" +
                "<extra></extra>",
            colorbar=dict(
                title="Focus Minutes"
            )
        )
    )

    # =========================
    # 6️⃣ LAYOUT (your purple theme)
    # =========================
    fig.update_layout(
        height=260,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",

        xaxis=dict(
            title=dict(
                text="Hour of Day",
                font=dict(color="#333333", size=13)
            ),
            tickfont=dict(color="#333333", size=12),
            dtick=1,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        ),

        yaxis=dict(
            showticklabels=False,
            showgrid=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟣 Darker = more focus time | Each cell = 1 hour of activity")

else:
    st.info("⏰ No sessions recorded today yet. Start your first focus session!")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# THIS WEEK SECTION
# ============================================
st.markdown("### 📊 This Week")

week_col1, week_col2, week_col3 = st.columns(3)

with week_col1:
    # Total Focus Hours this week
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Focus Hours</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_focus:.1f}h</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with week_col2:
    # Average Daily Focus this week
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Average Daily Focus</div>', unsafe_allow_html=True)
    avg_daily_focus = this_week_focus / 7 if this_week_focus > 0 else 0
    st.markdown(f'<div class="metric-value">{avg_daily_focus:.1f}h</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with week_col3:
    # Weekly Focus Hours (same as total, but keeping the label)
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Weekly Focus Hours</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_focus:.1f}h</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# THIS WEEK AREA CHART
# ============================================
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 📈 This Week Focus Trend")

import plotly.graph_objects as go
import pandas as pd
import numpy as np

# =========================
# 1️⃣ MOCK DATA (fallback)
# =========================
mock_week_data = pd.DataFrame([
    {"day": "Mon", "focus_hours": 1.2},
    {"day": "Tue", "focus_hours": 2.5},
    {"day": "Wed", "focus_hours": 0.8},
    {"day": "Thu", "focus_hours": 3.0},
    {"day": "Fri", "focus_hours": 2.2},
    {"day": "Sat", "focus_hours": 1.0},
    {"day": "Sun", "focus_hours": 1.5},
])

# =========================
# 2️⃣ GET REAL DATA
# =========================
USE_MOCK = False

if not daily_summary.empty:
    week_data = daily_summary.head(7).copy()
    week_data = week_data.sort_values("date")
    week_data["day"] = week_data["date"].apply(get_day_name)
    week_data["focus_hours"] = week_data["total_focus_hours"]
else:
    week_data = mock_week_data

# =========================
# 3️⃣ FILL MISSING DAYS (important)
# =========================
all_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
week_data = pd.DataFrame({"day": all_days}).merge(week_data, on="day", how="left")
week_data["focus_hours"] = week_data["focus_hours"].fillna(0)

# =========================
# 4️⃣ AREA CHART
# =========================
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=week_data["day"],
    y=week_data["focus_hours"],
    mode="lines+markers",
    line=dict(color="#8A2BE2", width=3),
    fill="tozeroy",   # 🔥 this makes it area chart
    fillcolor="rgba(138, 43, 226, 0.2)",
    marker=dict(size=6),
    hovertemplate=
        "<b>%{x}</b><br>" +
        "Focus: %{y:.1f}h<br>" +
        "<extra></extra>"
))

# =========================
# 5️⃣ LAYOUT (your theme)
# =========================
fig.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(
        title="Day",
        tickfont=dict(color="#333333"),
        gridcolor="rgba(0,0,0,0.05)"
    ),
    yaxis=dict(
        title="Focus Hours",
        tickfont=dict(color="#333333"),
        gridcolor="rgba(0,0,0,0.05)"
    )
)

st.plotly_chart(fig, use_container_width=True)

# ============================================
# WEEKLY PERFORMANCE (STABLE FULL VERSION)
# Calendar Range + Weekly Aggregation + Mock Fallback
# ============================================

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 📈 Weekly Focus Performance")

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =========================
# 1️⃣ CALENDAR RANGE
# =========================
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date")

with col2:
    end_date = st.date_input("End Date")

if start_date > end_date:
    st.error("Start date must be before end date")
    st.stop()

# =========================
# 2️⃣ MIN 5 WEEKS CHECK
# =========================
days_selected = (end_date - start_date).days + 1

if days_selected < 35:
    st.warning("⚠️ Please select at least 5 weeks (35 days minimum)")
    st.stop()

# =========================
# 3️⃣ GET RAW DATA (NO CUSTOM FUNCTION)
# =========================
df = session_storage.get_daily_summary(days=365)

# =========================
# 4️⃣ SAFE FILTER BY DATE
# =========================
if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    df = df[
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ]

USE_MOCK = df.empty

# =========================
# 5️⃣ MOCK DATA (SAFE FALLBACK)
# =========================
if USE_MOCK:
    weekly_df = pd.DataFrame([
        {"week_label": "Week 1", "total_focus_hours": 6.2, "session_count": 8},
        {"week_label": "Week 2", "total_focus_hours": 9.1, "session_count": 12},
        {"week_label": "Week 3", "total_focus_hours": 4.5, "session_count": 6},
        {"week_label": "Week 4", "total_focus_hours": 10.8, "session_count": 15},
        {"week_label": "Week 5", "total_focus_hours": 7.4, "session_count": 10},
    ])
else:
    # =========================
    # 6️⃣ WEEKLY GROUPING
    # =========================
    df["week"] = df["date"].dt.isocalendar().week

    weekly_df = df.groupby("week").agg({
        "total_focus_hours": "sum",
        "session_count": "sum"
    }).reset_index()

    weekly_df = weekly_df.sort_values("week")

    weekly_df["week_label"] = [
        f"Week {i+1}" for i in range(len(weekly_df))
    ]

# =========================
# 7️⃣ COLOR SCALE
# =========================
def get_color(h):
    if h < 5:
        return "#D6B3FF"
    elif h < 10:
        return "#8A2BE2"
    else:
        return "#4B0082"

colors = weekly_df["total_focus_hours"].apply(get_color)

# =========================
# 8️⃣ BAR CHART (ONE BAR PER WEEK)
# =========================
fig = go.Figure()

fig.add_trace(go.Bar(
    x=weekly_df["week_label"],
    y=weekly_df["total_focus_hours"],
    marker=dict(color=colors),
    width=0.6,
    hovertemplate=
        "<b>%{x}</b><br>" +
        "Focus: %{y:.1f}h<br>" +
        "<extra></extra>"
))

# =========================
# 9️⃣ SESSION LABELS
# =========================
for i, row in weekly_df.iterrows():
    fig.add_annotation(
        x=row["week_label"],
        y=row["total_focus_hours"],
        text=f"{int(row['session_count'])} sessions",
        showarrow=False,
        yshift=10,
        font=dict(color="#333", size=11)
    )

# =========================
# 🔟 LAYOUT
# =========================
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",

    xaxis=dict(
        title="Week",
        tickfont=dict(color="#333"),
        gridcolor="rgba(0,0,0,0.05)"
    ),

    yaxis=dict(
        title="Total Focus Hours",
        gridcolor="rgba(0,0,0,0.05)"
    ),

    height=420
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MODE INDICATOR
# =========================
if USE_MOCK:
    st.info("📊 Showing mock data (no sessions in selected range)")
else:
    st.success("📊 Showing real analytics data")

st.caption("Each bar = total focus per week | Minimum 5 weeks required")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**PAUSE Analytics Dashboard** • Data-driven insights for better focus • 📊")