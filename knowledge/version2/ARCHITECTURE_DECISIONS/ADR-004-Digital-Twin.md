# ADR-004 — Digital Twin Evidence-Driven Design

**Status:** Accepted  
**Date:** 2026-07-18  
**Authority:** Architectural  
**Milestone:** V2-013 P0.1 — Digital Twin Documentation Authority  

---

## Context

Adaptive learning fails when learner state is invented from engagement heuristics, opaque scores, or generative AI opinions. Kwalitec requires a Twin that can justify every educational conclusion from observable evidence, remain deterministic for core decisions, and stay reversible as new evidence arrives.

Governing documents:

- Philosophy — *why* ([`../DIGITAL_TWIN_PHILOSOPHY.md`](../DIGITAL_TWIN_PHILOSOPHY.md))
- Constitution — *what must be obeyed* ([`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md))
- Architecture — *how* ([`../STUDENT_DIGITAL_TWIN.md`](../STUDENT_DIGITAL_TWIN.md))

## Decision

The Digital Twin is an **evidence-driven, deterministic learner model**:

1. **Evidence only** — activities, assessments, practice, reflection, recall, confidence ratings, time-on-task, session/mission/revision outcomes. Never curriculum PDFs or AI responses as Twin truth.
2. **Deterministic modelling** — identical evidence → identical conclusions for core engines.
3. **Explainability** — every recommendation cites evidence, rationale, expected benefit, and confidence.
4. **Immutable history** — past events are never rewritten; state evolves by accumulation.
5. **Explicit confidence** — uncertainty is visible (bands/scores); low confidence is allowed; hidden certainty is not.
6. **Future adaptive learning** — curriculum, missions, revision, and scheduling may adapt *from* Twin outputs; they must not bypass Twin authority for learner-state claims.

AI may enrich experiences. AI must not own Twin mutations or declare educational truth.

## Alternatives Considered

1. **Engagement-optimised profile store** — rejected; optimises usage, not mastery.
2. **LLM-authored learner state** — rejected; non-deterministic and unexplainable as authority.
3. **Coverage-as-mastery** — rejected; Study Progress ≠ Twin understanding.

## Consequences

**Benefits**

- Trustworthy educational decisions
- Testable twin pipelines
- Clear non-responsibilities (no teaching, no curriculum storage)
- Foundation for adaptive learning without theatre

**Trade-offs**

- Cold-start Twin states are sparse by design
- Requires disciplined evidence emission from engines
- Dual Twin paths (Epic Twin vs Version 2 `student_twin`) need explicit future cutover

## Future Considerations

- Wire journey-attributed evidence into Twin updates without competing state stores
- Keep readiness/decision/recommendation consumers read-side unless Twin lawfully owns the field
- Deepen confidence and retention models without abandoning determinism or explainability

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md)).
