# EP-002.5 — Completion Report

**Milestone:** EP-002.5 — Study Insights Gated HTTP Cutover  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** First controlled student-facing activation of Twin-backed Study Insights on dashboard/home — **legacy fail-open fallback retained**; **no production-wide activation**  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `CUTOVER_DESIGN.md`, `ELIGIBILITY_MATRIX.md`, `ROLLBACK_PLAN.md`, `RISK_ASSESSMENT.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.5 introduces a gated HTTP cutover so eligible non-production dashboard/home requests may receive a Twin `build_study_insights` projection, while every other case continues to receive legacy `generate_recommendations`.

**Observation:** Before this milestone, EP-002.4 exercised Twin insights only as a diagnostic dual-run; students never received Study Insights over HTTP.  
**Evidence:** Dashboard routes now call `RecommendationService.get_dashboard_recommendations` / `get_dashboard_today_recommendation`; cutover requires Twin ON ∧ `KWALITEC_STUDY_INSIGHTS_CUTOVER` ON ∧ non-production env ∧ successful Twin response ∧ no blocking limitation. Controlled bench: **50** eligible requests, Twin served **35 / 50** (70%), legacy fallback **30%**, alignment rate **100%** among comparable pairs, behavioural regressions **0**, ownership violations **0**. Production remains ineligible by design.  
**Conclusion:** Objectives met. Eligible cohorts can receive Study Insights; fail-open legacy behaviour is validated; alignment reporting is operational. Production Twin / Authority / Cutover ON remain **not** authorised.  
**Recommendation:** Accept EP-002.5. Proceed to **EP-002.6** readiness dual-run → gated cutover only after staging soak on real dashboard traffic. Keep production Cutover / Twin / Authority OFF.

No schema migrations. No new recommendation engines. No ownership changes. No new Twin implementation.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, EP-002 programme brief, EP-002.1–4 completion reports, `RecommendationService`, dashboard/home routes, dual-run, consumer-chain telemetry, and `v2_flags`.

| Finding | Detail |
|---|---|
| Authoritative legacy path | `generate_recommendations` (bridges / Founder unchanged) |
| Twin path | `build_study_insights` — previously dual-run only |
| HTTP surface | Dashboard `index()` when EI recommendation card absent |
| Gap | No student-facing Twin projection; fingerprint divergence unusable as quality gate |
| New flag needed? | **Yes** — `KWALITEC_STUDY_INSIGHTS_CUTOVER` (default OFF; requires Twin) |
| Insertion point | Dashboard service methods + `consumer_chain/cutover.py` (not inside legacy `generate_recommendations`) |

Full detail: [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md), [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md), [`ELIGIBILITY_MATRIX.md`](ELIGIBILITY_MATRIX.md), [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md), [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md).

**Conclusion:** Implementation authorised only after discovery — gated cutover under `consumer_chain` + thin dashboard service API, not a redesign.

---

## 3. Cutover Design

Executed per [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md):

```
Dashboard / Home
        │
        ▼
get_dashboard_recommendations()
        │
        ├─ ineligible ──► generate_recommendations() ──► legacy
        │
        └─ eligible
                ├─ legacy (fail-open ready + alignment baseline)
                ├─ build_study_insights()
                ├─ None / exception / blocking ──► legacy
                └─ success ──► project → list[dict] (influences_student=True)
