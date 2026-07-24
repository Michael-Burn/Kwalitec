# PRD-001 Phase B — Performance Measurements

**Date:** 2026-07-24  
**Budget (PRD-001 §10):** event generation / dispatch ≤ **5 ms** p95  
**Harness:** in-process `AnalyticsEventDispatcher` + `MemoryOutboxSink` + Phase B registry  
**Host:** local developer machine (Darwin), Python 3.14  
**Sample size:** 500 dispatches per mode

## Results

| Mode | n | mean (ms) | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | Budget |
|---|---:|---:|---:|---:|---:|---:|---|
| Flag **OFF** (`session.started`) | 500 | 0.0001 | 0.0001 | 0.0001 | 0.0002 | 0.0017 | Pass |
| Flag **ON** (`session.started`) | 500 | 0.0338 | 0.0329 | 0.0479 | 0.0594 | 0.2490 | Pass |
| Flag **ON** (`session.completed`) | 500 | 0.0342 | 0.0334 | 0.0481 | 0.0645 | 0.1925 | Pass |
| Flag **ON** (abandoned) | 500 | 0.0341 | 0.0338 | 0.0480 | 0.0505 | 0.2123 | Pass |

All modes are **well under** the 5 ms p95 budget.

## Notes

- Flag OFF path remains a pure no-op gate — zero educational overhead at production default.
- No additional synchronous educational DB writes; analytics uses the approved outbox contract only when the flag is on.
- Automated gate: `tests/infrastructure/analytics/test_performance.py` (`test_session_event_dispatch_under_budget`).
