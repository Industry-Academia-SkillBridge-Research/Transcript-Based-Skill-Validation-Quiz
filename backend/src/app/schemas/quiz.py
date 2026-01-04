"""
Quiz schemas for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QuizPlanRequest(BaseModel):
    """Request schema for creating a quiz plan."""
    selected_skills: Optional[List[str]] = Field(
        None,
        description="Optional list of specific parent skills to include (max 5)"
    )


class QuizPlanOut(BaseModel):
    """Response schema for quiz plan."""
    id: int
    student_id: str
    skill_type: str
    skills_json: str
    questions_per_skill: int
    difficulty_mix_json: str
    created_at: datetime
    
    class Config:
        from_attributes = True
