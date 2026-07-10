# Student Digital Twin Domain

Pure domain vocabulary for the **Student Digital Twin** in Kwalitec.

This package is **not** persistence, HTTP, UI, scoring, prediction algorithms,
recommendation logic, or service orchestration. It defines the immutable
*state objects* that represent a learner’s current exam-preparation condition.

Canonical architecture: [`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md).  
Ubiquitous language: [`UBIQUITOUS_LANGUAGE.md`](../../../UBIQUITOUS_LANGUAGE.md).

## Purpose

Establish a framework-independent representation of *who the student is
relative to a syllabus and a sitting* — Knowledge, Memory, Behaviour,
Performance, Goals, Identity, and Prediction snapshots — as one aggregate.

The Twin is Kwalitec’s **single authoritative learner-state model**. Study
plans, missions, readiness scores, and recommendations are *consequences* of
Twin state; they must not become competing learner-state stores.

This capability (2.1) delivers **state objects only**. Update pipelines,
persistence, and intelligence engines belong to later capabilities.

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

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define repositories, database models, or Alembic migrations
- Persist Twin state or Learning Evidence
- Implement Twin update / belief-revision pipelines
- Compute mastery, retention decay, readiness, or pass probability
- Produce recommendations, plans, or missions
- Expose routes, templates, or HTTP APIs

## Relationship to Learning Evidence

Learning Evidence ([`LEARNING_EVIDENCE_MODEL.md`](../../../LEARNING_EVIDENCE_MODEL.md),
[`app/domain/evidence/`](../evidence/)) is the immutable, attributable *history*
of what the student did. The Twin is the authoritative *state* derived from
that history.

```
Learning Event
      → Evidence Candidate → Learning Evidence (canonical, append-only)
            → (later) Twin update pipeline
                  → DigitalTwin domain states
```

Rules that this package respects conceptually:

1. Evidence is the only legitimate input that may change Twin beliefs.
2. Twin domains reference curriculum identity and evidence ids — they do not
   invent syllabus structure.
3. This package stores structural slots and references; it does not apply
   evidence to beliefs (Capability 2.2+).

## Relationship to the future Insight Engine

The Insight Engine (and related Prediction / Recommendation consumers) will
**read** Twin state to produce explainable insights, forecasts, and next
actions. Insights must cite Twin factors and evidence lineage; they must not
silently mutate Knowledge or bypass Twin inputs.

Prediction snapshots on `PredictionState` are *stored outputs* of later
prediction capabilities — not algorithms living inside this package.

## Extension guidelines

1. **New structural fields** — add optional fields to the relevant `*State`
   dataclass when the concept is stable across producers. Prefer tuples for
   collections and defensive copies for dict bags.
2. **New nested records** — keep them frozen dataclasses in the owning state
   module (e.g. `TopicMasteryRecord` beside `KnowledgeState`).
3. **Planning / Readiness / Motivation domains** — the full Twin architecture
   includes these domains; introduce them as additional immutable state
   modules when a later capability requires them. Do not overload existing
   states with unrelated concerns.
4. **Do not** introduce Flask, ORM, HTTP, or service types into this package.
5. **Do not** add update methods that mutate beliefs in place — prefer
   constructing a new frozen aggregate in a future update pipeline.
6. **Do not** compute mastery, decay, readiness, or recommendations here.

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
  README.md
```
