# Analytics Production / Operational Runbook

**Programme:** EP-002  
**Flag:** `ANALYTICS_EVENTS_V1` (default **OFF**)

## Daily / periodic operations

| Cadence | Command | Purpose |
|---|---|---|
| Continuous / cron | `flask analytics-worker-once` | Drain outbox → event store |
| Daily | `flask analytics-retention --dry-run` then `--execute` | Enforce 18-month raw retention + outbox cleanup |
| On demand | `flask analytics-metrics` | Queue depth + counters |
| On demand | `flask analytics-replay` | Requeue dead letters |

## Composition

- **Outbox:** `SqlOutboxSink` (`analytics_outbox`)
- **Store:** `SqlAnalyticsEventStore` (`analytics_events`)
- **Audit:** `SqlAnalyticsAuditLog` (`analytics_audit_log`)
- **Worker:** `AnalyticsOutboxWorker` (at-least-once; idempotent append)

## Enable / disable (no deploy)

```bash
# Enable (staged environments only after checklist)
export ANALYTICS_EVENTS_V1=true

# Kill switch / rollback
unset ANALYTICS_EVENTS_V1
# or
export ANALYTICS_EVENTS_V1=false
```

Restart app processes after env change so workers/web pick up the flag. Pending outbox rows remain durable and can be drained with the flag off.

## Safety invariants

1. Educational transactions never roll back because analytics failed.
2. Analytics never writes Twin / ESS / Evidence / mission tables.
3. Payload policy: metadata + hashes only (no reflection body, no exam PII).
4. Student deletion cascades analytics tables only (`analytics-delete-user`).

## Related guides

- [`INCIDENT_RESPONSE.md`](INCIDENT_RESPONSE.md)
- [`REPLAY_SPECIFICATION.md`](REPLAY_SPECIFICATION.md)
- [`RECOVERY_GUIDE.md`](RECOVERY_GUIDE.md)
- [`MONITORING_SPECIFICATION.md`](MONITORING_SPECIFICATION.md)
- [`PRIVACY_OPERATIONS_GUIDE.md`](PRIVACY_OPERATIONS_GUIDE.md)
- [`FEATURE_FLAG_STRATEGY.md`](FEATURE_FLAG_STRATEGY.md)
