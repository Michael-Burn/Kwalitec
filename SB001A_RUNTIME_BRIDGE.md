# SB-001A — Runtime Bridge

**Programme:** SB-001A  
**Date:** 2026-07-31

---

## Decision 2B — Thin Runtime C bridge

Runtime C educational behaviour, SCI, traversal, and recommendation engines are **unchanged**.

```text
Baseline complete
    → Twin birth (curriculum scope from subject / version)
    → FounderStudentEnrolmentBridge.enrol(...)
         ├─ Runtime C: enrol_student + ensure_active_sci (unchanged)
         └─ Runtime A: StudyPlanService.create_study_plan (unchanged kwargs)
    → Home
```

## Consistency

Both runtimes initialise from the same Baseline declarations and Twin birth path. Neither asks a second baseline questionnaire after entry.

## Accepted non-changes

- No redesign of `EducationalRuntimeEngineService`
- No SCI schema / traversal changes
- No recommendation algorithm changes
- No StudyPlan generation redesign (only inputs from Baseline)

## Gate

`BaselineFinalizeCoordinator` refuses finalize until draft declarations are complete. Direct bridge enrolment without Baseline is outside the student-facing wizard path; Home gates active Study Plans missing Baseline to `/baseline/for-plan/<id>`.
