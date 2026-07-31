# UX-001 — Student Home Experience Redesign

**Programme:** UX-001 — Redesign the Student Home Experience  
**Status:** Complete  
**Date:** 2026-07-31

---

### Summary

Student Home is now a calm decision surface: greeting → Today's Mission hero → Progress → Tomorrow → quiet Quick Actions. Educational detail (why today, objectives, concept focus, stages, expected outcome, checkpoint/reflection previews) moved to Session Overview. START SESSION opens Overview without auto-beginning Activity; Begin Session on Overview starts practice. Runtime C, SCI lifecycle, and recommendation logic are unchanged — presentation and post-start landing only.

### Files Created

- `tests/presentation/student/test_ux001_home_session_split.py`
- `UX001_STUDENT_HOME_REDESIGN_REPORT.md` (this file)

### Files Modified

- `app/templates/student/home.html` — decision-only hierarchy
- `app/templates/design_system/macros.html` — `ds_mission_hero`
- `app/static/css/design_system.css` — calm Home + session briefing styles
- `app/templates/session/partials/session_body.html` — Overview briefing block
- `app/presentation/student/dto/student_home.py` — greeting / page question
- `app/presentation/student/dto/adaptive_workspace.py` — page question copy
- `app/presentation/student/services/student_home_service.py` — greeting, signals without duration duplicate
- `app/presentation/student/adaptive_workspace.py` — demote Start/Continue from Quick Actions
- `app/presentation/student/routes.py` — start/revision land on Overview (no auto-begin)
- `app/presentation/session/dto/study_session.py` — briefing fields
- `app/presentation/session/services/study_session_service.py` — Overview briefing projection
- Presentation contract tests updated for the Home/Session split

### Tests Executed

```bash
python3 -m pytest \
  tests/presentation/student/test_ux001_home_session_split.py \
  tests/presentation/student/test_ux001_premium_beta.py \
  tests/presentation/student/test_cq003_daily_habit_fit.py \
  tests/presentation/session/test_factory.py \
  tests/test_kwp013_adaptive_workspace.py \
  tests/test_kwp015_educational_authoring.py \
  tests/test_kwp006_home_exam_briefing.py \
  tests/test_kwp002_student_value_activation.py \
  tests/presentation/student/test_cq006_premium_craft.py \
  tests/presentation/student/test_templates.py \
  tests/presentation/test_sop001_student_os.py \
  tests/test_dx006b_student_home.py \
  tests/presentation/student/test_routes.py \
  tests/presentation/session/test_product_language.py \
  tests/test_v1s005_dogfood_remediation.py::test_home_template_has_remediation_markers \
  tests/presentation/student/test_rr001_2_premium_experience.py::test_home_mission_intelligence_relocated_off_home \
  tests/presentation/student/test_recommendation_commitment_contract.py::test_cf_a04_forbidden_shame_strings_absent \
  tests/test_kwp014_knowledge_architecture.py::test_templates_wire_curriculum_map_and_founder \
  -q
```

Outcome: passing for the suites above.

```bash
python3 -m ruff check app/presentation/student/services/student_home_service.py \
  app/presentation/student/routes.py \
  app/presentation/session/services/study_session_service.py \
  app/presentation/student/adaptive_workspace.py \
  app/presentation/student/dto/student_home.py \
  app/presentation/session/dto/study_session.py \
  app/presentation/student/dto/adaptive_workspace.py \
  tests/presentation/student/test_ux001_home_session_split.py
```

### Migration Impact

None.

### Architecture Compliance

- Presentation-only changes; blueprints still delegate to existing services.
- Curriculum V1/V2 traversal untouched.
- Runtime C enrolment / SCI `ensure_active_sci` / Adaptive recommendation ranking unchanged.
- Session FSM surfaces unchanged; Overview briefing is additive presentation.

### Technical Debt

- CQ-002 / CQ-003 “one click into Activity” habit continuity is intentionally reversed for UX-001 clarity. Habit metrics should be re-checked after dogfood.
- Overview briefing enrichment via Educational Authoring is best-effort; sparse topics may show fewer briefing blocks.
- Workspace composer still builds episodes/forecast for other consumers even though Home no longer renders them — fine for now, optional future trim.

### Known Limitations

- Extra Study / Forecast / Journey highlights are no longer on Home (reachable via Quick Actions / shell nav).
- MES “Why this Session?” disclosure is not yet a dedicated Session Overview accordion; why-copy uses overview `why_studying` plus authoring narrative when available.
- Resume Continue still deep-links to Overview (existing behaviour); activity resume redirect rules inside session routes remain authoritative once the student has begun.
