# 🚀 Active Working Files - SkillBridge Project

## Overview
This document lists **ONLY the active working files** in the SkillBridge system. Files are organized by workflow and purpose.

**System Type:** Direct Job Skills Mapping (65 industry-standard skill tags)

---

## 📁 Project Structure by Workflow

### 🔧 **1. Core Backend Infrastructure**

#### Main Application
```
backend/src/app/
├── main.py                    # FastAPI application entry point
├── db.py                      # Database configuration & SessionLocal
├── config.py                  # Environment configuration
└── __init__.py
```

#### Database Models
```
backend/src/app/models/
├── student.py                          # Student profile model
├── course.py                           # CourseTaken, CourseCatalog, CourseSkillMap
├── skill.py                            # SkillScore, ChildSkill models
├── quiz.py                             # Quiz, QuizQuestion models
├── quiz_answer.py                      # QuizAnswer model
├── question_bank.py                    # QuestionBank model
├── student_skill_portfolio.py          # StudentSkillPortfolio model
├── skill_profile_verified_parent.py    # SkillProfileVerifiedParent model
├── skill_profile_final_parent.py       # SkillProfileFinalParent model
└── skill_group_map.py                  # SkillGroupMap model (legacy mapping)
```

#### API Schemas (Request/Response validation)
```
backend/src/app/schemas/
├── transcript.py              # TranscriptUpload, CourseExtraction schemas
├── skill.py                   # SkillScore, SkillProfile schemas
├── quiz.py                    # QuizGenerate, QuizResponse schemas
└── quiz_submit.py             # QuizSubmit, QuizResult schemas
```

---

### 📤 **2. Transcript Upload & Processing Workflow**

#### API Routes
```
backend/src/app/routes/
└── transcript.py              # POST /upload - Upload transcript PDF
                              # GET /students/{id} - Get student details
                              # GET /students/{id}/courses - Get courses
```

#### Services
```
backend/src/app/services/
└── transcript_service.py      # extract_text_from_pdf()
                              # parse_transcript_text()
                              # save_to_database()
```

**Flow:**
1. Upload PDF → `transcript.py` route
2. Extract text → `transcript_service.extract_text_from_pdf()`
3. Parse courses → `transcript_service.parse_transcript_text()`
4. Save to DB → Student, CourseTaken tables
5. Auto-compute skills → Triggered after save

---

### 🎯 **3. Skill Scoring Workflow (Job Skills)**

#### API Routes
```
backend/src/app/routes/
├── skills.py                  # GET /skills/student/{id} - Get all skills
                              # GET /skills/student/{id}/job - Get job skills
└── parent_skills.py           # GET /skills/student/{id}/parent - Parent skills
```

#### Services
```
backend/src/app/services/
├── skill_scoring.py           # compute_skill_scores() - Child skills
├── job_skill_scoring.py       # compute_job_skill_scores() - PRIMARY
└── parent_skill_scoring.py    # compute_parent_skill_scores() - Aggregation
```

#### Key Algorithm (skill_scoring.py)
```python
# For each skill:
contribution = grade_normalized × map_weight × credits × recency
evidence_weight = map_weight × credits × recency

skill_score = (Σ contributions / Σ evidence_weights) × 100

# Where:
grade_normalized = GPA / 4.0
recency = e^(-0.4 × years_since_course)
map_weight = 0-1 (from course_skill_map.csv)
```

**Flow:**
1. Student uploads transcript → Courses saved
2. System queries `course_skill_map.csv`
3. For each course-skill mapping:
   - Calculate contribution & evidence
   - Aggregate by skill
4. Compute 65 job skill scores (PYTHON, SQL, etc.)
5. Store in `skill_scores` table

---

### 📝 **4. Quiz Generation & Execution Workflow**

#### API Routes
```
backend/src/app/routes/
└── quiz.py                    # POST /quiz/generate - Generate quiz
                              # POST /quiz/{id}/submit - Submit answers
                              # GET /quiz/{id} - Get quiz details
                              # GET /quiz/{id}/results - Get results
```

