# Kwalitec Project Index

**Purpose:** Minimise Cursor search effort. Concise map of packages, responsibilities, and entry points.

**Orientation:** Read this first, then [`.cursor/rules/99-CURRENT_MILESTONE.md`](rules/99-CURRENT_MILESTONE.md) for active scope.

---

## Repository layout

```
kwalitec/
├── .cursor/              # Cursor governance (this framework)
├── src/                  # Educational OS (V2/V3 authority) — hexagonal
│   ├── domain/           # Pure educational logic
│   ├── application/      # Use-cases, pipeline, ports, DTOs
│   ├── infrastructure/   # SQLAlchemy, security, AI, runtime
│   ├── adapters/         # Flask HTTP adapters
│   ├── presentation/     # View models, design system, templates logic
│   └── web/              # Web app factory (Flask wiring)
├── app/                  # Legacy V1 Flask product (coexists during migration)
├── tests/                # pytest suite + architecture gates
├── migrations/           # Alembic (V1 schema)
├── docs/                 # Architecture constitution, ADRs, dependency rules
├── knowledge/            # Product, design, and education deep docs
├── PROJECT_CONTEXT.md    # Product orientation
└── ARCHITECTURE.md       # Legacy application map
```

---

## Educational OS (`src/`)

### Domain (`src/domain/`)

Pure Python. Zero framework dependencies.

| Package | Responsibility |
|---|---|
| `education/` | Educational Core: evidence, digital twin, diagnosis, hypothesis, priority, intention, strategy, orchestrator, learning episodes, subject knowledge |
| `mission_generation/` | Deterministic `MissionSpecification` |
| `study_planning/` | Deterministic `StudyPlan` |
| `progress_evaluation/` | Deterministic `ProgressReport` |
| `recommendation/` | Deterministic `RecommendationSpecification` |
| `explainability/` | `EducationalExplanation` + decision trace |
| `student_experience/` | Presentation projection only (non-authoritative) |
| `onboarding/` | Step payloads and validation |
| `auth/` | Auth domain rules |

**Primary aggregates:** `EducationalDigitalTwin`, `EvidenceRecord`, `MissionSpecification`, `StudyPlan`, `ProgressReport`, `RecommendationSpecification`.

### Application (`src/application/`)

Orchestration and ports. No Flask, no SQLAlchemy (except composition root wiring).

| Package | Responsibility |
|---|---|
| `pipeline/` | `EducationalPipeline` — end-to-end orchestration |
| `composition/` | Composition root; constructs wired container |
| `ports/` | Abstract repository and service ports |
| `commands/` / `queries/` / `handlers/` | CQRS-style use-cases |
| `read_models/` | Dashboard, missions, recommendations, progress, timeline |
| `services/` | Application services (dashboard, learning, planning, twin, assessment) |
| `onboarding/` | Onboarding orchestration + twin initialization |
| `evidence_capture/` | Session outcome → evidence mapping |
| `evidence_update/` | Twin evidence mutations |
| `session_runtime/` | Active learning session runtime |
| `auth/` | Auth use-cases (ports for hashing, users) |
| `dto/` | Application data transfer objects |
| `events/` | Domain event dispatch contracts |

**Key entry:** `application.composition.application_factory.create_application()`

### Infrastructure (`src/infrastructure/`)

Adapters implementing ports.

| Package | Responsibility |
|---|---|
| `persistence/` | SQLAlchemy models, repositories, unit of work, Alembic |
| `security/` | Argon2 password hasher |
| `ai/` | AI providers and enrichment (presentation only) |
| `runtime/` | Clock, UUID generators |
| `observability/` | Pipeline observer, logging |
| `config/` | Environment configuration |
| `composition/` | Infrastructure factories invoked from composition root |
| `resilience/` | Retry/circuit patterns |

### Adapters (`src/adapters/flask/`)

Flask-specific HTTP wiring.

