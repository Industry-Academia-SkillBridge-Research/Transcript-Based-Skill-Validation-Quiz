"""
Skill Profile Final Parent model.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from datetime import datetime
from app.db import Base


class SkillProfileFinalParent(Base):
    __tablename__ = "skill_profile_final_parent"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    parent_skill = Column(String, nullable=False, index=True)
    claimed_score = Column(Float, nullable=False)
    verified_score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=False)
    final_level = Column(String, nullable=False)  # Beginner, Intermediate, Advanced
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('student_id', 'parent_skill', name='uq_final_parent_skill'),
    )
