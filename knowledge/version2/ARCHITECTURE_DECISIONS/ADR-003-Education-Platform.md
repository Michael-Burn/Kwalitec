# ADR-003 — Education Platform Composition

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-013 P0.1 — Digital Twin Documentation Authority  

---

## Context

Once Version 2 introduced multiple educational engines (Curriculum, Blueprint, Journey, Session, Activity, Mission), product surfaces risked wiring those engines directly. Direct wiring recreates god orchestrators inside dashboards, duplicates sequencing policy, and makes cutover/testing fragile.

Orchestration must be separated from educational rule ownership.

## Decision

Introduce **Education Platform** (`EducationPlatform`) as the sole public composition facade over the Educational Core.

- Owns workflow coordination and dependency injection of ports
- Owns no educational rules, mastery math, or content generation
- Exposes a single platform API for product-facing educational flows
- Engines remain independently testable and framework-independent

```text
Product / Dashboard / future API
            │
            ▼
     EducationPlatform
            │
   ports → Curriculum / Blueprint / Journey /
           Session / Activity / Mission
```

## Alternatives Considered

1. **Call engines directly from blueprints** — rejected; scatters orchestration and bypasses composition invariants.
2. **One mega-engine owning all rules** — rejected; destroys bounded-context ownership.
3. **Service locator / global registry only** — rejected without an explicit facade contract; hides dependencies.

## Consequences

**Benefits**

- Single entry point for Educational Core consumers
- Engines stay free of Flask and of each other's internals
- Parallel validation and migration become tractable
- Composition policies remain reviewable in one place

**Trade-offs**

- Extra abstraction layer
- Port/protocol discipline required
- Platform must not silently absorb educational decisions

## Future Considerations

- Twin integration should enter through explicit ports — not by embedding Twin math in the facade
- Keep diagnostics/health separate from educational authority
- Refuse feature flags that bypass EducationPlatform for production student flows without documented exception

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md)).
