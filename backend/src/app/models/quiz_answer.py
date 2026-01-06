"""
Quiz Answer model.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db import Base


class QuizAnswer(Base):
    __tablename__ = "quiz_answer"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    attempt_id = Column(Integer, nullable=False, index=True)
    question_id = Column(Integer, nullable=False, index=True)
    student_id = Column(String, nullable=False, index=True)
    selected_option = Column(String, nullable=False)  # A, B, C, or D
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
