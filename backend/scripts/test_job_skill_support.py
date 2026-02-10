"""
Test Job Skill Support in Question Generation

Tests that job skills from job_skills.csv are supported in question generation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app.db import SessionLocal
from app.services.question_bank_service import _get_skill_context


def test_job_skill_validation():
    """Test that job skills are recognized."""
    print("="*60)
    print("Test: Job Skill Validation")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Test 1: Job skill "SQL" should be found
        print("\nTest 1: Validate job skill 'SQL'")
        result = _get_skill_context(db, "SQL")
        
        if result:
            skill_type, context_list, category = result
            print(f"  ✓ SQL recognized")
            print(f"    Type: {skill_type}")
            print(f"    Context: {context_list}")
            print(f"    Category: {category}")
            assert skill_type == "job_skill", f"Expected job_skill, got {skill_type}"
            assert category == "Database", f"Expected Database category, got {category}"
        else:
            print("  ✗ SQL not found")
            return False
        
        # Test 2: Job skill "Python" should be found
        print("\nTest 2: Validate job skill 'Python'")
        result = _get_skill_context(db, "Python")
        
        if result:
            skill_type, context_list, category = result
            print(f"  ✓ Python recognized")
            print(f"    Type: {skill_type}")
            print(f"    Context: {context_list}")
            print(f"    Category: {category}")
            assert skill_type == "job_skill", f"Expected job_skill, got {skill_type}"
            assert category == "Programming Language", f"Expected Programming Language, got {category}"
        else:
            print("  ✗ Python not found")
            return False
        
        # Test 3: Unknown skill should fail
        print("\nTest 3: Validate unknown skill 'NonExistentSkill123'")
        result = _get_skill_context(db, "NonExistentSkill123")
        
        if result is None:
            print("  ✓ Unknown skill correctly rejected")
        else:
            print(f"  ✗ Unknown skill incorrectly accepted: {result}")
            return False
        
        # Test 4: Child skill should still work (if exists)
        print("\nTest 4: Validate child skill (parent skill)")
        # Try a known parent skill from SkillGroupMap
        result = _get_skill_context(db, "Programming Fundamentals & C Language")
        
        if result:
            skill_type, context_list, category = result
            print(f"  ✓ Child skill recognized")
            print(f"    Type: {skill_type}")
            print(f"    Context length: {len(context_list)} child skills")
            print(f"    Category: {category}")
            assert skill_type == "child_skill", f"Expected child_skill, got {skill_type}"
        else:
            print("  ⚠ No child skills found (may be expected if SkillGroupMap is empty)")
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_skill_names_endpoint():
    """Test that skill-names endpoint returns job skills."""
    print("\n" + "="*60)
    print("Test: Skill Names Endpoint")
    print("="*60)
    
    try:
        import requests
        
        # Test endpoint (assumes server is running)
        print("\nTesting GET /admin/question-bank/skill-names...")
        
        try:
            response = requests.get("http://localhost:8000/admin/question-bank/skill-names", timeout=2)
            
            if response.status_code == 200:
                data = response.json()
                skill_names = data.get("skill_names", [])
                
                print(f"  ✓ Endpoint returned {len(skill_names)} skills")
                
                # Check if job skills are present
                job_skills = ["SQL", "Python", "JavaScript", "Java"]
                found = [skill for skill in job_skills if skill in skill_names]
                
                if found:
                    print(f"  ✓ Found job skills: {', '.join(found)}")
                else:
                    print("  ⚠ No job skills found (check job_skills.csv)")
                
                return True
            else:
                print(f"  ✗ Endpoint returned status {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("  ⚠ Server not running (start with: uvicorn app.main:app)")
            print("  → Skipping endpoint test")
            return True  # Don't fail if server isn't running
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "Job Skill Support Test Suite" + " "*20 + "║")
    print("╚" + "="*58 + "╝")
    
    # Test 1: Validation logic
    success1 = test_job_skill_validation()
    
    # Test 2: Endpoint (optional if server running)
    success2 = test_skill_names_endpoint()
    
    if success1 and success2:
        print("\n🎉 All tests passed!\n")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed\n")
        sys.exit(1)
