# 🗑️ Unwanted Files - Safe to Delete

## Overview
These files are **legacy artifacts, one-time migration scripts, redundant documentation, or backup files** that are no longer needed for the active working system.

**Created:** February 12, 2026  
**System Status:** Job Skills (65) is the PRIMARY and ONLY active system

---

## ❌ SAFE TO DELETE

### 📊 **Legacy Data Files** (backend/data/)

```
❌ child_skills_unique.csv              # Old child skills list (135 skills)
❌ parent_skills_unique.csv             # Old parent skills list (27 skills)
❌ skill_group_map.csv                  # Legacy skill grouping hierarchy
❌ course_skill_mapping.csv             # Old mapping format (before job skills)
❌ course_skill_mapping_new.csv         # Intermediate migration file
```

**Why Delete:** These were part of the old 3-tier hierarchy (Child → Parent → Job). The current system uses **direct course-to-job-skill mapping** via `course_skill_map.csv`.

---

### 💾 **Backup Files**

```
❌ backend/src/app.db.backup_20260209_114450          # Database backup
❌ backend/data/course_skill_map.csv.backup_20260209_114452  # CSV backup
```

**Why Delete:** One-time migration backups from February 9, 2026. Keep only if you want historical reference, otherwise safe to remove.

---

### 🔧 **One-Time Migration Scripts** (backend/scripts/)

```
❌ migrate_to_job_skills.py            # Migration script (already executed)
❌ test_job_skill_support.py           # Testing script for migration
❌ test_export.py                      # Testing script for exports
```

**Why Delete:** These were used once to migrate from child/parent skills to job skills. Migration is complete - scripts no longer needed.

---

### 📝 **Redundant Documentation Files** (Project Root)

#### Migration-Related Docs (Migration Complete)
```
❌ MIGRATION_TO_JOB_SKILLS.md          # Migration guide (task complete)
❌ QUICK_MIGRATION.md                  # Quick migration steps (task complete)
```

#### Duplicate/Interim Documentation
```
❌ README_QUICK_START.md               # Duplicate of README.md content
❌ READY_TO_TEST.md                    # Testing checklist (feature complete)
❌ QUIZ_QUICK_REF.md                   # Redundant (covered in QUIZ_WORKFLOW_GUIDE.md)
❌ SKILL_SCORING_QUICK_REF.md          # Redundant (covered in SKILL_SCORING_ALGORITHM.md)
❌ QUIZ_IMPLEMENTATION_SUMMARY.md      # Redundant (covered in COMPLETE_PROJECT_DOCUMENTATION.md)
❌ PROJECT_OVERVIEW_FOR_SUPERVISOR.md  # Redundant (covered in COMPLETE_PROJECT_DOCUMENTATION.md)
❌ VIVA_EXPLANATION.md                 # Presentation-specific (archive if needed)
❌ SKILL_SCORING_VIVA_SLIDES.md        # Presentation-specific (archive if needed)
```

**Why Delete:** Either migration-related (tasks completed) or content duplicated in comprehensive docs like `COMPLETE_PROJECT_DOCUMENTATION.md` and `ACTIVE_WORKING_FILES.md`.

---

### 📓 **Jupyter Notebooks** (backend/notebooks/)

```
❌ clean_job_data.ipynb                # One-time data cleaning notebook
```

**Why Delete:** Used once to clean job data. Job_data.csv is already cleaned and in use.

---

### 📤 **Debug/Output Files** (backend/output/)

```
❌ debug_extracted_text_IT21013928.txt  # Debug output from transcript parsing
```

**Why Delete:** Temporary debug file. Safe to delete or clear output folder entirely.

---

### 🔧 **Additional Backend Files to Review**

```
⚠️ backend/src/app/models/skill_group_map.py  # Model for legacy skill_group_map.csv
⚠️ backend/src/app/migrate_student_table.py   # One-time migration script
⚠️ backend/add_specialization_column.py       # One-time database update script
⚠️ backend/fix_db.py                          # One-time database fix script
⚠️ backend/test_job_skills.py                 # Testing script
⚠️ backend/test_parent_skills.py              # Testing script
```

