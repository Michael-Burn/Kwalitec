# Analytics Recovery Guide

**Programme:** EP-002 WS3

## Scenarios

### 1. Normal shutdown / restart

Pending outbox rows are durable in SQL. On restart:

1. Start app (flag may stay OFF).
2. Run `flask analytics-worker-once` until queue empty.
3. Verify with `flask analytics-metrics`.

No educational recovery steps required.

### 2. Worker interruption mid-claim

Rows may remain `processing`. Recovery:

```bash
# Prefer targeted requeue by outbox_id once identified, or SQL:
# UPDATE analytics_outbox SET status='pending' WHERE status='processing'
# AND updated_at < now() - interval '15 minutes';
flask analytics-replay --outbox-id <id> --drain
```

Memory path (tests): `outbox.requeue(outbox_id)`.

### 3. Outbox corruption

Corrupt `payload_json` → worker dead-letters after max attempts.

1. Export / inspect row.
2. Repair JSON to valid envelope.
3. Replay per Replay Specification.

### 4. Feature flag transitions

| Transition | Effect |
|---|---|
| OFF → ON | New emits enqueue; prior educational history is not backfilled |
| ON → OFF | New emits no-op; outbox drain may continue |
| Kill switch | Immediate disable without deploy |

### 5. Database unavailable

Enqueue fails → `DispatchStatus.FAILED` (logged). Educational commit already succeeded. After DB recovery, new emits resume when flag ON; lost in-flight enqueues are not reconstructed (accepted residual mitigated by alerts).

### 6. Accidental dual workers

At-least-once + idempotency keys prevent duplicate durable events. Prefer single worker or SKIP LOCKED on PostgreSQL.
