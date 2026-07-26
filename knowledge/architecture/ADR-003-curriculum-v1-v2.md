# ADR-003: Curriculum V1 + V2 Coexistence

# Status

Accepted

# Date

2026-07-10

# Context

Kwalitec’s Curriculum Intelligence Engine began with a **flat** syllabus representation (V1): topics (and learning outcomes) loaded from JSON, imported into SQLAlchemy `Topic` rows, with optional parent-tree ordering via `parent_topic_id`.

Official syllabuses for professional exams are often **hierarchical**: sections (or syllabus parts) carry exam weight, and topics nest under those sections. Supporting that structure required a V2 format:

```
Section → Topic → Learning Objective
```

with section-level `exam_weight` and DB `Section` rows linked by nullable `Topic.section_id`.

A hard cutover was unacceptable:

- Existing study plans, missions, topic progress, and readiness calculations already depended on V1 data.
- Bundled and imported flat curricula must keep loading.
- Product features (planning, missions, readiness) must not require sections globally.

Breaking V1 would invalidate real learner state and block incremental syllabus upgrades.

# Decision

**V1 and V2 must coexist indefinitely until an explicit migration milestone retires V1.** New syllabuses should prefer V2; the engine and import path must keep V1 working.

| Aspect | V1 (legacy / flat) | V2 (canonical / hierarchical) |
|---|---|---|
| Engine dataclasses | `Curriculum`, `Topic`, `LearningOutcome` | `CurriculumDefinition`, `SectionDefinition`, `TopicDefinition`, `LearningObjectiveDefinition` |
| Structure | Flat topic list (+ optional parent tree in DB) | Section → Topic → Learning Objective |
| Exam weight | On topics (`syllabus_weight`) | On sections (`exam_weight`); topics often import with weight `0.0` |
| DB sections | None | `Section` rows; `Topic.section_id` set |
| Canonical order | `parent_topic_id` depth-first | `Section.display_order` then `Topic.order` |
| Loader | V1 path | `load_curriculum_v2` / V2 path |
| Detection | Engine auto-detects; import may try V1 then fall back to V2 | Same |

### Compatibility rules (non-negotiable)

1. Keep V1 loaders, schemas, validators, and import paths working.
2. `Topic.section_id` remains **nullable** so V1 topics stay valid.
3. Traversal branches: if sections exist → V2 path; else → V1 path (see [ADR-004](ADR-004-canonical-topic-traversal.md)).
4. Do not remove V1 support without an explicit, planned migration milestone.
5. Prefer additive V2 behaviour; do not hard-require sections in planning/missions/readiness.

JSON under `app/curriculum/data/{org}/{paper}/{year}.json` remains the syllabus source of truth before DB import.

# Consequences

### Positive consequences

- Learners on flat curricula keep working while hierarchical syllabuses land.
- Engine and DB can evolve additively (`Section` table, nullable FK).
- Tests can assert both formats (see [ADR-005](ADR-005-testing-strategy.md)).
- Aligns with `.cursor/rules/08-curriculum-v2.mdc` and design notes in `MILESTONE_1_1_*` / `MILESTONE_1_2_*`.

### Trade-offs

- Dual dataclasses and dual import paths increase cognitive load.
- Naming overlap (`Curriculum` / `Topic` in engine vs ORM) requires care; V2 uses `*Definition` suffixes for clarity.
- Feature code must never assume “every curriculum has sections.”

### Future considerations

- A future milestone may migrate remaining V1 JSON to V2 and deprecate flat loaders — only with data migration and dual-run tests.
- Do not rename stable official topic ids casually; progress rows depend on stable identity after import.
- Keep engine dataclasses distinct from ORM models; convert explicitly on import.

**See also:** [curriculum-engine.md](../subsystems/curriculum-engine.md), [`app/curriculum/README.md`](../../app/curriculum/README.md).

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../GOVERNANCE.md)).
