"""
Service for seeding course catalog and skill mapping data from CSV files.
"""

import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.course import CourseCatalog, CourseSkillMap
from app.models.skill_group_map import SkillGroupMap
import logging

logger = logging.getLogger(__name__)

# Resolve absolute paths
BACKEND_DIR = Path(__file__).resolve().parents[3]  # points to backend/
DATA_DIR = BACKEND_DIR / "data"
CATALOG_PATH = DATA_DIR / "course_catalog.csv"
SKILL_MAP_PATH = DATA_DIR / "course_skill_map.csv"
SKILL_GROUP_MAP_PATH = DATA_DIR / "skill_group_map.csv"


def seed_course_catalog(db: Session, path: Path = CATALOG_PATH) -> dict:
    """
    Seed course catalog data from CSV file.
    
    Args:
        db: Database session
        path: Path to course_catalog.csv
        
    Returns:
        Dictionary with inserted and updated counts
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Course catalog file not found: {path}")
    
    logger.info(f"Reading course catalog from: {path}")
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    
    # Validate required columns
    required_cols = ["course_code", "course_name"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in course catalog: {missing_cols}")
    
    inserted_count = 0
    updated_count = 0
    
    for idx, row in df.iterrows():
        course_code = str(row["course_code"]).strip()
        course_name = str(row["course_name"]).strip()
        
        if not course_code or not course_name:
            logger.warning(f"Skipping row {idx + 2}: missing course_code or course_name")
            continue
        
        # Extract optional fields
        main_skill = str(row.get("main_skill", "")).strip() or None
        course_level = str(row.get("course_level", "")).strip() or None
        
        credits = None
        if "credits" in df.columns and row.get("credits"):
            try:
                credits = float(row["credits"])
            except (ValueError, TypeError):
                logger.warning(f"Invalid credits value for {course_code}: {row.get('credits')}")
        
        year = None
        if "year" in df.columns and row.get("year"):
            try:
                year = int(row["year"])
            except (ValueError, TypeError):
                logger.warning(f"Invalid year value for {course_code}: {row.get('year')}")
        
        semester = None
        if "semester" in df.columns and row.get("semester"):
            try:
                semester = int(row["semester"])
            except (ValueError, TypeError):
                logger.warning(f"Invalid semester value for {course_code}: {row.get('semester')}")
        
        # Upsert: check if exists using db.get() for primary key
        # Flush to ensure pending inserts are visible
        db.flush()
        existing = db.get(CourseCatalog, course_code)
        
        if existing:
            existing.course_name = course_name
            existing.main_skill = main_skill
            existing.course_level = course_level
            existing.credits = credits
            existing.year = year
            existing.semester = semester
            updated_count += 1
            logger.debug(f"Updated course: {course_code}")
        else:
            new_course = CourseCatalog(
                course_code=course_code,
                course_name=course_name,
                main_skill=main_skill,
                course_level=course_level,
                credits=credits,
                year=year,
                semester=semester
            )
            db.add(new_course)
            inserted_count += 1
            logger.debug(f"Inserted course: {course_code}")
    
    db.commit()
    logger.info(f"Course catalog seeding complete: {inserted_count} inserted, {updated_count} updated")
    
    return {"inserted": inserted_count, "updated": updated_count}


def seed_course_skill_map(db: Session, path: Path = SKILL_MAP_PATH) -> dict:
    """
    Seed course-skill mapping data from CSV file.
    
    Args:
        db: Database session
        path: Path to course_skill_map.csv
        
    Returns:
        Dictionary with inserted and updated counts
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Course skill map file not found: {path}")
    
    logger.info(f"Reading course skill map from: {path}")
    df = pd.read_csv(file_path)
    
    # Validate required columns
    required_cols = ["course_code", "skill_name", "map_weight"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in course skill map: {missing_cols}")
    
    inserted_count = 0
    updated_count = 0
    
    for idx, row in df.iterrows():
        course_code = str(row["course_code"]).strip()
        skill_name = str(row["skill_name"]).strip()
        
        if not course_code or not skill_name:
            logger.warning(f"Skipping row {idx + 2}: missing course_code or skill_name")
            continue
        
        try:
            map_weight = float(row["map_weight"])
        except (ValueError, TypeError):
            logger.warning(f"Skipping row {idx + 2}: invalid map_weight value")
            continue
        
        # Validate map_weight is between 0 and 1
        if not (0 <= map_weight <= 1):
            logger.warning(f"Row {idx + 2}: map_weight {map_weight} is outside [0, 1] range for {course_code}/{skill_name}")
            continue
        
        # Upsert: check if exists by course_code + skill_name
        # Flush to ensure pending inserts are visible
        db.flush()
        existing = db.query(CourseSkillMap).filter_by(
            course_code=course_code,
            skill_name=skill_name
        ).first()
        
        if existing:
            existing.map_weight = map_weight
            updated_count += 1
            logger.debug(f"Updated mapping: {course_code}/{skill_name}")
        else:
            new_mapping = CourseSkillMap(
                course_code=course_code,
                skill_name=skill_name,
                map_weight=map_weight
            )
            db.add(new_mapping)
            inserted_count += 1
            logger.debug(f"Inserted mapping: {course_code}/{skill_name}")
    
    db.commit()
    logger.info(f"Course skill map seeding complete: {inserted_count} inserted, {updated_count} updated")
    
    return {"inserted": inserted_count, "updated": updated_count}


def seed_skill_group_map(db: Session, path: Path = SKILL_GROUP_MAP_PATH) -> dict:
    """
    Seed skill group mapping (parent-child skill relationships) from CSV file.
    
    Args:
        db: Database session
        path: Path to skill_group_map.csv
        
    Returns:
        Dictionary with inserted and updated counts
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Skill group map file not found: {path}")
    
    logger.info(f"Reading skill group map from: {path}")
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    
    # Validate required columns
    required_cols = ["child_skill", "parent_skill"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in skill group map: {missing_cols}")
    
    inserted_count = 0
    updated_count = 0
    
    for idx, row in df.iterrows():
        child_skill = str(row["child_skill"]).strip()
        parent_skill = str(row["parent_skill"]).strip()
        
        if not child_skill or not parent_skill:
            logger.warning(f"Skipping row {idx + 2}: missing child_skill or parent_skill")
            continue
        
        # Upsert: check if exists by (child_skill, parent_skill)
        # Flush to ensure pending inserts are visible
        db.flush()
        existing = db.query(SkillGroupMap).filter_by(
            child_skill=child_skill,
            parent_skill=parent_skill
        ).first()
        
        if existing:
            # No fields to update, just count
            updated_count += 1
            logger.debug(f"Mapping already exists: {child_skill} -> {parent_skill}")
        else:
            new_mapping = SkillGroupMap(
                child_skill=child_skill,
                parent_skill=parent_skill
            )
            db.add(new_mapping)
            inserted_count += 1
            logger.debug(f"Inserted mapping: {child_skill} -> {parent_skill}")
    
    db.commit()
    logger.info(f"Skill group map seeding complete: {inserted_count} inserted, {updated_count} updated")
    
    return {"inserted": inserted_count, "updated": updated_count}
