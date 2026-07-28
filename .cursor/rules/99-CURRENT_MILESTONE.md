# Current Milestone

**EI-004** — Student Curriculum Binding (**Active delivery**)

## Objective

Bind a student to exactly one Published Curriculum Edition per subject and persist educational state for every curriculum node — foundation of the Student Digital Twin. No recommendations, missions, mastery engines, or CKG mutations.

## Allowed modifications

- `app/domain/student_curriculum_binding/`
- `app/application/student_curriculum_binding/`
- `app/models/student_curriculum_binding.py` and model registration
- Alembic migration for EI-004 binding tables
- `tests/domain/student_curriculum_binding/` · `tests/application/student_curriculum_binding/`
- `knowledge/educational_intelligence/ei004_student_curriculum_binding/`
- Programme dashboard / milestone pointers for EI-004

## Forbidden

- Recommendations / study missions
- Forgetting curves / mastery calculation engines
- AI reasoning
- Modifying published Curriculum Knowledge Graph content
- Student runtime / CurriculumService cutover onto CKG

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. EI-004 does not reopen CQ engineering or Founder Validated CRI claims.

## Authoritative artefacts

- Architecture: `knowledge/educational_intelligence/ei004_student_curriculum_binding/ARCHITECTURE.md`
- Completion: `knowledge/educational_intelligence/ei004_student_curriculum_binding/EI004_COMPLETION_REPORT.md`
- Prior: EI-001 CKG · EI-002 Extraction · EI-003 Publishing

---

*This file is intentionally overwritten when the active milestone changes.*