#### Services
```
backend/src/app/services/
├── quiz_planner.py            # plan_adaptive_quiz() - Question difficulty
├── question_bank_service.py   # get_questions_from_bank() - PRIMARY
├── quiz_generation_llama.py   # generate_quiz_llama() - AI generation
├── quiz_scoring.py            # score_quiz() - Calculate quiz scores
├── quiz_scoring_service.py    # enhanced_quiz_scoring() - Advanced scoring
└── ollama_client.py           # LLM client for question generation
```

#### Two Question Sources

**A. Question Bank (PRIMARY)**
```
question_bank_service.py
├── Get questions from database (question_bank table)
├── Filter by selected skills
├── Balance difficulty levels
└── Return structured questions
```

**B. AI Generation (OPTIONAL)**
```
quiz_generation_llama.py
├── Use Ollama (llama3.2) 
├── ChromaDB vector store for RAG
├── Generate context-aware MCQs
└── Fallback to question bank
```

**Flow:**
1. User selects skills → `POST /quiz/generate`
2. Quiz planner creates difficulty distribution
3. Fetch questions from bank OR generate with AI
4. Create Quiz + QuizQuestion records
5. Return quiz_id to frontend
6. User answers → `POST /quiz/{id}/submit`
7. Score quiz → Update verified skills
8. Show results

---

### 📊 **5. Results & Portfolio Workflow**

#### API Routes
```
backend/src/app/routes/
├── profile.py                 # GET /profile/portfolio/{id} - Portfolio
                              # GET /profile/verified-skills/{id}
└── xai.py                     # GET /xai/explain/child-skill/{id}/{skill}
                              # GET /xai/explain/parent-skill/{id}/{skill}
```

#### Services
```
backend/src/app/services/
└── xai_service.py             # explain_skill_score() - Explainability
                              # get_contributing_courses()
                              # explain_parent_skill()
```

**Flow:**
1. User completes quiz
2. System calculates verified scores
3. Generate portfolio data
4. Show skill breakdown with evidence
5. Explain how each score was derived

---

### 💼 **6. Job Recommendation Workflow**

#### API Routes
```
backend/src/app/routes/
└── jobs.py                    # GET /jobs/recommendations/{id}
                              # GET /jobs/{job_id}
                              # GET /jobs/search
```

#### Services
```
backend/src/app/services/
└── job_recommendation_service.py
    ├── recommend_jobs() - Match skills to jobs
    ├── calculate_job_match_score()
    └── get_top_recommendations()
```

**Flow:**
1. System has verified job skills
2. Match against job requirements (Job_data.csv)
3. Calculate match percentage
4. Rank and return top jobs
5. Show skill gaps for each role

---

### 🎨 **Frontend Application**

#### Main Files
```
frontend/src/
├── main.jsx                   # React app entry
├── App.jsx                    # Router configuration
├── App.css
└── index.css
```

#### Pages (User Journey)
```
frontend/src/pages/
├── UploadPage.jsx             # 1. Upload transcript PDF
├── TranscriptPage.jsx         # 2. View extracted courses
├── SkillsPage.jsx             # 3. View computed job skills
├── QuizPage.jsx               # 4. Take validation quiz
├── ResultsPage.jsx            # 5. View quiz results
├── PortfolioPage.jsx          # 6. See verified skills portfolio
├── JobRecommendationsPage.jsx # 7. Browse matching jobs
├── JobDetailPage.jsx          # 8. View job requirements
├── SkillExplainPage.jsx       # Explain job skill derivation
├── ExplainChildSkillPage.jsx  # Explain child skill details
└── ExplainParentSkillPage.jsx # Explain parent skill aggregation
```

