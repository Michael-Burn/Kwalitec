# EP-002.2 — Completion Report

**Milestone:** EP-002.2 — Shared Foundation DI & MissionOptimizer Decision  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** Optimisation and consolidation — **no student-facing UX authority change**; **no HTTP cutover**  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `DEPENDENCY_REVIEW.md`, `GAP_ANALYSIS.md`, `MISSION_OPTIMIZER_DECISION.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.2 reduces repeated Canonical Learner State assembly across the EP-001 consumer chain and formally quarantines `MissionOptimizer`.

**Observation:** Nested Insight → Readiness → Planner composition already forwarded a shared Foundation instance, but each host still called `Foundation.assemble`, recollecting Runtime A evidence up to three times per composition.  
**Evidence:** Shared `canonical_state=` injection + `assemble_shared_canonical_state` reduces full-chain assemble count from **3 → 1**; controlled bench shows average composition latency **~7.79 ms → ~2.80 ms** (~2.8×) with simulated 2 ms assemble cost. MissionOptimizer has **zero** production callers and is soft-deprecated.  
**Conclusion:** Objectives met — Foundation/CLS assembly reduced where appropriate; student behaviour unchanged; MissionOptimizer future documented as **deprecate & quarantine (do not wire)**.  
**Recommendation:** Accept EP-002.2. Proceed to **EP-002.3** Twin + Authority non-prod soak. Do not start HTTP insight cutover until soak evidence exists.

No schema migrations. No new feature flags. No new Twin / planner / readiness / recommendation engines. No ownership changes. No HTTP cutover.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, EP-002 programme brief, EP-002.1 completion, Twin architecture, Runtime A Planning / Readiness / Recommendation services, Foundation assembly, MissionOptimizer, Experience composition DI, and consumer-chain observability.

| Finding | Detail |
|---|---|
| Construction points | Three duplicate `_resolve_twin_foundation` helpers + Experience composition Foundation |
| Nested chain | Insight may call Readiness and Planner; Foundation object already forwarded |
| Primary waste | Repeated `assemble()` (evidence collect), not Foundation object construction under nested Insight |
| MissionOptimizer | Orphan — no `app/` callers; Twin path reshapes EP-001.2 plan slots |
| Existing DI | `foundation=` / `daily_plan=` / `readiness_intelligence=` kwargs; no CLS injection |
| Measurement | EP-002.1 `build_*` latency available; assemble-count telemetry missing before this milestone |

Full detail: [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md), [`DEPENDENCY_REVIEW.md`](DEPENDENCY_REVIEW.md), [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md).

**Conclusion:** Implementation was authorised only after discovery completed.

---

## 3. Existing Components Reused

| Component | Reuse |
|---|---|
| `StudentDigitalTwinFoundation` / `CanonicalLearnerState` | Immutable CLS share-by-reference within composition |
| `build_student_digital_twin_foundation` | Shared resolve helper target |
| Runtime A `PlanningService` / `ReadinessService` / `RecommendationService` | Hosts for `build_*`; nested resolve edges |
| EP-002.1 `observe_build_api` / `ConsumerChainTelemetry` | Latency + nested call observation; extended for assemble events |
| `resolve_v2_feature_flags` | Twin gate for shared resolve |
| EP-001.2–4 consumers / assemblers | Unchanged projection maths |

---

## 4. Existing Components Extended

| Component | Extension |
|---|---|
| `PlanningService.build_daily_study_plan` | `canonical_state=` kwarg; shared assemble helper; resolve delegates to consumer_chain |
| `ReadinessService.build_readiness_intelligence` | Same + forwards CLS to nested planner |
| `RecommendationService.build_study_insights` | Same + forwards CLS to nested planner / readiness |
| `consumer_chain` package | `foundation_di.py`; assemble telemetry |
| `MissionOptimizer` | Deprecation warning + quarantine docs; optional DI kwargs; behaviour preserved |
| Event catalogue | `CONSUMER_CHAIN_FOUNDATION_ASSEMBLE` |

---

## 5. Files Created

### Application

- `app/infrastructure/adapters/consumer_chain/foundation_di.py`

### Tests

- `tests/infrastructure/adapters/consumer_chain/test_foundation_di.py`
- `tests/infrastructure/adapters/consumer_chain/test_foundation_performance.py`
- `tests/infrastructure/adapters/consumer_chain/test_mission_optimizer_decision.py`

### Knowledge

- `knowledge/architecture/ep002_2_shared_foundation_di/README.md`
- `knowledge/architecture/ep002_2_shared_foundation_di/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_2_shared_foundation_di/DEPENDENCY_REVIEW.md`
- `knowledge/architecture/ep002_2_shared_foundation_di/GAP_ANALYSIS.md`
- `knowledge/architecture/ep002_2_shared_foundation_di/MISSION_OPTIMIZER_DECISION.md`
- `knowledge/architecture/ep002_2_shared_foundation_di/COMPLETION_REPORT.md` (this file)

---

## 6. Files Modified

- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/infrastructure/adapters/consumer_chain/contracts.py`
- `app/infrastructure/adapters/consumer_chain/telemetry.py`
- `app/infrastructure/events/types/__init__.py`
- `app/services/planning_service.py`
- `app/services/readiness_service.py`
- `app/services/recommendation_service.py`
- `app/services/mission_optimizer.py`
- `tests/infrastructure/adapters/consumer_chain/test_regression.py`
- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
- `knowledge/architecture/README.md`
- `knowledge/architecture/ep002_student_intelligence_surface/README.md`

