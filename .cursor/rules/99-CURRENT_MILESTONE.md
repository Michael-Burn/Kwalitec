# Current Milestone

**EI-007** — Educational Reasoning Engine (**Active delivery**)

## Objective

Determine highest-value educational actions for a Student Curriculum Instance from published curriculum, Twin beliefs, and evidence references. Produce ordered, explainable decisions only — no mission text or student UI.

## Allowed modifications

- `app/domain/educational_reasoning_engine/`
- `app/application/educational_reasoning_engine/`
- `app/models/educational_reasoning_engine.py` and model registration
- Alembic migration for EI-007 decision tables
- `tests/domain/educational_reasoning_engine/` · `tests/application/educational_reasoning_engine/`
- `knowledge/educational_intelligence/ei007_educational_reasoning_engine/`
- Programme dashboard / milestone pointers for EI-007

## Forbidden

- Daily Missions / Coach responses / student UI
- Mutating Learning Evidence, Twin beliefs, or published curriculum
- Probabilistic AI / LLM reasoning in core learning paths

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. EI-007 does not reopen CQ engineering or Founder Validated CRI claims. Legacy `app.domain.educational_reasoning` is untouched.

## Authoritative artefacts

- Architecture: `knowledge/educational_intelligence/ei007_educational_reasoning_engine/ARCHITECTURE.md`
- Completion: `knowledge/educational_intelligence/ei007_educational_reasoning_engine/EI007_COMPLETION_REPORT.md`
- Prior: EI-001 CKG · EI-002 Extraction · EI-003 Publishing · EI-004 Binding · EI-005 Evidence · EI-006 Twin Inference

---

*This file is intentionally overwritten when the active milestone changes.*
