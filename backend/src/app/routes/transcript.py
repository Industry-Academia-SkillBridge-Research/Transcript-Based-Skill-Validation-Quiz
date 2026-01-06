"""
Transcript upload and processing routes.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.transcript_service import process_transcript_upload
from app.models.student import Student
from app.models.course import CourseTaken
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transcript", tags=["Transcript"])


@router.post("/upload")
async def upload_transcript(
    file: UploadFile = File(...),
    student_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a student transcript.
    
    Args:
        file: PDF transcript file
        student_id: Student identifier
        db: Database session
        
    Returns:
        Dictionary with parsed courses and warnings
    """
    try:
        logger.info(f"Processing transcript upload for student: {student_id}")
        
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Process transcript
        result = process_transcript_upload(db, file, student_id)
        
        return result
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Transcript upload failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Transcript processing failed: {str(e)}"
        )


@router.get("/{student_id}")
def get_transcript(student_id: str, db: Session = Depends(get_db)):
    """
    Get transcript details for a student.
    
    Args:
        student_id: Student identifier
        db: Database session
        
    Returns:
        Dictionary with student info and courses
    """
    try:
        # Get student info
        student = db.query(Student).filter(Student.student_id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"No transcript found for student {student_id}"
            )
        
        # Get courses
        courses = db.query(CourseTaken).filter(CourseTaken.student_id == student_id).all()
        
        return {
            "student_id": student.student_id,
            "name": student.name or "N/A",
            "program": student.program or "N/A",
            "intake": student.intake or "N/A",
            "specialization": student.specialization or "N/A",
            "courses": [
                {
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "grade": course.grade,
                    "credits": course.credits
                }
                for course in courses
            ]
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Failed to retrieve transcript: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve transcript: {str(e)}"
        )
