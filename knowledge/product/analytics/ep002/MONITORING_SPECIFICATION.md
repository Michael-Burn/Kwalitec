# Analytics Monitoring Specification

**Programme:** EP-002 WS2  
**Scope:** Infrastructure metrics only — **no** mastery, readiness, recommendation, or confidence scores.

## Metrics

| Metric | Meaning | Source |
|---|---|---|
| `events_received` | Dispatcher invocations (incl. disabled) | Dispatcher |
| `events_dispatched` | Successful enqueue / worker success | Dispatcher + worker |
| `events_failed` | Fail-open failures | Dispatcher + worker |
| `events_rejected` | Validation / allowlist rejects | Dispatcher |
| `events_duplicate` | Idempotent enqueue duplicates | Dispatcher |
| `events_disabled` | Flag-off no-ops | Dispatcher |
| `dispatch_latency_ms_avg` | Avg sync path latency | Dispatcher |
| `queue_depth` | `pending` + `failed` outbox rows | Worker / CLI |
| `replay_count` | Successful requeues | Replay service |
| `duplicate_count` | Duplicate suppressions (enqueue + drain) | Dispatcher + worker |
| `dead_letter_count` | Transitions to DLQ | Worker |
| `purge_deleted` | Retention deletions | Retention enforcer |
| `user_deletions` | Privacy cascade deletes | Privacy service |
| `exports_completed` | Student / audit exports | Privacy service |

## Access

```bash
flask analytics-metrics
```

Returns JSON snapshot including `feature_flag_enabled` and SQL `outbox_counts` when DB is available.

## Suggested alerts (staging / production)

| Alert | Condition | Action |
|---|---|---|
| Outbox lag | `queue_depth` > threshold for > 5 min | Run worker; check DB |
| DLQ growth | `dead_letter_count` delta > 0 sustained | Investigate + replay |
| Emit failures | `events_failed` rate spike | Check logs; kill switch if UX impacted |
| Retention overdue | No `analytics.purge_run` audit in 48h | Run retention |

## Non-goals

- Educational outcome dashboards (EP-001 WS7).
- Client RUM / third-party analytics SDKs.
