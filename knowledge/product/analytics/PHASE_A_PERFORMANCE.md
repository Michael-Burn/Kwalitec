# PRD-001 Phase A — Performance Measurements

**Date:** 2026-07-24  
**Budget (PRD-001 §10):** event generation / dispatch ≤ **5 ms** p95  
**Harness:** in-process `AnalyticsEventDispatcher` + `MemoryOutboxSink`  
**Host:** local developer machine (Darwin), Python 3.14  
**Sample size:** 500 dispatches per mode

## Results

| Mode | n | mean (ms) | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | Budget |
|---|---:|---:|---:|---:|---:|---:|---|
| Flag **OFF** (no-op) | 500 | 0.0001 | 0.0001 | 0.0004 | 0.0007 | 0.0021 | Pass |
| Flag **ON** (memory outbox) | 500 | 0.034 | 0.0326 | 0.050 | 0.074 | 0.200 | Pass |

Both modes are **well under** the 5 ms p95 budget.

## Notes

- Flag OFF path performs only the feature-flag gate — confirms zero educational overhead when disabled (production default).
- Flag ON path includes validate + serialize + memory enqueue; durable SQL outbox latency is **not** measured here (no production emits in Phase A).
- Staging PROFILE against PostgreSQL outbox enqueue remains a follow-up before enabling the flag beyond dogfood.

## Automated gate

`tests/infrastructure/analytics/test_performance.py` asserts p95 &lt; 5 ms for both modes (n=200).
