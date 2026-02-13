"""
Parent skill scoring service.

Aggregates child skill evidence into parent skill profiles using the skill hierarchy graph.
"""

import logging
from datetime import datetime
from typing import Dict, List, Set
from math import exp
from sqlalchemy.orm import Session
from app.models.skill import SkillEvidence, SkillProfileParentClaimed, SkillEvidenceParent
from app.models.skill_group_map import SkillGroupMap
from app.services.skill_scoring import compute_claimed_skills

logger = logging.getLogger(__name__)

CONFIDENCE_FACTOR = 0.25


def determine_parent_skill_level(score: float) -> str:
    """
    Determine parent skill level based on score.
    
    Args:
        score: Parent skill score (0-100)
        
    Returns:
        Skill level: Beginner, Intermediate, or Advanced
    """
    if score < 50:
        return "Beginner"
    elif score < 75:
        return "Intermediate"
    else:
        return "Advanced"


def load_skill_hierarchy(db: Session) -> Dict[str, Set[str]]:
    """
    Load skill hierarchy from SkillGroupMap.
    
    Returns:
        Dictionary mapping parent_skill -> set of child_skills
    """
    mappings = db.query(SkillGroupMap).all()
    
    hierarchy = {}
    for mapping in mappings:
        parent = mapping.parent_skill
        child = mapping.child_skill
        
        if parent not in hierarchy:
            hierarchy[parent] = set()
        hierarchy[parent].add(child)
    
    logger.debug(f"Loaded skill hierarchy with {len(hierarchy)} parent skills")
    return hierarchy


def compute_parent_claimed_skills(student_id: str, db: Session) -> Dict:
    """
    Compute parent (aggregate) claimed skills for a student based on child skill evidence.
    
    Process:
    1. Ensure child skills are computed (compute or read SkillEvidence)
    2. Load skill hierarchy (parent -> children mapping)
    3. Aggregate child evidence into parent evidence
    4. Compute parent_score, confidence, parent_level
    5. Store in SkillProfileParentClaimed and SkillEvidenceParent
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Dictionary with computation summary and parent skills list
    """
    logger.info(f"Computing parent claimed skills for student: {student_id}")
    
    # Step 1: Ensure child skills are computed
    child_evidence = db.query(SkillEvidence).filter(
        SkillEvidence.student_id == student_id
    ).all()
    
    if not child_evidence:
        logger.info(f"No child evidence found, computing child skills first...")
        result = compute_claimed_skills(student_id, db)
        
        if result["skills_computed"] == 0:
            logger.warning(f"No child skills computed for student: {student_id}")
            return {
                "student_id": student_id,
                "parent_skills_computed": 0,
                "parent_evidence_rows": 0,
                "parent_skills": []
            }
        
        # Fetch child evidence again
        child_evidence = db.query(SkillEvidence).filter(
            SkillEvidence.student_id == student_id
        ).all()
    
    logger.debug(f"Found {len(child_evidence)} child evidence rows")
    
    # Step 2: Load skill hierarchy
    skill_hierarchy = load_skill_hierarchy(db)
    
    if not skill_hierarchy:
        logger.warning("No skill hierarchy found in SkillGroupMap")
        return {
            "student_id": student_id,
            "parent_skills_computed": 0,
            "parent_evidence_rows": 0,
            "parent_skills": []
        }
    
    # Step 3: Clear existing parent skills and evidence for this student
    db.query(SkillProfileParentClaimed).filter(
        SkillProfileParentClaimed.student_id == student_id
    ).delete()
    
    db.query(SkillEvidenceParent).filter(
        SkillEvidenceParent.student_id == student_id
    ).delete()
    
    db.flush()
    
    # Step 4: Aggregate child evidence into parent evidence
    parent_aggregates = {}
    parent_evidence_rows = []
    
    for evidence in child_evidence:
        child_skill = evidence.skill_name
        
        # Find all parent skills for this child skill
        for parent_skill, children in skill_hierarchy.items():
            if child_skill in children:
                # This child skill belongs to this parent skill
                
                if parent_skill not in parent_aggregates:
                    parent_aggregates[parent_skill] = {
                        "total_contribution": 0.0,
                        "total_evidence_weight": 0.0
                    }
                
                # Accumulate contribution and evidence weight
                parent_aggregates[parent_skill]["total_contribution"] += evidence.contribution
                parent_aggregates[parent_skill]["total_evidence_weight"] += evidence.evidence_weight
                
                # Store parent evidence row for explainability
                parent_evidence_rows.append({
                    "student_id": student_id,
                    "parent_skill": parent_skill,
                    "child_skill": child_skill,
                    "course_code": evidence.course_code,
                    "contribution": evidence.contribution,
                    "evidence_weight": evidence.evidence_weight,
                    "recency": evidence.recency,
                    "grade": evidence.grade,
                    "credits": evidence.credits,
                    "map_weight": evidence.map_weight
                })
    
    if not parent_aggregates:
        logger.warning(f"No parent skills mapped for student: {student_id}")
        return {
            "student_id": student_id,
            "parent_skills_computed": 0,
            "parent_evidence_rows": 0,
            "parent_skills": []
        }
    
    # Step 5: Compute parent scores and insert
    parent_skills_computed = 0
    parent_skills_list = []
    
    for parent_skill, aggregates in parent_aggregates.items():
        total_contribution = aggregates["total_contribution"]
        total_evidence_weight = aggregates["total_evidence_weight"]
        
        if total_evidence_weight == 0:
            logger.warning(f"Zero evidence weight for parent skill: {parent_skill}")
            continue
        
        # Compute parent score
        parent_score = 100 * (total_contribution / total_evidence_weight)
        
        # Compute confidence
        confidence = 1 - exp(-CONFIDENCE_FACTOR * total_evidence_weight)
        
        # Determine parent level
        parent_level = determine_parent_skill_level(parent_score)
        
        # Store in SkillProfileParentClaimed
        parent_profile = SkillProfileParentClaimed(
            student_id=student_id,
            parent_skill=parent_skill,
            parent_score=parent_score,
            parent_level=parent_level,
            confidence=confidence,
            created_at=datetime.utcnow()
        )
        db.add(parent_profile)
        parent_skills_computed += 1
        
        # Add to result list
        parent_skills_list.append({
            "parent_skill": parent_skill,
            "parent_score": parent_score,
            "parent_level": parent_level,
            "confidence": confidence
        })
        
        logger.debug(
            f"Parent Skill: {parent_skill}, Score: {parent_score:.2f}, "
            f"Level: {parent_level}, Confidence: {confidence:.4f}"
        )
    
    # Step 6: Store all parent evidence rows
    for evidence_data in parent_evidence_rows:
        evidence_row = SkillEvidenceParent(**evidence_data)
        db.add(evidence_row)
    
    db.commit()
    
    # Sort parent skills by score descending
    parent_skills_list.sort(key=lambda x: x["parent_score"], reverse=True)
    
    logger.info(
        f"Computed {parent_skills_computed} parent skills with {len(parent_evidence_rows)} "
        f"evidence rows for student {student_id}"
    )
    
    return {
        "student_id": student_id,
        "parent_skills_computed": parent_skills_computed,
        "parent_evidence_rows": len(parent_evidence_rows),
        "parent_skills": parent_skills_list
    }