```

| Design choice | Rationale |
|---|---|
| New dashboard APIs (not mutate `generate_recommendations`) | Protects bridges / Founder blast radius |
| Project Twin → legacy card shape | Template unchanged; EI mutual exclusion preserved |
| Skip EducationalExplainability enrich for Twin rows | Insight already owns communication |
| Skip dual-run when cutover eligible | Avoid double Twin assemble |
| Request-scoped cache | Today + list share one Twin decision |

Rollback: [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) — kill switches = Cutover OFF and/or Twin OFF.

---

## 4. Eligibility Matrix

| Twin | Cutover | `APP_ENV` | Attempt? | Student response |
|---|---|---|---|---|
| OFF | * | any | No | Legacy |
| ON | OFF | non-prod | No | Legacy (+ dual-run diagnostic) |
| ON | ON | non-prod | **Yes** | Twin projection if success + non-blocking; else legacy |
| ON | ON | production / prod | No | Legacy |

Post-attempt serving also requires non-`None` Twin dict, no exception, and no blocking limitation (`twin_foundation_flag_off`, `canonical_learner_state_unavailable`, `invalid_student_id`, or both actionable fields absent).

Authority is **recorded**, not required for this Runtime A Foundation path.

---

## 5. HTTP Routing Changes

| Location | Change |
|---|---|
| `app/dashboard/routes.py` `index()` | Calls `get_dashboard_today_recommendation` / `get_dashboard_recommendations`; skips explainability enrich when `source_authority == "study_insights"` |
| `RecommendationService` | Adds dashboard cutover APIs; dual-run hook skips when cutover eligible/active |
| Templates | **Unchanged** (projection preserves `title` / `priority` / `category` / explainability fields) |
| Experience Recommendation Bridge | **Unchanged** (still `generate_recommendations`) |

**Observation:** Only the Runtime A dashboard recommendation surface is cut over.  
**Evidence:** Route + service diffs; bridge regression test.  
**Conclusion:** Surface scope matches programme WS4 first cutover.  
**Recommendation:** Do not broaden to readiness / mission in this milestone.

---

## 6. Fallback Behaviour

Fallback to legacy occurs for:

| Trigger | Reason code |
|---|---|
| Twin OFF | `twin_off` |
| Cutover flag OFF | `cutover_flag_off` |
| Production env | `production_env` |
| Config/flag resolve failure | `configuration_failure` |
| Twin `None` | `twin_unavailable` |
| Twin exception | `twin_exception` |
| Blocking limitation | `blocking_limitation` |
| Empty projection | `projection_empty` |

**Observation:** Student always receives a list (legacy or projected).  
**Evidence:** Fail-open unit tests for Twin OFF / flag OFF / production / None / exception / blocking.  
**Conclusion:** Constitutional fail-open preserved.  
**Recommendation:** Keep kill-switch order Cutover OFF → Twin OFF for ops drills.

---

## 7. Alignment Analysis

Lightweight semantic alignment (not fingerprint equality):

| Status | Meaning |
|---|---|
| `aligned` | Twin `topic_id` / field titles overlap legacy title/reason text |
| `mismatched` | Twin served but no topical overlap |
| `twin_unavailable` | Twin not attempted / None / exception / flag gates |
| `limitation_fallback` | Blocking limitation or empty projection |

**Observation:** Fingerprint divergence remains expected across shapes and is **not** used as a cutover quality gate (closes EP-002.4 TD-DR-01 for cutover decisions).  
**Evidence:** Alignment unit tests + controlled bench alignment rate **1.0** among aligned/mismatched pairs.  
**Conclusion:** Alignment reporting is operational for Architecture Metrics.  
**Recommendation:** Track mismatched rate on staging live traffic before production consideration.

---

## 8. Runtime Dependency Verification

```
HTTP dashboard (cutover-aware)
        │
        ▼
RecommendationService.get_dashboard_recommendations
        │
        ├── (ineligible) generate_recommendations  ← legacy authority
        │         └── EP-002.4 dual-run when Twin ON non-prod + Cutover OFF
        │
        └── (eligible) consumer_chain.cutover
                ├── legacy generate_recommendations (baseline + fallback)
                ├── build_study_insights
                │     → observe_build_api (EP-002.1)
                │     → Foundation CLS share (EP-002.2)
                │     → planner / readiness / insight assemblers
                ├── project + align
                └── CONSUMER_CHAIN_CUTOVER + cutover_health
