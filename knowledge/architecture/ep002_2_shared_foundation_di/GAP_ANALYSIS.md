# EP-002.2 — Gap Analysis

**Milestone:** EP-002.2 — Shared Foundation DI & MissionOptimizer Decision  
**Date:** 2026-07-26  
**Based on:** [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md), [`DEPENDENCY_REVIEW.md`](DEPENDENCY_REVIEW.md)

Legend: **O** · **E** · **C** · **R**

---

## Gaps addressed by this milestone

| ID | Gap (source) | Closure plan |
|---|---|---|
| IF-07 / TD nested assemble | Nested Insight → Readiness → Planner re-assembles CLS | Inject `canonical_state=` through nested resolves; assemble once per composition |
| Duplicate `_resolve_twin_foundation` | Three identical helpers | Shared `resolve_enabled_twin_foundation` in `consumer_chain` |
| Assemble count invisible | EP-002.1 measures `build_*` only | Emit Foundation assemble / share-hit observability |
| IF-09 / TD-ARCH-03 | MissionOptimizer orphan | Formal decision: **deprecate & quarantine** — do not wire to production |
| WS0 MissionOptimizer fate | Programme brief | Decision record + module quarantine markers |

---

## Gaps explicitly deferred

| ID | Gap | Why deferred |
|---|---|---|
| IF-06 / HTTP cutover | No HTTP callers of `build_*` | EP-002.4+ |
| Authority soak | Production Authority OFF | EP-002.3 |
| Dual presentation | Insight vs EducationalExplainability | EP-002.8 |
| Mission surface cutover | `generate_today_mission` vs plan | EP-002.7 (uses this decision) |
| Experience composition → Runtime A share | Composition Foundation not injected into services | Optional later; kwargs already allow external inject |
| Hard-delete MissionOptimizer module | Latent code remains | Soft deprecate now; delete only after EP-002.7 proves no need |

---

## Measurement gaps → acceptance

| Metric | Before (expected) | After (target) |
|---|---|---|
| CLS assemble count under full Insight compose | **3** | **1** |
| Foundation construct count under full Insight compose | **1** (already) | **1** |
| Nested `build_*` observations | 3 (Insight+Readiness+Planner) | 3 (unchanged — desired for chain visibility) |
| Public `build_*` payloads | Baseline | Byte-equivalent for same inputs |
| Student HTTP | Unchanged | Unchanged |

---

## Residual risks after planned closure

| Risk | Mitigation |
|---|---|
| Callers forget to pass `canonical_state` | Nested resolvers inside services always forward when they hold state |
| Tests mock `_resolve_twin_foundation` on services | Keep thin service wrappers that delegate to shared helper so monkeypatches remain viable **or** update tests to patch shared helper |
| Premature MissionOptimizer deletion breaks obscure scripts | Soft deprecate; keep behaviour for direct calls |
| Over-caching CLS across users | Key by student_id; never store on process singleton |

---

## Implementation readiness

**C:** Discovery complete. Gaps IF-07 and IF-09 have clear, constrained closures.  
**R:** Begin implementation — Foundation DI + assemble telemetry + MissionOptimizer decision artefacts + tests + COMPLETION_REPORT.
