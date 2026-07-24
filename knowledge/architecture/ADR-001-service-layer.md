# ADR-001: Service Layer

# Status

Accepted

# Date

2026-07-10

# Context

Early Flask applications often grow business rules inside route handlers: form parsing, SQLAlchemy queries, scoring math, and template context assembly in one function. That pattern appeared as a risk for Kwalitec because the product’s core value — deterministic study planning, mission prioritisation, readiness, and recommendations — is **domain logic**, not HTTP plumbing.

Without a clear home for that logic:

- Routes become untestable without a full request cycle.
- The same planning or ordering rules get copied across blueprints.
- Curriculum V1/V2 branching leaks into unrelated modules.
- Explainability suffers: “why this recommendation?” cannot be traced to a single service method.

Kwalitec also needed a layer that could orchestrate both SQLAlchemy models and the in-memory Curriculum Engine without coupling either to Flask’s `request` or `session` globals.

# Decision

All business logic lives under `app/services/`. Blueprints call services; services call models, the Curriculum Engine (via thin bridges), and the database session.

| Layer | Owns | Does not own |
|---|---|---|
| Blueprints | Auth decorators, WTForms, redirects, template selection | Planning math, mastery, readiness scores |
| Services | Domain rules, persistence orchestration, explainable outputs | `flask.request` / session globals, HTML rendering |
| Models / Engine | Schema and syllabus truth | HTTP or product workflows |

Representative services include `CurriculumService`, `StudyPlanService`, `PlanningService`, `MissionService` / `MissionOptimizer`, `ReadinessService`, `RecommendationService`, `AnalyticsService`, and `StartupService`.

Services accept explicit arguments (`user_id`, model instances, dates) and return models, dataclasses, or plain dicts suitable for templates.

# Consequences

### Positive consequences

- Business rules are unit-testable with an app context and fixtures, without inventing HTTP.
- Curriculum traversal and import stay centralised (see [ADR-004](ADR-004-canonical-topic-traversal.md)).
- New features have an obvious place to land: extend a service or add a cohesive new one.
- Layering matches [`ARCHITECTURE.md`](../../ARCHITECTURE.md) and `.cursor/rules/04-services.mdc`.

### Trade-offs

- Simple CRUD can feel “over-wrapped” compared to inline route queries — accepted for consistency.
- Developers must learn which service owns which domain (see [glossary](../development/glossary.md) and subsystem docs).
- Service modules can still grow large if responsibilities are not split; prefer one primary domain per module.

### Future considerations

- Keep extracting god-service tendencies early (e.g. do not dump analytics math into `CurriculumService`).
- Continue forbidding `request`/`session` imports inside services.
- When adding recommendation or readiness signals, document explainability inputs in the service docstring, not only in the UI.

**See also:** [ADR-002](ADR-002-blueprint-architecture.md), [coding-standards.md](../development/coding-standards.md), subsystem docs under [`../subsystems/`](../subsystems/).

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../GOVERNANCE.md)).
