"""
Question Bank models for pre-generated MCQs.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint
from datetime import datetime
from app.db import Base


class QuestionBank(Base):
    __tablename__ = "question_bank"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    skill_name = Column(String, nullable=False, index=True)  # parent skill
    difficulty = Column(String, nullable=False, index=True)  # easy|medium|hard
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON string {"A":..,"B":..,"C":..,"D":..}
    correct_option = Column(String, nullable=False)  # A|B|C|D
    explanation = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)  # e.g., "llama3.1:8b"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('skill_name', 'difficulty', 'question_text', name='uq_question_bank_content'),
    )