#### Components
```
frontend/src/components/
├── SkillCard.jsx              # Reusable skill display card
└── ui/                        # shadcn/ui components
    ├── Button.jsx
    ├── Card.jsx
    ├── Input.jsx
    ├── Table.jsx
    ├── Spinner.jsx
    └── ErrorAlert.jsx
```

---

### 📊 **Data Files (Active)**

#### Core Skill Mappings
```
backend/data/
├── job_skills.csv                     # 65 canonical job skills (PRIMARY)
├── course_skill_map.csv               # Course → Child Skill mappings (ACTIVE)
├── childskill_to_jobskill_map.csv     # Child → Job Skill mappings (ACTIVE)
├── job_skill_to_parent_skill.csv      # Job → Parent Skill mappings
├── course_catalog.csv                 # Course metadata
├── Job_data.csv                       # Job postings for recommendations
├── Job_data.json                      # Job data in JSON format
└── job_parent_skill_features.csv      # Job-parent skill requirements
```

#### Knowledge Base (for AI Quiz Generation)
```
backend/data/knowledge_base/
└── [Various text files with course content for RAG]
```

#### Legacy Files (NOT USED in current workflow)
```
❌ child_skills_unique.csv           # Old child skills list
❌ parent_skills_unique.csv          # Old parent skills list
❌ skill_group_map.csv               # Legacy skill grouping
❌ course_skill_mapping.csv          # Old mapping format
❌ course_skill_mapping_new.csv      # Old mapping format
```

---

### 🛠️ **Utility Scripts**

#### Active Scripts
```
backend/scripts/
├── build_job_skill_maps.py            # Generate job skill mappings
├── build_job_parent_features.py       # Build job-parent features
├── generate_and_export_questions.py   # Pre-generate questions
├── export_question_bank_json.py       # Export questions to JSON
├── model_training.py                  # Train ML model for skill prediction
├── test_model.py                      # Test trained ML model
└── convert_mapping_wide_to_long.py    # Convert mapping formats
```

#### Legacy/Test Scripts (NOT NEEDED)
```
❌ migrate_to_job_skills.py          # One-time migration (already done)
❌ test_job_skill_support.py         # Testing script
❌ test_export.py                    # Testing script
```

---

### ⚙️ **Configuration Files**

#### Backend
```
backend/
├── requirements.txt           # Python dependencies
└── src/app.db                 # SQLite database (generated)
```

#### Frontend
```
frontend/
├── package.json               # Node.js dependencies
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS config
├── tsconfig.json              # TypeScript config
├── components.json            # shadcn/ui config
└── index.html                 # HTML template
```

#### Project Root
```
├── start.ps1                  # PowerShell start script
├── stop.ps1                   # PowerShell stop script
└── .gitignore
```

---

### 📚 **Documentation Files (Active)**

```
Project Root:
├── COMPLETE_PROJECT_DOCUMENTATION.md  # Comprehensive guide (2300+ lines)
├── README.md                         # Quick start guide
├── READY_TO_USE.md                   # Production readiness checklist
├── SKILL_SCORING_ALGORITHM.md        # Scoring algorithm details
├── QUIZ_WORKFLOW_GUIDE.md            # Quiz generation workflow
├── JOB_SKILL_IMPLEMENTATION.md       # Job skills feature docs
├── VISUAL_SUMMARY.md                 # Visual architecture diagrams
├── MODEL_TRAINING_README.md          # ML model training guide
└── ACTIVE_WORKING_FILES.md           # This file

backend/:
├── ENDPOINT_MAPPING_GUIDE.md         # API endpoint reference
├── GENERATE_AND_EXPORT_API.md        # Question generation API
└── EXPORT_QUESTION_BANK_GUIDE.md     # Question bank export guide

frontend/:
├── FRONTEND_README.md                # Frontend setup guide
├── AUTHENTICATION_GUIDE.md           # Auth implementation
└── EXPLANATION_PAGES_GUIDE.md        # XAI pages guide
```

---

## 🔄 Complete Data Flow

