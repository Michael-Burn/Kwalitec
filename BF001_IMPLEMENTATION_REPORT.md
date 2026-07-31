# BF-001 — Implementation Report

**Programme:** Blocker Fix Programme BF-001  
**Phase:** Founder Validation Readiness  
**Authority:** RF-001 · PX-004 PASS  
**Date:** 2026-07-31  
**Verdict:** PASS — Founder workflows no longer trap operators; recovery paths restored.

---

## Summary

BF-001 repaired six Category A Founder Curriculum Studio blockers without redesign or new educational features. Expand/Collapse, back navigation, version assignment (`YYYY.N`), workflow restart, subject delete/archive, and catalogue duplicate rendering are restored to intended behaviour.

---

## Files Created

- `tests/presentation/curriculum_studio/test_bf001_blocker_remediation.py`
- `BF001_IMPLEMENTATION_REPORT.md`
- `BF001_ROOT_CAUSE_ANALYSIS.md`
- `BF001_REGRESSION_REPORT.md`

---

## Files Modified

### Client / presentation

- `app/static/js/curriculum_preview_tree.js` — plain-object forest; keyboard a11y
- `app/static/css/design_system.css` — catalogue list specificity
- `app/templates/curriculum_studio/workspace.html` — Back / Restart; version help
- `app/templates/design_system/macros.html` — lifecycle actions; `data-subject-id`
- `app/presentation/curriculum_studio/forms.py` — retreat/reset/archive/delete; `YYYY.N` validator
- `app/presentation/curriculum_studio/routes.py` — retreat, reset, archive, delete-draft; assign reconcile
- `app/presentation/curriculum_studio/view_models.py` — flashes
- `app/presentation/curriculum_studio/operator_guidance.py` — version/lifecycle recovery copy

### Application / founder projection

- `app/application/curriculum_studio/version_history_service.py` — subject ensure + error mapping
- `app/application/curriculum_studio/workspace_service.py` — `archive_workspace`, `delete_draft`
- `app/application/curriculum_studio/curriculum_studio_service.py` — facade methods
- `app/founder/dashboard/dto/founder_workspace.py` — `can_retreat`, `can_reset`
- `app/founder/dashboard/dto/founder_subjects.py` — lifecycle fields
- `app/founder/dashboard/services/founder_workspace_service.py` — recovery flags
- `app/founder/dashboard/services/founder_subjects_service.py` — lifecycle actions

### Tests

- `tests/presentation/curriculum_studio/test_forms.py` — reject semver; accept `2026.1`

---

## Tests Executed

```bash
python3 -m pytest \
  tests/presentation/curriculum_studio/test_bf001_blocker_remediation.py \
  tests/presentation/curriculum_studio/test_forms.py \
  tests/presentation/curriculum_studio/test_messaging.py \
  tests/presentation/curriculum_studio/test_product_language.py \
  tests/presentation/curriculum_studio/test_rendering.py \
  tests/test_dx006b_founder_subjects.py \
  tests/certification/test_pr001a_founder_operations.py::TestOperationalErrorRecovery \
  -q

python3 -m ruff check \
  app/presentation/curriculum_studio/ \
  app/application/curriculum_studio/workspace_service.py \
  app/application/curriculum_studio/version_history_service.py \
  app/founder/dashboard/services/founder_workspace_service.py \
  app/founder/dashboard/services/founder_subjects_service.py
```

**Outcome:** All listed pytest suites green; ruff clean on touched modules.

---

## Migration Impact

**None** — no Alembic revisions. Lifecycle uses existing workspace status vocabulary and registry delete.

---

## Architecture Compliance

- Presentation → services → registry/Management ports preserved.
- No Runtime / SCI / recommendation / curriculum processing changes.
- Curriculum V1/V2 traversal: **N/A** (Studio workflow repair only).
- Retreat/reset reuse existing domain transition map (no duplicate processing).

---

## Technical Debt

- Restart resets **stage** to Upload/SUBJECT; document bytes and checklist facts are retained (intentional — no orphan duplicates). Clearing facts on restart is a possible follow-up if Founders want a harder reset.
- Management archive on subject archive is best-effort when the version id is absent.
- Mobile catalogue still duplicates markup for responsive layout (CSS-gated); acceptable pattern.

---

## Known Limitations

- No Playwright browser run in this remediation (JS forest fix covered by source assertion + prior FV dogfood hooks).
- Jump-to-arbitrary-stage via stage strip clicks not implemented — one-step Back + Restart cover the RF blocker.
- Soft-delete / abandon status unused; drafts are hard-deleted from Studio projection.

---

## Success Criteria

| Criterion | Status |
|-----------|--------|
| Complete workflow without becoming trapped | PASS |
| Recover from mistakes (Back / Restart) | PASS |
| Version assignment succeeds (`YYYY.N`) | PASS |
| Lifecycle delete/archive behave correctly | PASS |
| No duplicate subject entries on desktop | PASS |
| Ready to resume RF-001A | PASS |