**Review Before Deleting:** These may have been one-time scripts. Check if still needed:
- If `skill_group_map` model isn't referenced in active routes/services → DELETE
- If migration scripts already executed → DELETE
- Testing scripts → KEEP if you use them, DELETE if obsolete

---

## ✅ KEEP - ACTIVE DOCUMENTATION

### Essential Docs (Keep These)
```
✅ COMPLETE_PROJECT_DOCUMENTATION.md   # Master documentation (2300+ lines)
✅ ACTIVE_WORKING_FILES.md             # This workflow guide
✅ README.md                           # Quick start guide
✅ SKILL_SCORING_ALGORITHM.md          # Core algorithm details
✅ QUIZ_WORKFLOW_GUIDE.md              # Quiz implementation guide
✅ JOB_SKILL_IMPLEMENTATION.md         # Job skills feature documentation
✅ VISUAL_SUMMARY.md                   # Architecture diagrams
✅ READY_TO_USE.md                     # Production checklist
✅ MODEL_TRAINING_README.md            # ML model documentation
```

### Backend Docs (Keep These)
```
✅ backend/ENDPOINT_MAPPING_GUIDE.md
✅ backend/GENERATE_AND_EXPORT_API.md
✅ backend/EXPORT_QUESTION_BANK_GUIDE.md
```

### Frontend Docs (Keep These)
```
✅ frontend/FRONTEND_README.md
✅ frontend/AUTHENTICATION_GUIDE.md
✅ frontend/EXPLANATION_PAGES_GUIDE.md
```

### Utility Scripts (Keep These)
```
✅ start.ps1                           # Start both servers
✅ stop.ps1                            # Stop servers
```

---

## 🛠️ How to Clean Up

### Option 1: Manual Deletion (Safer)

Review each file individually:

```powershell
# Navigate to project root
cd "D:\OneDrive\OneDrive - Sri Lanka Institute of Information Technology\Research\Transcript-Based-Skill-Validation-Quiz\Transcript-Based-Skill-Validation-Quiz"

# Delete legacy data files
Remove-Item "backend\data\child_skills_unique.csv"
Remove-Item "backend\data\parent_skills_unique.csv"
Remove-Item "backend\data\skill_group_map.csv"
Remove-Item "backend\data\course_skill_mapping.csv"
Remove-Item "backend\data\course_skill_mapping_new.csv"

# Delete backup files
Remove-Item "backend\src\app.db.backup_20260209_114450"
Remove-Item "backend\data\course_skill_map.csv.backup_20260209_114452"

# Delete migration scripts
Remove-Item "backend\scripts\migrate_to_job_skills.py"
Remove-Item "backend\scripts\test_job_skill_support.py"
Remove-Item "backend\scripts\test_export.py"

# Delete redundant documentation
Remove-Item "MIGRATION_TO_JOB_SKILLS.md"
Remove-Item "QUICK_MIGRATION.md"
Remove-Item "README_QUICK_START.md"
Remove-Item "READY_TO_TEST.md"
Remove-Item "QUIZ_QUICK_REF.md"
Remove-Item "SKILL_SCORING_QUICK_REF.md"
Remove-Item "QUIZ_IMPLEMENTATION_SUMMARY.md"
Remove-Item "PROJECT_OVERVIEW_FOR_SUPERVISOR.md"
Remove-Item "VIVA_EXPLANATION.md"
Remove-Item "SKILL_SCORING_VIVA_SLIDES.md"

# Delete notebooks and output
Remove-Item "backend\notebooks\clean_job_data.ipynb"
Remove-Item "backend\output\debug_extracted_text_IT21013928.txt"

# Delete one-time backend scripts
Remove-Item "backend\add_specialization_column.py"
Remove-Item "backend\fix_db.py"
Remove-Item "backend\test_job_skills.py"
Remove-Item "backend\test_parent_skills.py"
Remove-Item "backend\src\app\migrate_student_table.py"
```

