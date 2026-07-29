# PX-001 — Updated Student Flow

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Authoritative Student product workflow

---

## 1. Persona

Students **never** upload learning material.  
Students **consume** published (Verified) curricula only.  
Educational Intelligence personalises learning **after enrolment**.

---

## 2. Canonical onboarding

```
Welcome
    ↓
Choose Exam
    ↓
Exam Date
    ↓
Study Availability
    ↓
Begin Learning
```

**No uploads.** No CMP, no syllabus, no publish, no Knowledge Graph, no extraction.

---

## 3. Stage-by-stage product behaviour

| Stage | Student action | Rules |
|-------|----------------|-------|
| **Welcome** | Orient to Kwalitec as study preparation | Plain language; no Education OS / Studio jargon |
| **Choose Exam** | Pick a **Subject** from the Subject Catalogue | Only **Ready** subjects selectable; **Coming Soon** shows preparation message |
| **Exam Date** | Enter exam / sitting date | Required for planning |
| **Study Availability** | Enter available study time / days | Required for planning |
| **Begin Learning** | Confirm → enrol / create Study Plan | Triggers existing LP-001 / bridge / plan path — no new EI logic in UI |

Post-onboarding daily loop (unchanged architecture, clarified language):

```
Home (Today’s Focus) → Study session → Progress (Journey / History) → Revision as needed
```

---

## 4. What students must never see

| Forbidden surface / affordance | Rationale |
|--------------------------------|-----------|
| Upload CMP | Curriculum Authority only |
| Upload Syllabus | Curriculum Authority only |
| Publish Curriculum | Curriculum Authority only |
| Knowledge Graph | Internal / Founder Advanced |
| Extraction / Review Queue | Founder Studio |
| Curriculum Edition editors / workspaces | Students see Subjects + catalogue metadata only |
| Console / Founder Studio nav | Separate persona chrome |

---

## 5. Subject availability behaviour

| Availability | UI | Selection |
|--------------|-----|-----------|
| **Ready** | Shown as available | Allowed → continue to Exam Date |
| **Coming Soon** | Shown with professional message | **Not** selectable |

### Coming Soon message (canonical intent)

> This subject’s verified curriculum is still under preparation. It will become available when publishing is complete. You cannot start studying this exam yet.

Tone: professional, calm, no pipeline error codes.

---

## 6. Mapping from today’s wizard

| Today (approx.) | PX-001 |
|-----------------|--------|
| Alpha onboarding | Welcome (simplify) |
| Wizard step 1 Examination + step 2 Paper / “Published Curriculum” | **Choose Exam** (Subject Catalogue) |
| Step 3 Exam Date | **Exam Date** |
| Step 5 Availability | **Study Availability** |
| Steps 4 Position, 6 Learning Style, 7 Target, 8 Review | Fold, defer, or minimise — must not reintroduce uploads; keep only if product still requires them behind progressive disclosure |
| Calibration / Home | **Begin Learning** destinations per existing Runtime A/C law (VP-001 / PI-002A) — do not invent a third runtime |

PX-001 does **not** require deleting Runtime A Temporary compatibility. It requires the **visible** path to match Choose Exam → Date → Availability → Begin Learning.

---

## 7. When Educational Intelligence starts

```
Choose Exam (Ready subject)
  → Exam Date + Availability
  → Begin Learning (enrolment / Study Plan create)
  → LP-001 onboard_after_enrolment (when published edition exists)
  → EI personalisation on Home / Session / Revision via RI-001 Preferred Authority
```

Before enrolment: **no** student-facing Twin, Decisions, or Knowledge Graph.  
After enrolment: intelligence runs behind domain language (Today’s Focus, Study Plan) — internals stay hidden.

---

## 8. Navigation after Begin Learning

Student shell only (`NAVIGATION_CHANGES.md`):

- Home (Today’s Focus)  
- Journey  
- Revision  
- History  
- Study Plan  
- Settings  
- Help  

No Founder concepts in this tree.

---

## 9. Acceptance checks

- [ ] Onboarding path has no upload / publish / extraction steps  
- [ ] Choose Exam uses Subject Catalogue with Ready / Coming Soon  
- [ ] Coming Soon cannot enrol  
- [ ] Begin Learning uses LP-001 / existing bridge — no parallel intelligence bootstrap in the template  
- [ ] Student never navigates to `/console/studio`  
- [ ] Success criteria: students study only published (Ready) subjects  

---

**End of Updated Student Flow**
