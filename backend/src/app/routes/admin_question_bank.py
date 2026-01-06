"""
Admin Question Bank Routes

Endpoints for pre-generating questions offline using Ollama.
These operations can be slow - meant for admin use only.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

from ..db import get_db
from ..services import question_bank_service

router = APIRouter(prefix="/admin/question-bank", tags=["Admin - Question Bank"])


class GenerateQuestionsRequest(BaseModel):
    skill_names: List[str] = Field(..., description="List of parent skill names to generate questions for")
    questions_per_difficulty: int = Field(10, description="Number of questions per difficulty level (easy, medium, hard)")
    model_name: str = Field("llama3.1:8b", description="Ollama model to use")


class GenerateQuestionsResponse(BaseModel):
    status: str
    total_requested: int
    total_generated: int
    duplicates_skipped: int
    errors: int
    per_skill: dict
    message: str


class BankStatsResponse(BaseModel):
    total_questions: int
    by_skill: dict


@router.post("/generate", response_model=GenerateQuestionsResponse)
def generate_questions_for_skills(
    request: GenerateQuestionsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate questions for specified skills and store in QuestionBank.
    
    **This is a slow operation** - generates questions using Ollama.
    Use this offline/admin task to pre-populate the question bank.
    
    Example request:
    ```json
    {
        "skill_names": ["Python Programming", "Data Structures"],
        "questions_per_difficulty": 10,
        "model_name": "llama3.1:8b"
    }
    ```
    
    This will generate 10 easy + 10 medium + 10 hard = 30 questions per skill.
    """
    if not request.skill_names:
        raise HTTPException(status_code=400, detail="skill_names cannot be empty")
    
    if request.questions_per_difficulty < 1 or request.questions_per_difficulty > 50:
        raise HTTPException(status_code=400, detail="questions_per_difficulty must be between 1 and 50")
    
    # Generate questions (slow operation)
    stats = question_bank_service.generate_bank_for_skills(
        db=db,
        skill_names=request.skill_names,
        questions_per_difficulty=request.questions_per_difficulty,
        model_name=request.model_name
    )
    
    # Prepare response
    success_rate = (stats["total_generated"] / stats["total_requested"] * 100) if stats["total_requested"] > 0 else 0
    
    message = f"Generated {stats['total_generated']}/{stats['total_requested']} questions ({success_rate:.1f}% success). "
    
    if stats["duplicates_skipped"] > 0:
        message += f"{stats['duplicates_skipped']} duplicates skipped. "
    
    if stats["errors"] > 0:
        message += f"{stats['errors']} errors encountered."
    
    return GenerateQuestionsResponse(
        status="completed",
        total_requested=stats["total_requested"],
        total_generated=stats["total_generated"],
        duplicates_skipped=stats["duplicates_skipped"],
        errors=stats["errors"],
        per_skill=stats["per_skill"],
        message=message.strip()
    )


@router.get("/stats", response_model=BankStatsResponse)
def get_question_bank_statistics(db: Session = Depends(get_db)):
    """
    Get statistics about the current question bank.
    
    Returns total count and breakdown by skill/difficulty.
    """
    stats = question_bank_service.get_bank_statistics(db)
    
    return BankStatsResponse(
        total_questions=stats["total_questions"],
        by_skill=stats["by_skill"]
    )


@router.delete("/clear")
def clear_question_bank(
    skill_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Clear questions from the bank.
    
    - If skill_name is provided: clears only that skill
    - If skill_name is None: clears entire bank (use with caution!)
    """
    from ..models.question_bank import QuestionBank
    
    if skill_name:
        deleted = db.query(QuestionBank).filter(
            QuestionBank.skill_name == skill_name
        ).delete()
        db.commit()
        return {"status": "success", "deleted": deleted, "skill": skill_name}
    else:
        # Clear entire bank
        deleted = db.query(QuestionBank).delete()
        db.commit()
        return {"status": "success", "deleted": deleted, "message": "Entire question bank cleared"}
