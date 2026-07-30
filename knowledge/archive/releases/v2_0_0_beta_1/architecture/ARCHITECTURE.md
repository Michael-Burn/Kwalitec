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
├── presentation/student/ Blueprint("student", url_prefix="/student")   # canonical Dashboard
├── presentation/session/ Blueprint("session", url_prefix="/session")   # Session Experience
├── dashboard/            Blueprint("dashboard", ...)   # legacy shell → redirects under sole runtime
├── mission/              Blueprint("mission", url_prefix="/missions")  # legacy LXP shell
├── study_plan/           Blueprint("study_plan", url_prefix="/study-plan")
├── analytics/            Blueprint("analytics", ...)   # legacy shell → History under sole runtime
├── settings/             Blueprint("settings", ...)
├── research/             Blueprint("research", url_prefix="/research")
├── calibration/          Blueprint("calibration", ...)
└── founder/dashboard/    Blueprint("founder_dashboard", url_prefix="/founder")
```

| Blueprint | Audience | Notes |
|---|---|---|
| `auth` | All | Invite-only login; no public registration |
| `student` / `session` | Students | **Canonical Education Operating System** (V2-023 sole runtime) |
| `dashboard` / `mission` / `analytics` | Students | Legacy presentation shells; redirect under `KWALITEC_V2_SOLE_RUNTIME` |
| `study_plan` / `settings` | Authenticated | Shared workflow surfaces (Study Plan wizard, account settings) |
| `research` | Students | Product Check-in intake (`/research/checkin`) |
| `founder_dashboard` | Founders | Command Centre — Overview, **Operational Health**, Feedback, Vision Journal, Research, Releases |
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
│   ├── base.html              # DEP-003 router → EOS or legacy workspace
│   ├── eos_student.html       # Certified Education OS shell (sole runtime)
│   ├── legacy_workspace.html  # Legacy Contained shell (dual-run soak)
│   └── auth_base.html         # Unauthenticated layout
├── partials/                  # brand_*, flash, explainability, legacy sidebar/topnav
├── student/                   # Certified Home / Journey / Revision / History / …
├── session/                   # Certified Session Experience
├── auth/
├── dashboard/                 # Legacy Contained — READY FOR MIGRATION
├── mission/                   # Legacy LXP Contained — READY FOR MIGRATION
├── study_plan/                # Shared workflow (chrome via base router)
├── analytics/                 # Legacy Contained — READY FOR MIGRATION
├── settings/
├── research/                  # Product Check-in (student)
├── calibration/
├── errors/
└── (Founder) app/founder/dashboard/templates/founder_dashboard/
```

Conventions:

- **Authoritative student presentation** is the Education OS under `KWALITEC_V2_SOLE_RUNTIME` (`student` + `session` templates). See `knowledge/release/RR-002/RR002_3_RUNTIME_OWNERSHIP.md`.
- Extend `layouts/base.html` for authenticated pages that must follow DEP-003 chrome routing (EOS vs legacy).
- Do **not** extend legacy `dashboard/`, `mission/`, or `analytics/` templates for new educational features — they redirect under sole runtime and are Contained soak only.
- Keep feature templates in the matching folder name.
- Prefer partials for repeated chrome; avoid duplicating nav markup.
- Pass a `title` into the layout when possible.
- User-facing Founder / workspace labels come from `app/brand_identity.py` (e.g. Founder Command Centre, Learning Workspace, Revision Workspace, Operational Health).
- Legacy inventory and cleanup candidates: `knowledge/release/RR-002/RR002_3_LEGACY_INVENTORY.md`.

---

## JavaScript Layer

```
app/static/js/
├── app.js              # Shared behaviours
├── study_session.js    # Study session interactions (legacy dual-run soak)
└── theme.js            # Appearance / theme
```

CSS:

```
app/static/css/
├── app.css
└── wizard.css
```

Founder Command Centre CSS lives under `app/founder/dashboard/static/css/`.

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
| `flask create-admin` | Create initial admin from `ADMIN_EMAIL`/`ADMIN_PASSWORD` (skips if any user exists) |
| `flask sync-admin` | Sync admin password + Founder RBAC from env (explicit; local/dev QoL) |
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

## Curriculum Intelligence Pipeline (CIP-001 / CIP-002 / CIP-003)

Founder-uploaded curriculum PDFs (CS-DOC-001) feed a deterministic pipeline that
produces structured educational knowledge for the Student Digital Twin roadmap.

CIP-002 adds provenance, confidence, graph validation, Founder review, audit,
and quality metrics on top of CIP-001 artefacts. CIP-003 adds the canonical
**evidence retrieval** layer (`CurriculumRetrievalService`) — embeddings are
one strategy behind `VectorStorePort`; consumers never query vectors directly.

