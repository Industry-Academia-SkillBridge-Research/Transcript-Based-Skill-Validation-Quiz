# 🎓 Skill Scoring Algorithm - VIVA Explanation

## 📊 Overview

The system computes skill scores from academic transcripts using a **weighted evidence-based approach** that considers:
1. **Academic Performance** (grades)
2. **Course Relevance** (mapping weights)
3. **Course Credits** (importance)
4. **Temporal Decay** (recency of learning)

---

## 🧮 Mathematical Formula

### Core Formula

```
Skill Score = (Σ Contributions / Σ Evidence Weights) × 100

Where:
  Contribution = grade_norm × evidence_weight
  Evidence Weight = map_weight × credits × recency
```

### Component Formulas

```
1. Grade Normalization:
   grade_norm = GPA / 4.0
   
2. Recency Factor:
   recency = e^(-λ × years_since)
   where λ = 0.4 (decay rate)
   
3. Confidence Score:
   confidence = 1 - e^(-α × total_evidence_weight)
   where α = 0.25 (confidence factor)
```

---

## 📐 Step-by-Step Calculation

### Step 1: Extract Course Data from Transcript

**Input:** PDF transcript → **Output:** Course records

| Course Code | Grade | Credits | Year |
|-------------|-------|---------|------|
| IT1010      | A     | 3.0     | 1    |
| IT1090      | B+    | 3.0     | 1    |
| IT2040      | A-    | 3.0     | 2    |

### Step 2: Map Courses to Skills

Using `course_skill_map.csv`:

| Course Code | Skill Name    | Map Weight |
|-------------|---------------|------------|
| IT1010      | C Programming | 0.5        |
| IT1010      | Linux         | 0.2        |
| IT1090      | SQL           | 0.35       |
| IT2040      | SQL           | 0.35       |

### Step 3: Calculate Components for Each Course-Skill Pair

**Example: IT1010 → C Programming**

```python
# Constants
GRADE_MAPPING = {"A": 4.0, "B+": 3.3, "A-": 3.7}
RECENCY_DECAY = 0.4
current_academic_year = 4

# Course: IT1010
grade = "A"
credits = 3.0
academic_year = 1
map_weight = 0.5

# Calculate components
grade_points = GRADE_MAPPING["A"]              # = 4.0
grade_norm = grade_points / 4.0                # = 4.0/4.0 = 1.0

years_since = current_academic_year - academic_year  # = 4-1 = 3
recency = e^(-0.4 × 3)                         # = e^(-1.2) ≈ 0.301

evidence_weight = map_weight × credits × recency
                = 0.5 × 3.0 × 0.301
                = 0.4515

contribution = grade_norm × evidence_weight
             = 1.0 × 0.4515
             = 0.4515
```

### Step 4: Aggregate by Skill

**Example: SQL Skill**

SQL appears in two courses:
1. IT1090 (Grade B+, Year 1, weight 0.35)
2. IT2040 (Grade A-, Year 2, weight 0.35)

**Course 1: IT1090 → SQL**
```python
grade_norm = 3.3 / 4.0 = 0.825
recency = e^(-0.4 × 3) = 0.301
evidence_weight = 0.35 × 3.0 × 0.301 = 0.316
contribution = 0.825 × 0.316 = 0.261
```

**Course 2: IT2040 → SQL**
```python
grade_norm = 3.7 / 4.0 = 0.925
recency = e^(-0.4 × 2) = 0.449
evidence_weight = 0.35 × 3.0 × 0.449 = 0.471
contribution = 0.925 × 0.471 = 0.436
```

**Aggregation:**
```python
total_contribution = 0.261 + 0.436 = 0.697
total_evidence_weight = 0.316 + 0.471 = 0.787
```

### Step 5: Compute Final Score

```python
skill_score = (total_contribution / total_evidence_weight) × 100
            = (0.697 / 0.787) × 100
            = 88.6
```

### Step 6: Calculate Confidence

```python
confidence = 1 - e^(-0.25 × total_evidence_weight)
           = 1 - e^(-0.25 × 0.787)
           = 1 - e^(-0.197)
           = 1 - 0.821
           = 0.179 (17.9%)
```