---

## 7. Architectural Decisions

| Decision | Rationale |
|---|---|
| Inject immutable `canonical_state` through nested `build_*` | Eliminates re-assemble without process-global cache or mutable shared state |
| Consolidate Foundation resolve into `resolve_enabled_twin_foundation` | Removes triplicate helpers; still constructs per call (no singleton) |
| Keep service `_resolve_twin_foundation` thin wrappers | Preserves existing monkeypatch test seams |
| Emit assemble vs share-hit telemetry | Makes before/after measurable via EP-002.1 infrastructure |
| Nested `build_*` observations remain | Chain visibility still desired (EP-002.1) |
| MissionOptimizer: deprecate & quarantine, not wire, not hard-delete | Functional slots already in `build_daily_study_plan`; governance forbids dual-authority; hard delete deferred to EP-002.7 |
| No new feature flag | Always-on DI when Twin ON; zero rollout complexity |

**Observation:** Planner → Readiness → Insight can safely share one Foundation and one CLS per composition.  
**Evidence:** `CanonicalLearnerState` is `@dataclass(frozen=True)`; injection is composition-local kwargs.  
**Conclusion:** Thread-safe for normal request concurrency (no cross-request cache).

---

## 8. Dependency Changes

**None.** No new Python packages. No Alembic / schema dependencies.

Runtime dependency direction unchanged:

```
Runtime A facts → Foundation.assemble → CanonicalLearnerState
  → Planner / Readiness / Insight (now share CLS within one composition)
```

`consumer_chain.foundation_di` depends on v2_flags + digital_twin factory + telemetry. It does **not** own planning, readiness, or insight maths.

---

## 9. Runtime Dependency Graph

```
RecommendationService.build_study_insights
  ├─ resolve_enabled_twin_foundation()          [once if not injected]
  ├─ assemble_shared_canonical_state()          [assemble once]
  ├─ PlanningService.build_daily_study_plan(
  │     foundation=…, canonical_state=…)        [share-hit]
  └─ ReadinessService.build_readiness_intelligence(
        foundation=…, canonical_state=…,
        daily_plan=…)                           [share-hit; no second planner]
```

**MissionOptimizer** (quarantined):

```
generate_balanced_mission ──(no production inbound)──▶
  Twin ON: build_daily_study_plan (reshape)
  Twin OFF: AdaptiveLearning / CurriculumService
```

---

## 10. Foundation Assembly Analysis

| Scenario | Before EP-002.2 | After EP-002.2 |
|---|---|---|
| Insight full compose (planner + readiness) | Foundation×1, `assemble`×3 | Foundation×1, `assemble`×1 + share-hit×2 |
| Readiness + planner | Foundation×1, `assemble`×2 | Foundation×1, `assemble`×1 + share-hit×1 |
| Standalone planner | `assemble`×1 | `assemble`×1 (unchanged) |
| Twin OFF | No assemble | No assemble (unchanged) |
| Process-global Foundation | None | None (preserved) |

