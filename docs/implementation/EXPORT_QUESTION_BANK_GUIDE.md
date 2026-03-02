# Question Bank Export Guide

Complete guide for exporting quiz questions from the QuestionBank database to JSON files.

## Overview

The system provides three ways to export questions:

1. **CLI Script** - Export existing questions from database
2. **API Endpoint** - Export via HTTP GET request
3. **Combined Script** - Generate + Export in one command

---

## 1. CLI Export Script

Export questions from the database to JSON files.

### Basic Usage

```bash
# Export all questions (grouped format)
python backend/scripts/export_question_bank_json.py

# Export specific skills
python backend/scripts/export_question_bank_json.py --skills SQL Python "Data Structures"

# Export to custom path
python backend/scripts/export_question_bank_json.py --out exports/my_quiz.json
```

### Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--skills` | list | None | Skills to export (all if omitted) |
| `--out` | path | `exports/question_bank_export.json` | Output file path |
| `--format` | choice | `grouped` | Export format: `grouped` or `flat` |
| `--include_answers` | bool | `true` | Include correct answers |
| `--include_explanations` | bool | `true` | Include explanations |
| `--force` | flag | False | Overwrite existing file |
| `--pretty` | flag | False | Pretty-print JSON |

### Examples

```bash
# Export SQL questions without answers (for student quizzes)
python backend/scripts/export_question_bank_json.py \
  --skills SQL \
  --include_answers false \
  --out student_quiz.json \
  --pretty

# Export multiple skills in flat format
python backend/scripts/export_question_bank_json.py \
  --skills Python "Machine Learning" SQL \
  --format flat \
  --out exports/all_questions_flat.json

# Export with explanations but no answers
python backend/scripts/export_question_bank_json.py \
  --skills "Data Structures" \
  --include_answers false \
  --include_explanations true
```

---

## 2. API Endpoint

Export questions via HTTP GET request.

### Endpoint

```
GET /admin/question-bank/export
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skills` | array | None | Specific skills (all if omitted) |
| `format` | string | `grouped` | `grouped` or `flat` |
| `include_answers` | boolean | `true` | Include correct answers |
| `include_explanations` | boolean | `true` | Include explanations |

### Examples

```bash
# Export all questions (grouped)
curl http://localhost:8000/admin/question-bank/export

# Export specific skills
curl "http://localhost:8000/admin/question-bank/export?skills=Python&skills=SQL"

# Flat format without answers
curl "http://localhost:8000/admin/question-bank/export?format=flat&include_answers=false"

# Save to file
curl "http://localhost:8000/admin/question-bank/export?skills=Python" > python_quiz.json
```

### Response Formats

#### Grouped Format (Default)

Questions organized by skill → difficulty → questions.

```json
{
  "generated_at": "2024-01-15T10:30:00Z",
  "total_skills": 2,
  "total_questions": 60,
  "skills": [
    {
      "skill_name": "Python Programming",
      "quizzes": [
        {
          "difficulty": "easy",
          "questions": [
            {
              "id": 1,
              "question": "What is a Python list?",
              "options": [
                "An ordered collection",
                "A key-value store",
                "A function",
                "A class"
              ],
              "answer": "A",
              "explanation": "Lists are ordered, mutable collections in Python.",
              "source": "ollama",
              "model": "llama3.1:8b"
            }
          ]
        },
        {
          "difficulty": "medium",
          "questions": [ /* ... */ ]
        },
        {
          "difficulty": "hard",
          "questions": [ /* ... */ ]
        }
      ]
    },
    {
      "skill_name": "SQL",
      "quizzes": [ /* ... */ ]
    }
  ]
}
```

**Use Case**: Quiz UI that groups questions by difficulty levels.

#### Flat Format

Simple list of all questions.

```json
[
  {
    "id": 1,
    "skill_name": "Python Programming",
    "difficulty": "easy",
    "question": "What is a Python list?",
    "options": [
      "An ordered collection",
      "A key-value store",
      "A function",
      "A class"
    ],
    "answer": "A",
    "explanation": "Lists are ordered, mutable collections in Python.",
    "model": "llama3.1:8b",
    "created_at": "2024-01-15T10:00:00"
  },
  {
    "id": 2,
    "skill_name": "Python Programming",
    "difficulty": "easy",
    "question": "What keyword defines a function?",
    "options": ["def", "func", "function", "define"],
    "answer": "A",
    "explanation": "The 'def' keyword is used to define functions in Python.",
    "model": "llama3.1:8b",
    "created_at": "2024-01-15T10:01:30"
  }
]
```

