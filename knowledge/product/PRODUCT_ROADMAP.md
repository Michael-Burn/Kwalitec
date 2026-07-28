# Product Roadmap — Intelligent Learning Experience

**Programme:** ILE-000  
**Version:** 1.0  
**Status:** Active — programme roadmap (not a sprint backlog)  
**Effective:** 2026-07-28  

---

## Purpose

Organise future work as **product experience programmes** after platform certification and production readiness.

This roadmap does **not** prescribe architecture milestones. Engineering designs serve ILE outcomes and remain bound by Educational Constitution, Vision 2030, and architecture law.

Indicative sequencing only. Product Board may reorder on evidence (KSI gaps, Stage 1 findings, privacy gates).

---

## Roadmap principles

1. **Value over construction** — ship student-perceivable learning usefulness.  
2. **Surface certified intelligence** before inventing new engines.  
3. **Trust before breadth** — IFoA depth before multi-body sprawl.  
4. **Evidence creates features** — align with Version 2 evidence lifecycle.  
5. **One story on Home** — no competing educational authorities in UX.

---

## Programme catalogue

### ILE-001 — Adaptive Assessment

**Intent:** Make assessment feel like a learning instrument: capture evidence cleanly, interpret honestly, and feed the Twin without mastery theatre.

**Student outcome:** Attempts produce understandable feedback and visible effect on “what the system believes.”

**Depends on:** Assessment pipeline + Educational Intelligence orchestrator product wiring decisions; EQ/EVF honesty.

**Feeds:** ILE-002, ILE-003, ILE-005.

---

### ILE-002 — Adaptive Mission Experience

**Intent:** Complete the daily loop: one calm session, curriculum-bound, realistic duration, clear completion, bridge to tomorrow.

**Student outcome:** “I always know today’s session and why it exists.”

**Depends on:** Adaptive Mission Engine; Learning Experience Programme (LXP) intent; Home decision hygiene.

**Feeds:** ILE-004, ILE-006.

---

### ILE-003 — Explain My Learning

**Intent:** Student-facing explainability as a first-class experience — what / why / what next / uncertainty — for recommendations, readiness, and missions.

**Student outcome:** Trust through understanding, not through blind acceptance.

**Depends on:** Explainability Standard; Tutor explanation service; MES delivery patterns.

**Feeds:** Trust metrics, K8, recommendation acceptance quality.

---

### ILE-004 — Daily Mission Intelligence

**Intent:** One primary daily educational mission — the centre of the student's daily interaction — composed from authorised educational evidence with full explainability.

**Student outcome:** “This is the most valuable thing I can do today. I know why. I trust it.”

**Depends on:** ILE-010 / ILE-011; ILE-001C0 / ILE-001C; Decision Journal (ILE-002); Educational Timeline (ILE-003); P-001.2; P-001.3; authorised Runtime A recommendation / MES.

**Feeds:** Daily trust loop; journal/timeline continuity; later Study Intelligence.

> **Note:** An earlier ILE-000 roadmap draft titled ILE-004 “Learning Timeline”; that outcome was delivered as **ILE-003 Educational Timeline**. ILE-004 now names Daily Mission Intelligence per product programme brief.


---

### ILE-005 — Educational Feedback Loop

**Intent:** Evaluate whether Study Sensei guidance was educationally useful over time — via recommendation review, optional student reflection, and internal Sensei educational reviews — without changing selection.

**Student outcome:** Optional reflection on guidance usefulness; trust that outcomes are remembered honestly.

**Depends on:** Decision Journal (ILE-002); Educational Timeline (ILE-003); Daily Mission Intelligence (ILE-004); P-001.2; P-001.3; KSI.

**Feeds:** Educational quality governance; later Study Intelligence / Analytics honesty.

> **Note:** An earlier ILE-000 roadmap draft titled ILE-005 “Confidence & Uncertainty Experience”; that confidence UX theme remains covered by ILE-001 assessment contracts and journal qualitative bands. ILE-005 now names Educational Feedback Loop per product programme brief.

