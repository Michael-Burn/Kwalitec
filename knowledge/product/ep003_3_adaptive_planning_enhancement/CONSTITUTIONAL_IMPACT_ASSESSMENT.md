# EP-003.3 — Constitutional Impact Assessment

**Programme:** EP-003.3 — Adaptive Planning Enhancement  
**Date:** 2026-07-26  
**Phase:** Pre-implementation  

---

## 1. Ownership map (baseline)

| Concern | Required owner | Must not |
|---|---|---|
| Daily plan / mission persistence | PlanningService | Presentation, Recommendation, Readiness |
| Readiness scores / drivers | ReadinessService | Planning must not recalculate |
| Recommendation ranking | RecommendationService | Planning must not re-rank |
| Presentation speech selection | RuntimeAPresentationAdapter | Must not invent plans |

## 2. Proposed change impact

| Change | Ownership risk | Mitigation |
|---|---|---|
| `planning_quality.py` schema attachment | Low — inside PlanningService | Called only from PlanningService |
| Consume `get_overall_readiness` | Low — labelling / workload note | Never call dashboard readiness; never recalculate |
| Consume recommendation titles | Medium — recursion via mission surface | Reentrancy depth guard; fail-open |
| Assembler recovery / minute balance | None — planner-owned maths | Twin signals only; no sibling services |
| Presentation schema pass-through | Low | Gate on `has_complete_plan_explanation_schema` |

## 3. STOP criteria review

Would this create a second educational brain? **No** — Planning remains sole plan authority; sibling outputs are labels only.

Would presentation start planning? **No** — pass-through only.

**STOP not triggered.** Proceed.

## 4. Feature flags

No new flags. Inherits `KWALITEC_DIGITAL_TWIN`, `KWALITEC_DAILY_PLAN_CUTOVER`, and existing dual-run behaviour.
