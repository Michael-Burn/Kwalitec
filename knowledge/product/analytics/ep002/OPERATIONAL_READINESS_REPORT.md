# EP-002 Operational Readiness Report

**Date:** 2026-07-24  
**Programme:** EP-002 Analytics Operational Readiness  
**Verdict:** **READY FOR STAGED ACTIVATION** (flag remains OFF until staged rollout)

## Summary

EP-002 replaces development-only dispatch assumptions with production-grade durability, operational metrics, privacy workflows, reliability evidence, and runbooks. Educational authorities (Twin, Educational State, Evidence, Mission, Journey, Reflection) are unchanged. `ANALYTICS_EVENTS_V1` defaults OFF — dispatcher remains a no-op in production until an operator enables the env flag.

## Objectives

| ID | Objective | Status |
|---|---|---|
| O1 | Durable event delivery | Met — SQL outbox + worker + DLQ + replay + cleanup |
| O2 | Operational monitoring | Met — infra counters + CLI snapshot |
| O3 | Reliability & recovery | Met — reliability suite + recovery runbook |
| O4 | Privacy operations | Met — retention, delete, export, audit, consent |
| O5 | Production rollout strategy | Met — flag strategy + go-live checklist |

## Architecture (ops path)

```
emit (flag ON) → validate → sql_outbox.enqueue
                              │
                              ▼
                    analytics-worker-once
                              │
                              ▼
                    analytics_events (append-only)
                              │
                    fail → retry → dead_letter → replay
```

When the flag is OFF: emit path writes nothing; educational workflows are unaffected.

## Files created (code)

- `app/infrastructure/analytics/sqlalchemy_store.py`
- `app/infrastructure/analytics/worker.py`
- `app/infrastructure/analytics/replay.py`
- `app/infrastructure/analytics/cleanup.py`
- `app/infrastructure/analytics/privacy.py`
- `app/infrastructure/analytics/metrics.py`
- `app/infrastructure/analytics/status.py`
- `app/infrastructure/analytics/audit_log.py`
- `app/infrastructure/analytics/cli.py`
- `tests/infrastructure/analytics/test_reliability.py`
- `tests/infrastructure/analytics/test_sql_outbox_integration.py`
- `knowledge/product/analytics/ep002/*`

## Files modified (code)

- `app/infrastructure/analytics/outbox.py` — durable port + memory claim/DLQ/cleanup
- `app/infrastructure/analytics/dispatcher.py` — metrics hooks
- `app/infrastructure/analytics/repository.py` — user delete/list helpers
- `app/infrastructure/analytics/__init__.py` — EP-002 exports
- `app/__init__.py` — register analytics CLI commands

## Quality gates

| Gate | Result |
|---|---|
| No educational regressions (emit fail-open preserved) | Pass |
| Analytics removable / kill-switch without deploy code change | Pass (env flag) |
| Dispatch reliability demonstrated | Pass (see Reliability Test Report) |
| Privacy workflows verified | Pass |
| Monitoring operational | Pass (`flask analytics-metrics`) |
| Flag OFF by default | Pass |

## Migration impact

None. EP-002 reuses Phase A tables (`analytics_events`, `analytics_outbox`, `analytics_audit_log`). No Alembic revision added.

## Architecture compliance

- Analytics remains under `app/infrastructure/analytics/` (observe-only).
- Import guards unchanged and green.
- Curriculum V1/V2 traversal unaffected (N/A — no curriculum changes).
- Educational algorithms untouched.

## Technical debt

- Process-local metrics (not yet Prometheus/StatsD exporters).
- Weekly aggregate tables not yet persisted (student export returns empty `aggregates[]`).
- Worker is CLI/batch (`analytics-worker-once`); no always-on daemon scheduler shipped — ops must cron or compose a runner before flag-on traffic.
- Journey production emit still deferred (ADR-026).

## Known limitations

- Flag must stay OFF until go-live checklist is signed for the target cohort stage.
- Concurrent claim uses `FOR UPDATE SKIP LOCKED` on PostgreSQL; SQLite tests use unlocked claim.
- Consent verification encodes PRD §8 invite-only assumptions; jurisdiction expansion needs Privacy Review.

## Exit criteria

All EP-002 exit criteria met for **staged activation readiness**. Production emits remain disabled until staged rollout begins.
