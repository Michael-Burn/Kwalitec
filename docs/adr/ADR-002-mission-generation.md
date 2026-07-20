# ADR-002 — Mission Generation

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Daily missions are a primary student commitment. If mission content is invented in routes, templates, or AI prompts, students receive guidance that cannot be reproduced or explained from educational evidence.

## Decision

**Mission Generation** is a pure domain engine (`domain.mission_generation`) that produces a deterministic `MissionSpecification` from authorised educational inputs (for example Digital Twin, diagnosis, priority, teaching strategy, and learning trajectory signals).

Rules:

- No Flask, ORM, HTTP, DTOs, randomness, or AI inside the engine  
- AI may later enrich presentation of an already-generated specification; it must not author the specification  
- Student Experience may present the mission; it must not rewrite it  

## Alternatives Considered

1. **LLM-authored missions as authority** — rejected; non-deterministic and unexplainable.  
2. **Route-assembled mission dicts** — rejected; duplicates logic and bypasses invariants.

## Consequences

**Benefits:** Reproducible missions; clear test surface; safe enrichment boundary.  
**Trade-offs:** Richer educational inputs must be assembled before generation (application/pipeline responsibility).

## Related

- [ADR-008](ADR-008-ai-enrichment-boundary.md), [ADR-010](ADR-010-educational-pipeline.md)
- Package: `src/domain/mission_generation/`