---

### Option 2: Create Archive (Safest)

Move files to archive folder instead of deleting:

```powershell
# Create archive directory
New-Item -ItemType Directory -Path ".\ARCHIVE_2026_02_12" -Force

# Move legacy files
Move-Item "backend\data\child_skills_unique.csv" ".\ARCHIVE_2026_02_12\"
Move-Item "backend\data\parent_skills_unique.csv" ".\ARCHIVE_2026_02_12\"
# ... etc for all files
```

---

### Option 3: Bulk Cleanup Script

Create a PowerShell script `cleanup.ps1`:

```powershell
# Cleanup Script - Remove Legacy Files
Write-Host "🗑️ Cleaning up legacy files..." -ForegroundColor Yellow

$filesToDelete = @(
    "backend\data\child_skills_unique.csv",
    "backend\data\parent_skills_unique.csv",
    "backend\data\skill_group_map.csv",
    "backend\data\course_skill_mapping.csv",
    "backend\data\course_skill_mapping_new.csv",
    "backend\src\app.db.backup_20260209_114450",
    "backend\data\course_skill_map.csv.backup_20260209_114452",
    "backend\scripts\migrate_to_job_skills.py",
    "backend\scripts\test_job_skill_support.py",
    "backend\scripts\test_export.py",
    "MIGRATION_TO_JOB_SKILLS.md",
    "QUICK_MIGRATION.md",
    "README_QUICK_START.md",
    "READY_TO_TEST.md",
    "QUIZ_QUICK_REF.md",
    "SKILL_SCORING_QUICK_REF.md",
    "QUIZ_IMPLEMENTATION_SUMMARY.md",
    "PROJECT_OVERVIEW_FOR_SUPERVISOR.md",
    "VIVA_EXPLANATION.md",
    "SKILL_SCORING_VIVA_SLIDES.md",
    "backend\notebooks\clean_job_data.ipynb",
    "backend\output\debug_extracted_text_IT21013928.txt",
    "backend\add_specialization_column.py",
    "backend\fix_db.py",
    "backend\test_job_skills.py",
    "backend\test_parent_skills.py",
    "backend\src\app\migrate_student_table.py"
)

$deletedCount = 0
foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "✅ Deleted: $file" -ForegroundColor Green
        $deletedCount++
    } else {
        Write-Host "⚠️  Not found: $file" -ForegroundColor Gray
    }
}

Write-Host "`n✅ Cleanup complete! Deleted $deletedCount files." -ForegroundColor Green
Write-Host "💡 Run git status to review changes before committing." -ForegroundColor Cyan
```

Run with:
```powershell
.\cleanup.ps1
```

---

## 📊 Summary

### Files to Delete
- **Legacy Data Files:** 5 CSV files
- **Backup Files:** 2 files
- **Migration Scripts:** 3 Python files
- **Redundant Documentation:** 10 markdown files
- **Notebooks/Output:** 2 files
- **One-time Backend Scripts:** 5 Python files

**Total:** ~27 files can be safely removed

---

## ⚠️ Important Notes

1. **Backup First:** Even though these are "unwanted," consider creating a git commit or archive before deletion
2. **Test After Cleanup:** Run your application after deletion to ensure nothing breaks
3. **Review File by File:** If unsure about a specific file, keep it until you're certain
4. **Update .gitignore:** Add common backup/temp patterns to prevent future clutter

---

## 🔍 Verification After Cleanup

After deleting files, verify the system still works:

```powershell
# Start backend
cd backend\src
python -m uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev

# Test workflow:
# 1. Upload transcript
# 2. View job skills
# 3. Generate quiz
# 4. Submit quiz
# 5. View results
```

If everything works → ✅ Cleanup successful!

---

**Last Updated:** February 12, 2026  
**System:** Job Skills (65 tags) - Direct Mapping ONLY
