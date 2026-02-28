"""
Clear ONLY portfolio/verified skill records (not claimed skills from transcript).
This allows clearing quiz results while keeping the base skills computed from transcript.
"""

import sys
import os
import sqlite3

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'src', 'app.db')

def clear_portfolio_only(student_id):
    """Clear only portfolio/verified records, keep claimed skills from transcript."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Only clear portfolio and verified skill tables (NOT claimed skills)
    tables_to_clear = [
        'student_skill_portfolio',           # New portfolio system
        'skill_profile_verified_parent',     # Legacy verified skills
        'skill_profile_final_parent'         # Legacy final scores
    ]
    
    total_deleted = 0
    
    try:
        for table in tables_to_clear:
            try:
                # Count records
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE student_id = ?", (student_id,))
                count = cursor.fetchone()[0]
                
                if count > 0:
                    print(f"  - {table}: {count} records")
                    # Delete records
                    cursor.execute(f"DELETE FROM {table} WHERE student_id = ?", (student_id,))
                    total_deleted += count
                    
            except sqlite3.OperationalError as e:
                print(f"  ⚠️  {table}: table doesn't exist or no student_id column")
        
        conn.commit()
        
        if total_deleted > 0:
            print(f"\n✅ Successfully cleared {total_deleted} portfolio records")
            print(f"   Claimed skills from transcript are preserved ✓")
        else:
            print(f"\n✓ No portfolio records to clear")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    student_id = "IT21013928"
    
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
    
    print(f"🗑️  Clearing portfolio for student: {student_id}\n")
    clear_portfolio_only(student_id)
