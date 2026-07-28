# Deployment Validation — Educational Intelligence Platform

**Programme:** PR-001  
**Goal:** Validate operational readiness without changing educational behaviour.

---

## 1. Local validation commands

```bash
# Full suite
python -m pytest
ruff check .

# Certification + production orchestration
python -m pytest \
  tests/certification/educational_intelligence/ \
  tests/application/educational_intelligence_pipeline/ \
  -v --tb=short

# Alembic head unchanged
flask db heads
```

Expected Alembic head at PR-001: `202607270013`.

---

## 2. Health validation

```bash
curl -sS "$BASE_URL/health/live"
curl -sS "$BASE_URL/health/ready"
curl -sS "$BASE_URL/health/educational-intelligence"
```

Educational Intelligence payload must include:

- `"ready": true`
- `"certification_status": "certified"`
- `"orchestrator_version": "PR-001.educational_intelligence_pipeline.v1"`
- ok checks for contracts, pipeline, projection, mission, tutor, certification

---

## 3. Behavioural invariance checks

1. Run certification harness fixture.
2. Run the same inputs through `EducationalPipelineOrchestrator.execute`.
3. Compare fingerprints (`tests/certification/educational_intelligence/fingerprints.py`).

Identical evidence + identical correlation/reasoning IDs + identical clock → identical Observation / Decision / Twin / Projection / Mission / Explanation fingerprints.

---

## 4. Observability validation

1. Execute one pipeline run.
2. Confirm log lines for `pipeline_event` and `pipeline_summary`.
3. Confirm event sequence includes Started → Stage* → Completed (or Failed).
4. Confirm no forbidden educational keys appear in log JSON.

---

## 5. CI validation

On the release branch, confirm GitHub Actions job **Educational Intelligence Certification** is green and that **Production Gates** depends on it.

---

## 6. Sign-off

| Check | Owner | Pass? |
|---|---|---|
| Certification suite | Engineering | |
| Orchestrator parity | Engineering | |
| Health probes | Ops | |
| Privacy-safe logs | Ops / Security | |
| Docs present under `knowledge/release/` | Engineering | |

When all rows pass, the certified platform may be treated as operationally deployable under PR-001 scope.
