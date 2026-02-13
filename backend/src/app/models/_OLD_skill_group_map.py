from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.db import Base


class SkillGroupMap(Base):
    __tablename__ = "skill_group_map"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    child_skill = Column(String, nullable=False, index=True)
    parent_skill = Column(String, nullable=False, index=True)
    
    __table_args__ = (
        UniqueConstraint('child_skill', 'parent_skill', name='uq_skill_group_map'),
    )