### **End-to-End System Flow**

```
1. UPLOAD TRANSCRIPT
   ↓
   UploadPage.jsx → POST /upload → transcript_service.py
   ↓
   Extract PDF text → Parse courses → Save to database
   ↓
   Student + CourseTaken records created

2. AUTO-COMPUTE SKILLS (triggered automatically)
   ↓
   skill_scoring.py → Calculate child skill scores
   ↓
   job_skill_scoring.py → Aggregate to 65 job skills (PYTHON, SQL, etc.)
   ↓
   parent_skill_scoring.py → Roll up to 27 parent skills
   ↓
   SkillScore records created

3. VIEW SKILLS
   ↓
   SkillsPage.jsx → GET /skills/student/{id}/job
   ↓
   Display 65 job skills with scores (0-100)

4. GENERATE QUIZ
   ↓
   QuizPage.jsx → POST /quiz/generate
   ↓
   quiz_planner.py → Plan difficulty distribution
   ↓
   question_bank_service.py → Fetch questions from database
   OR
   quiz_generation_llama.py → Generate with AI (Ollama + ChromaDB)
   ↓
   Quiz + QuizQuestion records created

5. TAKE QUIZ
   ↓
   User answers questions → POST /quiz/{id}/submit
   ↓
   quiz_scoring_service.py → Score answers
   ↓
   Update verified skill scores

6. VIEW RESULTS
   ↓
   ResultsPage.jsx → GET /quiz/{id}/results
   ↓
   Show claimed vs verified scores

7. VIEW PORTFOLIO
   ↓
   PortfolioPage.jsx → GET /profile/portfolio/{id}
   ↓
   Display verified job skills

8. JOB RECOMMENDATIONS
   ↓
   JobRecommendationsPage.jsx → GET /jobs/recommendations/{id}
   ↓
   job_recommendation_service.py → Match skills to jobs
   ↓
   Display ranked job matches with skill gaps
```

---

## 🎯 Key Active Features

### ✅ Implemented & Working

1. **PDF Transcript Upload** - Automatic course extraction
2. **65 Job Skills System** - Industry-standard skill tags (PYTHON, SQL, JAVA, etc.)
3. **Advanced Scoring Algorithm** - Time-decay + credit-weighting + performance
4. **Question Bank System** - 200+ pre-generated questions
5. **AI Quiz Generation** - Ollama (llama3.2) with ChromaDB RAG
6. **Adaptive Quiz Planning** - Difficulty-balanced question selection
7. **Skill Verification** - Quiz-based validation with confidence scoring
8. **Explainable AI (XAI)** - Show how every score is calculated
9. **Job Recommendations** - Match verified skills to job postings
10. **Portfolio Export** - Professional skill profile generation
11. **ML Model Training** - Random Forest for skill score prediction

---

## 🗄️ Database Tables (Active)

### Core Tables
- `students` - Student profiles
- `courses_taken` - Student course history
- `skill_scores` - Computed skill scores (child skills)
- `course_catalog` - Course metadata
- `course_skill_map` - Course → Skill mappings

### Quiz Tables
- `quizzes` - Quiz metadata
- `quiz_questions` - Questions in each quiz
- `quiz_answers` - Student answers
- `question_bank` - Pre-generated questions

### Portfolio Tables
- `student_skill_portfolio` - Verified skill profiles
- `skill_profile_verified_parent` - Verified parent skills
- `skill_profile_final_parent` - Final parent skill scores

### Job Tables
- Jobs data stored in CSV (Job_data.csv)

---

## 📦 Dependencies

### Backend (Python 3.10+)
```
fastapi
uvicorn
sqlalchemy
pydantic
python-multipart
pdfplumber
pymupdf
sentence-transformers
chromadb
ollama
scikit-learn
matplotlib
seaborn
pandas
numpy
```

### Frontend (Node.js 18+)
```
react 19.2
react-router-dom v6
vite
tailwindcss
axios
lucide-react
shadcn/ui components
```

