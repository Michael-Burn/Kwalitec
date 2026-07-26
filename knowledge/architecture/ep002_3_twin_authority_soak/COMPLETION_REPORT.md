# EP-002.3 — Completion Report

**Milestone:** EP-002.3 — Twin & Authority Non-Production Soak  
**Programme:** EP-002 — Student Intelligence Surface  
**Date:** 2026-07-26  
**Nature:** Operational validation — **no production cutover**; **no student-facing UX authority change**; **no HTTP dual-run**  
**Authoritative review document:** this file  
**Supporting artefacts:** `DISCOVERY_REPORT.md`, `SOAK_PLAN.md`, `ROLLBACK_PLAN.md`, `SUCCESS_CRITERIA.md`

Legend used throughout: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Executive Summary

EP-002.3 validates that the EP-001 intelligence backbone can be exercised under Twin ON and Authority ON in non-production, measured via EP-002.1–2 observability, and rolled back to the pre-soak fail-open posture without behavioural regressions.

**Observation:** Before this milestone, Twin / Authority pathways were implemented but lacked a dedicated consumer-chain soak harness tying `build_*` workloads to Authority routing and rollback drills.  
**Evidence:** Controlled non-prod soak exercised **450** `build_*` requests across planner / readiness / insight; Authority matrix cells A–D all passed on real Experience composition; Twin OFF → Authority OFF rollback `ok=True`; production defaults remain Twin OFF / Authority OFF; HTTP unchanged.  
**Conclusion:** Objectives met. Operational readiness for **planning** EP-002.4 Study Insights dual-run is confirmed. Production Authority ON and HTTP cutover remain **not** authorised.  
**Recommendation:** Accept EP-002.3. Proceed to **EP-002.4** dual-run (legacy remains authoritative). Keep production Twin / Authority OFF.

No schema migrations. No new feature flags. No new Twin / planner / readiness / recommendation engines. No ownership changes. No HTTP cutover.

---

## 2. Discovery Summary

Mandatory discovery reviewed EP-001.5, EP-002 programme brief, EP-002.1–2 completion reports, Twin architecture, Twin quarantine, `v2_flags.py`, consumer-chain telemetry / Foundation DI, and Experience TwinPort Authority wiring.

| Finding | Detail |
|---|---|
| Flags | Twin + Authority only; Authority requires Twin (resolver AND) |
| Exercise targets | `build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights` |
| Measurement | EP-002.1 outcomes/latency + EP-002.2 assemble / share-hit |
| Gap | No Twin+Authority consumer-chain soak orchestrator |
| Reuse | TwinRollbackVerifier, Authority port fail-open, composition DI |

Full detail: [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md).

**Conclusion:** Implementation authorised only after discovery — observational soak harness under `consumer_chain`, not a redesign.

---

## 3. Soak Plan

Executed per [`SOAK_PLAN.md`](SOAK_PLAN.md):

1. Baseline cell A (Twin OFF / Authority OFF)  
2. Twin workload cell C (Twin ON / Authority OFF)  
3. Authority workload cell D (Twin ON / Authority ON)  
4. Invalid Authority env cell B (Twin OFF / Authority env ON → resolves OFF)  
5. Rollback cell E (Twin OFF → Authority OFF)  
6. Aggregate health + report  

Workload: 10 synthetic students × 10 Insight-chain iterations (Authority OFF) + half iterations (Authority ON), plus matrix / rollback / fail-open probes. Foundation assemble vs share-hit exercised via EP-002.2 helpers (1 assemble + 2 share-hits per nested compose sample × 30).

---

## 4. Soak Results

**Observation:** Twin-enabled and Authority-enabled non-prod runs completed without exceptions or ownership violations.  
**Evidence:**

| Result | Value |
|---|---|
| Soak `ok` | **True** |
| Requests exercised | **450** |
| Exception count | **0** |
| Failure count | **0** |
| Matrix cells passed | **4 / 4** |
| Rollback success | **True** |
| Behavioural regressions | **0** |
| Ownership violations | **0** |
| Limitation codes observed | `sparse_evidence` × 150 (injected readiness fixtures) |

Authority fail-open: Foundation assemble raise → fallback summary returned (`authority_fail_open_ok`).

Real Experience composition matrix (integration tests):

