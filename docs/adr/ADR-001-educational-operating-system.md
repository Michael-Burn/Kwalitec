# ADR-001 — Educational Operating System

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Version 1 concentrated educational behaviour across Flask services that mixed HTTP, persistence, and judgement. Version 2 requires a durable Educational Operating System that can host evidence-driven learning intelligence without coupling it to a web framework or ORM.

Without a named system boundary, new capabilities drift into routes, templates, or vendor AI calls and become untestable educational authorities.

## Decision

Kwalitec Version 2 treats the code under `src/` as an **Educational Operating System (EOS)** with four layers:

1. **Domain** — educational meaning and deterministic engines  
2. **Application** — use-cases, ports, pipeline orchestration, composition root  
3. **Infrastructure** — persistence, runtime, events, AI enrichment adapters  
4. **Web** — HTTP adapters only  

Educational authority for missions, plans, progress, recommendations, and explanations lives in domain engines composed by the application pipeline. Legacy `app/` surfaces may coexist during migration but must not silently become a second educational brain.

## Alternatives Considered

1. **Grow `app/services/` indefinitely** — rejected; framework entanglement and god services.  
2. **AI-centric unified tutor** — rejected; violates determinism and evidence-first law.  
3. **Microservice split per engine immediately** — deferred; package boundaries first.

## Consequences

**Benefits:** Clear ownership, framework-independent tests, replaceable adapters, explainable pipelines.  
**Trade-offs:** Dual paths during migration; discipline required at composition and import boundaries.  
**Enforcement:** Constitution Articles I–X; `tests/architecture/`.

## Related

- [ARCHITECTURE_CONSTITUTION.md](../ARCHITECTURE_CONSTITUTION.md)
- [ARCHITECTURE_OVERVIEW.md](../ARCHITECTURE_OVERVIEW.md)
- [ADR-009](ADR-009-composition-root.md), [ADR-010](ADR-010-educational-pipeline.md)
