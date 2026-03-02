# 📦 Portable Question Bank - Setup Guide

**Problem:** Every developer machine needs Ollama running to generate questions, which is:
- Slow (30-120 seconds per question)
- Resource-intensive (requires GPU/powerful CPU)
- Inconsistent (different outputs each time)
- Not scalable (can't handle multiple users)

**Solution:** Export/import system for pre-generated questions
- Generate questions **once** on integration server with Ollama
- Export to **JSON** or **CSV** file
- Commit file to Git repository
- Teammates **import** from file (no Ollama needed!)
- Student quizzes use `/quiz/from-bank` endpoint (instant <100ms)

---

## 🎯 Quick Start

### For Integration Server (Has Ollama)

```bash
# 1. Generate questions with Ollama
cd backend
python scripts/generate_and_export_questions.py

# 2. Export to portable JSON
python scripts/export_question_bank_json.py --out data/question_bank_seed.json --format flat --pretty

# 3. Commit to Git
git add data/question_bank_seed.json
git commit -m "Add pre-generated question bank"
git push
```

### For Developer Laptops (No Ollama)

```bash
# 1. Pull latest code
git pull

# 2. Import questions
cd backend
python scripts/import_question_bank_json.py

# 3. Verify import
python scripts/verify_question_bank.py
```

**Done!** Student quizzes now work instantly without Ollama.

---

## 📊 Export Scripts

### 1. Export to JSON (Primary Format)

**Script:** `backend/scripts/export_question_bank_json.py`

#### Basic Export (Flat Format)

```bash
cd backend
python scripts/export_question_bank_json.py \
  --out data/question_bank_seed.json \
  --format flat \
  --pretty
```

**Output:** `data/question_bank_seed.json`

```json
[
  {
    "id": 1,
    "skill_name": "Python Programming",
    "difficulty": "easy",
    "question": "What is a list comprehension in Python?",
    "options": [
      "A way to create lists using a single line of code",
      "A method to sort lists",
      "A function to filter lists",
      "A technique to reverse lists"
    ],
    "answer": "A",
    "explanation": "List comprehensions provide a concise way...",
    "model": "llama3.1:8b",
    "created_at": "2026-03-02T10:30:00"
  }
]
```

#### Options

```bash
# Export specific skills only
python scripts/export_question_bank_json.py \
  --skills "Python Programming" "SQL Databases" \
  --out exports/python_sql_only.json \
  --format flat \
  --pretty

# Export without answers (for practice quizzes)
python scripts/export_question_bank_json.py \
  --include_answers false \
  --out exports/practice_quiz.json

# Export grouped by skill and difficulty
python scripts/export_question_bank_json.py \
  --format grouped \
  --out exports/grouped_questions.json
```

#### Grouped Format Example

```json
{
  "generated_at": "2026-03-02T10:30:00Z",
  "total_skills": 3,
  "total_questions": 120,
  "skills": [
    {
      "skill_name": "Python Programming",
      "quizzes": [
        {
          "difficulty": "easy",
          "questions": [
            {
              "id": 1,
              "question": "What is...?",
              "options": ["...", "...", "...", "..."],
              "answer": "A",
              "explanation": "...",
              "model": "llama3.1:8b"
            }
          ]
        }
      ]
    }
  ]
}
```

---

### 2. Export to CSV (Alternative Format)

**Script:** `backend/scripts/export_question_bank_csv.py`

```bash
cd backend
python scripts/export_question_bank_csv.py --output data/question_bank_seed.csv
```

**Output:** `data/question_bank_seed.csv`

```csv
skill_name,difficulty,question_text,option_A,option_B,option_C,option_D,correct_option,explanation,model_name,created_at
Python Programming,easy,"What is a list comprehension?","A way to create lists...","A method to sort...","A function to filter...","A technique to reverse...",A,"List comprehensions provide...",llama3.1:8b,2026-03-02T10:30:00
```

**Advantages of CSV:**
- ✅ Open in Excel/Google Sheets
- ✅ Easy manual editing
- ✅ Simple format for non-developers

**Disadvantages:**
- ❌ CSV escaping issues with quotes
- ❌ Larger file size
- ❌ Less structured than JSON

---

## 📥 Import Scripts

### 1. Import from JSON (Primary)

**Script:** `backend/scripts/import_question_bank_json.py`

#### Basic Import

```bash
cd backend
python scripts/import_question_bank_json.py
```

**Default input:** `data/question_bank_seed.json`

#### Output Example

```
============================================================
  QUESTION BANK IMPORTER
============================================================

📂 Loading questions from: data/question_bank_seed.json
📊 Found 120 questions in file

🔍 Validating questions...
✅ Validation complete: 120 valid, 0 invalid

💾 Importing questions into database...
  💾 Inserted 50 questions...
  💾 Inserted 100 questions...

✅ Import complete!

📊 Summary:
   Total questions in file: 120
   Valid questions: 120
   Invalid questions: 0
   Duplicates skipped: 0
   Successfully inserted: 120

📈 Questions by skill:
   Linux Administration: 40 questions
   Python Programming: 40 questions
   SQL Databases: 40 questions

============================================================
✨ Import process completed successfully!
============================================================
```

#### Options

```bash
# Import from custom file
python scripts/import_question_bank_json.py --input exports/custom_questions.json

# Skip duplicate checking (faster, but may create duplicates)
python scripts/import_question_bank_json.py --skip-duplicate-check

# Dry run (validate only, don't insert)
python scripts/import_question_bank_json.py --dry-run
```

#### Duplicate Detection

The import script automatically detects duplicates using:
- Skill name
- Difficulty level  
- Question text (exact match)

**Duplicate Behavior:**
- ✅ Detected duplicates are **skipped**
- ✅ Report shows count: "Duplicates skipped: 15"
- ✅ No error thrown
- ✅ Database integrity maintained

**Performance:**
- With duplicate check: ~2-3 seconds per 100 questions
- Without duplicate check: ~0.5 seconds per 100 questions

---

### 2. Import from CSV (Alternative)

**Script:** `backend/scripts/import_question_bank_csv.py`

```bash
cd backend
python scripts/import_question_bank_csv.py
```

**Default input:** `data/question_bank_seed.csv`

#### Options

```bash
# Import from custom file
python scripts/import_question_bank_csv.py --input exports/custom_questions.csv

# Skip duplicate checking
python scripts/import_question_bank_csv.py --skip-duplicate-check

# Dry run
python scripts/import_question_bank_csv.py --dry-run
```

---

## ✅ Validation Rules

Both JSON and CSV imports validate:

### Required Fields
- ✅ `skill_name` - Must be non-empty
- ✅ `difficulty` - Must be "easy", "medium", or "hard"
- ✅ `question_text` or `question` - Must be non-empty
- ✅ `options` - Must have exactly 4 options (A, B, C, D)
- ✅ `correct_option` or `answer` - Must be "A", "B", "C", or "D"

### Optional Fields
- `explanation` - Added if present, empty string if missing
- `model_name` or `model` - Defaults to "llama3.1:8b"
- `created_at` - Defaults to current timestamp

### Validation Errors

**Invalid questions are skipped** with detailed error messages:

```
❌ Question 15: Missing required field: skill_name
❌ Question 23: Invalid difficulty: MEDIUM (must be easy/medium/hard)
❌ Question 42: Invalid answer: E (must be A, B, C, or D)
❌ Question 67: Options list must have exactly 4 items (has 3)
```

---

## 🔄 Complete Workflow

### Step 1: Generate Questions (Integration Server)

**Prerequisites:** Ollama installed and running

```bash
cd backend

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.1:8b

# Generate questions for all skills
python scripts/generate_and_export_questions.py

# This populates the question_bank table with questions
```

**Expected Output:**
```
Generating questions for Python Programming (easy): 10 questions
Generating questions for Python Programming (medium): 10 questions
Generating questions for Python Programming (hard): 10 questions
...
✅ Generated 120 questions in 45 minutes
```

---

### Step 2: Export to Portable Format

```bash
# Export to JSON (recommended)
python scripts/export_question_bank_json.py \
  --out data/question_bank_seed.json \
  --format flat \
  --pretty

# Also export to CSV (optional, for Excel editing)
python scripts/export_question_bank_csv.py \
  --output data/question_bank_seed.csv
```

**Output Files:**
- `backend/data/question_bank_seed.json` (primary)
- `backend/data/question_bank_seed.csv` (optional)

---

### Step 3: Commit to Git

```bash
git add backend/data/question_bank_seed.json
git add backend/data/question_bank_seed.csv
git commit -m "Add pre-generated question bank for portable deployment"
git push origin main
```

**File Sizes:**
- JSON: ~200 KB for 120 questions
- CSV: ~180 KB for 120 questions

Both are small enough to commit directly to Git.

---

### Step 4: Teammates Pull and Import

**On developer laptop (no Ollama required):**

```bash
# 1. Pull latest code
git pull

# 2. Import questions
cd backend
python scripts/import_question_bank_json.py

# 3. Verify import (optional)
python -c "
from src.app.db import SessionLocal
from src.app.models.question_bank import QuestionBank

db = SessionLocal()
count = db.query(QuestionBank).count()
print(f'✅ Question bank has {count} questions')
db.close()
"
```

**Expected Output:**
```
✅ Question bank has 120 questions
```

---

### Step 5: Run Application

```bash
# Start backend and frontend
./start.ps1

# Or manually:
cd backend/src
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd ../../frontend
npm run dev
```

**Student can now:**
1. Select skills to validate
2. Generate quiz instantly (<100ms using `/quiz/from-bank`)
3. Answer questions
4. Get results and updated portfolio

**No Ollama needed!** ✨

---

## 🔧 Maintenance

### Updating the Question Bank

**When to update:**
- New skills added to curriculum
- Existing questions need improvement
- Difficulty levels need rebalancing

**Process:**

```bash
# On integration server with Ollama

# 1. Generate new questions
cd backend
python scripts/generate_and_export_questions.py --skills "New Skill"

# 2. Export updated bank
python scripts/export_question_bank_json.py \
  --out data/question_bank_seed.json \
  --format flat \
  --pretty

# 3. Commit and push
git add data/question_bank_seed.json
git commit -m "Add questions for New Skill"
git push

# Teammates then:
git pull
python scripts/import_question_bank_json.py
# Duplicates will be automatically skipped!
```

---

### Merging Question Banks

**Scenario:** Multiple people generated questions separately

```bash
# Person A exports their questions
python scripts/export_question_bank_json.py --out bank_A.json --format flat

# Person B exports their questions
python scripts/export_question_bank_json.py --out bank_B.json --format flat

# Merge manually (JSON is just an array, concatenate them)
# Then import merged file
python scripts/import_question_bank_json.py --input merged_bank.json
# Duplicate detection prevents any conflicts!
```

---

### Verifying Question Bank Status

**Check question counts:**

```bash
cd backend
python -c "
from src.app.db import SessionLocal
from src.app.models.question_bank import QuestionBank
from sqlalchemy import func

db = SessionLocal()

# Total count
total = db.query(QuestionBank).count()
print(f'Total questions: {total}')
print()

# Breakdown by skill and difficulty
results = db.query(
    QuestionBank.skill_name,
    QuestionBank.difficulty,
    func.count(QuestionBank.id).label('count')
).group_by(
    QuestionBank.skill_name,
    QuestionBank.difficulty
).order_by(
    QuestionBank.skill_name,
    QuestionBank.difficulty
).all()

print('Breakdown:')
for skill, diff, count in results:
    print(f'  {skill} ({diff}): {count} questions')

db.close()
"
```

**Expected Output:**
```
Total questions: 120

Breakdown:
  Linux Administration (easy): 10 questions
  Linux Administration (medium): 10 questions
  Linux Administration (hard): 10 questions
  Python Programming (easy): 10 questions
  Python Programming (medium): 10 questions
  Python Programming (hard): 10 questions
  SQL Databases (easy): 10 questions
  SQL Databases (medium): 10 questions
  SQL Databases (hard): 10 questions
```

---

## 📝 File Formats Reference

### JSON Format (Flat)

```json
[
  {
    "id": 1,
    "skill_name": "Python Programming",
    "difficulty": "easy",
    "question": "What is a decorator in Python?",
    "options": [
      "A function that modifies another function",
      "A comment syntax",
      "A loop construct",
      "A variable type"
    ],
    "answer": "A",
    "explanation": "Decorators are functions that modify the behavior...",
    "model": "llama3.1:8b",
    "created_at": "2026-03-02T10:30:00"
  }
]
```

**Field Mappings:**
- `question` or `question_text` → question_text
- `answer` or `correct_option` → correct_option
- `model` or `model_name` → model_name
- `options` can be list or dict

---

### JSON Format (Grouped)

```json
{
  "generated_at": "2026-03-02T10:30:00Z",
  "total_skills": 1,
  "total_questions": 1,
  "skills": [
    {
      "skill_name": "Python Programming",
      "quizzes": [
        {
          "difficulty": "easy",
          "questions": [
            {
              "id": 1,
              "question": "What is...?",
              "options": ["...", "...", "...", "..."],
              "answer": "A",
              "explanation": "...",
              "model": "llama3.1:8b"
            }
          ]
        }
      ]
    }
  ]
}
```

---

### CSV Format

```csv
skill_name,difficulty,question_text,option_A,option_B,option_C,option_D,correct_option,explanation,model_name,created_at
"Python Programming","easy","What is a decorator?","A function that modifies another function","A comment syntax","A loop construct","A variable type","A","Decorators are functions that modify...","llama3.1:8b","2026-03-02T10:30:00"
```

**Notes:**
- Fields with commas or quotes must be quoted
- Use double quotes `""` to escape quotes inside fields
- UTF-8 encoding required

---

## 🚀 Performance Comparison

| Method                | Time per Question | Scalability | Dependencies        |
|----------------------|-------------------|-------------|---------------------|
| **Ollama Generation** | 3-10 seconds      | ❌ Poor      | Ollama + ChromaDB   |
| **Question Bank**     | <10 ms            | ✅✅✅ Excellent | MySQL only          |

### Real-World Timings

**Generating 120 questions with Ollama:**
- Total time: **45-60 minutes**
- Per question: **~30 seconds**
- Requires: GPU or powerful CPU

**Importing 120 questions from JSON:**
- Total time: **2-3 seconds**
- Per question: **~25 ms**
- Requires: Nothing special

**Generating quiz from question bank:**
- Total time: **<100 ms**
- Questions per quiz: 12
- Requires: MySQL only

**Conclusion:** Generate once, use forever! 🎯

---

## 🐛 Troubleshooting

### Issue: Import script not finding file

**Error:**
```
❌ File not found: backend/data/question_bank_seed.json
```

**Solution:**
```bash
# Check file exists
ls backend/data/question_bank_seed.json

# Or specify full path
python scripts/import_question_bank_json.py --input /full/path/to/file.json
```

---

### Issue: Validation errors during import

**Error:**
```
❌ Question 15: Invalid difficulty: MEDIUM (must be easy/medium/hard)
```

**Solution:**
- Open JSON/CSV file
- Find question 15
- Fix difficulty: `"MEDIUM"` → `"medium"`
- Re-run import

**Tip:** Use `--dry-run` flag to validate without importing:
```bash
python scripts/import_question_bank_json.py --dry-run
```

---

### Issue: All questions marked as duplicates

**Error:**
```
📊 Summary:
   Duplicates skipped: 120
   Successfully inserted: 0
```

**Cause:** Questions already exist in database

**Solution:**
```bash
# Option 1: Skip duplicate check (not recommended)
python scripts/import_question_bank_json.py --skip-duplicate-check

# Option 2: Clear database first (dangerous!)
# Only do this if you're sure!
mysql -u root -p -e "DELETE FROM skillbridge_db.question_bank;"
python scripts/import_question_bank_json.py
```

---

### Issue: Export produces empty file

**Error:**
```
⚠️ Warning: No questions found in question_bank table
```

**Cause:** Database has no questions yet

**Solution:**
```bash
# Generate questions first
cd backend
python scripts/generate_and_export_questions.py
```

---

## 📚 Related Documentation

- **[QUIZ_WORKFLOW_GUIDE.md](QUIZ_WORKFLOW_GUIDE.md)** - Complete quiz system workflow
- **[GENERATE_AND_EXPORT_API.md](GENERATE_AND_EXPORT_API.md)** - Question generation details
- **[ENDPOINT_MAPPING_GUIDE.md](ENDPOINT_MAPPING_GUIDE.md)** - API endpoints reference
- **[README.md](README.md)** - Project setup

---

## ✅ Checklist for New Team Members

**First-time setup (no Ollama):**

- [ ] Clone repository: `git clone ...`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Setup MySQL database: `python scripts/init_mysql_db.py`
- [ ] Import question bank: `python scripts/import_question_bank_json.py`
- [ ] Verify import: Check question counts
- [ ] Start application: `./start.ps1`
- [ ] Test quiz: Use `/quiz/from-bank` endpoint

**Total time: <10 minutes** ⚡

---

## 🎯 Summary

### What You Can Do

✅ **Export** question bank to JSON/CSV  
✅ **Import** pre-generated questions  
✅ **Share** question bank via Git  
✅ **Deploy** without Ollama dependency  
✅ **Generate quizzes** instantly (<100ms)  
✅ **Scale** to thousands of users  

### What You Don't Need

❌ Ollama running on every machine  
❌ ChromaDB for RAG  
❌ GPU or powerful CPU  
❌ 30+ seconds per question  
❌ Internet connection (after import)  

### File Recommendations

| Use Case                  | Format | File Name                    |
|--------------------------|--------|------------------------------|
| Production deployment    | JSON   | `question_bank_seed.json`    |
| Manual editing           | CSV    | `question_bank_seed.csv`     |
| Skill-specific export    | JSON   | `{skill}_questions.json`     |
| Practice quizzes         | JSON   | `practice_no_answers.json`   |

---

**Last Updated:** March 2, 2026  
**Version:** 1.0  
**Status:** ✅ Production Ready
