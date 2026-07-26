# EP-006.3 — Student Surface Pack (post–EP-006.2)

**Programme:** EP-006.3 — MES Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Purpose:** Student-visible experience judged by Tier B reviewers when `V1_REVIEW_PACKAGE` screens still describe pre-MES Coach copy.  
**Constraint:** Evidence-only — no runtime / UI / educational reasoning changes in this programme.  
**Authority:** REVIEW_PROTOCOL — when package and live student experience diverge, judge the **live student-facing experience**.

---

## 1. What changed for students (EP-006.2)

On the canonical Student Home (`/student/`), when Runtime A delivers a **schema-complete** recommendation MES:

| Element | Student-visible behaviour |
|---|---|
| L1 why | “Why it matters” shows authored `why_recommended` without expand |
| L1 next | “Next” shows authored `suggested_next_action` without expand |
| L2 disclosure | “Why this recommendation” `<details>` with evidence list, confidence + basis, expected benefit, review point |
| Coach panel | Passes through authored why + next (no hard clip when disclosure exists); does **not** invent “highest-value / learning evidence” speech when schema-complete |
| Readiness card | Shows estimate; why / next / evidence / review_point often **borrow recommendation explanation**; `readiness_drivers` on Home VM remain **empty** |

Mission and Analytics templates bind `plan_drivers` / `readiness_drivers` and `review_point` when the presentation adapter supplies schema narratives.

---

## 2. Capture artefacts used by Tier B

| File | Content |
|---|---|
| [`_capture/home_schema_complete.txt`](_capture/home_schema_complete.txt) | True Home VM render — schema-complete MES (no injected readiness drivers) |
| [`_capture/home_cold_start.txt`](_capture/home_cold_start.txt) | Incomplete / reason-code fallback Home render |
| EP-006.2 contract tests | Automated delivery proof for M/D fields |

Representative schema-complete Home speech observed:

> Why it matters — *Your recent practice shows soft recall on measures of location and spread.*  
> Next — *Start a 30-minute descriptive statistics practice session.*  
> Evidence — practice attempts below average; near-term revision list; incomplete syllabus coverage.  
> Confidence — *Suggested — Based on recent practice outcomes and syllabus position.*  
> Review point — *Reassess after tonight's practice set.*  
> Coach — same authored why + next (not “highest-value learning evidence”).

Representative cold-start / incomplete speech observed:

> Why it matters — *A short session on Descriptive statistics foundations offers strong educational return for the time invested.*  
> No Next line; no L2 disclosure; Coach duplicates generic return language + expected benefit.

---

## 3. Known limitations reviewers must treat as current product

1. Dual homes and 30-vs-90 duration mismatch remain (EP-005.2 REM-02 / REM-03 — not fixed by MES delivery).  
2. Home readiness **drivers** are not populated by `home_vm` (`readiness_drivers=()`).  
3. Session outcome / completion strings remain outside MES delivery scope.  
4. Personalisation factor disclosure (MES-10) deferred while flags OFF.  
5. `V1_REVIEW_PACKAGE` overview/walkthrough still mentions pre-MES Coach wording — **stale**; reviewers use this pack + live render instead.

---

## 4. Tier B cohort

Post-change re-reviews archived under [`tier_b_reviews/`](tier_b_reviews/) (baseline EP-004 corpus **not** overwritten):

SV-003, SV-005, SV-008, SV-010, SV-011, SV-012, SV-013, SV-014, SV-015 (N=9; meets methodology interview floor ≥8).

---

**End of STUDENT_SURFACE_PACK**
