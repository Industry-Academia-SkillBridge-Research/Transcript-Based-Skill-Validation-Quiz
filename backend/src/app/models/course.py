from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db import Base


class CourseTaken(Base):
    __tablename__ = "courses_taken"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False, index=True)
    course_code = Column(String, nullable=False, index=True)
    course_name = Column(String, nullable=True)
    grade = Column(String, nullable=False)
    year_taken = Column(Integer, nullable=True)
    credits = Column(Float, nullable=True)
    academic_year = Column(Integer, nullable=True)


class CourseCatalog(Base):
    __tablename__ = "course_catalog"
    
    course_code = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    main_skill = Column(String, nullable=True)
    course_level = Column(String, nullable=True)
    credits = Column(Float, nullable=True)
    year = Column(Integer, nullable=True)
    semester = Column(Integer, nullable=True)


class CourseSkillMap(Base):
    __tablename__ = "course_skill_map"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_code = Column(String, nullable=False, index=True)
    skill_name = Column(String, nullable=False, index=True)
    map_weight = Column(Float, nullable=False)