```

**Observation:** Dependency direction unchanged from EP-001.5 / EP-002.1–4.  
**Evidence:** `consumer_chain` still does not own planning/readiness/insight maths; Insight still does not write Runtime A.  
**Conclusion:** Constitutional runtime dependency graph preserved.  
**Recommendation:** Keep bridge callers on `generate_recommendations` until an explicit bridge cutover milestone exists.

---

## 9. Feature Flag Matrix

| Twin | Cutover | Authority | `APP_ENV` | Dual-run? | Cutover attempt? | Student response |
|---|---|---|---|---|---|---|
| OFF | * | * | any | No | No | Legacy |
| ON | OFF | * | non-prod | Yes | No | Legacy |
| ON | ON | OFF | non-prod | No (skipped) | **Yes** | Twin or legacy fail-open |
| ON | ON | ON | non-prod | No (skipped) | **Yes** | Twin or legacy fail-open |
| ON | ON | * | production | No | No | Legacy |

New env: `KWALITEC_STUDY_INSIGHTS_CUTOVER` → `ENABLE_STUDY_INSIGHTS_CUTOVER` (requires Twin; default OFF).

**Evidence:** Parametrised eligibility + flag unit tests.  
**Conclusion:** Production defaults remain fail-open / OFF.  
**Recommendation:** Staging may enable Cutover only with Twin ON and rollback drill completed.

---

## 10. Operational Metrics

| Signal | Status |
|---|---|
| `CONSUMER_CHAIN_CUTOVER` | Emitted with attempted/served/fallback/alignment/latencies/flags |
| Nested `observe_build_api` on Twin call | Still emits when Twin path runs |
| In-process cutover health metrics | Architecture Metrics source |
| Dual-run coexistence | Skipped when cutover eligible |
| Student UI exposure of ops fields | **None** (card content only) |

**Observation:** Engineers can answer “did cutover attempt, serve Twin, or fall back — and why?” on dashboard traffic in non-prod.  
**Evidence:** Telemetry integration event tests + health snapshot.  
**Conclusion:** Operational evidence channel for gated activation is live.  
**Recommendation:** Scrape staging cutover logs before EP-002.6.

---

## 11. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Accidental production cutover | Low | High | Env hard-exclude + flags default OFF |
| R2 | Bridge inherits Twin payload | Low | High | Cutover only on dashboard APIs |
| R3 | Twin latency on dashboard | Medium | Medium | P95 metrics; kill switch |
| R4 | Blocking rules too strict | Medium | Low | Metrics for limitation fallback rate |
| R5 | Explainability overwrite | Low | Medium | Skip enrich for Twin rows |
| R6 | Scope creep to readiness/mission | Medium | High | Explicit out-of-scope |

---

## 12. Technical Debt

| ID | Debt | Disposition |
|---|---|---|
| TD-CO-01 | In-process cutover metrics are process-local | Accept; logs are durable ops channel |
| TD-CO-02 | EI dashboard card path still separate narrator | Accept; WS7 after multi-surface cutover |
| TD-CO-03 | Alignment is heuristic (topic_id / title tokens) | Accept for gated non-prod; refine with live curriculum ids |
| TD-DR-02 (inherited) | EI card may skip legacy recommendation path | Unchanged; mutual exclusion intentional |

**Conclusion:** No new unjustified architectural debt; named items are sequenced.  
**Recommendation:** Burn TD-CO-03 with staging samples before production consideration.

---

## 13. Constitutional Compliance

| Invariant | Status |
|---|---|
| Twin owns learner-state read model | Preserved |
| Planner owns plans | Preserved |
| Readiness owns evaluation | Preserved |
| Insight owns communication only | Preserved (projection maps Insight fields) |
| Runtime A writes unchanged | Preserved |
| Curriculum V1/V2 traversal untouched | N/A — no curriculum diffs |
| Fail-open rollback | Cutover OFF / Twin OFF / production env |
| No fourth Twin stack | Preserved |
| No new recommendation engine | Preserved |
| Production Twin / Authority / Cutover OFF defaults | Preserved |
| No production-wide activation | Preserved |

**Observation:** Cutover is explicit and gated (`influences_student=True` only when Twin projection served).  
**Evidence:** Tests assert legacy identity for bridges; Twin exceptions swallowed.  
**Conclusion:** Constitutionally compliant.  
**Recommendation:** EP-002.6 must keep the same fail-open pattern for readiness.

---

## 14. Architectural Delta

| Before EP-002.5 | After EP-002.5 |
|---|---|
| Dual-run diagnostic only | Gated HTTP cutover on dashboard/home |
| No cutover flag | `KWALITEC_STUDY_INSIGHTS_CUTOVER` (default OFF) |
| No topical alignment | Semantic alignment report + metrics |
| No blocking-limitation serve gate | Defined blocking set + fail-open |
| Dashboard → `generate_*` only | Dashboard → cutover-aware APIs |
| Bridges | Unchanged (legacy) |
| Schema | **Unchanged** |
| Production defaults | **Unchanged** (OFF) |

---

## 15. Architecture Metrics

Controlled cutover bench (injected Twin builders; 50 eligible + ineligible probe):

| Metric | Value |
|---|---|
| Eligible Requests | **50** |
| Legacy Fallback Rate | **0.30** (15 / 50) |
| Twin Success Rate | **0.70** (35 / 50 served) |
| Alignment Rate | **1.0** (35 aligned / 35 comparable) |
| Limitation-Driven Fallback Rate | **0.12** (6 / 50) |
| Average Legacy Latency | **~0.0 ms** (stub) |
| Average Twin Latency | **0.879 ms** (1 ms sleep stub) |
| P95 Legacy Latency | **0.001 ms** |
| P95 Twin Latency | **1.261 ms** |
| Behavioural Regressions | **0** |
| Ownership Violations | **0** |
| Overall Cutover Readiness | **ready_for_ep002_6_planning** |

**Observation:** Metrics are from controlled harness + automated tests, not production traffic (production ineligible). Stub latencies understate live Foundation assemble cost.  
**Evidence:** `StudyInsightsCutoverHealthMetrics.snapshot()` + pytest suite (105 passed in cutover + dual-run + flags set).  
**Conclusion:** Cutover readiness for **planning** EP-002.6 is green; not a production cutover go.  
**Recommendation:** Recompute metrics on staging with live Foundation before any production checklist.

---

## 16. Recommendation for EP-002.6

**Observation:** EP-002.5 proves gated Study Insights HTTP activation with fail-open legacy on dashboard/home.  
**Evidence:** Success criteria below; dual-run (EP-002.4) + soak (EP-002.3) + this cutover complete.  
**Conclusion:** Safe to **plan** Readiness intelligence dual-run → gated cutover next.  
**Recommendation:**

1. Implement EP-002.6 readiness dual-run then gated cutover on analytics/home readiness surfaces.  
2. Keep legacy readiness getters for collectors (no recursion).  
3. Do **not** enable production Twin / Authority / Cutover until staging evidence + rollback drill.  
4. Leave mission/plan cutover to EP-002.7.  
5. Do not un-quarantine MissionOptimizer.  
6. Do not collapse Insight vs EducationalExplainability until WS7.

---

## Files Created

### Application

- `app/infrastructure/adapters/consumer_chain/cutover.py`
- `app/infrastructure/adapters/consumer_chain/cutover_health.py`

### Tests

- `tests/infrastructure/adapters/consumer_chain/test_study_insights_cutover.py`

### Knowledge

- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/README.md`
- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/CUTOVER_DESIGN.md`
- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/ELIGIBILITY_MATRIX.md`
- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/ROLLBACK_PLAN.md`
- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/RISK_ASSESSMENT.md`
- `knowledge/architecture/ep002_5_study_insights_gated_http_cutover/COMPLETION_REPORT.md` (this file)

