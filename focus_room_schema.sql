-- Focus Room System Database Schema
-- SQLite schema for PAUSE Pomodoro App Focus Room feature

-- ============================================
-- TABLE 1: users
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UN NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 2: friend_requests
-- ============================================
CREATE TABLE IF NOT EXISTS friend_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(sender_id, receiver_id) -- Prevent duplicate friend requests
);

-- ============================================
-- TABLE 3: friends
-- ============================================
CREATE TABLE IF NOT EXISTS friends (
    friend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    friend_user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (friend_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, friend_user_id) -- Ensure unique friendships
);

-- ============================================
-- TABLE 4: focus_rooms
-- ============================================
CREATE TABLE IF NOT EXISTS focus_rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    is_private BOOLEAN NOT NULL DEFAULT 0, -- 0 = public, 1 = private
    voice_enabled BOOLEAN NOT NULL DEFAULT 0,
    chat_enabled BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================
-- TABLE 5: room_members
-- ============================================
CREATE TABLE IF NOT EXISTS room_members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES focus_rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(room_id, user_id) -- Prevent duplicate room memberships
);

-- ============================================
-- TABLE 6: room_presence
-- ============================================
CREATE TABLE IF NOT EXISTS room_presence (
    presence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'online', -- 'online', 'focusing', 'break', 'paused', 'offline'
    remaining_time INTEGER, -- in seconds
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES focus_rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(room_id, user_id) -- One presence record per user per room
);

-- ============================================
-- INDEXES for performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_friend_requests_sender ON friend_requests(sender_id);
CREATE INDEX IF NOT EXISTS idx_friend_requests_receiver ON friend_requests(receiver_id);
CREATE INDEX IF NOT EXISTS idx_friend_requests_status ON friend_requests(status);
CREATE INDEX IF NOT EXISTS idx_friends_user ON friends(user_id);
CREATE INDEX IF NOT EXISTS idx_friends_friend ON friends(friend_user_id);
CREATE INDEX IF NOT EXISTS idx_focus_rooms_owner ON focus_rooms(owner_id);
CREATE INDEX IF NOT EXISTS idx_focus_rooms_private ON focus_rooms(is_private);
CREATE INDEX IF NOT EXISTS idx_room_members_room ON room_members(room_id);
CREATE INDEX IF NOT EXISTS idx_room_members_user ON room_members(user_id);
CREATE INDEX IF NOT EXISTS idx_room_presence_room ON room_presence(room_id);
CREATE INDEX IF NOT EXISTS idx_room_presence_user ON room_presence(user_id);
CREATE INDEX IF NOT EXISTS idx_room_presence_status ON room_presence(status);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- ============================================
-- SAMPLE DATA for testing
-- ============================================
-- Note: Passwords are hashed with 'password123' for testing
INSERT OR IGNORE INTO users (username, email, password_hash) VALUES
    ('xiangyi', 'xiangyi@example.com', 'hashed_password_123'),
    ('amir', 'amir@example.com', 'hashed_password_123'),
    ('danial', 'danial@example.com', 'hashed_password_123');

-- Create sample friend relationships
INSERT OR IGNORE INTO friends (user_id, friend_user_id) VALUES
    (1, 2), -- xiangyi friends with amir
    (1, 3), -- xiangyi friends with danial
    (2, 3); -- amir friends with danial

-- Create sample focus room
INSERT OR IGNORE INTO focus_rooms (room_name, owner_id, is_private, voice_enabled, chat_enabled) VALUES
    ('FYP Warriors', 1, 0, 0, 1); -- Public room, chat enabled, voice disabled

-- Add members to the room
INSERT OR IGNORE INTO room_members (room_id, user_id) VALUES
    (1, 1), -- xiangyi
    (1, 2), -- amir
    (1, 3); -- danial

-- Add sample presence data
INSERT OR IGNORE INTO room_presence (room_id, user_id, status, remaining_time) VALUES
    (1, 1, 'focusing', 1200), -- xiangyi: focusing, 20 minutes remaining
    (1, 2, 'break', 300),     -- amir: break, 5 minutes remaining
    (1, 3, 'online', NULL);   -- danial: online, no timer

-- ============================================
-- VIEWS for common queries
-- ============================================
CREATE VIEW IF NOT EXISTS v_user_friends AS
SELECT 
    u.user_id,
    u.username,
    f.friend_user_id,
    uf.username as friend_username,
    f.created_at as friendship_date
FROM users u
JOIN friends f ON u.user_id = f.user_id
JOIN users uf ON f.friend_user_id = uf.user_id;

CREATE VIEW IF NOT EXISTS v_room_details AS
SELECT 
    r.room_id,
    r.room_name,
    u.username as owner_name,
    r.is_private,
    r.voice_enabled,
    r.chat_enabled,
    r.created_at,
    COUNT(rm.user_id) as member_count
FROM focus_rooms r
JOIN users u ON r.owner_id = u.user_id
LEFT JOIN room_members rm ON r.room_id = rm.room_id
GROUP BY r.room_id;

CREATE VIEW IF NOT EXISTS v_room_presence_details AS
SELECT 
    rp.room_id,
    r.room_name,
    rp.user_id,
    u.username,
    rp.status,
    rp.remaining_time,
    rp.updated_at
FROM room_presence rp
JOIN users u ON rp.user_id = u.user_id
JOIN focus_rooms r ON rp.room_id = r.room_id;