```
Upload (CS-DOC-001)
  → Verify → Extract → Normalize → Structural Parse
  → Curriculum Map → Knowledge Graph → Ready for Embeddings
       ↘ CIP-002 evidence: provenance · confidence · validation · review · audit
       ↘ CIP-003 index: entity embeddings → CurriculumRetrievalService
```

| Concern | Location |
|---|---|
| Domain contracts / state machine | `app/domain/curriculum_intelligence/` |
| Evidence retrieval domain | `app/domain/curriculum_retrieval/` |
| Application services | `app/application/curriculum_intelligence/` |
| Retrieval services | `app/application/curriculum_retrieval/` |
| pypdf + processing adapter | `app/infrastructure/adapters/curriculum_intelligence/` |
| Vector / embedding adapters | `app/infrastructure/adapters/curriculum_retrieval/` |
| Normalised tables | `app/models/curriculum_intelligence.py` |
| CIP-001 design notes | `knowledge/product/cip001/ARCHITECTURE.md` |
| CIP-002 design notes | `knowledge/product/cip002/ARCHITECTURE.md` |
| CIP-003 design notes | `knowledge/product/cip003/ARCHITECTURE.md` |

Invariant: extraction artefacts never write directly into student Topic/Mission
entities; OCR/LLM remain out of scope. Vector technology stays behind ports.

---

## Student Digital Twin Foundation (SDT-001)

Canonical representation of the learner — the sole source of truth for evolving
educational state. Complements Curriculum Intelligence (WHAT) with the Twin
(WHO). Facts (observations) are append-only; inferences are reproducible via
`StudentReasoningService`, which **delegates educational logic** to the
Educational Reasoning Engine (SDT-002). Curriculum evidence is retrieved
exclusively through `CurriculumRetrievalService` (never vector store / graph /
embeddings directly).

```
Observation (fact)
  → Educational Reasoning Engine (SDT-002 rules)
       → Mastery · Confidence · Momentum · Consistency · Readiness
       → Knowledge Gaps / Prerequisites (via CurriculumRetrievalService)
       → Recommendations
  → StudentDigitalTwin aggregate
```

| Concern | Location |
|---|---|
| Domain aggregate | `app/domain/student_digital_twin/` |
| Application / Twin orchestration | `app/application/student_digital_twin/` |
| ORM tables | `app/models/student_digital_twin.py` |
| Founder diagnostics | `/founder/twin/*` (`app/presentation/student_digital_twin/`) |
| Design notes | `knowledge/product/sdt001/ARCHITECTURE.md` |

No LLM. No student-facing Twin UX in SDT-001. Future Adaptive Mission Engine,
Revision Planner, and Tutor must consume this Twin rather than inventing
parallel learner models.

---

## Educational Reasoning Engine (SDT-002)

Deterministic, explainable educational inference pipeline. Every educational
decision that updates the Student Digital Twin must be produced by this engine.
Independent of UI, missions, tutoring, and LLMs.

```
Observation
  → Retrieve Supporting Curriculum Evidence (CIP-003)
  → Apply Educational Rules (RuleRegistry)
  → Generate Educational Inference
  → Update Student Digital Twin
  → Record Reasoning History (immutable)
```

| Concern | Location |
|---|---|
| Domain (rules, registry, engine) | `app/domain/educational_reasoning/` |
| Application (evidence, persistence) | `app/application/educational_reasoning/` |
| ORM metadata tables | `app/models/educational_reasoning.py` |
| Founder diagnostics | `/founder/reasoning/*` |
| Design notes | `knowledge/product/sdt002/ARCHITECTURE.md` |

Rule types: mastery update, confidence adjustment, knowledge gap detection,
prerequisite analysis, recommendation, learning momentum, consistency,
readiness contribution. New rules are pluggable via `RuleRegistry` without
modifying existing rules. Reasoning history tables store metadata only — they
do not duplicate Twin inference rows. Prerequisite / recovery rules prefer
Learning Graph traversal when a graph is attached to `ReasoningContext`
(SDT-003).

---

## Learning Graph (SDT-003)

Canonical representation of how a learner's knowledge is interconnected.
Complements Curriculum Intelligence (WHAT) and the Student Digital Twin (WHO)
with relational prerequisite / dependency structure. One Learning Graph exists
per Twin. Twin mastery remains the source of truth; the graph stores structure
and mastery links, not duplicated inference rows.

```
Curriculum evidence (CIP-003)
  → Sync Learning Graph (nodes from Twin, edges from retrieval)
  → Educational Reasoning rules traverse prerequisites / recovery paths
  → Update Student Digital Twin
  → Refresh graph mastery projections
```

