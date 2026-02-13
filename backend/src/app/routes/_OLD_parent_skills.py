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
from app.services.job_skill_scoring import compute_job_skill_scores_for_student
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["Parent Skills"])


@router.get("/{student_id}/skills/parents/claimed")
def get_parent_claimed_skills(student_id: str, db: Session = Depends(get_db)):
    """
    Get all claimed parent skills for a student, including job skill aggregation.
    
    Computes parent skills by aggregating child skill evidence using the skill hierarchy.
    Also computes job skill scores by mapping child skills to canonical job skill tags.
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Dictionary with:
        - parent_skills: List of parent skills with scores (sorted by score desc)
        - job_skill_scores: List of {job_skill_id, job_skill_name, score, category}
        - job_skill_details: List of {job_skill_id, child_skill, contribution, map_weight}
        - mapping_stats: {total_job_skills, mapped_child_skills, total_child_skills}
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
    
    # Compute job skill scores
    try:
        job_skill_result = compute_job_skill_scores_for_student(student_id, db)
    except Exception as e:
        logger.error(f"Failed to compute job skills for student {student_id}: {e}")
        job_skill_result = {
            "job_skill_details": [],
            "mapping_stats": {"total_job_skills": 0, "mapped_child_skills": 0, "total_child_skills": 0}
        }
    
    return {
        "parent_skills": [ParentSkillOut.model_validate(ps) for ps in parent_skills],
        "job_skill_scores": job_skill_result["job_skill_details"],  # Array for frontend
        "job_skill_details": job_skill_result["job_skill_details"],
        "mapping_stats": job_skill_result["mapping_stats"]
    }


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
