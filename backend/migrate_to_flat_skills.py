"""
Migration Script: Parent/Child Skills -> Flat Skill Structure

This script:
1. Backs up the current database
2. Drops old parent/child skill tables  
3. Clears student skill portfolios
4. Prepares system for flat skill structure
"""

import shutil
import os
from datetime import datetime
from pathlib import Path

# Database backup
def backup_database():
    """Backup the current database before migration"""
    db_path = Path("src/app.db")
    if db_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(f"src/app.db.backup_flat_migration_{timestamp}")
        shutil.copy(db_path, backup_path)
        print(f"✓ Database backed up to: {backup_path}")
        return backup_path
    else:
        print("⚠ No database file found (will be created fresh)")
        return None

# Delete old CSV files
def delete_old_csv_files():
    """Delete old parent/child skill CSV files"""
    old_files = [
        "data/childskill_to_jobskill_map.csv",
        "data/job_skill_to_parent_skill.csv",
        "data/job_parent_skill_features.csv"
    ]
    
    for file in old_files:
        file_path = Path(file)
        if file_path.exists():
            os.remove(file_path)
            print(f"✓ Deleted: {file}")
        else:
            print(f"  Skipped (not found): {file}")

# Drop old database tables
def drop_old_tables():
    """Drop old parent/child skill tables from database"""
    import sys
    sys.path.insert(0, str(Path("src")))
    
    from app.db import engine
    from sqlalchemy import text
    
    old_tables = [
        "skill_group_map",
        "skill_profile_parent_claimed",
        "skill_profile_verified_parent",
        "skill_profile_final_parent",
        "skill_evidence_parent",
        "student_skill_portfolio"  # Will be recreated
    ]
    
    with engine.connect() as conn:
        for table in old_tables:
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                conn.commit()
                print(f"✓ Dropped table: {table}")
            except Exception as e:
                print(f"  Could not drop {table}: {e}")

def main():
    print("=" * 60)
    print("MIGRATING TO FLAT SKILL STRUCTURE")
    print("=" * 60)
    print()
    
    # Step 1: Backup database
    print(" 1. Backing up database...")
    backup_path = backup_database()
    print()
    
    # Step 2: Delete old CSV files
    print("2. Deleting old CSV files...")
    delete_old_csv_files()
    print()
    
    # Step 3: Drop old tables
    print("📊 3. Dropping old database tables...")
    try:
        drop_old_tables()
    except Exception as e:
        print(f"⚠ Error dropping tables: {e}")
        print("   This is OK if starting fresh")
    print()
    
    print("=" * 60)
    print("✅ MIGRATION PREPARATION COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run the updated backend server")
    print("2. Database will be recreated with new structure")
    print("3. Upload transcript to recompute skills with flat structure")
    print()
    if backup_path:
        print(f"💾 Backup saved at: {backup_path}")
        print("   You can restore if needed")

if __name__ == "__main__":
    main()
