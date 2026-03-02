# Generate and Export Questions - API Documentation

## Endpoint

```
POST /admin/question-bank/generate-and-export
```

Generate quiz questions using Ollama and export them to a JSON file in one operation.

---

## Request

### Request Body

```json
{
  "skill_names": ["SQL", "Python Programming"],
  "questions_per_difficulty": 10,
  "model_name": "llama3.1:8b"
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_names` | array[string] | ✓ | List of parent skill names to generate questions for |
| `questions_per_difficulty` | integer | ✓ | Number of questions per difficulty level (1-50) |
| `model_name` | string | ✓ | Ollama model to use (e.g., "llama3.1:8b") |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | string | `grouped` | Export format: `grouped` or `flat` |
| `include_answers` | boolean | `true` | Include correct answers in export |
| `include_explanations` | boolean | `true` | Include explanations in export |
| `force` | boolean | `false` | Overwrite export file if exists |

---

## Response

### Success Response (200 OK)

```json
{
  "status": "completed",
  "generation_stats": {
    "total_requested": 60,
    "total_generated": 58,
    "duplicates_skipped": 2,
    "errors": 0,
    "per_skill": {
      "SQL": {
        "requested": 30,
        "generated": 28,
        "duplicates": 2,
        "errors": 0
      },
      "Python Programming": {
        "requested": 30,
        "generated": 30,
        "duplicates": 0,
        "errors": 0
      }
    }
  },
  "export_file_path": "exports/question_bank_20240206_143022.json",
  "total_questions": 58,
  "skills": ["SQL", "Python Programming"],
  "format": "grouped",
  "message": "Generated and exported 58/60 questions (96.7% success). Exported to question_bank_20240206_143022.json."
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Operation status ("completed") |
| `generation_stats` | object | Detailed generation statistics |
| `export_file_path` | string | Relative path to exported JSON file |
| `total_questions` | integer | Total questions exported |
| `skills` | array[string] | Skills that were processed |
| `format` | string | Export format used |
| `message` | string | Human-readable summary |

### Error Responses

**400 Bad Request** - Invalid request parameters
```json
{
  "detail": "skill_names cannot be empty"
}
```

**409 Conflict** - Export file already exists
```json
{
  "detail": "Export file question_bank_20240206_143022.json already exists. Use force=true to overwrite."
}
```

**500 Internal Server Error** - Generation succeeded but export failed
```json
{
  "detail": "Questions were generated but could not be retrieved for export"
}
```

---

## Exported JSON Format

### Grouped Format (Default)

Questions organized by skill → difficulty → questions array.

```json
{
  "generated_at": "2024-02-06T14:30:22Z",
  "model_name": "llama3.1:8b",
  "questions_per_difficulty": 10,
  "skills": [
    {
      "skill_name": "SQL",
      "quizzes": [
        {
          "difficulty": "easy",
          "questions": [
            {
              "question": "What does SQL stand for?",
              "options": [
                "Structured Query Language",
                "Simple Question Language",
                "System Query Logic",
                "Standard Queue List"
              ],
              "answer": "A",
              "explanation": "SQL stands for Structured Query Language, used for managing relational databases."
            },
            {
              "question": "Which SQL command retrieves data?",
              "options": ["SELECT", "GET", "FETCH", "RETRIEVE"],
              "answer": "A",
              "explanation": "SELECT is the SQL command used to retrieve data from database tables."
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
      "skill_name": "Python Programming",
      "quizzes": [ /* ... */ ]
    }
  ]
}
```

**Use Case:** Quiz applications that group questions by difficulty level.

### Flat Format

Simple list of questions without nesting.

```json
{
  "generated_at": "2024-02-06T14:30:22Z",
  "model_name": "llama3.1:8b",
  "questions_per_difficulty": 10,
  "questions": [
    {
      "skill_name": "SQL",
      "difficulty": "easy",
      "question": "What does SQL stand for?",
      "options": [
        "Structured Query Language",
        "Simple Question Language",
        "System Query Logic",
        "Standard Queue List"
      ],
      "answer": "A",
      "explanation": "SQL stands for Structured Query Language..."
    },
    {
      "skill_name": "SQL",
      "difficulty": "easy",
      "question": "Which SQL command retrieves data?",
      "options": ["SELECT", "GET", "FETCH", "RETRIEVE"],
      "answer": "A",
      "explanation": "SELECT is the SQL command used to retrieve data..."
    }
  ]
}
```

**Use Case:** Data processing, analysis, or simple iteration.

### Without Answers (Student Version)

Set `include_answers=false` to create student quiz files:

```json
{
  "generated_at": "2024-02-06T14:30:22Z",
  "model_name": "llama3.1:8b",
  "questions_per_difficulty": 10,
  "skills": [
    {
      "skill_name": "SQL",
      "quizzes": [
        {
          "difficulty": "easy",
          "questions": [
            {
              "question": "What does SQL stand for?",
              "options": [
                "Structured Query Language",
                "Simple Question Language",
                "System Query Logic",
                "Standard Queue List"
              ]
              // No "answer" or "explanation" fields
            }
          ]
        }
      ]
    }
  ]
}
```

---

## cURL Examples

### Basic Usage

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL", "Python Programming"],
    "questions_per_difficulty": 10,
    "model_name": "llama3.1:8b"
  }'
```

### Flat Format

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?format=flat" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL"],
    "questions_per_difficulty": 15,
    "model_name": "llama3.1:8b"
  }'
```

### Student Quiz (No Answers)

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?include_answers=false" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["Data Structures", "Algorithms"],
    "questions_per_difficulty": 20,
    "model_name": "llama3.1:8b"
  }'
```

### Force Overwrite

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?force=true" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["Machine Learning"],
    "questions_per_difficulty": 10,
    "model_name": "llama3.1:8b"
  }'
```

### No Explanations

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?include_explanations=false" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL"],
    "questions_per_difficulty": 10,
    "model_name": "llama3.1:8b"
  }'
```

---

## Python Client Example

```python
import requests

url = "http://localhost:8000/admin/question-bank/generate-and-export"

# Request payload
payload = {
    "skill_names": ["SQL", "Python Programming"],
    "questions_per_difficulty": 10,
    "model_name": "llama3.1:8b"
}

# Query parameters
params = {
    "format": "grouped",
    "include_answers": True,
    "include_explanations": True,
    "force": False
}

# Make request
response = requests.post(url, json=payload, params=params)

if response.status_code == 200:
    result = response.json()
    print(f"✓ Export successful!")
    print(f"  File: {result['export_file_path']}")
    print(f"  Questions: {result['total_questions']}")
    print(f"  Message: {result['message']}")
else:
    print(f"✗ Error: {response.status_code}")
    print(response.json())
```

---

## JavaScript/Fetch Example

```javascript
const url = "http://localhost:8000/admin/question-bank/generate-and-export";

const payload = {
  skill_names: ["SQL", "Python Programming"],
  questions_per_difficulty: 10,
  model_name: "llama3.1:8b"
};

const params = new URLSearchParams({
  format: "grouped",
  include_answers: "true",
  include_explanations: "true"
});

fetch(`${url}?${params}`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
})
  .then(res => res.json())
  .then(data => {
    console.log("✓ Export successful!");
    console.log("File:", data.export_file_path);
    console.log("Questions:", data.total_questions);
    console.log("Message:", data.message);
  })
  .catch(err => console.error("Error:", err));
```

---

## File Management

### Export Directory

All files are saved to: `backend/exports/`

The directory is created automatically if it doesn't exist.

### Filename Convention

```
question_bank_YYYYMMDD_HHMMSS.json
```

Example: `question_bank_20240206_143022.json`

### Avoiding Overwrites

By default, the endpoint returns a 409 error if the file exists. Use `force=true` to overwrite:

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?force=true" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

---

## Workflow Examples

### Workflow 1: Generate Quiz Bank for Course

```bash
# Generate comprehensive question bank
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": [
      "Python Programming",
      "Data Structures",
      "Algorithms",
      "SQL",
      "Machine Learning"
    ],
    "questions_per_difficulty": 20,
    "model_name": "llama3.1:8b"
  }'

# Response includes: exports/question_bank_20240206_143022.json
# Contains: 5 skills × 20 questions × 3 difficulties = 300 questions
```

### Workflow 2: Create Student Practice Quiz

```bash
# Generate quiz without answers/explanations
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?include_answers=false&include_explanations=false" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["Python Programming"],
    "questions_per_difficulty": 15,
    "model_name": "llama3.1:8b"
  }'
```

### Workflow 3: Separate Answer Key

```bash
# Step 1: Generate questions (store in DB)
curl -X POST "http://localhost:8000/admin/question-bank/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL"],
    "questions_per_difficulty": 10,
    "model_name": "llama3.1:8b"
  }'

# Step 2: Export student version (no answers)
curl "http://localhost:8000/admin/question-bank/export?skills=SQL&include_answers=false" \
  > student_quiz.json

# Step 3: Export answer key (flat format)
curl "http://localhost:8000/admin/question-bank/export?skills=SQL&format=flat" \
  > answer_key.json
```

---

## Testing

### Quick Test

```bash
# Test with small batch
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL"],
    "questions_per_difficulty": 3,
    "model_name": "llama3.1:8b"
  }'
```

Expected: Generates 9 questions (3 easy + 3 medium + 3 hard) and exports to JSON.

### Validate JSON

```bash
# Check JSON validity
python -m json.tool exports/question_bank_*.json

# Count questions (grouped format)
cat exports/question_bank_*.json | \
  jq '[.skills[].quizzes[].questions[]] | length'

# Count questions (flat format)
cat exports/question_bank_*.json | \
  jq '.questions | length'
```

---

## Related Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/question-bank/generate` | POST | Generate questions only (no export) |
| `/admin/question-bank/export` | GET | Export existing questions from DB |
| `/admin/question-bank/stats` | GET | Get question bank statistics |
| `/admin/question-bank/clear` | DELETE | Clear questions from database |

---

## Notes

1. **Performance**: Generation is slow (uses Ollama). Expect 2-5 seconds per question.
   - 10 questions/difficulty × 3 difficulties = 30 questions ≈ 60-150 seconds
   - 20 questions/difficulty × 3 difficulties = 60 questions ≈ 120-300 seconds

2. **Duplicates**: The system prevents duplicate questions (same skill + difficulty + question text).
   - Duplicates are counted in `duplicates_skipped`
   - The export includes only successfully generated unique questions

3. **Database Storage**: All generated questions are stored in QuestionBank table.
   - Export retrieves questions created in the last 5 minutes matching the request
   - Questions remain in DB for future use/export

4. **File Naming**: Timestamp ensures unique filenames.
   - Format: `question_bank_YYYYMMDD_HHMMSS.json`
   - Multiple calls in the same second may conflict (use `force=true`)

5. **Options Format**: Options are always exported as array of 4 strings.
   - Database stores as JSON string: `{"A": "...", "B": "...", "C": "...", "D": "..."}`
   - Export converts to array: `["...", "...", "...", "..."]`

6. **Answer Field**: Correct answer is a single letter (A, B, C, or D).
   - Corresponds to index in options array (A=0, B=1, C=2, D=3)

---

## Troubleshooting

### Issue: 409 Conflict - File exists

**Solution**: Use `force=true` or wait 1 second and retry

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?force=true" ...
```

### Issue: 500 Error - Cannot retrieve questions

**Cause**: Database query failed or no questions generated

**Solution**: Check generation_stats in response, retry with different skills

### Issue: Empty export file

**Cause**: All questions were duplicates

**Solution**: Clear existing questions or use different skills:

```bash
# Clear existing questions for skill
curl -X DELETE "http://localhost:8000/admin/question-bank/clear?skill_name=SQL"

# Then regenerate
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export" ...
```

### Issue: Ollama connection error

**Cause**: Ollama service not running

**Solution**: Start Ollama service:

```bash
ollama serve
```

---

## File Locations

- **Endpoint**: `backend/src/app/routes/admin_question_bank.py`
- **Service**: `backend/src/app/services/question_bank_service.py`
- **Model**: `backend/src/app/models/question_bank.py`
- **Exports**: `backend/exports/`
