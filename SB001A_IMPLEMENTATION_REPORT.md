# SB-001A — Implementation Report

**Programme:** Student Baseline Integration Programme SB-001A  
**Phase:** Educational Continuity Implementation  
**Authority:** RF-001 · BF-001 · RF-001A · SB-001 Product Specification  
**Date:** 2026-07-31  
**Verdict:** PASS — Baseline replaces student-facing Calibration; Twin Builder reused; thin Runtime C bridge; history-safe reset.

---

## Summary

SB-001A establishes Baseline as the single educational entry point for newly enrolled subjects. Progressive one-question-at-a-time capture initialises the Student Digital Twin via existing Calibration builders, then creates a Runtime A Study Plan or Runtime C enrolment. Legacy Calibration routes redirect safely. Founder inspect / reset / restart never delete study history.

---

## Files Created

- `migrations/versions/202607310001_sb001a_student_baselines.py`
- `app/models/student_baseline.py`
- `app/application/student_baseline/` (`enums`, `declarations`, `mapper`, `service`, `birth`, `coordinator`, `__init__`)
- `app/student_baseline/` (`__init__`, `forms`, `routes`)
- `app/templates/student_baseline/` (`base`, step templates, `resume`)
- `app/founder/dashboard/templates/founder_dashboard/student_baseline.html`
- `tests/application/student_baseline/test_mapper_and_service.py`
- `tests/presentation/student_baseline/test_sb001a_baseline.py`
- `SB001_PRODUCT_SPECIFICATION.md`
- `SB001A_BASELINE_FLOW.md`
- `SB001A_DIGITAL_TWIN_MAPPING.md`
- `SB001A_RUNTIME_BRIDGE.md`
- `SB001A_CALIBRATION_DEPRECATION.md`
- `SB001A_IMPLEMENTATION_REPORT.md`
- `SB001A_REGRESSION_REPORT.md`

---

## Files Modified

- `app/models/__init__.py` — register `StudentBaseline`
- `app/__init__.py` — register `student_baseline_bp`
- `app/study_plan/routes.py` — availability → Baseline; review redirects
- `app/calibration/routes.py` — deprecate UI; redirect to Baseline
- `app/application/platform_integration/enrolment_bridge.py` — Runtime A redirect target
- `app/presentation/student/routes.py` — Home Baseline gate
- `app/founder/dashboard/routes.py` — inspect / reset / restart
- `app/founder/dashboard/templates/founder_dashboard/participants.html` — Baseline link
- `tests/test_routes.py`, `tests/test_smoke.py`, `tests/application/test_study_plan_calibration_integration.py`

---

## Tests Executed

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

python3 -m ruff check \
  app/application/student_baseline \
  app/student_baseline \
  app/calibration/routes.py \
  app/models/student_baseline.py
```

**Outcome:** 131 pytest cases green on the SB-001A + smoke + Twin builder suites; ruff clean on Baseline packages.

---

## Migration Impact

Alembic revision `202607310001` adds `student_baselines` only. No changes to SCI, Runtime C, study attempts, or twin snapshot schemas. Tests use `db.create_all()` and pick up the new ORM automatically.

---

## Architecture Compliance

- Layering preserved: Presentation → Application Baseline service/coordinator → existing Calibration Builder → TwinRepository / StudyPlanService / EnrolmentBridge
- Curriculum V1/V2: topic picker uses `CurriculumEngineService.get_topics_flat` / `load_auto`
- Absolute constraints respected: no Runtime C / SCI / recommendation / StudyPlan generation / Twin architecture redesign
- Evidence never discarded on Baseline restart/reset (supersede-only)

---

## Technical Debt

- Alembic still has multiple heads; `202607310001` revises `202611120001` (Twin snapshots). A merge revision may be needed before production migrate.
- Runtime C receives Baseline only as ordering/gate + stored Baseline row; no SCI node seed overrides (accepted thin-bridge debt).
- Home gate covers active Study Plan subjects; Runtime C-only enrolments without Study Plan rely on Baseline finalize having completed first.

---

## Known Limitations

- No adaptive placement / diagnostics (V2)
- Optional highest mark stored on Baseline only (contract still forbids marks as educational warrant)
- Calibration templates retained on disk but unused by live routes

---

## Student Impact Assessment

- **Problem:** Students were forced toward Chapter 1 / post-plan Calibration theatre
- **Benefit:** Kwalitec meets them where they are before teaching begins
- **Learning benefit:** Plans and Twin priors start from declared position and objective
- **Success metrics:** Baseline complete before Home/Mission; history intact on restart
- **Risks:** Thin Runtime C bridge does not yet seed SCI from Baseline
- **Assumptions:** Self-declared Baseline is honest enough for V1 planning

## Estimated KSI contribution

Provisional ΔKSI focused on continuity / onboarding honesty (K1/K3 framing). Infra-adjacent Twin birth reuse → modest provisional lift; validation deferred to RF-002 / G1.

## Evidence collected

- `tests/application/student_baseline/`
- `tests/presentation/student_baseline/`
- Updated smoke + PX-002 + calibration redirect suites
- Mapping docs above

## Lessons learned for student value

Replacing post-plan Calibration with pre-plan Baseline removes the “enrol → dashboard → calibrate” dissonance. Progressive disclosure keeps intake under two minutes without a questionnaire wall.

## Explainability Review

N/A for new recommendation surfaces — Baseline is self-declared intake. Twin provenance remains `self_declared` / `thin`.

## Recommendation Quality Review

N/A — recommendation algorithms unchanged.

## Version 1 readiness residual

Supports G1 continuity narrative; does not alone close commercial readiness gates. Residual: Alembic head merge; SCI seed from Baseline (optional follow-on).

## CRI domains improved

Provisional CR continuity / onboarding clarity. ΔCRI = 0 validated (no board update without Founder validation).
