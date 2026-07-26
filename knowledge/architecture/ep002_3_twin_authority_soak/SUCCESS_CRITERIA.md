# EP-002.3 — Success Criteria

**Milestone:** EP-002.3 — Twin & Authority Non-Production Soak

---

## Exit gates (all required)

| # | Criterion | Evidence |
|---|---|---|
| 1 | Twin successfully exercised in non-production | Soak orchestrator runs `build_*` under Twin ON; telemetry records twin_enabled=True |
| 2 | Authority successfully exercised | Matrix cell Twin ON + Authority ON routes Experience TwinPort to Foundation Authority |
| 3 | Rollback validated | Twin OFF → Authority OFF verifier `ok=True` |
| 4 | No behavioural regressions | Twin OFF `build_*` still `None`; HTTP unchanged; production defaults OFF |
| 5 | Observability captured useful operational evidence | Latency, assemble, share-hit, outcomes, limitations, exceptions aggregated |
| 6 | HTTP remains unchanged | No route / blueprint / template diffs for cutover |
| 7 | Production defaults remain OFF | `v2_flags` defaults False; no new flags |

---

## Feature flag matrix checks

| Twin env | Authority env | Resolved Twin | Resolved Authority | Pass if |
|---|---|---|---|---|
| 0 | 0 | OFF | OFF | ExperienceTwinAdapter; `build_*` unavailable |
| 0 | 1 | OFF | OFF | Same as OFF/OFF (AND rule) |
| 1 | 0 | ON | OFF | `build_*` path live; ExperienceTwinAdapter |
| 1 | 1 | ON | ON | Foundation Authority TwinPort; fail-open OK |

---

## Ownership / constitutional checks

| Check | Pass |
|---|---|
| No ownership changes | Twin / Planner / Readiness / Insight boundaries intact |
| No new Twin stack | Quarantine narrative unchanged |
| No Runtime A writes from soak | Soak modules observational only |
| No schema changes | No Alembic |
| Collector recursion invariant | `get_overall_readiness` not wrapped by intelligence |

---

## Non-claims (explicit)

- Not Twin Ready (T7)  
- Not production Authority ON  
- Not HTTP dual-run complete (EP-002.4)  
- Not student-visible guidance cutover  

---

## Proceed to EP-002.4 when

All exit gates pass **and** Completion Report recommends dual-run planning with production flags still OFF.
