# VERSION STATISTICS — 2.0.0-beta.1

**Measured:** 2026-07-30 (AR-001 archival pass)  
**Scope:** Quantitative inventory of the product tree associated with Private Beta release identity `2.0.0-beta.1`.  
**Method:** Filesystem counts on the repository at archive time; commit counts from git tag `v2.0.0-beta.1`.

---

## Identity anchors

| Item | Value |
|---|---|
| Version | `2.0.0-beta.1` |
| Tag | `v2.0.0-beta.1` |
| Tag commit | `f6245f45fa8dbf1c972f28980d0279829b6b846b` |
| Deploy commit | `7302bb7f955e4f2e8512d5af28ee258f34abbc00` |
| Alembic head | `202607300005` |
| Commits on tag | 261 |

---

## Major modules

| Module / package area | Count / note |
|---|---|
| `app/` Python files | 2,041 |
| `app/` Python LOC (approx.) | ~319,584 |
| `app/application/` top-level packages | 59 |
| `app/models/` model modules | 36 |
| `app/curriculum/` | Curriculum Engine (V1/V2 JSON) |
| `app/founder/` | Founder Console + subsystems |
| `app/presentation/` | Student, session, studio, tutor, twin, diagnostics |
| `app/services/` service modules | 61 (excl. `__init__`) |

### Application packages (59)

`adaptive_assessment`, `adaptive_learning`, `adaptive_mission`, `assessment_pipeline`, `calibration`, `config`, `constraints`, `curriculum`, `curriculum_extraction`, `curriculum_ingestion`, `curriculum_intelligence`, `curriculum_management`, `curriculum_publishing`, `curriculum_retrieval`, `curriculum_studio`, `curriculum_studio_foundation`, `daily_mission_intelligence`, `dashboard`, `decision_journal`, `education_platform`, `educational_engine_foundation`, `educational_experience`, `educational_experience_engine`, `educational_feedback_loop`, `educational_intelligence_pipeline`, `educational_quality`, `educational_reasoning`, `educational_reasoning_engine`, `educational_runtime_engine`, `educational_state`, `educational_timeline`, `founder_validation`, `instructional_blueprint`, `intelligent_tutor`, `learner_lifecycle`, `learning_activity`, `learning_evidence`, `learning_graph`, `learning_journey`, `learning_loop`, `learning_orchestrator`, `learning_session`, `mission_adapter`, `mission_engine`, `mission_engine_v2`, `orchestration`, `platform_integration`, `reasoning`, `runtime_integration`, `session_experience`, `student_curriculum_binding`, `student_digital_twin`, `student_experience`, `student_twin`, `twin`, `twin_inference`, `twin_repository`, `twin_update`, `unified_journey`

---

## Blueprints

| Metric | Value |
|---|---|
| `register_blueprint` call sites | 21 |
| Route modules (`*/routes.py` under `app/`) | 21+ (includes nested presentation/founder) |

**Registered:** auth, analytics, dashboard, mission, settings, study_plan, calibration, founder_dashboard, research, alpha, student, session, assessment, adaptive_assessment, studio, twin_diagnostics, reasoning_diagnostics, learning_graph_diagnostics, adaptive_mission_diagnostics, assessment_pipeline_diagnostics, intelligent_tutor_diagnostics.

---

## Templates / CSS / JavaScript

| Asset | Files | LOC (approx.) |
|---|---:|---:|
| `app/templates/` HTML | 99 | 9,794 |
| Founder HTML templates | 28 | 2,823 |
| `app/static/` CSS | 10 | 5,685 |
| Founder CSS | 1 | 571 |
| `app/static/` JavaScript | 13 | 2,174 |

---

## Tests

| Metric | Value |
|---|---|
| Test files under `tests/` | 1,401 |
| Test LOC (approx.) | ~246,577 |
| `test_*.py` files (glob earlier pass) | 1,099 |
| `def test_` function count (ripgrep) | ~7,804 |
| RC-001 focused pytest (pre-deploy) | 180 passed (programme report) |
| Identity / release artefact tests (RC-001) | 50 passed |

Additional in-package tests live under `app/founder/*/tests` and `app/automation/tests` (pytest `testpaths`).

---

## Database tables

| Metric | Value |
|---|---|
| `__tablename__` declarations under `app/models/` | ~145 |
| Notable domains | users/identity, study plans, missions/progress, CIP (`cip_*`), EI generations (`ei_*`), CKG (`ckg_*`), twin, tutor, assessment pipeline, private beta, vision journal, analytics |

Exact production table count may include Alembic version table and any ops-only objects; ORM declaration count is the archival baseline.

---

## Alembic revisions

| Metric | Value |
|---|---|
| Revision files under `migrations/versions/` | 58 |
| Head at release | `202607300005` |
| RC-001 additive set | `202607300001` … `202607300005` |

---

## Educational services

Representative educational/domain services and application facades present at beta.1 (non-exhaustive list for inventory):

- Curriculum: `CurriculumService`, `CurriculumEngineService`, CIP/EI application packages, educational quality / certification agents
- Certified learning (EI-002B): CertifiedMissionEngine, CertifiedTutorContextService, LearnerKnowledgeGraphBuilder, CertifiedProgressEngine, CertifiedAdaptiveLearningService, CurriculumObservatory
- Reasoning / twin / learning graph / adaptive mission / assessment pipeline / intelligent tutor application packages
- Evidence / explainability / readiness / recommendation quality helpers under `app/services/`

---

## Presentation services

| Area | Inventory |
|---|---|
| `app/presentation/student/` | ~16 Python modules (routes, DTOs, services) |
| `app/presentation/session/` | Session Experience |
| Presentation `*service*.py` files | 5 (plus additional non-`service`-named presenters) |
| Surfaces | Home, Journey, Tutor, Knowledge Map, History, Revision, Profile, Session steps |

---

## Founder services

| Metric | Value |
|---|---|
| `app/founder/**/services/*.py` | 15 |
| Examples | `founder_home_service`, `curriculum_health_service`, `beta_dashboard_service`, `command_centre_service`, `operational_health_service`, `founder_workspace_service`, `founder_subjects_service`, briefing / recommendations / operational_state / knowledge_engine query services |

---

## Student services

Cross-cutting student learning services under `app/services/` include (among others):

`mission_service`, `mission_optimizer`, `daily_mission_intelligence_service`, `study_plan_service`, `study_session_service`, `study_session_timer`, `planning_service`, `readiness_service`, `recommendation_service`, `adaptive_learning_service`, `learning_service`, `learning_lifecycle_service`, `welcome_service`, private_beta package services.

Presentation-layer student services sit under `app/presentation/student/services/`.

---

## Repository contributors (tag history)

| Author | Commits |
|---|---:|
| Michael Burn | 219 |
| Eidolon | 41 |
| Courage Shumba | 1 |

---

## Metrics folder note

Raw numeric pins for release identity also stored as:

- `release/PRODUCT_VERSION.txt`
- `release/DATABASE_REVISION.txt`
- `release/GIT_COMMIT_SHA.txt`
- `release/DEPLOY_COMMIT_SHA.txt`
- `release/GIT_TREE_SHA.txt`

---

*AR-001 statistics — objective inventory only.*
