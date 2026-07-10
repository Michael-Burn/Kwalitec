# Evidence Domain — Extraction and Validation

Pure domain vocabulary and frameworks for **Evidence Candidates** in Kwalitec.

This package is **not** persistence, HTTP, UI, scoring, transformation, or Twin
mutation. It answers:

1. *What evidence exists inside this Learning Event?* (Extraction)
2. *Is this Evidence Candidate structurally valid?* (Validation)

## Purpose

Convert a [`LearningEvent`](../learning_events/learning_event.py) into zero or
more immutable [`EvidenceCandidate`](evidence_candidate.py) objects, then
structurally validate each candidate before it may enter the Transformation
Stage.

Extraction identifies *possible* learning evidence. Validation protects Twin
integrity by rejecting structurally incomplete candidates. Downstream
capabilities transform, store, quality-weight, and apply evidence to the
Student Digital Twin. Those concerns are intentionally out of scope here.

## Responsibilities

| Module | Responsibility |
|---|---|
| `evidence_category.py` | Evidence category and qualitative confidence enumerations |
| `evidence_candidate.py` | Immutable candidate evidence object |
| `extractors/base_extractor.py` | Abstract extractor strategy interface |
| `evidence_extractor.py` | Registry coordinator that invokes supporting extractors |
| `validation_severity.py` | ERROR / WARNING / INFO severity vocabulary |
| `validation_message.py` | Immutable single validation finding |
| `validation_result.py` | Aggregated accept/reject outcome with severity summary |
| `validators/base_validator.py` | Abstract validator strategy interface |
| `validators/structural.py` | Structural presence/type validators |
| `validators/evidence_validator.py` | Registry coordinator that invokes validators |

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define repositories, database models, or Alembic migrations
- Persist evidence or Learning Events
- Transform candidates into stored Learning Evidence
- Assign numerical weights, mastery scores, or readiness scores
- Update the Student Digital Twin
- Expose routes, templates, or HTTP APIs
- Encode educational or business acceptance rules in validation

## Validation lifecycle

```
Learning Event
      │
      ▼
Evidence Extraction Engine  →  EvidenceCandidate(s)  (immutable)
      │
      ▼
Evidence Validation Stage   →  ValidationResult
      │                         (accepted + messages)
      ├── accepted=True  →  eligible for Transformation Stage (Capability 1.4+)
      └── accepted=False →  rejected; does not proceed
```

1. Receive **one** `EvidenceCandidate`.
2. Run every registered `BaseValidator` in registration order.
3. Collect `ValidationMessage` findings without mutating the candidate.
4. Aggregate into one `ValidationResult` (`accepted` is False if any ERROR).
5. Stop. Do not transform, score, persist, or update the Twin.

## Relationship to Learning Events

Learning Events (Capability 1.1) are the named *moments* in the learning
journey. The Evidence Extraction Engine inspects an event and emits candidates
describing what kinds of evidence that moment contains.

- One event may yield **zero, one, or many** candidates (e.g. a completed quiz
  may produce Performance and Time candidates).
- Events are inputs; candidates are outputs. Neither is Twin state.
- Validation does not re-interpret the event; it checks the candidate shape.

## Relationship to Evidence Candidates

An Evidence Candidate is a **proposal** that evidence exists — not yet the
immutable, stored Learning Evidence record. Validation ensures required
structural fields are present and correctly typed before transformation:

- Identifier, category, timestamp, originating event
- Source (provenance), metadata object, payload mapping

Candidates remain frozen throughout validation.

## Relationship to the Transformation Stage

The Transformation Stage (Capability 1.4+) consumes **accepted** candidates and
turns them into durable Learning Evidence. This package only produces
`ValidationResult`; it does not perform transformation.

Rejected candidates must not enter transformation. Warnings may accompany an
accepted result and are advisory for later stages.

## Relationship to the Student Digital Twin

The Twin ([`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md)) is
evidence-driven authoritative *state*. This package **never** writes Twin
domains. Validation exists so only structurally sound candidates can later
become evidence that updates the Twin.

## Extension guidelines

1. **New specialised extractors** — subclass `BaseExtractor`, implement
   `supports` and `extract`, then `EvidenceExtractor.register(...)` without
   editing the coordinator.
2. **New validators** — subclass `BaseValidator`, implement `validate`, then
   `EvidenceValidator.register(...)` or pass the instance into the constructor.
   Prefer composition over editing `EvidenceValidator`.
3. **Default structural set** — use `EvidenceValidator.with_structural_rules()`
   for the standard presence/type checks; add further validators on top.
4. **New categories** — add a member to `EvidenceCategory` when the Evidence
   Model recognises a stable high-level group.
5. **New confidence levels** — only if the Evidence Model vocabulary changes;
   do not invent numerical scores here.
6. **Severity** — use ERROR to reject; WARNING/INFO for advisory findings that
   do not flip `accepted`.
7. **Do not** introduce Flask, ORM, HTTP, transformation, scoring, or
   Twin-update types into this package. Keep infrastructure in outer layers.

## Package layout

```
app/domain/evidence/
  __init__.py
  evidence_candidate.py
  evidence_category.py
  evidence_extractor.py
  validation_message.py
  validation_result.py
  validation_severity.py
  extractors/
    __init__.py
    base_extractor.py
  validators/
    __init__.py
    base_validator.py
    evidence_validator.py
    structural.py
  README.md
```
