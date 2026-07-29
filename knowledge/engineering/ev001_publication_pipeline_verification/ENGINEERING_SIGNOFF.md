# Engineering Sign-off

**Programme:** EV-001 — Publication Pipeline Engineering Verification  
**Date:** 2026-07-29  
**Scope:** Engineering verification only (not Founder usability; not FV-001B)

---

## Sign-off choice

# VERIFIED WITH MINOR CONDITIONS

The publication pipeline is operational.

Minor non-blocking issues remain.

Recommend FV-001B.

---

## Statement

A real subject (**CS1V**) successfully transitioned through the normal production Founder path:

```text
Draft → Validated → Preview Ready → Approved → Published → Ready
```

without application code changes, gate bypasses, database publication edits, or seeded publication facts.

The same authoritative curriculum identity (`CS1V` / `ws-cs1v` / version `2026.1` / Foundation version id `1`) was used by Validation, Preview, Approval, Publication, and Ready package materialisation.

All required regression checks passed.

---

## Minor conditions

1. **Student Choose Exam 500** — `SubjectCatalogueService._format_release` raises `AttributeError` when authority `published_at` is a `str`. Active Ready package for CS1V exists, but `/study-plan/wizard/1` cannot render the catalogue.  
   - **Impact:** Blocks visible student discoverability/enrol cue verification.  
   - **Not:** a Studio Validate/Preview/Approve/Publish wiring failure.  
   - **Action before FV-001B student checks:** fix date coercion; re-verify Choose Exam shows CS1V as Ready.

2. **Workflow chrome lag** — After publish, workspace workflow chrome can still highlight Content Sources while Status already shows Published / Subjects shows Ready. Non-blocking honesty residual (PI-002 Phase 5 class).

---

## Exit criteria mapping

| Criterion | Status |
|---|---|
| Draft → … → Ready without manual intervention | ✓ |
| Same authoritative curriculum throughout | ✓ |
| All regression checks passed | ✓ |
| Engineering sign-off issued | ✓ (this document) |
| Student Subject Catalogue visible Ready | ✗ UI (condition #1) |

---

## Recommendation

Proceed to **FV-001B — Final Founder Studio Blind Validation** for the Studio publication experience.

Clear minor condition #1 before treating student discoverability as Founder-validated, or explicitly scope FV-001B to Studio Ready first and schedule a short student-catalogue recheck after the date-format fix.

---

## Evidence package

- [`EV001_EXECUTIVE_SUMMARY.md`](EV001_EXECUTIVE_SUMMARY.md)  
- [`LIFECYCLE_VERIFICATION.md`](LIFECYCLE_VERIFICATION.md)  
- [`CURRICULUM_IDENTITY_VERIFICATION.md`](CURRICULUM_IDENTITY_VERIFICATION.md)  
- [`STAGE_BY_STAGE_EVIDENCE.md`](STAGE_BY_STAGE_EVIDENCE.md)  
- [`REGRESSION_VERIFICATION.md`](REGRESSION_VERIFICATION.md)  
- [`_evidence/lifecycle.json`](_evidence/lifecycle.json)  
- [`_evidence/engineering_analysis.json`](_evidence/engineering_analysis.json)  
- [`_evidence/screenshots/`](_evidence/screenshots/)  

---

## Explicit non-claims

- This is not a Founder usability verdict.  
- This does not declare FV-001B GO.  
- Application code was not modified under EV-001.
