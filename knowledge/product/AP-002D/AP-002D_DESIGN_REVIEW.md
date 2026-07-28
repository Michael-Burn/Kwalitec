# AP-002D — Design Review

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration (design)  
**Document:** `AP-002D_DESIGN_REVIEW.md`  
**Status:** Design review (documentation milestone)  
**Date:** 2026-07-28  

---

## 1. Educational consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Assessment does not know the learner as belief | **Pass** | Evidence Boundary + Integration Spec |
| Evidence ≠ knowledge / mastery / confidence | **Pass** | Repeated across pack; strength = quality |
| Only StudentReasoningService infers | **Pass** | Reasoning Contract normative |
| Cold-start honesty | **Pass** | Twin Update Rules |
| Soft signals not sole high-mastery authority | **Pass** | Aligned with AP-002 Evidence / Scoring models |
| Anxiety-safe downstream framing | **Pass** | Defers to AP-002 UX; Mission/Tutor constraints |

**Residual educational risk:** Implementers may conflate `evidence_strength` with learner confidence in UI copy — require copy review at implementation.

---

## 2. Architecture consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Twin sole learner SoT | **Pass** | Twin Update Rules |
| Reasoning sole inference | **Pass** | Reasoning Contract |
| Mission consumes decisions only | **Pass** | Mission Impact Model |
| Graph relationships only | **Pass** | Learning Graph Impact |
| Tutor explains only | **Pass** | Integration Spec §3.8 |
| AP-001 retained as ingress | **Pass** | Explicit; no second Twin-write channel |
| No architecture redesign | **Pass** | Additive wiring only |
| Determinism / no LLM in Reasoning | **Pass** | Reasoning Contract |

**Residual architecture risk:** Pressure to “call Reasoning from packaging for speed” — blocked by boundary rules and planned architecture tests (D7).

---

## 3. Engineering consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Small independently testable tasks | **Pass** | Implementation Plan D1–D7 |
| Versioning of packaging vs engine | **Pass** | Reasoning Contract §6 |
| Error / idempotency design | **Pass** | Error Handling |
| Traceability end-to-end | **Pass** | Traceability Model |
| Aligns ENGINEERING_STANDARD / ARCHITECTURE_INVARIANTS | **Pass** | Cited throughout |
| Curriculum V1/V2 | **N/A / Pass** | Design does not alter traversal; Retrieval remains interface |

**Residual engineering risk:** Observation metadata may outgrow existing JSON conventions — prefer additive keys; coordinate if new ObservationKind required.

---

## 4. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Dual write path (Engine → Twin mastery) | High | Boundary + architecture tests |
| Double-counting duplicate evidence | High | Idempotent ingress |
| Thin evidence over-claimed as mastery | High | Strength gates in Reasoning (D5) |
| Partial package ambiguity | Medium | Fail-closed default |
| Missing LO / unknown concept fabrication | Medium | Error Handling honesty rules |
| Scope creep into AP-002E Mission triggers | Medium | Explicit non-goals |
| Explainability incomplete at ship | High | Explainability Requirements + checklist at impl |

---

## 5. Extensibility

Design leaves room for:

- Richer evidence dimensions without new authorities  
- Coordinated ObservationKind additions  
- AP-002E intent scheduling on top of improved Twin decisions  
- AP-002F Founder analytics over the same traceability chain  

---

## 6. Verdict

**AP-002D design is approved for implementation planning** under the Evidence Boundary and Reasoning Contract defined in this folder.

Implementation must not begin by modifying Twin, Mission, Graph, or Tutor aggregates beyond lawful projection refresh and decision consumption already in the architecture.

---

## 7. Pack inventory

| Document | Role |
|---|---|
| `INTEGRATION_SPECIFICATION.md` | Full lifecycle transitions |
| `EVIDENCE_BOUNDARY.md` | Exclusive ownership |
| `REASONING_CONTRACT.md` | I/O, errors, versions |
| `DIGITAL_TWIN_UPDATE_RULES.md` | Lawful Twin mutation |
| `MISSION_IMPACT_MODEL.md` | Decision-only mission impact |
| `LEARNING_GRAPH_IMPACT.md` | Projection-only graph impact |
| `EXPLAINABILITY_REQUIREMENTS.md` | Deterministic explainability |
| `ERROR_HANDLING.md` | Invalid / duplicate / partial / recovery |
| `TRACEABILITY_MODEL.md` | End-to-end reconstructability |
| `IMPLEMENTATION_PLAN.md` | D1–D7 engineering tasks |
| `AP-002D_DESIGN_REVIEW.md` | This review |
| `COMPLETION_REPORT.md` | Design milestone completion |
