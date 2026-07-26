# EP-002.7 — Completion Report

**Milestone:** EP-002.7 — Daily Plan & Mission Dual-Run and Gated HTTP Cutover  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** Dual-run diagnostics + first controlled student-facing activation of Twin-backed Daily Study Plan on dashboard/missions — **legacy fail-open fallback retained**; **MissionOptimizer remains quarantined**; **no production-wide activation**  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `CONSTITUTIONAL_IMPACT_ASSESSMENT.md`, `CONSTITUTIONAL_GAP_ANALYSIS.md`, `CUTOVER_DESIGN.md`, `ELIGIBILITY_MATRIX.md`, `ROLLBACK_PLAN.md`, `STUDENT_IMPACT_ASSESSMENT.md`, `RISK_ASSESSMENT.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.7 activates the final Runtime A intelligence surface using the constitutional pattern proven in EP-002.5/6: observe beside legacy → dual-run → gated HTTP cutover with fail-open fallback.

**Observation:** Before this milestone, `build_daily_study_plan` existed (EP-001.2) with observability and soak, but students never received Twin daily-plan projections over HTTP; dashboard/missions called `generate_today_mission` only.  
**Evidence:** Dashboard and mission routes now call `PlanningService.get_dashboard_mission_surface`; cutover requires Twin ON ∧ `KWALITEC_DAILY_PLAN_CUTOVER` ON ∧ non-production env ∧ successful Twin response ∧ no blocking limitation ∧ legacy ORM mission anchor. Controlled bench: **50** eligible requests, Twin served **38 / 50** (76%), legacy fallback **24%**, behavioural regressions **0**, ownership violations **0**. MissionOptimizer callers in cutover path **0**. Production remains ineligible by design.  
**Conclusion:** Objectives met. Eligible cohorts can receive Daily Plan projections; fail-open legacy behaviour is validated; alignment reporting is operational; MissionOptimizer quarantine holds; behaviour outside eligible cohorts is unchanged.  
**Recommendation:** Accept EP-002.7. Proceed to **EP-002.8** presentation consolidation only after staging soak. Keep production Twin / Authority / all Cutover flags OFF. Do not claim Twin Ready (T7).

No schema migrations. No new planning engines. No ownership changes. No MissionOptimizer wiring.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, EP-002 programme brief, EP-002.1–6 completion reports, PlanningService, `generate_today_mission`, `build_daily_study_plan`, dashboard/mission surfaces, consumer-chain cutover pattern, MissionOptimizer quarantine decision, and constitutional documents.

| Finding | Detail |
|---|---|
| Authoritative legacy path | `generate_today_mission` (ORM) + `MissionService.get_today_mission` |
| Twin path | `build_daily_study_plan` — previously observability/soak/grounding only |
| HTTP surfaces | `/dashboard` and `/missions` today-mission cards |
| Gap | No dual-run; no student-facing Twin projection |
| New flag needed? | **Yes** — `KWALITEC_DAILY_PLAN_CUTOVER` (default OFF; requires Twin) |
| Insertion point | `get_dashboard_mission_surface` + `consumer_chain/daily_plan_*.py` |
| Binding constraint | MissionOptimizer quarantined; Twin must not write ORM |

Full detail: supporting artefacts in this directory.

**Conclusion:** Implementation authorised only after discovery — dual-run + gated cutover under `consumer_chain` + thin PlanningService facade.

---

## 3. Constitutional Impact Assessment

See [`CONSTITUTIONAL_IMPACT_ASSESSMENT.md`](CONSTITUTIONAL_IMPACT_ASSESSMENT.md).

**Observation:** PlanningService remains sole owner of planning outputs and mission persistence; Twin owns learner-state read model only.  
**Evidence:** Cutover invokes `PlanningService.build_daily_study_plan` / `generate_today_mission` exclusively; `MissionDisplayProxy` never writes DB; MissionOptimizer not imported by cutover/dual-run modules.  
**Conclusion:** No ownership drift; no STOP condition.  
**Recommendation:** Keep Experience bridges on `generate_today_mission` until an explicit bridge milestone.

---

## 4. Student Impact Assessment

| Cohort | Impact |
|---|---|
| Production | None |
| Non-prod Twin OFF / Cutover OFF | None visible (dual-run only when Twin ON + Cutover OFF) |
| Non-prod Twin ON + Cutover ON + success | Today-mission title/narrative may reflect Twin plan slots |
| Eligible failure paths | Legacy fail-open |

Surfaces: `/dashboard`, `/missions` only. Experience MissionStartAdapter and StudyPlanService sync unchanged.

---

## 5. Cutover Design

Executed per [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md):

```
Dashboard / Missions
        │
        ▼
