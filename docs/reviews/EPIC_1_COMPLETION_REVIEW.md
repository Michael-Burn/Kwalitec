# Epic 1 Completion Review

**Status:** Accepted
**Date:** July 2026
**Epic:** Epic 1 — Curriculum Architecture Foundation
**Reviewer:** Kwalitec Engineering
**Version:** v0.4.0

---

## Summary

Epic 1 delivered the Curriculum Architecture Foundation, transforming Kwalitec's internal curriculum model from a flat topic list (V1) into a canonical four-level educational hierarchy (V2): Curriculum → Section → Topic → Learning Objective.

This transformation aligns the software with the structure of official professional examination syllabuses and establishes the educational data foundation required for all future adaptive learning capabilities.

The epic concluded with 977 automated tests passing, zero known regressions, and a stable architecture declared ready for Epic 2 (Educational Intelligence).

---

## Scope Reviewed

The following areas of the codebase were in scope for Epic 1.

### Curriculum Engine (in-memory)

- V2 dataclasses: `CurriculumDefinition`, `SectionDefinition`, `TopicDefinition`, `LearningObjectiveDefinition`
- V2 JSON schema (`app/curriculum/schemas.py`)
- V2 loader (`app/curriculum/loader.py`)
- Canonical format detection (`CurriculumRepository.load_auto`)
- V2 validation (`app/curriculum/validator.py` — `validate_curriculum_v2`, `validate_curriculum_unified`)
- Repository cache and query API (`app/curriculum/repository.py`)
- Bundled V2 curriculum JSON (`app/curriculum/data/`)

### Database Layer

- `Section` ORM model (`app/models/section.py`)
- `Topic.section_id` nullable foreign key (migration `202610070001`)
- `LearningObjective` model updates for V2 field alignment
- `flask backfill-sections` CLI command for retroactive section linking

### Service Layer

- `CurriculumEngineService.get_topics_flat()` — canonical engine-side flattener for V1/V2
- `CurriculumService.get_sections()` — section traversal for V2; returns `[]` for V1
- `CurriculumService.get_topics_for_section()` — topic traversal within a section
- `CurriculumService.get_all_topics_ordered()` — unified V1/V2 ordered topic list
- `CurriculumService.import_curricula()` — idempotent import with section persistence

### Study Plan Integration

- Study Plan wizard updated to use canonical `CurriculumService` traversal helpers
- Section-aware planning maintained backwards compatibility with all V1 study plans

### Testing

- `tests/test_curriculum_engine_v2.py` — V2 engine unit tests
- `tests/test_curriculum_section_aware.py` — section-aware service integration tests
- `tests/test_section_model.py` — Section ORM model tests
- `tests/test_topic_section_relationship.py` — Topic–Section relationship tests
- `tests/test_curriculum_importer.py` — import idempotency and V1/V2 compatibility tests
- Full regression suite for V1 compatibility

---

## Findings

### Architecture

**PASS.** The layering invariant (Templates → Blueprints → Services → Models + Curriculum Engine → DB/JSON) is preserved throughout Epic 1.

No route module contains curriculum traversal or planning logic. All ordering goes through `CurriculumService` helpers. The engine remains purely in-memory and stateless.

**Canonical entry points are correctly centralised:**

- `CurriculumRepository.load_auto()` is the only location implementing the V1-then-V2 fallback chain.
- `CurriculumEngineService.get_topics_flat()` is the only location implementing format-aware flat topic extraction.
- `CurriculumService.get_all_topics_ordered()` is the only location implementing V1/V2-branching DB traversal.

No duplication of these patterns was found across the codebase.

### V1 Backwards Compatibility

**PASS.** All V1 study plans, missions, progress records, and readiness calculations continue to function.

- `Topic.section_id` is nullable; V1 topics have `NULL` and are not affected by section migrations.
- V1 loaders, schemas, and import paths are preserved.
- The `parent_topic_id` depth-first traversal is retained for V1 `get_all_topics_ordered`.
- The V1 regression test suite passes in full.

### V2 Format Correctness