---

## Files Modified

- `app/application/config/v2_flags.py`
- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/infrastructure/adapters/consumer_chain/contracts.py`
- `app/infrastructure/adapters/consumer_chain/telemetry.py`
- `app/infrastructure/events/types/__init__.py`
- `app/services/recommendation_service.py`
- `app/dashboard/routes.py`
- `tests/application/config/test_v2_flags.py`
- `.env.example`
- `knowledge/architecture/ep002_student_intelligence_surface/README.md`
- `knowledge/architecture/README.md`

---

## Tests Executed

```bash
python3 -m pytest \
  tests/infrastructure/adapters/consumer_chain/test_study_insights_cutover.py \
  tests/infrastructure/adapters/consumer_chain/test_study_insights_dual_run.py \
  tests/application/config/test_v2_flags.py -v
```

**Outcome:** All passed (**105** tests).

```bash
python3 -m ruff check \
  app/infrastructure/adapters/consumer_chain/cutover.py \
  app/infrastructure/adapters/consumer_chain/cutover_health.py \
  app/infrastructure/adapters/consumer_chain/telemetry.py \
  app/infrastructure/adapters/consumer_chain/__init__.py \
  app/infrastructure/adapters/consumer_chain/contracts.py \
  app/application/config/v2_flags.py \
  app/dashboard/routes.py \
  tests/infrastructure/adapters/consumer_chain/test_study_insights_cutover.py
```

**Outcome:** All checks passed.

---

## Migration Impact

**None.** No Alembic revisions. No schema changes.

---

## Architecture Compliance

Layering preserved: blueprints call services; cutover lives in infrastructure `consumer_chain` + thin service APIs; Insight / Planner / Readiness ownership unchanged. Curriculum V1/V2 traversal not touched. Bridges remain on legacy recommendations. Production defaults OFF.

---

## Success Criteria Checklist

| Criterion | Status |
|---|---|
| Eligible requests receive Study Insights | ✓ |
| Ineligible requests receive legacy recommendations | ✓ |
| Fail-open behaviour validated | ✓ |
| Alignment reporting operational | ✓ |
| No ownership violations | ✓ |
| No behavioural regressions outside eligible cohorts | ✓ |
| No production-wide activation | ✓ |

---

## Final Verdict

| Question | Answer |
|---|---|
| Accept EP-002.5? | **Yes** |
| Student-visible behaviour changed? | **Yes — gated non-prod dashboard only** |
| Production cutover authorised? | **No** |
| Safe to proceed to EP-002.6 planning? | **Yes** |
| Twin Ready (T7)? | **No claim** |
