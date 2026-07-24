# PRD-001 Phase E — Performance

**Budget:** Dispatch overhead &lt; 5 ms p95 (in-process outbox). Twin `snapshot_hash` &lt; 20 ms p95.

## Measured path

Builders (`journey.progressed` / `twin.evolved`) → `AnalyticsEventDispatcher.dispatch` → MemoryOutbox enqueue.

Twin hash path: `compute_twin_snapshot_hash(encoded_codec_json)` at Twin persist authority (not in analytics package).

## Harness

`tests/infrastructure/analytics/test_performance.py`

- `test_journey_and_twin_event_dispatch_under_budget`
- `test_twin_snapshot_hash_under_budget`

## Notes

- Feature flag OFF path remains a pure no-op (Phase A harness).
- No synchronous analytics writes outside the analytics outbox contract.
- Twin educational algorithms and Journey progression math are unchanged; observe hooks are fail-open and after successful persist/save contract points.
