# Observability Guide — Educational Intelligence Pipeline

**Programme:** PR-001  
**Logger:** `kwalitec.educational_intelligence_pipeline`

---

## Event catalogue (operational)

| Event | When |
|---|---|
| `PipelineStarted` | Orchestrator begins a run |
| `PipelineStageStarted` | A certified stage begins |
| `PipelineStageCompleted` | A certified stage finishes successfully |
| `PipelineStageFailed` | A certified stage raises |
| `PipelineCompleted` | Full pipeline finishes successfully |
| `PipelineFailed` | Pipeline aborts after a stage failure |

Events are coordination signals. They are **not** educational artefacts.

---

## Structured fields

Each event / summary may include:

| Field | Description |
|---|---|
| `pipeline_id` | Run identity |
| `correlation_id` | Cross-system correlation |
| `student_id` | Opaque learner identity |
| `assessment_session_id` | Session identity only |
| `reasoning_request_id` | Reasoning request identity |
| `stage` | Stage token when applicable |
| `outcome` | `completed` / `failed` |
| `failure_cause` | Exception class + message (no educational payloads) |
| `duration_ms` / `execution_time_ms` | Timing |
| `stage_timing` | Per-stage milliseconds on summary |

---

## Privacy

`sanitize_log_fields` strips forbidden keys including:

`observation(s)`, `decision(s)`, `mastery`, `confidence_score`, `explanation_text`, `mission_text`, `tutor_text`, `evidence_items`, `payload`, `belief`, `answer`, `response`.

Never extend pipeline logging to dump stage artefacts.

---

## Log lines

- `pipeline_event {...}` — one line per operational event
- `pipeline_summary {...}` — end-of-run identifiers + timings

Configure log aggregation to index on `pipeline_id` and `correlation_id`.

---

## Health as observability

`GET /health/educational-intelligence` exposes registration and contract readiness without executing the educational pipeline.
