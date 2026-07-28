# AP-002D5 — Completion Report

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D5 — Mission Engine Integration  
**Date:** 2026-07-28  
**Status:** Complete  
**Commit message:** `feat(ap-002d5): integrate mission engine with twin decisions`

---

### Summary

Integrated validated Student Digital Twin decisions into the Mission Engine as **planning only**. `MissionPlanningService` consumes `EducationalDecisionSet` + Twin belief (and optional Learning Graph recovery structure), generates deterministic mission candidates using existing Adaptive Mission prioritisation scoring, validates fail-closed, and emits factual planning events. The Mission Engine never reasons, never interprets assessment evidence, and never estimates mastery independently. Assessment, Evidence Packaging, StudentReasoningService, Twin semantics, Learning Graph, and Tutor were not modified.

### Mission integration points

| Integration | Role |
|---|---|
| `MissionPlanningService.plan(...)` | Primary Twin→Mission planning pipeline |
| `MissionPlanningService.replay(...)` | Deterministic replay into a fresh ledger |
| `AdaptiveMissionService.plan_from_decisions(...)` | Existing mission facade orchestration entry |
| `CandidateBuilder` | Maps decisions → candidates using existing `_score_candidate` / recovery rules |
| `PlanningValidator` | Fail-closed contract / provenance / LO / duplicate checks |
| `PlanningPersistenceService` | Append-only in-process ledger (no Alembic) |
| DTOs / `map_planning_result` | Application-facing planning outcomes |

### Planning inputs

Consumed lawfully:

- Validated Twin belief (`StudentDigitalTwin`)
- `EducationalDecisionSet` (`AP-002D3.decision.v1`)
- Current curriculum position (optional constraint string)
- Existing mission request history (ledger duplicate protection)
- Learning Graph recovery paths (structure only)
- Workload constraint `available_minutes`

Not consumed:

- Assessment observations / raw responses
- Evidence bundles as authority
- Educational observations as reasoning input

### Validation

Rejects explicitly (never invents missing learner state):

- Unknown Twin versions (`twin.version < 1`)
- Invalid decision versions
- Broken learning-objective references (confidence practice)
- Unsupported planning contracts (`AP-002D5.planning.v1` only)
- Missing / incomplete provenance
- Duplicate mission requests (strict raise or idempotent skip)

### Traceability

Every candidate records:

- decision id / decision version / twin version
- evidence bundle id / educational observation ids
- reasoning request id / assessment session id / correlation id
- planning version + activity type + concept id

Plan provenance retains decision-set id, selected decision/candidate, and request context.

### Events

Factual only (no Tutor / student notifications):

- `MissionPlanningStarted`
- `MissionGenerated`
- `MissionPlanningSkipped`
- `MissionPlanningCompleted`

### Tests

- Domain: version, activity catalogue, context, batch duplicates, event kinds
- Application: generation, determinism, duplicate requests, soft-decision skip, validation, versioning, traceability, replay, DTO mapping, AdaptiveMissionService wiring, StudentReasoningService untouched regression, ranking
- Architecture purity: required structure; forbidden Assessment / Tutor / ReasoningService / Twin-write authority

### Deferred work for AP-002D6

- Wire Mission planning after D3 Twin belief + D4 Graph projection inside broader pipeline orchestration (without modifying Reasoning authority)
- Materialise `StudyMissionPlan` into persisted AdaptiveMission / student-visible daily mission cutover + feature flags
- Durable DB-backed planning audit tables if founder diagnostics require SQL persistence
- Adaptive assessment intent triggering remains **AP-002E**
- Tutor explanation of planned missions remains later Tutor integration

---

### Files Created

**Domain**

- `app/domain/mission/planning/__init__.py`
- `app/domain/mission/planning/activity_type.py`
- `app/domain/mission/planning/batch.py`
- `app/domain/mission/planning/candidate.py`
- `app/domain/mission/planning/context.py`
- `app/domain/mission/planning/errors.py`
- `app/domain/mission/planning/events.py`
- `app/domain/mission/planning/plan.py`
- `app/domain/mission/planning/reference.py`
- `app/domain/mission/planning/result.py`
- `app/domain/mission/planning/version.py`

**Application**

