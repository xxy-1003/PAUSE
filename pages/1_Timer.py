import streamlit as st
import time
import os
from datetime import date
from pause_storage import session_storage

def complete_session(focus_minutes: int):
    """
    Complete a focus session and update statistics.
    ONLY this function should update session count and streak.
    
    Args:
        focus_minutes: Duration of the completed focus session in minutes
    """
    # Get focus settings
    settings = st.session_state["focus_settings"]
    
    # 1. Increment completed sessions
    settings["completed_sessions"] += 1
    
    # 2. Add focus time to total
    settings["total_focus_time"] += focus_minutes
    
    # 3. Check and update streak if daily target is achieved
    # Streak is only incremented once per day when target is reached
    if not settings.get("streak_updated_today", False):
        if settings["completed_sessions"] >= settings["daily_target"]:
            settings["current_streak"] += 1
            settings["streak_updated_today"] = True
            st.success(f"🎉 Daily target reached! Streak updated to {settings['current_streak']} days!")
    else:
        st.success("Session completed!")
    
    # Save session to database
    try:
        session_storage.save_session(
            username="default_user",
            duration_minutes=focus_minutes
        )
    except Exception as e:
        st.error(f"Failed to save session: {e}")

# ===== CRITICAL: SESSION STATE INITIALIZATION =====
# Initialize ALL session state variables FIRST before any UI code
# This prevents AttributeError: st.session_state has no attribute "current_mode"

# Required minimum session state variables
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Focus"  # "Focus" or "Break"

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "focus_mode" not in st.session_state:
    st.session_state.focus_mode = False

if "timer_paused" not in st.session_state:
    st.session_state.timer_paused = False

if "timer_started" not in st.session_state:
    st.session_state.timer_started = False

if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 25 * 60  # 25 minutes in seconds

if "original_time" not in st.session_state:
    st.session_state.original_time = 25 * 60

if "break_running" not in st.session_state:
    st.session_state.break_running = False

if "break_paused" not in st.session_state:
    st.session_state.break_paused = False

# Additional session state variables for full functionality
if "timer_status" not in st.session_state:
    st.session_state.timer_status = "stopped"  # "running", "paused", "stopped", "completed"

if "session_completed_flag" not in st.session_state:
    st.session_state.session_completed_flag = False  # Flag to prevent multiple completions

if "selected_sound" not in st.session_state:
    st.session_state.selected_sound = "🔔 Classical Bell"  # Default sound

if "break_duration" not in st.session_state:
    st.session_state.break_duration = 5 * 60  # 5 minutes in seconds

if "break_remaining_time" not in st.session_state:
    st.session_state.break_remaining_time = 5 * 60  # 5 minutes in seconds

if "break_original_time" not in st.session_state:
    st.session_state.break_original_time = 5 * 60

if "interval_break_enabled" not in st.session_state:
    st.session_state.interval_break_enabled = False

if "interval_break_minutes" not in st.session_state:
    st.session_state.interval_break_minutes = 30  # Take break every 30 minutes

if "interval_break_duration" not in st.session_state:
    st.session_state.interval_break_duration = 5 * 60  # 5 minutes in seconds

if "interval_break_start_time" not in st.session_state:
    st.session_state.interval_break_start_time = 0  # Timestamp when current interval started

# Session Statistics variables - Now using global focus_settings dictionary
# Ensure focus_settings exists (it should be initialized in app.py)
if "focus_settings" not in st.session_state:
    # Fallback initialization if app.py didn't run first
    today = date.today().isoformat()
    st.session_state["focus_settings"] = {
        "completed_sessions": 0,
        "daily_target": 5,
        "current_streak": 0,
        "total_focus_time": 0,
        "streak_updated_today": False,
        "last_active_day": today
    }

if "auto_start_break" not in st.session_state:
    st.session_state.auto_start_break = True

if "auto_return_focus" not in st.session_state:
    st.session_state.auto_return_focus = True

# Timer loop control
if "last_update_time" not in st.session_state:
    st.session_state.last_update_time = 0
    st.session_state.next_rerun_time = 0

