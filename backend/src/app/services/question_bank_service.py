"""
Question Bank Service

Handles offline question generation and fast quiz sampling from the bank.
Uses Ollama for batch generation (slow, offline) and SQLite queries for instant sampling.
"""

import json
import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from ..models.question_bank import QuestionBank
from ..models.skill_group_map import SkillGroupMap
from .ollama_client import generate_mcq

logger = logging.getLogger(__name__)


def generate_bank_for_skills(
    db: Session,
    skill_names: List[str],
    questions_per_difficulty: int = 10,
    model_name: str = "llama3.1:8b"
) -> Dict[str, any]:
    """
    Generate questions for specified skills and store in QuestionBank.
    
    This is an offline admin operation - can be slow.
    
    Args:
        db: Database session
        skill_names: List of parent skill names to generate questions for
        questions_per_difficulty: How many questions per difficulty level (easy, medium, hard)
        model_name: Ollama model to use
    
    Returns:
        Dict with generation statistics and any errors
    """
    stats = {
        "total_requested": 0,
        "total_generated": 0,
        "duplicates_skipped": 0,
        "errors": 0,
        "per_skill": {}
    }
    
    difficulties = ["easy", "medium", "hard"]
    
    for skill_name in skill_names:
        # Get child skills scope for this parent skill
        skill_maps = db.query(SkillGroupMap).filter(
            SkillGroupMap.parent_skill == skill_name
        ).all()
        
        if not skill_maps:
            logger.warning(f"No SkillGroupMap found for skill: {skill_name}")
            stats["per_skill"][skill_name] = {"error": "SkillGroupMap not found"}
            continue
        
        child_skills = [sm.child_skill for sm in skill_maps]
        
        skill_stats = {
            "requested": len(difficulties) * questions_per_difficulty,
            "generated": 0,
            "duplicates": 0,
            "errors": 0
        }
        
        for difficulty in difficulties:
            for i in range(questions_per_difficulty):
                stats["total_requested"] += 1
                
                try:
                    # Generate question using Ollama
                    logger.info(f"Generating {skill_name} - {difficulty} - question {i+1}/{questions_per_difficulty}")
                    
                    result = generate_mcq(
                        skill_name=skill_name,
                        difficulty=difficulty,
                        scope_bullets=child_skills,  # Pass list, not string
                        model=model_name
                    )
                    
                    # generate_mcq returns the dict directly (not wrapped in status/data)
                    # Create QuestionBank entry
                    question = QuestionBank(
                        skill_name=skill_name,
                        difficulty=difficulty,
                        question_text=result["question_text"],
                        options_json=json.dumps(result["options"]),  # Convert dict to JSON string
                        correct_option=result["correct_option"],
                        explanation=result["explanation"],
                        model_name=model_name
                    )
                    
                    db.add(question)
                    
                    try:
                        db.commit()
                        skill_stats["generated"] += 1
                        stats["total_generated"] += 1
                        logger.info(f"✓ Stored question for {skill_name} ({difficulty})")
                    except IntegrityError:
                        # Duplicate question (UniqueConstraint violation)
                        db.rollback()
                        skill_stats["duplicates"] += 1
                        stats["duplicates_skipped"] += 1
                        logger.info(f"⊘ Duplicate question skipped for {skill_name} ({difficulty})")
                
                except ValueError as e:
                    # generate_mcq raises ValueError on failure (after retries)
                    logger.error(f"Question generation failed: {str(e)}")
                    skill_stats["errors"] += 1
                    stats["errors"] += 1
                    db.rollback()
                except Exception as e:
                    logger.error(f"Error generating question: {str(e)}")
                    skill_stats["errors"] += 1
                    stats["errors"] += 1
                    db.rollback()
        
        stats["per_skill"][skill_name] = skill_stats
    
    return stats


