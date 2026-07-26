# EP-002.3 — Twin & Authority Non-Production Soak

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.3 — Twin + Authority soak  
**Nature:** Operational validation — **no production cutover**; **no student-facing UX authority change**  
**Date:** 2026-07-26  
**Workstream:** WS3 (programme brief)

---

## Purpose

Validate operational readiness of the EP-001 intelligence backbone under controlled non-production Twin and Authority execution before any HTTP dual-run (EP-002.4).

## Artefacts

| Document | Role |
|---|---|
| [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) | Mandatory architecture discovery |
| [`SOAK_PLAN.md`](SOAK_PLAN.md) | Execution plan for Twin / Authority soak |
| [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) | Flag rollback drill procedure |
| [`SUCCESS_CRITERIA.md`](SUCCESS_CRITERIA.md) | Exit gates for this milestone |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Authoritative review document |

## Constraints (binding)

- No production cutover  
- No HTTP routing changes  
- No schema changes  
- No new feature flags  
- No new planners / readiness / recommendation engines  
- No ownership changes  
- Production defaults remain Twin OFF / Authority OFF  

## Implementation surface

Observational soak harness under `app/infrastructure/adapters/consumer_chain/` (`soak*.py`, `authority_matrix.py`), reusing EP-002.1–2 telemetry and existing Twin / Authority DI.
