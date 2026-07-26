# EP-002.1 — Completion Report

**Milestone:** EP-002.1 — Consumer-Chain Observability & Twin Quarantine  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** Implementation — observability + documentation; **no student-facing UX authority change**  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `GAP_ANALYSIS.md`, `IMPLEMENTATION_PLAN.md`, `../TWIN_STACK_QUARANTINE.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.1 makes the EP-001 consumer chain (`build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights`) operationally measurable without changing what students see.

**Observation:** Production HTTP still uses legacy Runtime A APIs; Twin defaults remain OFF.  
**Evidence:** Public `build_*` signatures and return semantics are preserved; observability wraps bodies via `observe_build_api`. Tests for Twin OFF / ON flag recording, Authority gating, dual-run eligibility, and EP-001.2–4 unit suites pass.  
**Conclusion:** TD-OPS-01 (live `build_*` observability), TD-ARCH-01 (Twin quarantine narrative), and TD-ARCH-06 (Shadow / Adaptive TwinInput doc drift) are closed for this milestone’s scope.  
**Recommendation:** Accept EP-002.1. Proceed to **EP-002.2** (shared Foundation DI + MissionOptimizer decision) using these signals to measure assemble cost before/after.

No schema migrations. No new feature flags. No new Twin / planner / readiness / recommendation engines. No HTTP cutover.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, the EP-002 programme brief, MS-004 Twin architecture, Runtime A Planning / Readiness / Recommendation services, `v2_flags.py`, and existing diagnostics / telemetry.

| Finding | Detail |
|---|---|
| Entry points | Three Twin-gated `build_*` hosts on Runtime A services |
| Logging | Ad-hoc module loggers only — no structured outcome matrix |
| Telemetry | Reusable `StructuredLogger`, `CorrelationContext`, `EventRegistry` |
| Flags | Twin + Authority only; Shadow / Adaptive TwinInput bundled under Twin ON |
| Gap | Engineers could not answer invocation / latency / outcome / None / limitations / flags for `build_*` |

Full detail: [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md).

**Conclusion:** Implementation should extend existing diagnostics + events — not invent a second framework. No new feature flag required.

---

## 3. Existing Components Reused

| Component | Reuse |
|---|---|
| `StructuredLogger` | Primary structured log sink |
| `CorrelationContext` | Request / pipeline identifier linkage |
| `EventRegistry` / `IntegrationEvent` | Optional in-process observational events |
| `resolve_v2_feature_flags` | Twin + Authority snapshot on each invocation |
| Runtime A `PlanningService` / `ReadinessService` / `RecommendationService` | Hosts for `build_*` (bodies preserved) |
| Experience-diagnostics telemetry pattern | Mirrored for consumer-chain emitters |

---

## 4. Existing Components Extended

| Component | Extension |
|---|---|
| `PlanningService.build_daily_study_plan` | Observability wrapper; body → `_build_daily_study_plan_body` |
| `ReadinessService.build_readiness_intelligence` | Same pattern → `_build_readiness_intelligence_body` |
| `RecommendationService.build_study_insights` | Same pattern → `_build_study_insights_body` |
| `app/infrastructure/events/types` | `CONSUMER_CHAIN_*` event types catalogue |
| Twin architecture docs | Flag composition + EP-002.1 status |
| `.env.example` | Observability / bundling / quarantine pointers |

---

## 5. Files Created

### Application

- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/infrastructure/adapters/consumer_chain/contracts.py`
- `app/infrastructure/adapters/consumer_chain/telemetry.py`
- `app/infrastructure/adapters/consumer_chain/observer.py`
- `app/infrastructure/adapters/consumer_chain/dual_run.py`

### Tests

- `tests/infrastructure/adapters/consumer_chain/test_observability.py`
- `tests/infrastructure/adapters/consumer_chain/test_regression.py`

### Knowledge

- `knowledge/architecture/ep002_1_consumer_chain_observability/README.md`
- `knowledge/architecture/ep002_1_consumer_chain_observability/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_1_consumer_chain_observability/GAP_ANALYSIS.md`
- `knowledge/architecture/ep002_1_consumer_chain_observability/IMPLEMENTATION_PLAN.md`
- `knowledge/architecture/ep002_1_consumer_chain_observability/COMPLETION_REPORT.md` (this file)
- `knowledge/architecture/TWIN_STACK_QUARANTINE.md`

