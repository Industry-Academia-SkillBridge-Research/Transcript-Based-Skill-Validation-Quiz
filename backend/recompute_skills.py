"""
Recompute skills from existing courses in the database.
This regenerates the skill_profile_claimed and skill_evidence tables.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.db import SessionLocal
from app.models.course import CourseTaken
from app.services.transcript_processor_flat import compute_skill_scores, save_skill_profile

def recompute_skills(student_id):
    """Recompute all skills from existing courses."""
    db = SessionLocal()
    try:
        # Check if student has courses
        courses = db.query(CourseTaken).filter(
            CourseTaken.student_id == student_id
        ).all()
        
        if not courses:
            print(f"❌ No courses found for student {student_id}")
            print("   Please upload a transcript first.")
            return
        
        print(f"📚 Found {len(courses)} courses for student {student_id}")
        print(f"🔄 Recomputing skills...\n")
        
        # Recompute all skills from courses
        skill_scores = compute_skill_scores(db, student_id)
        
        # Save to database
        save_skill_profile(db, student_id, skill_scores)
        
        db.commit()
        
        print(f"✅ Successfully computed {len(skill_scores['skills'])} skills!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    student_id = "IT21013928"
    
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
    
    recompute_skills(student_id)
