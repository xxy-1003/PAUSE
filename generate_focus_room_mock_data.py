"""
Focus Room Mock Data Generator
Generates sample data for testing the Focus Room system
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import random

def generate_mock_data(db_path="pause_focus_rooms.db"):
    """Generate comprehensive mock data for Focus Room system"""
    
    print("🔧 Generating Focus Room mock data...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data first
    print("  Clearing existing data...")
    cursor.execute('DELETE FROM room_presence')
    cursor.execute('DELETE FROM room_members')
    cursor.execute('DELETE FROM focus_rooms')
    cursor.execute('DELETE FROM friends')
    cursor.execute('DELETE FROM friend_requests')
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM sqlite_sequence')
    
    # Helper function to hash passwords
    def hash_password(password):
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt
    
    # ============================================
    # CREATE SAMPLE USERS
    # ============================================
    print("  Creating sample users...")
    
    sample_users = [
        {"username": "xiangyi", "email": "xiangyi@example.com", "password": "password123"},
        {"username": "amir", "email": "amir@example.com", "password": "password123"},
        {"username": "danial", "email": "danial@example.com", "password": "password123"},
        {"username": "sarah", "email": "sarah@example.com", "password": "password123"},
        {"username": "alex", "email": "alex@example.com", "password": "password123"},
        {"username": "maya", "email": "maya@example.com", "password": "password123"},
        {"username": "james", "email": "james@example.com", "password": "password123"},
        {"username": "lisa", "email": "lisa@example.com", "password": "password123"},
        {"username": "tom", "email": "tom@example.com", "password": "password123"},
        {"username": "emma", "email": "emma@example.com", "password": "password123"}
    ]
    
    for user in sample_users:
        password_hash = hash_password(user["password"])
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (user["username"], user["email"], password_hash)
        )
    
    # ============================================
    # CREATE FRIEND RELATIONSHIPS
    # ============================================
    print("  Creating friend relationships...")
    
    # Create friendships (bidirectional)
    friendships = [
        (1, 2), (1, 3), (1, 4),  # xiangyi friends with amir, danial, sarah
        (2, 3), (2, 5), (2, 6),  # amir friends with danial, alex, maya
        (3, 4), (3, 7),          # danial friends with sarah, james
        (4, 5), (4, 8),          # sarah friends with alex, lisa
        (5, 6), (5, 9),          # alex friends with maya, tom
        (6, 7), (6, 10),         # maya friends with james, emma
        (7, 8),                  # james friends with lisa
        (8, 9),                  # lisa friends with tom
        (9, 10),                 # tom friends with emma
        (10, 1)                  # emma friends with xiangyi
    ]
    
    for user_id, friend_id in friendships:
        # Insert both directions for friendship
        cursor.execute(
            "INSERT OR IGNORE INTO friends (user_id, friend_user_id) VALUES (?, ?)",
            (user_id, friend_id)
        )
        cursor.execute(
            "INSERT OR IGNORE INTO friends (user_id, friend_user_id) VALUES (?, ?)",
            (friend_id, user_id)
        )
    
    # Create some pending friend requests
    pending_requests = [
        (1, 5),  # xiangyi -> alex (pending)
        (2, 8),  # amir -> lisa (pending)
        (3, 9),  # danial -> tom (pending)
        (4, 10), # sarah -> emma (pending)
        (5, 1)   # alex -> xiangyi (pending - duplicate of above for testing)
    ]
    
    for sender_id, receiver_id in pending_requests:
        cursor.execute(
            "INSERT OR IGNORE INTO friend_requests (sender_id, receiver_id, status) VALUES (?, ?, 'pending')",
            (sender_id, receiver_id)
        )
    
    # ============================================
    # CREATE FOCUS ROOMS
    # ============================================
    print("  Creating focus rooms...")
    
    focus_rooms = [
        {
            "room_name": "FYP Warriors",
            "owner_id": 1,
            "is_private": False,
            "voice_enabled": False,
            "chat_enabled": True,
            "description": "Final Year Project collaboration room"
        },
        {
            "room_name": "Study Group Alpha",
            "owner_id": 2,
            "is_private": True,
            "voice_enabled": True,
            "chat_enabled": True,
            "description": "Private study group for advanced topics"
        },
        {
            "room_name": "Focus Zone",
            "owner_id": 3,
            "is_private": False,
            "voice_enabled": False,
            "chat_enabled": True,
            "description": "General focus room for productivity"
        },
        {
            "room_name": "Night Owls",
            "owner_id": 4,
            "is_private": False,
            "voice_enabled": True,
            "chat_enabled": True,
            "description": "For late-night study sessions"
        },
        {
            "room_name": "CS Students Hub",
            "owner_id": 5,
            "is_private": False,
            "voice_enabled": False,
            "chat_enabled": True,
            "description": "Computer Science students community"
        }
    ]
    
    room_memberships = {}
    
    for i, room in enumerate(focus_rooms, 1):
        cursor.execute(
            """
            INSERT INTO focus_rooms (room_name, owner_id, is_private, voice_enabled, chat_enabled)
            VALUES (?, ?, ?, ?, ?)
            """,
            (room["room_name"], room["owner_id"], 
             1 if room["is_private"] else 0, 
             1 if room["voice_enabled"] else 0, 
             1 if room["chat_enabled"] else 0)
        )
        room_id = cursor.lastrowid
        room_memberships[room_id] = []
        
        # Add owner as member
        cursor.execute(
            "INSERT INTO room_members (room_id, user_id) VALUES (?, ?)",
            (room_id, room["owner_id"])
        )
        room_memberships[room_id].append(room["owner_id"])
    
    # ============================================
    # ADD MEMBERS TO ROOMS
    # ============================================
    print("  Adding members to rooms...")
    
    # Room 1: FYP Warriors (room_id = 1)
    room1_members = [1, 2, 3, 4, 5]  # xiangyi, amir, danial, sarah, alex
    for user_id in room1_members:
        if user_id not in room_memberships[1]:
            cursor.execute(
                "INSERT INTO room_members (room_id, user_id) VALUES (?, ?)",
                (1, user_id)
            )
            room_memberships[1].append(user_id)
    
    # Room 2: Study Group Alpha (room_id = 2)
    room2_members = [2, 3, 6, 7]  # amir, danial, maya, james
    for user_id in room2_members:
        if user_id not in room_memberships[2]:
            cursor.execute(
                "INSERT INTO room_members (room_id, user_id) VALUES (?, ?)",
                (2, user_id)
            )
            room_memberships[2].append(user_id)
    
    # Room 3: Focus Zone (room_id = 3)
    room3_members = [3, 4, 5, 8, 9]  # danial, sarah, alex, lisa, tom
    for user_id in room3_members:
        if user_id not in room_memberships[3]:
            cursor.execute(
                "INSERT INTO room_members (room_id, user_id) VALUES (?, ?)",
                (3, user_id)
            )
            room_memberships[3].append(user_id)
    
    # Room 4: Night Owls (room_id = 4)
    room4_members = [4, 5, 6, 10]  # sarah, alex, maya, emma
    for user_id in room4_members:
        if user_id not in room_memberships[4]:
            cursor.execute(
                "INSERT INTO room_members (room_id, user_id) VALUES (?, ?)",
                (4, user_id)
            )
            room_memberships[4].append(user_id)
    
    # Room 5: CS Students Hub (room_id = 5)
    room5_members = [5, 6, 7, 8, 9, 10]  # alex, maya, james, lisa, tom, emma
    for user_id in room5_members:
        if user_id not in room_memberships[5]:
            cursor.execute(
                "INSERT INTO room_members (room_id, user_id) VALUES (?, ?)",
                (5, user_id)
            )
            room_memberships[5].append(user_id)
    
    # ============================================
    # ADD PRESENCE DATA
    # ============================================
    print("  Adding presence data...")
    
    # Status options with weights
    status_options = [
        ("focusing", 0.4),    # 40% chance
        ("break", 0.2),       # 20% chance
        ("online", 0.2),      # 20% chance
        ("paused", 0.1),      # 10% chance
        ("offline", 0.1)      # 10% chance
    ]
    
    # For each room, add presence data for members
    for room_id, members in room_memberships.items():
        for user_id in members:
            # Randomly select status based on weights
            rand_val = random.random()
            cumulative = 0
            selected_status = "online"  # default
            
            for status, weight in status_options:
                cumulative += weight
                if rand_val <= cumulative:
                    selected_status = status
                    break
            
            # Generate remaining time based on status
            remaining_time = None
            if selected_status == "focusing":
                remaining_time = random.randint(300, 1800)  # 5-30 minutes
            elif selected_status == "break":
                remaining_time = random.randint(60, 600)    # 1-10 minutes
            
            # Random timestamp within last 24 hours
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            updated_at = datetime.now() - timedelta(hours=hours_ago, minutes=minutes_ago)
            
            cursor.execute(
                """
                INSERT INTO room_presence (room_id, user_id, status, remaining_time, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (room_id, user_id, selected_status, remaining_time, updated_at)
            )
    
    # ============================================
    # COMMIT AND DISPLAY SUMMARY
    # ============================================
    conn.commit()
    
    # Get counts for summary
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM friends")
    friend_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM focus_rooms")
    room_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM room_members")
    member_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM room_presence")
    presence_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n✅ Mock data generation complete!")
    print("=" * 40)
    print(f"📊 Summary:")
    print(f"  👤 Users: {user_count}")
    print(f"  🤝 Friendships: {friend_count}")
    print(f"  🏠 Focus Rooms: {room_count}")
    print(f"  👥 Room Memberships: {member_count}")
    print(f"  🎯 Presence Records: {presence_count}")
    print("=" * 40)
    print("\n📝 Sample Users (username - password):")
    print("  xiangyi - password123")
    print("  amir - password123")
    print("  danial - password123")
    print("  sarah - password123")
    print("  alex - password123")
    print("\n🚀 To test the Focus Room system:")
    print("  1. Run: streamlit run app.py")
    print("  2. Navigate to Focus Rooms page")
    print("  3. Use sample credentials to explore")
    
    return True

def test_storage_module():
    """Test the storage module with generated data"""
    print("\n🧪 Testing storage module...")
    
    from focus_room_storage import FocusRoomStorage
    
    storage = FocusRoomStorage("pause_focus_rooms.db")
    
    # Test 1: Get user
    user = storage.get_user(username="xiangyi")
    if user:
        print(f"  ✅ Found user: {user['username']} (ID: {user['user_id']})")
    else:
        print("  ❌ User not found")
    
    # Test 2: Get friends
    friends = storage.get_friends(user_id=1)
    print(f"  ✅ {user['username']} has {len(friends)} friends")
    
    # Test 3: Get user rooms
    rooms = storage.get_user_rooms(user_id=1)
    print(f"  ✅ {user['username']} is in {len(rooms)} rooms")
    
    # Test 4: Get room members
    if rooms:
        members = storage.get_room_members(rooms[0]['room_id'])
        print(f"  ✅ Room '{rooms[0]['room_name']}' has {len(members)} members")
    
    # Test 5: Search users
    search_results = storage.search_users(query="a", exclude_user_id=1)
    print(f"  ✅ Found {len(search_results)} users matching 'a'")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    # Generate mock data
    generate_mock_data()
    
    # Test the storage module
    test_storage_module()