# ===== SOUND SYSTEM - SINGLE SOURCE OF TRUTH =====
# BASE_DIR must point to project root (one level up from /pages)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOUND_DIR = os.path.join(BASE_DIR, "assets", "ringtone")

# Validate SOUND_DIR exists
if not os.path.exists(SOUND_DIR):
    st.error(f"❌ SOUND_DIR not found: {SOUND_DIR}")
    st.error(f"BASE_DIR: {BASE_DIR}")
    st.error(f"Current working directory: {os.getcwd()}")

SOUND_FILES = {
    "🔔 Classical Bell": os.path.join(SOUND_DIR, "classicBell.mp3"),
    "📟 Digital Beep": os.path.join(SOUND_DIR, "digitalBeep.mp3"),
    "🌿 Nature Sound": os.path.join(SOUND_DIR, "natureSound.mp3"),
    "🎵 Soft Chimes": os.path.join(SOUND_DIR, "softChimes.mp3"),
    "🧘 Zen Bell": os.path.join(SOUND_DIR, "zenBell.mp3")
}

# Validate all sound files exist
VALID_SOUND_FILES = {}
for name, path in SOUND_FILES.items():
    if os.path.exists(path):
        VALID_SOUND_FILES[name] = path
    else:
        st.warning(f"⚠️ Sound file not found: {name} -> {path}")

# Use only valid sound files
if VALID_SOUND_FILES:
    SOUND_FILES = VALID_SOUND_FILES
else:
    st.error("❌ No valid sound files found! Check assets/ringtone/ directory")
    # Create empty dict to prevent crashes
    SOUND_FILES = {}

DEFAULT_SOUND = os.path.join(SOUND_DIR, "classicBell.mp3") if os.path.exists(os.path.join(SOUND_DIR, "classicBell.mp3")) else None

def play_sound(sound_name, autoplay=False):
    """Play selected sound with fallback to default if file missing
    
    Args:
        sound_name: Name of the sound to play
        autoplay: If True, sound will auto-play (requires user interaction first)
    """
    if not SOUND_FILES:
        st.warning("No sound files available")
        return None
    
    file_path = SOUND_FILES.get(sound_name)
    
    if not file_path:
        st.warning(f"Sound '{sound_name}' not found in mapping")
        # Try to use first available sound
        if SOUND_FILES:
            first_sound = list(SOUND_FILES.keys())[0]
            file_path = SOUND_FILES[first_sound]
            st.info(f"Using '{first_sound}' instead")
        else:
            st.error("No sound files available")
            return None
    
    if not os.path.exists(file_path):
        st.warning(f"Sound file not found: {file_path}")
        # Try default sound
        if DEFAULT_SOUND and os.path.exists(DEFAULT_SOUND):
            file_path = DEFAULT_SOUND
            st.info("Using default sound")
        else:
            st.error("No valid sound file found")
            return None
    
    # Create audio player with autoplay if requested
    audio_player = st.audio(file_path, autoplay=autoplay)
    
    # Show helpful message if autoplay is requested
    if autoplay:
        st.info("💡 Click the play button to hear the sound preview")
    
    return audio_player

def play_session_completion_sound():
    """Play sound when session completes"""
    if 'selected_sound' in st.session_state and st.session_state.selected_sound in SOUND_FILES:
        play_sound(st.session_state.selected_sound)
    else:
        # Use default sound or first available
        if DEFAULT_SOUND and os.path.exists(DEFAULT_SOUND):
            st.audio(DEFAULT_SOUND)
        elif SOUND_FILES:
            # Use first available sound
            first_sound = list(SOUND_FILES.keys())[0]
            play_sound(first_sound)