def sample_quiz_from_bank(
    db: Session,
    skill_difficulty_requirements: List[Dict[str, str]],
    questions_per_skill: int = 2
) -> Dict[str, any]:
    """
    Sample questions from QuestionBank to create a quiz instantly.
    
    This is fast - just SQLite queries, no Ollama calls.
    
    Args:
        db: Database session
        skill_difficulty_requirements: List of dicts with 'skill_name' and 'difficulty'
        questions_per_skill: How many questions to sample per skill
    
    Returns:
        Dict with sampled questions and any warnings
        
    Raises:
        HTTPException(400): If no questions are available in the bank after all fallback attempts
    """
    from fastapi import HTTPException
    
    sampled_questions = []
    warnings = []
    
    for req in skill_difficulty_requirements:
        skill_name = req["skill_name"]
        difficulty = req["difficulty"]
        
        # Check count before querying
        available_count = db.query(func.count(QuestionBank.id)).filter(
            QuestionBank.skill_name == skill_name,
            QuestionBank.difficulty == difficulty
        ).scalar()
        
        questions = []
        
        if available_count == 0:
            # No questions available for this skill/difficulty
            warnings.append({
                "skill": skill_name,
                "difficulty": difficulty,
                "message": f"No questions available for {skill_name} difficulty {difficulty}"
            })
            
            # Try fallback to easier difficulties (hard->medium->easy)
            fallback_order = {
                "hard": ["medium", "easy"],
                "medium": ["easy", "hard"],
                "easy": ["medium", "hard"]
            }
            fallback_difficulties = fallback_order.get(difficulty, [])
            
            for fallback_diff in fallback_difficulties:
                fallback_count = db.query(func.count(QuestionBank.id)).filter(
                    QuestionBank.skill_name == skill_name,
                    QuestionBank.difficulty == fallback_diff
                ).scalar()
                
                if fallback_count > 0:
                    questions = db.query(QuestionBank).filter(
                        QuestionBank.skill_name == skill_name,
                        QuestionBank.difficulty == fallback_diff
                    ).order_by(func.random()).limit(questions_per_skill).all()
                    
                    warnings.append({
                        "skill": skill_name,
                        "message": f"Used {len(questions)} {fallback_diff} questions instead of {difficulty}"
                    })
                    break
            
            # If still none available after fallback, skip this slot
            if not questions:
                warnings.append({
                    "skill": skill_name,
                    "message": f"Skipping {skill_name} - no questions available in any difficulty"
                })
                continue
                
        else:
            # Sample random questions from bank
            questions = db.query(QuestionBank).filter(
                QuestionBank.skill_name == skill_name,
                QuestionBank.difficulty == difficulty
            ).order_by(func.random()).limit(questions_per_skill).all()
            
            if len(questions) < questions_per_skill:
                # Not enough questions in bank for this skill/difficulty
                actual = len(questions)
                warnings.append({
                    "skill": skill_name,
                    "difficulty": difficulty,
                    "requested": questions_per_skill,
                    "found": actual,
                    "message": f"Only {actual}/{questions_per_skill} questions available for {skill_name} {difficulty}"
                })
                
                # Try to fill the gap with other difficulty levels
                fallback_order = {
                    "hard": ["medium", "easy"],
                    "medium": ["easy", "hard"],
                    "easy": ["medium", "hard"]
                }
                fallback_difficulties = fallback_order.get(difficulty, [])
                remaining = questions_per_skill - actual
                
                for fallback_diff in fallback_difficulties:
                    fallback_questions = db.query(QuestionBank).filter(
                        QuestionBank.skill_name == skill_name,
                        QuestionBank.difficulty == fallback_diff
                    ).order_by(func.random()).limit(remaining).all()
                    
                    if fallback_questions:
                        questions.extend(fallback_questions)
                        warnings.append({
                            "skill": skill_name,
                            "message": f"Filled {len(fallback_questions)} with {fallback_diff} difficulty"
                        })
                        remaining -= len(fallback_questions)
                        
                        if remaining <= 0:
                            break
        
        # Convert to dict format
        for q in questions:
            sampled_questions.append({
                "skill_name": q.skill_name,
                "difficulty": q.difficulty,
                "question": q.question_text,
                "options": json.loads(q.options_json),  # Parse JSON string to dict
                "correct_option": q.correct_option,
                "explanation": q.explanation
            })
    
    # After sampling, if total sampled questions == 0, raise error
    if len(sampled_questions) == 0:
        raise HTTPException(
            status_code=400,
            detail="Question bank has no matching questions for the quiz plan. Admin needs to generate questions for these skills."
        )
    
    return {
        "questions": sampled_questions,
        "total_sampled": len(sampled_questions),
        "warnings": warnings
    }


def get_bank_statistics(db: Session) -> Dict[str, any]:
    """
    Get statistics about the current question bank.
    
    Returns counts per skill and difficulty.
    """
    # Total questions
    total = db.query(func.count(QuestionBank.id)).scalar()
    
    # Breakdown by skill and difficulty
    breakdown = db.query(
        QuestionBank.skill_name,
        QuestionBank.difficulty,
        func.count(QuestionBank.id).label('count')
    ).group_by(
        QuestionBank.skill_name,
        QuestionBank.difficulty
    ).all()
    
    # Organize by skill
    by_skill = {}
    for skill_name, difficulty, count in breakdown:
        if skill_name not in by_skill:
            by_skill[skill_name] = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
        by_skill[skill_name][difficulty] = count
        by_skill[skill_name]["total"] += count
    
    return {
        "total_questions": total,
        "by_skill": by_skill
    }
