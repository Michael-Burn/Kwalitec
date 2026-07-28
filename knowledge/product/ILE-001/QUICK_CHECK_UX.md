# Quick Check UX — ILE-001B

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001B — Quick Check Experience  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** ILE-001 design pack + ILE-001A product foundations  

---

## Purpose

Describe the first student-visible Adaptive Assessment experience: a calm, Mission-embedded **Quick Check** that feels like a brief confidence-building learning conversation — never a quiz or exam.

Product goal: students finish feeling *“I understand why Kwalitec asked me those questions.”*

---

## Learner journey

```
Mission
  → Quick Check invitation (entry card)
  → Why this check? (introduction)
  → Begin
  → Questions (already-selected learning check)
  → Reflection
  → Completion
  → Mission resumes (evidence acknowledgement)
```

The learner should never feel they have left the Mission.

---

## Surfaces

| Surface | Role |
|---|---|
| **Mission entry card** | Title, duration, invitation, Continue / Why this? / Not now |
| **Introduction** | Why framing from copy registry; Begin |
| **Question** | Calm progress, stem, response, optional hint, Pause |
| **Paused** | Resume or defer — no pressure |
| **Reflection** | Brief reflective prompt |
| **Completion** | Thank you; evidence; uncertainty; Mission benefit; Return |
| **Mission return** | “We've gathered useful evidence.” |

---

## Entry experience

- **Title:** Quick Check  
- **Duration:** About 3–8 minutes (session registry)  
- **Invitation:** “Let's strengthen today's understanding.”  
- **Primary CTA:** Continue  
- **Secondary:** Why this?  
- **Note:** Tutor explanation available.  
- **Defer:** Not now  

Gated by `KWALITEC_ADAPTIVE_ASSESSMENT` + `KWALITEC_QUICK_CHECK` (and optional subject/cohort allow-lists).

---

## Question experience

**Never show**

- Question N of M  
- Score / timer countdown  
- Incorrect! / Correct!  
- Grades, pass/fail, mastery claims  

**Do show**

- Calm progress labels (“Take your time” / “Making progress” / “Almost there”)  
- Hints on request  
- Pause / Resume  
- Accessibility metadata (region, keyboard, reduced motion)

Items come from an **already-selected** presentation learning check (`selected_learning_check.py`). No adaptive selection in ILE-001B.

---

## Completion experience

Show:

1. Thank you  
2. What evidence was collected  
3. What remains uncertain  
4. How today's Mission may benefit  

Then return to Mission with acknowledgement copy.

---

## Copy & terminology

All learner chrome resolves through `app/application/adaptive_assessment/copy_registry.py`.  
Terminology validation (`terminology.py`) must pass — no exam/test/pass/fail/weak student language.

---

## Telemetry

Approved behavioural events only (`telemetry.py`):

- `AdaptiveAssessmentViewed`  
- `QuickCheckStarted` / `Dismissed` / `Completed`  
- `AssessmentDeferred` / `AssessmentExplained`  

No answers, scores, Twin state, or learner educational payloads.

---

## Implementation map

| Concern | Location |
|---|---|
| Experience orchestration | `app/application/adaptive_assessment/quick_check_experience.py` |
| Presentation contracts | `quick_check_contracts.py` |
| Already-selected check | `selected_learning_check.py` |
| HTTP / templates | `app/presentation/adaptive_assessment/` |
| Mission embed | `mission_embed.py` + Session / Mission templates |
| CSS / JS | `app/static/css|js/adaptive_assessment/` |

---

## Explicit non-goals (ILE-001B)

- Adaptive item selection  
- Twin / Reasoning / Mission planning changes  
- Assessment Engine scoring changes  
- Grades, pass/fail, mastery theatre  
- Database / Alembic changes  

Next: **ILE-001C — Intent framing + eligibility visibility**.

---

**End of QUICK_CHECK_UX**
