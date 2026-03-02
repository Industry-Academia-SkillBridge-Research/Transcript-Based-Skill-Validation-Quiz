# Migration to Flat Skill Structure

## Overview
Migrating from parent/child skill hierarchy to flat skill structure using direct course-skill mappings.

## What's Being Removed

### Old CSV Files:
- `childskill_to_jobskill_map.csv`
- `job_skill_to_parent_skill.csv`
- `job_parent_skill_features.csv`

### Old Database Tables:
- `skill_group_map` (parent-child mappings)
- `skill_profile_parent_claimed` (parent skill claims)
- `skill_profile_verified_parent` (parent skill verified)
- `skill_profile_final_parent` (parent skill finals)
- `skill_evidence_parent` (parent skill evidence)
- `student_skill_portfolio` (will be recreated with new structure)

### Old Model Files:
- `skill_group_map.py` - DELETE
- `skill_profile_verified_parent.py` - DELETE
- `skill_profile_final_parent.py` - DELETE

## New Structure

### New CSV (Already Exists):
- `course_skill_map.csv` - Direct course to skill mapping with weights

### New Database Tables:
- `course_skill_map` - Stores course-skill mappings
- `skill_evidence` - Direct skill evidence from courses (no parent)
- `skill_profile_claimed` - Student skill profiles
- `student_skill_portfolio` - Simplified portfolio (skill_name only)

### Skills are now flat:
- SQL, Python, Java, C++, JavaScript, etc.
- No parent/child hierarchy
- Direct mapping from courses

## Migration Steps
1. Backup existing database
2. Delete old CSV files
3. Drop old tables
4. Update models
5. Update services
6. Reload data from new course_skill_map.csv
7. Recompute skill profiles from transcripts