def check_and_update_session_completion():
    """Check if focus session has completed and update statistics"""
    # Check if we're in focus mode and timer has reached 0
    if (st.session_state.current_mode == "Focus" and 
        st.session_state.timer_running and 
        not st.session_state.timer_paused and
        st.session_state.remaining_time <= 0):
        
        # Check if we haven't already marked this session as completed
        if not st.session_state.session_completed_flag:
            # Calculate focus minutes from session
            focus_minutes = st.session_state.original_time // 60
            
            # Use the centralized complete_session function
            complete_session(focus_minutes)

            # Mark session as completed to prevent duplicate increments
            st.session_state.session_completed_flag = True
            
            # Play completion sound
            play_session_completion_sound()
            
            # Show completion message (already shown in complete_session)
            
            # Auto-start break if enabled
            if st.session_state.auto_start_break:
                st.session_state.current_mode = "Break"
                st.session_state.break_remaining_time = st.session_state.break_original_time
                st.session_state.break_running = True
                st.session_state.break_paused = False
                st.info("🌿 Break timer started automatically")
            
            return True
    
    # Reset completion flag if timer is reset or stopped
    elif (st.session_state.current_mode == "Focus" and 
          not st.session_state.timer_running and
          st.session_state.remaining_time == st.session_state.original_time):
        st.session_state.session_completed_flag = False
    
    return False

def check_and_update_break_completion():
    """Check if break has completed and auto-return to focus if enabled"""
    # Check if we're in break mode and timer has reached 0
    if (st.session_state.current_mode == "Break" and 
        st.session_state.break_running and 
        not st.session_state.break_paused and
        st.session_state.break_remaining_time <= 0):
        
        # Play completion sound
        play_session_completion_sound()
        
        # Auto-return to focus if enabled
        if st.session_state.auto_return_focus:
            st.session_state.current_mode = "Focus"
            st.session_state.remaining_time = st.session_state.original_time
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_started = False
            st.session_state.timer_status = "stopped"
            st.session_state.session_completed_flag = False
            st.session_state.interval_break_start_time = 0  # Reset for next interval
            st.info("🎯 Returning to focus mode automatically")
        
        return True
    
    return False

def update_timers():
    """Update running timers based on elapsed time"""
    current_time = time.time()
    
    # Calculate time elapsed since last update
    if st.session_state.last_update_time > 0:
        time_elapsed = current_time - st.session_state.last_update_time
    else:
        # First time update, set last_update_time but don't decrement timer
        time_elapsed = 0
    
    # Update focus timer if running
    if (st.session_state.current_mode == "Focus" and 
        st.session_state.timer_running and 
        not st.session_state.timer_paused and
        st.session_state.remaining_time > 0):
        
        # Decrement focus timer by fractional seconds
        if time_elapsed > 0:
            # Decrement by actual elapsed time (can be fractional)
            st.session_state.remaining_time = max(0, st.session_state.remaining_time - time_elapsed)
            
            # Check for interval breaks (simplified approach)
            if st.session_state.interval_break_enabled:
                current_time = time.time()
                
                # Initialize interval start time if not set
                if st.session_state.interval_break_start_time == 0:
                    st.session_state.interval_break_start_time = current_time
                
                # Check if interval time has elapsed
                elapsed_interval_time = current_time - st.session_state.interval_break_start_time
                if elapsed_interval_time >= st.session_state.interval_break_minutes * 60:
                    st.info(f"⏰ Interval break triggered after {st.session_state.interval_break_minutes} minutes")
                    
                    # Auto-start interval break if enabled
                    if st.session_state.auto_start_break:
                        st.session_state.current_mode = "Break"
                        st.session_state.break_remaining_time = st.session_state.interval_break_duration
                        st.session_state.break_running = True
                        st.session_state.break_paused = False
                        st.session_state.timer_running = False
                        st.session_state.timer_paused = False
                        # Reset interval start time for next interval
                        st.session_state.interval_break_start_time = 0
    
    # Update break timer if running
    elif (st.session_state.current_mode == "Break" and 
          st.session_state.break_running and 
          not st.session_state.break_paused and
          st.session_state.break_remaining_time > 0):
        
        # Decrement break timer by fractional seconds
        if time_elapsed > 0:
            # Decrement by actual elapsed time (can be fractional)
            st.session_state.break_remaining_time = max(0, st.session_state.break_remaining_time - time_elapsed)
    
    # Update last update time
    st.session_state.last_update_time = current_time

# Page configuration for Timer page
st.set_page_config(
    page_title="PAUSE - Focus Timer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"  # Ensure sidebar is always visible
)

# Minimal CSS for theme consistency
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

# Import top navigation component
import sys
import os
# Add parent directory to path to import components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.navigation import create_top_navigation

