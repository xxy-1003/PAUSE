import streamlit as st
import time
import os

# ===== CRITICAL: SESSION STATE INITIALIZATION =====
# Initialize ALL session state variables FIRST before any UI code
# This prevents AttributeError: st.session_state has no attribute "current_mode"

# Required minimum session state variables
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Focus"  # "Focus" or "Break"

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

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
if "session_count" not in st.session_state:
    st.session_state.session_count = 0

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

if "elapsed_focus_time" not in st.session_state:
    st.session_state.elapsed_focus_time = 0  # Track elapsed focus time for interval breaks

if "interval_break_triggered" not in st.session_state:
    st.session_state.interval_break_triggered = False  # Prevent multiple triggers

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

# Create top navigation (Timer is current page)
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
                # Starting the focus timer for the first time
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.session_state.timer_started = True
                st.session_state.timer_status = "running"
            elif st.session_state.timer_running and not st.session_state.timer_paused:
                # Pausing the running focus timer
                st.session_state.timer_paused = True
                st.session_state.timer_status = "paused"
            else:
                # Resuming the paused focus timer
                st.session_state.timer_paused = False
                st.session_state.timer_status = "running"
            
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
    # Reset button (resets current mode timer)
    if st.button("🔄 Reset", use_container_width=True):
        if st.session_state.current_mode == "Focus":
            st.session_state.remaining_time = st.session_state.original_time
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_started = False
            st.session_state.timer_status = "stopped"
            st.session_state.session_completed_flag = False
            st.session_state.elapsed_focus_time = 0
            st.session_state.interval_break_triggered = False
        else:
            st.session_state.break_remaining_time = st.session_state.break_original_time
            st.session_state.break_running = False
            st.session_state.break_paused = False
            st.session_state.interval_break_triggered = False
        
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
            st.session_state.interval_break_triggered = False
        else:
            # Switch to focus mode
            st.session_state.current_mode = "Focus"
            st.session_state.remaining_time = st.session_state.original_time
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_started = False
            st.session_state.timer_status = "stopped"
            st.session_state.session_completed_flag = False
            st.session_state.elapsed_focus_time = 0
            st.session_state.interval_break_triggered = False
        
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
            options=[15, 20, 25, 30, 45, 60],
            value=st.session_state.original_time // 60,
            help="Select your preferred focus session duration",
            key="focus_duration_slider"
        )
        
        # Handle focus session length changes
        new_original_time = session_length * 60
        
        if new_original_time != st.session_state.original_time:
            # Reset timer to new session length
            st.session_state.remaining_time = new_original_time
            st.session_state.original_time = new_original_time
            st.rerun()
        
        # Break duration selector
        break_length = st.select_slider(
            "Break Duration",
            options=[1, 2, 3, 5, 10, 15, 20],
            value=st.session_state.break_original_time // 60,
            help="Select your preferred break duration",
            key="break_duration_slider"
        )
        
        # Handle break duration changes
        new_break_original_time = break_length * 60
        
        if new_break_original_time != st.session_state.break_original_time:
            # Reset break timer to new duration
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
        
        # Save selected sound in session state
        st.session_state.selected_sound = selected_sound
        
        # Preview button
        if st.button("🔊 Preview Sound", key="preview_sound", use_container_width=True):
            # Show audio player for preview
            if selected_sound in SOUND_FILES and os.path.exists(SOUND_FILES[selected_sound]):
                st.audio(SOUND_FILES[selected_sound])
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
        
        if interval_enabled != st.session_state.interval_break_enabled:
            st.session_state.interval_break_enabled = interval_enabled
            st.session_state.interval_break_triggered = False
            st.session_state.elapsed_focus_time = 0
            st.rerun()
        
        # Show interval settings only when enabled
        if st.session_state.interval_break_enabled:
            # Interval frequency selector - RESTORED with requested options
            interval_minutes = st.select_slider(
                "Take Break Every:",
                options=[5, 10, 15, 20, 25],
                value=st.session_state.interval_break_minutes,
                help="How often to take interval breaks",
                key="interval_frequency"
            )
            
            if interval_minutes != st.session_state.interval_break_minutes:
                st.session_state.interval_break_minutes = interval_minutes
                st.session_state.interval_break_triggered = False
                st.session_state.elapsed_focus_time = 0
                st.rerun()
            
            # Interval break duration selector - RESTORED with requested options
            interval_duration = st.select_slider(
                "Break Duration:",
                options=[1, 2, 3, 5],
                value=st.session_state.interval_break_duration // 60,
                help="Duration of each interval break",
                key="interval_duration"
            )
            
            if interval_duration != st.session_state.interval_break_duration // 60:
                st.session_state.interval_break_duration = interval_duration * 60
                st.rerun()
        else:
            st.caption("Interval breaks disabled")

