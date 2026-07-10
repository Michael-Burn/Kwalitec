# Glossary

Kwalitec-specific terminology. Prefer these meanings in code reviews, ADRs, and agent prompts.

| Term | Definition |
|---|---|
| **Curriculum** | An official syllabus version for an organisation/paper/year. Exists as engine dataclasses (in-memory) and as an SQLAlchemy `Curriculum` row after import. Source JSON lives under `app/curriculum/data/`. |
| **Curriculum Engine** | In-memory package `app/curriculum/`: load, validate, cache, and query syllabus JSON. Not the ORM. See [curriculum-engine.md](../subsystems/curriculum-engine.md). |
| **Curriculum V1** | Legacy/flat syllabus format: topic list (engine `Curriculum` / `Topic` / `LearningOutcome`). DB topics typically have `section_id = NULL`. Must remain loadable ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md)). |
| **Curriculum V2** | Canonical hierarchical format: Section → Topic → Learning Objective (`*Definition` dataclasses). Section-level `exam_weight`; DB `Section` + `Topic.section_id`. |
| **Section** | V2 syllabus grouping (e.g. syllabus part). Ordered by `display_order`. Carries exam weight. Absent for pure V1 curricula. |
| **Topic** | Study unit within a curriculum. ORM `Topic` may link to a section (V2) or participate in a parent tree (V1). Engine types differ by format (`Topic` vs `TopicDefinition`). |
| **Learning Objective / Outcome** | Finest syllabus leaf describing what the candidate must be able to do. V1 often uses “learning outcome”; V2 uses learning objective definitions. Imported to ORM `LearningObjective`. |
| **Canonical Traversal** | The single approved way to walk topics in syllabus order via `CurriculumService.get_all_topics_ordered()` (and related helpers). Duplicate ordering logic is forbidden ([ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)). |
| **Syllabus weight / exam weight** | Relative importance for coverage and planning. V1: often on topics. V2: on sections (`exam_weight`); imported topics may have weight `0.0`. |
| **Study Plan** | User-specific schedule toward an exam date for a curriculum. Managed by `StudyPlanService` / wizard; may include `WeekPlan` rows. |
| **Planning** | Deterministic distribution of topics across available study time (`PlanningService`, `TimeEngineService`). |
| **Mission** | A day’s (or session’s) set of prioritised tasks for the learner (`Mission` / `MissionTask`), produced via `MissionService` and `MissionOptimizer`. |
| **Mission Optimizer** | Service that ranks candidate tasks from urgency, readiness, workload, and plan context — without replacing canonical topic identity. |
| **Readiness** | Explainable estimate of exam preparedness from coverage, pace, and related signals (`ReadinessService`). |
| **Recommendation** | Deterministic, explainable “study next” suggestion (`RecommendationService`), optionally recorded in the Decision Journal. |
| **Adaptive Learning** | Mastery scoring and spaced-repetition style scheduling from real attempts (`AdaptiveLearningService`). |
| **Decision Journal** | Audit trail of accepted/dismissed recommendations (`Decision` model / related flows). |
| **Burnout Monitor** | Workload intensity signals flagging unsustainable pacing (`BurnoutMonitor`). |
| **Blueprint** | Flask feature package exposing HTTP routes (e.g. `auth`, `mission`). Should stay thin ([ADR-002](../architecture/ADR-002-blueprint-architecture.md)). |
| **Service Layer** | `app/services/` modules owning business logic and persistence orchestration ([ADR-001](../architecture/ADR-001-service-layer.md)). |
| **Application Factory** | `create_app()` — sole app construction path (config, extensions, blueprints, security, optional startup). |
| **StartupService** | Production-gated bootstrap: migrate + ensure admin user. Idempotent and non-destructive. |
| **Idempotent import** | Re-running curriculum import / admin bootstrap does not create duplicate or corrupt state. |
| **Deterministic core** | Planning, readiness, and recommendation paths where the same inputs must yield the same outputs (no hidden randomness / LLM). |
| **Explainability** | Requirement that user-facing scores and suggestions be traceable to curriculum weights, progress, and time constraints. |

**See also:** [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md), [project-history.md](project-history.md).
