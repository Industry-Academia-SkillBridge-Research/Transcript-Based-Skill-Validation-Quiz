"""
Quiz planning models.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db import Base


class QuizPlan(Base):
    __tablename__ = "quiz_plan"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    skill_type = Column(String, nullable=False)  # "parent" or "child"
    skills_json = Column(Text, nullable=False)  # JSON list of skill names
    questions_per_skill = Column(Integer, nullable=False, default=4)
    difficulty_mix_json = Column(Text, nullable=False)  # JSON dict of difficulty mix
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