with col_timer_display:
    # Timer Display Section
    st.markdown("### 🎯 Timer Display")
    
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
    
    # Timer Controls
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
                    # Starting the focus timer for the first time
                    st.session_state.timer_running = True
                    st.session_state.timer_paused = False
                    st.session_state.timer_started = True
                    st.session_state.timer_status = "running"
                elif st.session_state.timer_running and not st.session_state.timer_paused:
                    # Pausing the running focus timer
                    st.session_state.timer_paused = True
                    st.session_state.timer_status = "paused"
                else:
                    # Resuming the paused focus timer
                    st.session_state.timer_paused = False
                    st.session_state.timer_status = "running"
                
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
        # Reset button (resets current mode timer)
        if st.button("🔄 Reset", use_container_width=True):
            if st.session_state.current_mode == "Focus":
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                st.session_state.timer_status = "stopped"
                st.session_state.session_completed_flag = False
                st.session_state.elapsed_focus_time = 0
                st.session_state.interval_break_triggered = False
            else:
                st.session_state.break_remaining_time = st.session_state.break_original_time
                st.session_state.break_running = False
                st.session_state.break_paused = False
                st.session_state.interval_break_triggered = False
            
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
                st.session_state.interval_break_triggered = False
            else:
                # Switch to focus mode
                st.session_state.current_mode = "Focus"
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                st.session_state.timer_status = "stopped"
                st.session_state.session_completed_flag = False
                st.session_state.elapsed_focus_time = 0
                st.session_state.interval_break_triggered = False
            
            st.rerun()

with col_timer_settings:
    # Timer Settings Section
    st.markdown("### ⚙️ Timer Settings")
    
    # Focus session length selector
    session_length = st.select_slider(
        "Focus Session Duration",
        options=[15, 20, 25, 30, 45, 60],
        value=st.session_state.original_time // 60,
        help="Select your preferred focus session duration",
        key="focus_duration_slider"
    )
    
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
    
    # Break duration selector
    break_length = st.select_slider(
        "Break Duration",
        options=[1, 2, 3, 5, 10, 15, 20],
        value=st.session_state.break_original_time // 60,
        help="Select your preferred break duration",
        key="break_duration_slider"
    )
    
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
    
    # Sound selector
    st.markdown("**🔔 Notification Sound**")
    
    # Get current sound from session state
    current_sound = st.session_state.get('selected_sound', "🔔 Classical Bell")
    
    # Find index of current sound
    sound_options = list(SOUND_FILES.keys()) if SOUND_FILES else ["🔔 Classical Bell"]
    current_index = sound_options.index(current_sound) if current_sound in sound_options else 0
    
    # Create selectbox with on_change callback simulation
    selected_sound = st.selectbox(
        "Choose sound",
        options=sound_options,
        index=current_index,
        label_visibility="collapsed",
        key="main_sound_selector"
    )
    
    # Check if sound selection changed
    if 'previous_sound' not in st.session_state:
        st.session_state.previous_sound = selected_sound
    
    # Auto-play when sound selection changes
    sound_changed = st.session_state.previous_sound != selected_sound
    
    # Save selected sound in session state
    st.session_state.selected_sound = selected_sound
    
    # Create a container for the preview button
    preview_col1, preview_col2 = st.columns([3, 1])
    
    with preview_col1:
        # Show visual feedback when sound changes
        if sound_changed and SOUND_FILES:
            st.success(f"🎵 Selected: {selected_sound}")
            st.session_state.previous_sound = selected_sound
        
        # Show preview feedback if triggered
        if st.session_state.get('show_preview_feedback', False):
            st.success(f"🔊 Playing preview of: {selected_sound}")
            # Reset the flag
            st.session_state.show_preview_feedback = False
    
    with preview_col2:
        # Manual preview button with immediate feedback
        if st.button("🔊 Preview", key="preview_sound", use_container_width=True):
            # Set flag to show feedback
            st.session_state.show_preview_feedback = True
            
            # Show audio player for preview (user can click play)
            if selected_sound in SOUND_FILES and os.path.exists(SOUND_FILES[selected_sound]):
                st.audio(SOUND_FILES[selected_sound])
            else:
                st.warning("Sound file not found")
            
            # Rerun to show feedback
            st.rerun()
    
    # Interval Break Settings
    st.markdown("**🔄 Interval Breaks**")
    
    # Enable/disable toggle
    interval_enabled = st.toggle(
        "Enable",
        value=st.session_state.interval_break_enabled,
        help="Take regular breaks during long focus sessions",
        key="interval_toggle"
    )
    
    if interval_enabled != st.session_state.interval_break_enabled:
        st.session_state.interval_break_enabled = interval_enabled
        st.session_state.interval_break_triggered = False
        st.session_state.elapsed_focus_time = 0
        st.rerun()
    
    # Show interval settings only when enabled
    if st.session_state.interval_break_enabled:
        # Interval frequency selector
        interval_minutes = st.select_slider(
            "Every (minutes)",
            options=[15, 20, 25, 30, 45, 60, 90, 120],
            value=st.session_state.interval_break_minutes,
            help="How often to take interval breaks",
            key="interval_frequency"
        )
        
        if interval_minutes != st.session_state.interval_break_minutes:
            st.session_state.interval_break_minutes = interval_minutes
            st.session_state.interval_break_triggered = False
            st.session_state.elapsed_focus_time = 0
            st.rerun()
        
        # Interval break duration selector
        interval_duration = st.select_slider(
            "Duration (minutes)",
            options=[1, 2, 3, 5, 10, 15],
            value=st.session_state.interval_break_duration // 60,
            help="Duration of each interval break",
            key="interval_duration"
        )
        
        if interval_duration != st.session_state.interval_break_duration // 60:
            st.session_state.interval_break_duration = interval_duration * 60
            st.rerun()
        
        # Show current interval progress (info only, not interactive)
        if st.session_state.timer_running and st.session_state.current_mode == "Focus":
            progress = min(st.session_state.elapsed_focus_time / (st.session_state.interval_break_minutes * 60), 1.0)
            st.progress(progress)
            remaining = max(0, st.session_state.interval_break_minutes * 60 - st.session_state.elapsed_focus_time)
            st.caption(f"Next break in: {remaining // 60}:{remaining % 60:02d}")
        elif st.session_state.interval_break_enabled:
            st.caption("Interval breaks enabled")
    else:
        st.caption("Interval breaks disabled")