---

## 6. Files Modified

- `app/services/planning_service.py`
- `app/services/readiness_service.py`
- `app/services/recommendation_service.py`
- `app/infrastructure/events/types/__init__.py`
- `.env.example`
- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
- `knowledge/architecture/DIGITAL_TWIN_INTERFACE_SPECIFICATION.md`
- `knowledge/architecture/README.md`
- `knowledge/architecture/ep002_student_intelligence_surface/README.md`

---

## 7. Architectural Decisions

| Decision | Rationale |
|---|---|
| Wrap public `build_*`; extract `_body` helpers | Preserve business logic byte-for-byte behaviour while guaranteeing observation on every call |
| Reuse StructuredLogger + EventRegistry | Avoid second telemetry framework (milestone constraint) |
| Emit on Twin OFF as well as ON | Answers “was the API called?” with outcome `unavailable` |
| No new feature flag for observability | Always-on operational emission; zero rollout complexity; no student influence |
| Dual-run gated by Twin ON + non-prod `APP_ENV` | Optional diagnostics without production response risk; no new flag |
| Dual-run is fingerprint compare helper, not auto-wired into HTTP/`build_*` | Prevents accidental legacy side effects / cost inside insight assembly |
| Quarantine as architecture note (not code deletion) | TD-ARCH-01 is operator confusion; stacks remain inventory debt |

**Observation:** Nested Insight → Readiness → Planner calls each emit observation.  
**Conclusion:** Desired for chain visibility; nested latency is expected until EP-002.2 DI sharing.

---

## 8. Dependency Changes

**None.** No new Python packages. No Alembic / schema dependencies.

Runtime dependency direction unchanged:

```
Runtime A facts → Foundation (MS-004 / EP-001.1)
  → Planner / Readiness / Insight (EP-001.2–4)
  → build_* hosts (now observed)
```

`consumer_chain` depends on diagnostics + events + v2_flags. It does **not** own planning, readiness, or insight maths.

---

## 9. Public Surface Changes

| Surface | Change |
|---|---|
| `build_*` return values | **Unchanged** |
| HTTP routes / templates | **Unchanged** |
| Feature flags | **Unchanged** (no additions) |
| Event catalogue | Additive `CONSUMER_CHAIN_*` types |
| Diagnostic helpers | Additive: `compare_legacy_vs_build`, `diagnostic_compare_study_insights`, `is_dual_run_diagnostics_eligible` — not wired to HTTP |

**Conclusion:** No student-facing public surface change.

---

## 10. Observability Coverage Matrix

| Field | `build_daily_study_plan` | `build_readiness_intelligence` | `build_study_insights` |
|---|---|---|---|
| Service name | PlanningService | ReadinessService | RecommendationService |
| API name | ✓ | ✓ | ✓ |
| Timestamp | ✓ | ✓ | ✓ |
| Correlation / request id | ✓ (CorrelationContext) | ✓ | ✓ |
| Twin enabled | ✓ | ✓ | ✓ |
| Authority enabled | ✓ | ✓ | ✓ |
| Duration (ms) | ✓ | ✓ | ✓ |
| Outcome success | ✓ | ✓ | ✓ |
| Outcome unavailable (`None`) | ✓ | ✓ | ✓ |
| Outcome limitation (codes) | ✓ when present | ✓ | ✓ |
| Outcome exception | ✓ (re-raises) | ✓ | ✓ |
| Returned None | ✓ | ✓ | ✓ |
| Limitation codes present | ✓ | ✓ | ✓ |
| Confidence available | when payload field present | ✓ | ✓ |
| Dual-run fingerprint (optional) | via helper | via helper | dedicated helper |

Engineer questions answered:

| Question | Mechanism |
|---|---|
| Was the API called? | `consumer_chain.invoked` / `CONSUMER_CHAIN_REQUESTED` |
| How long? | `duration_ms` + `CONSUMER_CHAIN_LATENCY` |
| Succeed / fail? | `outcome` + completed/failed events |
| Returned None? | `returned_none` |
| Limitation codes? | `limitation_codes` / `limitation_codes_present` |
| Which flags? | `twin_enabled`, `authority_enabled` |

---

## 11. Feature Flag Behaviour