| Package | Responsibility |
|---|---|
| `auth/` | Login, logout, session |
| `dashboard/` | Student dashboard routes |
| `mission/` | Mission workspace routes |
| `onboarding/` | Onboarding wizard routes |
| `reflection/` | Post-session reflection |
| `session/` | Learning session routes |
| `rendering/` | Jinja2 templates for EOS surfaces |
| `login/` | Login form adapter |

### Presentation (`src/presentation/`)

Framework-independent view layer.

| Package | Responsibility |
|---|---|
| `design_system/` | Tokens, components, layout, motion (V3) |
| `dashboard/` | Dashboard view models and mappers |
| `study_session/` | Session workspace presentation |
| `mission_workspace/` | Mission UI view models |
| `onboarding/` | Onboarding step presenters |
| `reflection/` | Reflection forms and mappers |

### Web (`src/web/`)

- `app.py` — Flask app factory for Educational OS surfaces
- `blueprints/` — Blueprint registration

---

## Legacy application (`app/`)

Historical V1 product. Still active for Internal Alpha dual-run.

| Area | Responsibility |
|---|---|
| `__init__.py` | `create_app()` — main WSGI entry |
| `auth/`, `dashboard/`, `mission/`, `study_plan/`, `analytics/`, `settings/` | V1 student blueprints |
| `founder/` | Founder Command Centre |
| `services/` | V1 business logic (planning, missions, recommendations, curriculum) |
| `models/` | V1 SQLAlchemy ORM |
| `curriculum/` | Curriculum Engine (JSON → dataclasses) |
| `templates/` + `static/` | V1 Jinja2 + CSS/JS |

**Entry points:** `run.py` (dev), `wsgi.py` (production).

---

## Testing structure (`tests/`)

| Directory | Scope |
|---|---|
| `architecture/` | Layer purity, composition root, pipeline, AI boundary gates |
| `domain/` | Domain engine unit tests |
| `application/` | Use-case and pipeline tests |
| `infrastructure/` | Repository and adapter tests |
| `presentation/` | View model and mapper tests |
| `education_os/` | End-to-end Educational OS integration |
| `curriculum/` | V1/V2 curriculum regression |
| `certification/` | Release certification harnesses |
| `operational/` | Ops and deployment checks |
| `conftest.py` | Shared fixtures (`app`, `db`, `client`) |

---

## Key relationships

```
HTTP Request
  → adapters.flask (route)
    → application service / handler
      → domain engine (decisions)
      → infrastructure repository (persist)
    → presentation mapper (view model)
  → Jinja2 template (render)
```

```
EducationalPipeline
  → domain engines (mission, plan, progress, recommendation, explainability)
  → student_experience (present)
  → infrastructure.ai (enrich wording)
  → PipelineResult → read models → presentation
```

---

## Important canonical documents

| Document | Use when |
|---|---|
| [`docs/ARCHITECTURE_CONSTITUTION.md`](../docs/ARCHITECTURE_CONSTITUTION.md) | Constitutional principles |
| [`docs/DEPENDENCY_RULES.md`](../docs/DEPENDENCY_RULES.md) | Import direction law |
| [`docs/ARCHITECTURE_OVERVIEW.md`](../docs/ARCHITECTURE_OVERVIEW.md) | Layer and subsystem map |
| [`docs/adr/`](../docs/adr/) | Binding ADRs (001–010) |
| [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) | Product and stack orientation |
| [`ARCHITECTURE.md`](../ARCHITECTURE.md) | Legacy V1 application map |
| [`.cursor/rules/00-CONSTITUTION.md`](rules/00-CONSTITUTION.md) | Cursor agent constitution |
| [`.cursor/ANTI_PATTERNS.md`](ANTI_PATTERNS.md) | What never to do |

---

## Configuration and deploy

| File | Role |
|---|---|
| `pyproject.toml` | pytest + ruff config |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deploy blueprint |
| `.env.example` | Local env template |
| `migrations/` | Alembic revisions |
