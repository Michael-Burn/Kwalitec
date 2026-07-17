# Kwalitec — Architecture

This document describes how Kwalitec is structured. For product context and status, see [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md). For workflow conventions, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Clients (Browser)                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTP
┌───────────────────────────────▼─────────────────────────────────┐
│                     Flask Application Factory                     │
│                        app/__init__.py                            │
│  create_app → config → extensions → blueprints → security/health │
└───┬───────────────┬───────────────┬───────────────┬─────────────┘
    │               │               │               │
    ▼               ▼               ▼               ▼
 Blueprints      Services      Curriculum       Models / DB
 (HTTP)       (business)      Engine (JSON)    (SQLAlchemy)
    │               │               │               │
    ▼               ▼               ▼               ▼
 Templates      Persistence    Repository      SQLite / Postgres
 + static       orchestration   + validation    via Alembic
```

**Invariant:** HTTP concerns stay in blueprints; domain rules stay in services; official syllabus truth stays in the Curriculum Engine until imported into the database.

---

## Blueprint Organisation

Blueprints are registered in `_register_blueprints()` inside `app/__init__.py`.

```
app/
├── auth/                 Blueprint("auth", url_prefix="/auth")
├── dashboard/            Blueprint("dashboard", ...)
├── mission/              Blueprint("mission", url_prefix="/missions")
├── study_plan/           Blueprint("study_plan", url_prefix="/study-plan")
├── analytics/            Blueprint("analytics", ...)
├── settings/             Blueprint("settings", ...)
├── research/             Blueprint("research", url_prefix="/research")
├── calibration/          Blueprint("calibration", ...)
└── founder/dashboard/    Blueprint("founder_dashboard", url_prefix="/founder")
```

| Blueprint | Audience | Notes |
|---|---|---|
| `auth` | All | Invite-only login; no public registration |
| `dashboard` / `mission` / `study_plan` / `analytics` | Students | Learning Workspace |
| `settings` | Authenticated | Includes Internal Alpha status |
| `research` | Students | Product Check-in intake (`/research/checkin`) |
| `founder_dashboard` | Founders | Command Centre — Overview, Feedback, Vision Journal, etc. |
| `calibration` | Operators | Calibration workflows |

### Blueprint responsibilities

| Concern | Belongs in blueprint | Does not belong in blueprint |
|---|---|---|
| Request/response | Yes | — |
| Form validation (WTForms) | Yes | — |
| Auth decorators (`login_required`) | Yes | — |
| Template selection / flash messages | Yes | — |
| Mastery scoring, planning math | No | Services |
| Curriculum import / traversal | No | `CurriculumService` / engine |
| Raw SQL / schema changes | No | Models + Alembic |

Typical route shape:

```
route → authenticate → validate form/input → call service → render template / redirect
```

---

## Service Layer

Services are plain Python classes/modules under `app/services/`. They:

- Accept domain primitives (user ids, model instances, dates)
- Orchestrate queries and writes through SQLAlchemy
- Return domain objects or plain dicts/dataclasses suitable for templates
- Do not import Flask request/session objects (prefer explicit arguments)

### Service map

```
                    ┌──────────────────────┐
                    │  Curriculum Engine    │
                    │  (app/curriculum/)    │
                    └──────────┬───────────┘
                               │
              ┌────────────────▼────────────────┐
              │ CurriculumEngineService          │
              │ (thin repository bridge)         │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │ CurriculumService                │
              │ import + DB traversal + progress │
              └────────────┬─────────────────────┘
                           │
     ┌───────────┬─────────┼─────────┬───────────┐
     ▼           ▼         ▼         ▼           ▼
 StudyPlan   Planning   Mission   Adaptive   Readiness
 Service     Service    /Optim.   Learning   /Recommend
     │           │         │         │           │
     └───────────┴─────────┴─────────┴───────────┘
                           │
                           ▼
                    Analytics / Dashboard
```

`StartupService` is orthogonal: production-only migration + admin bootstrap at app creation time.

---

## Database Layer

### Stack

- SQLAlchemy models in `app/models/`
- Session via `app.extensions.db`
- Schema evolution via Alembic under `migrations/versions/`
- Local default: SQLite file under `instance/`
- Production: PostgreSQL from `DATABASE_URL` (normalized for `psycopg`)

### Core domain tables (conceptual)

```
User
  ├── StudyPlan ──→ Curriculum
  │     └── WeekPlan
  ├── Mission ──→ MissionTask
  ├── TopicProgress ──→ Topic
  ├── StudyAttempt ──→ Topic
  ├── Mistake ──→ Topic
  └── Decision

