# Skill Explanation Pages - Implementation Guide

## Overview
This guide explains the new skill explanation pages that provide students with clear, beginner-friendly explanations of how their skill scores are calculated.

## Architecture

### Pages Created

1. **ExplainChildSkillPage** (`/students/:studentId/explain/child/:skillName`)
   - Shows detailed scoring for individual child skills
   - Displays course-by-course breakdown
   - Explains weights and contributions

2. **ExplainParentSkillPage** (`/students/:studentId/explain/parent/:parentSkill`)
   - Shows parent skill scoring (aggregated from child skills)
   - Groups evidence by child skill
   - Shows hierarchical contribution

3. **SkillCard Component**
   - Reusable card component for displaying skills
   - Includes "Explain Score" button
   - Can be used for both child and parent skills

## Routes Already Configured

```jsx
// In App.jsx
<Route path="/students/:studentId/explain/child/:skillName" element={<ExplainChildSkillPage />} />
<Route path="/students/:studentId/explain/parent/:parentSkill" element={<ExplainParentSkillPage />} />
```

## API Endpoints Expected

The pages call these endpoints (make sure they exist in your backend):

### Child Skills
- `GET /students/:studentId/skills/claimed`
  - Returns: `[{ skill_name, claimed_score, claimed_level, confidence }]`
  
- `GET /students/:studentId/skills/claimed/:skillName/evidence`
  - Returns: `[{ course_code, grade, grade_norm, map_weight, credits, recency, evidence_weight, contribution }]`

### Parent Skills
- `GET /students/:studentId/skills/parent`
  - Returns: `[{ parent_skill, parent_score, parent_level, confidence }]`
  
- `GET /students/:studentId/skills/parent/:parentSkill/evidence`
  - Returns: `[{ child_skill, course_code, grade, credits, recency, map_weight, evidence_weight, contribution }]`

## Using SkillCard Component

You can use the SkillCard component in any skills listing page:

```jsx
import { SkillCard } from '@/components/SkillCard';

// For child skills
<SkillCard
  skillName="Python Programming"
  score={85.5}
  level="Advanced"
  confidence={0.92}
  type="child"
  studentId="IT21013928"
/>

// For parent skills
<SkillCard
  skillName="Software Development"
  score={78.3}
  level="Intermediate"
  confidence={0.88}
  type="parent"
  studentId="IT21013928"
/>
```

## Features

### Beginner-Friendly Design
- **Simple English Explanations**: No technical jargon in main sections
- **Step-by-Step Breakdowns**: Clear numbered steps
- **Visual Indicators**: Color-coded scores, progress bars, badges
- **Collapsible Math Details**: Advanced formulas hidden by default

### Scoring Transparency
- Shows the exact formula used
- Displays intermediate calculation steps
- Explains each component (recency, weights, contributions)
- Visualizes final calculation

### Confidence Explanation
- Simple explanation of what confidence means
- Visual indicator of confidence level
- Contextual messages based on confidence value

### Evidence Display
- Course-by-course breakdown in tables
- Sortable, readable format
- Color-coded grades
- Running totals

## Formulas Displayed

The pages show these formulas in a collapsible "Math Details" section:

```
evidence_weight = map_weight × credits × recency
contribution = grade_norm × evidence_weight
claimed_score = (sum(contribution) / sum(evidence_weight)) × 100
confidence = 1 − exp(−0.25 × sum(evidence_weight))
```

## Styling

All pages use:
- **Tailwind CSS** for styling
- **Lucide React** icons
- Existing UI components (Card, Button, Spinner, ErrorAlert)
- Responsive design
- Gradient accents matching your app theme

## Navigation Flow

```
Skills Page → Click "Explain" → Explanation Page → Back to Skills

Current flow (SkillsPage.jsx):
- Already has "Explain" buttons
- Navigates to: /students/${studentId}/skills/${skillName}/explain
- This goes to the existing SkillExplainPage

New flow options:
1. Keep existing route for parent skills (recommended)
2. OR update to use new routes:
   - Parent skills: /students/${studentId}/explain/parent/${parentSkill}
   - Child skills: /students/${studentId}/explain/child/${skillName}
```

## Integration Options

### Option 1: Use Alongside Existing SkillExplainPage
Keep both the old and new pages, use them for different purposes.

### Option 2: Replace Existing SkillExplainPage
Update the SkillsPage.jsx navigation to use the new routes:

```jsx
// In SkillsPage.jsx, update the Explain button:
<Button
  variant="ghost"
  size="sm"
  onClick={() => navigate(`/students/${studentId}/explain/parent/${encodeURIComponent(skill.parent_skill)}`)}
  className="text-blue-600 hover:text-blue-700"
>
  Explain
</Button>
```

### Option 3: Create Separate Child Skills Page
Create a new page that lists child skills with SkillCard components:

```jsx
import { SkillCard } from '@/components/SkillCard';

export function ChildSkillsPage() {
  const [childSkills, setChildSkills] = useState([]);
  // Fetch child skills...
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {childSkills.map(skill => (
        <SkillCard
          key={skill.skill_name}
          skillName={skill.skill_name}
          score={skill.claimed_score}
          level={skill.claimed_level}
          confidence={skill.confidence}
          type="child"
          studentId={studentId}
        />
      ))}
    </div>
  );
}
```

## Testing Checklist

- [ ] Navigate to explanation pages via "Explain" button
- [ ] Verify all course data displays correctly
- [ ] Check calculation accuracy (totals match displayed score)
- [ ] Test "Back" button navigation
- [ ] Verify responsive design on mobile
- [ ] Test with missing/empty data
- [ ] Check error states
- [ ] Verify loading states
- [ ] Test collapsible Math Details section
- [ ] Verify confidence explanations

## Next Steps

1. **Test the pages**: Navigate to `/students/IT21013928/explain/parent/Software%20Development`
2. **Update backend if needed**: Ensure the evidence endpoints return all required fields
3. **Consider UX improvements**: Add skill comparisons, historical trends, etc.
4. **Add analytics**: Track which explanations students view most

## Example URLs

```
# Parent skill
http://localhost:5173/students/IT21013928/explain/parent/Software%20Development

# Child skill
http://localhost:5173/students/IT21013928/explain/child/Python%20Programming
```

## Troubleshooting

### "Skill not found" error
- Check that the backend returns the skill in the skills list
- Verify URL encoding of skill name (use encodeURIComponent)

### Missing evidence data
- Verify backend returns all required fields
- Check API_BASE URL in api.js

### Calculation mismatch
- Ensure backend and frontend use same rounding
- Check that totals are calculated correctly

### Layout issues
- Verify all UI components are imported
- Check Tailwind CSS is configured properly

## Documentation
- See `SkillCard.jsx` for component props
- See `ExplainChildSkillPage.jsx` for child skill implementation
- See `ExplainParentSkillPage.jsx` for parent skill implementation
