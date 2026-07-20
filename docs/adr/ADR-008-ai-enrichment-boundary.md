# ADR-008 — AI Enrichment Boundary

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Vendor AI can improve wording and summaries. Using AI as the educational brain would make Kwalitec non-deterministic, unexplainable, and vendor-coupled at the core.

## Decision

AI lives only in **infrastructure enrichment** (`infrastructure.ai`):

- Providers implement an `AIProvider` port abstraction  
- Enrichers produce enhanced *views* of already-decided missions and recommendations  
- Default provider construction occurs in the composition root  
- Pipeline AI failures must not fail educational stages  

Forbidden for AI modules:

- Authoritative diagnose / mastery / strategy / mission / recommendation generation  
- Mutating educational specifications  
- Becoming a required dependency of domain engines  

## Alternatives Considered

1. **AI-first tutor core** — rejected.  
2. **AI inside domain packages** — rejected; breaks framework independence and determinism.

## Consequences

**Benefits:** Optional enrichment; provider replaceability; educational correctness without AI.  
**Trade-offs:** Enrichment quality varies by vendor; must stay clearly non-authoritative in product language.

## Related

- Constitution Article VI; [ADR-009](ADR-009-composition-root.md)
- Package: `src/infrastructure/ai/`
- Tests: `tests/architecture/test_ai_enrichment_boundary.py`