### Step 7: Determine Skill Level

```python
if score >= 75:
    level = "Advanced"
elif score >= 50:
    level = "Intermediate"
else:
    level = "Beginner"

# SQL score = 88.6 → "Advanced"
```

---

## 🎯 Real Example: Complete Calculation

### Given: Student IT21013928's Transcript

| Course   | Grade | Credits | Year | Skill         | Weight |
|----------|-------|---------|------|---------------|--------|
| IT1010   | A     | 3.0     | 1    | C Programming | 0.5    |
| IT1010   | A     | 3.0     | 1    | Linux         | 0.2    |
| IT1090   | B+    | 3.0     | 1    | SQL           | 0.35   |
| IT2040   | A-    | 3.0     | 2    | SQL           | 0.35   |
| IT2030   | A     | 3.0     | 2    | Java          | 0.5    |

### Calculation: Python Skill

**Courses contributing to Python:**
- IT1010: Grade A, Year 1, Weight 0.15 (assumed)
- IT1030: Grade A, Year 1, Weight 0.15 (assumed)

**Course 1:**
```
grade_norm = 4.0/4.0 = 1.0
recency = e^(-0.4×3) = 0.301
evidence_weight = 0.15 × 3.0 × 0.301 = 0.135
contribution = 1.0 × 0.135 = 0.135
```

**Course 2:**
```
grade_norm = 4.0/4.0 = 1.0
recency = e^(-0.4×3) = 0.301
evidence_weight = 0.15 × 3.0 × 0.301 = 0.135
contribution = 1.0 × 0.135 = 0.135
```

**Final Python Score:**
```
total_contribution = 0.135 + 0.135 = 0.270
total_evidence_weight = 0.135 + 0.135 = 0.270
score = (0.270 / 0.270) × 100 = 100.0 ✅
confidence = 1 - e^(-0.25×0.270) = 0.065 (6.5%)
level = "Advanced"
```

---

## 🔍 Component Explanations

### 1. Grade Normalization (grade_norm)

**Purpose:** Convert letter grades to numerical scale (0-1)

**Mapping:**
```python
A+, A  → 4.0 → 1.00 (Perfect performance)
A-     → 3.7 → 0.93 (Excellent)
B+     → 3.3 → 0.83 (Very good)
B      → 3.0 → 0.75 (Good)
C      → 2.0 → 0.50 (Satisfactory)
D      → 1.0 → 0.25 (Pass)
F      → 0.0 → 0.00 (Fail)
```

**Why:** Higher grades contribute more to skill scores, reflecting better understanding.

### 2. Map Weight (map_weight)

**Purpose:** Indicates how relevant a course is to a specific skill

**Examples:**
- IT1010 → C Programming: **0.5** (50% of course is about C)
- IT1010 → Linux: **0.2** (20% of course is about Linux)
- IT1010 → Git: **0.1** (10% of course is about Git)

**Total:** 0.5 + 0.2 + 0.15 + 0.1 + 0.05 = 1.0 (100% of course)

**Why:** Reflects curriculum emphasis on each skill within the course.

### 3. Credits

**Purpose:** Course importance/workload (usually 3.0 or 4.0 credits)

**Why:** Higher-credit courses carry more weight in skill assessment.

### 4. Recency Factor (recency)

**Formula:** `recency = e^(-λ × years_since)` where λ = 0.4

**Decay Over Time:**
| Years Since | Recency Factor | Retention |
|-------------|----------------|-----------|
| 0 (current) | 1.000          | 100%      |
| 1           | 0.670          | 67%       |
| 2           | 0.449          | 45%       |
| 3           | 0.301          | 30%       |
| 4           | 0.202          | 20%       |

**Why:** Skills learned recently are fresher than those learned years ago (temporal decay).

**Rationale:** 
- Memory retention decreases exponentially over time (Ebbinghaus forgetting curve)
- Recent coursework reflects current capability better
- λ = 0.4 chosen to balance retention (not too harsh)

### 5. Evidence Weight

**Formula:** `evidence_weight = map_weight × credits × recency`

**Purpose:** Combined measure of evidence strength

**Interpretation:**
- High evidence weight: Strong, relevant, recent evidence
- Low evidence weight: Weak, tangential, or old evidence

