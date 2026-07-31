# SB-001A — Regression Report

**Programme:** SB-001A  
**Date:** 2026-07-31  
**Verdict:** PASS

---

## Matrix

| Scenario | Result |
|----------|--------|
| Brand new student finalize | PASS — plan stage not-started; Baseline complete |
| Continue from topic | PASS — `curriculum_topic_code` set; prior topics seeded |
| Restart objective | PASS — clears completed topics / position |
| Previously attempted | PASS — attempts mapped into contract |
| Revision experience | PASS — stage revising |
| Returning resume | PASS — no re-ask; restart CTA |
| Runtime A bridge | PASS — StudyPlan created after Twin birth attempt |
| Runtime C thin bridge ordering | PASS — `enrol` only after Baseline ready (spy) |
| Legacy Calibration GET/POST | PASS — redirect to Baseline |
| Founder reset | PASS — Baseline superseded; StudyPlan intact |
| Student restart | PASS — StudyAttempt preserved |
| Twin Builder / Persister suites | PASS — unchanged internals |
| Smoke end-to-end journey | PASS — wizard → Baseline → Home surfaces |
| PX-002 wizard routing | PASS — step 4 / review → Baseline |

## Recommendation / SCI / Runtime regressions

No recommendation algorithm, SCI schema, or Runtime C engine code paths redesigned. Enrolment bridge still calls `enrol_student` / `ensure_active_sci` unchanged after Baseline.

## Commands

```bash
python3 -m pytest \
  tests/application/student_baseline/ \
  tests/presentation/student_baseline/ \
  tests/test_routes.py::TestStudyPlanWizardPx002 \
  tests/application/test_study_plan_calibration_integration.py \
  tests/test_smoke.py \
  tests/application/test_student_calibration_builder.py \
  tests/application/test_calibration_birth_persistence.py \
  -q
```

**Outcome:** 131 passed.
