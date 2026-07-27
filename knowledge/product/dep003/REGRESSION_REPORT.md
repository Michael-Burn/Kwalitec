# DEP-003 — Regression Report

**Programme:** DEP-003 — Student Experience Unification  
**Date:** 2026-07-27

---

## Scope

Verify that presentation unification does not regress educational behaviour, auth, or admin surfaces.

---

## Results

| Area | Verification | Result |
|---|---|---|
| Recommendations | Student Home / templates suite (`test_templates`, trust contract untouched) | **Pass** — no recommendation service changes |
| Onboarding | `/alpha/onboarding` renders under EOS; routes unchanged | **Pass** (`test_dep003_unification`) |
| Study Plan | Wizard / list / view under EOS; forms retained | **Pass** |
| Authentication | Login auth_base; logout via EOS Sign out; login redirects unchanged | **Pass** |
| Session | `session/base` unchanged; dual-run workflow tests | **Pass** |
| Analytics | Still redirects to History under sole | **Pass** (`test_workflow_dual_run`, `test_canonical_journey`) |
| Admin / Console | Console blueprints untouched | **Pass** (blueprint presence assert) |
| Routes | No routes removed; all listed blueprints registered | **Pass** |
| Feature flags | `SOLE_RUNTIME` still gates dual-home + now chrome; dual-run chrome preserved when off | **Pass** |
| Brand / theme | PX-001 + theme surface tests | **Pass** |
| Accessibility drawer (legacy) | Dual-run sidebar backdrop still present | **Pass** (`test_rc001_accessibility`) |

---

## Commands executed

```bash
python3 -m pytest \
  tests/presentation/test_dep003_unification.py \
  tests/presentation/student/test_navigation.py \
  tests/presentation/test_canonical_journey.py \
  tests/presentation/student/test_templates.py \
  tests/presentation/workflows/test_workflow_dual_run.py \
  tests/test_px001_brand_identity.py \
  tests/test_theme_system.py \
  tests/test_rc001_accessibility.py \
  -v
```

**Outcome:** 108 + 37 overlapping suites green in focused runs (all selected tests passed).

---

## Intentionally unchanged behaviour

- Recommendation engines / Runtime A  
- PlanningService / StudyPlanService math  
- Mission engine  
- Persistence and Alembic heads  
- Public registration (still not exposed)

---

## Residual risk

| Risk | Mitigation |
|---|---|
| Shared pages load both `student.css` and `app.css` | Content styles needed; sidebar unused without markup |
| Founder research pages that extend `layouts/base` get EOS under sole | Acceptable; Console remains separate portal |
| Appearance switcher not in EOS topbar | Still on Settings preferences + login; theme.js present |
