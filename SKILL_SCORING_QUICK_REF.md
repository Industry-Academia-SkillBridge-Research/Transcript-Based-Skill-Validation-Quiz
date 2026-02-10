# 📊 Skill Scoring - Quick Reference Card

## 🎯 Core Formula (One Line)

```
Skill Score = (Σ(grade_norm × map_weight × credits × recency) / Σ(map_weight × credits × recency)) × 100
```

---

## 📐 Component Breakdown

| Component | Formula | Range | Purpose |
|-----------|---------|-------|---------|
| **Grade Norm** | `GPA / 4.0` | 0-1 | Academic performance |
| **Map Weight** | From CSV | 0-1 | Course relevance to skill |
| **Credits** | Usually 3.0 | 1-4 | Course importance |
| **Recency** | `e^(-0.4 × years)` | 0-1 | Temporal decay |
| **Evidence Weight** | `weight × credits × recency` | varies | Evidence strength |
| **Contribution** | `grade_norm × evidence_weight` | varies | Quality evidence |
| **Confidence** | `1 - e^(-0.25 × Σ weights)` | 0-1 | Reliability measure |

---

## 🧮 Quick Calculation Example

### Given:
- **Course**: IT1090
- **Skill**: SQL
- **Grade**: B+ = 3.3 GPA
- **Credits**: 3.0
- **Year**: 1 (3 years ago)
- **Map Weight**: 0.35

### Calculate:
```python
1. grade_norm = 3.3 / 4.0 = 0.825

2. recency = e^(-0.4 × 3)
           = e^(-1.2)
           = 0.301

3. evidence_weight = 0.35 × 3.0 × 0.301
                   = 0.316

4. contribution = 0.825 × 0.316
                = 0.261
```

### If SQL appears in 2 courses:
```python
Course 1: contribution = 0.261, weight = 0.316
Course 2: contribution = 0.436, weight = 0.471

Total: contribution = 0.697, weight = 0.787

Score = (0.697 / 0.787) × 100 = 88.6%
Confidence = 1 - e^(-0.25 × 0.787) = 17.9%
Level = "Advanced" (score >= 75)
```

---

## 📊 Grade to Norm Mapping

| Grade | GPA | Norm | %    |
|-------|-----|------|------|
| A+, A | 4.0 | 1.00 | 100% |
| A-    | 3.7 | 0.93 | 93%  |
| B+    | 3.3 | 0.83 | 83%  |
| B     | 3.0 | 0.75 | 75%  |
| B-    | 2.7 | 0.68 | 68%  |
| C+    | 2.3 | 0.58 | 58%  |
| C     | 2.0 | 0.50 | 50%  |
| D     | 1.0 | 0.25 | 25%  |
| F     | 0.0 | 0.00 | 0%   |

---

## ⏰ Recency Decay Table

| Years Since | Formula | Recency | Retention |
|-------------|---------|---------|-----------|
| 0 (current) | e^0     | 1.000   | 100%      |
| 1           | e^-0.4  | 0.670   | 67%       |
| 2           | e^-0.8  | 0.449   | 45%       |
| 3           | e^-1.2  | 0.301   | 30%       |
| 4           | e^-1.6  | 0.202   | 20%       |

**λ = 0.4** (decay constant)

---

## 🎯 Confidence Interpretation

| Evidence Weight | Confidence | Meaning | Courses |
|-----------------|------------|---------|---------|
| 0.5             | 12%        | Very Low | 1       |
| 1.0             | 22%        | Low | 1       |
| 3.0             | 53%        | Medium | 2-3     |
| 6.0             | 78%        | High | 4-5     |
| 10.0            | 92%        | Very High | 6+      |

**α = 0.25** (confidence factor)

---

## 🏆 Skill Level Classification

```
Score >= 75  →  Advanced      (Mastery)
Score >= 50  →  Intermediate  (Proficient)
Score <  50  →  Beginner      (Learning)
```

---

## 🔄 Processing Flow

```
1. Extract: Transcript PDF → Courses (code, grade, credits, year)
2. Join: Courses × Skills (via course_skill_map.csv)
3. Calculate: For each course-skill pair
   - grade_norm = GPA/4.0
   - recency = e^(-0.4 × years_since)
   - evidence = weight × credits × recency
   - contribution = grade_norm × evidence
4. Aggregate: Group by skill
   - Σ contributions
   - Σ evidence_weights
5. Score: (Σ contributions / Σ weights) × 100
6. Confidence: 1 - e^(-0.25 × Σ weights)
7. Level: Advanced/Intermediate/Beginner
```

---

## 💡 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Exponential decay** | Models memory forgetting curve (Ebbinghaus) |
| **Weighted average** | Not all courses equally relevant |
| **Confidence score** | Acknowledges epistemic uncertainty |
| **4.0 normalization** | Standard GPA scale |
| **λ = 0.4** | Balanced decay (not too harsh) |
| **α = 0.25** | Calibrated for 3-6 courses per skill |

---

## 🎤 VIVA Quick Answers

**Q: Why exponential decay?**
> "Models memory retention - skills learned 3 years ago are ~30% as fresh as current learning."

**Q: Why not simple average?**
> "Ignores relevance, timing, and course depth. Our weighted approach is more accurate."

**Q: How does confidence work?**
> "More courses = higher confidence. 1 course = 22%, 3 courses = 53%, 6+ courses = 92%."

**Q: What if grades vary?**
> "Recent excellent performance outweighs old poor performance due to recency weighting."

**Q: Example calculation?**
> "SQL with two courses: contribution₁=0.261, contribution₂=0.436, total=0.697. Evidence: 0.787. Score = 88.6%."

---

## 📈 Real Example Summary

**Student**: IT21013928  
**Skill**: Python

| Course | Grade | Year | Weight | Recency | Evidence | Contribution |
|--------|-------|------|--------|---------|----------|--------------|
| IT1010 | A     | 1    | 0.15   | 0.301   | 0.135    | 0.135        |
| IT1030 | A     | 1    | 0.15   | 0.301   | 0.135    | 0.135        |

**Result:**
- Score: 100.0 (perfect)
- Confidence: 6.5% (only 2 courses)
- Level: Advanced

---

## 🔢 Constants Reference

```python
GRADE_MAPPING = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0
}
DEFAULT_CREDITS = 3.0
RECENCY_DECAY = 0.4
CONFIDENCE_FACTOR = 0.25
```

---

## ✅ Validation Checklist

- ✓ Handles multiple courses per skill
- ✓ Temporal decay applied correctly
- ✓ Weighted by course relevance
- ✓ Confidence increases with evidence
- ✓ Grade mapping accurate
- ✓ Handles edge cases (no courses, zero weights)
- ✓ Outputs 0-100 scale
- ✓ Transparent & explainable

---

**Print this card for quick reference during your viva!**
