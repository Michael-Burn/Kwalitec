# Evidence Domain — Extraction, Validation, and Transformation

Pure domain vocabulary and frameworks for **Evidence Candidates** and
**Learning Evidence** in Kwalitec.

This package is **not** persistence, HTTP, UI, scoring, Twin mutation, or
recommendation logic. It answers:

1. *What evidence exists inside this Learning Event?* (Extraction)
2. *Is this Evidence Candidate structurally valid?* (Validation)
3. *What is the canonical Learning Evidence form of this accepted candidate?*
   (Transformation)

## Purpose

Convert a [`LearningEvent`](../learning_events/learning_event.py) into zero or
more immutable [`EvidenceCandidate`](evidence_candidate.py) objects, structurally
validate each candidate, then normalize each **accepted** candidate into one
immutable [`LearningEvidence`](learning_evidence.py) object.

Learning Evidence is the **single canonical evidence representation** consumed
by the Student Digital Twin and all future intelligence components.

Extraction identifies *possible* learning evidence. Validation protects Twin
integrity by rejecting structurally incomplete candidates. Transformation
performs **normalization only** — it does not score, persist, update the Twin,
or make recommendations.

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
| `evidence_type.py` | Canonical Learning Evidence type catalogue |
| `learning_evidence.py` | Immutable canonical Learning Evidence object |
| `transformers/base_transformer.py` | Abstract transformer strategy interface |
| `evidence_transformer.py` | Registry coordinator that invokes supporting transformers |

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define repositories, database models, or Alembic migrations
- Persist evidence or Learning Events
- Assign numerical weights, mastery scores, or readiness scores
- Update the Student Digital Twin
- Produce recommendations or planning outputs
- Expose routes, templates, or HTTP APIs
- Encode educational or business acceptance rules in validation
- Encode scoring or Twin-update logic in transformation

## Transformation lifecycle

```
Learning Event
      │
      ▼
Evidence Extraction Engine  →  EvidenceCandidate(s)  (immutable)
      │
      ▼
Evidence Validation Stage   →  ValidationResult
      │                         (accepted + messages)
      ├── accepted=False →  rejected; does not proceed
      └── accepted=True
            │
            ▼
Evidence Transformation Stage  →  LearningEvidence  (immutable, canonical)
            │
            ▼
  (later) Persistence / Twin update / intelligence consumers
```

1. Receive **one** validated `EvidenceCandidate` (caller must only pass
   candidates accepted by the Validation Stage).
2. Select the first registered `BaseTransformer` that reports
   `supports(candidate)`.
3. Invoke `transform(candidate)` to produce **one** `LearningEvidence`.
4. Stop. Do not score, persist, recommend, or update the Twin.

If no registered transformer supports the candidate, raise
`TransformationError`.

## Relationship to Learning Events

Learning Events (Capability 1.1) are the named *moments* in the learning
journey. The Evidence Extraction Engine inspects an event and emits candidates
describing what kinds of evidence that moment contains.

- One event may yield **zero, one, or many** candidates (e.g. a completed quiz
  may produce Performance and Time candidates).
- Events are inputs; candidates are intermediate; Learning Evidence is the
  canonical output of this package’s pipeline.
- Transformation records `originating_event_id` for audit correlation; it does
  not re-interpret the event beyond what the candidate already carries.

## Relationship to Evidence Candidates

An Evidence Candidate is a **proposal** that evidence exists — not yet the
canonical Learning Evidence record. After structural validation:

- Accepted candidates enter the Transformation Stage.
- Rejected candidates must not be transformed.
- Candidates remain frozen throughout validation and transformation.

Transformation normalizes candidate fields into Learning Evidence shape
(identity, type, curriculum references, payload, provenance, confidence,
metadata) without inventing scores or Twin mutations.

## Relationship to the Validation Stage

The Validation Stage (Capability 1.3) produces `ValidationResult`. Only
candidates with `accepted=True` are eligible for transformation. This package’s
transformer coordinator does not re-run validation; callers enforce the gate.

Warnings on an accepted result are advisory and may be copied into Learning
Evidence metadata by specialised transformers in later capabilities.

## Relationship to the Student Digital Twin

The Twin ([`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md)) is
evidence-driven authoritative *state*. Learning Evidence is the authoritative
*history* that may later update Twin domains.

This package **never** writes Twin domains. Transformation exists so Twin and
intelligence consumers share one canonical evidence representation. Persistence
and Twin update functions belong to later epics.

## Extension guidelines

1. **New specialised extractors** — subclass `BaseExtractor`, implement
   `supports` and `extract`, then `EvidenceExtractor.register(...)` without
   editing the coordinator.
2. **New validators** — subclass `BaseValidator`, implement `validate`, then
   `EvidenceValidator.register(...)` or pass the instance into the constructor.
   Prefer composition over editing `EvidenceValidator`.
3. **Default structural set** — use `EvidenceValidator.with_structural_rules()`
   for the standard presence/type checks; add further validators on top.
4. **New specialised transformers** — subclass `BaseTransformer`, implement
   `supports` and `transform`, then `EvidenceTransformer.register(...)`.
   Planned specialised transformers include KnowledgeTransformer,
   BehaviourTransformer, ConfidenceTransformer, RevisionTransformer,
   PlanningTransformer, and TimeTransformer. Register more specific
   transformers *before* broader ones so they take precedence.
5. **New evidence types** — add a member to `EvidenceType` when the Evidence
   Model catalogue recognises a stable type.
6. **New categories** — add a member to `EvidenceCategory` when the Evidence
   Model recognises a stable high-level group.
7. **New confidence levels** — only if the Evidence Model vocabulary changes;
   do not invent numerical scores here.
8. **Severity** — use ERROR to reject; WARNING/INFO for advisory findings that
   do not flip `accepted`.
9. **Do not** introduce Flask, ORM, HTTP, scoring, Twin-update, recommendation,
   or planning types into this package. Keep infrastructure in outer layers.

## Package layout

```
app/domain/evidence/
  __init__.py
  evidence_candidate.py
  evidence_category.py
  evidence_extractor.py
  evidence_transformer.py
  evidence_type.py
  learning_evidence.py
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
  transformers/
    __init__.py
    base_transformer.py
  README.md
```
