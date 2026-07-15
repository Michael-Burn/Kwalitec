# IA-002 — Study Plan State Synchronization

**Capability ID:** IA-002  
**Programme:** Internal Alpha Stabilization  
**Priority:** P1  
**Status:** Implemented — pending Architecture Review  
**Date:** 2026-07-15

---

## Problem

Internal Alpha testers reported that changing the active study plan left student
surfaces stale until a manual browser refresh.

Observed behaviour:

- Switch CS1 → CM1
- Dashboard / today's mission continued to show the previous subject
- Refresh corrected the display

Students should never need to refresh, log out, or navigate specially after a
plan switch.

---

## Root Cause

Active study plan state is stored only in the database (`StudyPlan.active`).
There is no Flask-session or client-side active-plan cache — that part was
already a single source of truth.

Propagation stopped at plan activation:

1. `StudyPlanService.set_active_plan` flipped `active` flags and committed.
2. It did **not** synchronize derived student state (today's mission for the
   newly active plan).
3. The HTTP handler redirected to the study-plan **list**, so the next rendered
   page did not recompose dashboard, recommendation card, or mission launch.
4. Browser refresh of an open dashboard/mission tab re-ran those compose paths
   and *appeared* to "fix" state — masking a missing post-activation sync
   and a wrong redirect target, not a separate UI state store.

IA-001 made missions plan-scoped (`study_plan_id`). IA-002 ensures activation
itself drives immediate synchronization onto student-facing surfaces.

---

## Architecture

```
POST /study-plan/<id>/set-active
        ↓
StudyPlanService.set_active_plan   ← StudyPlan.active = single SoT
        ↓
StudyPlanService.synchronize_student_surfaces
        ↓
PlanningService.generate_today_mission (active plan only)
        ↓
redirect → dashboard.index
        ↓
Dashboard / mission / recommendation compose from get_user_active_plan
```

Invariants:

- `StudyPlan.active` remains the only authoritative active-plan flag.
- No secondary session / localStorage / client duplicate of active plan.
- Derived work (today's mission) is regenerated or rebound for the new plan on
  activate.
- Successful activate returns the dashboard so all student cards re-read the
  same active plan in one response cycle.

---

## Solution

| Change | Purpose |
|--------|---------|
| `StudyPlanService.synchronize_student_surfaces` | Generate/bind today's mission for the active plan |
| `set_active_plan` calls synchronize after commit | Switch immediately updates derived state |
| `set_active_plan` route redirects to `dashboard.index` | Next page is a full fresh compose (no manual navigation) |
| Flash names the activated exam | Confirm which plan is now authoritative |

No Educational Intelligence, Twin, ranking, or dashboard redesign changes.

---

## Regression Tests

`tests/test_ia002_study_plan_state_synchronization.py`

| Test | Scenario |
|------|----------|
| `test_single_plan_unchanged` | 1 — single plan |
| `test_switch_cs1_to_cm1_updates_immediately` | 2 — switch + immediate dashboard/mission |
| `test_back_and_forth_preserves_plan_missions` | 3 — CS1 ↔ CM1 restores original CS1 mission |
| `test_reload_keeps_synchronized_state` | 4 — reload consistency |
| `test_mission_completion_after_switch_stays_on_plan` | 5 — complete after switch |
| `test_synchronize_student_surfaces_binds_mission` | Service sync helper |
| `test_activate_does_not_cache_foreign_plan_mission` | Negative CS1 ↛ CM1 |

---

## Known Limitations

1. Open tabs other than the activate response still hold previously rendered
   HTML until navigated or reloaded — HTTP cannot push into other tabs. The
   activate redirect path itself no longer requires refresh.
2. EI recommendation card content still depends on Twin availability for the
   active curriculum; IA-002 only guarantees plan context is current.
3. Legacy non-EI recommendation lists may still mix user-global weak/coverage
   metrics (see IA-001 limitations).
