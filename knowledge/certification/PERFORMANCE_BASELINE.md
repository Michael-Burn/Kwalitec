# Educational Intelligence — Performance Baseline

**Milestone:** AP-002D7  
**Date:** 2026-07-28  
**Mode:** Baseline recording only — no optimisation  

---

## Method

Measured via `EducationalIntelligencePipelineHarness` stage timers (`perf_counter`) inside:

`tests/certification/educational_intelligence/test_performance_baseline.py`

Environment: local developer machine (macOS), Python 3.14, in-process stage services with `persist=False`.

Soft CI budgets (not SLOs): pipeline &lt; 5000 ms; each stage &lt; 2000 ms.

---

## Recorded baselines (2026-07-28)

Strong-evidence pipeline sample:

| Stage | Duration (ms) |
|---|---|
| Interpretation | ~2.1 |
| Decision generation | ~0.25 |
| Twin apply | ~0.13 |
| Projection | ~0.16 |
| Mission planning | ~0.19 |
| Explanation | ~0.19 |
| **Total** | **~3.1** |

Replay sample (duplicate submission):

| Pass | Duration (ms) |
|---|---|
| First | ~0.55 |
| Second | ~0.40 |

---

## Observations

- End-to-end certified pipeline is well under soft budgets on local hardware.
- No performance regressions requiring optimisation were discovered.
- Numbers are baselines for future comparison; they are not production latency guarantees (DB persistence, Retrieval, and HTTP are out of scope for this certification harness).

---

## Follow-up (non-blocking)

- Optionally persist baseline JSON artefacts in CI for trend detection.
- Re-measure with durable ledger persistence when D4–D6 SQL audit tables are introduced.