---

## 🚀 Quick Start Commands

### Backend
```powershell
cd backend/src
python -m uvicorn app.main:app --reload
```

### Frontend
```powershell
cd frontend
npm run dev
```

### Both (from project root)
```powershell
.\start.ps1
```

---

## 🔗 API Endpoints (Active)

### Transcript
- `POST /upload` - Upload transcript PDF
- `GET /students/{id}` - Get student details
- `GET /students/{id}/courses` - Get student courses

### Skills
- `GET /skills/student/{id}` - Get all skill scores
- `GET /skills/student/{id}/job` - Get job skill scores (PRIMARY)
- `GET /skills/student/{id}/parent` - Get parent skill scores

### Quiz
- `POST /quiz/generate` - Generate new quiz
- `GET /quiz/{id}` - Get quiz details
- `POST /quiz/{id}/submit` - Submit quiz answers
- `GET /quiz/{id}/results` - Get quiz results

### Profile
- `GET /profile/portfolio/{id}` - Get skill portfolio
- `GET /profile/verified-skills/{id}` - Get verified skills

### Jobs
- `GET /jobs/recommendations/{id}` - Get job recommendations
- `GET /jobs/{job_id}` - Get job details
- `GET /jobs/search` - Search jobs

### XAI (Explainability)
- `GET /xai/explain/child-skill/{id}/{skill}` - Explain child skill
- `GET /xai/explain/parent-skill/{id}/{skill}` - Explain parent skill

### Admin
- `POST /admin/seed` - Seed initial data
- Question bank management endpoints

---

## 🎓 Machine Learning Component

### Model Training
```
backend/scripts/model_training.py
├── Extract training data from database
├── Features: grade_normalized, credits, recency, map_weight
├── Target: skill_score (0-100)
├── Algorithm: Random Forest Regressor (100 trees)
├── Metrics: MSE, RMSE, MAE, R²
└── Output: backend/models/skill_score_model.pkl
```

### Model Testing
```
backend/scripts/test_model.py
├── Load trained model
├── Test with sample data
├── Interactive prediction mode
└── Skill level classification
```

---

## 📈 Project Statistics

- **Backend Routes:** 10+ API route files
- **Services:** 15+ service modules
- **Database Models:** 12+ SQLAlchemy models
- **Frontend Pages:** 11 React pages
- **Job Skills:** 65 canonical tags
- **Child Skills:** 135 granular skills
- **Parent Skills:** 27 competency areas
- **Question Bank:** 200+ questions
- **Job Postings:** 100+ job listings
- **Documentation:** 15+ markdown files (8000+ lines)

---

## ✅ Production Checklist

- [x] PDF transcript parsing works
- [x] Skill scoring algorithm implemented
- [x] Job skills system operational
- [x] Question bank populated
- [x] Quiz generation (bank + AI) working
- [x] Quiz scoring functional
- [x] Job recommendations active
- [x] Portfolio generation ready
- [x] XAI explanations implemented
- [x] ML model training pipeline created
- [x] Frontend UI complete
- [x] API documentation ready
- [ ] Add authentication (future)
- [ ] Deploy to production (future)
- [ ] Clean up legacy files (future)

---

## 🎯 Next Steps

1. **Test ML Model** - Run `python model_training.py` to train
2. **Clean Legacy Files** - Remove child/parent skill CSV files
3. **Add Authentication** - JWT-based user authentication
4. **Deploy Backend** - Deploy FastAPI to cloud (AWS/Azure)
5. **Deploy Frontend** - Deploy React app to Vercel/Netlify
6. **Performance Testing** - Load testing with multiple users
7. **Documentation** - API documentation with Swagger/OpenAPI

---

**Last Updated:** February 12, 2026  
**Project Status:** ✅ Fully Functional - Ready for Testing  
**Active Skill System:** Job Skills (65 canonical tags)
