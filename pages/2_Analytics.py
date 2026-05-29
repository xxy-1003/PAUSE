import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

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

# Sample data generation functions
def generate_productivity_data():
    """Generate sample weekly productivity data"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    productivity = [78, 85, 72, 82, 88, 65, 70]
    focus_hours = [3.2, 4.1, 2.8, 3.9, 4.5, 1.5, 2.0]
    
    return pd.DataFrame({
        'Day': days,
        'Productivity (%)': productivity,
        'Focus Hours': focus_hours
    })

def calculate_weekly_trend(current, previous):
    """Calculate weekly trend percentage"""
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 1)

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

# Key Metrics Overview
st.markdown("### 📈 Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Weekly Focus Hours</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">24.1h</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(24.1, 22.5)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% vs last week</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% vs last week</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Avg Productivity</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">78%</div>', unsafe_allow_html=True)
    trend = calculate_weekly_trend(78, 75)
    if trend >= 0:
        st.markdown(f'<span class="metric-change positive">+{trend}% improvement</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="metric-change negative">{trend}% decline</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Session Completion</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">92%</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">of planned sessions</div>', unsafe_allow_html=True)
    st.markdown('<span class="metric-change positive">🎯 On track</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Focus Streak</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">7</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">days</div>', unsafe_allow_html=True)
    st.markdown('<span class="metric-change positive">🔥 Personal best!</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Analytics Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 📈 Weekly Productivity Trend")
    
    # Generate and display productivity chart
    data = generate_productivity_data()
    
    # Create a beautiful dual-axis chart
    fig = go.Figure()
    
    # Add productivity line
    fig.add_trace(go.Scatter(
        x=data['Day'],
        y=data['Productivity (%)'],
        name='Productivity',
        mode='lines+markers',
        line=dict(color='#8A2BE2', width=4),
        marker=dict(size=10, color='#8A2BE2'),
        yaxis='y'
    ))
    
    # Add focus hours bars
    fig.add_trace(go.Bar(
        x=data['Day'],
        y=data['Focus Hours'],
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
            range=[0, 5],
            showgrid=False
        ),
        xaxis=dict(
            gridcolor='rgba(138, 43, 226, 0.1)',
            showgrid=True
        ),
        height=400,
        margin=dict(l=20, r=50, t=40, b=40)
    )
    
    # Add some styling
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Track your productivity and focus hours throughout the week")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Daily Performance Breakdown")
    
    # Create a pie chart for focus distribution
    focus_data = pd.DataFrame({
        'Category': ['Deep Work', 'Meetings', 'Learning', 'Planning', 'Breaks'],
        'Hours': [3.2, 1.5, 1.0, 0.8, 0.5],
        'Color': ['#8A2BE2', '#9370DB', '#BA55D3', '#DA70D6', '#DDA0DD']
    })
    
    fig2 = px.pie(focus_data, values='Hours', names='Category', 
                  color_discrete_sequence=['#8A2BE2', '#9370DB', '#BA55D3', '#DA70D6', '#DDA0DD'])
    
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=1.2
        ),
        height=400,
        margin=dict(l=20, r=150, t=40, b=40)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Distribution of focus time across different activities")
    st.markdown('</div>', unsafe_allow_html=True)

# Additional Analytics
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### 📅 Monthly Progress Overview")

# Create a heatmap for monthly progress
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
progress_data = np.random.randint(60, 95, size=(len(weeks), len(months)))

fig3 = go.Figure(data=go.Heatmap(
    z=progress_data,
    x=months,
    y=weeks,
    colorscale='Purples',
    hoverongaps=False,
    text=progress_data,
    texttemplate="%{text}%",
    textfont={"size": 12}
))

fig3.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=400,
    xaxis_title="Month",
    yaxis_title="Week",
    margin=dict(l=20, r=20, t=40, b=40)
)

st.plotly_chart(fig3, use_container_width=True)
st.caption("Monthly productivity scores - track your consistency over time")
st.markdown('</div>', unsafe_allow_html=True)

# Data Export Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="stat-card">', unsafe_allow_html=True)
st.markdown("### 📥 Export Analytics")

col_export1, col_export2, col_export3 = st.columns(3)
with col_export1:
    if st.button("📄 Export Weekly Report", use_container_width=True):
        st.success("Weekly report generated and ready for download")
with col_export2:
    if st.button("📊 Export Raw Data", use_container_width=True):
        st.info("CSV file with raw analytics data prepared")
with col_export3:
    if st.button("🖼️ Export Charts", use_container_width=True):
        st.info("High-resolution charts exported as PNG files")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**PAUSE Analytics** • Data-driven insights for better focus • 📊")