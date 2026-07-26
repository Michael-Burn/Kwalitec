# EP-002.4 — Completion Report

**Milestone:** EP-002.4 — Study Insights Dual-Run  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** First student-surface activation under observation — **no production cutover**; **no HTTP response / template student-visible change**; legacy recommendations remain authoritative  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `DUAL_RUN_DESIGN.md`, `GAP_ANALYSIS.md`, `ROLLBACK_PLAN.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.4 wires Twin-backed `build_study_insights` as a fail-open diagnostic dual-run beside Runtime A `RecommendationService.generate_recommendations` in approved non-production environments.

**Observation:** Before this milestone, EP-002.1 left an unwired fingerprint helper; students never exercised Twin insights beside legacy recommendations on the live recommendation path.  
**Evidence:** Dual-run side-car executes after legacy compute; student return value is the legacy list only; structured comparison telemetry + in-process health metrics record latency, limitation codes, confidence, categories, unavailable states, correlation IDs, and flags. Controlled bench: **50** dual-run requests, legacy success **100%**, Twin success **80%**, behavioural regressions **0**, ownership violations **0**. Production eligibility remains closed.  
**Conclusion:** Objectives met. Legacy remains sole student-facing authority. Operational evidence for EP-002.5 gated HTTP cutover **planning** now exists. Production Twin / Authority ON and HTTP cutover remain **not** authorised.  
**Recommendation:** Accept EP-002.4. Proceed to **EP-002.5** only after non-prod dual-run soak on real dashboard traffic and an explicit cutover checklist. Keep production Twin / Authority OFF.

No schema migrations. No new feature flags. No new Twin / planner / readiness / recommendation engines. No ownership changes. No HTTP cutover.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, EP-002 programme brief, EP-002.1–3 completion reports, `RecommendationService`, `generate_recommendations`, `build_study_insights`, dashboard/home routes, consumer-chain observability, and `v2_flags`.

| Finding | Detail |
|---|---|
| Authoritative path | `generate_recommendations` (dashboard + bridges) |
| Twin path | `build_study_insights` — not previously HTTP-wired |
| Inherited gate | Twin ON ∧ `APP_ENV` ∉ {production, prod} |
| Gap | Helper unwired; comparison fingerprint-only |
| New flag needed? | **No** |
| Shape divergence | Legacy `list[dict]` vs Insight guidance `dict` — fingerprint mismatch expected |

Full detail: [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md), [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md), [`DUAL_RUN_DESIGN.md`](DUAL_RUN_DESIGN.md).

**Conclusion:** Implementation authorised only after discovery — observational side-car under `consumer_chain`, not a redesign or cutover.

---

## 3. Dual-Run Design

Executed per [`DUAL_RUN_DESIGN.md`](DUAL_RUN_DESIGN.md):

```
generate_recommendations()
        │
        ├─► legacy list  ──► student HTTP / templates (unchanged)
        │
        └─► (eligible only) fail-open build_study_insights()
                → structured comparison → telemetry + dual-run health metrics
