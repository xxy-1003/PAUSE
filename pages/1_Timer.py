import streamlit as st
import time
import random
import sys
import os

# Add parent directory to path to import data_storage
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_storage import session_storage

# Page configuration for Timer page
st.set_page_config(
    page_title="PAUSE - Focus Timer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS for theme consistency (no SVG/HTML graphics)
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 4rem !important;
        font-weight: 800 !important;
        color: #4B0082 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #666666 !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #8A2BE2;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(138, 43, 226, 0.2);
    }
    
    /* Container spacing */
    .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for motivational quotes
def get_focus_quote():
    """Return a random motivational focus quote"""
    quotes = [
        {
            "text": "The secret of getting ahead is getting started.",
            "author": "Mark Twain"
        },
        {
            "text": "Focus on being productive instead of busy.",
            "author": "Tim Ferriss"
        },
        {
            "text": "Concentrate all your thoughts upon the work at hand.",
            "author": "Alexander Graham Bell"
        },
        {
            "text": "The successful warrior is the average man, with laser-like focus.",
            "author": "Bruce Lee"
        },
        {
            "text": "Your mind is for having ideas, not holding them.",
            "author": "David Allen"
        },
        {
            "text": "The key is not to prioritize what's on your schedule, but to schedule your priorities.",
            "author": "Stephen Covey"
        },
        {
            "text": "Don't watch the clock; do what it does. Keep going.",
            "author": "Sam Levenson"
        },
        {
            "text": "Productivity is never an accident.",
            "author": "Paul J. Meyer"
        },
        {
            "text": "The shorter way to do many things is to do only one thing at a time.",
            "author": "Mozart"
        },
        {
            "text": "What you stay focused on will grow.",
            "author": "Roy T. Bennett"
        }
    ]
    return random.choice(quotes)

# Helper function for motion detection simulation
def simulate_motion_detection():
    """Simulate motion-based focus detection (demo version)"""
    # Randomly determine focus status (80% focused, 20% unfocused)
    # This simulates the probability of being focused vs unfocused
    if random.random() < 0.8:  # 80% chance of being focused
        return "Focused"
    else:  # 20% chance of being unfocused
        return "Unfocused Motion Detected"

# Page title using Streamlit components only
st.title("PAUSE")
st.markdown("### Pomodoro Focus Timer ⏱️")

# Navigation back to Dashboard
with st.container():
    col_nav, col_empty = st.columns([1, 3])
    with col_nav:
        if st.button("🏠 Back to Home", use_container_width=True, type="secondary"):
            st.switch_page("app.py")

