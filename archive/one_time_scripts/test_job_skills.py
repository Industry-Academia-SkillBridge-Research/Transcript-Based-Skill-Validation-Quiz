"""
Test script for job skill scoring functionality.

Run from backend directory:
    python test_job_skills.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from app.db import SessionLocal
from app.services.job_skill_scoring import (
    load_job_skills, 
    load_child_to_job_mapping,
    compute_job_skill_scores_for_student
)


def test_load_job_skills():
    """Test that job_skills.csv loads correctly."""
    print("\n=== Test 1: Load Job Skills ===")
    
    try:
        df = load_job_skills()
        print(f"✓ Loaded {len(df)} job skills")
        
        print("\nSample job skills:")
        for i, row in df.head(5).iterrows():
            print(f"  - {row['JobSkillID']}: {row['JobSkillName']} ({row['Category']})")
        
        categories = df['Category'].unique()
        print(f"\nCategories ({len(categories)})")
        
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_load_mappings():
    """Test mappings load."""
    print("\n=== Test 2: Load Mappings ===")
    
    try:
        df = load_child_to_job_mapping()
        print(f"✓ Loaded {len(df)} mappings")
        
        unique_js = df['JobSkillID'].nunique()
        unique_cs = df['ChildSkill'].nunique()
        print(f"✓ {unique_cs} child skills → {unique_js} job skills")
        
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_compute_scores(student_id="IT21013928"):
    """Test score computation."""
    print(f"\n=== Test 3: Compute Scores for {student_id} ===")
    
    db = SessionLocal()
    try:
        result = compute_job_skill_scores_for_student(student_id, db)
        
        print(f"✓ Computed {len(result['job_skill_details'])} job skills")
        print(f"  - Mapped: {result['mapping_stats']['mapped_child_skills']}")
        print(f"  - Total: {result['mapping_stats']['total_child_skills']}")
        
        top_skills = result['job_skill_details'][:10]
        if top_skills:
            print("\nTop 10 Job Skills:")
            for i, skill in enumerate(top_skills, 1):
                print(f"  {i}. {skill['job_skill_name']:20s}: {skill['score']:.2f}")
        
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Job Skill Scoring Test Suite")
    print("=" * 60)
    
    results = []
    results.append(("Load Job Skills", test_load_job_skills()))
    results.append(("Load Mappings", test_load_mappings()))
    results.append(("Compute Scores", test_compute_scores()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:12s} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    print(f"\n{passed}/{len(results)} tests passed")


if __name__ == "__main__":
    main()