```

| Design choice | Rationale |
|---|---|
| Wire after legacy compute in `generate_recommendations` | Covers dashboard + bridges; no template edits |
| Request-scoped dedupe | Dashboard may call today + list APIs |
| Nested dual-run ContextVar guard | Ops helper / recursion safety |
| No new feature flag | Reuse Twin + non-prod eligibility |
| Fail-open Twin exceptions | Student path never breaks |

Rollback: [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) — kill switch = Twin OFF.

---

## 4. Comparison Methodology

| Field | Capture |
|---|---|
| Execution time | `legacy_latency_ms`, `twin_latency_ms` |
| Limitation codes | Twin `limitations_codes` |
| Confidence | `confidence_level` / `confidence_available` |
| Recommendation categories | Unique sorted legacy `category` values |
| Twin field presence | `todays_key_focus`, `recommended_next_action`, … |
| Unavailable responses | `legacy_unavailable`, `twin_unavailable` |
| Correlation IDs | `CorrelationContext` correlation / causation |
| Feature flags | `twin_enabled`, `authority_enabled` |
| Opaque fingerprints | Secondary; mismatch expected across shapes |

**Observation:** Comparisons are never exposed in UI and never influence ranking/selection.  
**Evidence:** `influences_student=False` on every emission; return path returns the pre-computed legacy list.  
**Conclusion:** Methodology meets milestone capture requirements without student leakage.  
**Recommendation:** EP-002.5 should add topical alignment scoring (topic_id / title heuristics) before cutover — out of scope here.

---

## 5. Comparison Results

**Observation:** Controlled dual-run bench exercised structured compare under Twin ON / non-prod.  
**Evidence:**

| Result | Value |
|---|---|
| Dual-run requests | **50** |
| Legacy success | **50 / 50** (100%) |
| Twin success (non-None, no exception) | **40 / 50** (80%) |
| Twin unavailable (`None`) | **8** |
| Twin exceptions (fail-open) | **2** |
| Fingerprint divergences | **50 / 50** (100% — expected shape mismatch) |
| Limitation codes observed | `sparse_evidence` × 13 |
| Behavioural regressions | **0** |
| Ownership violations | **0** |
| Dual-run readiness signal | `ready_for_ep002_5_planning` |

Unit / integration suites: dual-run, regression, comparison integrity, feature-flag matrix, rollback — **all passed** (`test_study_insights_dual_run.py` + prior consumer-chain observability).

**Conclusion:** Dual-run operates as designed; fingerprint divergence is not a defect.  
**Recommendation:** Treat divergence rate as a **shape** signal until EP-002.5 defines topical alignment metrics.

---

## 6. Legacy vs Twin Analysis

| Dimension | Legacy | Twin Study Insights |
|---|---|---|
| Authority this milestone | **Student-facing** | Diagnostic only |
| Shape | Category/priority recommendation rows | Guidance fields (focus / risk / next / why) |
| Unavailable | Empty list possible | `None` when Twin OFF / CLS unavailable |
| Honesty | Heuristic explainability on rows | Limitation codes when upstream sparse |
| Ownership | Runtime A RecommendationService | Insight communication over Twin/Planner/Readiness |

**Observation:** Dual-run does not attempt to merge or pick between narrators.  
**Evidence:** No template binding to Twin fields; no HTTP DTO change.  
**Conclusion:** Dual presentation debt (Insight vs EducationalExplainability) remains for WS7 after cutover — unchanged and intentional.  
**Recommendation:** Do not collapse narrators in EP-002.5; cut over one surface first.

---

## 7. Performance Summary

Controlled dual-run bench (injected Twin builders; not live Foundation collect cost):

| Metric | Value |
|---|---|
| Average legacy latency | **1.8 ms** (injected timing) |
| P95 legacy latency | **2.4 ms** |
| Average Twin latency | **~0.0 ms** (stub builder) |
| P95 Twin latency | **0.002 ms** |

**Observation:** Stub latencies understate live Foundation + nested planner/readiness cost.  
**Evidence:** EP-002.2 nested compose ~2.8 ms with shared CLS under simulated 2 ms assemble; EP-002.3 soak recommended live side-by-side measurement.  
**Conclusion:** No performance blocker for continued non-prod dual-run; measure live staging assemble cost next.  
**Recommendation:** EP-002.5 cutover gate should include P95 Twin budget vs legacy under real collectors.

---

## 8. Runtime Dependency Verification

```
HTTP / bridges (unchanged)
        │
        ▼
RecommendationService.generate_recommendations  ← student authority
        │
        ├── legacy heuristic path (unchanged maths)
        │
        └── EP-002.4 dual-run (eligible only)
                build_study_insights
                  → observe_build_api (EP-002.1)
                  → Foundation CLS share (EP-002.2)
                  → planner / readiness / insight assemblers
                compare → CONSUMER_CHAIN_DUAL_RUN + dual_run_health
