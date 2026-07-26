# EP-006.5 — Student Surface Pack (post–EP-006.4)

**Programme:** EP-006.5 — Readiness Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Purpose:** Student-visible readiness experience judged by Tier B reviewers after Home readiness MES delivery.  
**Constraint:** Evidence-only — no runtime / UI / educational reasoning changes in this programme.  
**Authority:** REVIEW_PROTOCOL — when package and live student experience diverge, judge the **live student-facing experience**.

---

## 1. What changed for students (EP-006.4)

On the canonical Student Home (`/student/`), when ReadinessService delivers a **schema-complete** readiness surface:

| Element | Student-visible behaviour |
|---|---|
| L1 why | “Coverage and practice density…” (authored `why_this_estimate`) without expand |
| L1 next | Dedicated readiness next action (not borrowed recommendation next) |
| L2 disclosure | “Why this estimate?” with **named drivers**, evidence, confidence + basis, review point |
| Drivers | e.g. Curriculum coverage, Knowledge strength, Review discipline with approximate values |
| Confidence | **Suggested** + basis tied to coverage / practice density |
| Review point | Explicit reassessment cue (e.g. after two more practice sessions) |
| Fail-open | If readiness surface absent: score/trend may remain; drivers empty; next/review may fall back to recommendation cues |

Recommendation / Coach MES from EP-006.2 remains intact and is judged only as context for trust consistency.

---

## 2. Capture artefacts used by Tier B

| File | Content |
|---|---|
| [`_capture/home_schema_complete.txt`](_capture/home_schema_complete.txt) | Home VM render — schema-complete recommendation **and** readiness MES with drivers |
| [`_capture/home_cold_start.txt`](_capture/home_cold_start.txt) | Incomplete recommendation + no readiness explanation |
| EP-006.4 contract tests | Automated delivery proof for readiness drivers / completeness / fallback |

Representative schema-complete **Readiness** speech observed:

> On Track — *62%*  
> Why — *Coverage and practice density support a mid-band estimate.*  
> Next — *Practise cash flow timing questions for 30 minutes.*  
> Drivers — Curriculum coverage (~55%); Knowledge strength (~68%); Review discipline (~70%).  
> Evidence — topics started; moderate Estimated Knowledge; uneven practice density.  
> Confidence — *Suggested — Based on coverage and recent practice density.*  
> Review point — *Reassess after two more practice sessions.*

Representative cold-start speech observed:

> Mission why — *strong educational return for the time invested.*  
> Readiness card — countdown only; **no** why, drivers, next, or review disclosure.  
> Coach — duplicates generic return language.

Contrast with EP-006.3 pack: readiness card previously borrowed recommendation evidence and showed **`readiness_drivers=()`**.

---

## 3. Known limitations reviewers must treat as current product

1. Dual homes and 30-vs-90 duration mismatch remain (REM-02 / REM-03).  
2. Cold-start nights still lack readiness MES (fail-open / incomplete schema).  
3. “On Track” / percentage chrome can still feel more precise than evidence if L2 is ignored.  
4. Personalisation factor disclosure deferred while flags OFF.  
5. `V1_REVIEW_PACKAGE` may still lag live Home — reviewers use this pack + live render.  
6. Readiness remains **advisory** — not exam-sit clearance.

---

## 4. Tier B cohort

Post-change re-reviews archived under [`tier_b_reviews/`](tier_b_reviews/) (baseline corpora **not** overwritten):

SV-003, SV-005, SV-008, SV-010, SV-011, SV-012, SV-013, SV-014, SV-015 (N=9; meets methodology interview floor ≥8).

Focus: trust / explainability / feedback / adaptation / **calibration** / decision support — readiness unpackability is in-scope for all.

---

**End of STUDENT_SURFACE_PACK**
