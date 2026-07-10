# Evidence Extraction Engine

Pure domain vocabulary and framework for **Evidence Candidates** in Kwalitec.

This package is **not** persistence, HTTP, UI, scoring, or Twin mutation. It
answers only: *what evidence exists inside this Learning Event?*

## Purpose

Convert a [`LearningEvent`](../learning_events/learning_event.py) into zero or
more immutable [`EvidenceCandidate`](evidence_candidate.py) objects.

Extraction identifies *possible* learning evidence. Downstream capabilities
validate, store, quality-weight, and apply evidence to the Student Digital Twin.
Those concerns are intentionally out of scope here.

## Responsibilities

| Module | Responsibility |
|---|---|
| `evidence_category.py` | Evidence category and qualitative confidence enumerations |
| `evidence_candidate.py` | Immutable candidate evidence object |
| `extractors/base_extractor.py` | Abstract extractor strategy interface |
| `evidence_extractor.py` | Registry coordinator that invokes supporting extractors |

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define repositories, database models, or Alembic migrations
- Persist evidence or Learning Events
- Assign numerical weights, mastery scores, or readiness scores
- Update the Student Digital Twin
- Expose routes, templates, or HTTP APIs
- Implement specialised extractors (QuestionAttempt, Mission, …) yet

## Relationship to Learning Events

Learning Events (Capability 1.1) are the named *moments* in the learning
journey. The Evidence Extraction Engine inspects an event and emits candidates
describing what kinds of evidence that moment contains.

- One event may yield **zero, one, or many** candidates (e.g. a completed quiz
  may produce Performance and Time candidates).
- Events are inputs; candidates are outputs. Neither is Twin state.

## Relationship to Learning Evidence

Per [`LEARNING_EVIDENCE_MODEL.md`](../../../LEARNING_EVIDENCE_MODEL.md):

- An Evidence Candidate is a **proposal** that evidence exists — not yet the
  immutable, stored Learning Evidence record.
- Categories organise the catalogue (Knowledge, Performance, Behaviour, …).
- Confidence on a candidate is **qualitative only** (High / Medium / Low /
  Unknown); numerical weighting belongs to later Twin-update logic.
- Provenance and topic references support attribution and curriculum identity.

Validation, storage, aggregation, and Twin application are later capabilities.

## Relationship to the Student Digital Twin

The Twin ([`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md)) is
evidence-driven authoritative *state*. This engine **never** writes Twin
domains. It only surfaces candidates that a future evidence pipeline may
validate, store, and apply.

## Extension guidelines

1. **New specialised extractors** — subclass `BaseExtractor`, implement
   `supports` and `extract`, then `EvidenceExtractor.register(...)` without
   editing the coordinator.
2. **New categories** — add a member to `EvidenceCategory` when the Evidence
   Model recognises a stable high-level group.
3. **New confidence levels** — only if the Evidence Model vocabulary changes;
   do not invent numerical scores here.
4. **Multiple extractors per event** — register several strategies; the
   coordinator concatenates their candidates in registration order.
5. **Do not** introduce Flask, ORM, HTTP, or Twin-update types into this
   package. Keep infrastructure and scoring in outer layers.

## Package layout

```
app/domain/evidence/
  __init__.py
  evidence_candidate.py
  evidence_category.py
  evidence_extractor.py
  extractors/
    __init__.py
    base_extractor.py
  README.md
```
