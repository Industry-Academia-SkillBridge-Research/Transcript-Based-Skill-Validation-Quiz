from app.db import SessionLocal
from app.models.course import CourseTaken
from app.models.skill import SkillProfileClaimed

db = SessionLocal()

# Check courses
courses = db.query(CourseTaken).filter(CourseTaken.student_id == 'IT21013928').all()
print(f'Courses for IT21013928: {len(courses)}')
if len(courses) > 0:
    for c in courses[:10]:
        print(f'  {c.course_code} - {c.grade}')
    print()

# Check skills
skills = db.query(SkillProfileClaimed).filter(SkillProfileClaimed.student_id == 'IT21013928').all()
print(f'Skills for IT21013928: {len(skills)}')
if len(skills) > 0:
    for s in skills[:10]:
        print(f'  {s.skill_name}: {s.claimed_score:.1f}')

db.close()
