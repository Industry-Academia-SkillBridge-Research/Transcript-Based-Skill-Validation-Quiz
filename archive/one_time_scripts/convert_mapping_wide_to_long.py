"""
Convert course-skill mapping from wide format to long format.

Input: backend/data/course_skill_mapping.csv
Outputs:
  1) backend/data/course_skill_map.csv
  2) backend/data/course_catalog.csv
"""

import pandas as pd
import os
from pathlib import Path


def convert_mapping():
    # Define paths
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    data_dir = backend_dir / "data"
    
    input_file = data_dir / "course_skill_mapping.csv"
    output_skill_map = data_dir / "course_skill_map.csv"
    output_catalog = data_dir / "course_catalog.csv"
    
    # Read input CSV
    print(f"Reading input file: {input_file}")
    df = pd.read_csv(
        input_file,
        dtype=str,
        keep_default_na=False,
        encoding="cp1252"
    )

    
    total_courses_read = len(df)
    print(f"Total courses read: {total_courses_read}")
    
    # Initialize output lists
    skill_map_rows = []
    catalog_rows = []
    
    courses_written = 0
    courses_skipped_no_code = 0
    courses_skipped_no_skills = 0
    
    # Process each course row
    for idx, row in df.iterrows():
        # Validate CourseCode
        course_code = str(row.get('CourseCode', '')).strip()
        if not course_code:
            print(f"Warning: Row {idx + 2} skipped - missing CourseCode")
            courses_skipped_no_code += 1
            continue
        
        # Extract course metadata
        course_title = str(row.get('CourseTitle', '')).strip()
        main_skill = str(row.get('MainSkill', '')).strip()
        skill_level = str(row.get('SkillLevel', '')).strip()
        
        # Collect skills from Skill1 to Skill5
        skills = []
        for i in range(1, 6):
            skill_col = f'Skill{i}'
            skill_value = str(row.get(skill_col, '')).strip()
            if skill_value:
                skills.append(skill_value)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
        
        # Check if course has any skills
        if not unique_skills:
            print(f"Warning: Course {course_code} skipped - no valid skills found")
            courses_skipped_no_skills += 1
            continue
        
        # Calculate equal weight for each skill
        num_skills = len(unique_skills)
        weight = round(1.0 / num_skills, 4)
        
        # Create skill map rows
        for skill_name in unique_skills:
            skill_map_rows.append({
                'course_code': course_code,
                'skill_name': skill_name,
                'map_weight': weight
            })
        
        # Create catalog row
        catalog_rows.append({
            'course_code': course_code,
            'course_name': course_title,
            'main_skill': main_skill,
            'course_level': skill_level
        })
        
        courses_written += 1
    
    # Create output DataFrames
    df_skill_map = pd.DataFrame(skill_map_rows)
    df_catalog = pd.DataFrame(catalog_rows)
    
    # Write output files
    print(f"\nWriting skill map to: {output_skill_map}")
    df_skill_map.to_csv(output_skill_map, index=False)
    
    print(f"Writing course catalog to: {output_catalog}")
    df_catalog.to_csv(output_catalog, index=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    print(f"Total courses read:              {total_courses_read}")
    print(f"Courses skipped (no code):       {courses_skipped_no_code}")
    print(f"Courses skipped (no skills):     {courses_skipped_no_skills}")
    print(f"Total courses written:           {courses_written}")
    print(f"Total skill-course rows written: {len(skill_map_rows)}")
    print("=" * 60)
    print("\nConversion completed successfully!")


if __name__ == "__main__":
    convert_mapping()
