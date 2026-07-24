# ADR-003 — Study Planning

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Study plans coordinate multi-session learning. Plans that embed in UI wizards or ORM models become impossible to reason about, regress, or explain when curriculum structure changes.

## Decision

**Study Planning** is a pure domain engine (`domain.study_planning`) that produces a deterministic `StudyPlan` from authorised educational inputs and curriculum-aware constraints supplied to it.

Rules:

- Planning math lives in domain, not blueprints or templates  
- Application orchestrates loading of inputs; domain owns the plan  
- Plans are educational artefacts, not engagement theatre  

## Alternatives Considered

1. **Wizard-only plan construction in presentation** — rejected; couples education to UI.  
2. **Opaque optimiser without explainability hooks** — rejected; violates Constitution Article IV.

## Consequences

**Benefits:** Deterministic plans; curriculum-first sequencing retained; testable without HTTP.  
**Trade-offs:** Requires explicit input assembly from twin/progress/mission context.

## Related

- [ADR-002](ADR-002-mission-generation.md), [ADR-004](ADR-004-progress-evaluation.md)
- Package: `src/domain/study_planning/`

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../knowledge/GOVERNANCE.md)).
