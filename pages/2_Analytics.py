import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import sys
import os

# ============================================
# IMPORT THE CORRECT STORAGE SYSTEM
# ============================================

# Add parent directory to path to import pause_storage (which uses pause.db)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pause_storage import session_storage

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

def get_day_name(date_value):
    try:
        return pd.to_datetime(date_value).strftime("%a")
    except:
        return "Unknown"

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
    current_streak = st.session_state["focus_settings"]["current_streak"]
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
    """Get today's sessions aggregated by hour using real timestamps"""
    # Get today's sessions from the correct storage system
    today_sessions = session_storage.get_today_sessions("default_user")
    
    if today_sessions.empty:
        # Return empty dataframe with all 24 hours
        hourly_data = []
        for hour in range(24):
            hourly_data.append({
                'hour': hour,
                'focus_minutes': 0,
                'session_count': 0
            })
        return pd.DataFrame(hourly_data)
    
    # Initialize hourly counters
    focus_per_hour = {hour: 0 for hour in range(24)}
    sessions_per_hour = {hour: 0 for hour in range(24)}
    
    # Process each session
    for _, session in today_sessions.iterrows():
        try:
            # Extract hour from completed_at timestamp
            # Format: "YYYY-MM-DD HH:MM:SS"
            completed_at = session['completed_at']
            
            # Parse the timestamp
            if isinstance(completed_at, str):
                # Try to parse the timestamp
                try:
                    # Handle different timestamp formats
                    if ' ' in completed_at:
                        # Format: "YYYY-MM-DD HH:MM:SS"
                        time_part = completed_at.split(' ')[1]
                        hour = int(time_part.split(':')[0])
                    else:
                        # If no time part, use default hour (12 PM)
                        hour = 12
                except (ValueError, IndexError):
                    # If parsing fails, use default hour
                    hour = 12
            else:
                # If not a string, use default hour
                hour = 12
            
            # Ensure hour is within 0-23 range
            hour = max(0, min(23, hour))
            
            # Get duration in minutes
            duration_minutes = session['duration_minutes']
            
            # Add to hourly totals
            focus_per_hour[hour] += duration_minutes
            sessions_per_hour[hour] += 1
            
        except Exception as e:
            # Skip sessions with invalid data
            continue
    
    # Create hourly data
    hourly_data = []
    for hour in range(24):
        hourly_data.append({
            'hour': hour,
            'focus_minutes': focus_per_hour[hour],
            'session_count': sessions_per_hour[hour]
        })
    
    return pd.DataFrame(hourly_data)

create_top_navigation(current_page="Analytics")

st.markdown("<h1 class='main-title'>PAUSE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Analytics Dashboard 📊</p>", unsafe_allow_html=True)

# Data Management Buttons
st.markdown("### 🛠 Data Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Generate Mock Data"):
        session_storage.generate_mock_data()
        st.rerun()

with col2:
    if st.button("🗑 Clear All Data"):
        session_storage.clear_all_sessions()
        st.rerun()

st.divider()


# Analytics Data
username = "default_user"
daily_summary = session_storage.get_daily_summary(username, days=days_to_show)
# Note: pause_storage doesn't have get_weekly_summary, get_advanced_insights, or get_today_summary
# We'll use get_user_statistics instead of get_advanced_insights
user_stats = session_storage.get_user_statistics(username)
# Get today's sessions for today_summary
today_sessions = session_storage.get_today_sessions(username)

# Calculate current week vs last week using user_stats
this_week_focus = user_stats.get('weekly_minutes', 0) / 60  # Convert minutes to hours
this_week_sessions = user_stats.get('weekly_sessions', 0)
this_week_avg_session = user_stats.get('avg_duration', 0)  # Already in minutes

# For last week, we don't have direct data in pause_storage
# We'll calculate from daily_summary if available
last_week_focus = 0
last_week_sessions = 0
last_week_avg_session = 0

if not daily_summary.empty and len(daily_summary) >= 14:
    # Get last week's data (days 8-14)
    last_week_data = daily_summary.iloc[7:14]
    if not last_week_data.empty:
        last_week_focus = last_week_data['total_hours'].sum() if 'total_hours' in last_week_data.columns else 0
        last_week_sessions = last_week_data['session_count'].sum() if 'session_count' in last_week_data.columns else 0
        if last_week_sessions > 0:
            last_week_avg_session = last_week_data['avg_duration'].mean() if 'avg_duration' in last_week_data.columns else 0

