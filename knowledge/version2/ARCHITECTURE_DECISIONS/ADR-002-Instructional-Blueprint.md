# ADR-002 — Instructional Blueprint Independence

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-013 P0.1 — Digital Twin Documentation Authority  

---

## Context

Curriculum answers *what* must be learned (official syllabus structure). Pedagogy answers *how* learning should be sequenced and practised for a given educational intent.

If pedagogy is embedded inside curriculum JSON or Twin belief, syllabus updates become pedagogical rewrites, and learner-state updates risk inventing teaching methods. Version 2 needed an independent home for instructional strategy.

## Decision

Treat **Instructional Blueprint** as a bounded context independent from curriculum and learner state.

- Curriculum owns topics, objectives, prerequisites, and syllabus order.
- Blueprints own pedagogical profiles, effort bands, and step sequences.
- Twin owns evidence-derived learner beliefs — not lesson plans.
- Engines may *select* and *compile* blueprints against curriculum and constraints; they do not rewrite syllabus truth.

**Blueprint philosophy:** pedagogy is reusable strategy applied to curriculum structure, not content stored inside the Twin or the syllabus graph.

## Alternatives Considered

1. **Pedagogy fields on curriculum topics** — rejected; couples exam-board syllabus to product teaching style.
2. **Twin generates pedagogy from belief scores** — rejected; Twin observes, it does not teach.
3. **Hard-coded mission templates only** — rejected; not reusable across journeys/sessions/activities.

## Consequences

**Benefits**

- Curriculum remains official syllabus truth
- Pedagogy can evolve without re-ingesting syllabuses
- Twin stays free of teaching content
- Educational reasoning stays inspectable (which blueprint, why selected)

**Trade-offs**

- Requires blueprint selection/compilation policies
- Product must maintain blueprint catalogues
- Mis-selection can still produce poor missions if policies are weak

## Future Considerations

- Keep blueprint assignment under Curriculum Management publication lifecycle
- Never allow generative AI to silently author blueprint educational law
- Document selection rationale in engine outputs for explainability

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md)).
