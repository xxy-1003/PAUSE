# PAUSE Storage System

## Overview

This document describes the SQLite-based data storage system for the PAUSE Pomodoro application. The system provides a simple, production-ready storage layer for focus sessions with username support.

## Files Created

1. **`pause_storage.py`** - Main storage module with `SessionStorage` class
2. **`pause.db`** - SQLite database file (created automatically)
3. **`test_pause_storage.py`** - Test script to verify functionality
4. **`example_usage.py`** - Example integration with timer functionality

## Database Schema

### Table: `sessions`
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    session_date TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    completed_at TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_username_date ON sessions (username, session_date);
```

## SessionStorage Class Methods

### Core Methods
- `save_session(username, duration_minutes)` - Save a completed session
- `get_today_sessions(username)` - Get today's sessions
- `get_weekly_sessions(username)` - Get this week's sessions
- `get_all_sessions(username)` - Get all user sessions
- `get_total_focus_time(username)` - Get total focus time statistics

### Advanced Methods
- `get_daily_summary(username, days=30)` - Get daily summary for last N days
- `get_user_statistics(username)` - Get comprehensive user statistics
- `export_to_csv(username, filepath)` - Export sessions to CSV
- `generate_mock_data(username, days=60)` - Generate mock data for testing

### Utility Methods
- `clear_user_sessions(username)` - Clear all sessions for a user
- `clear_all_sessions()` - Clear all sessions from database

## Global Instance

For easy access, a global instance is available:

```python
from pause_storage import session_storage

# Save a session
session_id = session_storage.save_session("alice", 25)

# Get today's sessions
today_df = session_storage.get_today_sessions("alice")

# Get total focus time
stats = session_storage.get_total_focus_time("alice")
print(f"Total hours: {stats['total_hours']}")
print(f"Session count: {stats['session_count']}")
```

## Integration with Existing PAUSE App

### Option 1: Replace Existing Storage (Recommended)

Update the Timer page (`pages/1_Timer.py`) to use the new storage system:

```python
# Replace existing import
# from data_storage import session_storage  # Old
from pause_storage import session_storage  # New

# When a session completes:
def complete_focus_session(duration_minutes):
    username = st.session_state.get("username", "default_user")
    session_id = session_storage.save_session(username, duration_minutes)
    st.success(f"Session saved! (ID: {session_id})")
```

### Option 2: Keep Both Systems

If you want to maintain backward compatibility, you can use both systems:

```python
# Import both
from data_storage import session_storage as old_storage
from pause_storage import session_storage as new_storage

# Use new storage for new features
session_id = new_storage.save_session("username", 25)

# Migrate old data if needed
old_sessions = old_storage.get_sessions()
# Convert and save to new storage...
```

## Testing

Run the test script to verify functionality:

```bash
python test_pause_storage.py
```

Or run the built-in test:

```bash
python -c "from pause_storage import test_storage_system; test_storage_system()"
```

## Example Usage

See `example_usage.py` for a complete example of integrating the storage system with a timer class:

```python
from pause_storage import session_storage

class PauseTimer:
    def __init__(self, username="default_user"):
        self.username = username
    
    def complete_session(self, duration_minutes):
        session_id = session_storage.save_session(self.username, duration_minutes)
        print(f"✅ Session completed and saved! (ID: {session_id})")
        return session_id
    
    def show_statistics(self):
        stats = session_storage.get_user_statistics(self.username)
        print(f"Today sessions: {stats['today_sessions']}")
        print(f"Total hours: {stats['total_hours']}")
        print(f"Current streak: {stats['current_streak']} days")
```

## Error Handling

The storage system includes comprehensive error handling:

```python
try:
    session_id = session_storage.save_session("username", 25)
except ValueError as e:
    print(f"Invalid input: {e}")
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Data Export

Export user sessions to CSV:

```python
csv_path = session_storage.export_to_csv("username", "my_sessions.csv")
print(f"Exported to: {csv_path}")
```

## Mock Data Generation

Generate test data for development:

```python
# Generate 30 days of mock data
mock_count = session_storage.generate_mock_data("test_user", 30)
print(f"Generated {mock_count} mock sessions")
```

## Performance Considerations

1. **Indexing**: The `idx_sessions_username_date` index ensures fast queries by username and date
2. **Connection Pooling**: Each method manages its own database connection
3. **Error Recovery**: Methods handle database errors gracefully
4. **Data Validation**: Input validation prevents invalid data

## Security Notes

1. **SQL Injection Protection**: Uses parameterized queries
2. **Input Validation**: Validates duration_minutes > 0
3. **Error Messages**: Generic error messages don't expose database details
4. **File Permissions**: Database file has appropriate permissions

## Migration from Existing System

If migrating from the existing `data_storage.py`:

1. Export existing data from old system
2. Convert to new schema format
3. Import into new system
4. Update application imports
5. Test thoroughly

## Requirements

- Python 3.7+
- pandas
- sqlite3 (built-in)

## License

This storage system is part of the PAUSE Pomodoro application.