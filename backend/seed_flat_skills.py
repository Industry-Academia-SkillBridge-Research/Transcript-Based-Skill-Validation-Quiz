"""
Seed Database with Flat Skills

Loads course catalog and course-skill mappings from CSV files.
Run this after migration to populate the new flat skill structure.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from app.db import SessionLocal
from app.services.seed_service import seed_course_catalog, seed_course_skill_map
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Seed flat skills data"""
    print("=" * 60)
    print("SEEDING FLAT SKILLS DATABASE")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        # 1. Seed course catalog
        print("📚 1. Seeding course catalog...")
        catalog_result = seed_course_catalog(db)
        print(f"   ✓ Courses: {catalog_result['inserted']} inserted, {catalog_result['updated']} updated")
        print()
        
        # 2. Seed course-skill mappings (flat skills)
        print("🎯 2. Seeding course-skill mappings...")
        mapping_result = seed_course_skill_map(db)
        print(f"   ✓ Mappings: {mapping_result['inserted']} inserted, {mapping_result['updated']} updated")
        print()
        
        print("=" * 60)
        print("✅ SEEDING COMPLETE")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Upload a transcript to compute skills")
        print("2. Skills will be computed directly from course-skill mappings")
        print("3. Quiz questions will use flat skill names (SQL, Python, etc.)")
        
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        print(f"\n❌ ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
