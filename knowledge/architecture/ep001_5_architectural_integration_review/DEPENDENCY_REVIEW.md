# EP-001.5 — Dependency Review

**Milestone:** EP-001.5  
**Review area:** Dependency Integrity  
**Date:** 2026-07-26

Legend: **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Intended dependency direction

```
Curriculum Engine (syllabus SoT)
        ↓
Runtime A (transactional write SoT)
        ↓
MS-004 collectors / TwinRuntimeEvidence
        ↓
EP-001.1 CanonicalLearnerState (Foundation)
        ↓
   ┌────┴────┬────────────┐
   ↓         ↓            ↓
EP-001.2   EP-001.3     (direct)
Planner    Readiness    Insight inputs
   ↓         ↓            ↓
   └────┬────┘            │
        ↓                 │
     EP-001.4 Insight ←───┘
        ↓
   Experience / HTTP (future cutover; not yet wired)
```

**O:** EP-001 packages are projection/assembly consumers; Runtime A services host public `build_*` APIs.  
**C:** Intended direction matches constitutional layering (facts → learner state → planning/evaluation → communication).

---

## 2. Compile-time import edges

| From | Imports | Must not import | Status |
|---|---|---|---|
| `digital_twin/foundation.py` | assembler, builders, contracts, evidence, provenance, snapshot_builder | planner, readiness, insight, services | **Pass** |
| `digital_twin/authority.py` | foundation | services / EP-001.2–4 | **Pass** |
| `adaptive_study_planner/*` | `digital_twin.contracts`, `foundation.CanonicalLearnerState` | services | **Pass** |
| `readiness_intelligence/*` | `digital_twin.contracts`, foundation | services | **Pass** |
| `insight_recommendation/*` | `digital_twin.contracts`, foundation | services | **Pass** |
| `planning_service.py` | lazy: adaptive_study_planner, digital_twin, v2_flags | — | **Pass** |
| `readiness_service.py` | lazy: readiness_intelligence, digital_twin, planning_service | — | **Pass** |
| `recommendation_service.py` | lazy: insight_recommendation, readiness_service, planning_service, digital_twin | — | **Pass** |
| `adaptive_engine/twin_input.py` | adaptive_engine.contracts, digital_twin.contracts | Foundation, EP-001.2–4 | **Pass** |

**E:** Grep over `app/infrastructure/adapters/digital_twin/` finds zero references to `adaptive_study_planner`, `readiness_intelligence`, or `insight_recommendation`.  
**E:** EP-001.2–4 adapter packages import Foundation/contracts only; service imports are lazy inside `build_*` methods.  
**C:** No circular compile-time dependencies among EP-001 packages.

---

## 3. Runtime one-way chain (not a cycle)

**O:** Foundation assembly uses `TwinFacetAssembler.collect_evidence` → shared `ReadinessCollector` → `ReadinessService.get_overall_readiness` (legacy DB path).

**E:**
- `foundation.py` → `facet_assembler.collect_evidence`
- `adaptive_engine/collectors.py` `ReadinessCollector` calls `get_overall_readiness` / `get_curriculum_coverage` / `get_review_backlog`
- `CanonicalReadinessConsumer` docstring forbids calling ReadinessService getters (“avoids collector recursion”)
- `get_overall_readiness` does not call `build_readiness_intelligence`

**C:** This is a **one-way runtime chain**, not an authority cycle. EP-001.3 correctly preserves the legacy getter as the collector fact path.

**R:** Keep `get_overall_readiness` free of Foundation calls indefinitely (or until collectors are refactored off ReadinessService). Document as a hard invariant.

---

## 4. Bypass inventory

| Potential bypass | Present? | Notes |
|---|---|---|
| HTTP invents mastery/streaks without Twin | **Yes (legacy)** | Dashboard/analytics call ORM-backed services directly — intentional fail-open until cutover |
| Planner invents learner state | **No** | Consumer projects CanonicalLearnerState only |
| Readiness invents mastery | **No** | Consumer projects Twin; scores from available mastery payload |
| Insight invents readiness/plan | **No** | Partial guidance + limitation codes when planner/readiness missing |
| Twin imports Experience cutover adapters | **No** | Authority port wraps Foundation; Twin core does not import Experience routes |
| Adaptive synthesises Twin | **No** | `TwinInputAdapter` consumes snapshots only (MS-004 T4) |

**C:** No unconstitutional bypasses inside the EP-001 chain. Legacy HTTP paths are **compatibility bypasses**, not dependency violations of the new chain.

---

## 5. Service-layer DI note

**O:** `PlanningService` / `ReadinessService` / `RecommendationService` `_resolve_twin_foundation()` constructs a fresh Foundation when Twin ON and no injection, rather than reusing composition DI.

**E:** Composition wires shared Foundation for Experience Authority only (`student_experience/composition.py`).

**C:** Dependency direction remains correct; operational cost may duplicate collector work per `build_*` call.

**R:** Future consolidation — inject composition Foundation into Runtime A services (operational debt TD-OPS-01).

---

## 6. Verdict

| Criterion | Result |
|---|---|
| Dependency direction intact | **Yes** |
| Circular imports | **None found** |
| Reverse Twin ownership | **None found** |
| Collector recursion risk mitigated | **Yes** |
| Residual bypasses | Legacy HTTP only (by design) |
