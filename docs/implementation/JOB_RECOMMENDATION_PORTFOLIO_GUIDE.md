# 💼 Job Recommendation Guide - Portfolio Based

## Overview
Your system has **TWO job recommendation engines** that now prioritize **tested skills** (from portfolio) over claimed skills:

1. **Rule-Based Recommendations** - Fast, skill-matching algorithm
2. **ML-Enhanced Recommendations** - AI-powered with skill gap analysis

---

## 🎯 How It Works

### Priority Order:
1. **Portfolio Skills (Tested)** ✅ - Skills validated through quizzes (HIGHEST PRIORITY)
2. **Claimed Skills** - Skills from transcript (used to supplement)

### Job Matching Logic:
- Compares your skills against 50+ job postings
- Calculates match percentage
- Shows which skills you have vs. need
- Provides improvement recommendations

---

## 🚀 Usage Guide

### Option 1: Rule-Based Recommendations (Simple & Fast)

**Access via:**
- Frontend: `http://localhost:8080/students/IT21013928/jobs`
- Click "Browse Jobs" button from Skills page

**API Endpoint:**
```
GET /students/{student_id}/jobs/recommend?top_k=10&threshold=70
```

**Parameters:**
- `top_k`: Number of jobs to return (1-100, default: 10)
- `threshold`: Minimum score to consider skill "matched" (0-100, default: 70)
- `role_key`: Filter by role (optional): AIML, FULLSTACK, DEVOPS, etc.

**Example:**
```bash
curl http://localhost:8000/students/IT21013928/jobs/recommend?top_k=5&threshold=75
```

**Response:**
```json
{
  "job_id": 1,
  "title": "Full Stack Developer",
  "company": "Tech Corp",
  "match_score": 85.5,
  "matched_skills": [
    {"skill": "Python", "score": 90},
    {"skill": "SQL", "score": 85}
  ],
  "missing_skills": [
    {"skill": "Docker", "score": 0, "gap": 70}
  ]
}
```

---

### Option 2: ML-Enhanced Recommendations (Advanced)

**Access via:**
- Frontend: `http://localhost:8080/students/IT21013928/jobs/ml`
- Click "AI Job Matches" button from Skills page

**API Endpoint:**
```
GET /students/{student_id}/jobs/recommend/ml?use_verified=true
```

**Parameters:**
- `top_k`: Number of recommendations (default: 10)
- `threshold`: Skill proficiency threshold (default: 70)
- `use_verified`: Prefer verified skills (default: true) ⭐ **IMPORTANT**
- `role_key`: Filter by role (optional)

**Example:**
```bash
curl "http://localhost:8000/students/IT21013928/jobs/recommend/ml?use_verified=true&top_k=5"
```

**Enhanced Features:**
- ✅ Uses ML model for intelligent matching
- ✅ Prioritizes **verified (tested) skills**
- ✅ Shows skill levels (Beginner/Intermediate/Advanced)
- ✅ Detailed skill gap analysis
- ✅ Actionable improvement recommendations
- ✅ Readiness assessment

**Response Structure:**
```json
{
  "job_id": 1,
  "title": "AI Engineer",
  "match_score": 78.5,
  "readiness": "Almost Ready",
  "skill_gaps": {
    "proficient": [
      {"skill": "Python", "score": 85, "level": "Advanced"}
    ],
    "needs_improvement": [
      {"skill": "TensorFlow", "score": 55, "gap": 15, "recommendation": "Complete intermediate tutorials"}
    ],
    "missing": [
      {"skill": "Docker", "recommendation": "Start with foundational courses"}
    ]
  },
  "next_steps": ["Improve TensorFlow skills", "Learn Docker basics"]
}
```

---

## 📊 Current Workflow

### Step-by-Step:

1. **Upload Transcript** 
   - System extracts courses
   - Computes 129 claimed skills

2. **Take Quizzes** ⭐
   - Select up to 5 skills
   - Answer questions
   - Skills get verified and added to portfolio

3. **View Job Recommendations**
   - System uses **portfolio skills first** (tested)
   - Supplements with claimed skills
   - Shows best matches

4. **Check Job Details**
   - See required vs. your skills
   - Identify skill gaps
   - Get learning recommendations

---

## 🎓 Example User Journey

### Day 1: Initial Assessment
```
1. Upload transcript → 129 claimed skills computed
2. Browse jobs → See potential matches based on transcript
```

### Day 2: Skill Validation
```
1. Take quiz on: Python, SQL, Java, Git, Linux
2. All 5 skills verified and added to portfolio
```

### Day 3: Better Job Matching
```
1. Check job recommendations
2. System now prioritizes your 5 verified skills
3. More accurate match scores
4. Better job suggestions
```

### Result:
- **Higher confidence** - Employers see quiz-validated skills
- **Better matches** - Jobs aligned with proven abilities
- **Clear path** - Know exactly which skills to improve

---

## 🔧 Technical Details

### Database Tables Used:
- `student_skill_portfolio` - Verified skills (from quizzes)
- `skill_profile_claimed` - Claimed skills (from transcript)
- `Job_data.csv` - 50+ job listings with skill requirements

### Recommendation Algorithm:
1. Load student portfolio skills (priority)
2. Supplement with claimed skills (for coverage)
3. Compare against job requirements
4. Calculate match scores
5. Rank and return top matches

### Key Files:
- **Backend Service**: `backend/src/app/services/ml_job_recommendation_service.py`
- **API Routes**: `backend/src/app/routes/jobs.py`
- **Frontend Pages**: 
  - `frontend/src/pages/JobRecommendationsPage.jsx`
  - `frontend/src/pages/MLJobRecommendationsPage.jsx`

---

## ✅ Testing

### Test the recommendations:

1. **Check if it works now:**
```bash
# Basic recommendations
curl http://localhost:8000/students/IT21013928/jobs/recommend?top_k=5

# ML recommendations (uses portfolio)
curl "http://localhost:8000/students/IT21013928/jobs/recommend/ml?use_verified=true&top_k=5"
```

2. **From Frontend:**
- Go to Skills page
- Click "Browse Jobs" or "AI Job Matches"
- See personalized recommendations

3. **Take a quiz first:**
- Select 5 skills
- Complete quiz
- Then check job recommendations
- Should see better matches!

---

## 📈 Future Enhancements

Want even better recommendations?

1. **Add more jobs** - Update `backend/data/Job_data.csv`
2. **Train ML model** - Run `backend/scripts/model_training.py`
3. **Customize thresholds** - Adjust match percentages
4. **Add filters** - Location, salary, experience level

---

## 🎯 Summary

**Your job recommendation system is READY!**

✅ Portfolio skills (tested) have highest priority  
✅ Two recommendation engines available  
✅ Skill gap analysis included  
✅ Working frontend interfaces  

**Next Steps:**
1. Take some quizzes to build your portfolio
2. Visit the job recommendation pages
3. See personalized matches based on verified skills!
