# Learning Events Domain

Pure domain vocabulary for **Learning Events** in Kwalitec.

This package is **not** persistence, HTTP, UI, or service orchestration. It
defines the conceptual objects that later capabilities will capture, validate,
and store as Learning Evidence.

## Purpose

Establish a framework-independent representation of discrete occurrences in the
learning journey that can change how Kwalitec understands a learner — for
example starting a study session, attempting a question, completing a mission,
or updating confidence.

Learning Events are the named *moments*. Learning Evidence (see
[`LEARNING_EVIDENCE_MODEL.md`](../../../LEARNING_EVIDENCE_MODEL.md)) is the
immutable, attributable *record* derived from those moments. The Student Digital
Twin (see [`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md)) is the
authoritative *state* updated from accumulated evidence — never from ad-hoc
side channels.

## Responsibilities

| Module | Responsibility |
|---|---|
| `event_types.py` | Extensible enumeration of recognised Learning Event types |
| `event_source.py` | Provenance / producer channel for an event |
| `event_metadata.py` | Contextual attributes (time, topic, session, tags, …) |
| `learning_event.py` | Aggregate domain object tying type, source, and metadata |

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define database models, repositories, or Alembic migrations
- Expose routes, templates, or APIs
- Mutate Twin state or compute mastery / readiness scores

## Relationship to the Student Digital Twin

The Twin is evidence-driven. Learning Events feed the evidence path that updates
Twin domains (Knowledge, Memory, Behaviour, Performance, Motivation, Goals).
Events themselves are **not** Twin state. Downstream Twin update logic belongs
in later services that consume this vocabulary.

## Relationship to the Learning Evidence Model

Per the Evidence Model and ubiquitous language:

- A Learning Event is a **candidate** to become Learning Evidence.
- Evidence is immutable, attributable, and append-only once recorded.
- Event **source** supports quality weighting and explainability.
- Topic-scoped metadata should use **canonical curriculum identities**, not
  free-text-only topics.

This package encodes the event vocabulary; validation, storage, quality
weighting, and Twin application are out of scope here.

## Extension guidelines

1. **New event types** — add a member to `LearningEventType`. Prefer stable
   `snake_case` values aligned with the Evidence catalogue naming.
2. **New sources** — add a member to `EventSource` for a new producer channel.
3. **New contextual fields** — prefer `EventMetadata.attributes` or `tags` for
   experimental context; promote to first-class fields only when the field is
   stable across producers.
4. **Do not** introduce Flask, ORM, or HTTP types into this package to “make
   extension easier.” Keep infrastructure in outer layers.
5. **Do not** treat completion or self-report events as mastery by themselves —
   Twin belief updates remain a separate, evidence-weighted concern.

## Package layout

```
app/domain/
  __init__.py
  learning_events/
    __init__.py
    event_types.py
    event_source.py
    event_metadata.py
    learning_event.py
    README.md
```
