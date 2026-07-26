# EP-002.3 — Discovery Report

**Milestone:** EP-002.3 — Twin & Authority Non-Production Soak  
**Date:** 2026-07-26  
**Status:** Complete — implementation authorised only after this report  
**Legend:** **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Sources reviewed

| Source | Relevance |
|---|---|
| EP-001.5 Architectural Integration Review | Foundation accept; soak prerequisite for Authority / cutover |
| EP-002 Programme Brief | WS3 Twin + Authority soak; gates EP-002.4 |
| EP-002.1 Completion Report | `build_*` observability contracts + Twin quarantine |
| EP-002.2 Completion Report | Shared Foundation DI; assemble / share-hit telemetry |
| `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` | MS-004 + EP-001.1 Foundation / Authority semantics |
| `TWIN_STACK_QUARANTINE.md` | Operator authority matrix; Authority soak path |
| `app/application/config/v2_flags.py` | Twin + Authority flags; Authority requires Twin |
| `consumer_chain` telemetry / foundation_di | Latency, outcomes, assemble vs share-hit |
| Experience composition TwinPort wiring | Authority ON → Foundation port; OFF → ExperienceTwinAdapter |
| Existing Twin / Adaptive soak patterns | Reusable observational soak + rollback shapes |

---

## 2. Current operational posture

**Observation:** Production HTTP still calls legacy Runtime A APIs. Twin and Authority default OFF.

**Evidence:**

| Flag | Env | Default | Effect |
|---|---|---|---|
| Digital Twin | `KWALITEC_DIGITAL_TWIN` | OFF | Foundation DI + `build_*` return values; Shadow / Adaptive TwinInput bundled |
| Twin Authority | `KWALITEC_DIGITAL_TWIN_AUTHORITY` | OFF | Experience `StudentTwinPort` serves Foundation **only if Twin ON** |

| API | Twin OFF | Twin ON |
|---|---|---|
| `build_daily_study_plan` | `None` (legacy mission path) | Plan projection or `None` / limitations |
| `build_readiness_intelligence` | `None` (legacy readiness path) | Assessment or `None` / limitations |
| `build_study_insights` | `None` (legacy recommendations) | Guidance or `None` / limitations |

Experience TwinPort:

| Twin | Authority | UX TwinPort |
|---|---|---|
| OFF | (ignored — Authority requires Twin) | `ExperienceTwinAdapter` |
| ON | OFF | `ExperienceTwinAdapter` |
| ON | ON | `StudentTwinFoundationAuthorityPort` (fallback = ExperienceTwinAdapter) |

**Conclusion:** Fail-open design is intact. Soak must exercise Twin ON and Authority ON in non-prod only, then prove Twin OFF → Authority OFF restores pre-soak composition.

---

## 3. What already exists (reuse)

| Component | Reuse for soak |
|---|---|
| `observe_build_api` / `ConsumerChainTelemetry` | Latency, outcome, limitation codes, Twin/Authority flag snapshot |
| `assemble_shared_canonical_state` | Foundation assemble vs share-hit counts |
| `TwinRollbackVerifier` | Twin OFF removes Twin DI; Experience TwinPort preserved |
| `StudentTwinFoundationAuthorityPort` | Fail-open to ExperienceTwinAdapter on Foundation failure |
| `resolve_v2_feature_flags` | Matrix resolution (Authority ∧ Twin) |
| Adaptive / Twin shadow soak patterns | Orchestrator + health + rollback + telemetry shape |

**Observation:** No dedicated Twin+Authority consumer-chain soak orchestrator existed before this milestone.  
**Evidence:** Grep — soak modules under `adaptive_engine/` and Twin shadow rollback only; no `consumer_chain/soak*`.  
**Conclusion:** EP-002.3 must add observational soak harness, not a new educational engine.

---

## 4. Soak targets (binding)

Exercise under realistic non-production workloads:

1. `PlanningService.build_daily_study_plan`
2. `ReadinessService.build_readiness_intelligence`
3. `RecommendationService.build_study_insights`

Capture:

- Latency distributions (avg / p95)
- Foundation assembly count vs share-hit rate
- Failure / exception rates
- Limitation-code frequency
- Twin / Authority flag state on each observation
- Experience TwinPort routing per Authority matrix cell
- Rollback success (Twin OFF then Authority OFF → pre-soak)

---

## 5. Explicit non-goals

| Non-goal | Rationale |
|---|---|
| Production cutover | Programme P3 not authorised |
| HTTP dual-run / route changes | EP-002.4+ |
| Schema / Alembic | Constraint |
| New feature flags | Existing Twin + Authority sufficient |
| New planner / readiness / insight engines | EP-001 ownership preserved |
| Declaring Twin Ready (T7) | Explicit non-claim |
| Wiring MissionOptimizer | Quarantined (EP-002.2) |

---

## 6. Risks discovered

| ID | Risk | Mitigation |
|---|---|---|
| D-R1 | Soak harness accidentally influences HTTP | Keep soak observational; never register routes |
| D-R2 | Authority ON without Twin appears “broken” | Matrix documents Authority requires Twin; flag resolver already ANDs |
| D-R3 | Demo-seed under Authority confuses TwinPort | Composition already disables Twin demo seed when Authority ON |
| D-R4 | Nested Insight compose latency misread as regression | Use EP-002.2 share-hit metrics; report assemble vs injected |
| D-R5 | Operators treat soak green as production Authority go | Completion report forbids production ON |

---

## 7. Discovery verdict

**Observation:** EP-002.1–2 provide measurement and cheaper compose; EP-001 Authority port and Twin rollback already exist.  
**Evidence:** Programme brief WS3; EP-002.2 recommendation §20; quarantine note “Authority soak path”.  
**Conclusion:** Discovery complete. Implementation authorised as **ops harness + evidence report**, reusing existing flags and telemetry.  
**Recommendation:** Proceed with Soak Plan, Rollback Plan, and Success Criteria; then implement `consumer_chain` soak modules and execute non-prod soak.
