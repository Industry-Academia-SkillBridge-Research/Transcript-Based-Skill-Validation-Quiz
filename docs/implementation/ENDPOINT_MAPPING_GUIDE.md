# Backend API Endpoint Update Guide

## Current Situation

The frontend explanation pages expect these endpoints:
- `GET /students/:studentId/skills/claimed` ✅ EXISTS
- `GET /students/:studentId/skills/claimed/:skillName/evidence` ❌ NEEDS CREATION
- `GET /students/:studentId/skills/parent` ❌ NEEDS MAPPING
- `GET /students/:studentId/skills/parent/:parentSkill/evidence` ❌ NEEDS MAPPING

## Existing Endpoints

Your backend already has similar endpoints with different paths:

### Child Skills (exists in `skills.py`)
- `GET /students/{student_id}/skills/claimed` ✅
- `GET /students/{student_id}/explain/skill/{skill_name}` ✅

### Parent Skills (exists in `parent_skills.py`)  
- `GET /students/{student_id}/skills/parents/claimed` ✅
- `GET /students/{student_id}/explain/parent-skill/{parent_skill}` ✅

## Solution Options

### Option 1: Update Frontend to Use Existing Endpoints (RECOMMENDED)

Update the explanation pages to use the existing backend endpoints:

**In ExplainChildSkillPage.jsx:**
```javascript
// Change from:
const evidenceRes = await fetch(`${API_BASE}/students/${studentId}/skills/claimed/${skillName}/evidence`);

// To:
const evidenceRes = await fetch(`${API_BASE}/students/${studentId}/explain/skill/${skillName}`);
```

**In ExplainParentSkillPage.jsx:**
```javascript
// Change from:
const skillRes = await fetch(`${API_BASE}/students/${studentId}/skills/parent`);
const evidenceRes = await fetch(`${API_BASE}/students/${studentId}/skills/parent/${parentSkill}/evidence`);

// To:
const skillRes = await fetch(`${API_BASE}/students/${studentId}/skills/parents/claimed`);
const evidenceRes = await fetch(`${API_BASE}/students/${studentId}/explain/parent-skill/${parentSkill}`);
```

### Option 2: Add Alias Routes in Backend

Add these alias routes to match the frontend expectations:

**In `backend/src/app/routes/skills.py`:**
```python
@router.get("/{student_id}/skills/claimed/{skill_name}/evidence")
def get_skill_evidence(
    student_id: str,
    skill_name: str,
    db: Session = Depends(get_db)
):
    """
    Alias for explain_skill that returns just the evidence array.
    """
    explanation = explain_skill(student_id, skill_name, db)
    return explanation["evidence"]
```

**In `backend/src/app/routes/parent_skills.py`:**
```python
@router.get("/{student_id}/skills/parent")
def get_parent_skills_alias(student_id: str, db: Session = Depends(get_db)):
    """
    Alias for get_parent_claimed_skills.
    """
    return get_parent_claimed_skills(student_id, db)


@router.get("/{student_id}/skills/parent/{parent_skill}/evidence")
def get_parent_skill_evidence(
    student_id: str,
    parent_skill: str,
    db: Session = Depends(get_db)
):
    """
    Alias for explain_parent_skill that returns just the evidence array.
    """
    explanation = explain_parent_skill(student_id, parent_skill, db)
    return explanation["evidence"]
```

## Recommended Approach

**Use Option 1** - Update the frontend to use existing endpoints.

This avoids backend changes and uses the already-tested endpoints.

## Implementation Steps

1. Update the fetch calls in both explanation pages
2. Update the response handling to match the existing API response format
3. Test the pages

## Data Format Differences

### Existing `/explain/skill/{skill_name}` Response:
```json
{
  "skill_summary": {
    "skill_name": "Python",
    "claimed_score": 85.5,
    "claimed_level": "Advanced",
    "confidence": 0.92
  },
  "evidence": [...]
}
```

### Expected by Frontend:
The frontend expects separate calls, so we need to adapt:
1. First call gets all skills
2. Second call gets the explanation with evidence
3. Extract skill from list and evidence from explanation

See the next file for the updated frontend code.
