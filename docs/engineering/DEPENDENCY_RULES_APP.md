# Dependency Rules (app/)

**Programme:** V1S-003  
**Status:** Active  
**Effective:** 2026-07-31  
**Companion:** [`../DEPENDENCY_RULES.md`](../DEPENDENCY_RULES.md) governs `src/`.

---

## Allowed direction

```
presentation ──► application / services ──► domain
     │                    │                   ▲
     │                    ▼                   │
     └──────────► infrastructure ─────────────┘
                  (adapters; may read domain types)

curriculum (JSON engine) ◄── services / application (via CurriculumService / load_auto)
```

## Rules

1. **Presentation** may import application engines, services, and DTOs. It must not own educational evaluate math.
2. **Application** may import domain types and ports. Prefer injected infrastructure adapters over importing ORM sessions into engines.
3. **Domain** must not import Flask, blueprints, templates, or presentation packages.
4. **Services** may orchestrate models + application engines. Prefer not importing `flask.request`.
5. **Models** must not import blueprints or templates.
6. **Curriculum format detection** only via `CurriculumRepository.load_auto`.
7. **Archived packages** (`lifecycle=ARCHIVED` / `REMOVE`) must not gain new non-test imports from presentation or services.
8. **`app/` must not import `src.*` for dogfood product behaviour** (and vice versa for runtime coupling). Tests may import either tree.

## Educational authority consumption

Presentation and composers call:

- `get_*_engine()` factories for KWP authorities
- `compose_adaptive_workspace` for Home assembly
- `EducationalEvidenceAuthority` for evidence
- `ProgressEngine` for progress writes on Runtime C

They must not copy strategy / diagnostic / difficulty / forecast rules inline.

## Mission spine imports

Student Home / session paths may import:

- `educational_runtime_engine`
- `curriculum_intelligence.certified_mission_engine`
- `student_runtime`
- `learning_session`
- `educational_experience`
- KWP-007…015 packages + Adaptive Workspace

They must **not** import:

- `mission_engine_v2`
- `mission_adapter`
- Deprecated `mission_engine` shell (except founder Adaptive Mission → `planning/` until extract)

## Enforcement

- Static guards in programme tests (see `tests/test_v1s002_*.py`, `tests/test_v1s003_*.py`)
- Architecture purity suites under `tests/architecture/` for `src/`
- Package lifecycle matrix is the human-readable import policy map
