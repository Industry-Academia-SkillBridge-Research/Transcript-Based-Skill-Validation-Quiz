# Implementation Summary: Generate and Export Questions

## Overview

Added a new FastAPI endpoint that combines question generation and JSON export in a single operation.

---

## New Endpoint

### POST /admin/question-bank/generate-and-export

**Purpose**: Generate quiz questions using Ollama and export them to a JSON file in one API call.

**Location**: `backend/src/app/routes/admin_question_bank.py`

**Request**:
```json
{
  "skill_names": ["SQL", "Python"],
  "questions_per_difficulty": 10,
  "model_name": "llama3.1:8b"
}
```

**Query Parameters**:
- `format=grouped|flat` (default: grouped)
- `include_answers=true|false` (default: true)
- `include_explanations=true|false` (default: true)
- `force=true|false` (default: false)

**Response**:
```json
{
  "status": "completed",
  "generation_stats": { ... },
  "export_file_path": "exports/question_bank_20240206_143022.json",
  "total_questions": 58,
  "skills": ["SQL", "Python"],
  "format": "grouped",
  "message": "Generated and exported 58 questions"
}
```

---

## Implementation Details

### 1. Endpoint Logic

The endpoint follows this workflow:

1. **Validate** request parameters (skill_names, questions_per_difficulty)
2. **Generate** questions using existing `question_bank_service.generate_bank_for_skills()`
3. **Query** database for recently created questions (last 5 minutes, matching skills and model)
4. **Build** export data in requested format (grouped or flat)
5. **Write** JSON file to `exports/` directory with timestamp
6. **Return** response with file path and statistics

### 2. Data Flow

```
Request → Generate (Ollama) → Store (SQLite) → Query (Filter) → Export (JSON) → Response
```

**Key Design Decisions**:
- Reuses existing generation service (no duplication)
- Queries database for export (ensures consistency)
- Filters by creation time to export only current batch
- Supports multiple export formats and options

### 3. Helper Functions

Added two helper functions for building export data:

- `_export_grouped_with_metadata()`: Builds grouped format with metadata header
- `_export_flat_with_metadata()`: Builds flat format with metadata wrapper

Both functions:
- Parse `options_json` from database (stored as JSON string)
- Convert to array format `["A option", "B option", "C option", "D option"]`
- Include/exclude answers and explanations based on flags
- Add metadata (generated_at, model_name, questions_per_difficulty)

---

## Export Formats

### Grouped Format (Default)

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
              "question": "What is SQL?",
              "options": ["A..", "B..", "C..", "D.."],
              "answer": "A",
              "explanation": "..."
            }
          ]
        }
      ]
    }
  ]
}
```

**Use Case**: Quiz UI that organizes questions by difficulty level

### Flat Format

```json
{
  "generated_at": "2024-02-06T14:30:22Z",
  "model_name": "llama3.1:8b",
  "questions_per_difficulty": 10,
  "questions": [
    {
      "skill_name": "SQL",
      "difficulty": "easy",
      "question": "What is SQL?",
      "options": ["A..", "B..", "C..", "D.."],
      "answer": "A",
      "explanation": "..."
    }
  ]
}
```

**Use Case**: Data processing or simple iteration

---

## File Management

### Directory Structure

```
backend/
  exports/                          # Auto-created if missing
    question_bank_20240206_143022.json
    question_bank_20240206_150045.json
```

### Filename Convention

```
question_bank_YYYYMMDD_HHMMSS.json
```

- Timestamp ensures unique filenames
- Multiple calls in same second may conflict (use `force=true`)

### Overwrite Protection

- Default: Returns 409 error if file exists
- With `force=true`: Overwrites existing file

---

## Modified Files

### 1. backend/src/app/routes/admin_question_bank.py

**Changes**:
- Added imports: `datetime, timedelta, Path`
- Added response model: `GenerateAndExportResponse`
- Added endpoint: `POST /generate-and-export`
- Added helper functions: `_export_grouped_with_metadata()`, `_export_flat_with_metadata()`

**Lines Added**: ~200 lines

### 2. backend/GENERATE_AND_EXPORT_API.md (NEW)

**Purpose**: Complete API documentation with examples

**Sections**:
- Request/response schemas
- cURL examples
- Python/JavaScript client examples
- Workflow examples
- Troubleshooting guide

---

## Testing

### Quick Test

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL"],
    "questions_per_difficulty": 3,
    "model_name": "llama3.1:8b"
  }'
```

Expected: Generates 9 questions and exports to `exports/question_bank_*.json`

### Validate Export

```bash
# Check JSON validity
python -m json.tool exports/question_bank_*.json

# Count questions
cat exports/question_bank_*.json | jq '[.skills[].quizzes[].questions[]] | length'
```

---

## Related Existing Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/admin/question-bank/generate` | POST | Generate only (no export) |
| `/admin/question-bank/export` | GET | Export existing questions |
| `/admin/question-bank/stats` | GET | Get statistics |
| `/admin/question-bank/clear` | DELETE | Clear questions |

**Difference**: The new endpoint combines generation + export in one operation, while existing endpoints handle them separately.

---

## Usage Examples

