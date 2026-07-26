# EP-002.6 — Completion Report

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** Dual-run diagnostics + first controlled student-facing activation of Twin-backed Readiness Intelligence on dashboard/analytics — **legacy fail-open fallback retained**; **no production-wide activation**  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `CUTOVER_DESIGN.md`, `ELIGIBILITY_MATRIX.md`, `ROLLBACK_PLAN.md`, `STUDENT_IMPACT_ASSESSMENT.md`, `RISK_ASSESSMENT.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.6 introduces Readiness Intelligence onto Runtime A dashboard and analytics readiness surfaces using the same constitutional activation pattern proven for Study Insights (EP-002.4/5): observe beside legacy → dual-run → gated HTTP cutover with fail-open fallback.

**Observation:** Before this milestone, `build_readiness_intelligence` existed (EP-001.3) with observability and soak, but students never received readiness intelligence over HTTP; dashboard/analytics called legacy getters only.  
**Evidence:** Dashboard and analytics now call `ReadinessService.get_dashboard_readiness_surface`; cutover requires Twin ON ∧ `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` ON ∧ non-production env ∧ successful Twin response ∧ no blocking limitation. Controlled bench: **50** eligible requests, Twin served **38 / 50** (76%), legacy fallback **24%**, alignment rate **92.1%** among comparable pairs, behavioural regressions **0**, ownership violations **0**. Collectors still call pure `get_overall_readiness`. Production remains ineligible by design.  
**Conclusion:** Objectives met. Eligible cohorts can receive Readiness Intelligence; fail-open legacy behaviour is validated; alignment reporting is operational; behaviour outside eligible cohorts is unchanged. Production Twin / Authority / Cutover ON remain **not** authorised.  
**Recommendation:** Accept EP-002.6. Proceed to **EP-002.7** daily plan / mission dual-run → gated cutover only after staging soak on real dashboard/analytics traffic. Keep production Cutover / Twin / Authority OFF.

No schema migrations. No new readiness engines. No ownership changes. No Twin redesign. No collector recursion.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, EP-002 programme brief, EP-002.1–5 completion reports, `ReadinessService`, dashboard/analytics readiness surfaces, consumer-chain telemetry, Study Insights cutover pattern, and `v2_flags`.

| Finding | Detail |
|---|---|
| Authoritative legacy path | `get_overall_readiness` + weak/strong topic getters (collectors unchanged) |
| Twin path | `build_readiness_intelligence` — previously observability/soak only |
| HTTP surfaces | `/dashboard` and `/analytics` readiness score + topic lists |
| Gap | No dual-run; no student-facing Twin projection; fingerprint divergence expected |
| New flag needed? | **Yes** — `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` (default OFF; requires Twin) |
| Insertion point | `get_dashboard_readiness_surface` + `consumer_chain/readiness_*.py` (not inside legacy getters) |
| Binding risk | Collector recursion if intelligence wraps `get_overall_readiness` — mitigated by facade-only design |

Full detail: [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md), [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md), [`ELIGIBILITY_MATRIX.md`](ELIGIBILITY_MATRIX.md), [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md), [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md), [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md).

**Conclusion:** Implementation authorised only after discovery — dual-run + gated cutover under `consumer_chain` + thin readiness surface API, not a redesign.

---

## 3. Student Impact Assessment

| Cohort | Student-visible impact |
|---|---|
| Production | **None** — production always ineligible |
| Non-prod Twin OFF | **None** |
| Non-prod Twin ON + Cutover OFF | **None visible** (dual-run diagnostic only) |
| Non-prod Twin ON + Cutover ON + success | Readiness score / weak-strong lists may reflect Twin intelligence |
| Eligible but Twin failure / blocking | **None vs legacy** — fail-open |

Surfaces changed: `/dashboard` and `/analytics` readiness hero + topic highlights only. Review backlog, streaks, syllabus `calculate_readiness`, Experience `/student` TwinPort, and Education OS readiness are out of scope.

**Observation:** Blast radius is bounded to two Runtime A readiness surfaces under explicit non-prod gates.  
**Evidence:** [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md); route wiring diffs; collector regression test.  
**Conclusion:** Student impact matches programme WS5 intent.  
**Recommendation:** Keep production OFF; use staging soak before any broader cohort discussion.

---

## 4. Cutover Design

Executed per [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md):

```
Dashboard / Analytics
        │
        ▼
