"""
Check database tables and find portfolio data.
"""

import sys
import os
import sqlite3

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'src', 'app.db')

def check_database():
    """Check what tables exist and their contents."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("📊 Available tables:")
    print("=" * 60)
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} records")
    
    print("\n🔍 Looking for portfolio-related tables...")
    print("=" * 60)
    
    # Check for quiz attempts or portfolio data
    student_id = "IT21013928"
    
    # Check various possible tables
    possible_tables = [
        'student_skill_portfolio',
        'student_skills',
        'quiz_attempts',
        'skill_profile',
        'skills',
        'parent_skills',
        'child_skills'
    ]
    
    for table_name in possible_tables:
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE student_id = ? LIMIT 5", (student_id,))
            rows = cursor.fetchall()
            if rows:
                print(f"\n✅ Found data in '{table_name}':")
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"   Columns: {', '.join(columns)}")
                print(f"   Records: {len(rows)}")
        except sqlite3.OperationalError as e:
            pass  # Table doesn't exist
    
    conn.close()

if __name__ == "__main__":
    print(f"Database: {db_path}")
    print()
    check_database()