| Concern | Location |
|---|---|
| Domain aggregate + traversal | `app/domain/learning_graph/` |
| Application (sync, traversal) | `app/application/learning_graph/` |
| ORM structure tables | `app/models/learning_graph.py` |
| Founder diagnostics | `/founder/learning-graph/*` |
| Design notes | `knowledge/product/sdt003/ARCHITECTURE.md` |

No LLM. No student-facing Learning Graph UX in SDT-003. The Adaptive Mission
Engine (AME-001), Revision Planner, and Tutor must use this graph for
prerequisite reasoning rather than inventing isolated concept heuristics.

---

## Adaptive Mission Engine (AME-001)

Transforms educational decisions into one actionable daily learning mission.
Consumes Student Digital Twin state, Educational Reasoning decisions, Learning
Graph recovery structure, and Curriculum Retrieval evidence. Never performs
educational reasoning itself. Not a timetable — today's optimal learning plan.

```
Student Digital Twin
  → Educational Reasoning decisions (already on Twin)
  → Learning Graph recovery / prerequisites
  → Curriculum Retrieval (evidence enrichment)
  → Prioritise → Construct → Validate
  → Daily Adaptive Mission (one active per learner)
```

| Concern | Location |
|---|---|
| Domain aggregate + prioritisation / validation | `app/domain/adaptive_mission/` |
| Application orchestration | `app/application/adaptive_mission/` |
| ORM tables | `app/models/adaptive_mission.py` |
| Founder diagnostics | `/founder/missions/*` |
| Design notes | `knowledge/product/ame001/ARCHITECTURE.md` |

No LLM. Student Mission card UX unchanged in AME-001; `as_mission_card()`
provides a simple projection for future integration.

---

## Assessment & Learning Feedback Pipeline (AP-001)

Closes the adaptive learning loop: learner activity becomes structured
educational evidence that updates the Student Digital Twin. Never performs
educational reasoning — delegates Twin updates to `StudentReasoningService`.

```
Learner Activity
  → Validation → Assessment Event
  → Observation (SDT-001 fact)
  → StudentReasoningService / Educational Reasoning Engine
  → Student Digital Twin Update
  → Learning Feedback
  → Mission Refresh Trigger (AME-001)
```

| Concern | Location |
|---|---|
| Domain (events, feedback, validation) | `app/domain/assessment_pipeline/` |
| Application orchestration | `app/application/assessment_pipeline/` |
| ORM tables | `app/models/assessment_pipeline.py` |
| Founder diagnostics | `/founder/assessment/*` |
| Design notes | `knowledge/product/ap001/ARCHITECTURE.md` |

Mission progress/completion emits assessment events via
`AdaptiveMissionService` hooks. Future Tutor, Revision Planner, Exam Readiness
Forecasting, and Educational Analytics must consume the evolving Twin rather
than inventing parallel learner state. No LLM. Student dashboard unchanged.

---

## Evidence-Backed Intelligent Tutor (TUTOR-001)

Transforms educational intelligence into personalised, explainable guidance.
The Tutor **explains** decisions already produced by Educational Reasoning,
the Student Digital Twin, Learning Graph, Adaptive Missions, and Assessment
Feedback — it never becomes another reasoning engine.

```
Student Question
  → Student Digital Twin
  → Educational Reasoning decisions (already on Twin)
  → Learning Graph
  → Curriculum Retrieval (TUTOR profile)
  → Evidence Assembly → Explanation Builder
  → TutorGenerationPort (deterministic V1 placeholder)
  → Tutor Response
```

| Concern | Location |
|---|---|
| Domain (session, context, evidence, response) | `app/domain/intelligent_tutor/` |
| Application orchestration + generation port | `app/application/intelligent_tutor/` |
| ORM conversation tables | `app/models/intelligent_tutor.py` |
| Founder diagnostics | `/founder/tutor/*` |
| Student surface | Home Coach preview + `/student/tutor/explain-mission` |
| Design notes | `knowledge/product/tutor001/ARCHITECTURE.md` |

Conversation memory is session-scoped only. Twin remains the learner-state
system of record. Future LLM adapters replace `DeterministicTutorGeneration`
behind `TutorGenerationPort` without changing Tutor architecture.

---

## Related Rules

| Rule file | Topic |
|---|---|
| `01-architecture.mdc` | Layering principles |
| `03-flask.mdc` | Blueprint / factory conventions |
| `04-services.mdc` | Service boundaries |
| `08-curriculum-v2.mdc` | V1/V2 + traversal invariants |
| `09-ui-templates.mdc` | Jinja / CSS / JS |
