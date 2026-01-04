from sqlalchemy import Column, String
from app.db import Base


class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    program = Column(String, nullable=True)
    intake = Column(String, nullable=True)