**Use Case**: Data analysis, bulk processing, simple iteration.

---

## 3. Generate + Export (Combined)

Generate questions using Ollama and immediately export to JSON.

### Basic Usage

```bash
# Generate 10 questions per difficulty for SQL and Python
python backend/scripts/generate_and_export_questions.py \
  --skills SQL Python \
  --count 10

# Custom model and output path
python backend/scripts/generate_and_export_questions.py \
  --skills "Machine Learning" \
  --count 15 \
  --model llama3.1:8b \
  --out exports/ml_quiz.json
```

### Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--skills` | list | **required** | Skills to generate for |
| `--count` | int | 10 | Questions per difficulty (max: 50) |
| `--model` | string | `llama3.1:8b` | Ollama model name |
| `--out` | path | `exports/questions_TIMESTAMP.json` | Output file |
| `--format` | choice | `grouped` | `grouped` or `flat` |
| `--include_answers` | bool | `true` | Include answers in export |
| `--include_explanations` | bool | `true` | Include explanations |
| `--force` | flag | False | Overwrite existing file |
| `--skip_generation` | flag | False | Only export (skip generation) |

### Examples

```bash
# Generate and export SQL questions
python backend/scripts/generate_and_export_questions.py \
  --skills SQL \
  --count 15 \
  --out exports/sql_quiz_20240115.json

# Generate for multiple skills
python backend/scripts/generate_and_export_questions.py \
  --skills Python "Data Structures" "Machine Learning" \
  --count 10 \
  --model llama3.1:8b

# Generate but export without answers (student version)
python backend/scripts/generate_and_export_questions.py \
  --skills Python \
  --count 10 \
  --include_answers false \
  --out student_python_quiz.json

# Only export existing questions (skip generation)
python backend/scripts/generate_and_export_questions.py \
  --skills SQL \
  --skip_generation \
  --out exports/sql_existing.json
```

### Output Example

```
Generating questions for 2 skill(s)...
  Skills: SQL, Python
  Questions per difficulty: 10
  Model: llama3.1:8b
  Total expected: 60 questions

Generation complete:
  ✓ Generated: 58/60
  - Duplicates skipped: 2
  - Errors: 0

Exporting questions to JSON...
✓ Export complete:
  File: exports/questions_20240115_143022.json
  Format: grouped
  Questions: 58
  Skills: SQL, Python
  Answers included: True
  Explanations included: True
```

---

## Common Workflows

### Workflow 1: Create Student Quiz (No Answers)

```bash
# Generate questions without answers
python backend/scripts/generate_and_export_questions.py \
  --skills "Data Structures" "Algorithms" \
  --count 15 \
  --include_answers false \
  --out student_quiz.json \
  --force
```

### Workflow 2: Create Answer Key

```bash
# Export only answers for grading
python backend/scripts/export_question_bank_json.py \
  --skills "Data Structures" "Algorithms" \
  --format flat \
  --include_explanations false \
  --out answer_key.json
```

### Workflow 3: Batch Export All Skills

```bash
# Export each skill to separate file
for skill in "Python" "SQL" "Data Structures" "Machine Learning"; do
  python backend/scripts/export_question_bank_json.py \
    --skills "$skill" \
    --out "exports/${skill// /_}_quiz.json" \
    --pretty \
    --force
done
```

### Workflow 4: API Export with Postman/Frontend

```javascript
// Fetch questions for quiz
const response = await fetch(
  '/admin/question-bank/export?skills=Python&format=grouped&include_answers=false'
);
const quizData = await response.json();

// Use in quiz component
quizData.skills.forEach(skill => {
  skill.quizzes.forEach(quiz => {
    renderQuiz(quiz.difficulty, quiz.questions);
  });
});
```

---

## JSON Schema Reference

### Grouped Format Schema

