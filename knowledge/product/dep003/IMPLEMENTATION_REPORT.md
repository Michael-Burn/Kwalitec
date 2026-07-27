# DEP-003 — Implementation Report

**Programme:** DEP-003 — Student Experience Unification  
**Date:** 2026-07-27

---

## Summary of implementation

1. Extracted legacy Learning Workspace markup into `layouts/legacy_workspace.html`.  
2. Created shared `layouts/eos_student.html` (EOS header, nav, footer, Sign out).  
3. Converted `layouts/base.html` into a sole-runtime presentation router.  
4. Refactored `student/base.html` to extend the shared EOS layout.  
5. Extended navigation for request endpoints without a Student `page` model.  
6. Injected `eos_navigation` / `eos_active_surface` via template context.  
7. Added workspace width + sign-out styles; Study Plan eyebrows use EOS descriptor under sole.  
8. Added focused regression tests and knowledge deliverables.

---

## Files created (application)

- `app/templates/layouts/eos_student.html`
- `app/templates/layouts/legacy_workspace.html`
- `tests/presentation/test_dep003_unification.py`

## Files created (knowledge)

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

## Files modified

- `app/templates/layouts/base.html` — sole/dual presentation router  
- `app/templates/student/base.html` — extends shared EOS layout  
- `app/templates/student/components/navigation.html` — `eos_navigation` fallback  
- `app/templates/study_plan/list.html` — sole eyebrow → product descriptor  
- `app/templates/study_plan/view.html` — sole eyebrow → product descriptor  
- `app/static/css/student/student.css` — workspace width, topbar nav, sign-out  
- `app/presentation/student/navigation.py` — `build_navigation_for_request`, settings→profile  
- `app/presentation/consolidation.py` — DEP-003 documentation note  
- `app/__init__.py` — EOS nav context injection  
- `tests/presentation/student/test_navigation.py` — request-nav coverage  

---

## Constraints obeyed

| Constraint | Evidence |
|---|---|
| Do not delete blueprints / templates / routes / controllers / services | Templates moved/added; nothing deleted; blueprints asserted present |
| Do not delete migrations / feature flags | Untouched |
| Do not refactor business logic / rewrite planning / onboarding / help | Page bodies unchanged; only outer shell |
| Do not change recommendation engines / persistence / schema | No service/model/migration edits |
| Preserve rollback | `SOLE_RUNTIME=0` → legacy_workspace |

---

## Goals checklist

| Goal | Delivery |
|---|---|
| 1 Single Student Shell | `layouts/eos_student.html` |
| 2 Login Continuity | Wizard via sole `layouts/base` → EOS |
| 3 Navigation Ownership | EOS topnav + Sign out; sidebar hidden under sole |
| 4 Layout Unification | Router on `layouts/base.html` |
| 5 Journey Continuity | Route matrix; no V1 sidebar in journey under sole |
| 6 Template Standardisation | Shared EOS layout; student/base extends it |
| 7 Legacy Preservation | `legacy_workspace.html` + dual-run path |
