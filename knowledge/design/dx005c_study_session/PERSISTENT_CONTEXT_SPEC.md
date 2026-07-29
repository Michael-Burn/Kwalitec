# Persistent Context Spec

**Programme:** DX-005C  
**Status:** Binding for Study Session identity header  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-005A Mission Model; DX-003 Terminology; `SESSION_ARCHITECTURE.md`  

---

## 1. Purpose

The student must never lose track of **where they are in learning**. Persistent context is the identity and position anchor for the entire Session.

Nothing decorative. Orientation only.

---

## 2. Always visible fields

| Field | Required | Example | Visual role |
|---|---|---|---|
| **Subject** | Yes | CS1 · Probability | Dominant identity |
| **Current chapter** | Yes when available | Chapter 3 · Bayes' theorem | Position |
| **Current objective** | Yes | Apply Bayes to exam-style items | Mission alignment |
| **Current activity** | Yes | Question 4 of 12 | What mode now |
| **Session progress** | Yes | Session step 3 of 5 | Session orientation |

Example rendering:

```
CS1 · Probability
Chapter 3 · Bayes' theorem
Objective: Apply Bayes to exam-style items
Activity: Question 4 of 12 · Session step 3 of 5
```

Compressed (narrow):

```
CS1 · Probability · Ch 3 · Bayes' theorem
Q4/12 · Step 3/5 · Apply Bayes to exam-style items
```

---

## 3. Invariants

| Rule | Detail |
|---|---|
| **Never changes role** | Header is identity + position — not a KPI strip, not a nav hub |
| **Object permanence** | Subject matches Home Mission and Choose Exam enrolment |
| **No aliases** | Do not retitle “Learning Adventure: Probability Quest” |
| **Activity sync** | Current activity equals L0 activity label |
| **Progress sync** | Session step advances only when the step actually completes |

If Home Mission and Session disagree on subject/objective for the same session id, that is a defect.

---

## 4. Forbidden in persistent context

- Mastery %, readiness rings, study minutes  
- Streaks, badges, XP, leaderboard rank  
- Multiple CTAs  
- “Welcome back” / tutorial copy  
- Session UUID as primary display (belongs in L3)  
- Decorative icons that compete with type  
- Chapter map as expandable primary nav inside the header  

---

## 5. DTO fields (session header)

| Field | Source | Notes |
|---|---|---|
| `subject_id` | Mission / Session | Stable |
| `subject_code` | Curriculum | Display when available |
| `subject_name` | Curriculum | Display primary |
| `chapter_id` | Session position | Stable |
| `chapter_label` | Syllabus | Display |
| `objective_id` | Mission | Stable |
| `objective_label` | Mission | Display |
| `activity_type` | Current step | read / question / exercise / finding / complete |
| `activity_label` | Derived | e.g. Answer Question |
| `activity_ordinal` | Optional | e.g. 4 |
| `activity_total` | Optional | e.g. 12 |
| `session_step_index` | Session plan | 1-based |
| `session_step_total` | Session plan | |
| `session_id` | Session | L3 only for display |

Technical ids → L3 only.

---

## 6. Sticky behaviour

| Viewport | Behaviour |
|---|---|
| Desktop | Prefer sticky persistent context so identity remains while scrolling L1 |
| Narrow | Persistent context at top; may scroll; L0 Primary stays early in focus order |

Sticky must not obscure the Primary. On very short viewports, allow context to compress rather than covering L1 inputs.

---

## 7. After activity change

On advance / feedback / restore:

1. Update **Current activity** immediately.  
2. Update ordinals / session step when the step completes.  
3. Replace Primary label.  
4. Do **not** remount chrome that feels like a new product.

---

## 8. Relationship to Home continuity

Persistent context **displays** what Home continuity **points to**.

| Home continuity field | Session persistent field |
|---|---|
| `subject_name` | Subject |
| `chapter_id` / label | Current chapter |
| `objective_label` | Current objective |
| `question_ordinal` | Activity ordinal (when question) |

Session is the source of truth for live practice coordinates; Home reads the pointer for Primary resume.

---

## 9. Success test

Cover the L1 content. From the header alone, the student must answer:

1. Which subject?  
2. Which chapter?  
3. Which objective?  
4. Which activity?  
5. How far through this session?