**Example:**
```
Strong Evidence:
  map_weight=0.5, credits=3.0, recency=0.67
  → evidence_weight = 1.005

Weak Evidence:
  map_weight=0.1, credits=3.0, recency=0.30
  → evidence_weight = 0.090
```

### 6. Contribution

**Formula:** `contribution = grade_norm × evidence_weight`

**Purpose:** How much quality evidence a course provides for a skill

**Example:**
```
Excellent Performance + Strong Evidence:
  grade_norm=1.0, evidence_weight=1.0
  → contribution = 1.0

Poor Performance + Strong Evidence:
  grade_norm=0.5, evidence_weight=1.0
  → contribution = 0.5

Excellent Performance + Weak Evidence:
  grade_norm=1.0, evidence_weight=0.1
  → contribution = 0.1
```

### 7. Claimed Score

**Formula:** `claimed_score = (Σ contributions / Σ evidence_weights) × 100`

**Purpose:** Overall skill proficiency (0-100 scale)

**Interpretation:**
- **90-100**: Mastery level (consistent A grades)
- **75-89**: Advanced (mostly A/A- grades)
- **50-74**: Intermediate (B/C grades)
- **0-49**: Beginner (D/F grades or weak evidence)

**Why weighted average?**
- Not all courses contribute equally
- Accounts for relevance, performance, and recency
- More robust than simple averaging

### 8. Confidence Score

**Formula:** `confidence = 1 - e^(-α × total_evidence_weight)` where α = 0.25

**Purpose:** How reliable is the skill score estimate?

**Confidence by Evidence Weight:**
| Total Evidence | Confidence | Interpretation        |
|----------------|------------|-----------------------|
| 1.0            | 22%        | Low (1 course)        |
| 3.0            | 53%        | Medium (2-3 courses)  |
| 6.0            | 78%        | High (4-5 courses)    |
| 10.0           | 92%        | Very High (6+ courses)|

**Why:** 
- More evidence = higher confidence
- Single course is unreliable
- Multiple courses provide validation

**Mathematical Basis:**
- Asymptotic function approaching 1.0
- Never reaches 100% (epistemic humility)
- α = 0.25 calibrated for typical transcript (3-6 courses per skill)

---

## 🎯 Design Rationale

### Why This Algorithm?

**1. Evidence-Based**
- Uses actual academic performance
- Multiple data points per skill
- Transparent calculation

**2. Weighted Appropriately**
- Grades matter (performance indicator)
- Relevance matters (map_weight)
- Time matters (recency decay)
- Course depth matters (credits)

**3. Handles Real-World Scenarios**
- Multiple courses teach same skill → aggregation
- Skills decay over time → recency factor
- Varying course difficulty → credits weighting
- Incomplete evidence → confidence score

**4. Psychologically Sound**
- Exponential decay models memory retention
- Weighted averaging prevents outlier bias
- Confidence reflects epistemic uncertainty

### Advantages Over Simple Averaging

**Simple Average Problems:**
```python
# Simple: Average of grades for SQL courses
(B+ + A-) / 2 = (3.3 + 3.7) / 2 = 3.5 / 4.0 = 87.5%

Problems:
❌ Ignores relevance (all courses equal weight)
❌ Ignores timing (old = new)
❌ Ignores course depth (1 credit = 4 credits)
❌ No confidence measure
```

**Our Algorithm:**
```python
Weighted by:
✅ Course relevance to skill (map_weight)
✅ Course importance (credits)
✅ Learning recency (exponential decay)
✅ Confidence from evidence amount
```

---

## 📈 Use Cases Handled

### Case 1: Single Course for Skill
```
Python: Only IT1010
→ Score based on single course
→ Low confidence (1 course)
```

### Case 2: Multiple Courses, Different Grades
```
SQL: IT1090 (B+) + IT2040 (A-) + IT3031 (A)
→ Weighted average favoring recent, better performance
→ High confidence (3 courses)
```

### Case 3: Old vs Recent Learning
```
Java: IT1050 (A, Year 1) + IT2030 (A, Year 2)
→ IT2030 contributes more (recency = 0.67 vs 0.45)
→ Recent learning weighted higher
```

