# ADR-002: Blueprint Architecture

# Status

Accepted

# Date

2026-07-10

# Context

Kwalitec’s HTTP surface spans authentication, dashboard, daily missions, study-plan wizard, analytics, and settings. Putting every route in a single module (or mixing domain math into routes) made the application harder to navigate, review, and test.

Flask’s blueprint mechanism was the natural packaging unit, but packaging alone is not enough: without a **thin-route** rule, blueprints become miniature applications that reimplement service concerns.

The product also requires consistent security behaviour — Flask-Login, CSRF, open-redirect protection, and CSP headers — which must stay at the factory/blueprint boundary rather than being reinvented per feature.

# Decision

Feature HTTP surface lives in blueprints registered from `create_app()` via `_register_blueprints()` in `app/__init__.py`. Routes remain thin:

```
route → authenticate → validate form/input → call service → render template / redirect
```

| Blueprint | URL prefix | Purpose |
|---|---|---|
| `auth` | `/auth` | Login / logout (no public registration) |
| `dashboard` | `/dashboard` | Home / overview |
| `mission` | `/missions` | Daily missions and review |
| `study_plan` | `/study-plan` | Plan list and multi-step wizard |
| `analytics` | `/analytics` | Performance analytics |
| `settings` | `/settings` | User preferences / backup |

App-level routes (`/`, `/health`) stay on the application factory.

### What belongs in a blueprint

- Request/response handling
- `@login_required` and ownership checks at the edge
- WTForms validation
- Flash messages and template selection
- Passing service results into Jinja context

### What does not belong in a blueprint

- Mastery scoring, planning distribution, readiness formulas
- Curriculum import or topic ordering (use `CurriculumService`)
- Raw DDL or schema changes
- Cross-user queries without scoping

# Consequences

### Positive consequences

- Feature folders mirror URL space and templates (`app/templates/<feature>/`).
- Reviews can focus on HTTP concerns in blueprints and domain concerns in services separately.
- Security decorators and CSRF stay visible at the route layer.
- Matches [ADR-001](ADR-001-service-layer.md) and `.cursor/rules/03-flask.mdc`.

### Trade-offs

- A one-line “call service and render” route can look sparse — that is intentional.
- Shared UI chrome lives in layouts/partials, not in blueprints; blueprints must not duplicate nav markup.
- Cross-cutting concerns (e.g. “active study plan”) still need a clear owning service to avoid blueprint-to-blueprint imports of business logic.

### Future considerations

- New product areas should get a new blueprint + service pair rather than expanding an unrelated blueprint.
- Keep registration centralised in `app/__init__.py`; do not invent secondary app factories.
- Preserve progressive enhancement: routes must not depend on fragile client-only state for core flows.

**See also:** [authentication.md](../subsystems/authentication.md), [`ARCHITECTURE.md`](../../ARCHITECTURE.md).
