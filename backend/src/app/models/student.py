from sqlalchemy import Column, String, Text
from app.db import Base


class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    program = Column(String, nullable=True)
    intake = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    email = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)  # URL or base64 image
    bio = Column(Text, nullable=True)