- `app/application/mission_engine/planning/__init__.py`
- `app/application/mission_engine/planning/candidate_builder.py`
- `app/application/mission_engine/planning/errors.py`
- `app/application/mission_engine/planning/mission_planning_service.py`
- `app/application/mission_engine/planning/persistence.py`
- `app/application/mission_engine/planning/validator.py`
- `app/application/mission_engine/planning/versions.py`
- `app/application/mission_engine/dto/planning_dto.py`
- `app/application/mission_engine/mappers/__init__.py`
- `app/application/mission_engine/mappers/planning_mapper.py`

**Tests**

- `tests/domain/mission/__init__.py`
- `tests/domain/mission/test_planning.py`
- `tests/application/mission_engine/conftest_planning.py`
- `tests/application/mission_engine/test_twin_planning.py`
- `tests/application/mission_engine/test_planning_architecture_purity.py`

**Docs**

- `knowledge/product/AP-002D/AP-002D5_COMPLETION_REPORT.md` (this file)

### Files Modified

- `app/application/adaptive_mission/adaptive_mission_service.py` — `plan_from_decisions` + planning service wiring
- `app/application/mission_engine/__init__.py` — export planning API
- `app/application/mission_engine/dto/__init__.py` — export planning DTOs

### Tests Executed

```bash
.venv/bin/python -m pytest tests/domain/mission tests/application/mission_engine/test_twin_planning.py \
  tests/application/mission_engine/test_planning_architecture_purity.py -q
.venv/bin/python -m pytest -q
.venv/bin/ruff check app/domain/mission/planning app/application/mission_engine/planning \
  app/application/mission_engine/dto app/application/mission_engine/mappers \
  app/application/adaptive_mission tests/domain/mission \
  tests/application/mission_engine/test_twin_planning.py \
  tests/application/mission_engine/test_planning_architecture_purity.py \
  tests/application/mission_engine/conftest_planning.py
# Alembic head: 202607270013 (unchanged)
```

Outcomes: planning suites passed; full suite **44331 passed**, 7 skipped; milestone paths ruff clean; single Alembic head unchanged.

Note: repository-wide `ruff check .` may still report pre-existing errors outside this milestone’s paths (same posture as AP-002D1–D4).

### Migration Impact

None.

### Architecture Compliance

Layering preserved: Twin owns learner belief; Mission Engine owns scheduling/planning only. Planning services do not call Reasoning, Assessment, Tutor, or write Twin inferences. Curriculum V1/V2 traversal unaffected (N/A). Architecture purity tests forbid Assessment/Tutor/ReasoningService authority creep in planning packages. `StudentReasoningService` remains unmodified (explicit STOP boundary).

### Technical Debt

- Planning ledger is in-process (append-only) rather than Alembic-backed tables — sufficient for deterministic replay/tests; durable SQL audit deferred.
- CandidateBuilder reuses Adaptive Mission private scoring helpers (`_score_candidate`, `_recovery_for`) to avoid new heuristics; consider promoting those helpers to public planning utilities later.

### Known Limitations

- Does not auto-invoke planning from `StudentReasoningService` after D3 belief updates (explicit constraint — deferred wiring).
- Does not change student-visible daily mission persistence / UI.
- Adaptive assessment triggering remains AP-002E.

### Student Impact Assessment

**N/A for this planning milestone** as a student-facing surface change (no UI). When `StudyMissionPlan` is cut over into AdaptiveMission generation visibility, assess student value explicitly. Educational benefit intended: assessment-driven Twin decisions can honestly schedule “what next” without the Mission Engine re-scoring knowledge.

### Estimated KSI contribution

ΔKSI ≈ 0 for student-visible surfaces until cutover. Enables future K2/K8 integrity claims once planning is the sole mission consumer of Twin decisions.

### Evidence collected

- Planning tests under `tests/application/mission_engine/` and `tests/domain/mission/`
- Full regression: 44331 passed
- Architecture purity tests in the Mission planning package

### Lessons learned for student value

Keeping “what do you know?” off the Mission Engine forces every planned activity to cite a Twin decision — students can always ask “why this mission?” and land on reasoned belief, not a competing score.

### Explainability Review

N/A — no student-facing intelligence surface changes in this milestone (planning is service-level only).

### Recommendation Quality Review

N/A — recommendations are not generated or re-ranked on the D5 path; existing Adaptive Mission prioritisation scoring is reused without new educational heuristics.

### Version 1 readiness residual

N/A — no Version 1 production-ready declaration claimed.