get_dashboard_mission_surface()
        │
        ├─ ineligible ──► legacy mission ──► dual-run side-car (Twin ON non-prod)
        │
        └─ eligible
                ├─ legacy (fail-open + ORM anchor + alignment baseline)
                ├─ build_daily_study_plan()
                ├─ None / exception / blocking ──► legacy
                └─ success ──► project → MissionDisplayProxy (influences_student=True)
```

| Design choice | Rationale |
|---|---|
| New surface facade (not mutate `generate_today_mission`) | Protects bridges / sync paths |
| MissionDisplayProxy title overlay | Templates unchanged; Twin does not write ORM |
| Skip dual-run when cutover eligible | Avoid double Twin assemble |
| Request-scoped cache | Dashboard + missions share one Twin decision |
| Semantic plan/mission alignment | Topic / objective / sequencing / workload |

Rollback: [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md).

---

## 6. Eligibility Matrix

| Twin | Cutover | `APP_ENV` | Dual-run? | Cutover attempt? | Student response |
|---|---|---|---|---|---|
| OFF | * | any | No | No | Legacy |
| ON | OFF | non-prod | **Yes** | No | Legacy |
| ON | ON | non-prod | No (skipped) | **Yes** | Twin projection if success + non-blocking; else legacy |
| ON | ON | production / prod | No | No | Legacy |

Authority is **recorded**, not required for this Runtime A Foundation path.

---

## 7. HTTP Routing Changes

| Location | Change |
|---|---|
| `app/dashboard/routes.py` `index()` | Calls `get_dashboard_mission_surface`; skips EducationalExplainability when Twin authority |
| `app/mission/routes.py` missions view | Same surface facade |
| `PlanningService` | Adds `get_dashboard_mission_surface`; dual-run hook when cutover ineligible |
| Templates | **Unchanged** (proxy preserves Mission attribute access) |
| Experience MissionStartAdapter | **Unchanged** |
| MissionOptimizer | **Unchanged / quarantined** |

---

## 8. Fallback Behaviour

| Trigger | Reason code |
|---|---|
| Twin OFF | `twin_off` |
| Cutover flag OFF | `cutover_flag_off` |
| Production env | `production_env` |
| Config failure | `configuration_failure` |
| Twin `None` | `twin_unavailable` |
| Twin exception | `twin_exception` |
| Blocking limitation | `blocking_limitation` |
| Empty / unanchored projection | `projection_empty` |

**Evidence:** Fail-open unit tests for Twin OFF / flag OFF / production / None / exception / blocking.  
**Conclusion:** Constitutional fail-open preserved.

---

## 9. Alignment Analysis

| Status | Meaning |
|---|---|
| `aligned` | Topic ∧ objective ∧ sequencing ∧ workload agreement |
| `mismatched` | Twin served but dimension disagreement |
| `twin_unavailable` | Twin not attempted / None / exception / flag gates |
| `limitation_fallback` | Blocking limitation or empty projection |

Captured dimensions (milestone requirement): topic agreement, study objective agreement, sequencing agreement, workload agreement.

Fingerprint divergence remains expected and is **not** a cutover quality gate.

---

## 10. Runtime Dependency Verification

```
HTTP dashboard / missions (cutover-aware)
        │
        ▼
PlanningService.get_dashboard_mission_surface
        │
        ├── (ineligible) generate_today_mission  ← legacy authority + ORM writes
        │         └── EP-002.7 dual-run when Twin ON non-prod + Cutover OFF
        │
        └── (eligible) consumer_chain.daily_plan_cutover
                ├── generate_today_mission (baseline + fallback + ORM anchor)
                ├── build_daily_study_plan
                │     → observe_build_api (EP-002.1)
                │     → Foundation CLS share (EP-002.2)
                │     → adaptive_study_planner assembler
                ├── project + semantic align
                └── CONSUMER_CHAIN_CUTOVER + daily_plan_cutover_health
