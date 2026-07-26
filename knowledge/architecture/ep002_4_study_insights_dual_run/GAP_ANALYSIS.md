# EP-002.4 — Gap Analysis

**Milestone:** EP-002.4 — Study Insights Dual-Run  
**Date:** 2026-07-26  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Purpose

Map programme / milestone objectives against inherited capability from EP-002.1–3 and name the deltas this milestone must close.

---

## 2. Objective coverage

| Objective | Pre-EP-002.4 state | Gap | EP-002.4 close |
|---|---|---|---|
| Execute `build_study_insights` alongside legacy recommendations | Helper exists; **not** invoked from `generate_recommendations` / HTTP | Live side-car missing | Wire fail-open dual-run after legacy compute |
| Preserve legacy as authoritative student response | True by default (Twin not HTTP-wired) | Risk of accidental merge if poorly wired | Return legacy only; no template/HTTP changes |
| Capture structured comparisons | Fingerprints only | Missing latency, codes, confidence, categories, unavailable, correlation, flags | Enrich comparison + telemetry |
| Operational evidence for future HTTP cutover | Soak proves Twin operable; no side-by-side legacy vs insight on recommendation path | No dual-run request metrics for Study Insights | Dual-run metrics aggregator + completion report |
| No production cutover / no new engines / no schema | Enforced | — | Preserve |
| No new flags unless needed | Eligibility gate exists | Temptation to add `ENABLE_STUDY_INSIGHTS_DUAL_RUN` | **Do not add** — reuse Twin + non-prod |

---

## 3. Inherited assets (keep)

| Asset | Milestone | Role |
|---|---|---|
| `is_dual_run_diagnostics_eligible` | EP-002.1 | Gate |
| `fingerprint_payload` / `compare_legacy_vs_build` | EP-002.1 | Opaque secondary signal |
| `observe_build_api` | EP-002.1 | Twin invocation observation |
| Shared Foundation CLS DI | EP-002.2 | Cheaper nested compose when Twin runs |
| Soak rollback / matrix evidence | EP-002.3 | Non-prod Twin/Authority operable |

---

## 4. Gaps detailed

### G1 — Unwired dual-run

**O:** `diagnostic_compare_study_insights` docstring: “Not wired to HTTP.”  
**E:** Grep — no dashboard / `generate_recommendations` callers of dual-run helpers.  
**C:** Students never exercise Twin insight beside legacy on the recommendation path.  
**R:** Hook into `RecommendationService.generate_recommendations`.

### G2 — Thin comparison

**O:** `emit_dual_run` records fingerprints + match boolean.  
**E:** Milestone requires execution time, limitation codes, confidence, categories, unavailable, correlation IDs, flags.  
**C:** Fingerprints alone are insufficient for EP-002.5 cutover judgement.  
**R:** Extend comparison record and telemetry fields.

### G3 — Dashboard double invocation

**O:** Home may call today + list APIs.  
**E:** `dashboard/routes.py`.  
**C:** Naïve per-call dual-run doubles Twin cost.  
**R:** Request-scoped dedupe.

### G4 — Metrics for architecture review

**O:** EP-002.3 has soak health; dual-run has no equivalent aggregator.  
**C:** Completion report Architecture Metrics need in-process evidence.  
**R:** Add dual-run health metrics (observational).

### G5 — Explicit non-gaps

| Non-gap | Rationale |
|---|---|
| New recommendation engine | Forbidden; Insight already exists |
| Schema / Alembic | Forbidden |
| New feature flag | Eligibility already expressible |
| HTTP cutover | Owned by EP-002.5 |
| MissionOptimizer | Quarantined (EP-002.2); out of scope |

---

## 5. Test gaps to close

| Required suite | Pre-state | Close with |
|---|---|---|
| Dual-run tests | Fingerprint unit only | Live side-car + structured fields |
| Regression | `build_*` / Twin OFF None | Legacy list identity with dual-run ON |
| Comparison integrity | Match boolean only | Codes / categories / flags / unavailable |
| Feature flag matrix | Eligibility unit tests | Twin×Authority×env matrix on service path |
| Rollback validation | Soak rollback | Dual-run stops when Twin OFF / prod env |

---

## 6. Gap analysis conclusions

**Observation:** EP-002.1–3 delivered observability substrate and soak; Study Insights dual-run remains unwired and under-instrumented.  
**Evidence:** Code inspection of `consumer_chain/dual_run.py`, dashboard routes, EP-002.1–3 reports.  
**Conclusion:** Gaps G1–G4 are in-scope for EP-002.4; G5 items must stay closed.  
**Recommendation:** Implement per [`DUAL_RUN_DESIGN.md`](DUAL_RUN_DESIGN.md); do not expand into cutover.
