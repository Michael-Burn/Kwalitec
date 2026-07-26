# EP-004.3 — Discovery Report

**Programme:** EP-004.3 — Adaptive Planning Personalisation  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| Product Vision / Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Transparent, evidence-based planning; Final Test |
| Architecture Constitution | `docs/ARCHITECTURE_CONSTITUTION.md`, `.cursor/rules/00-CONSTITUTION.md` | Layering; no second educational brain |
| Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Evidence ≠ advice; plan coherence |
| EP-002.9 ownership baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Runtime A planning ownership |
| P-001.2 Explainability Standard | `knowledge/product/p001_2_explainability_standard/` | Mandatory plan schema |
| EP-003.3 Adaptive Planning | `knowledge/product/ep003_3_adaptive_planning_enhancement/` | Quality contract + recovery/workload |
| EP-004.1 Personal Learning Profile | `knowledge/product/ep004_1_personal_learning_profile/` | Evidence Port; confidence; unsupported |
| EP-004.2 Recommendation Personalisation | `knowledge/product/ep004_2_adaptive_recommendation_personalisation/` | Bounded closed-loop pattern to mirror |
| PlanningService | `app/services/planning_service.py`, `planning_quality.py` | Sole Runtime A planning authority |
| Adaptive study planner | `app/infrastructure/adapters/adaptive_study_planner/` | Slot order + minute allocation |
| RuntimeAPresentationAdapter | `app/presentation/intelligence_surface/adapter.py` | Presentation-only pass-through |

---

## 2. Current behaviour (pre-EP-004.3)

1. EP-003.3 attaches P-001.2 schema, readiness-informed workload notes, recovery after misses, and Decision Framework–aligned slot order.
2. EP-004.1 Port exists; `PlanningService.consume_personal_learning_profile` refreshed the profile after plan build but **discarded** the return value.
3. No profile attribute changed session duration, pacing, recovery emphasis, revision timing, or equivalent topic selection.
4. EP-004.2 closed the recommendation loop; planning remained the residual K4 gap called out in EP-004.1 residual analysis.
5. Presentation already pass-throughs schema-complete plans without re-planning.

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| Profile is ready as evidence, not as authority | Consume via Port inside PlanningService / quality path only |
| Educational slot order must remain primary | Personalisation = pacing / minutes / equivalent repair topics — never reorder review→repair→progression |
| Accept/dismiss is tip preference | Must not drive planning (Recommendation authority) |
| Thin / unsupported attributes are common | Confidence gates + graceful degrade required |
| Presentation must not personalise | Attach explanations at PlanningService boundary |
| Assembler already owns recovery mode from misses | Profile adjusts emphasis within that authorised structure |

---

## 4. Recommended implementation shape

1. Add `planning_personalisation.py` owned/called only via PlanningService quality path.
2. Resolve profile in `build_daily_study_plan` / `get_dashboard_mission_surface`; pass consumer view into quality contract.
3. Apply bounded rules **after** EP-003.3 schema attachment; abort if educational order would be violated.
4. Emit `personalisation_applied`, `personalisation_factors`, and student-safe evidence lines.
5. Keep `RuntimeAPresentationAdapter` pass-through; no profile inspection in presentation.
6. Preserve fail-open and `ENABLE_PERSONAL_LEARNING_PROFILE` default OFF.

---

## 5. Out of scope (explicit)

- Readiness personalisation loops (separate programme).
- Promoting plan slots from recommendation accept/dismiss.
- Inventing preferred study windows.
- Durable cross-process profile store.
- Changing curriculum sequence / Learning Mode topic selection maths.
- Twin Ready or production cutover changes.
