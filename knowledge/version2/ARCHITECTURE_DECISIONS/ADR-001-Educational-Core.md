# ADR-001 — Educational Core Bounded Contexts

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-013 P0.1 — Digital Twin Documentation Authority  

---

## Context

Version 1 concentrated educational behaviour across services that mixed curriculum traversal, planning, missions, and learner signals. Version 2 needed a structure that could grow without creating god services or collapsing distinct educational concerns into one module.

The Educational Core must support curriculum structure, pedagogy, journey progression, session execution, activity sequencing, mission orchestration, and learner state — each with different change rates and ownership.

## Decision

Separate the Educational Core into **bounded contexts**, each owning exactly one educational responsibility:

| Context | Owns |
|---------|------|
| Curriculum Graph | Syllabus structure and sequencing |
| Instructional Blueprint | Pedagogy profiles and sequencing rules |
| Learning Journey | Multi-session topic journeys |
| Learning Session | Session lifecycle and runtime |
| Learning Activity | In-session activity progression |
| Mission Engine 2.0 | Daily mission orchestration |
| Student Digital Twin | Evidence-driven learner state |
| Education Platform | Composition / public orchestration only |

Contexts communicate through explicit contracts (ports, snapshots, evidence). No context invents another's truth.

## Alternatives Considered

1. **Single monolithic educational service** — rejected; untestable and opaque.
2. **Feature folders by UI surface** — rejected; couples education to presentation.
3. **AI-centric unified brain** — rejected; violates evidence and determinism principles.

## Consequences

**Benefits**

- Clear ownership and test boundaries
- Independent evolution of curriculum, pedagogy, and learner state
- Explainable educational pipelines

**Trade-offs**

- More packages and integration surfaces
- Requires disciplined port/DTO design
- Temporary dual paths during Version 1 coexistence

## Future Considerations

- Keep Education Platform as the sole public composition facade
- Resist merging Twin belief with Study Progress coverage
- Add ADRs when a context boundary is intentionally redrawn

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md)).