# Quick Navigation
st.markdown("---")
st.markdown("#### 🔗 Quick Navigation")
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("📊 Analytics", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")
with nav_col2:
    if st.button("🧘 Wellness", use_container_width=True):
        st.switch_page("pages/3_Wellness.py")
with nav_col3:
    if st.button("⏱️ Timer", use_container_width=True, disabled=True):
        pass  # Current page, so disabled

st.markdown("---")

# Initialize session state for timer
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_paused' not in st.session_state:
    st.session_state.timer_paused = False
if 'timer_started' not in st.session_state:
    st.session_state.timer_started = False
if 'remaining_time' not in st.session_state:
    st.session_state.remaining_time = 25 * 60  # 25 minutes in seconds
if 'original_time' not in st.session_state:
    st.session_state.original_time = 25 * 60
if 'completed_sessions' not in st.session_state:
    st.session_state.completed_sessions = 0
if 'current_quote' not in st.session_state:
    st.session_state.current_quote = get_focus_quote()
if 'elapsed_focus_time' not in st.session_state:
    st.session_state.elapsed_focus_time = 0
if 'show_session_feedback' not in st.session_state:
    st.session_state.show_session_feedback = False
if 'session_productivity_score' not in st.session_state:
    st.session_state.session_productivity_score = 85
if 'session_notes' not in st.session_state:
    st.session_state.session_notes = ""
if 'session_already_saved' not in st.session_state:
    st.session_state.session_already_saved = False  # Flag to prevent duplicate saves

# Initialize session state for motion detection simulation
if 'motion_status' not in st.session_state:
    st.session_state.motion_status = "Focused"  # "Focused" or "Unfocused"
if 'motion_last_check' not in st.session_state:
    st.session_state.motion_last_check = 0  # Time of last motion check
if 'unfocused_duration' not in st.session_state:
    st.session_state.unfocused_duration = 0  # Seconds of continuous unfocused status
if 'motion_warning_shown' not in st.session_state:
    st.session_state.motion_warning_shown = False  # Track if warning was shown
if 'motion_auto_paused' not in st.session_state:
    st.session_state.motion_auto_paused = False  # Track if timer was auto-paused

# Initialize session state for break timer and workflow
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "Focus"  # "Focus" or "Break"
if 'break_duration' not in st.session_state:
    st.session_state.break_duration = 5 * 60  # 5 minutes in seconds
if 'break_remaining_time' not in st.session_state:
    st.session_state.break_remaining_time = 5 * 60  # 5 minutes in seconds
if 'break_original_time' not in st.session_state:
    st.session_state.break_original_time = 5 * 60
if 'break_running' not in st.session_state:
    st.session_state.break_running = False
if 'break_paused' not in st.session_state:
    st.session_state.break_paused = False
if 'auto_start_break' not in st.session_state:
    st.session_state.auto_start_break = True  # Default: auto-start break
if 'auto_return_focus' not in st.session_state:
    st.session_state.auto_return_focus = True  # Default: auto-return to focus
if 'show_start_break_button' not in st.session_state:
    st.session_state.show_start_break_button = False  # Show "Start Break" button when focus ends
if 'focus_completed' not in st.session_state:
    st.session_state.focus_completed = False  # Track if focus session just completed

# Main Timer Section
with st.container():
    st.markdown("## ⏱️ Pomodoro Timer")
    
    # Current mode display with new emojis
    if st.session_state.current_mode == "Focus":
        mode_emoji = "🎯"
        mode_text = "Focus Session"
        mode_color = "info"
    else:
        mode_emoji = "🌿"
        mode_text = "Break Session"
        mode_color = "success"
    
    st.markdown(f"### {mode_emoji} Current Mode: **{mode_text}**")
    
    # Timer status based on current mode
    if st.session_state.current_mode == "Focus":
        if st.session_state.timer_running and not st.session_state.timer_paused:
            st.info("⏱️ **Focus Timer Running** - Focus on your task!")
        elif st.session_state.timer_paused:
            st.warning("⏸️ **Focus Timer Paused** - Ready to continue?")
        else:
            st.info("⏹️ **Focus Timer Stopped** - Ready to start a focus session?")
    else:  # Break mode
        if st.session_state.break_running and not st.session_state.break_paused:
            st.success("🌿 **Break Timer Running** - Time to relax and recharge!")
        elif st.session_state.break_paused:
            st.warning("⏸️ **Break Timer Paused** - Ready to continue your break?")
        else:
            st.success("⏹️ **Break Timer Stopped** - Ready to start a break?")
    
    # Timer display based on current mode
    if st.session_state.current_mode == "Focus":
        # Focus timer display
        current_seconds = max(0, st.session_state.remaining_time)
        minutes = current_seconds // 60
        seconds = current_seconds % 60
        time_display = f"{minutes:02d}:{seconds:02d}"
        
        # Calculate progress for progress bar
        if st.session_state.original_time > 0:
            progress = 1 - (current_seconds / st.session_state.original_time)
            progress = max(0.0, min(1.0, progress))
        else:
            progress = 0.0
        
        # Display focus timer
        delta_text = None
        if not st.session_state.timer_running:
            delta_text = f"{st.session_state.original_time // 60}-min focus"
        
        st.metric(
            label="Focus Time Remaining",
            value=time_display,
            delta=delta_text
        )
        
        # Progress bar
        st.progress(progress)
        st.caption(f"Focus session progress: {int(progress * 100)}%")
    else:
        # Break timer display
        current_seconds = max(0, st.session_state.break_remaining_time)
        minutes = current_seconds // 60
        seconds = current_seconds % 60
        time_display = f"{minutes:02d}:{seconds:02d}"
        
        # Calculate progress for progress bar
        if st.session_state.break_original_time > 0:
            progress = 1 - (current_seconds / st.session_state.break_original_time)
            progress = max(0.0, min(1.0, progress))
        else:
            progress = 0.0
        
        # Display break timer
        delta_text = None
        if not st.session_state.break_running:
            delta_text = f"{st.session_state.break_original_time // 60}-min break"
        
        st.metric(
            label="Break Time Remaining",
            value=time_display,
            delta=delta_text
        )
        
        # Progress bar
        st.progress(progress)
        st.caption(f"Break progress: {int(progress * 100)}%")
    
    # Timer controls with dynamic button labels based on current mode
    st.markdown("#### Controls")
    
    # Show "Start Break" button if focus just completed and auto-break is disabled
    if st.session_state.focus_completed and not st.session_state.auto_start_break:
        st.markdown("##### Focus session completed! 🎉")
        col_start_break, col_empty = st.columns([1, 3])
        with col_start_break:
            if st.button("🌿 Start Break Session", use_container_width=True, type="success"):
                st.session_state.current_mode = "Break"
                st.session_state.break_remaining_time = st.session_state.break_original_time
                st.session_state.break_running = False
                st.session_state.break_paused = False
                st.session_state.focus_completed = False
                st.session_state.show_start_break_button = False
                st.rerun()
    
    col_main, col_reset, col_switch = st.columns([2, 1, 1])
    
    with col_main:
        if st.session_state.current_mode == "Focus":
            # Focus mode controls
            if not st.session_state.timer_started:
                button_label = "▶️ Start Focus"
                button_type = "primary"
            elif st.session_state.timer_running and not st.session_state.timer_paused:
                button_label = "⏸️ Pause Focus"
                button_type = "secondary"
            else:
                button_label = "▶️ Resume Focus"
                button_type = "primary"
            
            # Main control button for focus timer
            if st.button(button_label, use_container_width=True, type=button_type):
                if not st.session_state.timer_started:
                    # Starting the focus timer for the first time
                    st.session_state.timer_running = True
                    st.session_state.timer_paused = False
                    st.session_state.timer_started = True
                    # Reset session saved flag for new session
                    st.session_state.session_already_saved = False
                elif st.session_state.timer_running and not st.session_state.timer_paused:
                    # Pausing the running focus timer
                    st.session_state.timer_paused = True
                else:
                    # Resuming the paused focus timer
                    st.session_state.timer_paused = False
                
                st.rerun()
        else:
            # Break mode controls
            if not st.session_state.break_running:
                button_label = "▶️ Start Break"
                button_type = "primary"
            elif st.session_state.break_running and not st.session_state.break_paused:
                button_label = "⏸️ Pause Break"
                button_type = "secondary"
            else:
                button_label = "▶️ Resume Break"
                button_type = "primary"
            
            # Main control button for break timer
            if st.button(button_label, use_container_width=True, type=button_type):
                if not st.session_state.break_running:
                    # Starting the break timer
                    st.session_state.break_running = True
                    st.session_state.break_paused = False
                elif st.session_state.break_running and not st.session_state.break_paused:
                    # Pausing the running break timer
                    st.session_state.break_paused = True
                else:
                    # Resuming the paused break timer
                    st.session_state.break_paused = False
                
                st.rerun()
    
    with col_reset:
        # Create columns for reset and save buttons
        col_reset_inner, col_save_inner = st.columns(2)
        
        with col_reset_inner:
            # Reset button (resets current mode timer and workflow states)
            if st.button("🔄 Reset", use_container_width=True):
                if st.session_state.current_mode == "Focus":
                    st.session_state.remaining_time = st.session_state.original_time
                    st.session_state.timer_running = False
                    st.session_state.timer_paused = False
                    st.session_state.timer_started = False
                    # Reset motion detection state
                    st.session_state.motion_status = "Focused"
                    st.session_state.motion_last_check = 0
                    st.session_state.unfocused_duration = 0
                    st.session_state.motion_warning_shown = False
                    st.session_state.motion_auto_paused = False
                    # Reset session saved flag
                    st.session_state.session_already_saved = False
                else:
                    st.session_state.break_remaining_time = st.session_state.break_original_time
                    st.session_state.break_running = False
                    st.session_state.break_paused = False
                
                # Reset workflow states
                st.session_state.focus_completed = False
                st.session_state.show_start_break_button = False
                st.session_state.show_session_feedback = False
                
                st.rerun()
        
        with col_save_inner:
            # Save incomplete session button (only shown during focus sessions)
            if st.session_state.current_mode == "Focus" and st.session_state.timer_started:
                if st.button("💾 Save Session", use_container_width=True, type="secondary"):
                    # Show feedback form for incomplete session
                    st.session_state.show_session_feedback = True
                    st.rerun()
    
    with col_switch:
        # Mode switch button (manual override)
        if st.session_state.current_mode == "Focus":
            switch_label = "🌿 Start Break"
            switch_type = "secondary"
            switch_disabled = False
        else:
            switch_label = "🎯 Start Focus"
            switch_type = "primary"
            switch_disabled = False
        
        # Disable switch button if we're showing the "Start Break" button
        if st.session_state.focus_completed and not st.session_state.auto_start_break:
            switch_disabled = True
        
        if st.button(switch_label, use_container_width=True, type=switch_type, disabled=switch_disabled):
            if st.session_state.current_mode == "Focus":
                # Switch to break mode
                st.session_state.current_mode = "Break"
                st.session_state.break_remaining_time = st.session_state.break_original_time
                st.session_state.break_running = False
                st.session_state.break_paused = False
                st.session_state.focus_completed = False
                st.session_state.show_start_break_button = False
                st.session_state.show_session_feedback = False
            else:
                # Switch to focus mode
                st.session_state.current_mode = "Focus"
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                # Reset motion detection state
                st.session_state.motion_status = "Focused"
                st.session_state.motion_last_check = 0
                st.session_state.unfocused_duration = 0
                st.session_state.motion_warning_shown = False
                st.session_state.motion_auto_paused = False
                st.session_state.focus_completed = False
                st.session_state.show_start_break_button = False
                st.session_state.show_session_feedback = False
                # Reset session saved flag for new session
                st.session_state.session_already_saved = False
            
            st.rerun()

# Session Feedback Section (shown when session is completed)
if st.session_state.show_session_feedback:
    st.markdown("---")
    st.markdown("### 📝 Session Feedback")
    
    with st.container():
        st.info("How was your focus session? Your feedback helps improve your analytics.")
        
        col_feedback1, col_feedback2 = st.columns(2)
        
        with col_feedback1:
            # Productivity score input
            st.session_state.session_productivity_score = st.slider(
                "Productivity Score (0-100)",
                min_value=0,
                max_value=100,
                value=st.session_state.session_productivity_score,
                help="How productive were you during this session?"
            )
            
            # Session type selection
            session_type = st.selectbox(
                "Session Type",
                ["focus", "deep_work", "learning", "planning", "creative"],
                index=0,
                help="What type of work were you doing?"
            )
        
        with col_feedback2:
            # Session notes
            st.session_state.session_notes = st.text_area(
                "Session Notes (optional)",
                value=st.session_state.session_notes,
                height=100,
                placeholder="What did you work on? Any distractions? What went well?",
                help="Optional notes about your session"
            )
        
        # Save feedback button
        col_save1, col_save2, col_save3 = st.columns([1, 2, 1])
        with col_save2:
            if st.button("💾 Save Session Feedback", use_container_width=True, type="primary"):
                try:
                    # Calculate actual focus duration (original time minus remaining time)
                    actual_focus_duration = st.session_state.original_time - st.session_state.remaining_time
                    
                    # Determine if session was completed (timer reached 0)
                    session_completed = st.session_state.remaining_time == 0
                    
                    session_id = session_storage.save_session(
                        focus_duration=actual_focus_duration,
                        break_duration=st.session_state.break_original_time,
                        completed=session_completed,
                        productivity_score=st.session_state.session_productivity_score,
                        session_type=session_type,
                        notes=st.session_state.session_notes
                    )
                    
                    completion_status = "completed" if session_completed else "saved"
                    st.success(f"✅ Session #{session_id} {completion_status} with your feedback!")
                    st.session_state.show_session_feedback = False
                    st.session_state.session_notes = ""  # Reset notes
                    st.session_state.session_already_saved = True  # Mark as saved
                    
                    # If session was completed, increment counter
                    if session_completed:
                        st.session_state.completed_sessions += 1
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Could not save session: {str(e)}")
            
            if st.button("⏭️ Skip Feedback", use_container_width=True, type="secondary"):
                # Save session with default values
                try:
                    actual_focus_duration = st.session_state.original_time - st.session_state.remaining_time
                    session_completed = st.session_state.remaining_time == 0
                    
                    session_id = session_storage.save_session(
                        focus_duration=actual_focus_duration,
                        break_duration=st.session_state.break_original_time,
                        completed=session_completed,
                        productivity_score=85,  # Default score
                        session_type="focus",
                        notes="Session saved without feedback"
                    )
                    
                    completion_status = "completed" if session_completed else "saved"
                    st.info(f"📝 Session #{session_id} {completion_status} with default values")
                    st.session_state.show_session_feedback = False
                    st.session_state.session_already_saved = True  # Mark as saved
                    
                    # If session was completed, increment counter
                    if session_completed:
                        st.session_state.completed_sessions += 1
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Could not save session: {str(e)}")

# Session Statistics and Settings
st.markdown("---")
col_stats, col_settings = st.columns(2)

with col_stats:
    with st.container():
        st.markdown("#### 📊 Session Statistics")
        
        # Completed sessions
        st.metric(
            label="Completed Sessions",
            value=st.session_state.completed_sessions,
            delta=f"Target: 4 sessions"
        )
        
        # Daily progress
        target_sessions = 4
        session_progress = min(st.session_state.completed_sessions / target_sessions, 1.0)
        
        st.progress(session_progress)
        st.caption(f"Daily progress: {st.session_state.completed_sessions}/{target_sessions} sessions")
        
with col_settings:
    with st.container():
        st.markdown("#### ⚙️ Timer Settings")
        
        # Focus session length selector
        session_length = st.select_slider(
            "Focus Session Duration",
            options=[15, 20, 25, 30, 45, 60],
            value=st.session_state.original_time // 60,
            help="Select your preferred focus session duration",
            disabled=st.session_state.timer_running or st.session_state.break_running
        )
        
        # Break duration selector
        break_length = st.select_slider(
            "Break Duration",
            options=[1, 2, 3, 5, 10, 15, 20],
            value=st.session_state.break_original_time // 60,
            help="Select your preferred break duration",
            disabled=st.session_state.timer_running or st.session_state.break_running
        )
        
        # Workflow configuration
        st.markdown("#### 🔄 Workflow Settings")

        # Check if settings should be locked
        settings_locked = (
            st.session_state.timer_running or
            st.session_state.break_running
        )

        # Warning message
        if settings_locked:
            st.warning("⚠️ Timer settings are locked while session is running.")

        # Enable interval breaks
        enable_interval_breaks = st.toggle(
            "Enable interval breaks",
            value=st.session_state.get("enable_interval_breaks", True),
            disabled=settings_locked,
            help="Automatically take short breaks during long focus sessions"
        )

        st.session_state.enable_interval_breaks = enable_interval_breaks

        # Interval settings
        if enable_interval_breaks:
            focus_interval = st.select_slider(
                "Take break every (minutes)",
                options=[5, 10, 15, 20, 25],
                value=st.session_state.get("focus_interval", 10 * 60) // 60,
                disabled=settings_locked
            )

            interval_break_duration = st.select_slider(
                "Interval break duration (minutes)",
                options=[1, 2, 3, 5],
                value=st.session_state.get("interval_break_duration", 3 * 60) // 60,
                disabled=settings_locked
            )

            # Save settings
            st.session_state.focus_interval = focus_interval * 60
            st.session_state.interval_break_duration = interval_break_duration * 60

        # Auto-start break toggle
        auto_break = st.toggle(
            "Auto-start break session",
            value=st.session_state.auto_start_break,
            disabled=settings_locked,
            help="When focus session ends, automatically start break timer"
        )

        if auto_break != st.session_state.auto_start_break:
            st.session_state.auto_start_break = auto_break
            st.rerun()

        # Auto-return to focus toggle
        if st.session_state.auto_start_break:
            auto_return = st.toggle(
                "Auto-return to focus after break",
                value=st.session_state.auto_return_focus,
                disabled=settings_locked,
                help="When break ends, automatically return to focus mode"
            )

            if auto_return != st.session_state.auto_return_focus:
                st.session_state.auto_return_focus = auto_return
                st.rerun()
        
        # Handle focus session length changes
        new_original_time = session_length * 60
        
        if new_original_time != st.session_state.original_time:
            # Calculate the ratio to adjust current timer if running
            if st.session_state.timer_running and st.session_state.remaining_time > 0:
                # Adjust timer proportionally to new session length
                ratio = st.session_state.remaining_time / st.session_state.original_time
                st.session_state.remaining_time = int(new_original_time * ratio)
            else:
                # Reset timer to new session length
                st.session_state.remaining_time = new_original_time
            
            st.session_state.original_time = new_original_time
            st.rerun()
        
        # Handle break duration changes
        new_break_original_time = break_length * 60
        
        if new_break_original_time != st.session_state.break_original_time:
            # Calculate the ratio to adjust current break timer if running
            if st.session_state.break_running and st.session_state.break_remaining_time > 0:
                # Adjust break timer proportionally to new duration
                ratio = st.session_state.break_remaining_time / st.session_state.break_original_time
                st.session_state.break_remaining_time = int(new_break_original_time * ratio)
            else:
                # Reset break timer to new duration
                st.session_state.break_remaining_time = new_break_original_time
            
            st.session_state.break_original_time = new_break_original_time
            st.session_state.break_duration = new_break_original_time
            st.rerun()

        # Daily target session customization
        st.markdown("#### 🎯 Daily Goals")

        target_sessions = st.number_input(
            "Daily Target Sessions",
            min_value=1,
            max_value=20,
            value=4,
            help="Set how many focus sessions you want to complete today"
        )

        # Save target into session state
        st.session_state.target_sessions = target_sessions

        # Ringtone customization
        st.markdown("#### 🔔 Notification Sound")

        # Ringtone selection
        ringtone = st.selectbox(
            "Choose Notification Sound",
            [
                "Classic Bell",
                "Soft Chime",
                "Digital Beep",
                "Nature Sound",
                "Minimal Click"
            ],
            index=0
        )

        # Sound mapping
        sound_files = {
            "Classic Bell": "sounds/classic_bell.mp3",
            "Soft Chime": "sounds/soft_chime.mp3",
            "Digital Beep": "sounds/digital_beep.mp3",
            "Nature Sound": "sounds/nature_sound.mp3",
            "Minimal Click": "sounds/minimal_click.mp3"
        }

        selected_sound = sound_files[ringtone]

        # Auto-play preview
        audio_html = f"""
        <audio autoplay>
            <source src="{selected_sound}" type="audio/mp3">
        </audio>
        """

        st.markdown(audio_html, unsafe_allow_html=True)

        # Upload custom ringtone
        uploaded_sound = st.file_uploader(
            "Upload Custom Ringtone",
            type=["mp3", "wav"]
        )

        # Preview uploaded sound
        if uploaded_sound is not None:
            st.audio(uploaded_sound)

        # Save ringtone choice
        st.session_state.ringtone = ringtone

        st.caption(f"Current ringtone: {ringtone}")
        
        # Pomodoro info
        with st.expander("ℹ️ About Pomodoro Technique"):
            st.markdown(f"""
            **The Pomodoro Technique:**
            - **{st.session_state.original_time // 60} minutes** of focused work
            - **{st.session_state.break_original_time // 60} minutes** of break
            - After **4 sessions**: Take a **15-30 minute** break
            - Proven to boost productivity and maintain focus
            
            **Your Custom Settings:**
            - Focus: {st.session_state.original_time // 60} minutes
            - Break: {st.session_state.break_original_time // 60} minutes
            - Ratio: {st.session_state.original_time // 60}:{st.session_state.break_original_time // 60}
            """)

# Motion Detection Status Section
st.markdown("---")
with st.container():
    st.markdown("#### 🎯 Smart Motion Detection System")
    st.caption("Simulated motion-based focus detection (demo version)")
    
    # Visual indicator
    motion_col1, motion_col2, motion_col3 = st.columns([1, 2, 1])
    
    with motion_col1:
        # Status indicator with color
        if st.session_state.motion_status == "Focused":
            status_color = "🟢"
            status_text = "Focused"
            status_style = "color: green; font-weight: bold;"
        else:
            status_color = "🔴"
            status_text = "Unfocused"
            status_style = "color: red; font-weight: bold;"
        
        st.markdown(f"<h3 style='{status_style}'>{status_color} {status_text}</h3>", unsafe_allow_html=True)
    
    with motion_col2:
        # Status details
        st.markdown(f"**Status:** {st.session_state.motion_status}")
        st.markdown(f"**Unfocused Duration:** {st.session_state.unfocused_duration} seconds")
        
        # Warning message if timer was auto-paused
        if st.session_state.motion_auto_paused:
            st.warning("⚠️ **Focus lost. Timer paused automatically.**")
            if st.button("✅ Acknowledge & Resume", use_container_width=True):
                st.session_state.motion_auto_paused = False
                st.session_state.motion_warning_shown = False
                st.session_state.unfocused_duration = 0
                st.session_state.motion_status = "Focused"
                st.rerun()
    
    with motion_col3:
        # Manual override controls
        st.markdown("**Manual Override:**")
        if st.button("🎯 Force Focused", use_container_width=True, type="secondary"):
            st.session_state.motion_status = "Focused"
            st.session_state.unfocused_duration = 0
            st.session_state.motion_warning_shown = False
            st.rerun()
        
        if st.button("🚫 Force Unfocused", use_container_width=True, type="secondary"):
            st.session_state.motion_status = "Unfocused Motion Detected"
            st.rerun()
    
    # System info
    with st.expander("ℹ️ About Motion Detection System"):
        st.markdown("""
        **Simulated Smart Motion Detection:**
        - **Focused:** Green indicator - You're maintaining good posture and focus
        - **Unfocused:** Red indicator - Motion patterns suggest distraction
        - **Check Interval:** Every 10 seconds during active timer
        - **Auto-Pause:** Timer pauses if unfocused for >20 seconds
        - **Demo Note:** This is a simulation using random patterns, not real webcam AI
        """)

# Motivational Quote Section
st.markdown("---")
with st.container():
    st.markdown("#### 💭 Focus Inspiration")
    
    quote_col1, quote_col2 = st.columns([3, 1])
    
    with quote_col1:
        st.info(f'"{st.session_state.current_quote["text"]}"')
        st.caption(f"— {st.session_state.current_quote["author"]}")
    
    with quote_col2:
        if st.button("🔄 New Quote", use_container_width=True):
            st.session_state.current_quote = get_focus_quote()
            st.rerun()

# Timer countdown logic with motion detection and improved workflow system
# This runs after the UI is rendered to handle the countdown

# First, check if timer just completed but feedback hasn't been shown yet
if st.session_state.current_mode == "Focus" and st.session_state.remaining_time == 0 and not st.session_state.timer_running:
    # Timer is at 0 and not running (completed)
    if not st.session_state.session_already_saved and not st.session_state.show_session_feedback:
        # Show session feedback form for completed session
        st.session_state.show_session_feedback = True
        st.session_state.session_already_saved = True
        st.balloons()

# Check if focus timer is running and not paused
elif st.session_state.timer_running and not st.session_state.timer_paused and st.session_state.current_mode == "Focus":
    # Timer is running, decrease by 1 second
    # Use time.sleep to wait 1 second before decreasing
    time.sleep(1)
    st.session_state.remaining_time -= 1
    # Track elapsed focus time
    st.session_state.elapsed_focus_time += 1
    
    # Motion detection simulation - check every 10 seconds
    current_time = st.session_state.original_time - st.session_state.remaining_time
    if current_time - st.session_state.motion_last_check >= 10:
        # Update motion status
        st.session_state.motion_status = simulate_motion_detection()
        st.session_state.motion_last_check = current_time
        
        # Track unfocused duration
        if st.session_state.motion_status == "Unfocused Motion Detected":
            st.session_state.unfocused_duration += 10
            
            # Check if unfocused for more than 20 seconds
            if st.session_state.unfocused_duration > 20 and not st.session_state.motion_auto_paused:
                # Auto-pause the timer
                st.session_state.timer_paused = True
                st.session_state.motion_auto_paused = True
                st.session_state.motion_warning_shown = True
        else:
            # Reset unfocused duration when focused
            st.session_state.unfocused_duration = 0
            st.session_state.motion_warning_shown = False
    
    # Check if focus timer just reached 0
    if st.session_state.remaining_time <= 0:
        st.session_state.remaining_time = 0
        st.session_state.timer_running = False
        st.session_state.timer_paused = False
        st.session_state.timer_started = False
        
        # Reset motion detection state
        st.session_state.motion_status = "Focused"
        st.session_state.unfocused_duration = 0
        st.session_state.motion_warning_shown = False
        st.session_state.motion_auto_paused = False
        
        # Only increment completed sessions and show feedback if session hasn't been saved yet
        if not st.session_state.session_already_saved:
            # Auto-complete session counter
            st.session_state.completed_sessions += 1
            
            # Show session feedback form
            st.session_state.show_session_feedback = True
            st.session_state.session_already_saved = True
            
            st.balloons()
        
        # Handle workflow based on auto-start break setting
        if st.session_state.auto_start_break:
            # Auto-start break mode
            st.session_state.current_mode = "Break"
            st.session_state.break_remaining_time = st.session_state.break_original_time
            st.session_state.break_running = True
            st.session_state.break_paused = False
            st.session_state.focus_completed = False
            st.session_state.show_start_break_button = False
            st.success("🎉 Focus session completed! Starting break timer...")
        else:
            # Show Start Break button
            st.session_state.focus_completed = True
            st.session_state.show_start_break_button = True
            st.success("🎉 Focus session completed! Ready for a break?")
    
    # Rerun to update the display after each second
    st.rerun()

# Check if break timer is running and not paused
elif st.session_state.break_running and not st.session_state.break_paused and st.session_state.current_mode == "Break":
    # Decrease break timer by 1 second
    if st.session_state.break_remaining_time > 0:
        # Use time.sleep to wait 1 second before decreasing
        time.sleep(1)
        st.session_state.break_remaining_time -= 1
        
        # Check if break timer reached 0
        if st.session_state.break_remaining_time <= 0:
            st.session_state.break_remaining_time = 0
            st.session_state.break_running = False
            st.session_state.break_paused = False
            
            st.balloons()
            
            # Handle workflow based on auto-return to focus setting
            if st.session_state.auto_return_focus:
                # Auto-return to focus mode
                st.session_state.current_mode = "Focus"
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                # Reset motion detection state
                st.session_state.motion_status = "Focused"
                st.session_state.unfocused_duration = 0
                st.session_state.motion_warning_shown = False
                st.session_state.motion_auto_paused = False
                st.session_state.focus_completed = False
                st.session_state.show_start_break_button = False
                st.success("🌿 Break completed! Ready for next focus session?")
            else:
                # Stay in break mode, show completion message
                st.success("🌿 Break completed! Take your time before starting next focus session.")
        
        # Rerun to update the display
        st.rerun()
    else:
        # Break timer already at 0, stop it
        st.session_state.break_running = False
        st.session_state.break_paused = False

# Debug information (collapsed by default)
with st.expander("🐛 Debug Information"):
    st.markdown("### Session State Debug")
    
    col_debug1, col_debug2 = st.columns(2)
    
    with col_debug1:
        st.write("**Timer State:**")
        st.write(f"- timer_running: {st.session_state.timer_running}")
        st.write(f"- timer_paused: {st.session_state.timer_paused}")
        st.write(f"- timer_started: {st.session_state.timer_started}")
        st.write(f"- remaining_time: {st.session_state.remaining_time}s ({st.session_state.remaining_time // 60}:{st.session_state.remaining_time % 60:02d})")
        st.write(f"- original_time: {st.session_state.original_time}s")
        st.write(f"- current_mode: {st.session_state.current_mode}")
    
    with col_debug2:
        st.write("**Session Saving State:**")
        st.write(f"- session_already_saved: {st.session_state.session_already_saved}")
        st.write(f"- show_session_feedback: {st.session_state.show_session_feedback}")
        st.write(f"- completed_sessions: {st.session_state.completed_sessions}")
        st.write(f"- focus_completed: {st.session_state.focus_completed}")
        st.write(f"- show_start_break_button: {st.session_state.show_start_break_button}")
        
        # Test database connection
        if st.button("Test Database Connection", type="secondary"):
            try:
                count = session_storage.get_session_count()
                st.success(f"Database connection OK. Total sessions: {count}")
            except Exception as e:
                st.error(f"Database error: {str(e)}")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)
with footer_col1:
    st.caption("**PAUSE Timer**")
    st.caption("Focus smart. Live well.")
with footer_col2:
    st.caption(f"**Current Mode**")
    if st.session_state.current_mode == "Focus":
        st.caption("🎯 Focus")
    else:
        st.caption("🌿 Break")
with footer_col3:
    st.caption(f"**Session Duration**")
    if st.session_state.current_mode == "Focus":
        st.caption(f"{st.session_state.original_time // 60} min focus")
    else:
        st.caption(f"{st.session_state.break_original_time // 60} min break")
with footer_col4:
    st.caption("**Status**")
    if st.session_state.current_mode == "Focus":
        if st.session_state.timer_running and not st.session_state.timer_paused:
            st.caption("🟢 Running")
        elif st.session_state.timer_paused:
            st.caption("🟡 Paused")
        else:
            st.caption("⚪ Stopped")
    else:
        if st.session_state.break_running and not st.session_state.break_paused:
            st.caption("🟢 Running")
        elif st.session_state.break_paused:
            st.caption("🟡 Paused")
        else:
            st.caption("⚪ Stopped")