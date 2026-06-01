# PAUSE App - Focus Settings Architecture

## Problem Solved
Fixed KeyError: 'focus_settings' not initialized properly across pages and inconsistent streak logic between Timer and Analytics pages.

## New Architecture

### 1. Global State (app.py)
```python
st.session_state["focus_settings"] = {
    "completed_sessions": 0,           # Sessions completed today
    "daily_target": 5,                 # Default daily target (range 1-10)
    "current_streak": 0,               # Current consecutive days streak
    "total_focus_time": 0,             # Total focus time in minutes
    "streak_updated_today": False,     # Whether streak was already incremented today
    "last_active_day": "YYYY-MM-DD"    # Last day user was active (for daily reset)
}
```

### 2. Daily Reset Logic (app.py)
- Automatically resets `completed_sessions` to 0 when a new day is detected
- Resets `streak_updated_today` to False for new day
- Updates `last_active_day` to current date

### 3. Timer Page Rules (pages/1_Timer.py)
- **ONLY** Timer page can update `focus_settings`
- Centralized `complete_session(focus_minutes)` function:
  1. Increments `completed_sessions`
  2. Adds `focus_time` to total
  3. Checks and updates streak if daily target is reached AND streak hasn't been updated today
  4. Prevents duplicate streak increases in same day

### 4. Analytics Page Rules (pages/2_Analytics.py)
- **READ-ONLY ONLY** - Never modifies `focus_settings`
- Safely accesses `focus_settings` with fallbacks
- Displays current statistics in a dedicated section
- All calculations are based on database data, not session state

### 5. Key Features
- **Single Source of Truth**: `focus_settings` is the only place for session statistics
- **No KeyError**: Always initialized before any page access
- **No Duplicate Logic**: All updates centralized in `complete_session()`
- **Daily Reset**: Automatic reset of daily counters
- **Streak Protection**: Prevents multiple streak increments per day

## Files Modified

### app.py
- Added global `focus_settings` initialization
- Added daily reset logic

### pages/1_Timer.py
- Updated `complete_session()` to use `focus_settings`
- Removed individual session state variables
- Updated statistics display
- Updated reset button
- Removed legacy `session_count` variable

### pages/2_Analytics.py
- Added session state initialization
- Added read-only statistics display
- Updated `calculate_burnout_level()` to safely access `focus_settings`
- Made page truly read-only

## How to Run
```bash
streamlit run app.py
```

The app will now run without KeyError issues and with consistent streak logic across all pages.