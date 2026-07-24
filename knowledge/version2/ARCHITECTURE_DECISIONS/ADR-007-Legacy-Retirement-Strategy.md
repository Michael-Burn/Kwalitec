# ADR-007 — Legacy Retirement Strategy

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-017 — Production Integration Foundation  

---

## Context

Production still runs Version 1 educational services while Version 2 engines are framework-independent and, as of V2-017, executable through infrastructure adapters. Dual Twin paths, dual recommendation stacks, and mission cutover adapters create wrong-import and dual-truth risk until explicit retirement.

This ADR documents retirement strategy. It does **not** retire Version 1 in this milestone.

## Decision

### Legacy Twin retirement

1. **Authority target:** Version 2 `student_twin` is the learner-state authority for V2 paths (ADR-004 + ADR-006).
2. **Legacy `domain/twin` / `application/twin*`:** remain available for V1 runtime and migration comparison until dual-run exit criteria are met.
3. **No silent dual writes** of educational truth without feature-flag documentation.
4. **Kill date posture:** Legacy Twin must not gain new product features; fixes only. Cutover is gated by V2-020 prerequisites.

### Legacy recommendation services

1. V1 `recommendation_service` and pre-V2 `domain/recommendation` must not be called from V2 student next-action surfaces.
2. V2 product next actions bind to Adaptive Decision Engine (ADR-005).
3. Twin internal recommendation projections may exist for explainability / analysis but are not product next-action authority.

### Mission migration

1. Mission Adapter remains the cutover router while dual-run is active ([`../MISSION_ADAPTER.md`](../MISSION_ADAPTER.md)).
2. Mission Engine 2.0 is the V2 delivery authority; it consumes Adaptive Decision / Journey context and does not invent competing next-action law.
3. Historical V1 missions map conceptually to journey-session recommendations (see [`../MIGRATION_STRATEGY.md`](../MIGRATION_STRATEGY.md)); durable data migration is a later operational programme.

### Version 1 cutover strategy

1. Coexist until V2-020.
2. Feature flags / dual-run observability required before traffic cutover.
3. Alembic / StartupService safety guarantees remain (no drops, idempotent admin).
4. Student UX (roadmap student experience) and infrastructure persistence proof must precede sole-runtime cutover.

### Dual-run exit criteria

All must be true before retiring V1 educational runtime:

| # | Criterion |
|---|-----------|
| 1 | V2 persistence + adapters stable in production dual-run |
| 2 | Student learning path explainable end-to-end on V2 (Twin evidence → Adaptive next action → Mission delivery) |
| 3 | No unresolved dual-authority defects for next action or Twin state |
| 4 | Founder curriculum readiness operable via Studio over Management/Ingestion |
| 5 | Product Strategy evidence gates satisfied |
| 6 | Explicit V2-020 retirement runbook executed |

## Alternatives Considered

1. **Big-bang cutover now** — rejected; educational trust and history risk.
2. **Indefinite dual Twin product paths** — rejected; authority erosion.

## Consequences

- V2-017 establishes adapters and authority docs without deleting V1.
- Engineering must refuse new V1 recommendation/Twin feature work on V2 paths.
- Retirement is earned by evidence, not package completeness.

## Related

- [`../MIGRATION_STRATEGY.md`](../MIGRATION_STRATEGY.md)
- [`ADR-004-Digital-Twin.md`](ADR-004-Digital-Twin.md)
- [`ADR-005-Single-Next-Action-Authority.md`](ADR-005-Single-Next-Action-Authority.md)

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md)).
