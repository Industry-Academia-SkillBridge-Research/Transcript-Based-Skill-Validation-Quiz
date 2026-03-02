"""
Migration script to add new columns to students table.
Run this from backend directory: python src/app/migrate_student_table.py
"""

import sqlite3
import os

# Get the database path
db_path = os.path.join(os.path.dirname(__file__), "..", "app.db")

if not os.path.exists(db_path):
    db_path = os.path.join(os.path.dirname(__file__), "app.db")
    if not os.path.exists(db_path):
        print(f"Database not found. Tried:")
        print(f"  - {os.path.join(os.path.dirname(__file__), '..', 'app.db')}")
        print(f"  - {os.path.join(os.path.dirname(__file__), 'app.db')}")
        exit(1)

print(f"Migrating database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current columns
cursor.execute("PRAGMA table_info(students)")
existing_columns = [row[1] for row in cursor.fetchall()]
print(f"Existing columns: {existing_columns}")

# Add new columns if they don't exist
migrations = [
    ("email", "ALTER TABLE students ADD COLUMN email TEXT"),
    ("photo_url", "ALTER TABLE students ADD COLUMN photo_url TEXT"),
    ("bio", "ALTER TABLE students ADD COLUMN bio TEXT")
]

for col_name, sql in migrations:
    if col_name not in existing_columns:
        try:
            cursor.execute(sql)
            print(f"✓ Added column: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"✗ Failed to add {col_name}: {e}")
    else:
        print(f"○ Column already exists: {col_name}")

conn.commit()
conn.close()

print("\nMigration complete!")
