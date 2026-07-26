# ADR-005 — Single Next Action Authority

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-017 — Production Integration Foundation  

---

## Context

Version 2 Phase I delivered multiple engines that can influence what a learner does next: Student Digital Twin recommendations, Adaptive Decision Engine interventions, Journey continuation, Mission delivery, and Education Platform / Learning Orchestrator composition. The independent design review correctly flagged recommendation polyphony as a trust risk for an exam-oriented product.

Learners and Founders need one explainable answer to: *what should this student do next?*

## Decision

**Adaptive Decision Engine is the only component permitted to produce learner-facing next actions.**

Clarifying ownership:

| Concern | Authority |
|---------|-----------|
| Learner state (mastery, confidence, retention, readiness, evidence spine) | Student Digital Twin |
| Ranked learner-facing next action / revision intervention | Adaptive Decision Engine |
| Delivery of committed work units | Mission Engine |
| Multi-session topic context / continuation constraints | Learning Journey |
| Composition / live-event routing (no educational invention) | Education Platform / Learning Orchestrator |

Rules:

1. Twin owns learner **state**; it must not be the product next-action authority.
2. Mission **delivers** work derived from adaptive decisions / journey commitments; it must not independently invent competing next-action rankings for the student surface.
3. Journey provides **context** (position, progress, mode constraints); it must not emit an alternate student next-action ranking that bypasses Adaptive Decision.
4. Education Platform and Learning Orchestrator **compose and route**; they own no next-action educational law.
5. Infrastructure adapters must preserve this authority matrix (see [`../AUTHORITY_MATRIX.md`](../AUTHORITY_MATRIX.md)).

## Alternatives Considered

1. **Twin as next-action authority** — rejected; conflates state modelling with intervention selection.
2. **Mission as next-action authority** — rejected; missions are delivery vehicles, not decision brains.
3. **Orchestrator as next-action authority** — rejected; would recreate a god layer above declared facades.

## Consequences

**Benefits**

- One explainable student moment-of-truth
- Clear adapter and UI contracts for V2-017+
- Aligns Adaptive Decision explainability with product trust

**Trade-offs**

- Twin recommendation surfaces become advisory / internal projections unless explicitly demoted in product paths
- Mission and Journey UIs must consume Adaptive Decision outputs (or lawful none) rather than inventing alternatives

## Future Considerations

- Student Learning Experience (roadmap student UX) must bind next-action UI to Adaptive Decision payloads
- Legacy V1 recommendation services remain dual-run until ADR-007 exit criteria; they must not silently override Adaptive Decision on V2 paths

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md)).
