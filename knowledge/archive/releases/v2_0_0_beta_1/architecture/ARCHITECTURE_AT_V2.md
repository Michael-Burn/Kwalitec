# ARCHITECTURE AT V2.0.0-beta.1

**Snapshot date:** 2026-07-30  
**Source of truth at archive:** repository `ARCHITECTURE.md` (copied to this folder) plus RC-001 deployment topology.  
**Rule:** Describe the system as it existed at Private Beta release — **no future ideas**.

---

## 1. System overview

Kwalitec is a Flask commercial adaptive-learning product for professional exam preparation.

```
Browser
  → Flask application factory (app/__init__.py)
      → Blueprints (HTTP)
      → Services / application packages (domain)
      → Curriculum Engine (JSON, deterministic)
      → SQLAlchemy models + Alembic
      → SQLite (local) / PostgreSQL (production)
```

**Invariant:** HTTP stays in blueprints; domain rules in services/application; official syllabus truth starts in the Curriculum Engine until imported or published into runtime packages.

Invite-only authentication (no public registration). Production boots via `StartupService` (idempotent migrate + admin). Student canonical UI is the Education Operating System under V2 sole-runtime flags.

---

## 2. Major modules

| Area | Location | Role at V2 beta |
|---|---|---|
| App factory & security | `app/__init__.py` | Config, extensions, blueprints, CSP/headers, health |
| Auth | `app/auth/` | Login, session, open-redirect rejection |
| Student presentation | `app/presentation/student/`, `session/` | Canonical EOS: Home, Journey, Tutor, KG, sessions |
| Founder Console | `app/founder/dashboard/` | Command Centre, Studio, Curriculum Health, Beta Dashboard |
| Curriculum Studio (HTTP) | `app/presentation/curriculum_studio/` | Founder curriculum authoring surfaces |
| Services | `app/services/` | Planning, missions, readiness, twin-related helpers, private beta, health |
| Application packages | `app/application/` | Educational intelligence, publishing, twin, tutor, mission engines |
| Curriculum Engine | `app/curriculum/` | V1/V2 JSON load, validate, import bridge |
| Models | `app/models/` | Persistence (~145 table names) |
| Migrations | `migrations/versions/` | Alembic; head at release `202607300005` |
| Static / templates | `app/static/`, `app/templates/` | EOS + legacy soak shells |

**Registered blueprints (21):** auth, analytics, dashboard, mission, settings, study_plan, calibration, founder_dashboard, research, alpha, student, session, assessment, adaptive_assessment, studio, twin_diagnostics, reasoning_diagnostics, learning_graph_diagnostics, adaptive_mission_diagnostics, assessment_pipeline_diagnostics, intelligent_tutor_diagnostics.

Legacy student shells (`dashboard` / `mission` / `analytics`) redirect under sole runtime; they are Contained soak, not the primary product UI.

---

## 3. Educational Engine

At beta.1 the educational stack includes:

- **Curriculum Intelligence Pipeline (CIP)** — document extraction, structural nodes, provenance, confidence, validation reports (`cip_*` tables; `app/application/educational_intelligence_pipeline/`, curriculum extraction packages).
- **Curriculum Intelligence Generations (EI-001)** — generation chains, snapshots, educational nodes, regression reports, calibration profiles, certification records, decision ledger (`ei_*` tables).
- **Generation 7 certification** — quality / coverage / hierarchy / granularity / evidence / confidence gates; `CertificationDecision`; Educational Review Pack.
- **Educational Quality (EQ-001)** — semantic classification, front-matter gating, syllabus-first structure preparation toward 5 chapters / 15 topics / 73 LOs for CS1.

Student Runtime ingress for learning content is the **published curriculum package**, with certified-snapshot authority after RR-001.

---

## 4. Founder Console

Founder-facing Command Centre (`/console/` and related routes) provides:

