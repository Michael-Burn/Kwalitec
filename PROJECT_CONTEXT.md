# Kwalitec — Project Context

This document is the primary orientation guide for developers and AI agents working on Kwalitec. Read it before making architectural or product decisions. For structural detail, see [ARCHITECTURE.md](ARCHITECTURE.md). For contribution workflow, see [CONTRIBUTING.md](CONTRIBUTING.md). Cursor Agent rules live under [`.cursor/rules/`](.cursor/rules/).

---

## Purpose

Kwalitec is an adaptive learning platform for demanding professional examinations (actuarial, legal, medical, engineering, and similar qualifications).

Its product thesis is simple:

> **Reduce decisions. Increase learning.**

Students preparing for multi-month syllabuses struggle less with content than with the daily question of *what to study next*. Kwalitec answers that question deterministically from the student’s own performance history, available time, and exam deadline.

Kwalitec is **not** a generic study planner and **not** a black-box AI tutor. Core recommendations are explainable, reproducible, and grounded in curriculum structure plus learning data. There are no external LLM APIs in the recommendation path.

### Core product capabilities

| Capability | Role |
|---|---|
| Curriculum Intelligence Engine | Source of truth for official syllabuses (V1 flat + V2 hierarchical) |
| Study Plan Wizard | Exam-date-driven planning across available study days |
| Daily Mission Optimizer | Prioritized session tasks from urgency, readiness, and workload |
| Adaptive Learning | Spaced repetition and mastery scoring from real attempts |
| Exam Readiness Analytics | Coverage, projected pace, and pass-risk signals |
| Recommendation Engine | Deterministic, explainable “study next” suggestions |
| Decision Journal | Audit trail of accepted/dismissed recommendations |
| Burnout Monitor | Workload pacing and unsustainable-intensity flags |

---

## Technology Stack

| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| Web framework | Flask 3.1 (application factory) |
| ORM | Flask-SQLAlchemy 3.1 |
| Migrations | Flask-Migrate / Alembic |
| Auth | Flask-Login |
| Forms / CSRF | Flask-WTF + WTForms |
| Templates | Jinja2 |
| Frontend | Bootstrap 5.3 (CDN) + `app/static/css` + `app/static/js` |
| Local DB | SQLite (`instance/kwalitec.sqlite3`) |
| Production DB | PostgreSQL via `psycopg` (`DATABASE_URL`) |
| WSGI | Waitress (Render) / Gunicorn-compatible |
| Deploy | Render Blueprint (`render.yaml`) |
| Tests | pytest |
| Lint | ruff (target `py311`) |
| CI | GitHub Actions (`.github/workflows/ci.yml`) |

---

## Folder Structure

```
kwalitec/
├── .cursor/rules/           # Persistent Cursor Agent rules (this milestone)
├── prompts/                 # Reusable agent prompt templates
├── app/
│   ├── __init__.py          # create_app(), blueprints, security headers, health
│   ├── config.py            # Development / Production config
│   ├── extensions.py        # db, migrate, login_manager, csrf
│   ├── cli.py               # flask create-admin
│   ├── auth/                # Login / logout blueprint
│   ├── dashboard/           # Main dashboard blueprint
│   ├── mission/             # Daily missions blueprint
│   ├── study_plan/          # Study plan list + wizard blueprint
│   ├── analytics/           # Learning analytics blueprint
│   ├── settings/            # User settings blueprint
│   ├── models/              # SQLAlchemy ORM models
│   ├── services/            # Business logic (no HTTP)
│   ├── curriculum/          # In-memory Curriculum Engine (JSON → dataclasses)
│   │   └── data/            # Bundled syllabus JSON (e.g. ifoa/cs1/2026.json)
│   ├── templates/           # Jinja2 (layouts, partials, feature folders)
│   ├── static/              # css/, js/, images/
│   └── utils/               # Shared helpers
├── migrations/              # Alembic revision scripts
├── tests/                   # pytest suite
├── run.py                   # Local development entry
├── wsgi.py                  # Production WSGI entry
├── requirements.txt
├── pyproject.toml
├── render.yaml
├── PROJECT_CONTEXT.md       # This file
├── ARCHITECTURE.md
└── CONTRIBUTING.md
```

