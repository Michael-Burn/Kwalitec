# ADR-001: Curriculum Hierarchy

**Status:** Accepted
**Date:** July 2026
**Deciders:** Kwalitec Engineering
**Epic:** Epic 1 — Curriculum Architecture Foundation

---

## Context

### Background

Kwalitec was originally designed around a flat curriculum model (V1) in which a `Curriculum` contained a list of `Topic` objects, each with associated `LearningOutcome` entries. This structure was sufficient for an early study planner focused on recording activity rather than reasoning about learning.

As the product vision evolved toward Educational Intelligence, the limitations of the flat model became clear. Professional examination syllabuses are not flat lists. They are structured hierarchies published by awarding bodies and organised into major sections, each covering a coherent area of the examination domain. Within each section sit topics, and within each topic sit discrete, measurable learning objectives.

The V1 flat model could not faithfully represent this structure. Specifically:

- Section-level exam weightings (critical for planning and readiness calculations) could not be expressed in V1 without heuristic approximation.
- Topic ordering was handled through a `parent_topic_id` self-referential tree, which created depth-first traversal complexity without capturing the educational intent of sections.
- Learning outcomes in V1 were simple text descriptions. They did not capture cognitive level, learning type, or the granular time estimates needed for adaptive scheduling.
- There was no stable code scheme linking engine dataclasses to database rows, making imports fragile.

The existing V1 model served as the only curriculum representation. Replacing it entirely would break all existing study plans, missions, and readiness calculations for any student whose plan was built against a V1 curriculum.

### Constraints

1. **Backwards compatibility is non-negotiable.** Existing V1 study plans, missions, and progress records must continue to function without data migration.
2. **The curriculum engine must remain deterministic.** Given the same JSON input, the engine must produce identical output on every run.
3. **Format detection must be automatic.** Application code that loads a curriculum must not need to know in advance whether it is loading a V1 or V2 file.
4. **The database schema must support both formats.** `Section` and `Topic.section_id` must be nullable so that V1 topics remain valid without modification.
5. **Traversal logic must be centralised.** All ordering must go through `CurriculumService` helpers to prevent V1/V2 divergence across services.

---

## Decision

### Adopt a canonical four-level curriculum hierarchy (V2) alongside the existing V1 flat model

The Curriculum Engine is extended to support a second, canonical format (V2) defined by the following hierarchy:

```
Curriculum
  └── Section
        └── Topic
              └── Learning Objective
```

V2 dataclasses are named with the `Definition` suffix to distinguish them from V1 models:

| V1 Engine Dataclass | V2 Engine Dataclass             |
|---------------------|---------------------------------|
| `Curriculum`        | `CurriculumDefinition`          |
| *(none)*            | `SectionDefinition`             |
| `Topic`             | `TopicDefinition`               |
| `LearningOutcome`   | `LearningObjectiveDefinition`   |

The V2 hierarchy maps directly to the official professional examination syllabus structure used by awarding bodies such as the Institute and Faculty of Actuaries (IFoA).

### Key design choices

**Additive schema change.** A new `Section` ORM model is added to the database. `Topic` gains a nullable `section_id` foreign key. V1 topics leave `section_id` as `NULL`; V2 topics are linked to their parent section. No existing V1 data is modified.

**Automatic format detection.** The canonical loader `CurriculumRepository.load_auto()` attempts to load V1 first, then falls back to V2. Callers receive either a `Curriculum` (V1) or a `CurriculumDefinition` (V2) and can distinguish the format using `isinstance`. This pattern is centralised exclusively in `CurriculumRepository`; it must not be duplicated across services.

**Section exam weighting.** In V2, `exam_weight` belongs to `SectionDefinition`. Topics within a V2 curriculum import with `syllabus_weight = 0.0` at the topic level so that existing topic-weight-based code paths do not produce misleading values. Section-level weighting is used by the planning and readiness services.

**Canonical flat flattening.** `CurriculumEngineService.get_topics_flat()` is the single entry point for producing an ordered flat topic list from either format: V1 returns the existing flat list unchanged; V2 iterates sections and topics in `display_order`. This method must not be duplicated.

