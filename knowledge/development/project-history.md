# Project History

Architectural evolution of Kwalitec, summarised for onboarding. This is a narrative companion to ADRs — decisions are normative in [`../architecture/`](../architecture/); this file explains how the system got there.

## Initial Flask architecture

Kwalitec began as a Flask application aimed at adaptive exam preparation: reduce daily study decisions, increase learning. Early structure used an application factory, SQLAlchemy models, Jinja templates, and feature routes for auth, planning, and missions. Local development defaulted to SQLite; production targeted PostgreSQL.

Product invariants were already present in spirit: curriculum-grounded recommendations, deterministic planning, and explainability over black-box tutoring.

## Package restructuring

As features grew, code moved into clearer packages:

- `app/models/` for ORM
- `app/templates/` and `app/static/` for UI
- `app/services/` for domain logic
- `migrations/` for Alembic
- `tests/` for pytest

The factory in `app/__init__.py` remained the single construction path (extensions, blueprints, security headers, health).

## Blueprint extraction

HTTP was split into feature blueprints (`auth`, `dashboard`, `mission`, `study_plan`, `analytics`, `settings`) with URL prefixes and matching template folders. This established the thin-route pattern documented in [ADR-002](../architecture/ADR-002-blueprint-architecture.md): routes validate and render; they do not own planning math.

## Service extraction

Business rules moved into `app/services/` ([ADR-001](../architecture/ADR-001-service-layer.md)): curriculum import/traversal, study plans, planning distribution, missions/optimizer, adaptive learning, readiness, recommendations, analytics, time engine, burnout monitor, and production `StartupService`. Services take explicit arguments and avoid Flask request globals.

## Curriculum Engine and V2

The Curriculum Intelligence Engine (`app/curriculum/`) made official syllabus JSON the in-memory source of truth: load → validate → repository → import to DB. Initially **V1** flat topic lists sufficed.

Hierarchical official syllabuses drove **V2**: Section → Topic → Learning Objective, section-level exam weights, and DB `Section` with nullable `Topic.section_id`. Coexistence of V1 and V2 became a hard constraint ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md)). Design background: `MILESTONE_1_1_CURRICULUM_MODEL_ANALYSIS.md`, `MILESTONE_1_2_CANONICAL_CURRICULUM_JSON_FORMAT.md`.

## Canonical traversal

Duplicate “list topics in order” logic across planning, missions, and readiness risked silent V1/V2 bugs. Ordering was centralised on `CurriculumService.get_all_topics_ordered()` and related helpers ([ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)). Callers must not reimplement the branch.

## AI engineering standards

Milestone 0.1 established durable AI/dev infrastructure:

- `PROJECT_CONTEXT.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`
- `.cursor/rules/*.mdc` for always-on and scoped enforcement
- `prompts/` for feature, bugfix, refactor, migration, and review starts

Milestone 0.2 (this knowledge base) preserves **why** decisions exist and how subsystems work, so agents and developers can extend the app without rediscovering constraints from chat history.

## Testing and CI maturation

Pytest harness with temp SQLite, CSRF-off test config, smoke tests, and curriculum V1/V2 suites landed alongside ruff and GitHub Actions across Python 3.11–3.13 ([ADR-005](../architecture/ADR-005-testing-strategy.md)).

## Operational notes

- Production deploy via Render (`render.yaml`) with Waitress-compatible WSGI.
- `StartupService` performs production-only migrate + admin bootstrap; must stay idempotent and non-destructive.
- Local SQLite migration issues have been observed under disk I/O stress (`MIGRATION_INVESTIGATION_FINDINGS.md`); treat migration health as environment-sensitive.

## Future roadmap (directional)

Not commitments — themes that architecture should anticipate:

| Theme | Architectural implication |
|---|---|
| More V2 syllabuses / examining bodies | Engine data folders + import idempotency |
| Possible V1 retirement | Explicit migration milestone + dual-run tests |
| Richer readiness / recommendations | Keep determinism and explainability; no core LLM dependency |
| Coach / multi-role auth | Extend authz carefully; keep ownership scoping |
| Analytics depth | Share definitions with readiness; avoid formula forks |

**See also:** [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) “Current Project Status”, [ai-workflow.md](ai-workflow.md).
