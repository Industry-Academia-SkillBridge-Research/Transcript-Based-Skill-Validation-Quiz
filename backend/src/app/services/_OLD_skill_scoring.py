"""
Skill scoring and computation service.
"""

import logging
from datetime import datetime
from typing import Dict, List
from math import exp
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.course import CourseTaken, CourseSkillMap
from app.models.skill import SkillProfileClaimed, SkillEvidence

logger = logging.getLogger(__name__)

# Grade to GPA (4.0 scale) mapping
GRADE_MAPPING = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "F": 0.0,
}

DEFAULT_CREDITS = 3.0
RECENCY_DECAY = 0.4
CONFIDENCE_FACTOR = 0.25


def get_grade_points(grade: str) -> float:
    """
    Convert letter grade to GPA points (4.0 scale).
    
    Args:
        grade: Letter grade (e.g., A+, B, C-)
        
    Returns:
        Grade points on 4.0 scale
    """
    grade_upper = grade.strip().upper()
    return GRADE_MAPPING.get(grade_upper, 0.0)


def calculate_recency(academic_year: int = None, year_taken: int = None) -> float:
    """
    Calculate recency factor based on academic year or calendar year.
    Prefers academic_year if available, falls back to year_taken.
    
    Args:
        academic_year: Academic year when course was taken (1-4)
        year_taken: Calendar year when course was taken (e.g., 2021)
        
    Returns:
        Recency factor (0 to 1)
    """
    if academic_year is not None:
        # Use academic year (1-4)
        current_academic_year = 4
        years_since = max(0, current_academic_year - academic_year)
        recency = exp(-RECENCY_DECAY * years_since)
    elif year_taken is not None:
        # Fall back to calendar year
        current_year = datetime.now().year
        years_since = max(0, current_year - year_taken)
        recency = exp(-RECENCY_DECAY * years_since)
    else:
        # No temporal information, use default
        recency = 1.0
    
    return recency


def determine_skill_level(score: float) -> str:
    """
    Determine skill level based on claimed score.
    
    Args:
        score: Claimed skill score (0-100)
        
    Returns:
        Skill level: Beginner, Intermediate, or Advanced
    """
    if score < 50:
        return "Beginner"
    elif score < 75:
        return "Intermediate"
    else:
        return "Advanced"