---

### ILE-006 — Study Intelligence

**Intent:** Higher-order insights: pacing vs exam date, revision load, workload sustainability, pattern summaries — still explainable and non-authoritative where required.

**Student outcome:** Better multi-week judgement without dashboard sprawl.

**Depends on:** ILE-003–005 foundations; burnout monitor; Personal Learning Profile boundaries.

**Feeds:** Premium analytics narrative; institution reporting later.

---

### ILE-007 — Collaboration

**Intent:** Bounded collaboration (mentor/provider/employer views, shared goals) that does not create a social network or dual educational truth.

**Student outcome:** Optional human support informed by the same Educational State.

**Depends on:** Privacy / DPA readiness; institution licensing direction; student data ownership principles.

**Feeds:** Enterprise monetisation.

---

### ILE-008 — Mobile Experience

**Intent:** Daily mission and explainability usable on phones with parity of educational truth (not a cut-down contradictory app).

**Student outcome:** Study decisions on the commute without losing honesty.

**Depends on:** Stable Home/Session IA (ILE-002/003); performance budgets.

**Feeds:** Retention for employed candidates.

---

### ILE-009 — Analytics

**Intent:** Student and (later) cohort analytics that measure learning usefulness — completion quality, calibration, recommendation follow-through — not vanity DAU.

**Student outcome / operator outcome:** Insight that improves study and product decisions.

**Depends on:** Telemetry honesty; Stage 1 metric catalogue (EP-003 M1–M9); privacy.

**Feeds:** KSI recalculation; commercial packaging evidence.

---

## Indicative sequencing

```
Foundation (complete / parallel ops)
  Platform certification + PR-001 readiness
  Version 1 gates / Stage 1 privacy & effectiveness (ongoing Board HOLD items)

Wave A — Daily trust loop
  ILE-002 Adaptive Mission Experience
  ILE-003 Explain My Learning
  ILE-001 Adaptive Assessment (may parallel where evidence capture blocks the loop)

Wave B — Continuity & honesty of state
  ILE-005 Educational Feedback Loop
  ILE-004 Daily Mission Intelligence

Wave C — Depth
  ILE-006 Study Intelligence
  ILE-009 Analytics (student-first slice)

Wave D — Reach
  ILE-008 Mobile Experience
  ILE-007 Collaboration (after privacy + institutional packaging)
```

**Parallel non-ILE work** (not replaced by this roadmap): Stage 1 evidence closure, KSI → 80 programmes, curriculum publishing quality, commercial packaging.

---

## Dependency sketch

```mermaid
flowchart TD
  A[ILE-001 Adaptive Assessment] --> B[ILE-002 Adaptive Mission Experience]
  B --> C[ILE-003 Explain My Learning]
  C --> D[ILE-005 Educational Feedback Loop]
  C --> E[ILE-004 Daily Mission Intelligence]
  D --> F[ILE-006 Study Intelligence]
  E --> F
  F --> G[ILE-009 Analytics]
  B --> H[ILE-008 Mobile Experience]
  C --> H
  G --> I[ILE-007 Collaboration]
  H --> I
```

---

## Explicit non-goals of this roadmap

- Rewriting Educational Intelligence architecture for novelty  
- LLM recommendation authority  
- Multi-profession catalogue explosion before IFoA proof  
- Social gamification home  
- Declaring Version 1 production-ready without P-002.1 gates  

---

## How programmes enter delivery

1. Evidence (blind review, Stage 1, KSI gap, dogfood)  
2. PRD subordinate to Vision / Constitution / ILE strategy  
3. Architecture review if structural  
4. Implementation + explainability / recommendation reviews when in scope  
5. Perception or cohort validation before strong effectiveness claims  

Related: `PRODUCT_STRATEGY.md`, `SUCCESS_METRICS.md`, `PRODUCT_BLUEPRINT.md`, `knowledge/product/roadmap/VERSION2_PRODUCT_STRATEGY.md`.

---

**End of PRODUCT_ROADMAP**