### Case 4: High Weight vs Low Weight
```
IT1100: HTML (0.25) + JavaScript (0.25) + CSS (0.2)
→ HTML contributes most
→ Reflects curriculum emphasis
```

---

## 🎤 VIVA Questions & Answers

### Q1: Why exponential decay for recency?

**A:** "Exponential decay models human memory retention according to the Ebbinghaus forgetting curve. Skills learned 3 years ago have diminished compared to recent learning. We use λ=0.4, which means Year 1 courses retain 30% weight compared to current courses. This is neither too harsh (skills aren't completely forgotten) nor too lenient (old knowledge shouldn't dominate)."

### Q2: Why not just use GPA?

**A:** "GPA is a single aggregated number that:
1. Doesn't distinguish between skills (Python vs SQL)
2. Treats all courses equally (ignoring relevance)
3. Doesn't account for temporal factors
Our skill-specific scoring provides granular, temporal, and evidence-based assessment."

### Q3: How is confidence calculated and why?

**A:** "Confidence = 1 - e^(-0.25 × total_evidence_weight). It increases asymptotically with more evidence. One course gives ~20% confidence, three courses ~50%, six courses ~78%. This reflects epistemic uncertainty - we're never 100% confident, but more evidence increases reliability. This helps identify skills that need more validation via quizzes."

### Q4: What if a student got a poor grade in one course but excellent in another for the same skill?

**A:** "The weighted average accounts for this. If a student got C in IT1090 (SQL, Year 1) but A in IT2040 (SQL, Year 2), the recent A with higher recency factor will pull the average up, while the old C has diminished weight. This reflects learning improvement over time."

### Q5: Can you walk through a complete example?

**A:** "Sure! Let's calculate Python skill:
- IT1010: Grade A (1.0), Weight 0.15, Year 1, Recency 0.301
  → contribution = 1.0 × 0.15 × 3.0 × 0.301 = 0.135
  
- IT1030: Grade A (1.0), Weight 0.15, Year 1, Recency 0.301
  → contribution = 0.135
  
Total contribution = 0.270, Total evidence = 0.270
Score = (0.270/0.270) × 100 = 100%
Confidence = 1 - e^(-0.25×0.270) = 6.5%
Level: Advanced, but low confidence (only 2 courses)"

---

## 📊 Algorithm Summary Diagram

```
INPUT: Student Transcript (PDF)
  ↓
STEP 1: Extract Courses
  → course_code, grade, credits, year
  ↓
STEP 2: Map to Skills (course_skill_map.csv)
  → Join courses with skills via mapping weights
  ↓
STEP 3: Calculate Components
  → grade_norm = GPA / 4.0
  → recency = e^(-0.4 × years_since)
  → evidence_weight = map_weight × credits × recency
  → contribution = grade_norm × evidence_weight
  ↓
STEP 4: Aggregate by Skill
  → total_contribution = Σ contributions
  → total_evidence_weight = Σ evidence_weights
  ↓
STEP 5: Compute Scores
  → claimed_score = (total_contribution / total_evidence_weight) × 100
  → confidence = 1 - e^(-0.25 × total_evidence_weight)
  → level = if score >= 75: "Advanced" elif >= 50: "Intermediate" else "Beginner"
  ↓
OUTPUT: Skill Profile
  → skill_name, claimed_score, confidence, level
```

---

## 🔬 Validation & Testing

### Unit Tests
```python
test_grade_normalization()    # A → 1.0, B → 0.75
test_recency_calculation()     # Year 1 → 0.301, Year 4 → 1.0
test_evidence_weighting()      # Combined factors
test_skill_aggregation()       # Multiple courses → single score
test_confidence_computation()  # More evidence → higher confidence
```

### Edge Cases Handled
- ✅ No courses for skill → Score = 0
- ✅ Zero evidence weight → Skip skill
- ✅ Missing academic year → Derive from course code or use year_taken
- ✅ Invalid grades → Default to 0.0
- ✅ Multiple courses same skill → Proper aggregation

---

**Good luck with your viva! This algorithm demonstrates solid understanding of evidence-based assessment, temporal modeling, and statistical confidence.**
