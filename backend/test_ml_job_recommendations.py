"""
Test ML Job Recommendation Service

Run this to verify ML-based job recommendations work correctly.
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir / "src"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.skill_profile_verified_parent import SkillProfileVerifiedParent
from app.models.skill import SkillProfileParentClaimed
from app.services.ml_job_recommendation_service import (
    recommend_jobs_ml,
    get_student_skill_profile,
    calculate_skill_gap,
    load_ml_model,
    load_jobs_feature_table
)
from datetime import datetime


def test_load_ml_model():
    """Test loading the ML model."""
    print("\n=== Test 1: Load ML Model ===")
    
    model = load_ml_model()
    
    if model is not None:
        print("✓ ML model loaded successfully")
        print(f"  Model type: {type(model)}")
    else:
        print("⚠ ML model not found - will use cosine similarity fallback")
    
    return model is not None


def test_load_jobs():
    """Test loading job features."""
    print("\n=== Test 2: Load Job Features ===")
    
    try:
        jobs_df = load_jobs_feature_table()
        print(f"✓ Loaded {len(jobs_df)} jobs")
        print(f"  Columns: {len(jobs_df.columns)}")
        
        # Show sample
        print("\n  Sample jobs:")
        for idx, row in jobs_df.head(3).iterrows():
            print(f"    - {row['title']} at {row['company']} ({row['role_key']})")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load jobs: {e}")
        return False


def test_create_test_student(db):
    """Create a test student with verified skills."""
    print("\n=== Test 3: Create Test Student ===")
    
    student_id = "TEST_ML_STUDENT"
    
    # Clear existing test data
    db.query(SkillProfileVerifiedParent).filter(
        SkillProfileVerifiedParent.student_id == student_id
    ).delete()
    
    db.query(SkillProfileParentClaimed).filter(
        SkillProfileParentClaimed.student_id == student_id
    ).delete()
    
    db.commit()
    
    # Create verified skills (from quiz results)
    verified_skills = [
        ("Programming & Development", 85.0, "Advanced"),
        ("Web Development", 78.5, "Advanced"),
        ("Database Management", 72.0, "Intermediate"),
        ("Machine Learning & AI", 45.0, "Beginner"),
    ]
    
    for skill_name, score, level in verified_skills:
        skill = SkillProfileVerifiedParent(
            student_id=student_id,
            parent_skill=skill_name,
            verified_score=score,
            verified_level=level,
            created_at=datetime.utcnow()
        )
        db.add(skill)
    
    # Create claimed skills (from transcript)
    claimed_skills = [
        ("Programming & Development", 80.0, "Advanced", 0.85),
        ("DevOps & Cloud", 55.0, "Intermediate", 0.65),
        ("Software Engineering Practices", 68.0, "Intermediate", 0.72),
    ]
    
    for skill_name, score, level, conf in claimed_skills:
        skill = SkillProfileParentClaimed(
            student_id=student_id,
            parent_skill=skill_name,
            parent_score=score,
            parent_level=level,
            confidence=conf,
            created_at=datetime.utcnow()
        )
        db.add(skill)
    
    db.commit()
    
    print(f"✓ Created test student: {student_id}")
    print(f"  Verified skills: {len(verified_skills)}")
    print(f"  Claimed skills: {len(claimed_skills)}")
    
    return student_id


def test_get_student_profile(db, student_id):
    """Test getting student skill profile."""
    print("\n=== Test 4: Get Student Skill Profile ===")
    
    scores, levels = get_student_skill_profile(
        db, student_id, prefer_verified=True
    )
    
    print(f"✓ Retrieved student profile")
    print(f"  Total skills: {len(scores)}")
    
    print("\n  Skill breakdown:")
    for skill, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        level = levels.get(skill, "Unknown")
        print(f"    {skill:40s} {score:5.1f}  [{level}]")
    
    return scores, levels


def test_skill_gap_analysis(scores, levels):
    """Test skill gap calculation."""
    print("\n=== Test 5: Skill Gap Analysis ===")
    
    # Test with sample job requirements
    job_required_skills = [
        "Programming & Development",
        "Web Development",
        "Database Management",
        "DevOps & Cloud",
        "Machine Learning & AI"
    ]
    
    gap_analysis = calculate_skill_gap(
        scores, levels, job_required_skills, threshold=70.0
    )
    
    print(f"✓ Skill gap analysis complete")
    print(f"  Match percentage: {gap_analysis['match_percentage']:.1f}%")
    print(f"\n  Proficient skills ({len(gap_analysis['proficient'])}):")
    for skill in gap_analysis['proficient']:
        print(f"    ✓ {skill['skill']:40s} {skill['score']:5.1f}  [{skill['level']}]")
    
    print(f"\n  Needs improvement ({len(gap_analysis['needs_improvement'])}):")
    for skill in gap_analysis['needs_improvement']:
        print(f"    ⚠ {skill['skill']:40s} {skill['score']:5.1f}  (gap: {skill['gap']:.1f})")
        print(f"       → {skill['recommendation']}")
    
    print(f"\n  Missing skills ({len(gap_analysis['missing'])}):")
    for skill in gap_analysis['missing']:
        print(f"    ✗ {skill['skill']:40s}")
        print(f"       → {skill['recommendation']}")
    
    return gap_analysis


def test_ml_recommendations(db, student_id):
    """Test ML job recommendations."""
    print("\n=== Test 6: ML Job Recommendations ===")
    
    try:
        recommendations = recommend_jobs_ml(
            db=db,
            student_id=student_id,
            top_k=5,
            threshold=70.0,
            use_verified=True,
            role_key=None
        )
        
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        if recommendations:
            print("\n  Top 3 recommendations:")
            for i, job in enumerate(recommendations[:3], 1):
                print(f"\n  {i}. {job['title']} at {job['company']}")
                print(f"     Match Score: {job['match_score']:.1f}%")
                print(f"     Readiness: {job['readiness']['level']} ({job['readiness']['score']:.1f}%)")
                print(f"     Skills: {job['proficient_skills_count']} proficient, "
                      f"{job['needs_improvement_count']} improve, "
                      f"{job['missing_skills_count']} missing")
                
                if job['next_steps']:
                    print(f"     Next Steps:")
                    for step in job['next_steps'][:2]:
                        print(f"       → {step}")
        
        return True
    except Exception as e:
        print(f"✗ ML recommendation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("ML JOB RECOMMENDATION SERVICE - TEST SUITE")
    print("=" * 70)
    
    # Connect to database
    db_path = backend_dir / "src" / "app.db"
    engine = create_engine(f"sqlite:///{db_path}")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Run tests
        results = []
        
        results.append(("Load ML Model", test_load_ml_model()))
        results.append(("Load Job Features", test_load_jobs()))
        
        student_id = test_create_test_student(db)
        results.append(("Create Test Student", student_id is not None))
        
        scores, levels = test_get_student_profile(db, student_id)
        results.append(("Get Student Profile", len(scores) > 0))
        
        gap_analysis = test_skill_gap_analysis(scores, levels)
        results.append(("Skill Gap Analysis", gap_analysis is not None))
        
        results.append(("ML Recommendations", test_ml_recommendations(db, student_id)))
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status:10s} {test_name}")
        
        print(f"\n{passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! ML Job Recommendation system is working.")
        else:
            print("\n⚠ Some tests failed. Check the output above for details.")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