---

## Architectural Philosophy

1. **Curriculum first.** Educational features begin from official syllabus structure, not from heuristics or ML models.
2. **Deterministic by default.** Same inputs → same outputs. No randomness in core planning/recommendation paths.
3. **Blueprints for HTTP, services for logic.** Routes validate input, call services, render templates. Services own business rules and persistence orchestration.
4. **Thin routes, fat services (within reason).** Prefer extracting logic into `app/services/` over growing route modules.
5. **Explainability over opacity.** Recommendations and readiness scores must be traceable to curriculum weights, progress, and time constraints.
6. **Idempotent bootstrap.** Production startup (`StartupService`) and curriculum import are safe to re-run.
7. **Small, cohesive modules.** One responsibility per blueprint/service; avoid cross-cutting god objects.

See [ARCHITECTURE.md](ARCHITECTURE.md) for diagrams and dependency flow.

---

## Service-Layer Architecture

Business logic lives in `app/services/`. Representative services:

| Service | Responsibility |
|---|---|
| `curriculum_service.py` | DB curriculum import, section/topic traversal, progress helpers |
| `curriculum_engine_service.py` | Thin bridge over in-memory `CurriculumRepository` |
| `study_plan_service.py` | Study plan CRUD, wizard persistence, active plan |
| `planning_service.py` | Exam-date distribution and rebalancing |
| `mission_service.py` / `mission_optimizer.py` | Daily mission generation and task prioritization |
| `adaptive_learning_service.py` | Mastery / spaced-repetition scheduling |
| `learning_service.py` | Attempts, mistakes, learning records |
| `readiness_service.py` | Exam readiness metrics |
| `recommendation_service.py` | Explainable next-step recommendations |
| `analytics_service.py` | Dashboard/analytics aggregations |
| `time_engine_service.py` | Available study time calculations |
| `examination_catalogue.py` | Exam catalogue metadata |
| `exam_timeline.py` | Sitting dates and timeline helpers |
| `burnout_monitor.py` | Workload intensity signals |
| `startup_service.py` | Production-only migrate + admin bootstrap |

**Rule:** Prefer calling `CurriculumService` traversal helpers (`get_sections`, `get_topics_for_section`, `get_all_topics_ordered`) over ad-hoc topic queries so V1/V2 ordering stays consistent.

---

## Blueprint Architecture

| Blueprint | URL prefix | Purpose |
|---|---|---|
| `auth` | `/auth` | Login / logout (registration is not public) |
| `dashboard` | `/dashboard` | Home / overview |
| `mission` | `/missions` | Daily missions and review |
| `study_plan` | `/study-plan` | Plan list and multi-step wizard |
| `analytics` | `/analytics` | Performance analytics |
| `settings` | `/settings` | User preferences / backup |

App-level routes: `/` → dashboard redirect; `/health` public health check.

Blueprints are registered in `app/__init__.py` via `_register_blueprints()`.

---

## Curriculum V1 and V2 Compatibility

Kwalitec supports two curriculum formats simultaneously. This is a **hard architectural constraint**.

| Aspect | V1 (legacy / flat) | V2 (canonical / hierarchical) |
|---|---|---|
| Engine dataclasses | `Curriculum`, `Topic`, `LearningOutcome` | `CurriculumDefinition`, `SectionDefinition`, `TopicDefinition`, `LearningObjectiveDefinition` |
| Structure | Flat topic list | Section → Topic → Learning Objective |
| Exam weight | On topics (`syllabus_weight`) | On sections (`exam_weight`); topics import with weight `0.0` |
| DB sections | None | `Section` rows; `Topic.section_id` set |
| Canonical order | `parent_topic_id` depth-first via `Curriculum.get_all_topics_ordered()` | `Section.display_order` then `Topic.order` |
| Loader | `load_curriculum` / V1 path | `load_curriculum_v2` / V2 path |
| Detection | Engine auto-detects; import tries V1 then falls back to V2 |

