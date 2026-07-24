# ADR-007 — Student Experience

**Status:** Accepted  
**Date:** 2026-07-20  
**Milestone:** APP-003 — Architecture Governance  
**Authority:** Architectural  

---

## Context

Engagement features (streaks, achievements, celebrations, reminders, motivational messaging) improve continuity when honest. When they rewrite educational decisions, they corrupt trust.

## Decision

**Student Experience** is a pure presentation domain (`domain.student_experience`) that projects a `StudentExperience` from completed educational outputs.

Rules:

- May compute streaks, achievements, celebrations, motivation, reminders  
- Must not diagnose, prioritise, select strategies, generate authoritative missions/recommendations, or mutate educational specifications  
- No AI, persistence, Flask, or ORM inside the package  
- Recommendations are referenced, never modified  

## Alternatives Considered

1. **Merge experience into recommendation engine** — rejected; mixes authority with presentation.  
2. **Client-only gamification** — rejected; breaks consistency and explainability of milestones.

## Consequences

**Benefits:** Clear non-authority boundary; safer enrichment and UI.  
**Trade-offs:** Experience quality depends on upstream educational completeness.

## Related

- Constitution Article V; [DEPENDENCY_RULES.md](../DEPENDENCY_RULES.md)
- Package: `src/domain/student_experience/`
- Tests: `tests/architecture/test_student_experience_boundary.py`

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../knowledge/GOVERNANCE.md)).
