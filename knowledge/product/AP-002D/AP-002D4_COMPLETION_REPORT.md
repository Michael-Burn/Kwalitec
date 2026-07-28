# AP-002D4 — Completion Report

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D4 — Learning Graph Projection  
**Date:** 2026-07-28  
**Status:** Complete  
**Commit message:** `feat(ap-002d4): project twin decisions into learning graph`  
**Commit:** `8653fee`

---

### Summary

Projected validated Student Digital Twin decisions into the Learning Graph as educational **relationships only**. The Graph remains a deterministic, idempotent projection of Twin belief — it performs no reasoning, stores no independent mastery authority, and introduces no educational decisions. `StudentReasoningService`, Twin semantics, Mission, Tutor, Assessment, and Evidence Packaging were not modified.

### Projection objects

| Object | Role |
|---|---|
| `ProjectionRelationshipType` | Approved relationship catalogue (LO↔Concept, Concept↔Concept, Student↔LO/Concept/Misconception, Prerequisite, Dependency) |
| `RelationshipProjection` | Immutable graph relationship with Twin decision reference |
| `GraphProjection` | Immutable projection artefact for one Twin→Graph cycle |
| `ProjectionBatch` | Ordered immutable set with duplicate-id rejection |
| `ProjectionContext` | Twin / graph / request / bundle / session / correlation / version context |
| `ProjectionReference` | Decision → observation → evidence identity chain |
| `ProjectionVersion` | Contract version `AP-002D4.projection.v1` |
| `ProjectionResult` | Context + batch + graph projection + factual events |

### Relationship types

Projected only when justified by Twin decisions (never inferred):

- `student_concept` — from mastery belief decisions
- `learning_objective_concept` / `student_learning_objective` — when LO refs present
- `student_misconception` — only from explicit misconception tags in decision payload/provenance
- `concept_concept` / `prerequisite` / `dependency` — only from explicit decision payload lists

Soft decisions (`uncertainty_preserved`, `provenance_recorded`) emit `GraphProjectionSkipped`.

### Validation

Rejects explicitly (never invents missing relationships):

- Unknown relationship types
- Broken concept references
- Missing learning objectives
- Invalid decision versions
- Duplicate projections (strict mode)
- Unsupported projection versions
- Incomplete provenance

### Versioning

- Projection contract: `AP-002D4.projection.v1`
- Accepts Twin decisions at `AP-002D3.decision.v1`
- Every relationship records Twin version + decision version + projection version
- Append-only ledger version history supports audit / replay

### Replay support

- Deterministic projection ids from twin + decision + relationship endpoints
- Identical Twin decisions → identical relationship sets
- `TwinProjectionService.replay(...)` projects into a fresh ledger for comparison
- Idempotent re-projection emits `GraphProjectionSkipped` (duplicate protection)

### Pipeline

```
EducationalDecisionSet (+ Twin)
    → RelationshipBuilder
    → ProjectionBatch
    → ProjectionValidator (fail-closed)
    → GraphProjection + GraphProjectionCreated/Updated/Skipped
    → ProjectionPersistenceService (append-only, no Alembic)
    → LearningGraphService.project_twin_decisions (optional graph update history)
    → STOP
```

### Events

Factual only (no Mission / Tutor / orchestration notifications):

- `GraphProjectionCreated`
- `GraphProjectionUpdated`
- `GraphProjectionSkipped`

### Tests

- Domain: immutability, approved types, batch duplicates, events/versioning
- Application: generation, idempotency, identical-Twin identical-Graph, replay, versioning, validation, duplicate protection, traceability, DTO mapping, persistence ledger, LearningGraphService wiring, architecture purity, StudentReasoningService untouched regression

### Deferred work for AP-002D5

- Wire projection after D3 Twin belief updates inside broader Educational Reasoning / pipeline orchestration (without modifying D4 authority boundaries inappropriately)
- Durable DB-backed projection tables if founder audit requires SQL persistence (currently append-only in-process ledger + Graph update history)
- Student-visible cutover / feature flags if Graph traversal surfaces change
- Mission adaptive assessment triggering remains AP-002E

---

### Files Created

**Domain**

- `app/domain/learning_graph/projections/__init__.py`
- `app/domain/learning_graph/projections/batch.py`
- `app/domain/learning_graph/projections/context.py`
- `app/domain/learning_graph/projections/errors.py`
- `app/domain/learning_graph/projections/events.py`
- `app/domain/learning_graph/projections/projection.py`
- `app/domain/learning_graph/projections/reference.py`
- `app/domain/learning_graph/projections/relationship.py`
- `app/domain/learning_graph/projections/relationship_type.py`
- `app/domain/learning_graph/projections/result.py`
- `app/domain/learning_graph/projections/version.py`

