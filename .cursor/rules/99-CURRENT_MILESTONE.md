# Current Milestone

**EI-002** — Curriculum Extraction Pipeline (**Active delivery**)

## Objective

Transform Canonical Structured Documents (IFoA CMP + Syllabus) into a Draft Curriculum Knowledge Graph with provenance, confidence, validation, and `publication_state=draft` persistence — without Founder UI, publish, Twin, mission, or student runtime integration.

## Allowed modifications

- `app/domain/curriculum_extraction/`
- `app/application/curriculum_extraction/`
- `app/infrastructure/adapters/curriculum_extraction/`
- `app/models/curriculum_knowledge_graph.py` (draft fields + provenance/validation tables) and model registration
- Alembic migration for EI-002 CKG extensions
- `tests/domain/curriculum_extraction/` · `tests/application/curriculum_extraction/`
- `knowledge/educational_intelligence/ei002_curriculum_extraction_pipeline/`
- Programme dashboard / milestone pointers for EI-002

## Forbidden

- Founder approval / publish UI
- Student Digital Twin, missions, recommendations
- Student runtime / CurriculumService cutover onto CKG
- CIP stage contract changes
- LLM / OCR extraction inside Educational Intelligence

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. EI-002 does not reopen CQ engineering or Founder Validated CRI claims.

## Authoritative artefacts

- Architecture: `knowledge/educational_intelligence/ei002_curriculum_extraction_pipeline/ARCHITECTURE.md`
- Completion: `knowledge/educational_intelligence/ei002_curriculum_extraction_pipeline/EI002_COMPLETION_REPORT.md`
- Prior SoT: `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/ARCHITECTURE.md`

---

*This file is intentionally overwritten when the active milestone changes.*