| Scenario | `build_*` behaviour | Observability |
|---|---|---|
| Twin OFF, Authority OFF (production default) | Returns `None` | Emits requested + completed (`unavailable`) with both flags false |
| Twin ON, Authority OFF | Assembles when Foundation available | Flags recorded; success / limitation / unavailable as appropriate |
| Twin ON, Authority ON | Same `build_*` path (Authority does not gate `build_*`) | `authority_enabled=true` recorded |
| Authority ON, Twin OFF | Authority forced OFF by `v2_flags` AND-gate | Both flags false in telemetry |

**Evidence:** Unit tests `test_authority_flag_recorded_when_both_on`, `test_authority_requires_twin`, Twin OFF regression tests.  
**Conclusion:** No new flags; existing safe-by-default posture preserved.

Dual-run eligibility:

| Twin | `APP_ENV` | Dual-run helper |
|---|---|---|
| OFF | any | Skipped (`None`) |
| ON | production / prod | Skipped |
| ON | development (etc.) | Emits `CONSUMER_CHAIN_DUAL_RUN` fingerprints |

---

## 12. Runtime Dependency Graph

```
HTTP (legacy — unchanged)
        │
        ▼
Planning / Readiness / Recommendation (legacy APIs)
        │
        │  (Twin ON only — still not HTTP-wired)
        ▼
build_*  ──observe──► StructuredLogger + EventRegistry (CONSUMER_CHAIN_*)
        │
        ▼
Foundation.assemble → planner / readiness / insight assemblers
```

**Observation:** Graph ownership unchanged from EP-001.5.  
**Conclusion:** Observability is a side channel (`influences_student=False`), not a new authority.

---

## 13. Twin Quarantine Summary

Published: [`../TWIN_STACK_QUARANTINE.md`](../TWIN_STACK_QUARANTINE.md).

| Stack | Verdict |
|---|---|
| MS-004 + EP-001.1 Foundation | **Authoritative Runtime A product path — extend** |
| ExperienceTwinAdapter | Default UX TwinPort until Authority soak |
| Epic `app/domain/twin` | Historical / domain vocabulary — not production writer |
| V2 `student_twin` | Experimental / non-authority — do not extend for EP-002 |
| EOS digital twin | Isolated Education OS — non-authority for Flask Runtime A |

**Conclusion:** TD-ARCH-01 addressed at documentation / operator level without merging or deleting stacks.

---

## 14. Documentation Changes

| Doc | Change |
|---|---|
| `TWIN_STACK_QUARANTINE.md` | New quarantine narrative |
| `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` | §12 flag table corrected; T4/T6 bundling notes; EP-002.1 status |
| `DIGITAL_TWIN_INTERFACE_SPECIFICATION.md` | Two-flag composition; Adaptive TwinInput bundled |
| Architecture README / EP-002 README | Index + status updates |
| `.env.example` | Observability + bundling + quarantine pointers |

**Conclusion:** TD-ARCH-06 closed — docs match `v2_flags.py` (Shadow + Adaptive TwinInput under Twin ON).

---

## 15. Testing Summary

### Commands executed

```bash
python3 -m pytest tests/infrastructure/adapters/consumer_chain/ \
  tests/infrastructure/adapters/adaptive_study_planner/test_unit.py \
  tests/infrastructure/adapters/readiness_intelligence/test_unit.py \
  tests/infrastructure/adapters/insight_recommendation/test_unit.py -q
```

**Outcome:** 45 passed.

Also verified consumer-chain + events catalogue inclusion via broader events suite (prior run: consumer_chain tests green after `error_message` field fix).

### Coverage classes

| Class | Tests |
|---|---|
| Unit / classification | `classify_build_result`, fingerprint stability |
| Observability | requested/completed/failed/latency emission; correlation id |
| Feature flags | Twin OFF/ON; Authority ON requires Twin |
| Dual-run | Eligible non-prod; skipped production / Twin OFF |
| Regression | Public signatures; Twin OFF → `None`; disabled telemetry still returns |

### Migration Impact

**None.** No Alembic revisions. No schema changes.

---

