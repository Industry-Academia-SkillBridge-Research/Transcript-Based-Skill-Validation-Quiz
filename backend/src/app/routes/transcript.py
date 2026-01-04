"""
Transcript upload and processing routes.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.transcript_service import process_transcript_upload
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