# ============================================
# UPDATE TIMERS AND CHECK COMPLETION
# ============================================

update_timers()

session_completed = check_and_update_session_completion()

break_completed = check_and_update_break_completion()

# ============================================
# FOCUS MODE OVERLAY - DISTRACTION-FREE FULLSCREEN
# ============================================

if st.session_state.focus_mode:
    # ============================================
    # A. HIDE NAVIGATION DURING FOCUS MODE
    # ============================================
    # Navigation is NOT rendered when focus_mode is True
    # This creates a clean, distraction-free experience
    
    # ============================================
    # B. FULLSCREEN FOCUS LAYOUT
    # ============================================
    # Show only essential elements:
    # - Current mode (Focus / Break)
    # - Large countdown timer
    # - Progress indicator
    # - Control buttons
    
    # Hide everything else:
    # - Timer Settings
    # - Statistics
    # - Auto Settings
    # - Navigation Bar
    # - Any extra page content
    
    # Determine current mode and time
    if st.session_state.current_mode == "Focus":
        current_seconds = int(st.session_state.remaining_time)
        mode_text = "🎯 Focus Session"
        original_time = st.session_state.original_time
        is_running = st.session_state.timer_running
        is_paused = st.session_state.timer_paused
    else:
        current_seconds = int(st.session_state.break_remaining_time)
        mode_text = "🌿 Break Session"
        original_time = st.session_state.break_original_time
        is_running = st.session_state.break_running
        is_paused = st.session_state.break_paused
    
    # Format time display
    minutes = current_seconds // 60
    seconds = current_seconds % 60
    time_display = f"{minutes:02d}:{seconds:02d}"
    
    # Calculate progress
    if original_time > 0:
        progress = 1 - (current_seconds / original_time)
        progress = max(0.0, min(1.0, progress))
    else:
        progress = 0.0
    
    # ============================================
    # FOCUS MODE UI
    # ============================================
    
    # Center everything with fullscreen styling
    st.markdown("""
    <style>
        .focus-mode-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
            text-align: center;
            padding: 2rem;
        }
        .focus-mode-timer {
            font-size: 120px;
            font-weight: 800;
            color: #8A2BE2;
            margin: 1rem 0;
            font-family: monospace;
        }
        .focus-mode-status {
            font-size: 24px;
            color: #666;
            margin-bottom: 2rem;
        }
        .focus-mode-controls {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Status indicator
    status_text = ""
    if is_running and not is_paused:
        status_text = "⏱️ Running"
    elif is_paused:
        status_text = "⏸️ Paused"
    else:
        status_text = "⏹️ Stopped"
    
    # Main focus mode display
    st.markdown(f"""
    <div class="focus-mode-container">
        <h1 style="font-size: 36px; color: #4B0082; margin-bottom: 1rem;">{mode_text}</h1>
        <div class="focus-mode-status">{status_text}</div>
        <div class="focus-mode-timer">{time_display}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress)
    st.caption(f"Progress: {int(progress * 100)}%")
    
    # ============================================
    # C. PAUSE / RESUME BEHAVIOUR
    # ============================================
    # Button dynamically switches:
    # Running: ⏸ Pause
    # Paused: ▶ Resume
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Pause/Resume button
        if st.session_state.current_mode == "Focus":
            if st.session_state.timer_running and not st.session_state.timer_paused:
                button_label = "⏸ Pause"
                button_type = "secondary"
            else:
                button_label = "▶ Resume"
                button_type = "primary"
        else:
            if st.session_state.break_running and not st.session_state.break_paused:
                button_label = "⏸ Pause"
                button_type = "secondary"
            else:
                button_label = "▶ Resume"
                button_type = "primary"
        
        if st.button(button_label, use_container_width=True, type=button_type):
            if st.session_state.current_mode == "Focus":
                if st.session_state.timer_running and not st.session_state.timer_paused:
                    # Pause focus timer
                    st.session_state.timer_running = False
                    st.session_state.timer_paused = True
                else:
                    # Resume focus timer
                    st.session_state.timer_running = True
                    st.session_state.timer_paused = False
                    st.session_state.last_update_time = time.time()
            else:
                if st.session_state.break_running and not st.session_state.break_paused:
                    # Pause break timer
                    st.session_state.break_running = False
                    st.session_state.break_paused = True
                else:
                    # Resume break timer
                    st.session_state.break_running = True
                    st.session_state.break_paused = False
                    st.session_state.last_update_time = time.time()
            
            st.rerun()
    
    with col2:
        # Reset button
        if st.button("🔄 Reset", use_container_width=True):
            if st.session_state.current_mode == "Focus":
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                st.session_state.timer_status = "stopped"
                st.session_state.session_completed_flag = False
            else:
                st.session_state.break_remaining_time = st.session_state.break_original_time
                st.session_state.break_running = False
                st.session_state.break_paused = False
            
            st.rerun()
    
    with col3:
        # Mode switch button
        if st.session_state.current_mode == "Focus":
            switch_label = "🌿 Start Break"
        else:
            switch_label = "🎯 Start Focus"
        
        if st.button(switch_label, use_container_width=True):
            if st.session_state.current_mode == "Focus":
                # Switch to break mode
                st.session_state.current_mode = "Break"
                st.session_state.break_remaining_time = st.session_state.break_original_time
                st.session_state.break_running = False
                st.session_state.break_paused = False
                # Reset completion flag when switching to break
                st.session_state.session_completed_flag = False
            else:
                # Switch to focus mode
                st.session_state.current_mode = "Focus"
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                st.session_state.timer_status = "stopped"
                st.session_state.session_completed_flag = False
            
            st.rerun()
    
    with col4:
        # ============================================
        # G. EXIT BUTTON
        # ============================================
        # Only this button should leave focus_mode
        if st.button("❌ Exit Focus Mode", use_container_width=True):
            st.session_state.focus_mode = False
            st.rerun()
    
    # ============================================
    # D. AUTO REFRESH
    # ============================================
    # While timer or break timer is running:
    # if (st.session_state.timer_running or st.session_state.break_running):
    #     time.sleep(1)
    #     st.rerun()
    # This logic should exist inside Focus Mode before st.stop()
    
    if (st.session_state.timer_running and not st.session_state.timer_paused) or \
       (st.session_state.break_running and not st.session_state.break_paused):
        time.sleep(1)
        st.rerun()
    
    # ============================================
    # E. FOCUS SESSION COMPLETION
    # ============================================
    # When Focus completes:
    # If auto_start_break == True:
    #     stay inside focus_mode
    #     switch to Break mode automatically
    # Do NOT exit focus_mode.
    
    # ============================================
    # F. BREAK COMPLETION
    # ============================================
    # When Break completes:
    # If auto_return_focus == True:
    #     return to Focus mode
    # Do NOT exit focus_mode automatically.
    
    # Note: The completion logic is already handled by 
    # check_and_update_session_completion() and 
    # check_and_update_break_completion() functions above
    
    st.stop()

