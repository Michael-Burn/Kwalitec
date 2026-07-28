# Current Milestone

**EI-001** — Curriculum Knowledge Graph Foundation (**Active delivery**)

## Objective

Establish the Curriculum Knowledge Graph as the additive Single Source of Educational Truth for future Educational Intelligence programmes: domain model, stable ids, ORM persistence, and architecture documentation — without extraction, Twin, mission, or UI work.

## Allowed modifications

- `app/domain/curriculum_knowledge_graph/`
- `app/models/curriculum_knowledge_graph.py` and model registration
- Alembic migration for `ckg_*` tables
- `tests/domain/curriculum_knowledge_graph/`
- `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/`
- Programme dashboard / milestone pointers for EI-001

## Forbidden

- Founder upload workflow, PDF parse, AI extraction
- Mission generation, Twin redesign, UI redesign
- Modifying or replacing V1/V2 Curriculum Engine import/traversal
- CIP extraction pipeline changes
- Premature runtime cutover off V1/V2

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. EI-001 does not reopen CQ engineering or Founder Validated CRI claims.

## Authoritative artefacts

- Architecture: `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/ARCHITECTURE.md`
- Completion: `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/EI001_COMPLETION_REPORT.md`

---

*This file is intentionally overwritten when the active milestone changes.*
