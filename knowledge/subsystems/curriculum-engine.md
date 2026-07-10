# Curriculum Engine

## Purpose

The Curriculum Intelligence Engine (`app/curriculum/`) is the **in-memory, deterministic** source of truth for official examination syllabuses before (and alongside) database import. Every educational feature — study planning, missions, readiness, recommendations, analytics — ultimately depends on syllabus structure that originates here.

Kwalitec’s product thesis is curriculum-first: recommendations are grounded in official topics and weights, not in opaque ML models or external LLM APIs.

## Responsibilities

| Responsibility | Module / API |
|---|---|
| Load JSON from `app/curriculum/data/{org}/{paper}/{year}.json` | `loader.py` |
| Detect V1 vs V2 format | loader / repository |
| Validate JSON shape | `schemas.py` |
| Enforce business rules (weights, unique codes, prerequisites) | `validator.py` |
| Build dataclasses (V1 and V2 `*Definition` types) | `models.py` |
| Cache and query loaded curricula | `repository.py` |
| Bootstrap bundled curricula | `seed.py` |
| Bridge to services | `CurriculumEngineService` (thin) |
| Persist into SQLAlchemy | `CurriculumService.import_curricula()` |

Engine dataclasses are **not** ORM models. Naming overlap is historical; V2 uses `CurriculumDefinition`, `SectionDefinition`, `TopicDefinition`, `LearningObjectiveDefinition`.

## Dependencies

```
JSON files on disk
        ↓
Curriculum Engine (loader → schema → dataclasses → validator → repository)
        ↓
CurriculumEngineService  (thin repository bridge)
        ↓
CurriculumService        (import + DB traversal + progress)
        ↓
Study planning / missions / readiness / recommendations / analytics
```

- **Depends on:** filesystem JSON, Python dataclasses, project schemas/validators.
- **Does not depend on:** Flask request context, blueprints, or learner progress tables.
- **Consumed by:** `CurriculumEngineService`, `CurriculumService`, and indirectly all learning services.

## Data Flow

```
JSON on disk
    → loader (format detect V1/V2)
    → schemas.validate_instance()
    → dataclass build
    → validator (business rules)
    → CurriculumRepository cache
    → CurriculumEngineService / CurriculumService.import_curricula()
    → SQLAlchemy Curriculum / Section? / Topic / LearningObjective
```

### V1 vs V2 (after import)

```
V2                              V1
Curriculum                      Curriculum
  └─ Section (display_order)      └─ Topic tree (parent_topic_id, order)
       └─ Topic (order)                section_id NULL
            section_id set
```

Canonical **DB** ordering after import is owned by `CurriculumService` — see [ADR-004](../architecture/ADR-004-canonical-topic-traversal.md).

## Extension Points

- **New paper / year:** add JSON under `data/{org}/{paper}/{year}.json`; prefer V2 shape for new syllabuses ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md)).
- **New examining body:** new `org` folder + metadata; avoid hard-coding org names in services.
- **New validation rules:** extend `validator.py` deterministically; add engine tests.
- **New query helpers:** prefer `CurriculumRepository` / `CurriculumEngineService` for in-memory needs; prefer `CurriculumService` for DB product features.

## Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Treating engine dataclasses as ORM models | Wrong session/identity; import bugs |
| Bypassing `CurriculumService` for DB topic order | V1/V2 divergence ([ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)) |
| Assuming every curriculum has sections | Breaks V1 plans and missions |
| Non-idempotent import | Duplicate topics on re-run / startup |
| Renaming stable topic ids | Orphans `TopicProgress` / attempts |
| Putting learner mastery into the engine | Engine is syllabus truth, not progress |

## Future Improvements

- Broader V2 syllabus coverage (additional IFoA papers and other bodies).
- Explicit V1→V2 migration milestone for remaining flat JSON (only with dual-run tests).
- Clearer public API exports in `app/curriculum/__init__.py` as formats stabilise.
- Stronger documentation of weight-sum rules per examining body.

**See also:** [`app/curriculum/README.md`](../../app/curriculum/README.md), [ADR-003](../architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](../architecture/ADR-004-canonical-topic-traversal.md).
