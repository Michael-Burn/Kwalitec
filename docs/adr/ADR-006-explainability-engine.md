# ADR-006 — Explainability Engine

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Guidance without explanation erodes student trust. Explanations bolted on in templates after the fact diverge from the real decision path and become marketing copy.

## Decision

**Explainability** is a pure domain engine (`domain.explainability`) that builds an `EducationalExplanation` with a decision trace and evidence references from completed educational artefacts (mission, plan, progress, recommendations).

Rules:

- Explanation narrates decisions; it does not change them  
- The four-question contract (what we know, what we estimate, why, what next) is educational product law  
- No AI required for core explanation; AI must not replace the decision trace  

## Alternatives Considered

1. **Template-only “why” strings** — rejected; not tied to decision inputs.  
2. **Post-hoc LLM rationalisations** — rejected; can invent reasons.

## Consequences

**Benefits:** Traceable guidance; shared language across surfaces.  
**Trade-offs:** Engines must expose enough structured inputs for traces.

## Related

- Constitution Article IV; [ADR-005](ADR-005-recommendation-engine.md)
- Package: `src/domain/explainability/`