# ============================================
# BOTTOM SECTION: SESSION STATISTICS + DAILY GOAL
# ============================================

st.markdown("---")
st.markdown("## 📊 Productivity Tracking")

# Create two columns for Session Statistics (left) and Daily Session Target (right)
col_stats, col_target = st.columns([1, 1])

with col_stats:
    # Session Statistics Section
    st.markdown("### � Session Statistics")
    
    # Completed sessions
    st.metric(
        label="Completed Sessions",
        value=st.session_state.session_count,
        delta=f"Today's total"
    )
    
    # Daily progress (using default target of 4 sessions)
    default_target = 4
    session_progress = min(st.session_state.session_count / default_target, 1.0)
    
    st.progress(session_progress)
    st.caption(f"Progress: {st.session_state.session_count}/{default_target} sessions")
    
    # Current Streak (get from database)
    try:
        from data_storage import session_storage
        insights = session_storage.get_advanced_insights()
        current_streak = insights.get('current_streak', 0)
        streak_emoji = "🔥" if current_streak >= 7 else "⚡" if current_streak >= 3 else "📈"
        st.metric(
            label="Current Streak",
            value=f"{current_streak} days",
            delta=f"{streak_emoji} Keep it going!"
        )
    except:
        st.metric(
            label="Current Streak",
            value="0 days",
            delta="Start a streak!"
        )