**Canonical DB traversal.** `CurriculumService` provides traversal helpers (`get_sections`, `get_topics_for_section`, `get_all_topics_ordered`) that branch on whether sections exist. All services must call these helpers; they must not reimplement ordering logic.

**Cognitive level and learning type.** `LearningObjectiveDefinition` records the Bloom's taxonomy cognitive level (`remember`, `understand`, `apply`, `analyze`, `evaluate`, `create`) and the learning type (`concept`, `procedure`, `problem_solving`, `application`, `analysis`). These fields support future adaptive scheduling and difficulty modelling.

**Display order over position.** V2 uses explicit `display_order` fields on sections, topics, and learning objectives. This avoids relying on JSON array position and makes re-ordering safe without breaking identifiers.

**Stable identifiers.** V2 entities use structured, stable identifiers (e.g. `CS1-A-T01`, `CS1-A-T01-LO01`). These identifiers are stable across curriculum revisions and are used as foreign keys when importing into the database.

**Idempotent import.** Curriculum import (via `CurriculumService.import_curricula`) is idempotent. Re-running import on an already-imported curriculum is safe; it updates existing rows rather than creating duplicates.

**Backfill command.** A `flask backfill-sections` CLI command is provided to migrate any existing V2 `Curriculum` rows that were imported before the `Section` model was added. The command is idempotent and safe to run in production.

---

## Consequences

### Positive

- **Educational fidelity.** The data model now faithfully represents official professional examination syllabuses, enabling section-weighted planning and readiness calculations.
- **Foundation for Educational Intelligence.** Epic 2 (Behaviour Engine, Performance Engine, Decision Engine) depends on having granular, structured learning objectives. V2 provides that foundation.
- **Backwards compatibility preserved.** V1 study plans, missions, and progress calculations continue to function without any data change.
- **Centralised traversal eliminates V1/V2 drift.** All ordering goes through `CurriculumService` helpers, preventing divergence.
- **Deterministic and testable.** The engine remains purely in-memory and stateless. Given the same JSON input, output is identical.
- **Comprehensive test coverage.** 977 automated tests pass, including dedicated V2 and section-aware test suites.

### Negative / Trade-offs

- **Dual-format complexity.** Supporting two curriculum formats in parallel increases cognitive load for contributors. Mitigation: the canonical entry points (`load_auto`, `get_topics_flat`, `CurriculumService` helpers) encapsulate the branching.
- **Nullable `section_id`.** The nullable foreign key is a schema compromise to support both formats. Contributors must be aware that `section_id is NULL` does not indicate a data error for V1 topics.
- **V2 topics carry `syllabus_weight = 0.0`.** Code that sums topic weights to assess curriculum coverage must account for this; V2 uses section weights instead.
- **Migration required for legacy V2 imports.** Any V2 curriculum imported before `Section` rows existed must be backfilled via `flask backfill-sections`.

### Future obligations

- New syllabuses should be authored in V2 format.
- V1 loaders, schemas, and import paths must not be removed until an explicit migration milestone has been planned and approved.
- When implementing section-weighted recommendations (deferred to Epic 2), use `Section.exam_weight` rather than re-deriving weights from topic-level fields.
- The `load_auto` try-V1-then-V2 chain must remain exclusively in `CurriculumRepository`.

---

## Related Documents

| Document | Purpose |
|---|---|
| `ARCHITECTURE.md` | Full architecture diagrams, traversal reference |
| `PROJECT_CONTEXT.md` | V1/V2 compatibility constraints summary |
| `.cursor/rules/08-curriculum-v2.mdc` | Non-negotiable V1/V2 invariants for agents |
| `docs/reviews/CURRICULUM_ARCHITECTURE_REVIEW.md` | Detailed architecture review of Epic 1 |
| `docs/reviews/EPIC_1_COMPLETION_REVIEW.md` | Completion review for Epic 1 |
| `docs/TECHNICAL_DEBT_REGISTER.md` | Known technical debt introduced or deferred during Epic 1 |

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../knowledge/GOVERNANCE.md)).
