# Analytics Replay Specification

**Programme:** EP-002 WS1

## Purpose

Recover dead-letter or failed outbox rows after transient failures or payload fixes without re-emitting from educational services.

## Status model

| Status | Meaning |
|---|---|
| `pending` | Awaiting claim |
| `processing` | Claimed by a worker |
| `processed` | Appended to `analytics_events` (or duplicate suppressed) |
| `failed` | Retryable (`attempts < max_attempts`, default 5) |
| `dead_letter` | Exhausted retries — needs operator replay |

## CLI

```bash
# Requeue all dead letters (limit 100) and drain
flask analytics-replay --limit 100 --drain --reset-attempts

# Requeue without drain
flask analytics-replay --no-drain

# Specific ids
flask analytics-replay --outbox-id <hex> --outbox-id <hex>
```

## Service API

`AnalyticsReplayService.requeue_dead_letters` / `replay_and_drain`  
Metrics: `replay_count` incremented on successful requeue.

## Duplicate suppression

Replay after a successful prior append is safe: event store unique constraint on `(user_id, event_type, idempotency_key)` returns duplicate → still marks outbox `processed`.

## Operator checklist

1. Identify root cause (`last_error`).
2. Fix code / data / infra.
3. Optionally repair `payload_json` for corrupt rows.
4. Replay with `--reset-attempts` when appropriate.
5. Confirm `flask analytics-metrics` shows DLQ decline and `events_dispatched` rise.
6. Audit: structured logs `analytics.replay_requeued`.
