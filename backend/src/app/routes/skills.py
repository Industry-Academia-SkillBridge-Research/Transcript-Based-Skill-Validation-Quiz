"""
Skills API routes for claimed skills and explainability.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.skill import SkillProfileClaimed, SkillEvidence
from app.schemas.skill import ClaimedSkillOut, SkillEvidenceOut
from app.services.skill_scoring import compute_claimed_skills
from app.services.job_skill_scoring import compute_job_skill_scores_for_student
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["Skills"])


@router.get("/{student_id}/skills/claimed")
def get_claimed_skills(student_id: str, db: Session = Depends(get_db)):
    """
    Get all claimed skills for a student.
    
    Computes skills on-the-fly from transcript data.
    Supports both:
    - New system: Direct job skills (from course_skill_mapping_new.csv)
    - Old system: Child skills + Job skills aggregation
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Dictionary with:
        - claimed_skills: List of skills with scores
        - job_skill_scores: List for frontend display (compatible format)
    """
    # Compute child skills (existing logic)
    result = compute_claimed_skills(student_id, db)
    
    if result["skills_computed"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No courses or skill mappings found for student {student_id}"
        )
    
    # Try job skills computation (old system)
    child_skill_scores = {
        skill['skill_name']: skill['claimed_score']
        for skill in result["claimed_skills"]
    }
    
    try:
        job_skills_result = compute_job_skill_scores_for_student(student_id, db)
        # Old system: has job_skill_details from aggregation
        if job_skills_result.get("job_skill_details"):
            result["job_skill_scores"] = job_skills_result["job_skill_details"]
            result["job_skill_details"] = job_skills_result["job_skill_details"]
            result["mapping_stats"] = job_skills_result["mapping_stats"]
        else:
            # New system: claimed_skills ARE job skills (no aggregation needed)
            result["job_skill_scores"] = [
                {
                    "job_skill_name": skill["skill_name"],
                    "job_skill_id": skill["skill_name"].upper().replace(" ", "_"),
                    "score": skill["claimed_score"],
                    "category": "General",  # Could be enhanced with category lookup
                    "level": "Advanced" if skill["claimed_score"] >= 80 else "Intermediate" if skill["claimed_score"] >= 60 else "Beginner"
                }
                for skill in result["claimed_skills"]
            ]
    except Exception as e:
        logger.warning(f"Job skills computation failed, using claimed skills directly: {e}")
        # Fallback: treat claimed_skills as job skills
        result["job_skill_scores"] = [
            {
                "job_skill_name": skill["skill_name"],
                "job_skill_id": skill["skill_name"].upper().replace(" ", "_"),
                "score": skill["claimed_score"],
                "category": "General",
                "level": "Advanced" if skill["claimed_score"] >= 80 else "Intermediate" if skill["claimed_score"] >= 60 else "Beginner"
            }
            for skill in result["claimed_skills"]
        ]
    
    return result


@router.get("/{student_id}/explain/skill/{skill_name}")
def explain_skill(
    student_id: str,
    skill_name: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed evidence breakdown for a specific skill.
    
    Shows skill summary and all courses that contributed to the skill score,
    sorted by contribution (highest first).
    
    Args:
        student_id: Student identifier
        skill_name: Name of the skill to explain
        db: Database session
        
    Returns:
        Dictionary with skill summary and evidence list
    """
    # Fetch skill summary
    skill_summary = db.query(SkillProfileClaimed).filter(
        SkillProfileClaimed.student_id == student_id,
        SkillProfileClaimed.skill_name == skill_name
    ).first()
    
    if not skill_summary:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found for student {student_id}"
        )
    
    # Fetch evidence sorted by contribution descending
    evidence = db.query(SkillEvidence).filter(
        SkillEvidence.student_id == student_id,
        SkillEvidence.skill_name == skill_name
    ).order_by(SkillEvidence.contribution.desc()).all()
    
    return {
        "skill_summary": {
            "skill_name": skill_summary.skill_name,
            "claimed_score": skill_summary.claimed_score,
            "claimed_level": skill_summary.claimed_level,
            "confidence": skill_summary.confidence
        },
        "evidence": [
            {
                "course_code": e.course_code,
                "grade": e.grade,
                "credits": e.credits,
                "map_weight": e.map_weight,
                "academic_year": e.academic_year,
                "recency": e.recency,
                "contribution": e.contribution
            }
            for e in evidence
        ]
    }


@router.post("/{student_id}/skills/recompute")
def recompute_skills(student_id: str, db: Session = Depends(get_db)):
    """
    Force recomputation of claimed skills for a student.
    
    Useful after transcript updates.
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Computation summary
    """
    result = compute_claimed_skills(student_id, db)
    
    if result["skills_computed"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No courses or skill mappings found for student {student_id}"
        )
    
    return {
        "status": "ok",
        "message": f"Recomputed skills for student {student_id}",
        **result
    }
