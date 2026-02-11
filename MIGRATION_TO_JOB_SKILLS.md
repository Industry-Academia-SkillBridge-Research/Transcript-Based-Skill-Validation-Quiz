# Migration to Simplified Job Skills System

## Overview

Migrating from complex 3-level hierarchy (Child → Parent → Job Skills) to **direct Course → Job Skills** mapping.

## What's Changing

### OLD SYSTEM
```
Course → Child Skills (135) → Parent Skills (27) → Job Skills (65)
Example: IT1010 → "Procedural Programming Concepts" → "Programming & Development" → PYTHON
```

### NEW SYSTEM
```
Course → Job Skills (Direct)
Example: IT1010 → Python (0.5), Linux (0.2), Git (0.1)
```

## Benefits

✅ **Simpler**: Direct course-to-skill mapping  
✅ **Cleaner**: Industry-standard skill names (Python, SQL, AWS)  
✅ **Better Job Matching**: Skills align with job requirements  
✅ **Easier to Understand**: Students see familiar skill names  
✅ **Maintainable**: Easier to update mappings  

## Migration Steps

### Step 1: Backup Current Data
```powershell
# Backup database
Copy-Item backend\src\app.db backend\src\app.db.backup

# Backup old CSV
Copy-Item backend\data\course_skill_map.csv backend\data\course_skill_map.csv.old
```

### Step 2: Replace Mapping File
```powershell
# Copy new mapping to active location
Copy-Item backend\data\course_skill_mapping_new.csv backend\data\course_skill_map.csv -Force
```

### Step 3: Clear Old Skill Data
Run in backend:
```python
# Will create script: backend/scripts/clear_skill_data.py
```

### Step 4: Reseed Database
```bash
# POST http://localhost:8000/admin/seed-mapping
```

### Step 5: Recompute Student Skills
```bash
# POST http://localhost:8000/transcript/upload
# (Re-upload transcript for test student)
```

### Step 6: Verify Results
Check that skills now show as: Python, SQL, Java, etc.

## Files to Update

### ✅ No Changes Needed (Already Compatible)
- `backend/src/app/models/course.py` - CourseSkillMap model
- `backend/src/app/services/skill_scoring.py` - Works with any skill names
- `backend/src/app/services/seed_service.py` - Already expects (course_code, skill_name, map_weight)

### 🔄 Optional Simplifications
- `frontend/src/pages/SkillsPage.jsx` - Already shows skills (will just be simpler names)
- `backend/src/app/routes/skills.py` - Already returns skills (names will be different)

### ❌ Can Remove (No Longer Needed)
- `backend/data/parent_skills_unique.csv`
- `backend/data/child_skills_unique.csv`
- `backend/data/childskill_to_jobskill_map.csv`
- `backend/data/job_skills.csv`
- `backend/scripts/build_job_skill_maps.py`
- `backend/src/app/services/parent_skill_scoring.py`
- `backend/src/app/services/job_skill_scoring.py`

## Testing Checklist

- [ ] Upload transcript → Skills computed
- [ ] Skills display correctly (Python, SQL, etc.)
- [ ] Quiz generation works with new skills
- [ ] Results page shows new skill names
- [ ] Job recommendations work (if applicable)
- [ ] Explanation pages show evidence

## Rollback Plan

If issues occur:
```powershell
# Restore database
Copy-Item backend\src\app.db.backup backend\src\app.db -Force

# Restore old mapping
Copy-Item backend\data\course_skill_map.csv.old backend\data\course_skill_map.csv -Force

# Reseed
# POST http://localhost:8000/admin/seed-mapping
```

## Next Steps

1. **Test with sample student first**
2. **Verify all features work**
3. **Update documentation**
4. **Clean up unused files**
