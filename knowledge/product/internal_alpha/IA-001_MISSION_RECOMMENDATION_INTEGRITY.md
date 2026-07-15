# IA-001 — Mission Recommendation Integrity

**Capability ID:** IA-001  
**Programme:** Internal Alpha Stabilization  
**Priority:** P0 (Release Blocking)  
**Status:** Implemented — pending Architecture Review  
**Date:** 2026-07-15

---

## Problem

Internal Alpha testers observed that Kwalitec's recommendation surfaces disagreed with the mission students launched.

Examples:

- Dashboard showed Topic 4.2 while Today's Mission launched Topic 2.6
- Dashboard recommended CM1 while Start Today's Session opened CS1 work

Students could not trust the recommendation system. Recommendation integrity was therefore release blocking.

---

## Root Cause

Investigation traced the pipeline from study-plan selection through mission launch. Two defects combined:

### 1. Missions were not bound to the active study plan (primary)

ORM missions were keyed only by `user_id` + `mission_date`. There was no `study_plan_id`.

Consequences:

- Switching the active study plan left yesterday's-plan mission as "today's"
- `PlanningService.generate_today_mission` returned that stale row as idempotent
- `MissionService.get_today_mission` had no plan filter
- Dashboard labels / curriculum summary / EI recommendation followed the **new** active plan while `/missions` served the **old** mission

### 2. Dual display authority (secondary)

The dashboard "Today's Mission" card and mission hero preferred `curriculum_summary.current_topic_code` / `next_topic_code` (the study-plan syllabus pointer) over `today_mission.title` (the actual generated work). Labels and tasks could diverge even without a plan switch.

### 3. Cross-curriculum topic selection (contributing)

`PlanningService._select_topic_for_today` priorities 1–2 (due review / weak topics) queried all of a user's progress. A weak CS1 topic could win while the active plan was CM1. Priority order was unchanged; only the curriculum scope was wrong.

No Educational Intelligence ranking, Twin, or MissionIntelligence redesign was required for this capability.

---

## Architecture

Integrity authority for the product mission path:

```
StudyPlan.active (DB)
        ↓
StudyPlanService.get_user_active_plan
        ↓
PlanningService.generate_today_mission  ── creates / returns Mission(study_plan_id=…)
        ↓
MissionService.get_today_mission(study_plan_id=…)
        ↓
Dashboard card + /missions launch  ── render today_mission.title
```

Invariants after IA-001:

1. Every auto-generated mission stores `study_plan_id`.
2. Generate and retrieve are scoped to the active study plan.
3. A mission belonging to another study plan is never returned as today's mission.
4. UI "Today's Mission" copy comes from the mission row, not the syllabus pointer alone.
5. Weak/review selection for mission generation is filtered to the active plan's `curriculum_id`.

Layering preserved: blueprints → services → models. No route-owned recommendation math was introduced. Curriculum V1/V2 traversal remains via `CurriculumService`.

---

## Solution

| Change | Purpose |
|--------|---------|
| Alembic `202607150001` — nullable `missions.study_plan_id` + index | Persist plan binding |
| `Mission.study_plan_id` + `StudyPlan.missions` | Model relationship |
| `MissionService.create_mission(..., study_plan_id=)` | Write binding |
| `MissionService.get_today_mission(..., study_plan_id=)` | Read binding; default to active plan |
| `PlanningService.generate_today_mission` plan-scoped idempotency | Stop cross-plan reuse |
| Legacy orphan adoption for unfinished unbound rows | Soft migration for pre-IA-001 data |
| Scope weak/review picks to active curriculum | Prevent CS1↔CM1 topic theft |
| Dashboard + mission templates use `today_mission.title` | Single display authority |
| Mission index calls `generate_today_mission` | Launch path regenerates for new active plan |

Algorithms, ranking priorities (review → weak → next incomplete), Educational Orchestrator, Twin, and Founder Intelligence were not redesigned.

---

## Regression Tests

`tests/test_ia001_mission_recommendation_integrity.py`

| Test | Acceptance mapping |
|------|--------------------|
| `test_single_study_plan_recommendation_matches_mission` | Scenario 1 |
| `test_multiple_plans_switch_updates_mission` | Scenario 2 |
| `test_cs1_recommendation_never_returns_cm1_mission` | Negative (CS1 ↛ CM1) |
| `test_complete_mission_then_recommendation_stays_on_plan` | Scenario 3 |
| `test_reload_keeps_plan_scoped_mission` | Scenario 4 |
| `test_weak_topic_from_other_curriculum_cannot_win` | Cross-curriculum guard |
| `test_dashboard_and_mission_routes_agree` | Dashboard ↔ launch consistency |
| `test_legacy_orphan_mission_is_bound_not_cross_plan_leaked` | Soft migration |

---

## Known Limitations

1. **EI dual path (Stage A residual):** With Internal Alpha flags, the Educational Intelligence recommendation card can still describe Twin/Decision packaging while product persistence remains `PlanningService` → ORM Mission (`ENABLE_EI_MISSIONS=False`). IA-001 makes the ORM mission path plan-consistent; it does not merge EI and legacy mission engines.
2. **Nullable historical rows:** Completed unbound missions are left as historical; unfinished orphans are adopted onto the active plan on next generate.
3. **Legacy RecommendationService weak/coverage lists** remain user-global for non-EI dashboards. Progression labels were already active-plan scoped. Full legacy-list scoping is out of IA-001 scope.
4. **Subject placeholder** remains the shared `"Study Plan"` subject; distinction is via `study_plan_id`, not `subject_id`.

---

## Future Considerations

- Persist Decision → MissionIntelligence as the product mission authority (retire dual path).
- Optionally require non-null `study_plan_id` after a data backfill window.
- Scope legacy `RecommendationService` review/weak lists to the active curriculum for full advisory consistency when EI is off.
- Surface `study_plan_id` on mission APIs if mobile/clients consume missions directly.
