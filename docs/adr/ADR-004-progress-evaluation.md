# ADR-004 — Progress Evaluation

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Progress signals drive interventions, celebrations, and next-action confidence. Inflated or opaque progress destroys trust. Evaluation must be evidence-bound and deterministic.

## Decision

**Progress Evaluation** is a pure domain engine (`domain.progress_evaluation`) that produces a deterministic `ProgressReport` (including intervention signals where warranted) from observable educational inputs.

Rules:

- Evaluation does not invent evidence  
- Thresholds and bands are domain policy, not UI constants  
- Student Experience may celebrate reports; it may not alter them  
- AI must not recalculate progress as educational authority  

## Alternatives Considered

1. **Client-side progress percentages** — rejected; unverifiable.  
2. **Engagement proxies as mastery** — rejected; violates evidence-first law.

## Consequences

**Benefits:** Honest progress; shared authority for missions and recommendations.  
**Trade-offs:** Sparse evidence yields sparse reports — preferred over false confidence.

## Related

- [ADR-005](ADR-005-recommendation-engine.md), [ADR-007](ADR-007-student-experience.md)
- Package: `src/domain/progress_evaluation/`

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../knowledge/GOVERNANCE.md)).
