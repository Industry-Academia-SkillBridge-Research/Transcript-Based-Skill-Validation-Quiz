"""
Quiz Scoring Service

Handles quiz answer validation, scoring, and skill profile updates.
"""

import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from collections import defaultdict

from ..models.quiz import QuizQuestion, QuizAttempt
from ..models.quiz_answer import QuizAnswer
from ..models.skill_profile_verified_parent import SkillProfileVerifiedParent
from ..models.skill_profile_final_parent import SkillProfileFinalParent
from ..models.skill import SkillProfileParentClaimed

logger = logging.getLogger(__name__)


def determine_level(score: float) -> str:
    """
    Determine skill level based on score.
    
    Args:
        score: Score between 0-100
        
    Returns:
        Level string: Beginner, Intermediate, or Advanced
    """
    if score < 50:
        return "Beginner"
    elif score < 75:
        return "Intermediate"
    else:
        return "Advanced"


def score_attempt(
    student_id: str,
    attempt_id: int,
    answers: List[Dict[str, any]],
    db: Session
) -> Dict[str, any]:
    """
    Score a quiz attempt and update skill profiles.
    
    Args:
        student_id: Student identifier
        attempt_id: Quiz attempt ID
        answers: List of dicts with 'question_id' and 'selected_option'
        db: Database session
        
    Returns:
        Summary dict with attempt_id, overall_verified_score, per_skill details, and portfolio
        
    Raises:
        ValueError: If attempt not found, student mismatch, or invalid answers
    """
    # Verify attempt exists and belongs to student
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.attempt_id == attempt_id,
        QuizAttempt.student_id == student_id
    ).first()
    
    if not attempt:
        raise ValueError(f"Quiz attempt {attempt_id} not found for student {student_id}")
    
    # Load all questions for this attempt
    questions = db.query(QuizQuestion).filter(
        QuizQuestion.attempt_id == attempt_id,
        QuizQuestion.student_id == student_id
    ).all()
    
    if not questions:
        raise ValueError(f"No questions found for attempt {attempt_id}")
    
    # Build question lookup
    question_map = {q.question_id: q for q in questions}
    
    # Validate all answers have valid question_ids
    answer_map = {ans["question_id"]: ans["selected_option"] for ans in answers}
    
    for question_id in answer_map.keys():
        if question_id not in question_map:
            raise ValueError(f"Invalid question_id {question_id} for attempt {attempt_id}")
    
    # Track skill-level statistics
    skill_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    
    # Process each question and create QuizAnswer records
    quiz_answers = []
    for question in questions:
        selected_option = answer_map.get(question.question_id)
        
        if not selected_option:
            # Question not answered - mark as incorrect
            is_correct = False
        else:
            is_correct = (selected_option == question.correct_option)
        
        # Create QuizAnswer record
        quiz_answer = QuizAnswer(
            attempt_id=attempt_id,
            question_id=question.question_id,
            student_id=student_id,
            selected_option=selected_option or "UNANSWERED",
            is_correct=is_correct
        )
        quiz_answers.append(quiz_answer)
        db.add(quiz_answer)
        
        # Update skill stats
        skill_stats[question.skill_name]["total"] += 1
        if is_correct:
            skill_stats[question.skill_name]["correct"] += 1
    
    # Calculate verified scores per skill
    verified_scores = {}
    for skill_name, stats in skill_stats.items():
        if stats["total"] > 0:
            verified_scores[skill_name] = 100.0 * stats["correct"] / stats["total"]
        else:
            verified_scores[skill_name] = 0.0
    
    # Load claimed parent scores
    claimed_profiles = db.query(SkillProfileParentClaimed).filter(
        SkillProfileParentClaimed.student_id == student_id
    ).all()
    
    claimed_scores = {p.parent_skill: p.parent_score for p in claimed_profiles}
    
    # Delete old verified and final profiles for this student
    db.query(SkillProfileVerifiedParent).filter(
        SkillProfileVerifiedParent.student_id == student_id
    ).delete()
    
    db.query(SkillProfileFinalParent).filter(
        SkillProfileFinalParent.student_id == student_id
    ).delete()
    
    # Create new verified and final profiles
    portfolio = []
    per_skill_details = []
    
    for skill_name, verified_score in verified_scores.items():
        verified_level = determine_level(verified_score)
        
        # Create SkillProfileVerifiedParent
        verified_profile = SkillProfileVerifiedParent(
            student_id=student_id,
            parent_skill=skill_name,
            verified_score=verified_score,
            verified_level=verified_level
        )
        db.add(verified_profile)
        
        # Calculate final score (0.3 claimed + 0.7 verified)
        claimed_score = claimed_scores.get(skill_name, 0.0)
        final_score = 0.3 * claimed_score + 0.7 * verified_score
        final_level = determine_level(final_score)
        
        # Create SkillProfileFinalParent
        final_profile = SkillProfileFinalParent(
            student_id=student_id,
            parent_skill=skill_name,
            claimed_score=claimed_score,
            verified_score=verified_score,
            final_score=final_score,
            final_level=final_level
        )
        db.add(final_profile)
        
        # Build per-skill detail
        per_skill_details.append({
            "skill_name": skill_name,
            "correct": skill_stats[skill_name]["correct"],
            "total": skill_stats[skill_name]["total"],
            "verified_score": round(verified_score, 2),
            "verified_level": verified_level
        })
        
        # Build portfolio entry
        portfolio.append({
            "skill_name": skill_name,
            "claimed_score": round(claimed_score, 2),
            "verified_score": round(verified_score, 2),
            "final_score": round(final_score, 2),
            "final_level": final_level
        })
    
    # Commit all changes
    db.commit()
    
    # Calculate overall verified score
    total_correct = sum(stats["correct"] for stats in skill_stats.values())
    total_questions = sum(stats["total"] for stats in skill_stats.values())
    overall_verified_score = (100.0 * total_correct / total_questions) if total_questions > 0 else 0.0
    
    logger.info(
        f"Quiz scored for student {student_id}, attempt {attempt_id}: "
        f"{total_correct}/{total_questions} correct ({overall_verified_score:.1f}%)"
    )
    
    return {
        "attempt_id": attempt_id,
        "overall_verified_score": round(overall_verified_score, 2),
        "total_correct": total_correct,
        "total_questions": total_questions,
        "per_skill": per_skill_details,
        "portfolio": portfolio
    }
