# EP-003.3 — Discovery Report

**Programme:** EP-003.3 — Adaptive Planning Enhancement  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| Product Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Final Test; honest, explainable daily guidance |
| P-001.1 KSI Framework | `knowledge/product/p001_1_ksi_baseline/` | K1 baseline **62** (Partial); planning usefulness gap |
| P-001.2 Explainability Standard | `knowledge/product/p001_2_explainability_standard/` | Mandatory Explanation Schema for planning decisions |
| P-001.3 Recommendation Quality | `knowledge/product/p001_3_recommendation_quality_standard/` | Decision Framework ladder for recommendation-aware order |
| EP-003.1 outputs | `knowledge/product/ep003_1_recommendation_engine_enhancement/` | Quality-contract pattern to mirror |
| EP-003.2 outputs | `knowledge/product/ep003_2_readiness_intelligence_enhancement/` | Readiness quality + presentation pass-through pattern |
| EP-002.9 baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Ownership: Planning plans; presentation does not |
| PlanningService | `app/services/planning_service.py` | Runtime A planning authority |
| Adaptive Study Planner | `app/infrastructure/adapters/adaptive_study_planner/` | EP-001.2 Twin-backed daily plan |
| RuntimeAPresentationAdapter | `app/presentation/intelligence_surface/adapter.py` | Presentation selection only |
| Subsystem doc | `knowledge/subsystems/study-planning.md` | Planning responsibilities |

---

## 2. Current Runtime A behaviour (pre-EP-003.3)

1. **Twin adaptive plan** (`build_daily_study_plan`): review / weak / progression slots from Canonical Learner State; light-load heuristic; informal explainability dict — no P-001.2 schema.
2. **Legacy mission** (`generate_today_mission`): Learning Mode follows first incomplete topic; Revision rotates kinds — weak interruption deferred.
3. **HTTP facade** (`get_dashboard_mission_surface`): EP-002.7 cutover or legacy; no mandatory explanation schema.
4. **Sibling consumption:** Recommendation and Readiness consume planner outputs; Planning did **not** consume readiness/recommendation outputs.
5. **Missed sessions:** `mission_missed_count` projected into planner inputs but unused in assembly.
6. **Presentation:** Twin mission narrative shallowly re-spoke slot reasons — compensating for missing service schema (same defect EP-003.1/003.2 fixed).

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| K1 = 62 (Partial) | Prefer clear rationale, balanced priorities, completable days |
| Twin planner already exists | Enhance quality + recovery; do not invent a second planner |
| No planning quality module | Add `planning_quality.py` inside PlanningService |
| Circular dependency risk | Consume `get_overall_readiness` only; recommendation titles with reentrancy guard |
| Presentation re-narrates | Move schema into PlanningService; adapter pass-through when complete |
| Ownership settled (EP-002.9) | Enhance inside PlanningService only |

---

## 4. Recommended implementation shape

1. Enhance `DailyStudyPlanAssembler` for recovery, balanced minute allocation, and Decision Framework–aligned slot order.
2. Add `app/services/planning_quality.py` owned and called only by `PlanningService`.
3. Apply mandatory explanation schema, readiness/recommendation alignment labels, and workload notes on daily plans and dashboard mission surfaces.
4. Keep `RuntimeAPresentationAdapter` presentation-only: pass through when plan schema complete.
5. Preserve fail-open dual-run / cutover flags; no new production flag.

---

## 5. Out of scope (explicit)

- Reopening EP-001.1–4 ownership or Twin Ready claims.
- Deleting legacy `generate_today_mission` or promoting MissionOptimizer.
- Changing week-plan long-horizon distribution maths.
- Recalculating readiness scores or ranking recommendations inside Planning.
- Production HTTP cutover declaration changes.