get_dashboard_readiness_surface()
        │
        ├─ ineligible ──► legacy surface ──► dual-run side-car (Twin ON non-prod)
        │
        └─ eligible
                ├─ legacy (fail-open ready + alignment baseline)
                ├─ build_readiness_intelligence()
                ├─ None / exception / blocking ──► legacy
                └─ success ──► project → surface DTO (influences_student=True)
```

| Design choice | Rationale |
|---|---|
| New surface facade (not mutate `get_overall_readiness`) | Protects collectors / Adaptive TwinInput |
| Project Twin → legacy template shape | Templates unchanged |
| Skip topic-row enrich for Twin areas | Twin already owns area communication |
| Skip dual-run when cutover eligible | Avoid double Twin assemble |
| Request-scoped cache | Dashboard + analytics share one Twin decision per request |
| Semantic readiness alignment | Score / confidence / limitations / area overlap — not fingerprints |

Rollback: [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) — kill switches = Cutover OFF and/or Twin OFF.

---

## 5. Eligibility Matrix

| Twin | Cutover | `APP_ENV` | Dual-run? | Cutover attempt? | Student response |
|---|---|---|---|---|---|
| OFF | * | any | No | No | Legacy |
| ON | OFF | non-prod | **Yes** | No | Legacy |
| ON | ON | non-prod | No (skipped) | **Yes** | Twin projection if success + non-blocking; else legacy |
| ON | ON | production / prod | No | No | Legacy |

Post-attempt serving also requires non-`None` Twin dict, no exception, no blocking limitation (`twin_foundation_flag_off`, `canonical_learner_state_unavailable`, `invalid_student_id`, unavailable availability, or missing `readiness_score`).

Authority is **recorded**, not required for this Runtime A Foundation path.

Binding detail: [`ELIGIBILITY_MATRIX.md`](ELIGIBILITY_MATRIX.md).

---

## 6. HTTP Routing Changes

| Location | Change |
|---|---|
| `app/dashboard/routes.py` `index()` | Calls `get_dashboard_readiness_surface`; skips topic enrich when `source_authority == "readiness_intelligence"` |
| `app/analytics/routes.py` `index()` | Same surface facade (weak/strong limit 5) |
| `ReadinessService` | Adds `get_dashboard_readiness_surface`; dual-run hook when cutover ineligible |
| Templates | **Unchanged** (projection preserves score / topic row fields) |
| Collectors / settings / exam timeline | **Unchanged** (still legacy getters) |
| Experience `/student` | **Unchanged** |

**Observation:** Only Runtime A dashboard/analytics readiness score + topic lists are cut over.  
**Evidence:** Route + service diffs; collector regression test asserting no `get_dashboard_readiness_surface` in Adaptive collectors.  
**Conclusion:** Surface scope matches programme WS5.  
**Recommendation:** Do not broaden to mission plan or Experience TwinPort in this milestone (EP-002.7 owns plan/mission).

---

## 7. Fallback Behaviour

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
| Empty / unscored projection | `projection_empty` |

**Observation:** Student always receives a readiness surface (legacy or projected).  
**Evidence:** Fail-open unit tests for Twin OFF / flag OFF / production / None / exception / blocking.  
**Conclusion:** Constitutional fail-open preserved.  
**Recommendation:** Keep kill-switch order Cutover OFF → Twin OFF for ops drills.

---

## 8. Alignment Analysis

Semantic readiness alignment (not fingerprint equality):

| Status | Meaning |
|---|---|
| `aligned` | Score agreement (Δ ≤ 10) ∧ area topic overlap (or both empty) |
| `mismatched` | Twin served but score/area disagreement |
| `twin_unavailable` | Twin not attempted / None / exception / flag gates |
| `limitation_fallback` | Blocking limitation or empty projection |

Captured dimensions:

| Dimension | Capture |
|---|---|
| Readiness agreement | Absolute score delta ≤ 10 |
| Confidence agreement | Twin `confidence_level` present when score served |
| Limitation agreement | Blocking codes map to `limitation_fallback` |
| Unavailable responses | Twin `None` / exception / pre-gate |
| Fallback reasons | Enumerated reason codes on every decision |

**Observation:** Fingerprint divergence remains expected across shapes and is **not** used as a cutover quality gate.  
**Evidence:** Alignment unit tests + controlled bench alignment rate **0.921** among aligned/mismatched pairs.  
**Conclusion:** Alignment reporting is operational for Architecture Metrics.  
**Recommendation:** Track mismatched rate on staging live traffic before production consideration.

---

## 9. Runtime Dependency Verification

```
HTTP dashboard / analytics (cutover-aware)
        │
        ▼