| Cell | Twin env | Authority env | Resolved | TwinPort |
|---|---|---|---|---|
| A | OFF | OFF | Twin OFF / Auth OFF | ExperienceTwinAdapter |
| B | OFF | ON | Twin OFF / Auth OFF | ExperienceTwinAdapter |
| C | ON | OFF | Twin ON / Auth OFF | ExperienceTwinAdapter |
| D | ON | ON | Twin ON / Auth ON | StudentTwinFoundationAuthorityPort |

**Conclusion:** Twin and Authority pathways are operationally exercisable in non-prod with expected routing.

---

## 5. Performance Summary

Controlled soak with light artificial per-call delay to make latency distributions measurable (builders themselves are sub-millisecond without sleep).

| Metric | Value |
|---|---|
| Soak duration | **~401.5 ms** |
| Average latency | **0.756 ms** |
| P95 latency | **1.011 ms** |
| Requests | **450** |

**Observation:** Latency is dominated by soak harness timing of injected builders, not production Foundation collect cost.  
**Evidence:** EP-002.2 bench already showed nested compose ~2.8 ms with shared CLS under simulated 2 ms assemble.  
**Conclusion:** No performance blocker for dual-run planning; continue to measure live assemble cost when Twin ON in staging with real collectors.  
**Recommendation:** EP-002.4 dual-run should log side-by-side latency for legacy vs `build_study_insights` under Twin ON non-prod.

---

## 6. Foundation Metrics

Nested Planner → Readiness → Insight compose samples (30 cycles):

| Metric | Value |
|---|---|
| Foundation assembly count | **30** |
| Share-hit count | **60** |
| Share-hit rate | **0.667** (60 / 90) |

**Observation:** EP-002.2 DI sharing remains effective under soak (one assemble, two injections per compose).  
**Evidence:** `consumer_chain.foundation_assemble` records with `assembled` vs `assemble_source=injected`.  
**Conclusion:** Soak confirms assemble vs share-hit telemetry is usable operational evidence for EP-002.4.

---

## 7. Authority Validation

| Check | Result |
|---|---|
| Authority OFF / Twin OFF | ExperienceTwinAdapter; `build_*` unavailable |
| Authority env ON / Twin OFF | Authority resolves OFF (AND rule) |
| Authority OFF / Twin ON | ExperienceTwinAdapter; `build_*` path live |
| Authority ON / Twin ON | Foundation Authority TwinPort; demo seed disabled |
| Fail-open on Foundation failure | Fallback TwinPort summary returned |
| No ownership violation | Soak modules contain no Runtime A writes |

**Observation:** Authority is correctly gated and fail-open.  
**Evidence:** Integration matrix + `verify_authority_fail_open` + composition `_seed_demo` false under Authority.  
**Conclusion:** Authority soak exit criteria met for non-prod.  
**Recommendation:** Do **not** enable Authority in production until EP-002.4+ dual-run evidence and an explicit production checklist.

---

## 8. Rollback Validation

Sequence validated: soak peak (Twin ON + Authority ON) → Twin OFF → Authority OFF.

| Check | Result |
|---|---|
| Twin OFF removes Twin DI / Foundation / shadow | Pass |
| Authority auto-clears when Twin OFF | Pass |
| ExperienceTwinAdapter restored | Pass |
| Explicit Authority OFF matches pre-soak flags | Pass |
| Adaptive flags independent | Pass |
| Twin shadow rollback verifier | Pass |
| Behavioural regressions | **0** |

Procedure: [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md). Automated: `verify_twin_authority_soak_rollback()`.

**Conclusion:** Rollback returns the system to pre-soak state without behavioural regressions attributable to this soak.

---

## 9. Runtime Dependency Verification

```
Runtime A facts
  → Foundation.assemble → CanonicalLearnerState
      → build_daily_study_plan / build_readiness_intelligence / build_study_insights
      → (optional) Experience TwinPort via StudentTwinFoundationAuthorityPort
```

| Dependency check | Result |
|---|---|
| Soak → educational write | None |
| Soak → HTTP routes | None |
| Twin packages import planner/readiness/insight for authority | None (unchanged) |
| Circular imports introduced | None |
| New engines | None |
| MissionOptimizer wired | No (remains quarantined) |

---

## 10. Feature Flag Matrix

