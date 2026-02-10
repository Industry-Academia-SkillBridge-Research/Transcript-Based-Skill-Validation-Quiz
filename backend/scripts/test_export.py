"""
Test Question Bank Export Functionality

Quick validation tests for export functions.
Run this after implementing export features.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app.db import SessionLocal
from app.models.question_bank import QuestionBank


def test_export_functions():
    """Test that export helper functions work correctly."""
    db = SessionLocal()
    
    try:
        # Get some test questions
        questions = db.query(QuestionBank).limit(5).all()
        
        if not questions:
            print("⚠️  No questions in database. Generate some first:")
            print("   python backend/scripts/generate_and_export_questions.py --skills SQL --count 5")
            return False
        
        print(f"✓ Found {len(questions)} test questions")
        
        # Test 1: Parse options_json
        print("\nTest 1: Parsing options_json...")
        for q in questions:
            try:
                options = json.loads(q.options_json)
                
                # Convert to list format
                if isinstance(options, dict):
                    options_list = [options.get(k, "") for k in ["A", "B", "C", "D"]]
                else:
                    options_list = options
                
                assert len(options_list) == 4, f"Expected 4 options, got {len(options_list)}"
                assert all(isinstance(opt, str) for opt in options_list), "Options must be strings"
                
                print(f"  ✓ Question {q.id}: {len(options_list)} options parsed")
                
            except json.JSONDecodeError as e:
                print(f"  ✗ Question {q.id}: Invalid JSON - {e}")
                return False
            except Exception as e:
                print(f"  ✗ Question {q.id}: Error - {e}")
                return False
        
        # Test 2: Validate correct_option
        print("\nTest 2: Validating correct_option...")
        for q in questions:
            assert q.correct_option in ["A", "B", "C", "D"], \
                f"Invalid correct_option '{q.correct_option}' for question {q.id}"
            print(f"  ✓ Question {q.id}: correct_option = {q.correct_option}")
        
        # Test 3: Validate difficulty
        print("\nTest 3: Validating difficulty...")
        for q in questions:
            assert q.difficulty in ["easy", "medium", "hard"], \
                f"Invalid difficulty '{q.difficulty}' for question {q.id}"
            print(f"  ✓ Question {q.id}: difficulty = {q.difficulty}")
        
        # Test 4: Build sample grouped export
        print("\nTest 4: Building grouped export structure...")
        
        skills_dict = {}
        for q in questions:
            if q.skill_name not in skills_dict:
                skills_dict[q.skill_name] = {"quizzes": {}}
            
            if q.difficulty not in skills_dict[q.skill_name]["quizzes"]:
                skills_dict[q.skill_name]["quizzes"][q.difficulty] = []
            
            options = json.loads(q.options_json)
            if isinstance(options, dict):
                options_list = [options.get(k, "") for k in ["A", "B", "C", "D"]]
            else:
                options_list = options
            
            skills_dict[q.skill_name]["quizzes"][q.difficulty].append({
                "id": q.id,
                "question": q.question_text,
                "options": options_list,
                "answer": q.correct_option
            })
        
        print(f"  ✓ Grouped structure created:")
        for skill, data in skills_dict.items():
            print(f"    - {skill}: {sum(len(qs) for qs in data['quizzes'].values())} questions")
        
        # Test 5: Build sample flat export
        print("\nTest 5: Building flat export structure...")
        
        flat_list = []
        for q in questions:
            options = json.loads(q.options_json)
            if isinstance(options, dict):
                options_list = [options.get(k, "") for k in ["A", "B", "C", "D"]]
            else:
                options_list = options
            
            flat_list.append({
                "id": q.id,
                "skill_name": q.skill_name,
                "difficulty": q.difficulty,
                "question": q.question_text,
                "options": options_list,
                "answer": q.correct_option
            })
        
        print(f"  ✓ Flat list created: {len(flat_list)} questions")
        
        # Test 6: Validate JSON serializability
        print("\nTest 6: Testing JSON serializability...")
        
        try:
            json.dumps({"skills": list(skills_dict.values())})
            print("  ✓ Grouped format is JSON serializable")
        except Exception as e:
            print(f"  ✗ Grouped format serialization failed: {e}")
            return False
        
        try:
            json.dumps(flat_list)
            print("  ✓ Flat format is JSON serializable")
        except Exception as e:
            print(f"  ✗ Flat format serialization failed: {e}")
            return False
        
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()


def test_cli_script_import():
    """Test that CLI scripts can be imported."""
    print("\nTest: CLI script imports...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Test export script
        import export_question_bank_json
        print("  ✓ export_question_bank_json.py imports successfully")
        
        # Test generate+export script
        import generate_and_export_questions
        print("  ✓ generate_and_export_questions.py imports successfully")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


if __name__ == "__main__":
    print("="*50)
    print("Question Bank Export Tests")
    print("="*50)
    
    # Test 1: Export functions
    success1 = test_export_functions()
    
    # Test 2: CLI imports
    success2 = test_cli_script_import()
    
    if success1 and success2:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