- Overview / workspace home
- Curriculum Studio (subjects, upload, process, validate, preview, approve, publish)
- Curriculum Health (certification, publication, review packs, calibration, observatory summaries)
- Private Beta Dashboard (`/console/beta`)
- Operational health, feedback, research, releases (per Founder dashboard services)

Authorization: Founder/admin capabilities; not a public surface.

---

## 5. Student Runtime

Canonical **Education Operating System** (`student` + `session` blueprints):

- Home (mission-first)
- Daily Mission → Study Session lifecycle (overview / activity / reflection / summary)
- Journey / Progress
- Tutor (`/student/tutor`)
- Knowledge Map / Graph (`/student/knowledge_graph`)
- History, Revision, Profile, Help, Feedback
- Study Plan wizard and Settings (shared authenticated workflows)

EI-002B certified-learning facade projects certified node IDs into missions, KG, tutor context filters, progress, and adaptive signals. Twin / mission / tutor engines were not replaced; they consume certified artefacts.

---

## 6. Publication pipeline

Founder path (as proven in FV-002 / RR-001 / RC-001):

```
Create subject → bind CMP/syllabus → CIP/EI processing
  → validate → preview (certified snapshot when certified)
  → approve → publish → Student catalogue / Begin Learning
```

`PublicationBridge` binds certified dual-read so publish does not fall through to noisy unbound CIP/Foundation structure. Republish paths preserve certification stamps (RR-001 C1/C2 fixes).

---

## 7. Knowledge Graph

- **Curriculum Knowledge Graph (CKG)** persistence (`ckg_*` tables) and learner-facing Knowledge Map built from published package structure (parent_of / requires / learning_objective_of).
- Student UI uses hierarchical native disclosure patterns (UX-001), not a heavy virtualized tree on the beta surface.
- Tutor grounding filters to certified identifiers; foreign IDs rejected.

---

## 8. Tutor

**Evidence-backed Intelligent Tutor** (`intelligent_tutor` application + models: `tutor_sessions`, `tutor_messages`, `tutor_explanations`, `tutor_feedback`).

At beta.1: dedicated student Tutor page; curriculum context; citations / provenance metadata; certified context filtering (EI-002B). No new LLM-black-box core inserted by RC-001 (feature freeze).

---

## 9. Mission Engine

Multiple related layers exist in the tree (historical evolution preserved):

- Classic mission/planning services (`MissionService`, `mission_optimizer`, planning/readiness)
- Application mission engines (`mission_engine`, `mission_engine_v2`, `adaptive_mission`, `daily_mission_intelligence`)
- **CertifiedMissionEngine** (EI-002B) selecting from certified Learning Objectives for Daily Missions, with Runtime provenance on `MISSION_GENERATED`

Study Session lifecycle remains the student execution vehicle for mission instances.

---

## 10. Deployment architecture

| Concern | At V2.0.0-beta.1 |
|---|---|
| Host | Render web service `kwalitec` |
| URL | https://kwalitec.onrender.com |
| Build | `pip install -r requirements.txt` |
| Release | `flask db upgrade` |
| Start | `waitress-serve --port=$PORT wsgi:app` |
| Data store | Managed PostgreSQL (`kwalitec-db`) |
| Instance files | Present under Render instance path; **persistent disk not proven** (accepted beta residual / DP-003) |
| Config | Env vars: `SECRET_KEY`, `DATABASE_URL`, `ADMIN_*`, EI/V2 flags in `render.yaml` |
| Health | `/health`, `/health/live`, `/health/ready` |
| Identity | `/auth/login` shows `Kwalitec v2.0.0-beta.1`, build `beta.1` |

---

## 11. What this snapshot deliberately excludes

Future V3 ideas, speculative AI expansions, unpaid commercial expansion programmes, and “should redesign” notes. Those belong outside this archive.

For the full narrative architecture document as frozen into the archive tree, see `architecture/ARCHITECTURE.md`.

---

*AR-001 architecture snapshot — immutable historical reference.*
