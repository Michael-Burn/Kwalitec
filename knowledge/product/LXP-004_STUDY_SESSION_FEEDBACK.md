# LXP-004 — Study Session Feedback & Educational Explainability

**Capability ID:** LXP-004  
**Programme:** Learning Experience Programme  
**Sprint:** Sprint 1  
**Title:** Study Session Feedback & Educational Explainability  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-15  
**Nature:** Product interaction — truthful post-session feedback after Practice Outcome Capture  

---

## Purpose

Explain today's study session in truthful, student-centred language immediately after Practice Outcome Capture (LXP-003).

Students should leave understanding:

- what happened today,
- what Kwalitec observed,
- what Kwalitec can honestly conclude,
- and what happens next.

This capability does **not** redesign:

- Educational Evidence Authority  
- Digital Twin  
- Educational Intelligence  
- Recommendation algorithms  
- Readiness algorithms  
- Learning Mode  

---

## Educational meaning

Feedback is **presentation only**. It narrates lawful persisted state — mission status, study attempts, practice counts — without inventing educational conclusions.

Practice outcomes describe what happened in today's questions. They do **not** mean understanding, knowledge, or mastery increased by themselves.

---

## Workflow

```
Today's Mission
        ↓
Start Study Session (LXP-002)
        ↓
Study Session Screen
        ↓
Finish Study Session
        ↓
Practice Outcome Capture (LXP-003)
        ↓
Study Session Feedback (this capability)
```

### Routes

| Step | Route |
|------|--------|
| Capture | `GET\|POST /missions/<id>/session/finish` |
| Feedback | `GET /missions/<id>/session/recorded` |

Students may close without practice via **I didn't practise today** on the capture screen — lawful `finish_session` with no structured question results.

---

## Four questions answered

Every feedback screen answers:

### 1. What happened today?

Observed session facts only — completion, topic studied, practice counts when recorded.

**Example (practice recorded):**

- You completed today's study session.  
- You studied Topic 4.2.  
- You attempted 20 practice questions.  
- You answered 15 correctly.  

### 2. What did Kwalitec observe?

Only what the student reported or the system lawfully recorded. Never invent conclusions.

### 3. What can Kwalitec honestly conclude?

**Practice recorded:**

- Practice outcomes have been recorded.  
- Future educational guidance can become more reliable as additional practice sessions are completed.  

**No practice:**

- No practice outcomes were available today, so Kwalitec cannot yet update its educational estimates for this topic.  

**Never state:**

- Knowledge increased.  
- Mastery increased.  
- Readiness improved.  

### 4. What happens next?

Guidance on continuing the learning journey — tomorrow's mission, consistent study, returning when ready.

---

## Conditional scenarios

| Scenario | Detection | Honest conclusion boundary |
|----------|-----------|----------------------------|
| **Practice recorded** | Structured question results on latest StudyAttempt | Outcomes recorded; guidance may improve with more sessions |
| **No practice completed** | Mission completed, no structured results | Cannot update practice-based estimates for this topic |
| **Partial study session** | Attempt notes `Session completion: Partially` | Partial session; no practice-based guidance update |
| **Session abandoned** | Attempt notes `Session completion: No` or mission still open | No practice outcomes; mission may remain open |

Scenario resolution: `StudySessionService.resolve_feedback_scenario`.  
Narrative assembly: `EducationalExplainabilityService.build_study_session_feedback`.

---

## Message rules

### Use

- study, practice, understanding, learning, guidance  
- practice outcomes, educational estimates (when explaining limits)  
- honestly, recorded, observed  

### Avoid (student-facing)

- Digital Twin, Evidence, Inference  
- Mastery calculations, confidence scores  
- Internal state names  
- Unsupported attainment claims  

Follow **EDUCATIONAL_EXPLAINABILITY_STANDARD.md** (EIP-003) — facts and estimates visibly distinct; uncertainty named.

---

## Claim boundaries

| Allowed | Forbidden |
|---------|-----------|
| Practice outcomes recorded | Knowledge increased |
| Cannot yet update estimates without practice | Mastery increased |
| Session partially completed | Readiness improved |
| Mission remains open | Presenting estimates as proof |
| Future guidance may become more reliable | Engineering / Twin jargon |

---

## Architecture compliance

Preserves:

- Educational Constitution  
- Logic Registry  
- Evidence Authority  
- Learning Mode  
- State Ownership  

Layering:

```
Templates → mission routes → StudySessionService.build_session_feedback
                          → EducationalExplainabilityService.build_study_session_feedback
```

No Readiness, Recommendation, Twin, or Evidence Authority redesign.

---

## Examples

### Practice recorded

**What happened:** You completed today's study session. You studied Study Topic 4.2. You attempted 10 practice questions. You answered 8 correctly.

**Conclusion:** Practice outcomes have been recorded. Future educational guidance can become more reliable as additional practice sessions are completed.

### No practice

**What happened:** … No practice questions were recorded today.

**Conclusion:** No practice outcomes were available today, so Kwalitec cannot yet update its educational estimates for this topic.

---

## Version 1 limitations

1. Feedback reads latest mission attempt only — not a full session history timeline.  
2. Partial / abandoned paths rely on LXP-002 `finish_session` markers in attempt notes when no practice was captured.  
3. Study Progress update flag on feedback is query-driven for legacy paths only.  
4. No inline links to analytics or readiness surfaces from this screen.  

---

## Cross references

- `LXP-002_STUDY_SESSION_EXPERIENCE.md` — Study Session lifecycle  
- `LXP-003_PRACTICE_OUTCOME_CAPTURE.md` — Practice Outcome Capture  
- `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` — EIP-003 governing standard  
- `BLIND_INTERNAL_ALPHA_REVIEW.md` — student need for post-session explainability  
