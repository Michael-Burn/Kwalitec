# EV-001 — Executive Summary

**Programme:** EV-001 — Publication Pipeline Engineering Verification  
**Status:** Complete  
**Predecessor:** PI-002R — Publication Validation Wiring  
**Date:** 2026-07-29  
**Method:** Visible Founder workflow + supporting engineering evidence (no application code changes; no gate bypass; no DB seeding of publication facts)

---

## Verdict

# VERIFIED WITH MINOR CONDITIONS

The publication pipeline is operational for the Founder Studio happy path:

```text
Draft → Validated → Preview Ready → Approved → Published → Ready
```

Subject **CS1V** (`ws-cs1v`, version **2026.1**) completed every Studio lifecycle state through the normal production UI path after PI-002R.

One minor non-blocking condition remains on the student Choose Exam surface (see below). Recommend **FV-001B** after clearing that condition (or with Founder scope limited to Studio Ready if student discovery is deferred).

---

## What was proved

| Stage | Result | Key evidence |
|---|---|---|
| 1 Subject Creation | Pass | CS1V created; Draft workspace `ws-cs1v` |
| 2 Document Upload | Pass | Official CMP + Official Syllabus uploaded to correct slots; documents Ready |
| 3 Structure Preparation | Pass | CIP entities materialised; 21 topics/subtopics + 5 objectives in package |
| 4 Validation | Pass | `Validation completed successfully · passed`; blocking issues = 0 |
| 5 Preview | Pass | `Preview ready · ready_for_review · 23 topics` |
| 6 Approval | Pass | `We've approved your curriculum successfully`; preview · approved |
| 7 Publication | Pass | `We've published your verified curriculum successfully`; Status Published |
| 8 Ready (Subjects) | Pass | `CS1V Ready · Current Version 2026.1 · Published 2026-07-28` |
| 9 Student Catalogue | Fail (UI) | Active package exists; Choose Exam raises `AttributeError` in `_format_release` |

---

## Curriculum identity

Exactly one authoritative chain was used:

`CS1V` → `ws-cs1v` → Foundation version id **1** / label **2026.1** → active `published_curriculum_packages` row id **1** (same `version_id`).

Validation, Preview, Approval, Publication, and Ready all consumed that instance. No duplicate curriculum representation was observed.

---

## Regression

UI gate probes (incomplete CS1Z) and PI-002R pytest suites passed:

- Publish without approval refused  
- Approve without validation refused  
- Validate without documents fails with missing CMP + syllabus findings  
- Preview without structure not ready  
- `189` + `41` related tests green  

Publication safety was not weakened.

---

## Minor condition (must clear before student-facing FV checks)

`SubjectCatalogueService._format_release` assumes `published_at` is a `datetime`, but the authority projection can supply a `str`. Consequence:

- `/study-plan/wizard/1` returns **500** when listing published subjects  
- Students cannot see/enrol CS1V in Choose Exam despite Ready package materialisation  

This is a presentation/projection defect, not a Studio publication-gate failure. Data-layer Ready is present.

---

## Recommendation

1. Fix `_format_release` / authority date typing (tiny follow-up; out of EV-001 scope — EV-001 did not modify application code).  
2. Re-check Choose Exam discoverability for CS1V.  
3. Proceed to **FV-001B — Final Founder Studio Blind Validation**.

---

## Artefacts

| File | Purpose |
|---|---|
| [`LIFECYCLE_VERIFICATION.md`](LIFECYCLE_VERIFICATION.md) | Stage pass/fail rollup |
| [`CURRICULUM_IDENTITY_VERIFICATION.md`](CURRICULUM_IDENTITY_VERIFICATION.md) | Single-identity proof |
| [`STAGE_BY_STAGE_EVIDENCE.md`](STAGE_BY_STAGE_EVIDENCE.md) | Screenshots + facts |
| [`REGRESSION_VERIFICATION.md`](REGRESSION_VERIFICATION.md) | Safety gate evidence |
| [`ENGINEERING_SIGNOFF.md`](ENGINEERING_SIGNOFF.md) | Formal sign-off |
| [`_evidence/`](_evidence/) | Raw JSON, walk script, screenshots |
