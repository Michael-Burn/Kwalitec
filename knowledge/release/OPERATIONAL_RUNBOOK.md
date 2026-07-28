# Operational Runbook — Educational Intelligence Pipeline

**Programme:** PR-001  
**Audience:** Operators / on-call engineers  
**Scope:** Operational procedures only (no educational tuning)

---

## 1. Pipeline identity

| Field | Source |
|---|---|
| Orchestrator version | `PR-001.educational_intelligence_pipeline.v1` |
| Certification programme | AP-002D7 |
| Certification status | `certified` |
| Logger name | `kwalitec.educational_intelligence_pipeline` |

---

## 2. Health probes

| Endpoint | Meaning |
|---|---|
| `GET /health/live` | Process liveness |
| `GET /health/ready` | DB + migrations readiness |
| `GET /health/educational-intelligence` | Educational Intelligence platform readiness |

Educational Intelligence checks cover:

- Contract versions
- Pipeline registration
- Projection registration
- Mission registration
- Tutor registration
- Certification status

Expect HTTP **200** with `"ready": true` before treating the platform as release-ready.

---

## 3. Executing the pipeline (application callers)

Callers that need the certified chain should use:

```python
from app.application.educational_intelligence_pipeline import (
    EducationalPipelineOrchestrator,
)

result = EducationalPipelineOrchestrator().execute(
    twin,
    evidence_bundle,
    correlation_id=correlation_id,
    reasoning_request_id=reasoning_request_id,
    persist=False,  # default: no ledger writes unless explicitly required
)
```

Do **not** re-implement stage order in routes or blueprints.

Do **not** modify `StudentReasoningService` to auto-invoke D4/D5/D6.

---

## 4. Incident triage

### PipelineFailed

1. Read `failure_cause` and `failed_stage` from logs / `PipelineExecutionResult`.
2. Confirm `/health/educational-intelligence` still reports ready.
3. Re-run the same evidence with the same `correlation_id` / `reasoning_request_id` in a non-production harness if investigating determinism.
4. Escalate stage-owner packages only (Interpretation / Decision / Twin / Projection / Mission / Tutor). Orchestration itself has no educational heuristics to “tune”.

### Health not ready

1. Inspect which check failed in the JSON payload.
2. Contract drift → compare stage `versions.py` against AP-002D7 matrix.
3. Registration failure → confirm stage modules import cleanly.
4. Certification status ≠ certified → block release.

---

## 5. Privacy rules

Operational logs may include:

- Pipeline ID, correlation ID, student ID, assessment session ID, reasoning request ID
- Stage names, timings, outcome, failure cause class/message

Operational logs must **not** include:

- Observation / decision payloads
- Mastery or confidence scores
- Mission or tutor prose
- Answer content / evidence item bodies

---

## 6. Rollback posture

PR-001 is additive. If the orchestrator path must be disabled, stop calling `EducationalPipelineOrchestrator.execute`. Certified stage services remain independently callable. No migration rollback is required for this milestone.
