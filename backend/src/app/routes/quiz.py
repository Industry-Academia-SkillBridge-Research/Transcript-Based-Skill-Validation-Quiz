"""
Quiz API routes for quiz planning and management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.quiz import QuizPlan
from app.schemas.quiz import QuizPlanRequest, QuizPlanOut
from app.services.quiz_planner import create_quiz_plan
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["Quiz"])


@router.post("/{student_id}/quiz/plan", response_model=QuizPlanOut)
def create_student_quiz_plan(
    student_id: str,
    request: QuizPlanRequest = QuizPlanRequest(),
    db: Session = Depends(get_db)
):
    """
    Create a quiz plan for a student based on parent skills.
    
    If selected_skills is provided, uses those specific skills (max 5).
    Otherwise, auto-selects skills based on confidence and score.
    
    Args:
        student_id: Student identifier
        request: Quiz plan request with optional selected_skills
        db: Database session
        
    Returns:
        Created quiz plan object
    """
    try:
        quiz_plan = create_quiz_plan(
            student_id=student_id,
            db=db,
            selected_skills=request.selected_skills
        )
        
        logger.info(f"Quiz plan created for student {student_id}")
        return quiz_plan
        
    except ValueError as e:
        logger.warning(f"Quiz plan creation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating quiz plan: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create quiz plan")


@router.get("/{student_id}/quiz/plan/latest", response_model=QuizPlanOut)
def get_latest_quiz_plan(student_id: str, db: Session = Depends(get_db)):
    """
    Get the latest quiz plan for a student.
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Latest quiz plan object
    """
    quiz_plan = db.query(QuizPlan).filter(
        QuizPlan.student_id == student_id
    ).order_by(QuizPlan.created_at.desc()).first()
    
    if not quiz_plan:
        raise HTTPException(
            status_code=404,
            detail=f"No quiz plan found for student {student_id}"
        )
    
    return quiz_plan
