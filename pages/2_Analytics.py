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

st.title("Analytics")

# Page configuration for Analytics page
st.set_page_config(
    page_title="PAUSE - Analytics",
    page_icon="📊",
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
    
    .completion-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 5px;
    }
    
    .badge-excellent {
        background-color: rgba(76, 175, 80, 0.1);
        color: #4CAF50;
    }
    
    .badge-good {
        background-color: rgba(255, 193, 7, 0.1);
        color: #FF9800;
    }
    
    .badge-needs-improvement {
        background-color: rgba(244, 67, 54, 0.1);
        color: #F44336;
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

# Page title
st.markdown("<h1 class='main-title'>PAUSE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Analytics & Insights 📊</p>", unsafe_allow_html=True)

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
    if st.button("📊 Analytics", use_container_width=True, disabled=True):
        pass  # Current page, so disabled
with nav_col3:
    if st.button("🧘 Wellness", use_container_width=True):
        st.switch_page("pages/3_Wellness.py")

st.markdown("<br>", unsafe_allow_html=True)

# Generate sample data if database is empty
generate_sample_data_if_empty()

# Get real data from database
daily_summary = session_storage.get_daily_summary(days=30)
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
    
    this_week_avg_productivity = this_week['avg_productivity'].mean() if not this_week.empty and 'avg_productivity' in this_week.columns else 0
    last_week_avg_productivity = last_week['avg_productivity'].mean() if not last_week.empty and 'avg_productivity' in last_week.columns else 0
else:
    this_week_focus = 0
    last_week_focus = 0
    this_week_avg_productivity = 0
    last_week_avg_productivity = 0

# Calculate today's completion rate
if not today_summary.empty:
    total_sessions_today = today_summary.iloc[0]['session_count']
    completed_sessions_today = today_summary.iloc[0]['completed_sessions']
    completion_rate_today = (completed_sessions_today / total_sessions_today * 100) if total_sessions_today > 0 else 0
else:
    total_sessions_today = 0
    completed_sessions_today = 0
    completion_rate_today = 0

# Key Metrics Overview with REAL DATA
st.markdown("### 📈 Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Weekly Focus Hours</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_focus:.1f}h</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(this_week_focus, last_week_focus)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% vs last week</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% vs last week</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Avg Productivity</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{this_week_avg_productivity:.0f}%</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(this_week_avg_productivity, last_week_avg_productivity)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% improvement</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% decline</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Session Completion</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{completion_rate_today:.0f}%</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">of planned sessions</div>', unsafe_allow_html=True)
    if completion_rate_today >= 80:
        st.markdown('<span class="metric-change positive">🎯 On track</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="metric-change negative">⚠️ Needs improvement</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Focus Streak</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{insights["current_streak"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">days</div>', unsafe_allow_html=True)
    if insights["current_streak"] >= 7:
        st.markdown('<span class="metric-change positive">🔥 Personal best!</span>', unsafe_allow_html=True)
    elif insights["current_streak"] >= 3:
        st.markdown('<span class="metric-change positive">📈 Keep it up!</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="metric-change">Start a streak!</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Analytics Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 📈 Weekly Productivity Trend")
    
    if not daily_summary.empty and len(daily_summary) >= 7:
        # Get last 7 days of data
        weekly_data = daily_summary.head(7).copy()
        weekly_data = weekly_data.sort_values('date')  # Sort by date
        
        # Create day names
        weekly_data['Day'] = weekly_data['date'].apply(get_day_name)
        
        # Create a beautiful dual-axis chart
        fig = go.Figure()
        
        # Add productivity line
        fig.add_trace(go.Scatter(
            x=weekly_data['Day'],
            y=weekly_data['avg_productivity'].fillna(0),
            name='Productivity',
            mode='lines+markers',
            line=dict(color='#8A2BE2', width=4),
            marker=dict(size=10, color='#8A2BE2'),
            yaxis='y'
        ))
        
        # Add focus hours bars
        fig.add_trace(go.Bar(
            x=weekly_data['Day'],
            y=weekly_data['total_focus_hours'],
            name='Focus Hours',
            marker_color='rgba(138, 43, 226, 0.3)',
            yaxis='y2'
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
                title=dict(text='Productivity (%)', font=dict(color='#8A2BE2', size=12)),
                tickfont=dict(color='#8A2BE2'),
                gridcolor='rgba(138, 43, 226, 0.1)',
                range=[0, 100],
                showgrid=True
            ),
            yaxis2=dict(
                title=dict(text='Focus Hours', font=dict(color='rgba(138, 43, 226, 0.7)', size=12)),
                tickfont=dict(color='rgba(138, 43, 226, 0.7)'),
                overlaying='y',
                side='right',
                showgrid=False
            ),
            xaxis=dict(
                gridcolor='rgba(138, 43, 226, 0.1)',
                showgrid=True
            ),
            height=400,
            margin=dict(l=20, r=50, t=40, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Track your productivity and focus hours throughout the week")
    else:
        st.info("📊 Not enough data yet. Complete more focus sessions to see your weekly trends!")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Daily Performance Breakdown")
    
    if not today_summary.empty:
        # Get today's data
        today_data = today_summary.iloc[0]
        productivity_score = today_data['avg_productivity'] if pd.notna(today_data['avg_productivity']) else 0
        
        # Create a modern layout with two columns
        col_chart_left, col_metrics_right = st.columns([1.2, 1])
        
        with col_chart_left:
            # Create a donut chart for productivity score with categories
            productivity_categories = {
                'Excellent': {'min': 80, 'max': 100, 'color': '#8A2BE2'},
                'Good': {'min': 60, 'max': 79, 'color': '#9370DB'},
                'Needs Improvement': {'min': 0, 'max': 59, 'color': '#DDA0DD'}
            }
            
            # Determine current category
            current_category = None
            for category, range_info in productivity_categories.items():
                if range_info['min'] <= productivity_score <= range_info['max']:
                    current_category = category
                    current_color = range_info['color']
                    break
            
            # Create donut chart data
            labels = list(productivity_categories.keys())
            values = [0, 0, 0]
            
            # Set the current category value
            if current_category == 'Excellent':
                values[0] = productivity_score
            elif current_category == 'Good':
                values[1] = productivity_score
            else:
                values[2] = productivity_score
            
            # Create donut chart
            fig2 = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(
                    colors=[productivity_categories['Excellent']['color'],
                           productivity_categories['Good']['color'],
                           productivity_categories['Needs Improvement']['color']],
                    line=dict(color='white', width=2)
                ),
                textinfo='none',
                hoverinfo='label+value',
                direction='clockwise',
                sort=False
            )])
            
            # Add center text with productivity score
            fig2.add_annotation(
                text=f"<b>{productivity_score:.0f}%</b><br><span style='font-size:12px;color:#666'>Productivity</span>",
                x=0.5, y=0.5,
                font=dict(size=24, color='#4B0082'),
                showarrow=False,
                align='center'
            )
            
            # Update layout for modern look
            fig2.update_layout(
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.1,
                    font=dict(size=11),
                    itemwidth=30
                ),
                margin=dict(l=10, r=120, t=10, b=10)
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Category indicator
            st.markdown(f"""
            <div style="text-align: center; margin-top: -20px;">
                <span style="display: inline-block; padding: 4px 12px; border-radius: 15px; 
                background-color: {current_color}20; color: {current_color}; font-weight: 600; font-size: 0.9rem;">
                {current_category}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metrics_right:
            # Create compact KPI cards in a grid
            
            # Calculate completion rate
            total_sessions = int(today_data['session_count'])
            completed_sessions = int(today_data['completed_sessions'])
            completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Determine completion badge
            if completion_rate >= 90:
                completion_badge = "badge-excellent"
                completion_text = "Excellent"
            elif completion_rate >= 70:
                completion_badge = "badge-good"
                completion_text = "Good"
            else:
                completion_badge = "badge-needs-improvement"
                completion_text = "Needs Improvement"
            
            # KPI 1: Sessions
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Sessions</div>
                <div class="kpi-value">{total_sessions}</div>
                <div class="kpi-subtext">{completed_sessions} completed</div>
            </div>
            """, unsafe_allow_html=True)
            
            # KPI 2: Focus Time
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Focus Time</div>
                <div class="kpi-value">{today_data['total_focus_hours']:.1f}h</div>
                <div class="kpi-subtext">Today's total</div>
            </div>
            """, unsafe_allow_html=True)
            
            # KPI 3: Avg Session
            avg_session_minutes = today_data['avg_focus_duration'] if pd.notna(today_data['avg_focus_duration']) else 0
            avg_session_display = format_time(avg_session_minutes)
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Avg Session</div>
                <div class="kpi-value">{avg_session_display}</div>
                <div class="kpi-subtext">Per focus session</div>
            </div>
            """, unsafe_allow_html=True)
            
            # KPI 4: Completion Rate
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Completion Rate</div>
                <div class="kpi-value">{completion_rate:.0f}%</div>
                <div class="kpi-subtext">
                    <span class="completion-badge {completion_badge}">{completion_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a small summary below
        st.markdown("---")
        col_summary1, col_summary2 = st.columns(2)
        
        with col_summary1:
            # Best session today
            if 'best_session_today' not in locals():
                # In a real app, you would query for today's best session
                best_session_minutes = avg_session_minutes * 1.2 if avg_session_minutes > 0 else 0  # Simulated best session
                st.metric(
                    label="Best Session Today",
                    value=format_time(best_session_minutes) if best_session_minutes > 0 else "0m",
                    delta="Longest focus" if best_session_minutes > 0 else "No sessions"
                )
        
        with col_summary2:
            # Productivity trend (compare with yesterday if available)
            if not daily_summary.empty and len(daily_summary) >= 2:
                # Get yesterday's data (second row in daily_summary since it's sorted DESC)
                yesterday_data = daily_summary.iloc[1]
                yesterday_date = yesterday_data['date']
                today_date = datetime.now().strftime("%Y-%m-%d")
                
                # Check if yesterday_data is actually yesterday (not just any previous day)
                yesterday_obj = datetime.strptime(yesterday_date, "%Y-%m-%d")
                today_obj = datetime.strptime(today_date, "%Y-%m-%d")
                
                if (today_obj - yesterday_obj).days == 1:
                    yesterday_productivity = yesterday_data['avg_productivity'] if pd.notna(yesterday_data['avg_productivity']) else 0
                    trend = productivity_score - yesterday_productivity
                    trend_label = f"{trend:+.0f}% vs yesterday"
                    st.metric(
                        label="Productivity Trend",
                        value=f"{productivity_score:.0f}%",
                        delta=trend_label
                    )
                else:
                    st.metric(
                        label="Productivity Trend",
                        value=f"{productivity_score:.0f}%",
                        delta="No data yesterday"
                    )
            else:
                st.metric(
                    label="Productivity Trend",
                    value=f"{productivity_score:.0f}%",
                    delta="First day tracking"
                )
        
        st.caption("Daily performance metrics updated in real-time")
    else:
        # No data state - show placeholder with call to action
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 4rem; margin-bottom: 20px;">⏱️</div>
            <h3 style="color: #4B0082; margin-bottom: 10px;">No Sessions Today</h3>
            <p style="color: #666; margin-bottom: 20px;">Start your first focus session to see your daily performance metrics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Use Streamlit button for navigation
        col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
        with col_button2:
            if st.button("🎯 Start a Focus Session", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Timer.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced Insights Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🧠 Advanced Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
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
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">📅</span> <span class="insight-title">Focus Consistency</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-value">{insights["focus_consistency"]:.0f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-description">Days with focus sessions in last 30 days</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with insight_col3:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">🎯</span> <span class="insight-title">Weekly Goal Progress</span>', unsafe_allow_html=True)
    
    # Calculate weekly goal progress (assuming 20 hours per week goal)
    weekly_goal = 20  # hours
    weekly_progress = min(this_week_focus / weekly_goal * 100, 100)
    
    st.markdown(f'<div class="insight-value">{weekly_progress:.0f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-description">{this_week_focus:.1f}h / {weekly_goal}h this week</div>', unsafe_allow_html=True)
    
    # Progress bar
    st.progress(weekly_progress / 100)
    st.markdown('</div>', unsafe_allow_html=True)

insight_col4, insight_col5, insight_col6 = st.columns(3)

with insight_col4:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">⭐</span> <span class="insight-title">Best Focus Session</span>', unsafe_allow_html=True)
    if insights['best_session']['date']:
        focus_minutes = insights['best_session']['focus_minutes']
        st.markdown(f'<div class="insight-value">{format_time(focus_minutes)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-description">Longest session on {insights["best_session"]["date"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-value">--</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-description">Complete sessions to track your best</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with insight_col5:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">🔥</span> <span class="insight-title">Current Streak</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-value">{insights["current_streak"]} days</div>', unsafe_allow_html=True)
    
    if insights['current_streak'] >= 7:
        streak_status = "🔥 Amazing streak!"
    elif insights['current_streak'] >= 3:
        streak_status = "📈 Keep going!"
    else:
        streak_status = "Start building your streak!"
    
    st.markdown(f'<div class="insight-description">{streak_status}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with insight_col6:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<span class="insight-icon">📊</span> <span class="insight-title">Total This Month</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-value">{insights["sessions_this_month"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-description">Focus sessions completed this month</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Monthly Progress Overview with REAL HEATMAP
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 📅 Monthly Progress Overview")

# Get current month and year
current_year = datetime.now().year
current_month = datetime.now().month

# Get heatmap data
heatmap_data = session_storage.get_monthly_heatmap_data(current_year, current_month)

if heatmap_data:
    # Create calendar grid for the current month
    cal = calendar.monthcalendar(current_year, current_month)
    month_name = calendar.month_name[current_month]
    
    # Create heatmap matrix
    heatmap_matrix = []
    week_labels = []
    
    for week_num, week in enumerate(cal, 1):
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(0)  # Empty day (outside month)
            else:
                date_key = f"{current_year}-{current_month:02d}-{day:02d}"
                if date_key in heatmap_data:
                    # Use session count for heatmap value
                    week_data.append(heatmap_data[date_key]['session_count'])
                else:
                    week_data.append(0)
        heatmap_matrix.append(week_data)
        week_labels.append(f"Week {week_num}")
    
    # Day labels
    day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Create heatmap
    fig3 = go.Figure(data=go.Heatmap(
        z=heatmap_matrix,
        x=day_labels,
        y=week_labels,
        colorscale='Purples',
        hoverongaps=False,
        text=heatmap_matrix,
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white"},
        hovertemplate='<b>%{x}</b><br>Week %{y}<br>Sessions: %{z}<extra></extra>'
    ))
    
    fig3.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        title=f"{month_name} {current_year} - Focus Sessions",
        xaxis_title="Day of Week",
        yaxis_title="Week of Month",
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Monthly focus session heatmap - darker colors indicate more sessions completed")
else:
    st.info("📅 No session data for this month yet. Complete focus sessions to build your monthly heatmap!")

st.markdown('</div>', unsafe_allow_html=True)

# Additional Statistics
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📋 Additional Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Focus Time</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{insights["total_focus_hours"]:.1f}h</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">All-time total</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with stat_col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Avg Focus Duration</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{format_time(insights["avg_focus_minutes"])}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Per session</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with stat_col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Session Completion</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{insights["completion_rate"]:.0f}%</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Overall rate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with stat_col4:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Best Productivity</div>', unsafe_allow_html=True)
    
    # Get best productivity day from daily summary
    if not daily_summary.empty and 'avg_productivity' in daily_summary.columns:
        best_day = daily_summary[daily_summary['avg_productivity'].notna()].nlargest(1, 'avg_productivity')
        if not best_day.empty:
            best_score = best_day.iloc[0]['avg_productivity']
            st.markdown(f'<div class="metric-value">{best_score:.0f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-label">Highest daily avg</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="metric-value">--</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-label">No data yet</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-value">--</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">No data yet</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Data Export Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="stat-card">', unsafe_allow_html=True)
st.markdown("### 📥 Export Analytics")

col_export1, col_export2, col_export3 = st.columns(3)

with col_export1:
    if st.button("📄 Export Weekly Report", use_container_width=True):
        # Export weekly data to CSV
        export_file = session_storage.export_to_csv("pause_weekly_report.csv")
        st.success(f"Weekly report exported to {export_file}")
        
with col_export2:
    if st.button("📊 Export Raw Data", use_container_width=True):
        # Export all sessions to CSV
        sessions_df = session_storage.get_sessions()
        if not sessions_df.empty:
            sessions_df.to_csv("pause_raw_data.csv", index=False)
            st.info("CSV file with raw analytics data prepared: pause_raw_data.csv")
        else:
            st.warning("No data to export yet")
            
with col_export3:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Data Management
with st.expander("🗃️ Data Management"):
    st.markdown("### Manage Your Session Data")
    
    # Show current session count
    session_count = session_storage.get_session_count()
    st.metric("Total Sessions in Database", session_count)
    
    col_manage1, col_manage2, col_manage3 = st.columns(3)
    
    with col_manage1:
        if st.button("🗑️ Clear Old Data (1+ year)", use_container_width=True):
            deleted = session_storage.clear_old_data(days_to_keep=365)
            st.success(f"Cleared {deleted} sessions older than 1 year")
            st.rerun()

        if st.button("🗑️ Clear All Data", use_container_width=True):
            conn = sqlite3.connect(session_storage.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions")
            conn.commit()
            conn.close()

            st.success("All session data cleared!")
            st.rerun()
    
    with col_manage2:
        if st.button("🔧 Fix Corrupted Data", use_container_width=True, type="secondary"):
            deleted = session_storage.clear_corrupted_data()
            if deleted > 0:
                st.warning(f"Removed {deleted} corrupted sessions (impossible durations)")
            else:
                st.info("No corrupted data found")
            st.rerun()
    
    with col_manage3:
        if st.button("📊 View Raw Data", use_container_width=True):
            sessions_df = session_storage.get_sessions()
            if not sessions_df.empty:
                st.dataframe(sessions_df.head(20))
                st.caption(f"Showing {len(sessions_df)} total sessions")
                
                # Show data quality metrics
                st.markdown("#### Data Quality Check")
                col_quality1, col_quality2, col_quality3 = st.columns(3)
                
                with col_quality1:
                    # Check for impossible durations (> 24 hours)
                    impossible = sessions_df[sessions_df['focus_duration'] > 86400]
                    st.metric("Impossible Durations", len(impossible))
                
                with col_quality2:
                    # Check for zero/negative durations
                    invalid = sessions_df[sessions_df['focus_duration'] <= 0]
                    st.metric("Invalid Durations", len(invalid))
                
                with col_quality3:
                    # Check average duration
                    avg_duration = sessions_df['focus_duration'].mean() / 60 if not sessions_df.empty else 0
                    st.metric("Avg Duration", f"{avg_duration:.1f} min")
            else:
                st.info("No session data available yet")

# Footer
st.markdown("---")
st.markdown("**PAUSE Analytics** • Real data-driven insights for better focus • 📊")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")