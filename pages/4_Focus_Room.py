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
    
    /* Streamlit button overrides for purple theme */
    .stButton > button {
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8A2BE2, #4B0082) !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4B0082, #8A2BE2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #8A2BE2 !important;
        border: 2px solid #8A2BE2 !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #8A2BE2 !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid rgba(138, 43, 226, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8A2BE2 !important;
        box-shadow: 0 0 0 2px rgba(138, 43, 226, 0.1) !important;
    }
    
    .stCheckbox > div {
        color: #4B0082 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.05), rgba(75, 0, 130, 0.05)) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(138, 43, 226, 0.1) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #4B0082 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Divider styling */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(138, 43, 226, 0.2), transparent) !important;
        margin: 20px 0 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #F9F5FF !important;
        border-radius: 8px !important;
        border: 1px solid rgba(138, 43, 226, 0.1) !important;
        color: #4B0082 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F5F0FF !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .room-card-container {
            padding: 15px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
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
                # Friend card container
                st.markdown("""
                <style>
                    .streamlit-friend-card {
                        background: #F9F5FF;
                        border-radius: 12px;
                        padding: 15px;
                        margin-bottom: 10px;
                        border-left: 4px solid #8A2BE2;
                        transition: all 0.3s ease;
                    }
                    .streamlit-friend-card:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.15);
                    }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="streamlit-friend-card">', unsafe_allow_html=True)
                
                col_friend1, col_friend2 = st.columns([2, 1])
                
                with col_friend1:
                    # Friend name and status
                    st.markdown(f"<strong style='color: #4B0082;'>{friend['username']}</strong>", unsafe_allow_html=True)
                    
                    # Status indicator
                    status_color = {
                        'online': '#3B82F6',
                        'focusing': '#10B981', 
                        'break': '#F59E0B',
                        'offline': '#9CA3AF'
                    }.get(friend['status'].lower(), '#9CA3AF')
                    
                    st.markdown(f"""
                    <div style='display: flex; align-items: center; margin-top: 5px;'>
                        <div style='width: 10px; height: 10px; border-radius: 50%; background: {status_color}; margin-right: 8px;'></div>
                        <span style='font-size: 0.85rem; color: #666;'>{friend['status']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_friend2:
                    # Last active and invite button
                    st.markdown(f"<div style='font-size: 0.8rem; color: #999; text-align: right;'>{friend['last_active']}</div>", unsafe_allow_html=True)
                    
                    # Invite button using Streamlit
                    if st.button(
                        "Invite",
                        key=f"invite_{friend['username']}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        st.success(f"Invitation sent to {friend['username']}!")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
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
        
        rooms = focus_room_storage.get_user_rooms(1)
        
        if not rooms:
            st.info("You haven't joined any rooms yet. Create or join a room to get started!")
        else:
            for room in rooms:
                # Create a container for each room card
                with st.container():
                    # Apply custom styling to the container
                    st.markdown("""
                    <style>
                        .room-card-container {
                            background: white;
                            border-radius: 12px;
                            padding: 20px;
                            margin-bottom: 15px;
                            border: 1px solid rgba(138, 43, 226, 0.15);
                            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.08);
                            transition: all 0.3s ease;
                        }
                        .room-card-container:hover {
                            box-shadow: 0 10px 25px rgba(138, 43, 226, 0.12);
                            transform: translateY(-2px);
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Room card container
                    st.markdown('<div class="room-card-container">', unsafe_allow_html=True)
                    
                    # Room header with name and icons
                    col_header1, col_header2 = st.columns([3, 1])
                    
                    with col_header1:
                        # Room name with purple color
                        st.markdown(f"<h4 style='color: #4B0082; margin: 0 0 10px 0;'>{room['room_name']}</h4>", unsafe_allow_html=True)
                        
                        # Room details row
                        privacy_icon = "🔒" if room["is_private"] else "🌐"
                        voice_icon = "🎤" if room["voice_enabled"] else "🔇"
                        chat_icon = "💬" if room["chat_enabled"] else "🚫"
                        
                        col_details1, col_details2, col_details3 = st.columns(3)
                        with col_details1:
                            st.markdown(f"<div style='font-size: 0.85rem; color: #666;'>👑 {room['owner_name']}</div>", unsafe_allow_html=True)
                        with col_details2:
                            st.markdown(f"<div style='font-size: 0.85rem; color: #666;'>👥 {room['member_count']} members</div>", unsafe_allow_html=True)
                        with col_details3:
                            st.markdown(f"<div style='font-size: 0.85rem; color: #666;'>{privacy_icon} {voice_icon} {chat_icon}</div>", unsafe_allow_html=True)
                    
                    with col_header2:
                        # Room status indicator
                        room_info = focus_room_storage.get_room_info(room['room_id'])
                        if room_info:
                            is_private = "Private" if room_info['is_private'] else "Public"
                            st.markdown(f"<div style='text-align: right; font-size: 0.8rem; color: #8A2BE2; font-weight: 600;'>{is_private}</div>", unsafe_allow_html=True)
                    
                    # Room information display
                    st.markdown("---")
                    
                    # Room details in columns
                    col_info1, col_info2, col_info3 = st.columns(3)
                    
                    with col_info1:
                        st.markdown(f"""
                        <div style='text-align: center;'>
                            <div style='font-size: 0.75rem; color: #666;'>Room ID</div>
                            <div style='font-size: 1rem; color: #4B0082; font-weight: 600;'>{room['room_id']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_info2:
                        st.markdown(f"""
                        <div style='text-align: center;'>
                            <div style='font-size: 0.75rem; color: #666;'>Created</div>
                            <div style='font-size: 0.9rem; color: #4B0082;'>{room['created_at'][:10] if room['created_at'] else 'N/A'}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_info3:
                        st.markdown(f"""
                        <div style='text-align: center;'>
                            <div style='font-size: 0.75rem; color: #666;'>You Joined</div>
                            <div style='font-size: 0.9rem; color: #4B0082;'>{room['joined_at'][:10] if room['joined_at'] else 'N/A'}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Action buttons
                    st.markdown("---")
                    col_actions1, col_actions2, col_actions3 = st.columns([2, 2, 1])
                    
                    with col_actions1:
                        # Enter Room button with purple styling
                        if st.button(
                            "🚪 Enter Room",
                            key=f"enter_{room['room_id']}",
                            use_container_width=True,
                            type="primary"
                        ):
                            # User is already a member, just set active room
                            st.session_state['active_room'] = room['room_id']
                            st.session_state['active_room_name'] = room['room_name']
                            st.session_state['active_room_owner'] = room['owner_name']
                            
                            st.success(f"Entering {room['room_name']}...")
                            # In a real app, this would navigate to room view
                    
                    with col_actions2:
                        # View Members button
                        if st.button(
                            "👥 View Members",
                            key=f"members_{room['room_id']}",
                            use_container_width=True
                        ):
                            members = focus_room_storage.get_room_members(room['room_id'])
                            with st.expander(f"Room Members ({len(members)})"):
                                for member in members:
                                    status_color = {
                                        'focusing': '#10B981',
                                        'break': '#F59E0B',
                                        'online': '#3B82F6',
                                        'paused': '#6B7280',
                                        'offline': '#9CA3AF'
                                    }.get(member['status'], '#9CA3AF')
                                    
                                    st.markdown(f"""
                                    <div style='display: flex; align-items: center; margin: 5px 0; padding: 8px; background: #F8F9FA; border-radius: 8px;'>
                                        <div style='width: 10px; height: 10px; border-radius: 50%; background: {status_color}; margin-right: 10px;'></div>
                                        <div style='flex: 1;'>
                                            <strong>{member['username']}</strong>
                                            <div style='font-size: 0.8rem; color: #666;'>{member['status'].title()}</div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                    
                    with col_actions3:
                        # Delete Room button (only show if user is owner)
                        if room['owner_id'] == 1:  # Current user ID (xiangyi)
                            if st.button(
                                "🗑️",
                                key=f"delete_{room['room_id']}",
                                use_container_width=True,
                                help="Delete this room (owner only)"
                            ):
                                current_user_id = 1  # xiangyi's user_id
                                success = focus_room_storage.delete_room(
                                    room['room_id'],
                                    user_id=current_user_id
                                )
                                
                                if success:
                                    st.success("Room deleted successfully!")
                                    time.sleep(0.5)  # Brief delay to show message
                                    st.rerun()
                                else:
                                    st.error("Failed to delete room. You may not be the owner.")
                        else:
                            # Leave Room button for non-owners
                            if st.button(
                                "🚪 Leave",
                                key=f"leave_{room['room_id']}",
                                use_container_width=True,
                                type="secondary"
                            ):
                                current_user_id = 1  # xiangyi's user_id
                                success = focus_room_storage.leave_room(
                                    room['room_id'],
                                    user_id=current_user_id
                                )
                                
                                if success:
                                    st.success("Left the room successfully!")
                                    st.info(f"Debug: leave_room({room['room_id']}, {current_user_id}) = {success}")
                                    time.sleep(0.5)  # Brief delay to show message
                                    st.rerun()
                                else:
                                    st.error("Failed to leave room.")
                                    st.info(f"Debug: leave_room({room['room_id']}, {current_user_id}) = {success}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # End room card container
    
    with col_rooms2:
        # Create Room Form
        st.subheader("Create New Room")
        
        with st.form("create_room_form", clear_on_submit=True):
            room_name = st.text_input("Room Name", placeholder="e.g., Study Session", help="Choose a descriptive name for your room")
            is_private = st.checkbox("Private Room", value=False, help="Only invited friends can join private rooms")
            voice_enabled = st.checkbox("Enable Voice Chat", value=False, help="Allow voice communication in the room")
            chat_enabled = st.checkbox("Enable Text Chat", value=True, help="Enable text chat for room members")
            
            create_submitted = st.form_submit_button("Create Room", type="primary", use_container_width=True)
            
            if create_submitted:
                if not room_name:
                    st.error("Please enter a room name")
                else:
                    current_user_id = 1  # xiangyi's user_id
                    room_id = focus_room_storage.create_room(
                        room_name=room_name,
                        owner_id=current_user_id,
                        is_private=is_private,
                        voice_enabled=voice_enabled,
                        chat_enabled=chat_enabled
                    )

                    if room_id:
                        st.success(f"Room '{room_name}' created successfully!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Failed to create room. Please try again.")
        
        # Public Rooms Section
        st.subheader("Public Rooms")
        st.caption("Join public rooms to study with others")
        
        public_rooms = focus_room_storage.get_public_rooms()
        
        for room in public_rooms:
            with st.container():
                # Public room card container
                st.markdown("""
                <style>
                    .public-room-card {
                        background: linear-gradient(135deg, rgba(138, 43, 226, 0.03), rgba(75, 0, 130, 0.03));
                        border-radius: 12px;
                        padding: 15px;
                        margin-bottom: 10px;
                        border: 1px solid rgba(138, 43, 226, 0.1);
                        transition: all 0.3s ease;
                    }
                    .public-room-card:hover {
                        background: linear-gradient(135deg, rgba(138, 43, 226, 0.05), rgba(75, 0, 130, 0.05));
                        transform: translateY(-2px);
                        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.1);
                    }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="public-room-card">', unsafe_allow_html=True)
                
                col_public1, col_public2 = st.columns([3, 1])
                
                with col_public1:
                    # Room name and owner
                    st.markdown(f"<h5 style='color: #4B0082; margin: 0 0 5px 0;'>{room['room_name']}</h5>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='font-size: 0.85rem; color: #666; margin-bottom: 5px;'>"
                        f"Created by {room.get('owner_name', 'Unknown')}"
                        f"</div>",
                        unsafe_allow_html=True
                    )    
                                    
                    # Room stats
                    col_stats1, col_stats2 = st.columns(2)
                    with col_stats1:
                        st.markdown(f"""
                        <div style='display: flex; align-items: center; gap: 5px;'>
                            <span style='color: #8A2BE2;'>👥</span>
                            <span style='font-size: 0.8rem; color: #666;'>{room.get('member_count', 0)} members</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stats2:
                        # Room features
                        privacy_icon = "🔒" if room.get("is_private", False) else "🌐"
                        voice_icon = "🎤" if room.get("voice_enabled", False) else "🔇"
                        chat_icon = "💬" if room.get("chat_enabled", True) else "🚫"
                        st.markdown(f"""
                        <div style='display: flex; align-items: center; gap: 5px;'>
                            <span style='color: #8A2BE2;'>{privacy_icon} {voice_icon} {chat_icon}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_public2:
                    # Join button with purple styling
                    if st.button(
                        "Join Room",
                        key=f"join_public_{room.get('room_id', 0)}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        # REAL join logic - use actual room_id and user_id
                        current_user_id = 1  # xiangyi's user_id
                        room_id = room.get('room_id')
                        
                        if room_id:
                            success = focus_room_storage.join_room(
                                room_id=room_id, 
                                user_id=current_user_id
                            )
                            
                            if success:
                                st.success(f"Joined {room.get('room_name', 'the room')} successfully!")
                                time.sleep(0.5)  # Brief delay to show message
                                st.rerun()
                            else:
                                st.error(f"Failed to join room. You may already be a member.")
                        else:
                            st.error("Invalid room ID")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
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