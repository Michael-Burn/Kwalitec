# Performance Guide — Educational Intelligence Pipeline

**Programme:** PR-001  
**Policy:** Record metrics only. Do **not** optimise educational stages in this milestone.

---

## Measured stages

| Metric field | Stage |
|---|---|
| `interpretation_ms` | Evidence interpretation |
| `decision_ms` | Decision generation |
| `twin_update_ms` | Twin update |
| `graph_projection_ms` | Learning Graph projection |
| `mission_planning_ms` | Mission planning |
| `tutor_explanation_ms` | Tutor explanation |
| `total_ms` | Full pipeline wall-clock |

Timings are also available per stage via `PipelineMetrics.stage_timings` / `to_dict()["stages"]`.

---

## Collection

Metrics are collected by `EducationalPipelineOrchestrator` through `MetricsCollector` during each `execute` call. They are returned on `PipelineExecutionResult.metrics` and summarised in operational logs.

Certification baseline timings remain documented under:

`knowledge/certification/PERFORMANCE_BASELINE.md`

---

## How to use timings

1. Compare production `total_ms` distributions against the certification baseline.
2. Attribute regressions to a stage using per-stage fields.
3. Escalate to the owning stage package — do not alter orchestrator order or invent caches that change educational outputs.
4. Treat timing as operational signal only; never use latency to change educational decisions.

---

## Non-goals

- No caching that could alter deterministic artefacts
- No parallel stage execution (order is a certification invariant)
- No threshold-based educational fallbacks
- No schema for durable metrics storage in PR-001 (in-process / logs only)
