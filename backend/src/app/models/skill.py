from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db import Base


class SkillProfileClaimed(Base):
    __tablename__ = "skill_profile_claimed"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    skill_name = Column(String, nullable=False, index=True)
    claimed_score = Column(Float, nullable=False)
    claimed_level = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SkillEvidence(Base):
    __tablename__ = "skill_evidence"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    skill_name = Column(String, nullable=False, index=True)
    course_code = Column(String, nullable=False)
    map_weight = Column(Float, nullable=False)
    credits = Column(Float, nullable=False)
    grade = Column(String, nullable=False)
    grade_norm = Column(Float, nullable=False)
    academic_year = Column(Integer, nullable=True)
    recency = Column(Float, nullable=False)
    evidence_weight = Column(Float, nullable=False)
    contribution = Column(Float, nullable=False)


class SkillProfileParentClaimed(Base):
    __tablename__ = "skill_profile_parent_claimed"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    parent_skill = Column(String, nullable=False, index=True)
    parent_score = Column(Float, nullable=False)
    parent_level = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SkillEvidenceParent(Base):
    __tablename__ = "skill_evidence_parent"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    parent_skill = Column(String, nullable=False, index=True)
    child_skill = Column(String, nullable=False)
    course_code = Column(String, nullable=False)
    contribution = Column(Float, nullable=False)
    evidence_weight = Column(Float, nullable=False)
    recency = Column(Float, nullable=False)
    grade = Column(String, nullable=False)
    credits = Column(Float, nullable=False)
    map_weight = Column(Float, nullable=False)