```

**Hard invariants verified:**

- `generate_today_mission` does not call cutover / Foundation for HTTP authority.  
- MissionOptimizer is not imported by dual-run or cutover modules.  
- Twin projection does not persist missions.

---

## 11. Feature Flag Matrix

| Twin | Cutover | Authority | `APP_ENV` | Dual-run? | Cutover attempt? | Student response |
|---|---|---|---|---|---|---|
| OFF | * | * | any | No | No | Legacy |
| ON | OFF | * | non-prod | Yes | No | Legacy |
| ON | ON | OFF | non-prod | No | **Yes** | Twin or legacy fail-open |
| ON | ON | ON | non-prod | No | **Yes** | Twin or legacy fail-open |
| ON | ON | * | production | No | No | Legacy |

New env: `KWALITEC_DAILY_PLAN_CUTOVER` → `ENABLE_DAILY_PLAN_CUTOVER` (requires Twin; default OFF).

---

## 12. Operational Metrics

| Signal | Status |
|---|---|
| `CONSUMER_CHAIN_CUTOVER` (api=`build_daily_study_plan`) | Emitted with attempted/served/fallback/alignment/latencies/flags |
| Dual-run telemetry (api=`build_daily_study_plan`) | Emitted when Twin ON non-prod and cutover OFF |
| Nested `observe_build_api` on Twin call | Still emits when Twin path runs |
| In-process daily-plan cutover health metrics | Architecture Metrics source |
| Student UI exposure of ops fields | **None** |

---

## 13. Risks

| ID | Risk | Mitigation status |
|---|---|---|
| R1 | Accidental production cutover | **Mitigated** — env hard-exclude + defaults OFF |
| R2 | Display ≠ ORM session topic | **Accepted** as TD-DP-01 |
| R3 | Twin latency | Metrics + kill switch |
| R4 | MissionOptimizer re-wire | Quarantine tests |
| R5 | Ownership drift | Facade-only design |
| R6 | Double assemble | Shared DI + ContextVars |
| R7 | Experience scope creep | Explicit out-of-scope |

Full register: [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md).

---

## 14. Technical Debt

| ID | Debt | Disposition |
|---|---|---|
| TD-DP-01 | Twin display title may diverge from legacy ORM session topic | Accept for gated non-prod; future PlanningService generation alignment |
| TD-DP-02 | Experience MissionStartAdapter still legacy | Accept; separate bridge milestone |
| TD-DP-03 | In-process metrics are process-local | Accept; logs are durable ops channel |
| TD-DP-04 | MissionOptimizer hard-delete deferred | Accept; quarantine sufficient (EP-002.2) |
| TD-CO-02 (inherited) | Presentation dual-path residual | WS7 / EP-002.8 |

---

## 15. Constitutional Compliance

| Invariant | Status | Evidence |
|---|---|---|
| Twin owns learner-state read model | Preserved | No Twin redesign; Foundation assemble only |
| Planner owns plans | Preserved | `build_daily_study_plan` remains PlanningService API |
| Readiness owns evaluation | Preserved | Independent cutover |
| Insight owns communication only | Preserved | Independent cutover |
| Runtime A writes unchanged | Preserved | Twin does not write Mission rows |
| Curriculum V1/V2 traversal untouched | N/A | No curriculum diffs |
| MissionOptimizer quarantined | **Preserved** | Source guards + EP-002.2 tests |
| No new Twin stack / planning engine | Preserved | Package inventory delta limited to `consumer_chain/daily_plan_*` |
| No schema migrations | Preserved | No Alembic |
| Production defaults Twin/Cutover OFF | Preserved | Flag tests |
| Not claiming Twin Ready (T7) | Explicit non-claim | This section |

---

## 16. Constitutional Verification

| Check | Result | Evidence |
|---|---|---|
| Cutover never calls MissionOptimizer | **Pass** | `test_mission_optimizer_quarantine_preserved`; import guards |
| Dual-run never calls MissionOptimizer | **Pass** | `test_mission_optimizer_not_imported_by_dual_run` |
| `generate_today_mission` body free of cutover | **Pass** | `test_generate_today_mission_unchanged_for_bridges` |
| Fail-open for Twin OFF / flag OFF / production | **Pass** | Parametrised cutover tests |
| Fail-open for None / exception / blocking | **Pass** | Dedicated cutover tests |
| Eligible Twin serve projects plan into mission DTO | **Pass** | `test_cutover_serves_twin_when_eligible` + projection test |
| Ownership violations counter | **0** | Controlled bench health snapshot |
| Behavioural regressions counter | **0** | Controlled bench health snapshot |
| No collector-style recursion into legacy getters | **Pass** | Facade-only; bridges unchanged |

**Observation:** Every constitutional assertion above is backed by an automated check or explicit source inspection test.  
**Conclusion:** Constitutional verification **passes**.  
**Recommendation:** Keep quarantine regression tests in CI.

---

## 17. Constitutional Drift Register

| Drift ID | Description | Status | Evidence |
|---|---|---|---|
| CD-01 | MissionOptimizer production wiring | **None observed** | Quarantine tests green |
| CD-02 | Twin writing Mission ORM | **None observed** | Projection proxy only; no `db.session` in cutover |
| CD-03 | Parallel mission engine package | **None observed** | No new planner package |
| CD-04 | Planning authority outside PlanningService | **None observed** | Cutover delegates to PlanningService APIs |
| CD-05 | Production cutover eligibility | **None observed** | Env gate tests |
| CD-06 | Display/persistence topic split | **Known accepted** (TD-DP-01) | Documented limitation — not silent drift |

---

## 18. Constitutional Sign-Off

| Statement | Signed? | Evidence |
|---|---|---|
| Discovery completed before implementation | **Yes** | Discovery artefacts in this directory |
| MissionOptimizer remains quarantined | **Yes** | §16 verification + EP-002.2 decision |
| PlanningService remains sole planning owner | **Yes** | §3 / §15 |
| No duplicate planning authority | **Yes** | §15 / drift register |
| No ownership violations | **Yes** | Health counter = 0; verification table |
| Fail-open legacy retained | **Yes** | §8 + tests |
| Production not activated | **Yes** | Eligibility matrix + flag defaults |
| No unjustified constitutional assertion | **Yes** | Every claim includes Evidence column |

**Sign-off verdict:** **ACCEPT EP-002.7** as constitutionally compliant gated non-prod activation.

---

## 19. Architectural Delta

| Area | Before EP-002.7 | After EP-002.7 |
|---|---|---|
| Dual-run | Insights + Readiness | + Daily Plan |
| HTTP mission authority | Legacy ORM only | Gated Twin projection on dashboard/missions |
| Flag surface | Insights + Readiness cutovers | + `KWALITEC_DAILY_PLAN_CUTOVER` |
| MissionOptimizer | Quarantined | Quarantined |
| Templates | Legacy Mission fields | Unchanged (proxy) |
| Schema | — | No change |
| Ownership | Twin / Planner / Readiness / Insight | Unchanged |

New modules:

- `app/infrastructure/adapters/consumer_chain/daily_plan_dual_run.py`
- `app/infrastructure/adapters/consumer_chain/daily_plan_cutover.py`
- `app/infrastructure/adapters/consumer_chain/daily_plan_dual_run_health.py`
- `app/infrastructure/adapters/consumer_chain/daily_plan_cutover_health.py`
- `tests/infrastructure/adapters/consumer_chain/test_daily_plan_dual_run.py`
- `tests/infrastructure/adapters/consumer_chain/test_daily_plan_cutover.py`

---

## 20. Architecture Metrics

Controlled bench (n=50 eligible non-prod cutover attempts with injected Twin success / None / blocking / exception mix):

| Metric | Value | Notes |
|---|---|---|
| Eligible Requests | **50** | Cutover attempted |
| Legacy Fallback Rate | **0.24** (12/50) | Fail-open path |
| Twin Success Rate (served) | **0.76** (38/50) | `cutover_served` |
| Limitation-Driven Fallback Rate | **0.08** (4/50) | Blocking |
| Behavioural Regressions | **0** | Health counter |
| Ownership Violations | **0** | Health counter |
| Student Impact Scope | Non-prod gated dashboard/missions only | Production = none |
| Overall Daily Plan Cutover Health | **`ready_for_ep002_8_presentation`** | No regressions / ownership violations; Twin served |

Bench latencies are orchestration stubs and must not be treated as production SLOs.

### Tests executed

```bash
python3 -m pytest \
  tests/infrastructure/adapters/consumer_chain/test_daily_plan_dual_run.py \
  tests/infrastructure/adapters/consumer_chain/test_daily_plan_cutover.py \
  tests/application/config/test_v2_flags.py::test_daily_plan_cutover_flag_defaults_off \
  tests/application/config/test_v2_flags.py::test_daily_plan_cutover_flag_requires_twin \
  tests/application/config/test_v2_flags.py::test_daily_plan_cutover_flag_enables_with_twin \
  tests/infrastructure/adapters/consumer_chain/test_mission_optimizer_decision.py \
  -q
