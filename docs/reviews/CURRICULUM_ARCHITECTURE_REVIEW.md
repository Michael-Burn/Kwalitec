# Curriculum Architecture Review

**Status:** Accepted
**Date:** July 2026
**Epic:** Epic 1 — Curriculum Architecture Foundation
**Reviewer:** Kwalitec Engineering
**Version:** v0.4.0

---

## Summary

This document reviews the curriculum architecture introduced in Epic 1 of Kwalitec. It assesses the design decisions, implementation quality, and architectural compliance of the Curriculum Engine V2, the associated database layer changes, and the service-layer integration.

Epic 1 replaced the original flat curriculum model (V1) with a canonical four-level hierarchy (V2) while preserving complete backwards compatibility. The review confirms that the architecture is sound, the implementation is complete, and the system is ready for production release as v0.4.0.

---

## Scope Reviewed

This review covers the following components introduced or modified during Epic 1.

### Curriculum Engine (`app/curriculum/`)

| Module | Review Coverage |
|---|---|
| `models.py` | V2 dataclass definitions and V1 compatibility |
| `schemas.py` | JSON schema validation for V1 and V2 |
| `loader.py` | V1 and V2 loaders; format detection |
| `validator.py` | Business rule validation for V1 and V2 |
| `repository.py` | Cache layer and `load_auto` canonical entry point |
| `seed.py` | Bootstrap path for bundled curricula |
| `exceptions.py` | Exception hierarchy |
| `data/` | Bundled V2 curriculum JSON files |

### Database Layer (`app/models/`, `migrations/`)

| Component | Review Coverage |
|---|---|
| `Section` ORM model | Full |
| `Topic.section_id` foreign key | Full |
| Migration `202610070001` | Full |
| `flask backfill-sections` CLI | Full |

### Service Layer (`app/services/`)

| Service | Review Coverage |
|---|---|
| `CurriculumEngineService` | `load_auto`, `get_topics_flat` |
| `CurriculumService` | `import_curricula`, `get_sections`, `get_topics_for_section`, `get_all_topics_ordered` |

---

## Findings

### Finding 1 — Curriculum Hierarchy Alignment with Professional Examination Syllabuses

**Assessment: PASS**

The V2 hierarchy (Curriculum → Section → Topic → Learning Objective) is a faithful representation of the structure used by professional examination awarding bodies, including the Institute and Faculty of Actuaries (IFoA).