**PASS.** V2 curricula load, validate, and import correctly.

- Section exam weights sum to 100% within the defined tolerance.
- `display_order` fields are positive and unique within their parent.
- `section_id` and `topic_id` cross-references are validated at load time.
- Cognitive level and learning type values are validated against the permitted enums.
- Import is idempotent: re-running against an already-imported curriculum does not create duplicate rows.

### Database Schema

**PASS.** The `Section` model and `Topic.section_id` foreign key are implemented correctly.

- Migration `202610070001` applies cleanly on a fresh database.
- Migration is reversible.
- The `flask backfill-sections` command correctly links existing V2 topics to their sections; it is idempotent and safe on production.

### Test Coverage

**PASS.** 977 automated tests pass. Zero failures.

| Test Suite | Count (approx.) | Status |
|---|---|---|
| Core models and services | 450+ | PASS |
| Curriculum engine (V1 + V2) | 150+ | PASS |
| Routes and blueprints | 200+ | PASS |
| Auth, CLI, config, startup | 80+ | PASS |
| Section-aware integration | 50+ | PASS |
| Smoke tests | 20+ | PASS |

### Lint

One category of lint issues remains in `app/curriculum/validator.py`: five imported symbols from `app.curriculum.models` are unused. These imports were identified during the audit and are resolved as a pre-release blocker (see BLOCKER 2 in the release audit).

All other lint checks pass.

### Security

**PASS.** No security regressions were introduced.

- No new routes were added without `@login_required`.
- No user input is interpolated into SQL.
- No secrets were added to code or templates.
- CSP and security headers remain intact.

### Migration Safety

**PASS.** The migration chain was verified on both a fresh database and an existing database with V1 data.

- No production data is dropped by any migration in Epic 1.
- `StartupService` idempotency is preserved.
- Migration `202610070001` is the only schema change introduced in Epic 1.

---

## Outcomes / Follow-ups

### Accepted

Epic 1 is **accepted** as complete. The Curriculum Architecture Foundation is production-ready as of v0.4.0.

### Deferred Items

The following items were explicitly deferred and are recorded in `docs/TECHNICAL_DEBT_REGISTER.md`:

| ID | Description | Target |
|---|---|---|
| TD-001 | SQLAlchemy 2.x deprecation cleanup | Maintenance Sprint after Epic 2 |
| TD-002 | Large route module decomposition | Future Architecture Improvement |
| TD-003 | Further service decomposition | Epic 3+ |
| TD-004 | Remaining lint warnings (non-blocker) | Ongoing |
| TD-005 | SQLAlchemy warning cleanup | Maintenance Sprint |
| TD-006 | Architecture Guardian pre-existing findings | Epic 3 |
| TD-007 | Performance optimisation for curriculum queries | When scale justifies |

No new technical debt was accepted during Epic 1.

### Pre-Release Blockers (resolved before v0.4.0 release)

The engineering audit identified three pre-release blockers:

1. **Placeholder documentation** — Three files (`ADR-001-Curriculum-Hierarchy.md`, `EPIC_1_COMPLETION_REVIEW.md`, `CURRICULUM_ARCHITECTURE_REVIEW.md`) existed as stubs and required completion.
2. **Unused imports in `validator.py`** — Five unused model imports reported by ruff.
3. **Repository cleanliness verification** — Confirmation that no debug code, temporary comments, or placeholder content remained.

All three blockers are resolved as part of release preparation.

### Next Epic

Epic 2 (Educational Intelligence) will begin after v0.4.0 is released.

Epic 2 capabilities include:

- Behaviour Engine
- Performance Engine
- Readiness Aggregation
- Decision Engine
- Explainable Recommendations
- Section-weighted recommendation scoring

Epic 2 depends on the stable V2 curriculum hierarchy delivered by Epic 1.

---

## Release Recommendation

**GO for v0.4.0 release.**

The Curriculum Architecture Foundation is complete, tested, backwards-compatible, and architecturally sound. The three pre-release blockers have been resolved. No known regressions exist. The test suite passes in full.
