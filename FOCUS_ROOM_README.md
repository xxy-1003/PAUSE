# Focus Room System - Architecture Documentation

## Overview
The Focus Room System is a foundation architecture for a future social productivity feature in the PAUSE Pomodoro App. It provides the database schema, storage layer, and UI structure for collaborative focus sessions without implementing real-time features yet.

## Architecture Components

### 1. Database Schema (`focus_room_schema.sql`)
**Tables:**
- `users`: User accounts with authentication
- `friend_requests`: Friend request management
- `friends`: Bidirectional friendship relationships
- `focus_rooms`: Room configuration and settings
- `room_members`: Room membership tracking
- `room_presence`: Real-time user status in rooms

**Key Features:**
- Proper foreign key constraints with CASCADE delete
- Unique constraints to prevent duplicates
- Indexes for performance optimization
- Sample data for immediate testing

### 2. Storage Module (`focus_room_storage.py`)
**Core Functions:**

**User Management:**
- `create_user()` - Register new users
- `get_user()` - Retrieve user by ID or username
- `authenticate_user()` - Password verification

**Friend System:**
- `send_friend_request()` - Send friend requests
- `accept_friend_request()` - Accept pending requests
- `reject_friend_request()` - Reject pending requests
- `get_friends()` - List user's friends
- `get_pending_requests()` - Show pending friend requests

**Room Management:**
- `create_room()` - Create new focus rooms
- `delete_room()` - Delete rooms (owner only)
- `join_room()` - Join existing rooms
- `leave_room()` - Leave rooms
- `update_presence()` - Update user status in rooms
- `get_room_members()` - List room members with presence
- `get_room_info()` - Get room details
- `get_user_rooms()` - List user's rooms

**Search & Discovery:**
- `search_users()` - Search for users by username

### 3. UI Structure (`pages/4_Focus_Room.py`)
**Three Main Sections:**

1. **Friends Section**
   - Search and add friends
   - Manage pending friend requests
   - View friend list with status

2. **Rooms Section**
   - Create new rooms with settings
   - View joined rooms
   - Browse public rooms
   - Room settings (private/public, voice/chat enabled)

3. **Active Room Section**
   - Room member presence display
   - Status indicators (focusing, break, online, etc.)
   - Remaining time display
   - Mock chat interface
   - Room controls

### 4. Mock Data Generator (`generate_focus_room_mock_data.py`)
**Generates:**
- 10 sample users with credentials
- Complex friend network
- 5 focus rooms with different settings
- Room memberships
- Realistic presence data

## Database Design Details

### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Friend System
- **Bidirectional friendships**: Automatically creates entries in both directions
- **Prevent duplicates**: Unique constraints on (user_id, friend_user_id)
- **Request tracking**: Status-based friend request system

### Room System
- **Room ownership**: Each room has an owner who can delete it
- **Privacy settings**: Public vs private rooms
- **Feature flags**: Voice and chat enabled/disabled per room
- **Presence tracking**: Real-time status updates

### Presence System
**Status Options:**
- `focusing`: User is in a focus session
- `break`: User is on a break
- `online`: User is online but not in session
- `paused`: Session is paused
- `offline`: User is not active

**Remaining Time:** Tracks seconds remaining in current session/break

## Future-Ready Architecture

### Plug-in Points for Future Features:

1. **Authentication System**
   - Current: Simple password hashing
   - Future: OAuth, JWT tokens, session management

2. **Real-time Updates**
   - Current: Mock data and static UI
   - Future: WebSocket connections, live presence updates

3. **Communication Features**
   - Current: Mock chat interface
   - Future: Real-time messaging, voice channels, video calls

4. **Notifications**
   - Current: None
   - Future: Friend requests, room invites, session reminders

5. **Advanced Features**
   - Current: Basic room management
   - Future: Room scheduling, shared timers, collaborative goals

### Extension Points in Code:

1. **Storage Module**: Add methods for new features
2. **Database Schema**: Add tables without breaking existing structure
3. **UI Components**: Replace mock data with real API calls
4. **Authentication**: Integrate with existing user system

## Setup and Testing

### 1. Initial Setup
```bash
# The storage module auto-creates the database on first import
python -c "from focus_room_storage import focus_room_storage; print('Database ready')"
```

### 2. Generate Mock Data
```bash
python generate_focus_room_mock_data.py
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Test Credentials
```
Username: xiangyi, amir, danial, sarah, alex
Password: password123 (for all test users)
```

## Testing the Storage Module

```python
from focus_room_storage import focus_room_storage

# Test user authentication
user = focus_room_storage.authenticate_user("xiangyi", "password123")
print(f"Authenticated: {user['username']}")

# Test friend system
friends = focus_room_storage.get_friends(user['user_id'])
print(f"Friends: {len(friends)}")

# Test room system
rooms = focus_room_storage.get_user_rooms(user['user_id'])
print(f"Rooms: {len(rooms)}")

# Test presence system
if rooms:
    members = focus_room_storage.get_room_members(rooms[0]['room_id'])
    print(f"Room members: {len(members)}")
```

## Design Principles

### 1. Separation of Concerns
- Database layer isolated in storage module
- UI layer uses mock data (can be replaced with real data)
- Business logic separated from presentation

### 2. Extensibility
- Modular design allows feature-by-feature implementation
- Database schema supports future additions
- UI structured for easy enhancement

### 3. Security Foundation
- Password hashing (ready for stronger algorithms)
- Input validation in storage methods
- Ownership checks for sensitive operations

### 4. Performance Considerations
- Indexes on frequently queried columns
- Efficient JOIN queries for common operations
- Scalable table structure

## Next Steps for Implementation

### Phase 1: Authentication Integration
1. Integrate with existing user system
2. Add login/logout functionality
3. Implement session management

### Phase 2: Real-time Features
1. Add WebSocket support
2. Implement live presence updates
3. Add real-time chat

### Phase 3: Advanced Features
1. Voice/video integration
2. Room scheduling
3. Collaborative timers
4. Notifications system

## File Structure
```
PAUSE/
├── focus_room_schema.sql          # Database schema
├── focus_room_storage.py          # Storage module
├── pages/4_Focus_Room.py          # UI page
├── generate_focus_room_mock_data.py # Data generator
├── pause_focus_rooms.db           # Database file (auto-created)
└── FOCUS_ROOM_README.md           # This documentation
```

## Notes
- **No external dependencies** beyond Streamlit and SQLite
- **Backward compatible** with existing PAUSE app
- **Production-ready** database design
- **Mock UI** for demonstration and testing
- **Sample data** for immediate usability testing

The architecture is designed to be incrementally enhanced while maintaining stability of the core PAUSE application.