| Twin env | Authority env | Resolved Twin | Resolved Authority | TwinPort | `build_*` |
|---|---|---|---|---|---|
| 0 | 0 | OFF | OFF | ExperienceTwinAdapter | Unavailable (`None`) |
| 0 | 1 | OFF | OFF | ExperienceTwinAdapter | Unavailable |
| 1 | 0 | ON | OFF | ExperienceTwinAdapter | Exercised |
| 1 | 1 | ON | ON | Foundation Authority | Exercised |

Production defaults (`resolve_v2_feature_flags(environ={})`): both **OFF**.  
No new flags added (no `ENABLE_CONSUMER_CHAIN_SOAK`).

---

## 11. Observability Findings

| Signal | Finding |
|---|---|
| `build_*` outcomes | Success / limitation / unavailable classified; exceptions = 0 |
| Flag snapshot | Twin / Authority recorded on soak completed events |
| Foundation assemble | Assembled vs injected distinguishable |
| Limitation frequency | Fixture `sparse_evidence` counted correctly |
| Soak events | `CONSUMER_CHAIN_SOAK_*` catalogue extended |
| Influence marker | All soak / chain events `influences_student=False` |

**Observation:** EP-002.1–2 telemetry is sufficient for soak ops evidence.  
**Conclusion:** TD-OPS-01 class gap for Twin/Authority soak is closed for non-prod harness scope.

---

## 12. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Operators treat soak green as production Authority go | Medium | High | Explicit non-claim; production defaults OFF |
| R2 | Staging Twin ON with sparse data floods limitation codes | Medium | Low | Expected honesty; monitor codes, do not invent scores |
| R3 | EP-002.4 dual-run accidentally flips HTTP authority | Medium | High | Dual-run must keep legacy authoritative |
| R4 | Controlled soak latency understates collector cost | Low | Medium | Measure real assemble in staging before cutover |
| R5 | MissionOptimizer accidentally rewired during dual-run | Low | High | Remains quarantined (EP-002.2) |

---

## 13. Technical Debt

| Item | Notes |
|---|---|
| Live staging soak window with real learner evidence | Harness delivered; operator-run staging window still valuable |
| HTTP still legacy-authoritative | Intentional until EP-002.4–5 |
| Dual presentation (Insight vs EducationalExplainability) | EP-002.8 |
| MissionOptimizer soft-deprecated code remains | EP-002.7 / WS8 |
| Soak not wired into Experience composition DI | Optional; callable from tests/ops — intentional (no HTTP) |

**None introduced** that violates constitutional ownership.

---

## 14. Constitutional Compliance

| Rule | Status |
|---|---|
| Twin owns learner-state read model | Preserved |
| Planner owns plans | Preserved |
| Readiness owns evaluation | Preserved |
| Insight owns communication only | Preserved |
| No fourth Twin stack | Preserved |
| Fail-open Twin OFF / Authority OFF | Preserved + drilled |
| Collector recursion invariant | Preserved |
| Curriculum V1/V2 traversal | N/A — untouched |
| No production cutover / HTTP / schema / new flags | Preserved |
| Twin Ready (T7) claimed | **No** |

---

## 15. Architectural Delta

| Before EP-002.3 | After EP-002.3 |
|---|---|
| Twin/Authority pathways unsoaked as a consumer-chain unit | Observational soak orchestrator + matrix + rollback |
| Rollback covered Twin DI (T6) primarily | Twin OFF → Authority OFF pre-soak drill |
| Assemble/share-hit measurable but not soak-aggregated | Soak health aggregates latency, assemble, share-hit, outcomes |
| EP-002.4 blocked on soak evidence | Soak exit criteria green for dual-run **planning** |

**Not changed:** HTTP authority, educational algorithms, schemas, ownership boundaries, default flags, MissionOptimizer quarantine.

---

## 16. Architecture Metrics

| Metric | Value |
|---|---|
| Soak Duration | **~401.5 ms** (controlled 450-request soak + matrix + rollback) |
| Requests Exercised | **450** |
| Average Latency | **0.756 ms** |
| P95 Latency | **1.011 ms** |
| Foundation Assembly Count | **30** |
| Share-Hit Rate | **66.7%** |
| Rollback Success | **True** |
| Ownership Violations | **0** |
| Behavioural Regressions | **0** |
| Overall Operational Readiness | **Ready for EP-002.4 dual-run planning; not ready for production Authority or HTTP cutover** |