ReadinessService.get_dashboard_readiness_surface
        │
        ├── (ineligible) legacy getters  ← collector-safe authority
        │         └── EP-002.6 dual-run when Twin ON non-prod + Cutover OFF
        │
        └── (eligible) consumer_chain.readiness_cutover
                ├── legacy getters (baseline + fallback)
                ├── build_readiness_intelligence
                │     → observe_build_api (EP-002.1)
                │     → Foundation CLS share (EP-002.2)
                │     → readiness_intelligence consumer / assessment
                ├── project + semantic align
                └── CONSUMER_CHAIN_CUTOVER + readiness_cutover_health
```

**Hard invariant verified:** `get_overall_readiness` does not call Foundation / intelligence / dual-run / cutover.

**Observation:** Dependency direction unchanged from EP-001.5 / EP-002.1–5.  
**Evidence:** Service source inspection test; collector source regression; package inventory delta limited to `consumer_chain/readiness_*`.  
**Conclusion:** Constitutional runtime dependency graph preserved; no recursion into Runtime A collectors.  
**Recommendation:** Keep Adaptive / settings callers on legacy getters until an explicit collector refactor milestone exists (out of EP-002 critical path).

---

## 10. Operational Metrics

| Signal | Status |
|---|---|
| `CONSUMER_CHAIN_CUTOVER` (api=`build_readiness_intelligence`) | Emitted with attempted/served/fallback/alignment/latencies/flags |
| Dual-run telemetry (api=`build_readiness_intelligence`) | Emitted when Twin ON non-prod and cutover OFF |
| Nested `observe_build_api` on Twin call | Still emits when Twin path runs |
| In-process readiness cutover health metrics | Architecture Metrics source |
| In-process readiness dual-run health metrics | Dual-run ops channel |
| Student UI exposure of ops fields | **None** (score/topics only) |

**Observation:** Engineers can answer “did readiness cutover attempt, serve Twin, or fall back — and why?” on dashboard/analytics traffic in non-prod.  
**Evidence:** Health snapshot tests + controlled bench.  
**Conclusion:** Operational evidence channel for gated readiness activation is live.  
**Recommendation:** Scrape staging readiness cutover logs before EP-002.7 / production consideration.

---

## 11. Risks

| ID | Risk | Likelihood | Impact | Mitigation status |
|---|---|---|---|---|
| R1 | Collector recursion | Low | High | **Mitigated** — facade-only; regression tests |
| R2 | Accidental production cutover | Low | High | Env hard-exclude + flags default OFF |
| R3 | Score divergence confuses staging reviewers | Medium | Medium | Semantic alignment + tolerance ≤ 10 |
| R4 | Twin latency on dashboard/analytics | Medium | Medium | P95 metrics; kill switch |
| R5 | Double Twin assemble with Insights cutover | Medium | Low | Shared Foundation DI; independent ContextVars |
| R6 | Scope creep to mission / Experience | Medium | High | Explicit out-of-scope |

Full register: [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md).

---

## 12. Technical Debt

| ID | Debt | Disposition |
|---|---|---|
| TD-RI-01 | In-process cutover/dual-run metrics are process-local | Accept; logs are durable ops channel |
| TD-RI-02 | Narrative still uses EducationalExplainability on projected score | Accept; WS7 after multi-surface cutover |
| TD-RI-03 | Alignment score tolerance is heuristic (10 points) | Accept for gated non-prod; refine with live staging samples |
| TD-RI-04 | Experience `/student` home not on this cutover path | Accept; separate Experience TwinPort track |
| TD-CO-02 (inherited) | EI dashboard card path still separate narrator | Unchanged; WS7 |

**Conclusion:** No new unjustified architectural debt; named items are sequenced.  
**Recommendation:** Burn TD-RI-03 with staging samples before production consideration.

---

## 13. Constitutional Compliance

| Invariant | Status |
|---|---|
| Twin owns learner-state read model | Preserved |
| Planner owns plans | Preserved |
| Readiness owns evaluation | Preserved (projection maps readiness assessment) |
| Insight owns communication only | Preserved (Insights cutover independent) |
| Runtime A writes unchanged | Preserved |
| Curriculum V1/V2 traversal untouched | N/A — no curriculum diffs |
| Collectors keep legacy getters | **Preserved** |
| No new Twin stack / readiness engine | Preserved |
| No schema migrations | Preserved |
| Production defaults Twin/Cutover OFF | Preserved |
| Not claiming Twin Ready (T7) | Explicit non-claim |

**Observation:** Ownership matrix unchanged.  
**Evidence:** Diff review against EP-001.3 contracts; no new evaluation maths outside readiness_intelligence package.  
**Conclusion:** Constitutionally compliant.  
**Recommendation:** Reject any follow-up that wraps `get_overall_readiness` with Foundation calls.

---

## 14. Architectural Delta

| Area | Before EP-002.6 | After EP-002.6 |
|---|---|---|
| Dual-run | Study Insights only | + Readiness Intelligence dual-run |
| HTTP readiness authority | Legacy getters only | Gated Twin projection on dashboard/analytics |
| Flag surface | Study Insights cutover | + `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` |
| Collectors | Legacy getters | **Unchanged** |
| Templates | Legacy field contract | Unchanged (projection) |
| Schema | — | No change |
| Ownership | Twin / Planner / Readiness / Insight | Unchanged |

New modules:

- `app/infrastructure/adapters/consumer_chain/readiness_dual_run.py`
- `app/infrastructure/adapters/consumer_chain/readiness_cutover.py`
- `app/infrastructure/adapters/consumer_chain/readiness_dual_run_health.py`
- `app/infrastructure/adapters/consumer_chain/readiness_cutover_health.py`

---

## 15. Architecture Metrics

Controlled bench (n=50 eligible non-prod cutover attempts with injected Twin success / None / blocking / exception mix):

| Metric | Value | Notes |
|---|---|---|
| Eligible Requests | **50** | Cutover attempted |
| Legacy Fallback Rate | **0.24** (12/50) | Fail-open path |
| Readiness Success Rate (Twin served) | **0.76** (38/50) | `cutover_served` |
| Alignment Rate | **0.921** (35 aligned / 38 comparable) | Among aligned+mismatched |
| Limitation-Driven Fallback Rate | **0.08** (4/50) | Blocking / empty projection |
| Average Legacy Latency | **~0.001 ms** | Bench stubs (not live DB) |
| Average Readiness Latency | **~0.001 ms** | Bench stubs (not live Twin assemble) |
| P95 Legacy Latency | **~0.002 ms** | Bench stubs |
| P95 Readiness Latency | **~0.003 ms** | Bench stubs |
| Behavioural Regressions | **0** | Health counter |
| Ownership Violations | **0** | Health counter |
| Student Impact Scope | Non-prod gated dashboard/analytics readiness only | Production = none |
| Overall Readiness Cutover Health | **`ready_for_ep002_7_planning`** | No regressions / ownership violations; Twin served |

**Observation:** Bench latencies are orchestration stubs and must not be treated as production SLOs.  
**Evidence:** In-process `ReadinessCutoverHealthMetrics.snapshot()` from controlled bench; pytest suite green (24 readiness dual-run/cutover tests + flag tests).  
**Conclusion:** Cutover health is green for **planning** EP-002.7 — not for production activation.  
**Recommendation:** Recompute Architecture Metrics on staging with live Foundation assemble before any production gate discussion. Treat live P95 Twin latency as the go/no-go signal.

### Tests executed

```bash
python3 -m pytest \
  tests/infrastructure/adapters/consumer_chain/test_readiness_dual_run.py \
  tests/infrastructure/adapters/consumer_chain/test_readiness_cutover.py \
  tests/application/config/test_v2_flags.py::test_readiness_intelligence_cutover_flag_defaults_off \
  tests/application/config/test_v2_flags.py::test_readiness_intelligence_cutover_flag_requires_twin \
  tests/application/config/test_v2_flags.py::test_readiness_intelligence_cutover_flag_enables_with_twin \
  tests/application/config/test_v2_flags.py::test_v2_flags_default_keep_v1_primary \
  -q
