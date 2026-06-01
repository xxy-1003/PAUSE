"""
Focus Room Storage Module for PAUSE Pomodoro App
Handles database operations for Focus Room feature
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import json

class FocusRoomStorage:
    """SQLite database storage for Focus Room system"""
    
    def __init__(self, db_path: str = "pause_focus_rooms.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create friend_requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS friend_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(sender_id, receiver_id)
            )
        ''')
        
        # Create friends table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS friends (
                friend_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                friend_user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (friend_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(user_id, friend_user_id)
            )
        ''')
        
        # Create focus_rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS focus_rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_name TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                is_private BOOLEAN NOT NULL DEFAULT 0,
                voice_enabled BOOLEAN NOT NULL DEFAULT 0,
                chat_enabled BOOLEAN NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        ''')
        
        # Create room_members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES focus_rooms(room_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(room_id, user_id)
            )
        ''')
        
        # Create room_presence table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_presence (
                presence_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'online',
                remaining_time INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES focus_rooms(room_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(room_id, user_id)
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_friend_requests_sender ON friend_requests(sender_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_friend_requests_receiver ON friend_requests(receiver_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_friend_requests_status ON friend_requests(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_friends_user ON friends(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_friends_friend ON friends(friend_user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_focus_rooms_owner ON focus_rooms(owner_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_focus_rooms_private ON focus_rooms(is_private)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_members_room ON room_members(room_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_members_user ON room_members(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_presence_room ON room_presence(room_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_presence_user ON room_presence(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_presence_status ON room_presence(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
        
        conn.commit()
        conn.close()
        
        # Create sample data if tables are empty
        self._create_sample_data()
    
    def _hash_password(self, password: str) -> str:
        """Hash password for storage (simple implementation for now)"""
        # In production, use proper password hashing like bcrypt
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt
    
    def _verify_password(self, stored_hash: str, password: str) -> bool:
        """Verify password against stored hash"""
        try:
            hash_value, salt = stored_hash.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hash_value
        except:
            return False
    
    # ============================================
    # USER MANAGEMENT FUNCTIONS
    # ============================================
    
    def create_user(self, username: str, password: str, email: str = None) -> Optional[int]:
        """
        Create a new user
        
        Args:
            username: Unique username
            password: Plain text password
            email: Optional email
            
        Returns:
            user_id if successful, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return user_id
        except sqlite3.IntegrityError:
            # Username already exists
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: int = None, username: str = None) -> Optional[Dict]:
        """
        Get user by ID or username
        
        Args:
            user_id: User ID to look up
            username: Username to look up
            
        Returns:
            User dictionary or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            elif username:
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            else:
                return None
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User dictionary if authenticated, None otherwise
        """
        user = self.get_user(username=username)
        if user and self._verify_password(user['password_hash'], password):
            # Don't return password hash
            user.pop('password_hash', None)
            return user
        return None
    
    # ============================================
    # FRIEND MANAGEMENT FUNCTIONS
    # ============================================
    
    def send_friend_request(self, sender_id: int, receiver_id: int) -> Optional[int]:
        """
        Send a friend request
        
        Args:
            sender_id: ID of user sending request
            receiver_id: ID of user receiving request
            
        Returns:
            request_id if successful, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if request already exists
            cursor.execute('''
                SELECT request_id FROM friend_requests 
                WHERE (sender_id = ? AND receiver_id = ?) 
                   OR (sender_id = ? AND receiver_id = ?)
            ''', (sender_id, receiver_id, receiver_id, sender_id))
            
            if cursor.fetchone():
                conn.close()
                return None  # Request already exists
            
            cursor.execute('''
                INSERT INTO friend_requests (sender_id, receiver_id, status)
                VALUES (?, ?, 'pending')
            ''', (sender_id, receiver_id))
            
            request_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return request_id
        except Exception as e:
            print(f"Error sending friend request: {e}")
            return None
    
    def accept_friend_request(self, request_id: int) -> bool:
        """
        Accept a friend request
        
        Args:
            request_id: ID of friend request to accept
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get request details
            cursor.execute('SELECT sender_id, receiver_id FROM friend_requests WHERE request_id = ?', (request_id,))
            request = cursor.fetchone()
            
            if not request:
                conn.close()
                return False
            
            sender_id, receiver_id = request
            
            # Update request status
            cursor.execute('UPDATE friend_requests SET status = "accepted" WHERE request_id = ?', (request_id,))
            
            # Create friendship in both directions
            cursor.execute('INSERT OR IGNORE INTO friends (user_id, friend_user_id) VALUES (?, ?)', (sender_id, receiver_id))
            cursor.execute('INSERT OR IGNORE INTO friends (user_id, friend_user_id) VALUES (?, ?)', (receiver_id, sender_id))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error accepting friend request: {e}")
            return False
    
    def reject_friend_request(self, request_id: int) -> bool:
        """
        Reject a friend request
        
        Args:
            request_id: ID of friend request to reject
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('UPDATE friend_requests SET status = "rejected" WHERE request_id = ?', (request_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error rejecting friend request: {e}")
            return False
    
    def get_friends(self, user_id: int) -> List[Dict]:
        """
        Get list of friends for a user
        
        Args:
            user_id: ID of user
            
        Returns:
            List of friend dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT u.user_id, u.username, u.email, f.created_at
                FROM friends f
                JOIN users u ON f.friend_user_id = u.user_id
                WHERE f.user_id = ?
                ORDER BY u.username
            ''', (user_id,))
            
            friends = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return friends
        except Exception as e:
            print(f"Error getting friends: {e}")
            return []
    
    def get_pending_requests(self, user_id: int) -> List[Dict]:
        """
        Get pending friend requests for a user
        
        Args:
            user_id: ID of user
            
        Returns:
            List of pending request dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT fr.request_id, fr.sender_id, u.username as sender_username, fr.created_at
                FROM friend_requests fr
                JOIN users u ON fr.sender_id = u.user_id
                WHERE fr.receiver_id = ? AND fr.status = 'pending'
                ORDER BY fr.created_at DESC
            ''', (user_id,))
            
            requests = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return requests
        except Exception as e:
            print(f"Error getting pending requests: {e}")
            return []
    
    # ============================================
    # ROOM MANAGEMENT FUNCTIONS
    # ============================================
    
    def create_room(self, room_name: str, owner_id: int, is_private: bool = False, 
                   voice_enabled: bool = False, chat_enabled: bool = True) -> Optional[int]:
        """
        Create a new focus room
        
        Args:
            room_name: Name of the room
            owner_id: ID of room owner
            is_private: Whether room is private
            voice_enabled: Whether voice chat is enabled
            chat_enabled: Whether text chat is enabled
            
        Returns:
            room_id if successful, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO focus_rooms (room_name, owner_id, is_private, voice_enabled, chat_enabled)
                VALUES (?, ?, ?, ?, ?)
            ''', (room_name, owner_id, 1 if is_private else 0, 1 if voice_enabled else 0, 1 if chat_enabled else 0))
            
            room_id = cursor.lastrowid
            
            # Add owner as first member
            cursor.execute('''
                INSERT INTO room_members (room_id, user_id)
                VALUES (?, ?)
            ''', (room_id, owner_id))
            
            # Set owner presence
            cursor.execute('''
                INSERT OR REPLACE INTO room_presence (room_id, user_id, status)
                VALUES (?, ?, 'online')
            ''', (room_id, owner_id))
            
            conn.commit()
            conn.close()
            
            return room_id
        except Exception as e:
            print(f"Error creating room: {e}")
            return None
        
    def delete_room(self, room_id: int, user_id: int) -> bool:
        """
        Delete a focus room (only owner can delete)
        
        Args:
            room_id: ID of room to delete
            user_id: ID of user attempting deletion
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user is room owner
            cursor.execute('SELECT owner_id FROM focus_rooms WHERE room_id = ?', (room_id,))
            room = cursor.fetchone()
            
            if not room or room[0] != user_id:
                conn.close()
                return False
            
            # Delete room (cascade will delete members and presence)
            cursor.execute('DELETE FROM focus_rooms WHERE room_id = ?', (room_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error deleting room: {e}")
            return False
    
    def join_room(self, room_id: int, user_id: int) -> bool:
        """
        Join a focus room
        
        Args:
            room_id: ID of room to join
            user_id: ID of user joining
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if room exists and is not private (for now, allow all)
            cursor.execute('SELECT room_id FROM focus_rooms WHERE room_id = ?', (room_id,))
            if not cursor.fetchone():
                conn.close()
                return False
            
            # Add user as member
            cursor.execute('''
                INSERT OR IGNORE INTO room_members (room_id, user_id)
                VALUES (?, ?)
            ''', (room_id, user_id))
            
            # Set user presence
            cursor.execute('''
                INSERT OR REPLACE INTO room_presence (room_id, user_id, status)
                VALUES (?, ?, 'online')
            ''', (room_id, user_id))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error joining room: {e}")
            return False
    
    def leave_room(self, room_id: int, user_id: int) -> bool:
        """
        Leave a focus room
        
        Args:
            room_id: ID of room to leave
            user_id: ID of user leaving
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Remove user from members
            cursor.execute('DELETE FROM room_members WHERE room_id = ? AND user_id = ?', (room_id, user_id))
            
            # Remove user presence
            cursor.execute('DELETE FROM room_presence WHERE room_id = ? AND user_id = ?', (room_id, user_id))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error leaving room: {e}")
            return False
    
    def update_presence(self, room_id: int, user_id: int, status: str, remaining_time: int = None) -> bool:
        """
        Update user presence in a room
        
        Args:
            room_id: ID of room
            user_id: ID of user
            status: Presence status ('online', 'focusing', 'break', 'paused', 'offline')
            remaining_time: Remaining time in seconds (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO room_presence (room_id, user_id, status, remaining_time, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (room_id, user_id, status, remaining_time))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error updating presence: {e}")
            return False
    
    def get_room_members(self, room_id: int) -> List[Dict]:
        """
        Get all members of a room with their presence info
        
        Args:
            room_id: ID of room
            
        Returns:
            List of member dictionaries with presence info
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    u.user_id, u.username, u.email,
                    COALESCE(rp.status, 'offline') as status,
                    rp.remaining_time,
                    rp.updated_at as last_seen,
                    rm.joined_at
                FROM room_members rm
                JOIN users u ON rm.user_id = u.user_id
                LEFT JOIN room_presence rp ON rm.room_id = rp.room_id AND rm.user_id = rp.user_id
                WHERE rm.room_id = ?
                ORDER BY 
                    CASE COALESCE(rp.status, 'offline')
                        WHEN 'focusing' THEN 1
                        WHEN 'break' THEN 2
                        WHEN 'paused' THEN 3
                        WHEN 'online' THEN 4
                        ELSE 5
                    END,
                    u.username
            ''', (room_id,))
            
            members = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return members
        except Exception as e:
            print(f"Error getting room members: {e}")
            return []
    
    def get_room_info(self, room_id: int) -> Optional[Dict]:
        """
        Get detailed information about a room
        
        Args:
            room_id: ID of room
            
        Returns:
            Room dictionary with details or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    r.*,
                    u.username as owner_name,
                    COUNT(rm.user_id) as member_count
                FROM focus_rooms r
                JOIN users u ON r.owner_id = u.user_id
                LEFT JOIN room_members rm ON r.room_id = rm.room_id
                WHERE r.room_id = ?
                GROUP BY r.room_id
            ''', (room_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                room_info = dict(row)
                # Convert boolean values from SQLite integers
                room_info['is_private'] = bool(room_info['is_private'])
                room_info['voice_enabled'] = bool(room_info['voice_enabled'])
                room_info['chat_enabled'] = bool(room_info['chat_enabled'])
                return room_info
            return None
        except Exception as e:
            print(f"Error getting room info: {e}")
            return None
    
    def get_user_rooms(self, user_id: int) -> List[Dict]:
        """
        Get all rooms a user is a member of
        
        Args:
            user_id: ID of user
            
        Returns:
            List of room dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    r.*,
                    u.username as owner_name,
                    COUNT(rm2.user_id) as member_count,
                    rm.joined_at
                FROM room_members rm
                JOIN focus_rooms r ON rm.room_id = r.room_id
                JOIN users u ON r.owner_id = u.user_id
                LEFT JOIN room_members rm2 ON r.room_id = rm2.room_id
                WHERE rm.user_id = ?
                GROUP BY r.room_id
                ORDER BY rm.joined_at DESC
            ''', (user_id,))
            
            rooms = [dict(row) for row in cursor.fetchall()]
            
            # Convert boolean values
            for room in rooms:
                room['is_private'] = bool(room['is_private'])
                room['voice_enabled'] = bool(room['voice_enabled'])
                room['chat_enabled'] = bool(room['chat_enabled'])
            
            conn.close()
            
            return rooms
        except Exception as e:
            print(f"Error getting user rooms: {e}")
            return []
    
    def get_public_rooms(self) -> List[Dict]:
        """
        Get all public rooms (is_private = 0)
        
        Returns:
            List of public room dictionaries with member_count
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    r.*,
                    u.username as owner_name,
                    COUNT(rm.user_id) as member_count
                FROM focus_rooms r
                JOIN users u ON r.owner_id = u.user_id
                LEFT JOIN room_members rm ON r.room_id = rm.room_id
                WHERE r.is_private = 0
                GROUP BY r.room_id
                ORDER BY r.created_at DESC
            ''')
            
            rooms = [dict(row) for row in cursor.fetchall()]
            
            # Convert boolean values
            for room in rooms:
                room['is_private'] = bool(room['is_private'])
                room['voice_enabled'] = bool(room['voice_enabled'])
                room['chat_enabled'] = bool(room['chat_enabled'])
            
            conn.close()
            
            return rooms
        except Exception as e:
            print(f"Error getting public rooms: {e}")
            return []
    
    def search_users(self, query: str, exclude_user_id: int = None) -> List[Dict]:
        """
        Search for users by username
        
        Args:
            query: Search query (partial username)
            exclude_user_id: User ID to exclude from results
            
        Returns:
            List of user dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            search_query = f"%{query}%"
            
            if exclude_user_id:
                cursor.execute('''
                    SELECT user_id, username, email, created_at
                    FROM users
                    WHERE username LIKE ? AND user_id != ?
                    ORDER BY username
                    LIMIT 20
                ''', (search_query, exclude_user_id))
            else:
                cursor.execute('''
                    SELECT user_id, username, email, created_at
                    FROM users
                    WHERE username LIKE ?
                    ORDER BY username
                    LIMIT 20
                ''', (search_query,))
            
            users = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return users
        except Exception as e:
            print(f"Error searching users: {e}")
            return []

    def get_public_rooms(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT r.room_id, r.room_name, r.owner_id,
                r.is_private, r.voice_enabled, r.chat_enabled,
                u.username as owner_name
            FROM focus_rooms r
            JOIN users u ON r.owner_id = u.user_id
            WHERE r.is_private = 0
            ORDER BY r.created_at DESC
        """)

        rooms = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rooms
    
    # ============================================
    # SAMPLE DATA GENERATION
    # ============================================
    
    def _create_sample_data(self):
        """Create sample data for testing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if we already have sample users
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                # Create sample users with simple password hash for testing
                sample_password_hash = self._hash_password('password123')
                
                cursor.execute('''
                    INSERT OR IGNORE INTO users (username, email, password_hash) VALUES
                    ('xiangyi', 'xiangyi@example.com', ?),
                    ('amir', 'amir@example.com', ?),
                    ('danial', 'danial@example.com', ?)
                ''', (sample_password_hash, sample_password_hash, sample_password_hash))
                
                # Create sample friend relationships
                cursor.execute('''
                    INSERT OR IGNORE INTO friends (user_id, friend_user_id) VALUES
                    (1, 2),
                    (1, 3),
                    (2, 3)
                ''')
                
                # Create sample focus room
                cursor.execute('''
                    INSERT OR IGNORE INTO focus_rooms (room_name, owner_id, is_private, voice_enabled, chat_enabled) VALUES
                    ('FYP Warriors', 1, 0, 0, 1)
                ''')
                
                # Add members to the room
                cursor.execute('''
                    INSERT OR IGNORE INTO room_members (room_id, user_id) VALUES
                    (1, 1),
                    (1, 2),
                    (1, 3)
                ''')
                
                # Add sample presence data
                cursor.execute('''
                    INSERT OR IGNORE INTO room_presence (room_id, user_id, status, remaining_time) VALUES
                    (1, 1, 'focusing', 1200),
                    (1, 2, 'break', 300),
                    (1, 3, 'online', NULL)
                ''')
                
                conn.commit()
                print("✅ Sample data created successfully")
            
            conn.close()
            
        except Exception as e:
            print(f"Error creating sample data: {e}")
    
    def clear_all_data(self):
        """Clear all data from focus room tables (for testing)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clear tables in reverse order of dependencies
            cursor.execute('DELETE FROM room_presence')
            cursor.execute('DELETE FROM room_members')
            cursor.execute('DELETE FROM focus_rooms')
            cursor.execute('DELETE FROM friends')
            cursor.execute('DELETE FROM friend_requests')
            cursor.execute('DELETE FROM users')
            
            # Reset autoincrement counters
            cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("users", "friend_requests", "friends", "focus_rooms", "room_members", "room_presence")')
            
            conn.commit()
            conn.close()
            
            print("✅ All focus room data cleared")
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False

# Global instance for easy access
focus_room_storage = FocusRoomStorage()