---

## 17. Recommendation for EP-002.4

**Observation:** Consumer chain is observable (EP-002.1), cheaper to compose (EP-002.2), and Twin/Authority pathways are soak-validated in non-prod (EP-002.3).  
**Evidence:** Matrix 4/4; rollback ok; 450 requests / 0 exceptions; production defaults OFF; HTTP unchanged.  
**Conclusion:** Safe to begin **Study Insights dual-run** with legacy `generate_recommendations` remaining authoritative.  
**Recommendation:**

1. Implement EP-002.4 dual-run on dashboard / home (log compare only; no UX flip).  
2. Keep Twin ON only in non-prod / gated cohorts for observation.  
3. Keep Authority OFF in production; optional non-prod Authority ON behind ops checklist.  
4. Kill switch remains Twin OFF → Authority OFF.  
5. Do not declare Twin Ready (T7).  
6. Do not wire MissionOptimizer.

---

## Files Created

### Application

- `app/infrastructure/adapters/consumer_chain/soak_contracts.py`
- `app/infrastructure/adapters/consumer_chain/soak_health.py`
- `app/infrastructure/adapters/consumer_chain/soak_telemetry.py`
- `app/infrastructure/adapters/consumer_chain/authority_matrix.py`
- `app/infrastructure/adapters/consumer_chain/soak_rollback.py`
- `app/infrastructure/adapters/consumer_chain/soak.py`

### Tests

- `tests/infrastructure/adapters/consumer_chain/test_twin_authority_soak.py`
- `tests/infrastructure/adapters/consumer_chain/test_twin_authority_soak_integration.py`
- `tests/infrastructure/adapters/consumer_chain/test_soak_regression.py`

### Knowledge

- `knowledge/architecture/ep002_3_twin_authority_soak/README.md`
- `knowledge/architecture/ep002_3_twin_authority_soak/DISCOVERY_REPORT.md`
- `knowledge/architecture/ep002_3_twin_authority_soak/SOAK_PLAN.md`
- `knowledge/architecture/ep002_3_twin_authority_soak/ROLLBACK_PLAN.md`
- `knowledge/architecture/ep002_3_twin_authority_soak/SUCCESS_CRITERIA.md`
- `knowledge/architecture/ep002_3_twin_authority_soak/COMPLETION_REPORT.md` (this file)

---

## Files Modified

- `app/infrastructure/adapters/consumer_chain/__init__.py`
- `app/infrastructure/events/types/__init__.py`
- `.env.example`
- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
- `knowledge/architecture/TWIN_STACK_QUARANTINE.md`
- `knowledge/architecture/ep002_student_intelligence_surface/README.md`

---

## Tests Executed

```bash
python3 -m pytest \
  tests/infrastructure/adapters/consumer_chain/test_twin_authority_soak.py \
  tests/infrastructure/adapters/consumer_chain/test_twin_authority_soak_integration.py \
  tests/infrastructure/adapters/consumer_chain/test_soak_regression.py \
  tests/infrastructure/adapters/consumer_chain/test_regression.py \
  -v
```

**Outcome:** 20 passed.

```bash
ruff check app/infrastructure/adapters/consumer_chain/ \
  app/infrastructure/events/types/__init__.py \
  tests/infrastructure/adapters/consumer_chain/test_twin_authority_soak*.py \
  tests/infrastructure/adapters/consumer_chain/test_soak_regression.py
```

**Outcome:** Clean after fixes.

---

## Migration Impact

**None.** No Alembic revisions. No schema changes.

---

## Success Criteria Checklist

| Criterion | Status |
|---|---|
| Twin successfully exercised in non-production | ✓ |
| Authority successfully exercised | ✓ |
| Rollback validated | ✓ |
| No behavioural regressions | ✓ |
| Observability captured useful operational evidence | ✓ |
| HTTP remains unchanged | ✓ |
| Production defaults remain OFF | ✓ |

---

## Final Verdict

| Question | Answer |
|---|---|
| Milestone successful? | **Yes** |
| Student-facing change? | **No** |
| Safe to proceed to EP-002.4 dual-run planning? | **Yes** |
| Production Authority ON? | **No** |
| HTTP cutover authorised? | **No** |
| Twin Ready (T7)? | **No — not claimed** |