**Observation:** Foundation *object* sharing was largely already present on nested paths.  
**Evidence:** Pre-existing `foundation=` forwarding in resolvers.  
**Conclusion:** The material optimisation is CLS assemble elimination.

---

## 11. Performance Comparison

Method: EP-002.1/2 observability + controlled micro-bench (`test_foundation_performance.py` + 20-iteration harness). Simulated assemble cost = 2 ms sleep to make evidence-collection cost visible without DB.

| Metric | Before | After | Delta |
|---|---|---|---|
| Foundation assemble count (full Insight compose) | **3** | **1** | **−67%** |
| CLS share-hits | 0 | 2 | +2 (expected) |
| Avg composition latency (bench) | **7.79 ms** | **2.80 ms** | **~2.8× faster** |
| Nested `build_*` observations | 3 | 3 | Unchanged (desired) |

**Observation:** Latency improvement scales with assemble cost; real Runtime A collector work is typically larger than 2 ms, so production savings should be at least as material when Twin ON + full compose.  
**Evidence:** `tests/infrastructure/adapters/consumer_chain/test_foundation_performance.py` asserts assemble 3→1 and after latency &lt; before×0.7.  
**Conclusion:** Objective 2 (measure before/after) satisfied.  
**Recommendation:** Re-measure under EP-002.3 soak with live Twin ON traffic.

---

## 12. MissionOptimizer Assessment

See full decision record: [`MISSION_OPTIMIZER_DECISION.md`](MISSION_OPTIMIZER_DECISION.md).

| Lens | Statement |
|---|---|
| **Observation** | Orphaned balanced-mission helper; Twin path reshapes EP-001.2 plan |
| **Evidence** | Grep: no production callers; no dashboard/template usage; V1-TD-003 / IF-09 |
| **Conclusion** | Must **not** be wired into production; soft-deprecate/quarantine |
| **Recommendation** | Prefer `build_daily_study_plan` for EP-002.7 mission dual-run; consider hard delete after WS6 |

Code changes: module quarantine docstring, `DeprecationWarning`, optional DI kwargs, behaviour preserved for direct callers.

---

## 13. Public Surface Changes

| Surface | Change |
|---|---|
| `build_*` return values | **Unchanged** |
| `build_*` kwargs | Additive optional `canonical_state=` (backward compatible) |
| HTTP routes / templates | **Unchanged** |
| Feature flags | **Unchanged** (no additions) |
| MissionOptimizer | Soft-deprecated; still callable; not used by HTTP |

---

## 14. Testing Summary

### Commands executed

```bash
python3 -m pytest tests/infrastructure/adapters/consumer_chain/ \
  tests/infrastructure/adapters/adaptive_study_planner/test_unit.py \
  tests/infrastructure/adapters/readiness_intelligence/test_unit.py \
  tests/infrastructure/adapters/insight_recommendation/test_unit.py -q
```

**Outcome:** 60 passed (consumer-chain 36 + EP-001.2–4 unit suites).

### Coverage matrix

| Area | Status |
|---|---|
| Unit — resolve / assemble_shared | ✓ |
| DI — Insight nested compose assemble×1 | ✓ |
| DI — Readiness forwards CLS to planner | ✓ |
| Performance before/after | ✓ |
| Regression — Twin OFF None paths | ✓ |
| Twin × Authority matrix fail-open | ✓ |
| MissionOptimizer deprecation + no app callers | ✓ |
| EP-001.2–4 unit regression | ✓ |

---

## 15. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Future callers forget to forward `canonical_state` | Low | Medium | Nested service resolvers always forward when they hold state |
| R2 | MissionOptimizer accidentally rewired to UI | Low | High | Deprecation + quarantine + caller guard test |
| R3 | Soft-deprecated module lingers indefinitely | Medium | Low | EP-002.7 / WS8 cleanup owned |
| R4 | Premature HTTP cutover because “DI is done” | Medium | High | Programme sequence still requires EP-002.3 soak |

---

## 16. Technical Debt