# 28 passed

python3 -m ruff check \
  app/infrastructure/adapters/consumer_chain/readiness_*.py \
  app/services/readiness_service.py \
  app/dashboard/routes.py \
  app/analytics/routes.py \
  app/application/config/v2_flags.py \
  tests/infrastructure/adapters/consumer_chain/test_readiness_*.py \
  --ignore E712
# All checks passed
```

Coverage includes: HTTP integration, cutover eligibility, fallback paths, semantic alignment, collector regression, feature flags, Twin OFF/ON, blocking limitations, legacy fail-open.

### Migration impact

**None** — no Alembic / schema changes.

---

## 16. Recommendation for EP-002.7

**Observation:** EP-002 programme order is recommendations → readiness → mission/plan. Insights cutover (EP-002.5) and readiness cutover (EP-002.6) now exist as gated non-prod surfaces.  
**Evidence:** Programme brief WS6; MissionOptimizer quarantine decision from EP-002.2; higher blast radius for mission start / today mission.  
**Conclusion:** Safe to **plan** EP-002.7 — Daily plan / mission dual-run → gated HTTP cutover — after staging soak evidence for readiness cutover on real traffic.  
**Recommendation:**

1. Soak EP-002.6 on staging with Twin ON + Readiness Cutover ON; confirm fallback rates and alignment.  
2. Keep production Twin / Authority / both Cutover flags OFF.  
3. Start EP-002.7 discovery for `build_daily_study_plan` vs `generate_today_mission` with MissionOptimizer quarantine respected.  
4. Do not merge Experience `/student` readiness into EP-002.7 without a separate brief.  
5. Do not declare Twin Ready (T7) from this milestone.

---

## Files Created

- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/README.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/CUTOVER_DESIGN.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/ELIGIBILITY_MATRIX.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/ROLLBACK_PLAN.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/STUDENT_IMPACT_ASSESSMENT.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/RISK_ASSESSMENT.md`
- `knowledge/architecture/ep002_6_readiness_intelligence_cutover/COMPLETION_REPORT.md`
- `app/infrastructure/adapters/consumer_chain/readiness_dual_run.py`
- `app/infrastructure/adapters/consumer_chain/readiness_cutover.py`
- `app/infrastructure/adapters/consumer_chain/readiness_dual_run_health.py`
- `app/infrastructure/adapters/consumer_chain/readiness_cutover_health.py`
- `tests/infrastructure/adapters/consumer_chain/test_readiness_dual_run.py`
- `tests/infrastructure/adapters/consumer_chain/test_readiness_cutover.py`

## Files Modified

- `app/application/config/v2_flags.py`
- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/services/readiness_service.py`
- `app/dashboard/routes.py`
- `app/analytics/routes.py`
- `.env.example`
- `tests/application/config/test_v2_flags.py`

---

## Exit verdict

| Success criterion | Status |
|---|---|
| Eligible requests receive Readiness Intelligence | ✓ |
| Legacy readiness remains fail-open | ✓ |
| Alignment reporting operational | ✓ |
| Behaviour unchanged outside eligible cohorts | ✓ |
| No ownership violations | ✓ |
| No schema changes / no new engines / no Twin redesign | ✓ |
| No collector recursion | ✓ |
| No production-wide activation | ✓ |

**Accept EP-002.6. Next: staging soak, then EP-002.7 discovery.**
