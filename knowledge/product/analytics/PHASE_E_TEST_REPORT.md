# PRD-001 Phase E — Test Report

**Date:** 2026-07-24  
**Scope:** Unit, integration, performance, architecture guards for Journey + Twin observation

## Commands

```bash
python -m pytest \
  tests/infrastructure/analytics/test_twin_events.py \
  tests/infrastructure/analytics/test_twin_integration.py \
  tests/infrastructure/analytics/test_journey_events.py \
  tests/infrastructure/analytics/test_journey_integration.py \
  tests/infrastructure/analytics/test_contracts_registry_validator.py \
  tests/infrastructure/analytics/test_performance.py \
  tests/architecture/test_analytics_import_guard.py \
  tests/infrastructure/analytics/test_session_integration.py \
  tests/infrastructure/analytics/test_reflection_integration.py \
  tests/infrastructure/analytics/test_educational_state_integration.py \
  -q
```

## Coverage

| Area | Result |
|---|---|
| Twin event construction / validation / serialization | Pass |
| Twin snapshot_hash determinism | Pass |
| Twin persist integration (flag ON / OFF / fail-open) | Pass |
| Journey event construction / validation / serialization | Pass |
| Journey post-save observe contract (flag ON / OFF / fail-open) | Pass |
| Registry Phase E allowlist | Pass |
| Dispatch p95 budget (< 5 ms) | Pass |
| Twin hash p95 budget (< 20 ms) | Pass |
| Architecture import guard | Pass |
| Session / Reflection / ESS regression integration | Pass (unchanged behaviour) |

## Negative cases

- Invalid `snapshot_hash` / `evolution_reason` / `transition_id` rejected at build time
- Feature flag OFF → `DISABLED`, no outbox writes
- Analytics validation failure → Twin persist / Journey observe still succeed
- Non-numeric student/learner ids skip emit