# 34 passed

python3 -m ruff check \
  app/infrastructure/adapters/consumer_chain/daily_plan_*.py \
  app/infrastructure/adapters/consumer_chain/__init__.py \
  app/dashboard/routes.py \
  app/mission/routes.py \
  app/application/config/v2_flags.py \
  tests/infrastructure/adapters/consumer_chain/test_daily_plan_*.py \
  --ignore E712
# All checks passed
```

Coverage includes: HTTP facade, cutover eligibility, fallback paths, semantic alignment, MissionOptimizer quarantine, feature flags, Twin OFF/ON, blocking limitations, legacy fail-open, controlled bench.

### Migration impact

**None** — no Alembic / schema changes.

### Architecture compliance

Layering preserved (routes → PlanningService → consumer_chain / planner adapters). Curriculum V1/V2 traversal untouched. Twin packages do not gain planning authority. MissionOptimizer quarantine preserved.

---

## 21. Recommendation for EP-002.8

**Observation:** Programme order after WS6 is presentation consolidation (WS7).  
**Evidence:** Programme brief EP-002.8; health gate `ready_for_ep002_8_presentation`.  
**Conclusion:** Safe to **plan** EP-002.8 after staging soak of daily-plan cutover.  
**Recommendation:**

1. Soak EP-002.7 on staging with Twin ON + Daily Plan Cutover ON; confirm fallback and alignment.  
2. Keep production Twin / Authority / all Cutover flags OFF.  
3. Do not un-quarantine MissionOptimizer; hard-delete remains optional.  
4. Address TD-DP-01 only via PlanningService-owned generation design — not via Twin writes.  
5. Do not declare Twin Ready (T7).

---

## Files Created

- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/README.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/CONSTITUTIONAL_IMPACT_ASSESSMENT.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/CONSTITUTIONAL_GAP_ANALYSIS.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/STUDENT_IMPACT_ASSESSMENT.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/CUTOVER_DESIGN.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/ELIGIBILITY_MATRIX.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/ROLLBACK_PLAN.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/RISK_ASSESSMENT.md`
- `knowledge/architecture/ep002_7_daily_plan_mission_cutover/COMPLETION_REPORT.md`
- `app/infrastructure/adapters/consumer_chain/daily_plan_dual_run.py`
- `app/infrastructure/adapters/consumer_chain/daily_plan_cutover.py`
- `app/infrastructure/adapters/consumer_chain/daily_plan_dual_run_health.py`
- `app/infrastructure/adapters/consumer_chain/daily_plan_cutover_health.py`
- `tests/infrastructure/adapters/consumer_chain/test_daily_plan_dual_run.py`
- `tests/infrastructure/adapters/consumer_chain/test_daily_plan_cutover.py`

## Files Modified

- `app/application/config/v2_flags.py`
- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/services/planning_service.py`
- `app/dashboard/routes.py`
- `app/mission/routes.py`
- `.env.example`
- `tests/application/config/test_v2_flags.py`

---

## Exit verdict

| Success criterion | Status |
|---|---|
| Daily Plan served for eligible requests | ✓ |
| Legacy retained as fail-open | ✓ |
| MissionOptimizer remains quarantined | ✓ |
| Constitutional verification passes | ✓ |
| No ownership violations | ✓ |
| Behaviour unchanged outside eligible cohorts | ✓ |
| No schema changes / no new engines / no Twin redesign | ✓ |
| No production-wide activation | ✓ |

**Accept EP-002.7. Next: staging soak, then EP-002.8 presentation consolidation.**
