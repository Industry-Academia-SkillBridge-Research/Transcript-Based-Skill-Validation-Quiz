"""
XAI (Explainable AI) service for skill score explanations.

Provides transparency into how skill scores are calculated using:
1. Course-level contribution breakdowns
2. Evidence weight analysis
3. SHAP-based feature importance (for role recommendations)
"""

import logging
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.skill import SkillEvidence, SkillEvidenceParent, SkillProfileParentClaimed
from app.models.course import CourseTaken

logger = logging.getLogger(__name__)


def get_skill_explanation(
    db: Session, 
    student_id: str, 
    skill_name: str,
    skill_type: str = "parent"
) -> Dict:
    """
    Get detailed explanation of how a skill score was calculated.
    
    Args:
        db: Database session
        student_id: Student ID
        skill_name: Name of the skill (parent or child)
        skill_type: "parent" or "child"
        
    Returns:
        Dictionary with explanation details
    """
    if skill_type == "parent":
        return _explain_parent_skill(db, student_id, skill_name)
    else:
        return _explain_child_skill(db, student_id, skill_name)


def _explain_parent_skill(db: Session, student_id: str, parent_skill: str) -> Dict:
    """
    Explain how a parent skill score was calculated.
    
    Returns breakdown by:
    - Contributing child skills
    - Course evidence
    - Contribution weights
    """
    # Get parent skill profile
    profile = db.query(SkillProfileParentClaimed).filter_by(
        student_id=student_id,
        parent_skill=parent_skill
    ).first()
    
    if not profile:
        return {
            "error": f"No profile found for parent skill: {parent_skill}",
            "skill_name": parent_skill,
            "skill_type": "parent"
        }
    
    # Get all evidence contributing to this parent skill
    evidence_rows = db.query(SkillEvidenceParent).filter_by(
        student_id=student_id,
        parent_skill=parent_skill
    ).all()
    
    # Group by child skill
    child_skill_contributions = {}
    course_contributions = []
    
    total_contribution = 0.0
    total_weight = 0.0
    
    for evidence in evidence_rows:
        child_skill = evidence.child_skill
        
        # Aggregate by child skill
        if child_skill not in child_skill_contributions:
            child_skill_contributions[child_skill] = {
                "child_skill": child_skill,
                "total_contribution": 0.0,
                "total_weight": 0.0,
                "course_count": 0,
                "courses": []
            }
        
        child_skill_contributions[child_skill]["total_contribution"] += evidence.contribution
        child_skill_contributions[child_skill]["total_weight"] += evidence.evidence_weight
        child_skill_contributions[child_skill]["course_count"] += 1
        child_skill_contributions[child_skill]["courses"].append({
            "course_code": evidence.course_code,
            "contribution": round(evidence.contribution, 4),
            "weight": round(evidence.evidence_weight, 4),
            "grade": evidence.grade,
            "credits": evidence.credits,
            "recency": round(evidence.recency, 4),
            "map_weight": round(evidence.map_weight, 4)
        })
        
        # Track overall totals
        total_contribution += evidence.contribution
        total_weight += evidence.evidence_weight
        
        # Add to course-level breakdown
        course_contributions.append({
            "course_code": evidence.course_code,
            "child_skill": child_skill,
            "contribution": round(evidence.contribution, 4),
            "weight": round(evidence.evidence_weight, 4),
            "grade": evidence.grade,
            "credits": evidence.credits,
            "recency": round(evidence.recency, 4),
            "map_weight": round(evidence.map_weight, 4)
        })
    
    # Calculate percentage contribution for each child skill
    child_skills_list = []
    for child_data in child_skill_contributions.values():
        contribution_pct = (child_data["total_contribution"] / total_contribution * 100) if total_contribution > 0 else 0
        weight_pct = (child_data["total_weight"] / total_weight * 100) if total_weight > 0 else 0
        
        child_skills_list.append({
            "child_skill": child_data["child_skill"],
            "contribution": round(child_data["total_contribution"], 4),
            "contribution_percentage": round(contribution_pct, 2),
            "weight": round(child_data["total_weight"], 4),
            "weight_percentage": round(weight_pct, 2),
            "course_count": child_data["course_count"],
            "courses": child_data["courses"]
        })
    
    # Sort by contribution descending
    child_skills_list.sort(key=lambda x: x["contribution"], reverse=True)
    course_contributions.sort(key=lambda x: x["contribution"], reverse=True)
    
    return {
        "skill_name": parent_skill,
        "skill_type": "parent",
        "score": round(profile.parent_score, 2),
        "level": profile.parent_level,
        "confidence": round(profile.confidence, 4),
        "calculation": {
            "total_contribution": round(total_contribution, 4),
            "total_weight": round(total_weight, 4),
            "formula": "score = 100 * (total_contribution / total_weight)",
            "confidence_formula": "confidence = 1 - exp(-0.25 * total_weight)"
        },
        "child_skills": child_skills_list,
        "course_breakdown": course_contributions,
        "summary": {
            "total_courses": len(evidence_rows),
            "unique_child_skills": len(child_skill_contributions),
            "strongest_contributor": child_skills_list[0]["child_skill"] if child_skills_list else None
        }
    }


