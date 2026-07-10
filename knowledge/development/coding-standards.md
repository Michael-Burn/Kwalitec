# Coding Standards

Standards for human and AI contributors. Enforceable Cursor rules live under [`.cursor/rules/`](../../.cursor/rules/); this document summarises what “good Kwalitec code” looks like in practice.

## Python style

| Rule | Detail |
|---|---|
| Version | Python **3.11+** (`pyproject.toml`) |
| Future annotations | `from __future__ import annotations` in app modules that declare types |
| Generics | Prefer `list[str]`, `dict[str, Any]` over `typing.List` |
| Lint | `ruff check app/ tests/` — selects `E`, `F`, `I`, `N`, `W`, `UP` |
| Quotes | Double quotes |
| Indentation | Spaces; match surrounding file |
| Logging | `logger = logging.getLogger(__name__)`; no `print()` in committed code |
| Exceptions | Avoid bare `except:`; startup paths may catch broad `Exception` with logging |

Keep functions focused. Extract helpers rather than growing 200-line route handlers. Do not reformat unrelated files while fixing a bug.

## Flask style

- **Application factory only:** `create_app()` in `app/__init__.py` is the sole construction path.
- **Blueprints for HTTP:** feature packages under `app/auth`, `app/mission`, etc.; register via `_register_blueprints()`.
- **Thin routes:** authenticate → validate → call service → render/redirect ([ADR-002](../architecture/ADR-002-blueprint-architecture.md)).
- **Forms:** WTForms / Flask-WTF for POST; CSRF on outside tests.
- **Templates:** Jinja2 under `app/templates/` mirroring feature folders; extend `layouts/base.html` when authenticated.
- **Config:** Development/Production in `app/config.py`; secrets from environment.

Do not put planning, mastery, or readiness math in routes.

## Service rules

- Business logic lives in `app/services/` ([ADR-001](../architecture/ADR-001-service-layer.md)).
- Pass `user_id`, models, and primitives explicitly — do not import `flask.request` or `session`.
- Return models, dataclasses, or plain dicts — not rendered HTML.
- One primary domain per service module.
- Curriculum DB ordering: only via `CurriculumService` helpers ([ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)).
- `CurriculumService.import_curricula()` and `StartupService` must remain idempotent / non-destructive as designed.
- Static methods on service classes are common in this repo — match local style.

## Naming conventions

| Kind | Convention | Examples |
|---|---|---|
| Blueprints | package + `*_bp` | `auth_bp`, `mission_bp` |
| Services | `*_service.py` / `*Service` | `ReadinessService` |
| ORM models | singular nouns in `app/models/` | `StudyPlan`, `MissionTask` |
| Engine V2 types | `*Definition` suffix | `TopicDefinition` |
| Tests | `test_*.py` under `tests/` | `test_curriculum_engine_v2.py` |
| Migrations | Alembic under `migrations/versions/` | timestamped revision ids |

Prefer clarity over clever abbreviations. Stable curriculum/topic ids are part of the data contract — do not rename casually.

## Documentation expectations

- Public service methods: clear purpose plus Args / Returns / Raises when useful.
- Milestone completion: report sections per `.cursor/rules/07-reporting.mdc`.
- Architectural changes: update or add ADRs under `knowledge/architecture/` and note V1/V2 impact.
- Do not add markdown files the milestone did not ask for; do not leave placeholder “TBD” docs.

## Type hints

- Annotate public service method signatures.
- Prefer built-in generics and `|` unions on 3.11+.
- Avoid noisy `# type: ignore` without cause.
- Engine and ORM types with similar names must not be mixed without explicit conversion on import.

## Testing expectations

- Add or update tests for behaviour you change ([ADR-005](../architecture/ADR-005-testing-strategy.md)).
- Curriculum changes: V1 regression **and** V2/section-aware coverage when relevant.
- Commands before claiming done:

```bash
python -m pytest tests/ -v
ruff check app/ tests/
```

- Do not weaken assertions to green CI.
- Prefer deterministic tests (inject dates; use `conftest.py` factories).

## Out of scope for “drive-by” edits

- New dependencies without clear need
- Unrelated refactors
- Editing `.venv`, `__pycache__`, `.pytest_cache`
- Committing `.env` or secrets

**See also:** [`CONTRIBUTING.md`](../../CONTRIBUTING.md), `.cursor/rules/02-python.mdc`, `03-flask.mdc`, `04-services.mdc`.
