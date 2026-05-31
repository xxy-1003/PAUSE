"""
Focus Room Page for PAUSE Pomodoro App
UI structure for Focus Room feature (mock data only)
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from focus_room_storage import focus_room_storage

# Page configuration
st.set_page_config(
    page_title="PAUSE - Focus Rooms",
    page_icon="👥",
    layout="wide"
)

# Custom CSS for Focus Room page
st.markdown("""
<style>
    .focus-room-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.08);
        border: 1px solid rgba(138, 43, 226, 0.1);
        margin-bottom: 25px;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4B0082;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(138, 43, 226, 0.1);
    }
    
    .friend-card {
        background: #F9F5FF;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #8A2BE2;
        transition: all 0.3s ease;
    }
    
    .friend-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.15);
    }
    
    .room-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(138, 43, 226, 0.15);
        transition: all 0.3s ease;
    }
    
    .room-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(138, 43, 226, 0.12);
    }
    
    .member-card {
        background: #F8F9FA;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .status-focusing {
        background-color: #10B981;
        animation: pulse 2s infinite;
    }
    
    .status-break {
        background-color: #F59E0B;
    }
    
    .status-online {
        background-color: #3B82F6;
    }
    
    .status-paused {
        background-color: #6B7280;
    }
    
    .status-offline {
        background-color: #9CA3AF;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .time-badge {
        background: #E6E6FA;
        color: #4B0082;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Focus Room page"""
    
    st.markdown('<div class="focus-room-container">', unsafe_allow_html=True)
    
    # Page header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <h1 style="color: #4B0082; margin-bottom: 5px;">👥 Focus Rooms</h1>
        <p style="color: #666; margin-bottom: 30px;">
            Study together, stay accountable. Join focus rooms with friends and track each other's progress.
        </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: right; padding-top: 10px;">
            <div style="font-size: 0.9rem; color: #666;">Current User</div>
            <div style="font-weight: 600; color: #4B0082;">xiangyi</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # SECTION 1: FRIENDS
    # ============================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Friends</div>', unsafe_allow_html=True)
    
    col_friends1, col_friends2 = st.columns(2)
    
    with col_friends1:
        # Search and Add Friend
        st.subheader("Add Friend")
        with st.form("add_friend_form"):
            search_username = st.text_input("Search username", placeholder="Enter username to search")
            search_submitted = st.form_submit_button("🔍 Search")
            
            if search_submitted and search_username:
                # Mock search results
                mock_users = [
                    {"username": "studybuddy42", "user_id": 4},
                    {"username": "focusmaster", "user_id": 5},
                    {"username": "productivitypro", "user_id": 6}
                ]
                
                if search_username.lower() in ["studybuddy42", "focusmaster", "productivitypro"]:
                    st.success(f"Found user: {search_username}")
                    if st.button(f"➕ Send Friend Request to {search_username}"):
                        st.info("Friend request sent! (Mock action)")
                else:
                    st.warning(f"No user found with username: {search_username}")
        
        # Pending Requests
        st.subheader("Pending Requests")
        
        # Mock pending requests
        mock_pending_requests = [
            {"request_id": 1, "sender_username": "coder123", "created_at": "2024-01-15"},
            {"request_id": 2, "sender_username": "studyguru", "created_at": "2024-01-14"}
        ]
        
        if mock_pending_requests:
            for req in mock_pending_requests:
                col_req1, col_req2, col_req3 = st.columns([3, 1, 1])
                with col_req1:
                    st.write(f"**{req['sender_username']}**")
                    st.caption(f"Sent: {req['created_at']}")
                with col_req2:
                    if st.button("✅", key=f"accept_{req['request_id']}"):
                        st.success(f"Accepted request from {req['sender_username']} (Mock)")
                with col_req3:
                    if st.button("❌", key=f"reject_{req['request_id']}"):
                        st.info(f"Rejected request from {req['sender_username']} (Mock)")
                st.divider()
        else:
            st.info("No pending friend requests")
    
    with col_friends2:
        # Friend List
        st.subheader("Friend List")
        
        # Mock friends list
        mock_friends = [
            {"username": "amir", "status": "Online", "last_active": "Just now"},
            {"username": "danial", "status": "Focusing", "last_active": "5 min ago"},
            {"username": "alex", "status": "Offline", "last_active": "2 hours ago"},
            {"username": "sarah", "status": "Break", "last_active": "10 min ago"}
        ]
        
        for friend in mock_friends:
            with st.container():
                st.markdown(f"""
                <div class="friend-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{friend['username']}</strong>
                            <div style="display: flex; align-items: center; margin-top: 5px;">
                                <span class="status-indicator status-{friend['status'].lower()}"></span>
                                <span style="font-size: 0.85rem; color: #666;">{friend['status']}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.8rem; color: #999;">{friend['last_active']}</div>
                            <button style="margin-top: 5px; padding: 4px 12px; font-size: 0.8rem;" 
                                    onclick="alert('Invite sent to {friend['username']}!')">
                                Invite to Room
                            </button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End section card
    
    # ============================================
    # SECTION 2: ROOMS
    # ============================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏠 Rooms</div>', unsafe_allow_html=True)
    
    col_rooms1, col_rooms2 = st.columns([2, 1])
    
    with col_rooms1:
        # Room List
        st.subheader("Your Rooms")
        
        # Mock rooms
        mock_rooms = [
            {
                "room_id": 1,
                "room_name": "FYP Warriors",
                "owner": "xiangyi",
                "member_count": 3,
                "is_private": False,
                "voice_enabled": False,
                "chat_enabled": True,
                "joined_at": "2024-01-10"
            },
            {
                "room_id": 2,
                "room_name": "Study Group Alpha",
                "owner": "amir",
                "member_count": 5,
                "is_private": True,
                "voice_enabled": True,
                "chat_enabled": True,
                "joined_at": "2024-01-12"
            },
            {
                "room_id": 3,
                "room_name": "Focus Zone",
                "owner": "danial",
                "member_count": 2,
                "is_private": False,
                "voice_enabled": False,
                "chat_enabled": True,
                "joined_at": "2024-01-14"
            }
        ]
        
        for room in mock_rooms:
            with st.container():
                privacy_icon = "🔒" if room["is_private"] else "🌐"
                voice_icon = "🎤" if room["voice_enabled"] else "🔇"
                chat_icon = "💬" if room["chat_enabled"] else "🚫"
                
                st.markdown(f"""
                <div class="room-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="margin: 0 0 5px 0; color: #4B0082;">{room['room_name']}</h4>
                            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                                <span style="font-size: 0.85rem; color: #666;">👑 {room['owner']}</span>
                                <span style="font-size: 0.85rem; color: #666;">👥 {room['member_count']} members</span>
                                <span style="font-size: 0.85rem; color: #666;">{privacy_icon} {voice_icon} {chat_icon}</span>
                            </div>
                        </div>
                        <div>
                            <button style="padding: 6px 15px; background: #8A2BE2; color: white; border: none; border-radius: 8px; cursor: pointer;"
                                    onclick="alert('Entering {room['room_name']}...')">
                                Enter Room
                            </button>
                        </div>
                    </div>
                    <div style="font-size: 0.8rem; color: #999; margin-top: 10px;">
                        Joined: {room['joined_at']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col_rooms2:
        # Create Room Form
        st.subheader("Create New Room")
        
        with st.form("create_room_form"):
            room_name = st.text_input("Room Name", placeholder="e.g., Study Session")
            is_private = st.checkbox("Private Room", value=False)
            voice_enabled = st.checkbox("Enable Voice Chat", value=False)
            chat_enabled = st.checkbox("Enable Text Chat", value=True)
            
            create_submitted = st.form_submit_button("Create Room", type="primary")
            
            if create_submitted:
                if room_name:
                    st.success(f"Room '{room_name}' created successfully! (Mock)")
                    st.info(f"Settings: Private={is_private}, Voice={voice_enabled}, Chat={chat_enabled}")
                else:
                    st.warning("Please enter a room name")
        
        # Available Rooms (Public)
        st.subheader("Public Rooms")
        
        mock_public_rooms = [
            {"name": "Global Study Hub", "members": 12, "topic": "General Study"},
            {"name": "CS Students", "members": 8, "topic": "Computer Science"},
            {"name": "Late Night Crew", "members": 5, "topic": "Night Owls"}
        ]
        
        for room in mock_public_rooms:
            col_room1, col_room2 = st.columns([3, 1])
            with col_room1:
                st.write(f"**{room['name']}**")
                st.caption(f"{room['topic']} • {room['members']} members")
            with col_room2:
                if st.button("Join", key=f"join_{room['name']}"):
                    st.info(f"Joined {room['name']} (Mock)")
    
    st.markdown('</div>', unsafe_allow_html=True)  # End section card
    
    # ============================================
    # SECTION 3: ACTIVE ROOM (MOCK)
    # ============================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Active Room: FYP Warriors</div>', unsafe_allow_html=True)
    
    # Room info header
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Total Members", "3")
    with col_info2:
        st.metric("Currently Focusing", "1")
    with col_info3:
        st.metric("Room Uptime", "2h 15m")
    
    st.divider()
    
    # Room Members with Presence
    st.subheader("Room Members")
    
    # Mock room members with presence data
    mock_members = [
        {
            "username": "xiangyi",
            "status": "focusing",
            "remaining_time": 1200,  # 20 minutes in seconds
            "focus_session": "Chapter 3 Review",
            "joined_at": "10:30 AM"
        },
        {
            "username": "amir",
            "status": "break",
            "remaining_time": 300,  # 5 minutes in seconds
            "focus_session": "Algorithm Design",
            "joined_at": "10:45 AM"
        },
        {
            "username": "danial",
            "status": "online",
            "remaining_time": None,
            "focus_session": "Not in session",
            "joined_at": "11:00 AM"
        }
    ]
    
    # Display members in columns
    cols = st.columns(3)
    for idx, member in enumerate(mock_members):
        with cols[idx % 3]:
            # Status color mapping
            status_colors = {
                "focusing": "#10B981",
                "break": "#F59E0B",
                "online": "#3B82F6",
                "paused": "#6B7280",
                "offline": "#9CA3AF"
            }
            
            status_color = status_colors.get(member["status"], "#9CA3AF")
            
            # Format remaining time
            if member["remaining_time"]:
                minutes = member["remaining_time"] // 60
                seconds = member["remaining_time"] % 60
                time_display = f"{minutes}:{seconds:02d}"
            else:
                time_display = "N/A"
            
            st.markdown(f"""
            <div class="member-card">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color}; margin-right: 8px;"></div>
                        <strong style="color: #4B0082;">{member['username']}</strong>
                    </div>
                    <div style="font-size: 0.85rem; color: #666; margin-bottom: 5px;">
                        {member['focus_session']}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.8rem; color: #999;">Joined: {member['joined_at']}</span>
                        <span class="time-badge">{time_display}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Room Controls
    st.divider()
    st.subheader("Room Controls")
    
    col_controls1, col_controls2, col_controls3 = st.columns(3)
    
    with col_controls1:
        if st.button("🎯 Start Focus Session", use_container_width=True):
            st.info("Starting 25-minute focus session... (Mock)")
    
    with col_controls2:
        if st.button("☕ Take Break", use_container_width=True):
            st.info("Starting 5-minute break... (Mock)")
    
    with col_controls3:
        if st.button("🚪 Leave Room", use_container_width=True, type="secondary"):
            st.warning("Left the room. (Mock)")
    
    # Chat Preview (Mock)
    st.divider()
    st.subheader("Chat Preview")
    
    mock_messages = [
        {"user": "xiangyi", "message": "Starting my focus session now!", "time": "10:30 AM"},
        {"user": "amir", "message": "Good luck! I'll join in 5 min", "time": "10:31 AM"},
        {"user": "danial", "message": "Just finished Chapter 2, moving to 3", "time": "10:45 AM"},
    ]
    
    for msg in mock_messages:
        st.markdown(f"""
        <div style="margin-bottom: 10px; padding: 10px; background: #F8F9FA; border-radius: 10px;">
            <div style="display: flex; justify-content: space-between;">
                <strong style="color: #4B0082;">{msg['user']}</strong>
                <span style="font-size: 0.8rem; color: #999;">{msg['time']}</span>
            </div>
            <div style="margin-top: 5px;">{msg['message']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input (mock)
    chat_input = st.text_input("Type a message...", key="chat_input")
    if st.button("Send", key="send_chat"):
        if chat_input:
            st.info(f"Message sent: '{chat_input}' (Mock)")
    
    st.markdown('</div>', unsafe_allow_html=True)  # End section card
    
    # ============================================
    # FOOTER & INFO
    # ============================================
    st.markdown("""
    <div style="margin-top: 40px; padding: 20px; background: #F9F5FF; border-radius: 12px; text-align: center;">
        <h4 style="color: #4B0082; margin-bottom: 10px;">🚀 Future Features Preview</h4>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 15px;">
            <div style="padding: 10px 15px; background: white; border-radius: 8px; border: 1px solid rgba(138, 43, 226, 0.1);">
                🔐 Authentication System
            </div>
            <div style="padding: 10px 15px; background: white; border-radius: 8px; border: 1px solid rgba(138, 43, 226, 0.1);">
                🔄 Real-time Updates
            </div>
            <div style="padding: 10px 15px; background: white; border-radius: 8px; border: 1px solid rgba(138, 43, 226, 0.1);">
                😊 Emoji Reactions
            </div>
            <div style="padding: 10px 15px; background: white; border-radius: 8px; border: 1px solid rgba(138, 43, 226, 0.1);">
                🎤 Voice Channels
            </div>
            <div style="padding: 10px 15px; background: white; border-radius: 8px; border: 1px solid rgba(138, 43, 226, 0.1);">
                🔔 Notifications
            </div>
        </div>
        <p style="margin-top: 20px; color: #666; font-size: 0.9rem;">
            This is a foundation architecture. Future features can be plugged in seamlessly.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End container

if __name__ == "__main__":
    main()