### Example 1: Generate Course Quiz Bank

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["Python", "SQL", "Data Structures"],
    "questions_per_difficulty": 15,
    "model_name": "llama3.1:8b"
  }'
```

Result: 135 questions (3 skills × 15 questions × 3 difficulties) exported to JSON

### Example 2: Student Practice Quiz (No Answers)

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?include_answers=false" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["Python"],
    "questions_per_difficulty": 10,
    "model_name": "llama3.1:8b"
  }'
```

Result: 30 questions without answers or explanations (suitable for students)

### Example 3: Flat Format for Analysis

```bash
curl -X POST "http://localhost:8000/admin/question-bank/generate-and-export?format=flat" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_names": ["SQL"],
    "questions_per_difficulty": 20,
    "model_name": "llama3.1:8b"
  }'
```

Result: 60 questions in flat list format (easy to process with pandas/analysis tools)

---

## Error Handling

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Empty skill_names | `{"detail": "skill_names cannot be empty"}` |
| 400 | Invalid questions_per_difficulty | `{"detail": "questions_per_difficulty must be between 1 and 50"}` |
| 409 | File exists | `{"detail": "Export file ... already exists. Use force=true"}` |
| 500 | Export failed | `{"detail": "Questions were generated but could not be retrieved"}` |

---

## Performance Considerations

### Generation Time

- **Ollama LLM**: 2-5 seconds per question
- **10 questions/difficulty**: ~60-150 seconds total
- **20 questions/difficulty**: ~120-300 seconds total

### Optimization

The endpoint:
- Generates in parallel where possible (handled by question_bank_service)
- Uses database transactions efficiently
- Queries only recent questions (last 5 minutes filter)
- Writes JSON in single operation

---

## Database Schema

Questions are stored in `QuestionBank` table:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| skill_name | TEXT | Parent skill name |
| difficulty | TEXT | easy/medium/hard |
| question_text | TEXT | Question content |
| options_json | TEXT | JSON string: `{"A":"..","B":"..","C":"..","D":".."}` |
| correct_option | TEXT | A/B/C/D |
| explanation | TEXT | Answer explanation |
| model_name | TEXT | Ollama model used |
| created_at | TIMESTAMP | Generation timestamp |

**Unique Constraint**: (skill_name, difficulty, question_text)

---

## Integration Examples

### Python Client

```python
import requests

response = requests.post(
    "http://localhost:8000/admin/question-bank/generate-and-export",
    json={
        "skill_names": ["SQL"],
        "questions_per_difficulty": 10,
        "model_name": "llama3.1:8b"
    },
    params={"format": "grouped"}
)

result = response.json()
print(f"Exported to: {result['export_file_path']}")
```

### Frontend JavaScript

```javascript
const response = await fetch(
  "/admin/question-bank/generate-and-export",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      skill_names: ["Python"],
      questions_per_difficulty: 10,
      model_name: "llama3.1:8b"
    })
  }
);

const data = await response.json();
console.log(`Exported ${data.total_questions} questions`);
```

---

## Documentation Files

### 1. GENERATE_AND_EXPORT_API.md

**Location**: `backend/GENERATE_AND_EXPORT_API.md`

**Content**:
- Complete API reference
- Request/response schemas
- cURL examples
- Client code examples (Python, JavaScript)
- Workflow examples
- Troubleshooting guide

### 2. EXPORT_QUESTION_BANK_GUIDE.md (Previously Created)

**Location**: `backend/EXPORT_QUESTION_BANK_GUIDE.md`

**Content**:
- CLI script documentation
- GET /export endpoint documentation
- Combined generate+export script docs
- JSON format schemas
- Integration examples

---

## Backward Compatibility

✅ **No Breaking Changes**

- Existing endpoints remain unchanged
- Existing generation logic reused (not modified)
- New endpoint is additive only
- Database schema unchanged

---

## Next Steps

### Recommended Testing

1. **Unit Tests**: Test helper functions for export formatting
2. **Integration Tests**: Test full endpoint with real Ollama
3. **Load Tests**: Test with large question batches (50 questions × 3 difficulties)

### Potential Enhancements

1. **Batch Export**: Export multiple skills to separate files
2. **Custom Formats**: Support additional export formats (CSV, XML)
3. **Compression**: Add option to gzip large exports
4. **Versioning**: Add version field to track export schema changes

---

## Summary

✅ Implemented `POST /admin/question-bank/generate-and-export`
✅ Supports grouped and flat export formats
✅ Includes optional answer/explanation filtering
✅ Auto-creates exports directory
✅ Timestamp-based unique filenames
✅ Comprehensive API documentation
✅ Zero breaking changes to existing code

**Files Modified**:
- `backend/src/app/routes/admin_question_bank.py` (endpoint + helpers)

**Files Created**:
- `backend/GENERATE_AND_EXPORT_API.md` (API documentation)
- `backend/EXPORT_QUESTION_BANK_GUIDE.md` (previous - CLI/export guide)
- `backend/scripts/export_question_bank_json.py` (previous - CLI script)
- `backend/scripts/generate_and_export_questions.py` (previous - combined CLI)
- `backend/scripts/test_export.py` (previous - validation tests)