# Calculate today's completion rate
if not today_sessions.empty:
    total_sessions_today = len(today_sessions)
    # In pause_storage, all sessions are assumed completed when saved
    completed_sessions_today = total_sessions_today
    completion_rate_today = 100 if total_sessions_today > 0 else 0
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
    if not today_sessions.empty:
        today_focus_minutes = today_sessions['duration_minutes'].sum()
        today_focus_hours = today_focus_minutes / 60
        st.markdown(f'<div class="metric-value">{today_focus_hours:.1f}h</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-value">0h</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with today_col2:
    # Today's Sessions
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Sessions</div>', unsafe_allow_html=True)
    if not today_sessions.empty:
        total_sessions = len(today_sessions)
        # All sessions are completed in pause_storage
        completed_sessions = total_sessions
        st.markdown(f'<div class="metric-value">{completed_sessions}/{total_sessions}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-value">0/0</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with today_col3:
    # Today's Completion Rate
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Completion Rate</div>', unsafe_allow_html=True)
    if not today_sessions.empty and total_sessions_today > 0:
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
# 2️⃣ GET HOURLY DATA
# =========================
hourly_data = get_today_sessions_by_hour()

# =========================
# 3️⃣ CREATE HEATMAP
# =========================
if not hourly_data.empty and hourly_data['focus_minutes'].sum() > 0:
    # =========================
    # 4️⃣ HEATMAP DATA
    # =========================
    heatmap_data = [hourly_data["focus_minutes"].values]

    # =========================
    # 5️⃣ PLOTLY HEATMAP WITH PROPER SCALING
    # =========================
    # Get min and max values for better color scaling
    focus_values = hourly_data["focus_minutes"].values
    zmin = 0  # Always start at 0 for better contrast
    zmax = max(focus_values) * 1.1 if max(focus_values) > 0 else 1  # Add 10% padding
    
    # Use a more dynamic color scale with better contrast
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data,
            x=list(range(24)),
            y=["Today"],
            zmin=zmin,
            zmax=zmax,
            colorscale=[
                [0.0, "#F5F0FF"],    # Very light purple for 0
                [0.1, "#E6E6FA"],    # Light lavender for low values
                [0.3, "#D6B3FF"],    # Light purple
                [0.5, "#B57CFF"],    # Medium purple
                [0.7, "#8A2BE2"],    # Primary purple
                [0.9, "#4B0082"],    # Dark purple
                [1.0, "#2E004D"]     # Very dark purple for high values
            ],
            hovertemplate=
                "<b>Hour %{x}:00</b><br>" +
                "Focus: %{z:.1f} min<br>" +
                "<extra></extra>",
            colorbar=dict(
                title="Focus Minutes",
                tickformat=".0f"
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

    st.caption("🟣 Darker = more focus time | Each cell = 1 hour of activity based on actual session timestamps")

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
    # Average Session Duration this week
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Avg Session Duration</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_avg_session:.0f} min</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with week_col3:
    # Weekly Sessions Count
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Weekly Sessions</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_sessions}</div>', unsafe_allow_html=True)
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
# 2️⃣ GET REAL DATA WITH PROPER DAY ORDERING
# =========================
if not daily_summary.empty:
    # Get last 7 days of data
    week_data = daily_summary.head(7).copy()
    
    # Convert date strings to datetime for proper sorting
    try:
        week_data["date_dt"] = pd.to_datetime(week_data["date"])
        week_data = week_data.sort_values("date_dt")
        
        # Get day names
        week_data["day"] = week_data["date_dt"].dt.strftime("%a")
        week_data["focus_hours"] = week_data["total_focus_hours"]
        
        # Keep only needed columns
        week_data = week_data[["day", "focus_hours"]]
    except Exception as e:
        # Fallback if date parsing fails
        week_data = pd.DataFrame({
            "day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            "focus_hours": [0,0,0,0,0,0,0]
        })
else:
    week_data = pd.DataFrame({
        "day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "focus_hours": [0,0,0,0,0,0,0]
    })

# =========================
# 3️⃣ ENSURE ALL DAYS ARE PRESENT IN CORRECT ORDER
# =========================
day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
week_data = pd.DataFrame({"day": day_order}).merge(week_data, on="day", how="left")
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
# BURNOUT LEVEL ASSESSMENT
# ============================================
st.markdown("### 📊 Burnout Breakdown")

chart_data = [
    {"metric": "Focus", "value": metrics["focus_intensity"]},
    {"metric": "Streak", "value": metrics["streak_length"]},
    {"metric": "Session", "value": metrics["session_length"]},
    {"metric": "Rest", "value": metrics["rest_frequency"]},
    {"metric": "Consistency", "value": metrics["consistency"]},
    {"metric": "Completion", "value": metrics["completion_rate"]},
    {"metric": "Distractions", "value": metrics["distractions"]},
]

import plotly.express as px

fig = px.bar(chart_data, x="metric", y="value", color="value")
fig.update_layout(
    height=300,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ============================================
# WEEKLY PERFORMANCE CHART 
# ============================================

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 📈 Weekly Focus Performance")

# =========================
# 1️⃣ LOAD RAW DATA FIRST
# =========================
all_sessions = session_storage.get_all_sessions("default_user")

# Always create weekly_df even if empty
if all_sessions.empty:
    weekly_df = pd.DataFrame(columns=['year_week', 'total_focus_minutes', 'session_count', 'total_focus_hours', 'week_label'])
else:
    # =========================
    # 2️⃣ CLEAN + PREP DATA
    # =========================
    all_sessions['date_dt'] = pd.to_datetime(all_sessions['session_date'], errors='coerce')
    all_sessions = all_sessions.dropna(subset=['date_dt'])

    if all_sessions.empty:
        weekly_df = pd.DataFrame(columns=['year_week', 'total_focus_minutes', 'session_count', 'total_focus_hours', 'week_label'])
    else:
        # Create week grouping
        all_sessions['year_week'] = all_sessions['date_dt'].dt.strftime('%Y-W%U')

        weekly_df = all_sessions.groupby('year_week').agg({
            'duration_minutes': 'sum',
            'id': 'count'
        }).reset_index()

        weekly_df = weekly_df.rename(columns={
            'duration_minutes': 'total_focus_minutes',
            'id': 'session_count'
        })

        weekly_df['total_focus_hours'] = weekly_df['total_focus_minutes'] / 60
        weekly_df['week_label'] = weekly_df['year_week']
        weekly_df = weekly_df.sort_values('year_week')

# Create week grouping
all_sessions['year_week'] = all_sessions['date_dt'].dt.strftime('%Y-W%U')

weekly_df = all_sessions.groupby('year_week').agg({
    'duration_minutes': 'sum',
    'id': 'count'
}).reset_index()

weekly_df = weekly_df.rename(columns={
    'duration_minutes': 'total_focus_minutes',
    'id': 'session_count'
})

weekly_df['total_focus_hours'] = weekly_df['total_focus_minutes'] / 60
weekly_df['week_label'] = weekly_df['year_week']
weekly_df = weekly_df.sort_values('year_week')

# =========================
# 3️⃣ WEEK SELECTOR (RESTORED)
# =========================
if weekly_df.empty:
    st.info("No weekly data available. Complete some focus sessions first.")
    available_weeks = ["No data available"]
    selected_week = "No data available"
    filtered_df = pd.DataFrame(columns=['week_label', 'total_focus_hours', 'session_count'])
else:
    available_weeks = weekly_df["week_label"].tolist()[::-1]
    selected_week = st.selectbox(
        "Select Week",
        available_weeks,
        index=0
    )
    filtered_df = weekly_df[weekly_df["week_label"] == selected_week]

# =========================
# 4️⃣ CHART (USES FILTERED DATA)
# =========================
import plotly.graph_objects as go

fig = go.Figure()

if not filtered_df.empty and not weekly_df.empty:
    fig.add_trace(go.Bar(
        x=filtered_df["week_label"],
        y=filtered_df["total_focus_hours"],
        marker=dict(color="#8A2BE2"),
        width=0.6,
        hovertemplate=
            "<b>%{x}</b><br>" +
            "Focus: %{y:.1f} hours<br>" +
            "Sessions: %{customdata[0]}<br>" +
            "<extra></extra>",
        customdata=filtered_df[["session_count"]].values
    ))
else:
    # Add empty bar for visual consistency
    fig.add_trace(go.Bar(
        x=["No data"],
        y=[0],
        marker=dict(color="#E6E6FA"),
        width=0.6,
        hovertemplate="No weekly data available"
    ))

# =========================
# 5️⃣ LAYOUT
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
    height=420,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 6️⃣ SMALL INSIGHT TEXT
# =========================
if not weekly_df.empty and not filtered_df.empty:
    st.caption(f"📊 Showing data for {selected_week} • {int(filtered_df['session_count'].sum())} sessions total")
else:
    st.caption("📊 No weekly data available")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**PAUSE Analytics Dashboard** • Data-driven insights for better focus • 📊")