```

**Observation:** Dependency direction unchanged from EP-001.5 / EP-002.1–3.  
**Evidence:** `consumer_chain` still does not own planning/readiness/insight maths; Insight still does not write Runtime A.  
**Conclusion:** Constitutional runtime dependency graph preserved.  
**Recommendation:** Keep dual-run inside RecommendationService until EP-002.5 introduces an explicit HTTP projection adapter.

---

## 9. Feature Flag Matrix

| Twin | Authority | `APP_ENV` | Dual-run? | Student response |
|---|---|---|---|---|
| OFF | OFF | any | No | Legacy only |
| OFF | ON (env) | any | No (Authority forced OFF) | Legacy only |
| ON | OFF | non-prod | **Yes** | Legacy only |
| ON | ON | non-prod | **Yes** | Legacy only |
| ON | * | production / prod | No | Legacy only |

**Evidence:** Parametrised eligibility tests + service-hook Twin OFF skip test.  
**Conclusion:** No new flags; production defaults remain fail-open / OFF.  
**Recommendation:** Do not add `ENABLE_STUDY_INSIGHTS_DUAL_RUN`; Twin OFF remains the kill switch.

---

## 10. Observability Findings

| Signal | Status |
|---|---|
| `CONSUMER_CHAIN_DUAL_RUN` enriched fields | Latency, codes, confidence, categories, unavailable, flags |
| Nested `observe_build_api` on Twin call | Still emits when Twin path runs |
| Correlation / causation on dual-run | Captured from `CorrelationContext` |
| In-process dual-run health metrics | Architecture Metrics source |
| Student UI exposure | **None** |

**Observation:** Engineers can now answer “did Twin run beside legacy, and what differed?” on the recommendation path in non-prod.  
**Evidence:** Telemetry unit tests + dual-run suite.  
**Conclusion:** TD-OPS gap for Study Insights dual-run on the recommendation path is closed for this milestone.  
**Recommendation:** Add staging dashboard scrape of dual-run logs before EP-002.5.

---

## 11. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Accidental HTTP cutover in a follow-on PR | Medium | High | Explicit EP-002.5 scope; templates untouched here |
| R2 | Twin assemble cost on every recommendation call in staging | Medium | Medium | Request dedupe; Twin OFF kill switch |
| R3 | Operators misread fingerprint divergence as failure | Medium | Low | This report + design doc clarify expected mismatch |
| R4 | EI dashboard path skips legacy (no dual-run) | Low | Medium | Documented; dual-run covers `generate_recommendations` callers |
| R5 | MissionOptimizer rewiring during dual-run | Low | High | Remains quarantined (EP-002.2) |

---

## 12. Technical Debt

| ID | Debt | Disposition |
|---|---|---|
| TD-DR-01 | Fingerprint divergence not topical alignment | Accept for EP-002.4; address in EP-002.5 prep |
| TD-DR-02 | Educational Intelligence card path may skip dual-run | Accept; first activation is legacy recommendation pipeline |
| TD-DR-03 | In-process metrics are process-local (not durable) | Accept; logs are durable ops channel |
| TD-ARCH / presentation dual path | Insight vs EducationalExplainability | Deferred to WS7 after cutover |

**Conclusion:** No new unjustified architectural debt; named items are sequenced.  
**Recommendation:** Burn TD-DR-01 before production cutover.

---

## 13. Constitutional Compliance

| Invariant | Status |
|---|---|
| Twin owns learner-state read model | Preserved |
| Planner owns plans | Preserved |
| Readiness owns evaluation | Preserved |
| Insight owns communication only | Preserved |
| Runtime A writes unchanged | Preserved |
| Curriculum V1/V2 traversal untouched | N/A — no curriculum diffs |
| Fail-open rollback | Twin OFF kills dual-run |
| No fourth Twin stack | Preserved |
| No new recommendation engine | Preserved |
| Production Twin / Authority OFF defaults | Preserved |

**Observation:** Dual-run is a side channel (`influences_student=False`).  
**Evidence:** Tests assert legacy list identity; Twin exceptions swallowed.  
**Conclusion:** Constitutionally compliant.  
**Recommendation:** EP-002.5 must keep fail-open fallback to legacy on Twin errors.

---

## 14. Architectural Delta

| Before EP-002.4 | After EP-002.4 |
|---|---|
| Dual-run helper ops-only, unwired | Live side-car on `generate_recommendations` |
| Fingerprint-only compare | Structured comparison fields |
| No dual-run health aggregator | `StudyInsightsDualRunHealthMetrics` |
| No student-path Twin exercise on recommendations | Non-prod Twin ON exercises insight beside legacy |
| HTTP / templates | **Unchanged** |
| Feature flags | **Unchanged** (no additions) |
| Schema | **Unchanged** |

---

## 15. Architecture Metrics

| Metric | Value |
|---|---|
| Dual-Run Requests | **50** (controlled bench) |
| Legacy Success Rate | **1.0** |
| Twin Success Rate | **0.8** |
| Divergence Rate | **1.0** (opaque fingerprint; expected) |
| Limitation-Code Frequency | `sparse_evidence` × 13 |
| Average Legacy Latency | **1.8 ms** (bench timing) |
| Average Twin Latency | **~0.0 ms** (stub) |
| P95 Legacy Latency | **2.4 ms** |
| P95 Twin Latency | **0.002 ms** |
| Behavioural Regressions | **0** |
| Ownership Violations | **0** |
| Overall Dual-Run Readiness | **ready_for_ep002_5_planning** |

**Observation:** Metrics are from controlled dual-run harness plus automated tests, not production traffic (production ineligible).  
**Evidence:** `StudyInsightsDualRunHealthMetrics.snapshot()` + pytest suite.  
**Conclusion:** Dual-run readiness for **planning** EP-002.5 is green; not a production cutover go.  
**Recommendation:** Recompute metrics on staging with live Foundation before EP-002.5 implementation.

---

## 16. Recommendation for EP-002.5

**Observation:** EP-002.4 proves side-by-side execution and structured observation without student impact.  
**Evidence:** Success criteria below; soak (EP-002.3) + dual-run (this milestone) complete.  
**Conclusion:** Safe to **plan** Study Insights gated HTTP cutover with legacy fallback.  
**Recommendation:**

1. Implement EP-002.5 gated cutover on dashboard/home only (cohort / non-prod first).  
2. Keep legacy as fail-open fallback on Twin `None` / exception.  
3. Add topical alignment compare (not fingerprint-only) as cutover gate.  
4. Do **not** enable production Twin / Authority until cutover checklist + rollback drill.  
5. Leave readiness / mission dual-run to EP-002.6–7.  
6. Do not un-quarantine MissionOptimizer.

---

## Files Created

### Application

- `app/infrastructure/adapters/consumer_chain/dual_run_health.py`

### Tests

- `tests/infrastructure/adapters/consumer_chain/test_study_insights_dual_run.py`

### Knowledge

- `knowledge/architecture/ep002_4_study_insights_dual_run/README.md`
- `knowledge/architecture/ep002_4_study_insights_dual_run/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_4_study_insights_dual_run/DUAL_RUN_DESIGN.md`
- `knowledge/architecture/ep002_4_study_insights_dual_run/GAP_ANALYSIS.md`
- `knowledge/architecture/ep002_4_study_insights_dual_run/ROLLBACK_PLAN.md`
- `knowledge/architecture/ep002_4_study_insights_dual_run/COMPLETION_REPORT.md` (this file)

---

## Files Modified

- `app/infrastructure/adapters/consumer_chain/dual_run.py`
- `app/infrastructure/adapters/consumer_chain/telemetry.py`
- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/services/recommendation_service.py`
- `knowledge/architecture/ep002_student_intelligence_surface/README.md`
- `knowledge/architecture/README.md`
- `.env.example`

