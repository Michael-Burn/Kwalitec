# PX-001 — Operational Model Alignment

**Programme:** PX-001  
**Status:** Approved — design artefacts complete  
**Date:** 2026-07-28  
**Precedence:** Operational Model in the programme brief takes precedence over conflicting implementation habits.

## Objective

Realign visible product behaviour so Founder (Curriculum Authority) and Student (Learner) experiences are separated. Educational Intelligence architecture is **not** redesigned.

## Artefacts

| Document | Description |
|----------|-------------|
| [PX001_IMPLEMENTATION_SUMMARY.md](PX001_IMPLEMENTATION_SUMMARY.md) | Gap analysis, phases, success criteria |
| [ROLE_SEPARATION_REPORT.md](ROLE_SEPARATION_REPORT.md) | Persona permissions and separation rules |
| [SUBJECT_CATALOGUE_DESIGN.md](SUBJECT_CATALOGUE_DESIGN.md) | First-class Subject Catalogue |
| [NAVIGATION_CHANGES.md](NAVIGATION_CHANGES.md) | Independent Founder / Student navigation |
| [TERMINOLOGY_CHANGES.md](TERMINOLOGY_CHANGES.md) | Domain vs implementation language |
| [UPDATED_FOUNDER_FLOW.md](UPDATED_FOUNDER_FLOW.md) | New Subject → … → Publish → Available |
| [UPDATED_STUDENT_FLOW.md](UPDATED_STUDENT_FLOW.md) | Welcome → Choose Exam → Date → Availability → Begin Learning |

## Naming note

Earlier programmes reused the `PX-001` id for experience audit / Runtime C integration (`knowledge/product/px001/`, `px001_experience/`). **This** programme is Operational Model Alignment and lives only under `px001_operational_model_alignment/`.

## Constraints

- Do not redesign Twin, Decisions, Runtime, Experience Models, or Knowledge Graph cores.  
- Do not bypass LP-001 or VP-001.  
- Do not duplicate Runtime behaviour.  
- Application code changes are a follow-on phase (see Implementation Summary §5).