**Compatibility rules (non-negotiable):**

- Existing V1 study plans, missions, and readiness calculations must keep working.
- `Topic.section_id` is nullable so V1 topics remain valid.
- Traversal must branch: if sections exist → V2 path; else → V1 path.
- Do not remove V1 loaders, schemas, or import paths without an explicit migration milestone.
- New syllabuses should prefer V2; the engine remains the source of truth under `app/curriculum/`.

Detailed rules: [`.cursor/rules/08-curriculum-v2.mdc`](.cursor/rules/08-curriculum-v2.mdc). Design background: `MILESTONE_1_1_CURRICULUM_MODEL_ANALYSIS.md`, `MILESTONE_1_2_CANONICAL_CURRICULUM_JSON_FORMAT.md`.

---

## Current Project Status

As of Milestone 0.1 (AI development infrastructure):

| Area | Status |
|---|---|
| Flask app factory, auth, CSRF, security headers | Stable |
| Study plan wizard, missions, analytics, settings | Stable |
| Adaptive learning, readiness, recommendations | Stable |
| Curriculum Engine (in-memory JSON) | Stable; V1 + V2 support in engine/services |
| DB `Section` model + `Topic.section_id` | Introduced (curriculum architecture track) |
| Production Render deploy + `StartupService` | Stable |
| Automated tests + CI (Python 3.11–3.13) | Active |
| Public self-registration | Intentionally disabled; admin via CLI / startup |
| AI development framework (this milestone) | Established |

Known operational note: local SQLite migration failures have been observed under disk I/O conditions (see `MIGRATION_INVESTIGATION_FINDINGS.md`). Treat migration health as environment-sensitive; prefer clean DB recreate when investigating schema issues locally.

---

## Development Philosophy

- Ship small, reviewable changes aligned to milestones.
- Prefer correctness and explainability over clever abstractions.
- Do not invent product features outside the stated milestone scope.
- Do not modify application code when the milestone is documentation-only.
- Keep secrets out of git (`.env` is local; use `.env.example` as the template).
- Match existing naming, typing (`from __future__ import annotations`), and docstring style.
- Lint with ruff; test with pytest before claiming completion.

---

## AI Workflow

Future Cursor Agent sessions should:

1. Read this file + [ARCHITECTURE.md](ARCHITECTURE.md) + relevant `.cursor/rules/*.mdc`.
2. Use a prompt from [`prompts/`](prompts/) when starting a feature, bugfix, refactor, migration, or review.
3. Respect milestone scope and “do not modify X” constraints literally.
4. Prefer services over routes for business logic; prefer curriculum helpers for traversal.
5. Produce a completion report per [`.cursor/rules/07-reporting.mdc`](.cursor/rules/07-reporting.mdc) when a milestone asks for one.
6. Commit only when explicitly requested (or when the milestone completion requirements mandate it).

---

## Testing Philosophy

- Tests live in `tests/` and use fixtures from `conftest.py` (temp SQLite, CSRF off, truncated tables per test).
- Cover models, services, routes, config, CLI, startup, and curriculum engine/import paths.
- Curriculum changes require V1 regression coverage **and** V2/section-aware coverage where applicable.
- CI runs pytest on Python 3.11, 3.12, and 3.13, plus ruff.
- Prefer focused unit/integration tests over brittle end-to-end UI scripts; smoke tests already cover critical workflows.

Run locally:

```bash
python -m pytest tests/ -v
ruff check app/ tests/
```

---

## Related Documents

| Document | Use when |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Need diagrams, layers, dependency flow |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Branching, commits, PRs, milestones |
| [README.md](README.md) | Setup, deploy, endpoint overview |
| `app/curriculum/README.md` | Curriculum Engine API and JSON conventions |
| `.cursor/rules/` | Always-on / scoped agent enforcement |
| `prompts/` | Starting a structured agent task |
