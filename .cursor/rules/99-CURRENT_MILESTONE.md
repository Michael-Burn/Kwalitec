# Current Milestone

**EI-003** — Founder Curriculum Publishing Workflow (**Active delivery**)

## Objective

Transform a validated Draft Curriculum Knowledge Graph into a Founder-approved Published Curriculum Edition with inspection, editorial operations, explicit publication, auditability, and edition history — without Twin, mission, recommendation, student UI, or runtime CKG cutover.

## Allowed modifications

- `app/domain/curriculum_publishing/`
- `app/application/curriculum_publishing/`
- `app/models/curriculum_knowledge_graph.py` (review/publication/audit/snapshot tables) and model registration
- Alembic migration for EI-003 publishing extensions
- `tests/domain/curriculum_publishing/` · `tests/application/curriculum_publishing/`
- `knowledge/educational_intelligence/ei003_curriculum_publishing/`
- Programme dashboard / milestone pointers for EI-003

## Forbidden

- Student Digital Twin, missions, recommendations
- Exposing drafts to students
- Student runtime / CurriculumService cutover onto CKG
- Founder HTTP UI redesign
- CIP stage contract changes

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. EI-003 does not reopen CQ engineering or Founder Validated CRI claims.

## Authoritative artefacts

- Architecture: `knowledge/educational_intelligence/ei003_curriculum_publishing/ARCHITECTURE.md`
- Completion: `knowledge/educational_intelligence/ei003_curriculum_publishing/EI003_COMPLETION_REPORT.md`
- Prior: EI-001 CKG · EI-002 Extraction Pipeline

---

*This file is intentionally overwritten when the active milestone changes.*
