"""
Skill Profile Verified Parent model.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from datetime import datetime
from app.db import Base


class SkillProfileVerifiedParent(Base):
    __tablename__ = "skill_profile_verified_parent"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    parent_skill = Column(String, nullable=False, index=True)
    verified_score = Column(Float, nullable=False)
    verified_level = Column(String, nullable=False)  # Beginner, Intermediate, Advanced
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('student_id', 'parent_skill', name='uq_verified_parent_skill'),
    )
