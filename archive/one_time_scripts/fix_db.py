"""
Script to check and fix database schema by adding missing specialization column
"""
import sqlite3
import os
from pathlib import Path

# Find all .db files
backend_dir = Path(__file__).parent
db_files = list(backend_dir.rglob("*.db"))

print(f"Found {len(db_files)} database files:")
for db_file in db_files:
    print(f"\n{'='*60}")
    print(f"Database: {db_file}")
    print(f"{'='*60}")
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    try:
        # Get current schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
        result = cursor.fetchone()
        
        if result:
            print("Current students table schema:")
            print(result[0])
            
            # Check if specialization column exists
            cursor.execute("PRAGMA table_info(students)")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"\nColumns: {columns}")
            
            if 'specialization' not in columns:
                print("\n⚠️  Missing specialization column! Adding it now...")
                cursor.execute("ALTER TABLE students ADD COLUMN specialization TEXT")
                conn.commit()
                print("✓ Added specialization column successfully")
            else:
                print("\n✓ Specialization column already exists")
        else:
            print("❌ No students table found in this database")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        conn.close()

print(f"\n{'='*60}")
print("Done!")