Curriculum
  ├── Section (V2; optional for V1)
  └── Topic
        ├── section_id? (V2 link)
        ├── parent_topic_id? (V1 tree)
        └── LearningObjective
```

### Rules

- Prefer Alembic migrations over `db.create_all()` outside tests.
- Tests may use `create_all` / truncate for isolation (`tests/conftest.py`).
- Never drop production data in startup paths.
- Keep migrations reversible when practical; document irreversible steps.

---

## Template Layer

```
app/templates/
├── layouts/
│   ├── base.html          # Authenticated shell (sidebar + topnav)
│   └── auth_base.html     # Unauthenticated layout
├── partials/
│   ├── sidebar.html
│   ├── topnav.html
│   └── flash_messages.html
├── auth/
├── dashboard/
├── mission/
├── study_plan/            # list, view, edit, wizard_step_*.html
├── analytics/
├── settings/
└── errors/                # 403, 404, 500
```

Conventions:

- Extend `layouts/base.html` for authenticated pages.
- Keep feature templates in the matching folder name.
- Prefer partials for repeated chrome; avoid duplicating nav markup.
- Pass a `title` into the layout when possible.

---

## JavaScript Layer

```
app/static/js/
├── app.js          # Shared behaviours
└── mission.js      # Mission-specific interactions
```

CSS:

```
app/static/css/
├── app.css
└── wizard.css
```

Conventions:

- Prefer progressive enhancement; core flows must work without fragile client-side state.
- Keep JS feature-scoped; do not dump large frameworks into the repo.
- Bootstrap is loaded from CDN (see CSP in `app/__init__.py`).
- CSRF token is available via `<meta name="csrf-token">` in the base layout.

---

## Curriculum Engine

The Curriculum Engine (`app/curriculum/`) is an **in-memory, deterministic** subsystem separate from SQLAlchemy models.

```
JSON on disk
    → loader (format detect V1/V2)
    → schemas.validate_instance()
    → dataclass build
    → validator (business rules)
    → CurriculumRepository cache
    → CurriculumEngineService / CurriculumService.import_curricula()
    → SQLAlchemy Curriculum / Section / Topic / LearningObjective
```

### Package layout

```
app/curriculum/
├── models.py        # V1 + V2 dataclasses
├── schemas.py       # JSON schema + validation
├── loader.py        # I/O + format detection
├── validator.py     # Weightings, uniqueness, prerequisites
├── repository.py    # Cache + query API (load_auto canonical entry point)
├── seed.py          # Bootstrap bundled curricula
├── exceptions.py
└── data/{org}/{paper}/{year}.json
```

Engine models are **not** ORM models. Naming overlap (`Curriculum`, `Topic`) is intentional historically; V2 uses `*Definition` suffixes for clarity.

### Canonical loading — `load_auto()`

All application code that needs to load a curriculum **without knowing its format in advance** must use the canonical loader chain:

```python
# Engine layer (lowest level — repository)
repo.load_auto(organisation, paper, version)
    → Curriculum (V1) | CurriculumDefinition (V2)

# Service layer (recommended for application code)
engine_service.load_auto(exam, paper, version)
    → Curriculum (V1) | CurriculumDefinition (V2)
```

`load_auto()` tries V1 first (backwards compatibility), then falls back to V2.
Caller can detect the format afterwards: `isinstance(result, CurriculumDefinition)`.

**Never** duplicate the V1 → V2 try/except chain outside `CurriculumRepository`.

### Canonical engine flattening — `get_topics_flat()`

All code that needs a flat ordered topic list from an engine curriculum must use:

```python
CurriculumEngineService.get_topics_flat(curriculum)
    → list[Topic]          # V1: flat .topics list unchanged
    → list[TopicDefinition]  # V2: sections → topics in display_order