def compute_claimed_skills(student_id: str, db: Session) -> Dict:
    """
    Compute claimed skills for a student based on their transcript.
    
    Process:
    1. Join CourseTaken with CourseSkillMap
    2. Calculate grade_norm, recency, evidence_weight for each course-skill
    3. Aggregate by skill to compute claimed_score and confidence
    4. Store in SkillProfileClaimed and SkillEvidence
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Dictionary with computation summary
    """
    logger.info(f"Computing claimed skills for student: {student_id}")
    
    # Clear existing claimed skills and evidence for this student
    db.query(SkillProfileClaimed).filter(
        SkillProfileClaimed.student_id == student_id
    ).delete()
    
    db.query(SkillEvidence).filter(
        SkillEvidence.student_id == student_id
    ).delete()
    
    db.flush()
    
    # Fetch courses taken by student
    courses_taken = db.query(CourseTaken).filter(
        CourseTaken.student_id == student_id
    ).all()
    
    if not courses_taken:
        logger.warning(f"No courses found for student: {student_id}")
        return {
            "student_id": student_id,
            "skills_computed": 0,
            "evidence_rows": 0
        }
    
    # Build evidence data: join with CourseSkillMap
    evidence_data = []
    
    for course in courses_taken:
        # Get skill mappings for this course
        skill_mappings = db.query(CourseSkillMap).filter(
            CourseSkillMap.course_code == course.course_code
        ).all()
        
        if not skill_mappings:
            logger.debug(f"No skill mappings found for course: {course.course_code}")
            continue
        
        # Calculate course metrics
        grade_points = get_grade_points(course.grade)
        grade_norm = grade_points / 4.0
        
        # Use course credits if available, otherwise default
        credits = course.credits if course.credits else DEFAULT_CREDITS
        
        # Determine academic_year (use stored value or derive from course_code)
        academic_year = course.academic_year
        if academic_year is None:
            import re
            match = re.match(r"\bIT([1-4])\d{3}\b", course.course_code)
            if match:
                academic_year = int(match.group(1))
                if not (1 <= academic_year <= 4):
                    academic_year = None
        
        # Calculate recency (prefers academic_year, falls back to year_taken)
        recency = calculate_recency(academic_year, course.year_taken)
        
        # Create evidence for each skill mapped to this course
        for mapping in skill_mappings:
            evidence_weight = mapping.map_weight * credits * recency
            contribution = grade_norm * evidence_weight
            
            evidence_data.append({
                "student_id": student_id,
                "skill_name": mapping.skill_name,
                "course_code": course.course_code,
                "map_weight": mapping.map_weight,
                "credits": credits,
                "grade": course.grade,
                "grade_norm": grade_norm,
                "academic_year": academic_year,
                "recency": recency,
                "evidence_weight": evidence_weight,
                "contribution": contribution
            })
    
    if not evidence_data:
        logger.warning(f"No evidence data generated for student: {student_id}")
        return {
            "student_id": student_id,
            "skills_computed": 0,
            "evidence_rows": 0
        }
    
    # Aggregate by skill
    skill_aggregates = {}
    for evidence in evidence_data:
        skill_name = evidence["skill_name"]
        
        if skill_name not in skill_aggregates:
            skill_aggregates[skill_name] = {
                "total_contribution": 0.0,
                "total_evidence_weight": 0.0
            }
        
        skill_aggregates[skill_name]["total_contribution"] += evidence["contribution"]
        skill_aggregates[skill_name]["total_evidence_weight"] += evidence["evidence_weight"]
    
    # Compute claimed scores and confidence
    claimed_skills = []
    skills_computed = 0
    
    for skill_name, aggregates in skill_aggregates.items():
        total_contribution = aggregates["total_contribution"]
        total_evidence_weight = aggregates["total_evidence_weight"]
        
        if total_evidence_weight == 0:
            logger.warning(f"Zero evidence weight for skill: {skill_name}")
            continue
        
        # Claimed score
        claimed_score = 100 * (total_contribution / total_evidence_weight)
        
        # Confidence
        confidence = 1 - exp(-CONFIDENCE_FACTOR * total_evidence_weight)
        
        # Skill level
        claimed_level = determine_skill_level(claimed_score)
        
        # Store in SkillProfileClaimed
        skill_profile = SkillProfileClaimed(
            student_id=student_id,
            skill_name=skill_name,
            claimed_score=claimed_score,
            claimed_level=claimed_level,
            confidence=confidence,
            created_at=datetime.utcnow()
        )
        db.add(skill_profile)
        skills_computed += 1
        
        # Add to result list
        claimed_skills.append({
            "skill_name": skill_name,
            "claimed_score": claimed_score,
            "claimed_level": claimed_level,
            "confidence": confidence
        })
        
        logger.debug(
            f"Skill: {skill_name}, Score: {claimed_score:.2f}, "
            f"Level: {claimed_level}, Confidence: {confidence:.4f}"
        )
    
    # Store all evidence rows
    for evidence in evidence_data:
        evidence_row = SkillEvidence(**evidence)
        db.add(evidence_row)
    
    db.commit()
    
    # Sort claimed skills by score descending
    claimed_skills.sort(key=lambda x: x["claimed_score"], reverse=True)
    
    logger.info(
        f"Computed {skills_computed} skills with {len(evidence_data)} "
        f"evidence rows for student {student_id}"
    )
    
    return {
        "student_id": student_id,
        "skills_computed": skills_computed,
        "evidence_rows": len(evidence_data),
        "claimed_skills": claimed_skills
    }
