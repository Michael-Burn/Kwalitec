# ADR-006 — Authority Boundaries

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-017 — Production Integration Foundation  

---

## Context

Version 2 contains many bounded contexts. Without an explicit ownership map, adapters and product surfaces risk duplicating authorities (especially around curriculum publication and learner advice).

## Decision

Authority by bounded context:

### Curriculum Management

- **Owns:** subject products, version lifecycle, asset references, validation gates, approval, publication / archive / rollback posture.
- **Does not own:** PDF parsing, Twin state, learner next actions, Studio UI policy invention.

### Curriculum Studio

- **Owns:** Founder readiness orchestration, checklist projection, workflow presentation, version-history display, structural diff presentation.
- **Does not own:** publication law (Management), ingestion parsing (Ingestion), student learning orchestration.

### Curriculum Ingestion

- **Owns:** classify → extract → normalise → validate document-to-structure pipeline.
- **Does not own:** publication, Twin, pedagogy, activity generation.

### Education Platform

- **Owns:** composition of Curriculum → Blueprint → Journey → Session → Activity → Mission workflows for the Educational Core facade.
- **Does not own:** educational algorithms inside engines; publication lifecycle; Twin truths; Adaptive next-action law.

### Learning Orchestrator

- **Owns:** ordered live-event pipeline coordination (Evidence → Twin → Adaptive → Mission → Analytics) via ports.
- **Does not own:** educational recalculation, next-action invention, persistence rules beyond calling ports.

### Student Digital Twin

- **Owns:** evidence-driven learner state and explainable state projections.
- **Does not own:** curriculum structure, mission scheduling, learner-facing next-action authority (ADR-005).

### Adaptive Decision Engine

- **Owns:** learner-facing next-action / revision intervention selection with priority, ROI, and explanations (ADR-005).
- **Does not own:** Twin mutation, curriculum publication, mission persistence internals.

### Mission Engine

- **Owns:** daily commitment generation / lifecycle / delivery of work units.
- **Does not own:** independent next-action ranking that competes with Adaptive Decision; Twin state; curriculum authority.

## Consequences

- Production adapters implement application ports and must not cross these ownership lines.
- Studio consumes Management / Ingestion / Platform only through ports.
- Duplicate publication ontologies and recommendation authorities are architectural defects.

## Related

- [`ADR-005-Single-Next-Action-Authority.md`](ADR-005-Single-Next-Action-Authority.md)
- [`../AUTHORITY_MATRIX.md`](../AUTHORITY_MATRIX.md)
- [`../PRODUCTION_INTEGRATION.md`](../PRODUCTION_INTEGRATION.md)
