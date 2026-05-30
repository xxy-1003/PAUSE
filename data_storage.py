"""
Data Storage Module for PAUSE Pomodoro App
Stores completed focus sessions persistently using SQLite
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Tuple

class SessionStorage:
    """SQLite database for storing completed focus sessions"""
    
    def __init__(self, db_path: str = "pause_sessions.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                focus_duration INTEGER NOT NULL,  -- in seconds
                break_duration INTEGER NOT NULL,   -- in seconds
                completed BOOLEAN NOT NULL,
                productivity_score INTEGER,        -- 0-100
                session_type TEXT,                 -- 'focus', 'break', 'interval'
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create daily goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                target_sessions INTEGER NOT NULL,
                completed_sessions INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create streaks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date TEXT NOT NULL,
                end_date TEXT,
                streak_days INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_session(self, focus_duration: int, break_duration: int, 
                 completed: bool = True, productivity_score: int = None, 
                 session_type: str = "focus", notes: str = None,
                 session_date: str = None) -> int:
        """
        Save a completed session to the database
        
        Args:
            focus_duration: Focus time in seconds
            break_duration: Break time in seconds
            completed: Whether session was completed
            productivity_score: Self-assessed productivity score (0-100)
            session_type: Type of session ('focus', 'break', 'interval')
            notes: Optional notes about the session
            
        Returns:
            session_id: ID of the saved session
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_date = session_date or datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute('''
            INSERT INTO sessions (date, focus_duration, break_duration, 
                                 completed, productivity_score, session_type, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_date, focus_duration, break_duration, 
              completed, productivity_score, session_type, notes))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Update streak after saving session
        self.update_streak(current_date)
        
        return session_id
    
    def get_sessions(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Get sessions within a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with session data
        """
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM sessions WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC, created_at DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_daily_summary(self, days: int = 30) -> pd.DataFrame:
        """
        Get daily summary of sessions for the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            DataFrame with daily summaries
        """
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                date,
                COUNT(*) as session_count,
                SUM(focus_duration) as total_focus_seconds,
                SUM(break_duration) as total_break_seconds,
                AVG(productivity_score) as avg_productivity,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_sessions
            FROM sessions
            WHERE date BETWEEN ? AND ?
            GROUP BY date
            ORDER BY date DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        # Convert seconds to hours
        if not df.empty:
            df['total_focus_hours'] = df['total_focus_seconds'] / 3600
            df['total_break_hours'] = df['total_break_seconds'] / 3600
            # Calculate average focus duration in minutes, handle division by zero, round to 1 decimal
            df['avg_focus_duration'] = df.apply(
                lambda row: round(row['total_focus_seconds'] / row['session_count'] / 60, 1) if row['session_count'] > 0 else 0,
                axis=1
            )
        
        return df
    
    def get_today_summary(self) -> pd.DataFrame:
        """
        Get summary of sessions for today only
        
        Returns:
            DataFrame with today's summary (empty if no sessions today)
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                date,
                COUNT(*) as session_count,
                SUM(focus_duration) as total_focus_seconds,
                SUM(break_duration) as total_break_seconds,
                AVG(productivity_score) as avg_productivity,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_sessions
            FROM sessions
            WHERE date = ?
            GROUP BY date
        '''
        
        df = pd.read_sql_query(query, conn, params=(today,))
        conn.close()
        
        # Convert seconds to hours
        if not df.empty:
            df['total_focus_hours'] = df['total_focus_seconds'] / 3600
            df['total_break_hours'] = df['total_break_seconds'] / 3600
            # Calculate average focus duration in minutes, handle division by zero, round to 1 decimal
            df['avg_focus_duration'] = df.apply(
                lambda row: round(row['total_focus_seconds'] / row['session_count'] / 60, 1) if row['session_count'] > 0 else 0,
                axis=1
            )
        
        return df
    
    def get_weekly_summary(self, weeks: int = 8) -> pd.DataFrame:
        """
        Get weekly summary of sessions
        
        Args:
            weeks: Number of weeks to look back
            
        Returns:
            DataFrame with weekly summaries
        """
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                strftime('%Y-%W', date) as week,
                COUNT(*) as session_count,
                SUM(focus_duration) as total_focus_seconds,
                AVG(productivity_score) as avg_productivity,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_sessions
            FROM sessions
            WHERE date >= date('now', ? || ' days')
            GROUP BY week
            ORDER BY week DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(f"-{weeks*7}",))
        conn.close()
        
        # Convert seconds to hours
        if not df.empty:
            df['total_focus_hours'] = df['total_focus_seconds'] / 3600
            # Calculate average focus duration in minutes, handle division by zero, round to 1 decimal
            df['avg_focus_duration'] = df.apply(
                lambda row: round(row['total_focus_seconds'] / row['session_count'] / 60, 1) if row['session_count'] > 0 else 0,
                axis=1
            )
        
        return df
    
    def get_monthly_heatmap_data(self, year: int = None, month: int = None) -> Dict:
        """
        Get data for monthly heatmap visualization
        
        Args:
            year: Year to get data for (default: current year)
            month: Month to get data for (default: current month)
            
        Returns:
            Dictionary with heatmap data
        """
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                date,
                COUNT(*) as session_count,
                SUM(focus_duration) as total_focus_minutes
            FROM sessions
            WHERE date >= ? AND date < ?
            GROUP BY date
        '''
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        # Create heatmap data structure
        heatmap_data = {}
        for _, row in df.iterrows():
            date_obj = datetime.strptime(row['date'], "%Y-%m-%d")
            day_key = date_obj.strftime("%Y-%m-%d")
            heatmap_data[day_key] = {
                'session_count': int(row['session_count']),
                'total_focus_minutes': int(row['total_focus_minutes'] / 60) if pd.notna(row['total_focus_minutes']) else 0
            }
        
        return heatmap_data
    
    def get_advanced_insights(self, days: int = 30) -> Dict:
        """
        Calculate advanced insights from session data
        
        Args:
            days: Number of days to look back for insights
            
        Returns:
            Dictionary with various insights
        """
        conn = sqlite3.connect(self.db_path)
        
        insights = {}
        
        # Calculate date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        # Total focus time within date range
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(focus_duration) FROM sessions WHERE completed = 1 AND date BETWEEN ? AND ?", 
                      (start_date, end_date))
        total_focus_seconds = cursor.fetchone()[0] or 0
        insights['total_focus_hours'] = total_focus_seconds / 3600
        
        # Average focus duration within date range
        cursor.execute("SELECT AVG(focus_duration) FROM sessions WHERE completed = 1 AND date BETWEEN ? AND ?", 
                      (start_date, end_date))
        avg_focus_seconds = cursor.fetchone()[0] or 0
        insights['avg_focus_minutes'] = round(avg_focus_seconds / 60, 1)  # Round to 1 decimal place
        
        # Session completion rate within date range
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE date BETWEEN ? AND ?", (start_date, end_date))
        total_sessions = cursor.fetchone()[0] or 1
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE completed = 1 AND date BETWEEN ? AND ?", 
                      (start_date, end_date))
        completed_sessions = cursor.fetchone()[0] or 0
        insights['completion_rate'] = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Most productive day (by session count) within date range
        cursor.execute('''
            SELECT date, COUNT(*) as session_count 
            FROM sessions 
            WHERE completed = 1 AND date BETWEEN ? AND ?
            GROUP BY date 
            ORDER BY session_count DESC 
            LIMIT 1
        ''', (start_date, end_date))
        result = cursor.fetchone()
        insights['most_productive_day'] = {
            'date': result[0] if result else None,
            'session_count': result[1] if result else 0
        }
        
        # Current streak
        cursor.execute('''
            SELECT streak_days 
            FROM streaks 
            WHERE is_active = 1 
            ORDER BY start_date DESC 
            LIMIT 1
        ''')
        result = cursor.fetchone()
        insights['current_streak'] = result[0] if result else 0
        
        # Best focus session (longest focus duration) within date range
        cursor.execute('''
            SELECT date, focus_duration 
            FROM sessions 
            WHERE completed = 1 AND date BETWEEN ? AND ?
            ORDER BY focus_duration DESC 
            LIMIT 1
        ''', (start_date, end_date))
        result = cursor.fetchone()
        insights['best_session'] = {
            'date': result[0] if result else None,
            'focus_minutes': (result[1] / 60) if result else 0
        }
        
        # Sessions within date range
        cursor.execute('''
            SELECT COUNT(*) 
            FROM sessions 
            WHERE date BETWEEN ? AND ? AND completed = 1
        ''', (start_date, end_date))
        result = cursor.fetchone()
        insights['sessions_in_range'] = result[0] if result else 0
        
        # Focus consistency (days with at least one session in date range)
        cursor.execute('''
            SELECT COUNT(DISTINCT date) 
            FROM sessions 
            WHERE date BETWEEN ? AND ? AND completed = 1
        ''', (start_date, end_date))
        result = cursor.fetchone()
        days_with_sessions = result[0] if result else 0
        insights['focus_consistency'] = (days_with_sessions / days * 100) if days > 0 else 0
        
        # Additional metrics for burnout assessment
        # Average daily focus hours
        if days_with_sessions > 0:
            insights['avg_daily_focus_hours'] = insights['total_focus_hours'] / days_with_sessions
        else:
            insights['avg_daily_focus_hours'] = 0
            
        # Distraction metric (incomplete sessions)
        cursor.execute('''
            SELECT COUNT(*) 
            FROM sessions 
            WHERE date BETWEEN ? AND ? AND completed = 0
        ''', (start_date, end_date))
        result = cursor.fetchone()
        insights['incomplete_sessions'] = result[0] if result else 0
        
        conn.close()
        
        return insights
    
    def update_streak(self, current_date: str):
        """Update streak information based on current date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if there was a session yesterday
        yesterday = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE date = ?", (yesterday,))
        had_session_yesterday = cursor.fetchone()[0] > 0
        
        # Get current active streak
        cursor.execute("SELECT streak_id, streak_days FROM streaks WHERE is_active = 1 ORDER BY start_date DESC LIMIT 1")
        current_streak = cursor.fetchone()
        
        if current_streak:
            streak_id, streak_days = current_streak
            
            if had_session_yesterday:
                # Continue streak
                cursor.execute("UPDATE streaks SET streak_days = streak_days + 1 WHERE streak_id = ?", (streak_id,))
            else:
                # Break streak
                cursor.execute("UPDATE streaks SET is_active = 0, end_date = ? WHERE streak_id = ?", (yesterday, streak_id))
                # Start new streak
                cursor.execute('''
                    INSERT INTO streaks (start_date, streak_days, is_active)
                    VALUES (?, 1, 1)
                ''', (current_date,))
        else:
            # Start first streak
            cursor.execute('''
                INSERT INTO streaks (start_date, streak_days, is_active)
                VALUES (?, 1, 1)
            ''', (current_date,))
        
        conn.commit()
        conn.close()
    
    def export_to_csv(self, filepath: str = "pause_sessions_export.csv"):
        """Export all sessions to CSV file"""
        df = self.get_sessions()
        df.to_csv(filepath, index=False)
        return filepath
    
    def clear_old_data(self, days_to_keep: int = 365):
        """Clear sessions older than specified days (for data management)"""
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE date < ?", (cutoff_date,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def clear_corrupted_data(self):
        """
        Clear obviously corrupted data:
        - Sessions with focus_duration > 24 hours (86400 seconds)
        - Sessions with negative focus_duration
        - Sessions with focus_duration = 0
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete sessions with impossible focus durations
        cursor.execute("""
            DELETE FROM sessions 
            WHERE focus_duration > 86400  -- More than 24 hours
               OR focus_duration <= 0     -- Negative or zero duration
               OR focus_duration IS NULL  -- NULL duration
        """)
        
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_session_count(self):
        """Get total number of sessions in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sessions")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count


# Global instance for easy access
session_storage = SessionStorage()