---

## Tests Executed

```bash
python3 -m pytest \
  tests/infrastructure/adapters/consumer_chain/test_study_insights_dual_run.py \
  tests/infrastructure/adapters/consumer_chain/test_observability.py \
  tests/infrastructure/adapters/consumer_chain/test_regression.py -v
```

**Outcome:** All passed (40 tests in the combined dual-run + observability + regression set for the dual-run focused run; dual-run file alone 19 passed).

```bash
python3 -m ruff check \
  app/infrastructure/adapters/consumer_chain/dual_run.py \
  app/infrastructure/adapters/consumer_chain/dual_run_health.py \
  app/infrastructure/adapters/consumer_chain/telemetry.py \
  app/infrastructure/adapters/consumer_chain/__init__.py \
  tests/infrastructure/adapters/consumer_chain/test_study_insights_dual_run.py
```

**Outcome:** All checks passed.

---

## Migration Impact

**None.** No Alembic revisions. No schema changes.

---

## Architecture Compliance

Layering preserved: blueprints unchanged; dual-run lives in infrastructure `consumer_chain` + thin service hook; Insight / Planner / Readiness ownership unchanged. Curriculum V1/V2 traversal not touched. Application HTTP responses and student-visible templates unchanged.

---

## Success Criteria Checklist

| Criterion | Status |
|---|---|
| Legacy recommendations remain authoritative | ✓ |
| Twin insights execute successfully in dual-run | ✓ |
| Structured comparison data collected | ✓ |
| No behavioural regressions | ✓ |
| HTTP responses unchanged | ✓ |
| Production defaults remain OFF | ✓ |

---

## Final Verdict

| Question | Answer |
|---|---|
| Accept EP-002.4? | **Yes** |
| Student-visible behaviour changed? | **No** |
| Production cutover authorised? | **No** |
| Safe to proceed to EP-002.5 planning? | **Yes** |
| Twin Ready (T7)? | **No claim** |
