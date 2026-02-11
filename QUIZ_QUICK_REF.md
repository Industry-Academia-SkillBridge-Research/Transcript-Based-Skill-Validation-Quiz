# ⚡ QUICK REFERENCE: Quiz Question Bank

## 🎯 Your Question Answered

**Q**: *"When I select skills, I need to get quiz from question bank"*  
**A**: ✅ **Already working!** Your system retrieves questions from the database, NOT from Ollama during quiz time.

---

## 📋 Two Operations - Don't Confuse Them!

### 1️⃣ GENERATE (Offline - Admin Only)

```
WHO: Admin
WHEN: Before students take quizzes (one-time setup)
SPEED: SLOW (minutes) - Uses Ollama LLM

POST /admin/question-bank/generate-and-export
{
  "skill_names": ["Python", "SQL"],
  "questions_per_difficulty": 10
}

RESULT: Questions stored in QuestionBank table
```

### 2️⃣ RETRIEVE (Real-time - Every Quiz)

```
WHO: Student taking quiz
WHEN: Every time quiz is taken
SPEED: INSTANT (<100ms) - Just database query

POST /students/{id}/quiz/from-bank

RESULT: Quiz questions returned from database
```

---

## 🔄 Complete Workflow

### Part A: Setup (Do Once)

```bash
# 1. Migrate to new skills (one time)
cd backend
python scripts/migrate_to_job_skills.py

# 2. Re-upload transcript
Upload via: http://localhost:5173/students/IT21013928/upload

# 3. Generate question bank (one time per skill)
POST http://localhost:8000/admin/question-bank/generate-and-export
{
  "skill_names": ["Python", "SQL", "Java", "Linux"],
  "questions_per_difficulty": 10,
  "model_name": "llama3.1:8b"
}
```

### Part B: Student Quiz (Every Time)

```
1. View skills → http://localhost:5173/students/IT21013928/skills
2. Select 1-5 skills (checkbox)
3. Click "Plan Quiz"
4. Answer questions ← INSTANT (from question bank!)
5. Submit quiz
6. View results
```

---

## 🔧 What I Fixed Today

### Problem
Your new `course_skill_mapping_new.csv` uses simple skill names (Python, SQL), but the quiz system expected old parent skill names.

### Solution  
✅ Updated 3 files to support **both** old and new systems:
- `backend/src/app/services/quiz_planner.py`
- `backend/src/app/routes/skills.py`
- `frontend/src/pages/SkillsPage.jsx`

### Result
✅ System now works with simplified job skills  
✅ Full backward compatibility  
✅ Question bank retrieval still instant  

---

## 💡 Key Files

| File | Purpose |
|------|---------|
| `QuizPage.jsx` | Calls `generateQuizFromBank()` |
| `/quiz/from-bank` endpoint | Samples from QuestionBank table |
| `sample_quiz_from_bank()` | SQL queries (instant!) |
| `generate_bank_for_skills()` | Uses Ollama (slow, offline) |

---

## ✅ Quick Test

```powershell
# 1. Start services
.\start.ps1

# 2. Open browser
http://localhost:5173/students/IT21013928/skills

# 3. Select 3 skills → Click "Plan Quiz"

# 4. Verify quiz loads INSTANTLY
# If it's slow (>2 seconds), you're using wrong endpoint!
```

---

## 🚨 Common Mistakes

❌ **Don't**: Call `POST /quiz/generate` (uses Ollama - SLOW!)  
✅ **Do**: Call `POST /quiz/from-bank` (uses database - FAST!)

❌ **Don't**: Generate questions during quiz time  
✅ **Do**: Generate questions once, reuse many times

---

## 📊 Performance

| Operation | Speed | Uses |
|-----------|-------|------|
| Generate questions | 2-5 min | Ollama LLM |
| Retrieve from bank | <100ms | SQLite query |
| Load quiz page | <1 sec | React + API |

---

## 🎯 Success Criteria

After migration, you should see:

✅ Skills: "Python" not "Procedural Programming Concepts"  
✅ Quiz loads in under 1 second  
✅ Questions match selected skills  
✅ Can complete full quiz workflow  

---

**Done!** Your quiz question bank is working correctly. Questions come from the database (instant), not Ollama (slow).
