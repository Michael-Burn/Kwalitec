# ADR-010 — Educational Pipeline

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Educational engines must run in a lawful order. If each route invents its own sequence (or embeds judgement in the orchestrator), educational integrity diverges across surfaces.

## Decision

The **Educational Pipeline** (`application.pipeline.EducationalPipeline`) is an application orchestrator that:

1. Sequences canonical stages (evidence analysis → mission → plan → progress → recommendations → explanation → student experience → optional enrichment)  
2. Delegates every educational decision to injected domain engines  
3. Calls enrichment ports only after educational artefacts exist  
4. Treats AI enrichment failure as non-fatal to educational results  

The pipeline **performs orchestration only**. It must not define educational intelligence methods (diagnose, calculate mastery, choose strategy, interpret evidence as authority, etc.), own persistence, or depend on Flask.

## Alternatives Considered

1. **God service that both orchestrates and decides** — rejected.  
2. **Implicit sequencing inside web handlers** — rejected; inconsistent authority.

## Consequences

**Benefits:** One spine for EOS product journeys; clear stage names for explainability and tests.  
**Trade-offs:** Pipeline API must stay thin; new stages require ADR-level scrutiny if they invent judgement.

## Related

- [ADR-001](ADR-001-educational-operating-system.md), [ADR-008](ADR-008-ai-enrichment-boundary.md)
- Package: `src/application/pipeline/`
- Tests: `tests/architecture/test_pipeline_orchestration.py`
