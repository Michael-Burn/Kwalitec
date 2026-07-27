# DEP-003 — Completion Report

**Programme:** DEP-003 — Student Experience Unification  
**Date:** 2026-07-27  
**Status:** Implementation complete (presentation unification)  
**Predecessor:** DEP-002 (root cause H)

---

## Summary

DEP-003 removes the student-visible dual-application experience identified by DEP-002 without deleting the legacy runtime. Under `KWALITEC_V2_SOLE_RUNTIME=1`, every student-facing page that previously rendered the Learning Workspace sidebar now renders inside a single Education Operating System shell (`layouts/eos_student.html`), including Study Plan wizard (login continuity), Help, Onboarding, and Settings. Controllers, services, blueprints, routes, feature flags, and database schema are unchanged. Dual-run rollback restores legacy chrome via the same layout router when sole runtime is off.

---

## Files Created

### Application

- `app/templates/layouts/eos_student.html`
- `app/templates/layouts/legacy_workspace.html`
- `tests/presentation/test_dep003_unification.py`

### Knowledge

- `knowledge/product/dep003/EXECUTIVE_SUMMARY.md`
- `knowledge/product/dep003/STUDENT_ROUTE_MATRIX.md`
- `knowledge/product/dep003/LAYOUT_STANDARDISATION.md`
- `knowledge/product/dep003/NAVIGATION_MIGRATION.md`
- `knowledge/product/dep003/PRESENTATION_ARCHITECTURE.md`
- `knowledge/product/dep003/REGRESSION_REPORT.md`
- `knowledge/product/dep003/IMPLEMENTATION_REPORT.md`
- `knowledge/product/dep003/VALIDATION_REPORT.md`
- `knowledge/product/dep003/COMPLETION_REPORT.md`

---

## Files Modified

- `app/templates/layouts/base.html`
- `app/templates/student/base.html`
- `app/templates/student/components/navigation.html`
- `app/templates/study_plan/list.html`
- `app/templates/study_plan/view.html`
- `app/static/css/student/student.css`
- `app/presentation/student/navigation.py`
- `app/presentation/consolidation.py`
- `app/__init__.py`
- `tests/presentation/student/test_navigation.py`

---

## Tests Executed

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

**Outcome:** All selected tests passed (DEP-003 suite 37 passed; broader related suites 108 passed in the combined focused run).

---

## Migration Impact

**None.** No Alembic revisions added or changed. No schema changes.

---

## Architecture Compliance

- Layering preserved: presentation-only changes in templates/CSS and thin nav helpers; blueprints remain HTTP; services/engines untouched.  
- Curriculum V1/V2: **unaffected** — no curriculum import, traversal, or engine edits.  
- Sole runtime remains a presentation gate (ADR / V2-023 posture); physical blueprint retirement deferred.  
- `student/base` and shared student templates now share one EOS layout under sole (Goal 6).

---

## Technical Debt

- Legacy templates and sidebar partials remain on disk for dual-run / soak (intentional).  
- Soft-dead dashboard/mission/analytics templates still exist (redirect-only under sole).  
- EOS topbar does not yet include appearance switcher (available on Settings preferences).  
- Future programme may physically quarantine or delete legacy chrome after soak.

---

## Known Limitations

- Registration is not publicly exposed (product constraint; out of scope).  
- Session uses a focused EOS Session chrome rather than full product nav (by design).  
- Under dual-run, shared pages intentionally show legacy chrome again.  
- Authenticated production dogfood walkthrough recommended post-deploy (see `VALIDATION_REPORT.md`).

---

## Success criteria

| Criterion | Met? |
|---|---|
| Students perceive one application under sole | **Yes** |
| All student-facing pages in EOS shell under sole | **Yes** |
| Legacy presentation hidden from students under sole | **Yes** |
| Legacy implementation available / rollback intact | **Yes** |
| No business logic / migrations / blueprint removal | **Yes** |
| Production deployable at every commit | **Yes** |
