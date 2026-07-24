# Analytics Incident Response Guide

**Programme:** EP-002

## Severity

| Sev | Example | Immediate action |
|---|---|---|
| SEV-1 | Analytics causes student-facing errors | Kill switch: set `ANALYTICS_EVENTS_V1=false`; verify educational paths healthy |
| SEV-2 | Outbox backlog / DLQ growth | Run worker; inspect dead letters; replay after fix |
| SEV-3 | Metric gap / delayed purge | Schedule retention; document backlog |

## Playbooks

### A. Educational UX degraded (unexpected)

1. Confirm whether analytics is involved (emit is fail-open — should not block UX).
2. If any doubt: **kill switch** (`ANALYTICS_EVENTS_V1=false`).
3. Capture logs matching `analytics.emit_failed` / `analytics.worker_unexpected`.
4. Do **not** drop Twin / ESS / Evidence tables.

### B. Outbox depth rising

1. `flask analytics-metrics` → check `queue_depth` / `outbox_counts`.
2. `flask analytics-worker-once` (repeat / cron).
3. If failures: inspect `last_error` on failed/dead_letter rows.
4. Fix root cause → [`REPLAY_SPECIFICATION.md`](REPLAY_SPECIFICATION.md).

### C. Database unavailable

1. Educational path continues (fail-open).
2. Events may be lost only if enqueue itself fails after educational commit — accepted residual; alert on `events_failed`.
3. Restore DB → drain pending outbox → verify with metrics.

### D. Suspected privacy incident

1. Kill switch.
2. Freeze exports.
3. Follow [`PRIVACY_OPERATIONS_GUIDE.md`](PRIVACY_OPERATIONS_GUIDE.md) + Security.
4. Audit via `flask analytics-export-audit`.

## Communications

- Founder / Engineering own kill switch.
- Privacy owns student deletion / export fulfilment SLAs (30-day delete; 14-day export in beta).