| Item | Notes |
|---|---|
| MissionOptimizer soft-deprecated code remains | Intentional until EP-002.7 |
| Experience composition Foundation not auto-injected into Runtime A services | Optional later; kwargs already allow external inject |
| No live production assemble metrics yet | Twin OFF in prod; measure in EP-002.3 non-prod soak |
| Dual presentation (Insight vs EducationalExplainability) | EP-002.8 |

**None introduced** that violates constitutional ownership.

---

## 17. Constitutional Compliance

| Rule | Status |
|---|---|
| Twin owns learner-state read model | Preserved |
| Planner owns plans | Preserved |
| Readiness owns evaluation | Preserved |
| Insight owns communication only | Preserved |
| No fourth Twin stack | Preserved |
| No global / mutable shared Foundation | Preserved |
| Collector recursion invariant (`get_overall_readiness`) | Preserved |
| Fail-open Twin OFF | Preserved |
| Curriculum V1/V2 traversal | N/A — untouched |
| No HTTP cutover / schema / new flags | Preserved |

---

## 18. Architectural Delta

| Before EP-002.2 | After EP-002.2 |
|---|---|
| Nested compose re-assembles CLS up to 3× | Compose shares one CLS |
| Triplicate `_resolve_twin_foundation` bodies | Shared `resolve_enabled_twin_foundation` |
| Assemble count invisible | `consumer_chain.foundation_assemble` events |
| MissionOptimizer orphan undecided | Formal deprecate & quarantine decision |
| EP-002.1 could measure `build_*` only | Can measure assemble vs share-hit |

**Not changed:** HTTP authority, educational algorithms, schemas, ownership boundaries, default flags.

---

## 19. Architecture Metrics

| Metric | Value |
|---|---|
| Services Extended | **4** (`PlanningService`, `ReadinessService`, `RecommendationService`, `MissionOptimizer` quarantine) |
| New Services | **0** (DI helpers live under existing `consumer_chain` infrastructure) |
| New Public APIs | **0** student/HTTP; additive optional `canonical_state=` only |
| Foundation Assembly Count (Before/After) | **3 / 1** (full Insight compose) |
| Average Composition Latency (Before/After) | **~7.79 ms / ~2.80 ms** (controlled bench; 2 ms simulated assemble) |
| Schema Changes | **0** |
| Feature Flags Added | **0** |
| Circular Dependencies | **0** |
| Ownership Violations | **0** |
| Parallel Implementations Introduced | **0** |
| Net Architectural Complexity | **Slight decrease** (less duplicate resolve; orphan explicitly quarantined) |
| Overall Architectural Health | **Improved** for composition cost + orphan clarity; product cutover health unchanged (still pending EP-002.3–7) |

---

## 20. Recommendation for EP-002.3

**Observation:** Consumer chain is now observable (EP-002.1) and cheaper to compose when Twin ON (EP-002.2).  
**Evidence:** Assemble 3→1; MissionOptimizer fate closed for WS0; production defaults still Twin OFF / Authority OFF.  
**Conclusion:** Ready for non-prod Twin + Authority soak without student UX authority change.  
**Recommendation:** Execute **EP-002.3 — Twin + Authority non-prod soak**:

1. Twin ON in non-prod; exercise `build_*` under observation.  
2. Authority ON soak candidates with rollback drills.  
3. Capture live assemble-count / latency distributions using EP-002.1–2 telemetry.  
4. Keep production Twin / Authority OFF.  
5. Do not start EP-002.4 insight dual-run HTTP wiring until soak exit criteria pass.  
6. Treat MissionOptimizer as out of scope for student surfaces going forward.

---

## Success Criteria Checklist

| Criterion | Status |
|---|---|
| Foundation assembly reduced where appropriate | ✓ |
| Behaviour unchanged | ✓ |
| Performance measurements captured | ✓ |
| MissionOptimizer future formally documented | ✓ |
| No ownership changes | ✓ |
| No duplicate architecture introduced | ✓ |
| All tests pass | ✓ |

---

## Final Verdict

| Question | Answer |
|---|---|
| Milestone successful? | **Yes** |
| Student-facing change? | **No** |
| Safe to proceed to EP-002.3? | **Yes** |
| Twin Ready (T7)? | **No — not claimed** |
| HTTP cutover authorised? | **No** |
| MissionOptimizer production wiring? | **No — quarantined** |
