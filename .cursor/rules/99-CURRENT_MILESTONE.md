# Current Milestone

**EI-005** — Learning Evidence Engine (**Active delivery**)

## Objective

Record observable educational events against a Student Curriculum Instance — append-only evidence foundation of the Student Digital Twin. No mastery inference, recommendations, or study missions.

## Allowed modifications

- `app/domain/learning_evidence/`
- `app/application/learning_evidence/`
- `app/models/learning_evidence.py` and model registration
- Alembic migration for EI-005 evidence tables
- `tests/domain/learning_evidence/` · `tests/application/learning_evidence/`
- `knowledge/educational_intelligence/ei005_learning_evidence_engine/`
- Programme dashboard / milestone pointers for EI-005

## Forbidden

- Mastery / confidence calculation
- Forgetting curves
- Recommendations / study missions
- Modifying published Curriculum Knowledge Graph content
- Twin inference engines

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. EI-005 does not reopen CQ engineering or Founder Validated CRI claims.

## Authoritative artefacts

- Architecture: `knowledge/educational_intelligence/ei005_learning_evidence_engine/ARCHITECTURE.md`
- Completion: `knowledge/educational_intelligence/ei005_learning_evidence_engine/EI005_COMPLETION_REPORT.md`
- Prior: EI-001 CKG · EI-002 Extraction · EI-003 Publishing · EI-004 Binding

---

*This file is intentionally overwritten when the active milestone changes.*
