"""
Migration script to add specialization column to students table.
Run this once to update the database schema.
"""

import sqlite3
from pathlib import Path

# Get database path
BACKEND_DIR = Path(__file__).resolve().parent
DB_PATH = BACKEND_DIR / "transcript_validation.db"

def add_specialization_column():
    """Add specialization column to students table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'specialization' not in columns:
            print("Adding specialization column to students table...")
            cursor.execute("ALTER TABLE students ADD COLUMN specialization TEXT")
            conn.commit()
            print("✓ Successfully added specialization column")
        else:
            print("✓ Specialization column already exists")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("Running database migration...")
    add_specialization_column()
    print("Migration complete!")