# ============================================
# NORMAL TIMER PAGE (WHEN NOT IN FOCUS MODE)
# ============================================

# Create top navigation (Timer is current page)
# Only show navigation when NOT in focus mode
create_top_navigation(current_page="Timer")

# Page title
st.title("PAUSE")
st.markdown("### Pomodoro Focus Timer ⏱️")

# Session state variables are already initialized at the top of the file
# All session state variables are guaranteed to exist before any UI code runs

# ============================================
# SECTION 1: TIMER DISPLAY
# ============================================

st.markdown("## ⏱️ Pomodoro Focus Timer")

# Current mode display
if st.session_state.current_mode == "Focus":
    mode_emoji = "🎯"
    mode_text = "Focus Session"
else:
    mode_emoji = "🌿"
    mode_text = "Break Session"

st.markdown(f"#### {mode_emoji} Current Mode: **{mode_text}**")

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
    current_seconds = int(max(0, st.session_state.remaining_time))
    minutes = int(current_seconds // 60)
    seconds = int(current_seconds % 60)
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
    current_seconds = int(max(0, st.session_state.break_remaining_time))
    minutes = int(current_seconds // 60)
    seconds = int(current_seconds % 60)
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

# ============================================
# SECTION 2: TIMER CONTROLS
# ============================================

st.markdown("#### ⚙️ Timer Controls")

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
                # First Start
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.session_state.timer_started = True
                st.session_state.timer_status = "running"
                st.session_state.last_update_time = time.time()

                # Enter Focus Overlay
                st.session_state.focus_mode = True

            elif st.session_state.timer_running and not st.session_state.timer_paused:
                # Pause
                st.session_state.timer_running = False
                st.session_state.timer_paused = True
                st.session_state.timer_status = "paused"

            else:
                # Resume
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.session_state.timer_status = "running"
                st.session_state.last_update_time = time.time()
                
                # Enter Focus Overlay when resuming
                st.session_state.focus_mode = True

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
                # Initialize last_update_time when break starts
                st.session_state.last_update_time = time.time()
                # Enter Focus Overlay when starting break
                st.session_state.focus_mode = True
            elif st.session_state.break_running and not st.session_state.break_paused:
                # Pausing the running break timer
                st.session_state.break_paused = True
            else:
                # Resuming the paused break timer
                st.session_state.break_paused = False
                # Update last_update_time when resuming
                st.session_state.last_update_time = time.time()
                # Enter Focus Overlay when resuming break
                st.session_state.focus_mode = True
            
            st.rerun()

with col_reset:
    # Reset button (resets current mode timer)
    if st.button("🔄 Reset", use_container_width=True):
        if st.session_state.current_mode == "Focus":
            st.session_state.remaining_time = st.session_state.original_time
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_started = False
            st.session_state.timer_status = "stopped"
            st.session_state.session_completed_flag = False
            st.session_state.interval_break_start_time = 0
        else:
            st.session_state.break_remaining_time = st.session_state.break_original_time
            st.session_state.break_running = False
            st.session_state.break_paused = False
            st.session_state.interval_break_start_time = 0
        st.rerun()

with col_switch:
    # Mode switch button (manual override)
    if st.session_state.current_mode == "Focus":
        switch_label = "🌿 Start Break"
        switch_type = "secondary"
    else:
        switch_label = "🎯 Start Focus"
        switch_type = "primary"
    
    if st.button(switch_label, use_container_width=True, type=switch_type):
        if st.session_state.current_mode == "Focus":
            # Switch to break mode
            st.session_state.current_mode = "Break"
            st.session_state.break_remaining_time = st.session_state.break_original_time
            st.session_state.break_running = False
            st.session_state.break_paused = False
            st.session_state.interval_break_start_time = 0
            # Reset completion flag when switching to break
            st.session_state.session_completed_flag = False
        else:
            # Switch to focus mode
            st.session_state.current_mode = "Focus"
            st.session_state.remaining_time = st.session_state.original_time
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_started = False
            st.session_state.timer_status = "stopped"
            st.session_state.session_completed_flag = False
            st.session_state.interval_break_start_time = 0
        st.rerun()

# ============================================
# SECTION 3: TIMER SETTINGS
# ============================================

st.markdown("---")
st.markdown("### ⚙️ Timer Settings")

# Check if timer is running to determine if settings should be locked
timer_active = (st.session_state.timer_running and not st.session_state.timer_paused) or (st.session_state.break_running and not st.session_state.break_paused)

if timer_active:
    st.info("🔒 **Focus Mode Active** - Settings are locked during active sessions")
    
    # Show current settings as read-only
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.markdown(f"**Focus Duration:** {st.session_state.original_time // 60} minutes")
        st.markdown(f"**Break Duration:** {st.session_state.break_original_time // 60} minutes")
    
    with col_set2:
        st.markdown(f"**Selected Sound:** {st.session_state.selected_sound}")
        if st.session_state.interval_break_enabled:
            st.markdown(f"**Interval Breaks:** Every {st.session_state.interval_break_minutes} min for {st.session_state.interval_break_duration // 60} min")
        else:
            st.markdown("**Interval Breaks:** Disabled")
else:
    # Settings are editable when timer is not running
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        # Focus session length selector
        session_length = st.select_slider(
            "Focus Session Duration",
            options=[1, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120],
            value=st.session_state.original_time // 60,
            help="Select your preferred focus session duration",
            key="focus_duration_slider"
        )
        
        # Update timer when focus duration changes
        if session_length != st.session_state.original_time // 60:
            new_original_time = session_length * 60
            st.session_state.remaining_time = new_original_time
            st.session_state.original_time = new_original_time

            st.rerun()

        # Break duration selector
        break_length = st.select_slider(
            "Break Duration",
            options=[1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40],
            value=st.session_state.break_original_time // 60,
            help="Select your preferred break duration",
            key="break_duration_slider"
        )
        
        # Update break timer when duration changes
        if break_length != st.session_state.break_original_time // 60:
            new_break_original_time = break_length * 60
            st.session_state.break_remaining_time = new_break_original_time
            st.session_state.break_original_time = new_break_original_time
            st.session_state.break_duration = new_break_original_time
    
            st.rerun()

    with col_set2:
        # Sound selector
        st.markdown("**🔔 Notification Sound**")
        
        # Get current sound from session state
        current_sound = st.session_state.get('selected_sound', "🔔 Classical Bell")
        
        # Find index of current sound
        sound_options = list(SOUND_FILES.keys()) if SOUND_FILES else ["🔔 Classical Bell"]
        current_index = sound_options.index(current_sound) if current_sound in sound_options else 0
        
        # Create selectbox
        selected_sound = st.selectbox(
            "Choose sound",
            options=sound_options,
            index=current_index,
            label_visibility="collapsed",
            key="main_sound_selector"
        )
        
        # Update selected sound in session state
        st.session_state.selected_sound = selected_sound
        
        # Preview button
        if st.button("🔊 Preview Sound", key="preview_sound", use_container_width=True):
            # Play sound immediately with autoplay
            if selected_sound in SOUND_FILES and os.path.exists(SOUND_FILES[selected_sound]):
                play_sound(selected_sound, autoplay=True)
                st.success(f"Playing: {selected_sound}")
            else:
                st.warning("Sound file not found")
        
        # Interval Break Settings
        st.markdown("**🔄 Interval Breaks**")
        
        # Enable/disable toggle
        interval_enabled = st.toggle(
            "Enable Interval Breaks",
            value=st.session_state.interval_break_enabled,
            help="Take regular breaks during long focus sessions",
            key="interval_toggle"
        )
        
        # Update interval break enabled state
        if interval_enabled != st.session_state.interval_break_enabled:
            st.session_state.interval_break_enabled = interval_enabled
            st.session_state.interval_break_start_time = 0
        
        # Show interval settings only when enabled
        if st.session_state.interval_break_enabled:
            
            interval_options = [5, 10, 15, 20, 25, 30, 35, 40]

            current_value = st.session_state.interval_break_minutes

            if current_value not in interval_options:
                current_value = 30
                st.session_state.interval_break_minutes = 30
            
            # Interval frequency selector - RESTORED with requested options
            interval_minutes = st.select_slider(
                "Take Break Every:",
                options=interval_options,
                value=current_value,
                help="How often to take interval breaks",
                key="interval_frequency"
            )
            
            # Update interval frequency
            if interval_minutes != st.session_state.interval_break_minutes:
                st.session_state.interval_break_minutes = interval_minutes
                st.session_state.interval_break_start_time = 0
            
            # Interval break duration selector - RESTORED with requested options
            interval_duration = st.select_slider(
                "Break Duration:",
                options=[1, 2, 3, 5, 10, 15, 20],
                value=st.session_state.interval_break_duration // 60,
                help="Duration of each interval break",
                key="interval_duration"
            )
            
            # Update interval break duration
            if interval_duration != st.session_state.interval_break_duration // 60:
                st.session_state.interval_break_duration = interval_duration * 60
        else:
            st.caption("Interval breaks disabled")

# ============================================
# SECTION 4: SESSION STATISTICS
# ============================================

st.markdown("---")
st.markdown("### 📊 Session Statistics")

col_stat1, col_stat2 = st.columns(2)

# -------------------------
# LEFT COLUMN
# -------------------------
with col_stat1:
    # Get focus settings for display
    settings = st.session_state["focus_settings"]

    st.metric(
        "Completed Sessions Today",
        settings["completed_sessions"]
    )

    st.metric(
        "Focus Time Today",
        f"{settings['total_focus_time']} min"
    )

    st.metric(
        "Current Streak",
        f"{settings['current_streak']} days"
    )

# -------------------------
# RIGHT COLUMN
# -------------------------
settings = st.session_state["focus_settings"]

with col_stat2:

    st.markdown("**🎯 Daily Session Target**")

    # =====================================
    # LOCK WHEN TIMER IS RUNNING
    # =====================================
    if timer_active:
        st.info("🔒 Statistics settings locked")

        st.markdown(
            f"**Target:** {settings['daily_target']} Sessions"
        )

    else:
        new_target = st.select_slider(
            "Target Sessions Per Day",
            options=list(range(1, 11)),  # ⭐ 改成 1–10
            value=settings["daily_target"],
            key="daily_target_slider"
        )

        settings["daily_target"] = new_target

    # =====================================
    # CURRENT PROGRESS
    # =====================================
    st.markdown(
        f"**Current:** {settings['completed_sessions']} Sessions"
    )

    # =====================================
    # PROGRESS BAR
    # =====================================
    if settings["daily_target"] > 0:

        progress = min(
            settings["completed_sessions"] / settings["daily_target"],
            1.0
        )

        st.progress(progress)

        st.caption(
            f"Daily progress: "
            f"{settings['completed_sessions']}/"
            f"{settings['daily_target']} "
            f"sessions ({int(progress * 100)}%)"
        )

    # =====================================
    # RESET SECTION
    # =====================================
    if not timer_active:

        st.markdown("---")
        st.markdown("**🗑 Reset Statistics**")

        if st.button(
            "Reset All Statistics",
            key="reset_stats",
            use_container_width=True
        ):
            # Get today's date for reset
            today = date.today().isoformat()
            
            st.session_state["focus_settings"] = {
                "completed_sessions": 0,
                "daily_target": settings["daily_target"],  # Keep user's target setting
                "current_streak": 0,
                "total_focus_time": 0,
                "streak_updated_today": False,
                "last_active_day": today
            }

            st.success("Statistics reset successfully!")
                    
# ============================================
# SECTION 5: AUTO-SETTINGS
# ============================================

st.markdown("---")
st.markdown("### ⚡ Auto-Settings")

if timer_active:
    st.info("🔒 **Focus Mode Active** - Auto-settings are locked during active sessions")
    
    # Show current auto-settings as read-only
    col_auto1, col_auto2 = st.columns(2)
    
    with col_auto1:
        st.markdown(f"**Auto Start Break:** {'✅ Enabled' if st.session_state.auto_start_break else '❌ Disabled'}")
    
    with col_auto2:
        st.markdown(f"**Auto Return Focus:** {'✅ Enabled' if st.session_state.auto_return_focus else '❌ Disabled'}")
else:
    # Auto-settings are editable when timer is not running
    col_auto1, col_auto2 = st.columns(2)
    
    with col_auto1:
        # Auto Start Break toggle
        auto_start_break = st.toggle(
            "Auto Start Break",
            value=st.session_state.auto_start_break,
            help="Automatically start break timer when focus session ends",
            key="auto_start_break_toggle"
        )
        
        # Update auto-start break setting
        if auto_start_break != st.session_state.auto_start_break:
            st.session_state.auto_start_break = auto_start_break
    
    with col_auto2:
        # Auto Return Focus toggle
        auto_return_focus = st.toggle(
            "Auto Return Focus",
            value=st.session_state.auto_return_focus,
            help="Automatically return to focus mode when break ends",
            key="auto_return_focus_toggle"
        )
        
        # Update auto-return focus setting
        if auto_return_focus != st.session_state.auto_return_focus:
            st.session_state.auto_return_focus = auto_return_focus


# # ============================================
# # AUTO-RERUN LOGIC FOR TIMER COUNTDOWN
# # ============================================

if (st.session_state.timer_running and not st.session_state.timer_paused) or \
   (st.session_state.break_running and not st.session_state.break_paused):

    time.sleep(1)
    st.rerun()