# PRD-001 Phase D — Performance Measurements

**Budget (PRD-001 §10):** event generation / dispatch ≤ **5 ms** p95  
**Budget (PRD-001 §10):** Educational State hash overhead ≤ **20 ms** p95 on material evolution  
**Mission constraint:** snapshot observation path remains under the 5 ms dispatch budget (no Educational State payload serialisation into analytics)

## Method

Pytest harness in `tests/infrastructure/analytics/test_performance.py`:

- `test_educational_state_snapshot_dispatch_under_budget` — build + dispatch × 200 samples
- `test_educational_state_content_hash_under_budget` — SHA-256 canonical hash × 200 samples

In-process `MemoryOutboxSink`; feature flag ON for dispatch samples.

## Expected

| Path | p95 budget |
|---|---|
| Snapshot event build + dispatch | < 5 ms |
| Content hash generation | < 20 ms |

Exact local timings vary by host; CI asserts the budgets above.

## Notes

- Canonical JSON for hashing is an in-memory hashing input only — it is **not** written to the analytics store.
- Material-change gate avoids hashing-driven emits on every identical page view across requests (process-scoped last hash).
