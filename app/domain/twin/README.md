# Student Digital Twin Domain

Pure domain vocabulary for the **Student Digital Twin** in Kwalitec, plus the
**Twin Update Pipeline** orchestration framework.

This package is **not** persistence, HTTP, UI, educational scoring algorithms,
recommendation logic, or service-layer orchestration. It defines:

1. Immutable *state objects* that represent a learner’s current exam-preparation
   condition.
2. A registry-backed *update pipeline* that coordinates future update strategies
   without implementing educational belief revision.

Canonical architecture: [`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md).  
Ubiquitous language: [`UBIQUITOUS_LANGUAGE.md`](../../../UBIQUITOUS_LANGUAGE.md).

## Purpose

Establish a framework-independent representation of *who the student is
relative to a syllabus and a sitting* — Knowledge, Memory, Behaviour,
Performance, Goals, Identity, and Prediction snapshots — as one aggregate.

Provide the orchestration mechanism that applies Learning Evidence to that
aggregate via registered **Update Strategies**, producing a new immutable Twin
snapshot.

The Twin is Kwalitec’s **single authoritative learner-state model**. Study
plans, missions, readiness scores, and recommendations are *consequences* of
Twin state; they must not become competing learner-state stores.

Capability 2.1 delivered **state objects**. Capability 2.2 delivers the
**update orchestration framework only** — no Knowledge / Memory / Behaviour /
Performance / Prediction algorithms.

## Responsibilities

| Module | Responsibility |
|---|---|
| `identity_state.py` | Who the learner is (student, curriculum, exam, sitting) |
| `goal_state.py` | Pass ambition, completion date, planned weekly hours |
| `knowledge_state.py` | Structural topic-mastery slots and evidence references |
| `memory_state.py` | Structural retention slots and revision references |
| `behaviour_state.py` | Consistency metrics and session / pattern references |
| `performance_state.py` | Assessment references and performance summaries |
| `prediction_state.py` | Stored readiness / pass-probability snapshots |
| `digital_twin.py` | Immutable aggregate composing the domains above |
| `update_context.py` | Immutable context (Twin + evidence + metadata) |
| `update_result.py` | Pipeline outcome (original / updated Twin, messages) |
| `update_strategy.py` | Public strategy contract alias |
| `strategies/base_strategy.py` | Abstract update strategy interface |
| `update_pipeline.py` | Registry coordinator that invokes applicable strategies |

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define repositories, database models, or Alembic migrations
- Persist Twin state or Learning Evidence
- Implement Knowledge / Memory / Behaviour / Performance / Prediction algorithms
- Produce recommendations, plans, or missions
- Expose routes, templates, or HTTP APIs

## Update lifecycle

```
Learning Evidence (one or more)
      │
      ▼
UpdateContext  (current Twin + evidence + metadata)  — immutable
      │
      ▼
TwinUpdatePipeline
      │  discover registered strategies (registration order)
      │  for each strategy where supports(context):
      │       updated Twin ← strategy.apply(context)
      │       context ← context.with_twin(updated Twin)
      ▼
UpdateResult
      ├── original_twin
      ├── updated_twin          (new snapshot; may equal original)
      ├── applied_strategies
      ├── processing_messages
      └── success
```

1. Receive a `DigitalTwin` and one or more `LearningEvidence` records.
2. Build an immutable `UpdateContext`.
3. If **no strategies are registered**, return an `UpdateResult` whose
   `updated_twin` is the original Twin, with processing messages explaining
   the no-op (`success=True`).
4. Otherwise, invoke every registered strategy that reports
   `supports(context)`, in registration order.
5. Each strategy returns a **new** Twin; the pipeline never mutates the
   original aggregate in place.
6. Return `UpdateResult` describing what ran.

## Relationship to Learning Evidence

Learning Evidence ([`LEARNING_EVIDENCE_MODEL.md`](../../../LEARNING_EVIDENCE_MODEL.md),
[`app/domain/evidence/`](../evidence/)) is the immutable, attributable *history*
of what the student did. The Twin is the authoritative *state* derived from
that history.

```
Learning Event
      → Evidence Candidate → Learning Evidence (canonical, append-only)
            → Twin Update Pipeline (this package)
                  → DigitalTwin domain states (new snapshot)
```

Rules:

1. Evidence is the only legitimate input that may change Twin beliefs.
2. Twin domains reference curriculum identity and evidence ids — they do not
   invent syllabus structure.
3. The pipeline coordinates strategy application; specialised strategies (later
   capabilities) own belief revision.

## Relationship to the Student Digital Twin

`DigitalTwin` remains a frozen aggregate of domain states. It exposes **no**
in-place update methods. Evolution happens only by constructing a new Twin
through the Update Pipeline (or by explicit `DigitalTwin.create` composition
in tests / bootstrap).

## Future Update Strategies

Registered later (Capability 2.3+); **not** implemented here:

| Strategy | Intended concern |
|---|---|
| `KnowledgeUpdateStrategy` | Mastery / belief revision from knowledge evidence |
| `MemoryUpdateStrategy` | Retention / decay / revision signals |
| `BehaviourUpdateStrategy` | Consistency, skips, session patterns |
| `PerformanceUpdateStrategy` | Assessment and mock outcomes |
| `PredictionSnapshotStrategy` | Store readiness / pass-probability snapshots |

Each inherits `BaseUpdateStrategy`, implements `supports` / `apply`, and is
registered with `TwinUpdatePipeline` without modifying the pipeline class.

## Relationship to the future Insight Engine

The Insight Engine (and related Prediction / Recommendation consumers) will
**read** Twin state to produce explainable insights, forecasts, and next
actions. Insights must cite Twin factors and evidence lineage; they must not
silently mutate Knowledge or bypass Twin inputs.

The Update Pipeline **writes** new Twin snapshots from evidence. The Insight
Engine **reads** those snapshots. They must not be conflated.

## Extension guidelines

1. **New structural fields** — add optional fields to the relevant `*State`
   dataclass when the concept is stable across producers. Prefer tuples for
   collections and defensive copies for dict bags.
2. **New nested records** — keep them frozen dataclasses in the owning state
   module (e.g. `TopicMasteryRecord` beside `KnowledgeState`).
3. **New update strategies** — subclass `BaseUpdateStrategy` under
   `strategies/`, register with the pipeline; do not put educational math in
   `update_pipeline.py`.
4. **Planning / Readiness / Motivation domains** — introduce as additional
   immutable state modules when a later capability requires them.
5. **Do not** introduce Flask, ORM, HTTP, or service types into this package.
6. **Do not** mutate Twin aggregates in place — always return a new frozen
   snapshot from `apply`.

## Package layout

```
app/domain/twin/
  __init__.py
  digital_twin.py
  identity_state.py
  goal_state.py
  knowledge_state.py
  memory_state.py
  behaviour_state.py
  performance_state.py
  prediction_state.py
  update_context.py
  update_result.py
  update_strategy.py
  update_pipeline.py
  strategies/
    __init__.py
    base_strategy.py
  README.md
```
