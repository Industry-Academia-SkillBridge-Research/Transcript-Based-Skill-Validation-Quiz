"""
Migration script to switch from child skills to direct job skills mapping.

This script:
1. Backs up current database
2. Clears old skill data
3. Replaces course_skill_map.csv with new version
4. Reseeds the database
"""

import sys
from pathlib import Path
import shutil
from datetime import datetime

# Add backend/src to path
SCRIPT_DIR = Path(__file__).parent
BACKEND_DIR = SCRIPT_DIR.parent
SRC_DIR = BACKEND_DIR / "src"
DATA_DIR = BACKEND_DIR / "data"
sys.path.insert(0, str(SRC_DIR))

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.skill import SkillProfileClaimed, SkillEvidence, SkillProfileParentClaimed, SkillEvidenceParent
from app.models.course import CourseSkillMap
from app.services.seed_service import seed_course_skill_map


def backup_database():
    """Backup the current database."""
    db_path = SRC_DIR / "app.db"
    if not db_path.exists():
        print("⚠️  No database found to backup")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = SRC_DIR / f"app.db.backup_{timestamp}"
    
    shutil.copy2(db_path, backup_path)
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path


def backup_csv():
    """Backup the current course_skill_map.csv."""
    csv_path = DATA_DIR / "course_skill_map.csv"
    if not csv_path.exists():
        print("⚠️  No course_skill_map.csv found to backup")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = DATA_DIR / f"course_skill_map.csv.backup_{timestamp}"
    
    shutil.copy2(csv_path, backup_path)
    print(f"✅ CSV backed up to: {backup_path.name}")
    return backup_path


def replace_csv():
    """Replace course_skill_map.csv with course_skill_mapping_new.csv."""
    new_csv = DATA_DIR / "course_skill_mapping_new.csv"
    target_csv = DATA_DIR / "course_skill_map.csv"
    
    if not new_csv.exists():
        raise FileNotFoundError(f"New mapping file not found: {new_csv}")
    
    shutil.copy2(new_csv, target_csv)
    print(f"✅ Replaced course_skill_map.csv with course_skill_mapping_new.csv")


def clear_skill_data(db: Session):
    """Clear all existing skill profile data."""
    print("\n🗑️  Clearing old skill data...")
    
    # Count before deletion
    claimed_count = db.query(SkillProfileClaimed).count()
    evidence_count = db.query(SkillEvidence).count()
    parent_claimed_count = db.query(SkillProfileParentClaimed).count()
    parent_evidence_count = db.query(SkillEvidenceParent).count()
    
    print(f"   - SkillProfileClaimed: {claimed_count} records")
    print(f"   - SkillEvidence: {evidence_count} records")
    print(f"   - SkillProfileParentClaimed: {parent_claimed_count} records")
    print(f"   - SkillEvidenceParent: {parent_evidence_count} records")
    
    # Delete all skill data
    db.query(SkillProfileClaimed).delete()
    db.query(SkillEvidence).delete()
    db.query(SkillProfileParentClaimed).delete()
    db.query(SkillEvidenceParent).delete()
    
    db.commit()
    print("✅ Old skill data cleared")


def clear_course_skill_mappings(db: Session):
    """Clear existing course-skill mappings."""
    print("\n🗑️  Clearing old course-skill mappings...")
    
    count = db.query(CourseSkillMap).count()
    print(f"   - Deleting {count} mapping records")
    
    db.query(CourseSkillMap).delete()
    db.commit()
    print("✅ Old mappings cleared")


def reseed_mappings(db: Session):
    """Reseed course-skill mappings from new CSV."""
    print("\n🌱 Reseeding course-skill mappings...")
    
    result = seed_course_skill_map(db)
    print(f"✅ Mappings reseeded:")
    print(f"   - Inserted: {result['inserted']}")
    print(f"   - Updated: {result['updated']}")
    
    return result


def verify_migration(db: Session):
    """Verify the migration completed successfully."""
    print("\n🔍 Verifying migration...")
    
    # Check mappings
    mapping_count = db.query(CourseSkillMap).count()
    print(f"   - CourseSkillMap records: {mapping_count}")
    
    # Show sample skills
    sample_mappings = db.query(CourseSkillMap).limit(5).all()
    print(f"\n   Sample mappings:")
    for mapping in sample_mappings:
        print(f"     {mapping.course_code} → {mapping.skill_name} (weight: {mapping.map_weight})")
    
    # Check unique skills
    unique_skills = db.query(CourseSkillMap.skill_name).distinct().all()
    skill_names = sorted([s[0] for s in unique_skills])
    print(f"\n   Total unique skills: {len(skill_names)}")
    print(f"   Sample skills: {', '.join(skill_names[:10])}...")
    
    print("\n✅ Migration verification complete")


def main():
    """Run the migration."""
    print("=" * 60)
    print("MIGRATION: Child Skills → Direct Job Skills")
    print("=" * 60)
    
    # Confirm
    response = input("\n⚠️  This will backup and replace your skill mapping data. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Migration cancelled")
        return
    
    try:
        # Step 1: Backups
        print("\n📦 Step 1: Creating backups...")
        db_backup = backup_database()
        csv_backup = backup_csv()
        
        # Step 2: Replace CSV
        print("\n📝 Step 2: Replacing CSV file...")
        replace_csv()
        
        # Step 3: Database operations
        db = SessionLocal()
        try:
            print("\n🗄️  Step 3: Updating database...")
            clear_skill_data(db)
            clear_course_skill_mappings(db)
            reseed_mappings(db)
            
            # Step 4: Verify
            verify_migration(db)
            
        finally:
            db.close()
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Restart backend server")
        print("2. Re-upload student transcripts to recompute skills")
        print("3. Verify skills display correctly in frontend")
        print("\nRollback instructions:")
        if db_backup:
            print(f"   Database: Copy {db_backup.name} back to app.db")
        if csv_backup:
            print(f"   CSV: Copy {csv_backup.name} back to course_skill_map.csv")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nPlease restore from backups if needed")
        raise


if __name__ == "__main__":
    main()
