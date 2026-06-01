"""
SQLite-based data storage system for PAUSE Pomodoro application.
This module provides a simple, production-ready storage layer for focus sessions.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import os


class SessionStorage:
    """SQLite database for storing completed focus sessions with username support"""
    
    def __init__(self, db_path: str = "pause.db"):
        """
        Initialize database connection and create tables if they don't exist
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table with required schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                session_date TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries by username and date
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sessions_username_date 
            ON sessions (username, session_date)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_session(self, username: str, duration_minutes: int) -> int:
        """
        Save a completed session to the database
        
        Args:
            username: User identifier
            duration_minutes: Duration of the focus session in minutes
            
        Returns:
            session_id: ID of the saved session
            
        Raises:
            ValueError: If duration_minutes is not positive
            sqlite3.Error: If database operation fails
        """
        if duration_minutes <= 0:
            raise ValueError("Duration must be positive")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO sessions (username, session_date, duration_minutes, completed_at)
                VALUES (?, ?, ?, ?)
            ''', (username, current_date, duration_minutes, completed_at))
            
            session_id = cursor.lastrowid
            conn.commit()
            
            return session_id
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to save session: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_today_sessions(self, username: str) -> pd.DataFrame:
        """
        Get all sessions for the current user today
        
        Args:
            username: User identifier
            
        Returns:
            DataFrame with today's sessions, empty DataFrame if no sessions
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            query = '''
                SELECT 
                    id,
                    username,
                    session_date,
                    duration_minutes,
                    completed_at,
                    created_at
                FROM sessions
                WHERE username = ? AND session_date = ?
                ORDER BY completed_at DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(username, today))
            return df
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get today's sessions: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_weekly_sessions(self, username: str) -> pd.DataFrame:
        """
        Get all sessions for the current user in the current week
        
        Args:
            username: User identifier
            
        Returns:
            DataFrame with this week's sessions, empty DataFrame if no sessions
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Calculate start of week (Monday)
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            start_date = start_of_week.strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
            
            query = '''
                SELECT 
                    id,
                    username,
                    session_date,
                    duration_minutes,
                    completed_at,
                    created_at
                FROM sessions
                WHERE username = ? AND session_date BETWEEN ? AND ?
                ORDER BY session_date DESC, completed_at DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(username, start_date, end_date))
            return df
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get weekly sessions: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_all_sessions(self, username: str) -> pd.DataFrame:
        """
        Get all sessions for the current user
        
        Args:
            username: User identifier
            
        Returns:
            DataFrame with all user's sessions, empty DataFrame if no sessions
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT 
                    id,
                    username,
                    session_date,
                    duration_minutes,
                    completed_at,
                    created_at
                FROM sessions
                WHERE username = ?
                ORDER BY session_date DESC, completed_at DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(username,))
            return df
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get all sessions: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_total_focus_time(self, username: str) -> Dict[str, float]:
        """
        Get total focus time statistics for the current user
        
        Args:
            username: User identifier
            
        Returns:
            Dictionary with focus time statistics:
            - total_minutes: Total focus time in minutes
            - total_hours: Total focus time in hours
            - session_count: Total number of sessions
            - avg_duration: Average session duration in minutes
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total minutes and session count
            cursor.execute('''
                SELECT 
                    SUM(duration_minutes) as total_minutes,
                    COUNT(*) as session_count
                FROM sessions
                WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            total_minutes = result[0] or 0
            session_count = result[1] or 0
            
            # Calculate statistics
            stats = {
                'total_minutes': float(total_minutes),
                'total_hours': round(total_minutes / 60, 2),
                'session_count': session_count,
                'avg_duration': round(total_minutes / session_count, 1) if session_count > 0 else 0
            }
            
            return stats
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get total focus time: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_daily_summary(self, username: str, days: int = 30) -> pd.DataFrame:
        """
        Get daily summary of sessions for the last N days
        
        Args:
            username: User identifier
            days: Number of days to look back
            
        Returns:
            DataFrame with daily summaries
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            query = '''
                SELECT 
                    session_date,
                    COUNT(*) as session_count,
                    SUM(duration_minutes) as total_minutes,
                    AVG(duration_minutes) as avg_duration
                FROM sessions
                WHERE username = ? AND session_date BETWEEN ? AND ?
                GROUP BY session_date
                ORDER BY session_date DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(username, start_date, end_date))
            
            # Add calculated columns
            if not df.empty:
                df['total_hours'] = df['total_minutes'] / 60
                df['total_hours'] = df['total_hours'].round(2)
                df['avg_duration'] = df['avg_duration'].round(1)
            
            return df
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get daily summary: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_user_statistics(self, username: str) -> Dict:
        """
        Get comprehensive statistics for a user
        
        Args:
            username: User identifier
            
        Returns:
            Dictionary with user statistics
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            stats = {}
            
            # Get total focus time
            focus_stats = self.get_total_focus_time(username)
            stats.update(focus_stats)
            
            # Get today's sessions
            today_sessions = self.get_today_sessions(username)
            stats['today_sessions'] = len(today_sessions)
            stats['today_minutes'] = today_sessions['duration_minutes'].sum() if not today_sessions.empty else 0
            
            # Get weekly sessions
            weekly_sessions = self.get_weekly_sessions(username)
            stats['weekly_sessions'] = len(weekly_sessions)
            stats['weekly_minutes'] = weekly_sessions['duration_minutes'].sum() if not weekly_sessions.empty else 0
            
            # Get current streak (consecutive days with at least one session)
            all_sessions = self.get_all_sessions(username)
            if not all_sessions.empty:
                # Convert session_date to datetime and get unique dates
                all_sessions['date_dt'] = pd.to_datetime(all_sessions['session_date'])
                unique_dates = sorted(all_sessions['date_dt'].unique(), reverse=True)
                
                # Calculate streak
                streak = 0
                current_date = datetime.now().date()
                
                for i, session_date in enumerate(unique_dates):
                    date_diff = (current_date - session_date.date()).days
                    if date_diff == i:
                        streak += 1
                    else:
                        break
                
                stats['current_streak'] = streak
            else:
                stats['current_streak'] = 0
            
            return stats
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get user statistics: {e}")
    
    def clear_user_sessions(self, username: str) -> int:
        """
        Clear all sessions for a specific user
        
        Args:
            username: User identifier
            
        Returns:
            Number of sessions deleted
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM sessions WHERE username = ?', (username,))
            deleted_count = cursor.rowcount
            
            conn.commit()
            return deleted_count
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to clear user sessions: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def clear_all_sessions(self) -> int:
        """
        Clear all sessions from the database
        
        Returns:
            Number of sessions deleted
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM sessions')
            deleted_count = cursor.rowcount
            
            conn.commit()
            return deleted_count
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to clear all sessions: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def generate_mock_data(self, username: str = "default_user", days: int = 60) -> int:
        """
        Generate mock session data for testing
        
        Args:
            username: User identifier for mock data
            days: Number of days to generate data for
            
        Returns:
            Number of mock sessions created
        """
        import random
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now()
            session_count = 0
            
            for i in range(days):
                # 70% chance of having sessions on a given day
                if random.random() < 0.7:
                    # 1-4 sessions per day
                    daily_sessions = random.randint(1, 4)
                    
                    for j in range(daily_sessions):
                        session_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                        
                        # Generate random completion time within the day
                        hour = random.randint(8, 20)
                        minute = random.randint(0, 59)
                        second = random.randint(0, 59)
                        completed_at = f"{session_date} {hour:02d}:{minute:02d}:{second:02d}"
                        
                        # Random duration between 25-50 minutes (typical Pomodoro)
                        duration_minutes = random.randint(25, 50)
                        
                        cursor.execute('''
                            INSERT INTO sessions (username, session_date, duration_minutes, completed_at)
                            VALUES (?, ?, ?, ?)
                        ''', (username, session_date, duration_minutes, completed_at))
                        
                        session_count += 1
            
            conn.commit()
            return session_count
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to generate mock data: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def export_to_csv(self, username: str, filepath: str = None) -> str:
        """
        Export user's sessions to CSV file
        
        Args:
            username: User identifier
            filepath: Path to save CSV file (default: username_sessions.csv)
            
        Returns:
            Path to the saved CSV file
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        if filepath is None:
            filepath = f"{username}_sessions.csv"
        
        try:
            df = self.get_all_sessions(username)
            df.to_csv(filepath, index=False)
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to export to CSV: {e}")


# Global instance for easy access
session_storage = SessionStorage()


def test_storage_system():
    """Test the storage system with sample data"""
    print("Testing PAUSE storage system...")
    
    # Create storage instance
    storage = SessionStorage("test_pause.db")
    
    # Test 1: Save sessions
    print("\n1. Saving test sessions...")
    session_ids = []
    for i in range(5):
        session_id = storage.save_session("test_user", 25 + i * 5)
        session_ids.append(session_id)
        print(f"  Saved session {session_id}: 25+{i*5} minutes")
    
    # Test 2: Get today's sessions
    print("\n2. Getting today's sessions...")
    today_df = storage.get_today_sessions("test_user")
    print(f"  Found {len(today_df)} sessions today")
    if not today_df.empty:
        print(f"  Total minutes today: {today_df['duration_minutes'].sum()}")
    
    # Test 3: Get weekly sessions
    print("\n3. Getting weekly sessions...")
    weekly_df = storage.get_weekly_sessions("test_user")
    print(f"  Found {len(weekly_df)} sessions this week")
    
    # Test 4: Get all sessions
    print("\n4. Getting all sessions...")
    all_df = storage.get_all_sessions("test_user")
    print(f"  Found {len(all_df)} total sessions")
    
    # Test 5: Get total focus time
    print("\n5. Getting total focus time...")
    focus_stats = storage.get_total_focus_time("test_user")
    print(f"  Total minutes: {focus_stats['total_minutes']}")
    print(f"  Total hours: {focus_stats['total_hours']}")
    print(f"  Session count: {focus_stats['session_count']}")
    print(f"  Average duration: {focus_stats['avg_duration']} minutes")
    
    # Test 6: Get daily summary
    print("\n6. Getting daily summary...")
    daily_summary = storage.get_daily_summary("test_user", 7)
    print(f"  Daily summary for last 7 days:")
    if not daily_summary.empty:
        for _, row in daily_summary.iterrows():
            print(f"    {row['session_date']}: {row['session_count']} sessions, {row['total_minutes']} minutes")
    
    # Test 7: Get user statistics
    print("\n7. Getting user statistics...")
    user_stats = storage.get_user_statistics("test_user")
    print(f"  Today sessions: {user_stats['today_sessions']}")
    print(f"  Today minutes: {user_stats['today_minutes']}")
    print(f"  Weekly sessions: {user_stats['weekly_sessions']}")
    print(f"  Weekly minutes: {user_stats['weekly_minutes']}")
    print(f"  Current streak: {user_stats['current_streak']} days")
    
    # Test 8: Export to CSV
    print("\n8. Exporting to CSV...")
    csv_path = storage.export_to_csv("test_user", "test_export.csv")
    print(f"  Exported to: {csv_path}")
    
    # Cleanup
    print("\n9. Cleaning up test data...")
    deleted = storage.clear_user_sessions("test_user")
    print(f"  Deleted {deleted} test sessions")
    
    # Delete test database
    if os.path.exists("test_pause.db"):
        os.remove("test_pause.db")
        print("  Removed test database")
    
    print("\n✅ All tests completed successfully!")


if __name__ == "__main__":
    test_storage_system()