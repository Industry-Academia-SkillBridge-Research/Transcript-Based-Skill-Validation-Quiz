# Quick Migration Guide 🚀

## Switch to New Job Skills Mapping in 3 Commands

Your new `course_skill_mapping_new.csv` maps courses directly to industry skills (Python, SQL, Java) instead of long child skill names.

### Prerequisites
- Backend server should be stopped
- Make sure you have `course_skill_mapping_new.csv` in `backend/data/`

### Option 1: Automated Migration (Recommended)

```powershell
cd backend
python scripts/migrate_to_job_skills.py
```

This script will:
- ✅ Backup your database and CSV files
- ✅ Replace the old mapping file
- ✅ Clear old skill data
- ✅ Reseed with new mappings
- ✅ Verify everything worked

### Option 2: Manual Migration

```powershell
# 1. Backup current data
Copy-Item backend\src\app.db backend\src\app.db.backup
Copy-Item backend\data\course_skill_map.csv backend\data\course_skill_map.csv.old

# 2. Replace with new mapping
Copy-Item backend\data\course_skill_mapping_new.csv backend\data\course_skill_map.csv -Force

# 3. Start backend and reseed
cd backend\src
& ..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

Then in browser: `POST http://localhost:8000/admin/seed-mapping`

Or use curl:
```powershell
curl -X POST http://localhost:8000/admin/seed-mapping
```

### Step 3: Recompute Skills

After migration, re-upload student transcripts to compute skills with new mapping:

1. Go to `http://localhost:5173/students/IT21013928/upload`
2. Upload the transcript again
3. Check skills - they should now show: Python, SQL, Java, etc.

### Verify Success

Visit skills page: `http://localhost:5173/students/IT21013928/skills`

✅ **You should see simple skill names like:**
- Python
- SQL  
- Java
- Linux
- Git
- AWS
etc.

❌ **NOT long names like:**
- "Procedural Programming Concepts"
- "Schema Refinement & Normalization"

### Rollback (If Needed)

```powershell
# Restore database
Copy-Item backend\src\app.db.backup backend\src\app.db -Force

# Restore old CSV
Copy-Item backend\data\course_skill_map.csv.old backend\data\course_skill_map.csv -Force

# Restart backend and reseed
```

### What Changed?

**Before:**
```
IT1010 → "Procedural Programming Concepts" (0.2)
IT1010 → "Control Structures & Loops" (0.2)
IT1010 → "Functions & Recursion" (0.2)
...
```

**After:**
```
IT1010 → C Programming (0.5)
IT1010 → Linux (0.2)
IT1010 → Unit Testing (0.15)
IT1010 → Git (0.1)
IT1010 → CI/CD (0.05)
```

### Benefits

✅ Cleaner skill names  
✅ Better for job matching  
✅ Easier to understand  
✅ Industry-standard terminology  
✅ Direct course-to-skill mapping  

---

**Questions?** Check `MIGRATION_TO_JOB_SKILLS.md` for detailed information.
