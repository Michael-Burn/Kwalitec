# ADR-005 — Recommendation Engine

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Recommendations are high-trust guidance. Opaque ranking, vendor-model selection, or UI heuristics as recommendation authority would violate explainability and determinism.

## Decision

**Recommendation Engine** is a pure domain engine (`domain.recommendation`) that produces a deterministic `RecommendationSpecification` from authorised educational inputs (mission, plan, progress, and related educational state).

Rules:

- Recommendations are educational decisions, not marketing content  
- Explainability must be able to narrate recommendation rationale from inputs  
- AI enrichment may improve presentation wording only after specification exists  
- Student Experience references recommendations; it never mutates them  

## Alternatives Considered

1. **LLM as recommendation authority** — rejected.  
2. **Hard-coded UI suggestion lists** — rejected; not evidence-driven.

## Consequences

**Benefits:** Reproducible, explainable next actions.  
**Trade-offs:** Enrichment copy must remain clearly non-authoritative.

## Related

- [ADR-006](ADR-006-explainability-engine.md), [ADR-008](ADR-008-ai-enrichment-boundary.md)
- Package: `src/domain/recommendation/`

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../knowledge/GOVERNANCE.md)).