def _explain_child_skill(db: Session, student_id: str, child_skill: str) -> Dict:
    """
    Explain how a child skill score was calculated.
    
    Returns breakdown by:
    - Contributing courses
    - Grade impact
    - Recency impact
    - Mapping weights
    """
    # Get all evidence for this child skill
    evidence_rows = db.query(SkillEvidence).filter_by(
        student_id=student_id,
        child_skill=child_skill
    ).all()
    
    if not evidence_rows:
        return {
            "error": f"No evidence found for child skill: {child_skill}",
            "skill_name": child_skill,
            "skill_type": "child"
        }
    
    # Build course breakdown
    course_contributions = []
    total_contribution = 0.0
    total_weight = 0.0
    
    for evidence in evidence_rows:
        total_contribution += evidence.contribution
        total_weight += evidence.evidence_weight
        
        course_contributions.append({
            "course_code": evidence.course_code,
            "contribution": round(evidence.contribution, 4),
            "weight": round(evidence.evidence_weight, 4),
            "grade": evidence.grade,
            "grade_points": round(evidence.grade_points, 2),
            "credits": evidence.credits,
            "recency": round(evidence.recency, 4),
            "map_weight": round(evidence.map_weight, 4),
            "components": {
                "base_contribution": f"{evidence.credits} credits × {evidence.map_weight} map_weight",
                "grade_multiplier": f"× {evidence.grade_points}/4.0 (grade: {evidence.grade})",
                "recency_factor": f"× {round(evidence.recency, 4)} (time decay)",
                "final_contribution": round(evidence.contribution, 4)
            }
        })
    
    # Sort by contribution
    course_contributions.sort(key=lambda x: x["contribution"], reverse=True)
    
    # Calculate final score
    child_score = (total_contribution / total_weight * 100) if total_weight > 0 else 0
    
    return {
        "skill_name": child_skill,
        "skill_type": "child",
        "score": round(child_score, 2),
        "calculation": {
            "total_contribution": round(total_contribution, 4),
            "total_weight": round(total_weight, 4),
            "formula": "contribution = credits × map_weight × (grade_points/4.0) × recency_factor",
            "final_formula": "score = 100 × (total_contribution / total_weight)"
        },
        "course_breakdown": course_contributions,
        "summary": {
            "total_courses": len(evidence_rows),
            "top_contributor": course_contributions[0]["course_code"] if course_contributions else None,
            "top_contribution_percentage": round(course_contributions[0]["contribution"] / total_contribution * 100, 2) if course_contributions and total_contribution > 0 else 0
        }
    }


def get_all_skills_summary(db: Session, student_id: str) -> Dict:
    """
    Get summary of all parent skills with brief explanations.
    
    Returns:
        Dictionary with all parent skills and their key contributors
    """
    parent_profiles = db.query(SkillProfileParentClaimed).filter_by(
        student_id=student_id
    ).all()
    
    if not parent_profiles:
        return {
            "student_id": student_id,
            "parent_skills": [],
            "total_count": 0
        }
    
    skills_summary = []
    
    for profile in parent_profiles:
        # Get top 3 child skill contributors
        evidence_rows = db.query(
            SkillEvidenceParent.child_skill,
            func.sum(SkillEvidenceParent.contribution).label("total_contribution"),
            func.count(SkillEvidenceParent.course_code).label("course_count")
        ).filter_by(
            student_id=student_id,
            parent_skill=profile.parent_skill
        ).group_by(
            SkillEvidenceParent.child_skill
        ).order_by(
            func.sum(SkillEvidenceParent.contribution).desc()
        ).limit(3).all()
        
        top_contributors = [
            {
                "child_skill": row.child_skill,
                "contribution": round(row.total_contribution, 2),
                "course_count": row.course_count
            }
            for row in evidence_rows
        ]
        
        skills_summary.append({
            "parent_skill": profile.parent_skill,
            "score": round(profile.parent_score, 2),
            "level": profile.parent_level,
            "confidence": round(profile.confidence, 4),
            "top_contributors": top_contributors
        })
    
    # Sort by score descending
    skills_summary.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "student_id": student_id,
        "parent_skills": skills_summary,
        "total_count": len(skills_summary)
    }