```json
{
  "generated_at": "ISO 8601 timestamp",
  "total_skills": "number",
  "total_questions": "number",
  "skills": [
    {
      "skill_name": "string",
      "quizzes": [
        {
          "difficulty": "easy|medium|hard",
          "questions": [
            {
              "id": "number (database ID)",
              "question": "string",
              "options": ["string", "string", "string", "string"],
              "answer": "A|B|C|D (optional)",
              "explanation": "string (optional)",
              "source": "ollama",
              "model": "string (model name)"
            }
          ]
        }
      ]
    }
  ]
}
```

### Flat Format Schema

```json
[
  {
    "id": "number",
    "skill_name": "string",
    "difficulty": "easy|medium|hard",
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "answer": "A|B|C|D (optional)",
    "explanation": "string (optional)",
    "model": "string",
    "created_at": "ISO 8601 timestamp or null"
  }
]
```

---

## Validation & Safety

### Before Exporting

```bash
# Check how many questions exist
curl http://localhost:8000/admin/question-bank/stats

# Check specific skill count
python backend/scripts/export_question_bank_json.py --skills SQL --out /tmp/test.json
```

### Validate JSON

```bash
# Pretty-print and validate
python -m json.tool exports/quiz.json

# Count questions in flat format
jq 'length' exports/flat_quiz.json

# Count questions in grouped format
jq '[.skills[].quizzes[].questions[]] | length' exports/grouped_quiz.json
```

---

## Troubleshooting

### No questions exported

**Problem**: Script says "No questions found"

**Solution**:
```bash
# Check database
curl http://localhost:8000/admin/question-bank/stats

# Generate questions first
python backend/scripts/generate_and_export_questions.py --skills SQL --count 10
```

### File already exists error

**Problem**: `Error: Output file already exists`

**Solution**: Use `--force` flag
```bash
python backend/scripts/export_question_bank_json.py --out quiz.json --force
```

### Options not parsing correctly

**Problem**: Options appear as JSON string instead of array

**Cause**: Old database records before migration

**Solution**: Regenerate questions or fix manually:
```python
# Fix script (run once)
from app.db import SessionLocal
from app.models.question_bank import QuestionBank
import json

db = SessionLocal()
questions = db.query(QuestionBank).all()

for q in questions:
    try:
        # Test if options_json is valid
        options = json.loads(q.options_json)
        if isinstance(options, dict):
            # Already correct format
            continue
    except:
        # Fix invalid JSON
        print(f"Fixing question ID {q.id}")
        
db.close()
```

---

## Integration Examples

### Frontend React Component

```jsx
import { useState, useEffect } from 'react';

function QuizPage({ skillName }) {
  const [quiz, setQuiz] = useState(null);
  
  useEffect(() => {
    fetch(`/admin/question-bank/export?skills=${skillName}&format=grouped&include_answers=false`)
      .then(res => res.json())
      .then(data => {
        if (data.skills && data.skills[0]) {
          setQuiz(data.skills[0].quizzes);
        }
      });
  }, [skillName]);
  
  return (
    <div>
      {quiz && quiz.map((difficulty, idx) => (
        <QuizSection 
          key={idx} 
          difficulty={difficulty.difficulty}
          questions={difficulty.questions}
        />
      ))}
    </div>
  );
}
```

### Python Data Analysis

```python
import json
import pandas as pd

# Load flat format
with open('exports/questions_flat.json') as f:
    questions = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(questions)

# Analyze
print(df['difficulty'].value_counts())
print(df.groupby(['skill_name', 'difficulty']).size())

# Export specific difficulty
easy_questions = df[df['difficulty'] == 'easy']
easy_questions.to_json('easy_only.json', orient='records', indent=2)
```

---

## Next Steps

1. **Generate questions**: See [ENDPOINT_MAPPING_GUIDE.md](backend/ENDPOINT_MAPPING_GUIDE.md)
2. **Quiz API**: See [QUIZ_API_GUIDE.md](backend/QUIZ_API_GUIDE.md) (if exists)
3. **Frontend integration**: Use exported JSON in quiz components

---

## File Locations

- **CLI Scripts**:
  - `backend/scripts/export_question_bank_json.py`
  - `backend/scripts/generate_and_export_questions.py`

- **API Route**:
  - `backend/src/app/routes/admin_question_bank.py` (GET `/admin/question-bank/export`)

- **Models**:
  - `backend/src/app/models/question_bank.py`

- **Services**:
  - `backend/src/app/services/question_bank_service.py`
  - `backend/src/app/services/question_persistence.py`