## 16. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Nested observation volume under Insight composition | Medium | Low | Accept for visibility; measure in EP-002.2 |
| R2 | Engineers mistake dual-run helper for HTTP cutover | Low | Medium | Docs mark `diagnostic_only` / `influences_student=False` |
| R3 | Doc drift reappears on Shadow flags | Low | Low | Quarantine + corrected tables are canonical |
| R4 | Premature cutover because “we have metrics” | Medium | High | Programme sequence: soak → dual-run → cutover still binding |

---

## 17. Technical Debt

| Item | Notes |
|---|---|
| Nested Foundation re-assemble | Still present (EP-002.2) |
| MissionOptimizer orphan | Still present (EP-002.2) |
| No HTTP callers of `build_*` | Intentional until EP-002.4+ |
| Process-default telemetry sink | Adequate for logs + tests; composition-level EventRegistry drain not required this milestone |
| Programme ID collision with Analytics EP-002 | Unchanged; directories remain separate |

**None introduced** that violates constitutional ownership.

---

## 18. Constitutional Compliance

| Rule | Status |
|---|---|
| Twin owns learner-state read model | Preserved |
| Planner owns plans | Preserved |
| Readiness owns evaluation | Preserved |
| Insight owns communication only | Preserved |
| No fourth Twin stack | Preserved (+ quarantine narrative) |
| Fail-open Twin OFF | Preserved |
| Curriculum V1/V2 traversal | N/A — untouched |
| No educational writes from Twin / observability | Preserved (`influences_student=False`) |
| No product analytics event catalogue expansion | Preserved (ops IntegrationEvents only) |

---

## 19. Architectural Delta

| Before EP-002.1 | After EP-002.1 |
|---|---|
| `build_*` callable but dark to ops | Structured invocation / latency / outcome events |
| Twin stack narrative fragmented | Quarantine note published |
| Docs claimed separate Shadow / Adaptive-input flags | Docs match bundled Twin ON behaviour |
| Dual-run for insights not available | Optional non-prod fingerprint helper |

**Not changed:** HTTP authority, algorithms, schemas, ownership boundaries, default flags.

---

## 20. Architecture Metrics

| Metric | Value |
|---|---|
| Services Extended | **3** (`PlanningService`, `ReadinessService`, `RecommendationService`) |
| New Services | **0** (observability package is infrastructure, not a domain service) |
| New Public APIs | **0** student/HTTP; additive diagnostic helpers only |
| Schema Changes | **0** |
| Feature Flags Added | **0** |
| Circular Dependencies | **0** |
| Ownership Violations | **0** |
| Parallel Implementations Introduced | **0** |
| Observability Coverage | **3 / 3** `build_*` APIs (100%) |
| Net Architectural Complexity | **Low increase** (thin observer + docs); no parallel engines |
| Overall Architectural Health | **Improved** for ops readiness; product cutover health unchanged (still pending EP-002.3–7) |

---

## 21. Recommendation for EP-002.2

**Observation:** EP-002.1 can now measure Foundation / `build_*` latency and nested call fan-out.  
**Evidence:** Programme brief WS2 depends on WS1 measurement; IF-07 nested resolve remains.  
**Conclusion:** EP-002.1 exit criteria met; foundation is ready for DI consolidation measurement.  
**Recommendation:** Execute **EP-002.2 — Shared Foundation DI + MissionOptimizer decision record** next:

1. Inject shared Foundation into planner / readiness / insight composition to cut nested re-assemble cost.  
2. Use consumer-chain latency before/after as acceptance evidence.  
3. Record explicit wire-or-retire decision for `MissionOptimizer.generate_balanced_mission`.  
4. Keep Twin / Authority production defaults OFF.  
5. Do not start HTTP insight cutover until EP-002.3 soak evidence exists.

---

## Success Criteria Checklist

| Criterion | Status |
|---|---|
| Every `build_*` API emits structured observability | ✓ |
| Existing behaviour unchanged | ✓ |
| No HTTP responses change | ✓ |
| No ownership boundaries change | ✓ |
| No duplicated observability framework | ✓ |
| Twin quarantine documentation complete | ✓ |
| Documentation matches implementation | ✓ |
| All tests pass | ✓ |

---

## Final Verdict

| Question | Answer |
|---|---|
| Milestone successful? | **Yes** |
| Student-facing change? | **No** |
| Safe to proceed to EP-002.2? | **Yes** |
| Twin Ready (T7)? | **No — not claimed** |
| HTTP cutover authorised? | **No** |
