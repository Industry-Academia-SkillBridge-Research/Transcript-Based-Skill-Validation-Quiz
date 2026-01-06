"""
Parent Skills API routes for aggregated parent skill profiles and explainability.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.skill import SkillProfileParentClaimed, SkillEvidenceParent
from app.schemas.skill import ParentSkillOut, ParentSkillEvidenceOut
from app.services.parent_skill_scoring import compute_parent_claimed_skills
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["Parent Skills"])


@router.get("/{student_id}/skills/parents/claimed", response_model=List[ParentSkillOut])
def get_parent_claimed_skills(student_id: str, db: Session = Depends(get_db)):
    """
    Get all claimed parent skills for a student.
    
    Computes parent skills by aggregating child skill evidence using the skill hierarchy.
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        List of parent skills with scores and confidence, sorted by score descending
    """
    result = compute_parent_claimed_skills(student_id, db)
    
    if result["parent_skills_computed"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No parent skills computed for student {student_id}. "
                   f"Ensure child skills exist and skill hierarchy is seeded."
        )
    
    # Query the actual database objects for proper serialization
    parent_skills = db.query(SkillProfileParentClaimed).filter(
        SkillProfileParentClaimed.student_id == student_id
    ).order_by(SkillProfileParentClaimed.parent_score.desc()).all()
    
    return parent_skills


@router.get("/{student_id}/explain/parent-skill/{parent_skill}")
def explain_parent_skill(
    student_id: str,
    parent_skill: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed evidence breakdown for a specific parent skill.
    
    Shows parent skill summary and all child skills + courses that contributed,
    sorted by contribution (highest first).
    
    Args:
        student_id: Student identifier
        parent_skill: Name of the parent skill to explain
        db: Database session
        
    Returns:
        Dictionary with parent skill summary and evidence list
    """
    # Fetch parent skill summary
    parent_summary = db.query(SkillProfileParentClaimed).filter(
        SkillProfileParentClaimed.student_id == student_id,
        SkillProfileParentClaimed.parent_skill == parent_skill
    ).first()
    
    if not parent_summary:
        raise HTTPException(
            status_code=404,
            detail=f"Parent skill '{parent_skill}' not found for student {student_id}"
        )
    
    # Fetch evidence sorted by contribution descending
    evidence = db.query(SkillEvidenceParent).filter(
        SkillEvidenceParent.student_id == student_id,
        SkillEvidenceParent.parent_skill == parent_skill
    ).order_by(SkillEvidenceParent.contribution.desc()).all()
    
    return {
        "parent_summary": ParentSkillOut.model_validate(parent_summary),
        "evidence": [ParentSkillEvidenceOut.model_validate(e) for e in evidence]
    }