Section-level `exam_weight` fields enable accurate planning based on official syllabus weighting rather than heuristic approximation. Learning objectives carry `cognitive_level` (Bloom's taxonomy) and `learning_type` fields that provide the granularity required for future adaptive learning capabilities.

The decision to use `display_order` fields rather than rely on JSON array position is correct. It makes re-ordering safe and avoids brittle positional assumptions.

### Finding 2 — V1 Backwards Compatibility

**Assessment: PASS**

The V1 flat model is fully preserved. All V1 dataclasses (`Curriculum`, `Topic`, `LearningOutcome`), loaders, schemas, and import paths remain intact. No V1 data is modified by any Epic 1 change.

`Topic.section_id` is nullable, ensuring V1 topics carry `NULL` without constraint violations. The `CurriculumService` traversal helpers branch correctly: V2 topics (with `section_id` set) use the `Section.display_order` → `Topic.order` path; V1 topics (with `section_id` NULL) use the `parent_topic_id` depth-first path.

The V1 regression test suite passes in full. No V1 study plan, mission, or readiness calculation is broken.

### Finding 3 — Canonical Entry Points and Duplication Risk

**Assessment: PASS**

The three canonical entry points are correctly implemented and centralised:

**`CurriculumRepository.load_auto()`** is the only location that implements the V1-then-V2 format detection fallback. No other module or service duplicates this try/except pattern.

**`CurriculumEngineService.get_topics_flat()`** is the only location that implements format-aware flat topic extraction from an engine curriculum. No other code duplicates the `sorted(sections, key=display_order) → sorted(topics, key=display_order)` pattern.

**`CurriculumService.get_all_topics_ordered()`** is the only location that implements V1/V2-branching ordered topic traversal at the database level. No other service reimplements topic ordering.

The risk of V1/V2 ordering drift caused by duplicated traversal logic is therefore low.

### Finding 4 — Database Schema

**Assessment: PASS**

The `Section` model is correctly designed. It holds `curriculum_id`, `title`, `code`, `exam_weight`, `estimated_hours`, `difficulty`, `display_order`, and `description`. The `back_populates` relationship with `Curriculum` and `Topic` is correctly configured.

The `Topic.section_id` nullable foreign key to `Section.id` is correctly defined. The cascade and relationship configuration is consistent with existing ORM patterns in the codebase.

Migration `202610070001` applies cleanly on a fresh database and on an existing database with V1 data. The migration is reversible. No existing data is deleted.

The `flask backfill-sections` command is idempotent and correctly skips already-linked topics. It is safe to run on production.

### Finding 5 — Validation

**Assessment: PASS**

`validate_curriculum_v2()` enforces all expected business rules:

- Unique section IDs, topic IDs, and learning objective IDs across the curriculum
- Unique learning objective codes
- Section `exam_weight` sum within ±5% of 100
- Positive `estimated_hours` for sections
- Positive `estimated_minutes` for topics and learning objectives
- Valid `section_id` cross-references (each topic's `section_id` matches its parent section)
- Valid `topic_id` cross-references (each learning objective's `topic_id` matches its parent topic)
- `difficulty` values restricted to `{foundational, intermediate, advanced}`
- `cognitive_level` values restricted to the six Bloom's taxonomy levels
- `learning_type` values restricted to the five permitted types
- Positive `display_order` for sections, topics, and learning objectives

`validate_curriculum_unified()` correctly dispatches to V1 or V2 validation based on `isinstance`, and raises `TypeError` for unrecognised inputs.

One minor pre-release issue was identified: five model symbols imported in `validator.py` (`LearningObjectiveDefinition`, `LearningOutcome`, `SectionDefinition`, `Topic`, `TopicDefinition`) are unused. These were removed as part of the pre-release audit (BLOCKER 2).

### Finding 6 — Import Idempotency

**Assessment: PASS**

`CurriculumService.import_curricula()` is idempotent. Running the import against an already-imported curriculum updates existing rows rather than creating duplicates. The idempotency guarantee is tested and is required for the `StartupService` bootstrap path to be safe on repeated restarts.

### Finding 7 — JSON Schema Coverage

**Assessment: PASS**

The V2 JSON schema (`schemas.py`) enforces the required fields, types, and structural constraints before dataclass construction. Format detection is driven by the presence of the `"sections"` key. The schema validation runs before the validator, meaning malformed input fails early with a clear schema error rather than producing a partially constructed dataclass.

### Finding 8 — Test Coverage

**Assessment: PASS**

The curriculum test suite is comprehensive:

| Suite | Coverage |
|---|---|
| `test_curriculum_engine.py` | V1 engine: loading, validation, error handling |
| `test_curriculum_engine_v2.py` | V2 engine: loading, validation, traversal, edge cases |
| `test_curriculum_importer.py` | Import idempotency, V1/V2 compatibility, section persistence |
| `test_curriculum_section_aware.py` | Section-aware service integration |
| `test_section_model.py` | Section ORM model CRUD and relationships |
| `test_topic_section_relationship.py` | Topic–Section relationship queries |

977 tests pass in total. No failures.

### Finding 9 — Layering Compliance

**Assessment: PASS**

The layering invariant is preserved:

- Route modules do not contain curriculum traversal or ordering logic.
- Services do not import `flask.request` or session globals.
- The Curriculum Engine modules (`app/curriculum/`) do not import SQLAlchemy models or blueprints.
- ORM models do not import blueprints or services.

The dependency direction (Templates → Blueprints → Services → Models + Engine → DB/JSON) is correctly maintained throughout Epic 1.

### Finding 10 — Repository Cleanliness

**Assessment: PASS (after pre-release audit)**

No debug code, `print()` statements, temporary comments, or commented-out production code were introduced during Epic 1. The pre-release audit verified cleanliness across all Epic 1 files. Three placeholder documentation stubs were identified and completed as pre-release blockers.

---

## Architecture Compliance

### Curriculum V1/V2 Invariants

All V1/V2 invariants defined in `.cursor/rules/08-curriculum-v2.mdc` and `ARCHITECTURE.md` are satisfied:

| Invariant | Status |
|---|---|
| V1 and V2 both loadable and traversable | PASS |
| `load_auto` fallback chain in `CurriculumRepository` only | PASS |
| `get_topics_flat` in `CurriculumEngineService` only | PASS |
| `get_all_topics_ordered` in `CurriculumService` only | PASS |
| `Topic.section_id` nullable for V1 compatibility | PASS |
| V1 loaders and schemas preserved | PASS |
| No V1 data dropped or modified | PASS |
| Import idempotent | PASS |

### Structural Invariants

All application factory (`create_app`) patterns are preserved. The `Section` model is correctly imported in the extension initialisation path for ORM metadata registration. The `flask backfill-sections` CLI command is registered in `cli.py`. No blueprint or route was modified outside the explicitly stated scope.

---

## Outcomes / Follow-ups

### Architecture is Accepted

The Curriculum Architecture V2 is accepted as the canonical curriculum format for Kwalitec.

New syllabuses must be authored in V2 format. V1 support remains in place for existing curricula until an explicit migration milestone authorises its removal.

### Monitoring Recommendations

The following items should be monitored in production:

1. **Backfill completeness.** After deploying v0.4.0, verify that `flask backfill-sections` has been run and that all V2 topics have `section_id` set.
2. **Import idempotency.** Monitor `StartupService` logs to confirm that curriculum import completes without errors on first boot and is silent on subsequent boots.
3. **Traversal correctness.** Confirm that study plans built against V2 curricula display sections and topics in the correct `display_order` sequence.

### Deferred Items

The following architectural improvements were explicitly deferred:

| Item | Reason | Target |
|---|---|---|
| Section-weighted recommendation scoring | Depends on Epic 2 Decision Engine | Epic 2 |
| Graph-based prerequisite relationships | Current hierarchy is sufficient | Future |
| Topic-level progress at LO granularity | Topic-level is the right usability balance | Deferred |
| Performance optimisation for curriculum queries | Not justified at current scale | When scale warrants |

### Epic 2 Prerequisites Satisfied

Epic 2 (Educational Intelligence) requires:

- Structured learning objectives with cognitive level and learning type — **delivered**
- Section-weighted curriculum for planning — **delivered**
- Stable entity identifiers for LO-level progress tracking — **delivered**
- Deterministic traversal guaranteed by centralised helpers — **delivered**

The Curriculum Architecture Foundation is complete and the system is ready to proceed to Epic 2.