with col_target:
    # Daily Session Target Section
    st.markdown("### 🎯 Daily Session Target")
    
    # Initialize daily target in session state if not exists
    if 'daily_target' not in st.session_state:
        st.session_state.daily_target = 4
    
    # Daily target setting
    daily_target = st.number_input(
        "Target Sessions per Day",
        min_value=1,
        max_value=10,
        value=st.session_state.daily_target,
        help="Set your daily focus session goal",
        key="daily_target_input"
    )
    
    # Update session state if changed
    if daily_target != st.session_state.daily_target:
        st.session_state.daily_target = daily_target
        st.rerun()
    
    # Display current target
    st.markdown(f"#### 🎯 Target: **{daily_target} sessions**")
    
    # Calculate progress toward target
    progress_toward_target = min(st.session_state.session_count / daily_target, 1.0) if daily_target > 0 else 0
    
    # Progress visualization
    st.progress(progress_toward_target)
    
    # Status message
    if st.session_state.session_count >= daily_target:
        st.success(f"✅ Goal achieved! {st.session_state.session_count}/{daily_target} sessions")
    elif st.session_state.session_count > 0:
        remaining = daily_target - st.session_state.session_count
        st.info(f"📊 Progress: {st.session_state.session_count}/{daily_target} sessions ({remaining} to go)")
    else:
        st.warning(f"⏳ No sessions yet. Target: {daily_target} sessions")
    
    # Recommendation
    if daily_target > 0:
        if daily_target <= 3:
            st.caption("🎯 **Beginner goal** - Great for building consistency")
        elif daily_target <= 6:
            st.caption("⚡ **Intermediate goal** - Balanced productivity")
        else:
            st.caption("🔥 **Advanced goal** - High-intensity focus")

# Timer countdown logic
# Check if focus timer is running and not paused
if st.session_state.timer_running and not st.session_state.timer_paused and st.session_state.current_mode == "Focus":
    # Decrease focus timer by 1 second
    if st.session_state.remaining_time > 0:
        # Use time.sleep to wait 1 second before decreasing
        time.sleep(1)
        st.session_state.remaining_time -= 1
        
        # Track elapsed focus time for interval breaks
        if st.session_state.interval_break_enabled:
            st.session_state.elapsed_focus_time += 1
            
            # Check if it's time for an interval break
            if (st.session_state.elapsed_focus_time >= st.session_state.interval_break_minutes * 60 and 
                not st.session_state.interval_break_triggered):
                
                # Trigger interval break
                st.session_state.interval_break_triggered = True
                st.session_state.current_mode = "Break"
                st.session_state.break_remaining_time = st.session_state.interval_break_duration
                st.session_state.break_original_time = st.session_state.interval_break_duration
                st.session_state.break_running = True
                st.session_state.break_paused = False
                
                # Pause focus timer
                st.session_state.timer_paused = True
                
                st.toast(f"🌿 Interval break time! Take {st.session_state.interval_break_duration // 60} minutes to recharge", icon="✅")
                st.rerun()
        
        # Check if focus timer reached 0
        if st.session_state.remaining_time <= 0:
            st.session_state.remaining_time = 0
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_started = False
            
            # Reset interval tracking
            st.session_state.elapsed_focus_time = 0
            st.session_state.interval_break_triggered = False
            
            # SESSION COMPLETION LOGIC - Only run once
            if not st.session_state.session_completed_flag:
                st.session_state.timer_status = "completed"
                st.session_state.session_count += 1
                st.session_state.remaining_time = st.session_state.original_time  # Reset for next session
                st.session_state.session_completed_flag = True
                
                # Show toast notification
                st.toast("🎉 Session completed! +1 Focus Session", icon="✅")
                
                # Play completion sound
                play_session_completion_sound()
            
            st.rerun()
        else:
            # Rerun to update the display
            st.rerun()
    else:
        # Focus timer already at 0, stop it
        st.session_state.timer_running = False
        st.session_state.timer_paused = False
        st.session_state.timer_started = False
        st.session_state.elapsed_focus_time = 0
        st.session_state.interval_break_triggered = False

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
            
            # Handle interval break completion
            if st.session_state.interval_break_enabled and st.session_state.interval_break_triggered:
                # Resume focus timer after interval break
                st.session_state.current_mode = "Focus"
                st.session_state.timer_paused = False
                st.session_state.interval_break_triggered = False
                st.session_state.elapsed_focus_time = 0  # Reset interval tracking
                
                st.toast("🌿 Interval break completed! Back to focus mode", icon="✅")
            else:
                # Regular break completion
                st.session_state.current_mode = "Focus"
                st.session_state.remaining_time = st.session_state.original_time
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_started = False
                st.session_state.timer_status = "stopped"
                st.session_state.session_completed_flag = False
                
                st.toast("🌿 Break completed! Ready for next focus session?", icon="✅")
            
            st.rerun()
        else:
            # Rerun to update the display
            st.rerun()
    else:
        # Break timer already at 0, stop it
        st.session_state.break_running = False
        st.session_state.break_paused = False

# Reset completion flag when timer is reset or mode changes
if st.session_state.timer_status != "completed":
    st.session_state.session_completed_flag = False

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