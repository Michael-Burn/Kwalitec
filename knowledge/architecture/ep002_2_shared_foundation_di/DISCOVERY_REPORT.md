# EP-002.2 — Architecture Discovery Report

**Milestone:** EP-002.2 — Shared Foundation DI & MissionOptimizer Decision  
**Date:** 2026-07-26  
**Nature:** Mandatory discovery before implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Scope of discovery

Reviewed:

| Artefact | Path / location |
|---|---|
| EP-001.5 Architectural Integration Review | `knowledge/architecture/ep001_5_architectural_integration_review/` |
| EP-002 Programme Brief | `knowledge/architecture/ep002_student_intelligence_surface/PROGRAMME_BRIEF.md` |
| EP-002.1 Completion Report | `knowledge/architecture/ep002_1_consumer_chain_observability/COMPLETION_REPORT.md` |
| Student Digital Twin Architecture | `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` |
| PlanningService | `app/services/planning_service.py` |
| ReadinessService | `app/services/readiness_service.py` |
| RecommendationService | `app/services/recommendation_service.py` |
| Foundation assembly | `app/infrastructure/adapters/digital_twin/foundation.py` |
| MissionOptimizer | `app/services/mission_optimizer.py` |
| Experience composition DI | `app/infrastructure/adapters/student_experience/composition.py` |
| Consumer-chain observability | `app/infrastructure/adapters/consumer_chain/` |

---

## 2. Current Foundation construction points

| Site | When | Shared? |
|---|---|---|
| `PlanningService._resolve_twin_foundation` | Twin ON + no `foundation=` | Builds fresh via `build_student_digital_twin_foundation` |
| `ReadinessService._resolve_twin_foundation` | Same | **Duplicate** of Planning helper |
| `RecommendationService._resolve_twin_foundation` | Same | **Duplicate** of Planning helper |
| `composition.py` (Experience) | Twin ON for Experience Authority / TwinPort | Shared facet assembler + Foundation for Experience only — **not** injected into Runtime A `build_*` |
| Tests / direct injection | Callers pass `foundation=` | Already supported on all three `build_*` APIs |

**O:** Three identical `_resolve_twin_foundation` static methods exist.  
**E:** Grep / side-by-side read of the three service modules.  
**C:** Resolve logic should be consolidated into one consumer-chain helper (DRY; not a new Twin).

---

## 3. Nested compose chain (runtime)

```
RecommendationService.build_study_insights
  ├─ resolve Foundation (once if not injected)
  ├─ foundation.assemble(user)          ← CLS #1
  ├─ PlanningService.build_daily_study_plan(foundation=…)
  │     └─ foundation.assemble(user)    ← CLS #2 (duplicate evidence collect)
  └─ ReadinessService.build_readiness_intelligence(foundation=…, daily_plan=…)
        └─ foundation.assemble(user)    ← CLS #3 (duplicate evidence collect)
```

When Readiness is the top-level caller with `include_planner=True`:

```
ReadinessService.build_readiness_intelligence
  ├─ resolve Foundation
  ├─ foundation.assemble(user)          ← CLS #1
  └─ PlanningService.build_daily_study_plan(foundation=…)
        └─ foundation.assemble(user)    ← CLS #2
```

**O:** Nested resolvers already pass the **same Foundation instance** when composing.  
**E:** `RecommendationService._resolve_daily_plan` / `_resolve_readiness_intelligence` and `ReadinessService._resolve_daily_plan` forward `foundation=`.  
**C:** Foundation *object* sharing is partially solved; the remaining cost is **repeated `assemble()`** (each recollects Runtime A evidence via `TwinFacetAssembler`).

**O:** `CanonicalLearnerState` is `@dataclass(frozen=True)` — safe to share by reference within one composition.  
**E:** `foundation.py` class definition.  
**C:** Injecting an already-assembled CLS into nested `build_*` calls is thread-safe and free of mutable shared state when the injection is request/composition-local.

---

## 4. Duplicate assembly paths

| Path | Status |
|---|---|
| Three `_resolve_twin_foundation` copies | Duplicate construction helpers |
| Nested `assemble()` without CLS injection | Duplicate evidence collection |
| Experience composition Foundation vs Runtime A resolve | Parallel construction for different consumers (acceptable; Experience Authority path) |
| MissionOptimizer → `build_daily_study_plan` | Would re-enter planner (orphan; no production callers) |

---

## 5. Existing dependency injection mechanisms

| Mechanism | Role |
|---|---|
| `foundation=` kwarg on `build_*` | Optional Foundation injection (EP-001.2–4) |
| `daily_plan=` / `readiness_intelligence=` | Skip nested resolve when payloads provided |
| `include_planner` / `include_readiness` | Opt out of nested composition |
| Experience `compose_student_experience` Twin DI | Shared Foundation for Authority port only |
| `observe_build_api` (EP-002.1) | Observability wrapper; preserves return values |

**Gap:** No `canonical_state=` (or equivalent) to skip re-assemble when Foundation is already shared.

---

## 6. MissionOptimizer production usage

| Check | Result |
|---|---|
| Definition | `MissionOptimizer.generate_balanced_mission` in `app/services/mission_optimizer.py` |
| Callers under `app/` | **None** (only definition site) |
| Dashboard / templates | **No** references |
| Tests | **No** dedicated tests |
| Twin ON path | Delegates to `PlanningService.build_daily_study_plan` then reshapes slots |
| Twin OFF path | AdaptiveLearning + CurriculumService balanced dict |
| Educational status | Accepted V1 technical debt (V1-TD-003); latent dual-authority risk if rewired |

**O:** EP-001.2 already absorbed balanced review/weak/progression slots into `build_daily_study_plan` (`today_missions`).  
**C:** MissionOptimizer is a **redundant projection layer**, not a missing production capability.

---

## 7. Observability available for before/after (EP-002.1)

| Signal | Use in EP-002.2 |
|---|---|
| Nested `build_*` invocation counts | Fan-out under Insight composition |
| `duration_ms` on completed events | Composition latency before/after |
| Twin / Authority flag snapshot | Matrix tests Twin×Authority |
| Dual-run helper | Unchanged; not required for DI |

**Gap:** No dedicated “Foundation assemble count” event yet — required for objective measurement of DI success.

---

## 8. Safety constraints confirmed

| Constraint | Status |
|---|---|
| No global Foundation singleton | Must preserve |
| No mutable shared CLS across requests | Must preserve — composition-local injection only |
| Thread safety | Immutable CLS + per-call DI |
| Collector recursion | Do not put Foundation inside `get_overall_readiness` |
| Ownership | Twin owns CLS; Planner/Readiness/Insight unchanged |
| No HTTP cutover / new flags / schema | Binding |

---

## 9. Discovery conclusions

| ID | Conclusion |
|---|---|
| D1 | Safe to share one Foundation **and** one assembled CLS per composition request |
| D2 | Primary optimisation is CLS re-assemble elimination, not only Foundation object reuse |
| D3 | Consolidate `_resolve_twin_foundation` into consumer-chain DI helper |
| D4 | Emit observational assemble-count telemetry for before/after evidence |
| D5 | MissionOptimizer should **not** be wired to production; deprecate / quarantine (decision record) |
| D6 | Do not start implementation of HTTP cutover or new engines |

**R:** Proceed to Dependency Review + Gap Analysis, then implement CLS injection + shared resolve + assemble telemetry + MissionOptimizer decision artefacts.