**Application**

- `app/application/learning_graph/projections/__init__.py`
- `app/application/learning_graph/projections/errors.py`
- `app/application/learning_graph/projections/persistence.py`
- `app/application/learning_graph/projections/relationship_builder.py`
- `app/application/learning_graph/projections/twin_projection_service.py`
- `app/application/learning_graph/projections/validator.py`
- `app/application/learning_graph/projections/versions.py`
- `app/application/learning_graph/dto/__init__.py`
- `app/application/learning_graph/dto/projection_dto.py`
- `app/application/learning_graph/mappers/__init__.py`
- `app/application/learning_graph/mappers/projection_mapper.py`

**Tests**

- `tests/application/learning_graph/conftest.py`
- `tests/application/learning_graph/test_projection_architecture_purity.py`
- `tests/application/learning_graph/test_twin_projection.py`
- `tests/domain/learning_graph/__init__.py`
- `tests/domain/learning_graph/test_projections.py`

**Docs**

- `knowledge/product/AP-002D/AP-002D4_COMPLETION_REPORT.md` (this file)

### Files Modified

- `app/application/learning_graph/__init__.py` — export projection pipeline
- `app/application/learning_graph/learning_graph_service.py` — `project_twin_decisions`
- `app/domain/learning_graph/__init__.py` — export projection domain types
- `app/domain/learning_graph/graph_update.py` — `PROJECT_FROM_TWIN_DECISIONS`

### Tests Executed

```bash
.venv/bin/python -m pytest tests/application/learning_graph tests/domain/learning_graph -q
.venv/bin/python -m pytest -q
.venv/bin/ruff check app/domain/learning_graph app/application/learning_graph \
  tests/application/learning_graph tests/domain/learning_graph
# Alembic head: 202607270013 (unchanged)
```

Outcomes: projection + Learning Graph suites passed; full suite **44290 passed**, 7 skipped; milestone paths ruff clean; single Alembic head unchanged.

Note: repository-wide `ruff check .` still reports pre-existing errors outside this milestone’s paths (same posture as AP-002D1–D3).

### Migration Impact

None.

### Architecture Compliance

Layering preserved: Twin owns learner belief; Graph owns projected relationships only. Projection services do not call Reasoning, Mission, Tutor, or Assessment. Curriculum V1/V2 traversal unaffected (N/A). Architecture purity tests forbid Mission/Tutor/Assessment/ReasoningService authority creep in the projection packages. `StudentReasoningService` remains unmodified (explicit STOP boundary).

### Technical Debt

- Projection ledger is in-process (append-only) rather than Alembic-backed tables — sufficient for deterministic replay/tests; durable SQL audit deferred.
- Concept↔concept / prerequisite / dependency edges require explicit decision payload lists; curriculum-structure sync remains the existing Learning Graph builder path.

### Known Limitations

- Does not auto-invoke projection from `StudentReasoningService` after D3 belief updates (explicit constraint — deferred wiring).
- Does not change Mission / Tutor behaviour.
- Adaptive mission triggering remains AP-002E.

### Student Impact Assessment

**N/A for this projection milestone** as a student-facing surface change (no UI). When Graph relationship projections are cut over into Mission traversal visibility, assess student value explicitly. Educational benefit intended: assessment-driven Twin belief can honestly refresh Graph relationships without inventing mastery on the Graph.

### Estimated KSI contribution

ΔKSI ≈ 0 for student-visible surfaces until cutover. Enables future K1/K8 integrity claims once Graph projections are consumed honestly.

### Evidence collected

- Projection tests under `tests/application/learning_graph/` and `tests/domain/learning_graph/`
- Full regression: 44290 passed
- Architecture purity tests in the Learning Graph projection package

### Lessons learned for student value

Keeping mastery off the Graph forces every edge to cite a Twin decision — students (and founders) can always ask “why is this relationship here?” and land on evidence, not a competing score.

### Explainability Review

N/A — no student-facing intelligence surface changes in this milestone (projection is service-level only).

### Recommendation Quality Review

N/A — recommendations are explicitly not generated or re-ranked on the D4 path.

### Version 1 readiness residual

N/A — no Version 1 production-ready declaration claimed.
