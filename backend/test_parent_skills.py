import sys
sys.path.insert(0, 'src')

from app.db import SessionLocal
from app.services.parent_skill_scoring import compute_parent_claimed_skills

db = SessionLocal()
try:
    result = compute_parent_claimed_skills("IT21013928", db)
    print("Success!")
    print(f"Parent skills computed: {result['parent_skills_computed']}")
    print(f"Evidence rows: {result['parent_evidence_rows']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