```

**Never** copy the `sorted(curriculum.sections, ...) for topic in sorted(...)` pattern
outside `CurriculumEngineService.get_topics_flat()`.

---

## Curriculum Traversal

### Engine-side (in-memory)

| Method | Where | Behaviour |
|---|---|---|
| `repo.load_auto(org, paper, ver)` | `CurriculumRepository` | Single V1/V2 loader |
| `engine.load_auto(exam, paper, ver)` | `CurriculumEngineService` | Public load_auto wrapper |
| `CurriculumEngineService.get_topics_flat(c)` | `CurriculumEngineService` | Flat ordered topic list |

### DB-side (SQLAlchemy)

Canonical DB traversal lives on `CurriculumService`:

| Method | Behaviour |
|---|---|
| `get_sections(curriculum)` | Sections by `display_order`; `[]` for V1 |
| `get_topics_for_section(section)` | Active topics by `Topic.order` |
| `get_all_topics_ordered(curriculum)` | V2: section then topic; V1: parent-tree DFS |
| `get_ordered_topics(curriculum)` | Alias → `get_all_topics_ordered` |
| `get_learning_objectives_for_topic(topic)` | Active LOs by `LearningObjective.order` |
| `get_next_incomplete_topic(...)` | First incomplete leaf in canonical order |

```
V2 path
────────
Curriculum
  └─ Section (display_order)
       └─ Topic (order)  [section_id set]
            └─ LearningObjective

V1 path
────────
Curriculum
  └─ Topic tree (parent_topic_id, order)  [section_id NULL]
       └─ LearningObjective
```

**Do not** reimplement ordering in planning, missions, or readiness. Call the helpers above.

---

## CLI Commands

| Command | Purpose |
|---|---|
| `flask create-admin` | Create initial admin from `ADMIN_EMAIL`/`ADMIN_PASSWORD` env vars |
| `flask backfill-sections` | Backfill Section rows + `Topic.section_id` for legacy V2 curricula |
| `flask db upgrade` | Apply Alembic migrations |

### `flask backfill-sections`

Run after `flask db upgrade` on any database that contains V2 `Curriculum` rows
imported **before** the sections migration (`202610070001`) was applied.

```bash
flask backfill-sections --dry-run  # preview changes
flask backfill-sections            # apply changes
```

The command is **idempotent**: already-linked topics are skipped.
Safe on production; no data is deleted.

---

## Dependency Flow

Allowed dependency direction (top depends on bottom):

```
Templates / JS
      ↓
Blueprints (routes, forms)
      ↓
Services
      ↓
Models + Curriculum Engine + Extensions (db)
      ↓
Database / JSON files
```

### Forbidden / discouraged

| Pattern | Why |
|---|---|
| Models importing blueprints | Circular / layer violation |
| Services importing `flask.request` | Hidden HTTP coupling |
| Routes containing planning math | Untestable business logic |
| Bypassing `CurriculumService` ordering | V1/V2 regressions |
| Writing secrets into templates or JS | Security |

### Startup sequence

```
create_app()
  → select config
  → logging + env validation
  → init extensions + import models
  → register blueprints, CLI, routes, error handlers, health
  → after_request security headers
  → log Alembic state (read-only)
  → StartupService.run(app)   # production only: migrate + admin
```

---

## Security Architecture (summary)

- Session auth via Flask-Login; login view `auth.login`.
- CSRF via Flask-WTF on state-changing forms.
- Security headers + CSP on every response (`_add_security_headers`).
- Open redirect protection on post-login `next` URLs (path-absolute only; rejects `//`, `///`, backslashes, and encoded bypasses).
- Production cookies: `Secure`, `HttpOnly`, `SameSite=Lax` for session and remember-me.
- Static assets: long-lived `Cache-Control` with `v=` fingerprint; HTML remains `no-store`.
- Registration not exposed; admin created via CLI or production startup.
- Secrets from environment (`.env` locally; Render env vars in production). Insecure `SECRET_KEY` is rejected whenever `ProductionConfig` is selected.

Details: [`.cursor/rules/10-security.mdc`](.cursor/rules/10-security.mdc).

---

## Testing Architecture

```
tests/
├── conftest.py                 # app, db, client, factories
├── test_models.py
├── test_services.py
├── test_routes.py
├── test_auth.py / test_cli.py / test_config.py
├── test_startup_service.py
├── test_curriculum_engine.py
├── test_curriculum_engine_v2.py
├── test_curriculum_importer.py
├── test_curriculum_section_aware.py
├── test_section_model.py
├── test_topic_section_relationship.py
├── test_time_engine.py
└── test_smoke.py
```

CI matrix: Python 3.11 / 3.12 / 3.13 + ruff + deploy dry-run on `main`.

---

## Related Rules

| Rule file | Topic |
|---|---|
| `01-architecture.mdc` | Layering principles |
| `03-flask.mdc` | Blueprint / factory conventions |
| `04-services.mdc` | Service boundaries |
| `08-curriculum-v2.mdc` | V1/V2 + traversal invariants |
| `09-ui-templates.mdc` | Jinja / CSS / JS |
