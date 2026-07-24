# ADR-009 — Composition Root

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

If routes, handlers, or domain modules construct SQLAlchemy sessions, AI providers, and engines ad hoc, dependency rules collapse and tests cannot substitute fakes cleanly.

## Decision

There is a single **composition root** for the Educational Operating System:

- Primary assembly: `application.composition.application_factory` (`assemble` / `create_application`)  
- Supporting factories: `infrastructure.composition` (session factory, unit of work, application services, runtime providers)  
- Web may call `create_application` or accept an injected `ApplicationContainer`  
- Business modules receive collaborators; they do not new up production graphs  

Composition is the only production site that wires `EducationalPipeline`, mission/recommendation enrichers, and the default AI provider.

## Alternatives Considered

1. **Service locator sprinkled through domain** — rejected.  
2. **Flask `current_app` as DI container for educational engines** — rejected; framework coupling.

## Consequences

**Benefits:** Replaceable adapters; test doubles at the edge; clear construction ownership.  
**Trade-offs:** Composition modules may import infrastructure (explicit exception to application purity).

## Related

- [DEPENDENCY_RULES.md](../DEPENDENCY_RULES.md)
- Tests: `tests/architecture/test_composition_root.py`

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../knowledge/GOVERNANCE.md)).
