# AP-002D — Integration Specification

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative for implementation)  
**Related:** [`ARCHITECTURE_INVARIANTS.md`](../../engineering/ARCHITECTURE_INVARIANTS.md), [`AP-002/EVIDENCE_MODEL.md`](../AP-002/EVIDENCE_MODEL.md), [`AP-002/DIGITAL_TWIN_INTEGRATION.md`](../AP-002/DIGITAL_TWIN_INTEGRATION.md), AP-002C Evidence Packaging  

---

## 1. Purpose

Define the complete lifecycle by which Assessment Evidence enters the Educational Intelligence Platform — without Assessment becoming a second reasoning authority.

This specification governs AP-002D implementation. It does not redesign Twin, Reasoning, Mission, Graph, or Tutor aggregates.

---

## 2. Canonical lifecycle

```
Assessment Session
        ↓
Observation (Engine facts)
        ↓
Evidence Bundle (AP-002C packaged facts)
        ↓
Evidence Boundary (AP-001 ingress)
        ↓
StudentReasoningService
        ↓
Educational Decisions
        ↓
Student Digital Twin (inferences applied)
        ↓
Learning Graph (projection refresh)
        ↓
Mission Engine (consumes decisions)
        ↓
Tutor (explains)
```

**Invariant:** Evidence is not knowledge. Evidence is not mastery. Evidence is not confidence. Only `StudentReasoningService` may transform evidence into educational understanding.

---

## 3. Transition contracts

### 3.1 Assessment Session → Observation

| Aspect | Contract |
|---|---|
| **Input** | Active `AssessmentSession`, committed `Response`, instrument item, evaluation rules |
| **Output** | Immutable Engine `Observation` (or equivalent fact record) with evidence dimensions: correctness, confidence, hints, retries, timing, misconception tags, curriculum refs |
| **Authority** | Assessment Engine (delivery + evaluation) |
| **Responsibilities** | Capture what happened; evaluate against accepted response/rubric; attach provenance (session, item version, intent) |
| **Forbidden** | Mastery writes; gap creation; recommendations; mission priority; Twin inference mutators; learner-state interpretation |

Assessment knows only observations. Assessment does not know the learner as an educational belief model.

---

### 3.2 Observation → Evidence Bundle

| Aspect | Contract |
|---|---|
| **Input** | Ordered session observations (`ObservationCollection`) |
| **Output** | Immutable `EvidenceBundle` (`EvidenceItem`s, metadata, summary, strength band thin/moderate/strong) |
| **Authority** | Assessment Engine packaging (`EvidencePackagingService` / domain packager) |
| **Responsibilities** | Aggregate, de-duplicate, validate structural integrity, band evidence **quality** (not educational certainty), preserve observation traceability |
| **Forbidden** | Inference; Estimated Knowledge / Mastery language; Twin updates; calling Reasoning; inventing curriculum claims |

Strength bands describe packaging quality (completeness, scaffolding, coverage). They never assert learner mastery.

---

### 3.3 Evidence Bundle → StudentReasoningService (via Evidence Boundary)

| Aspect | Contract |
|---|---|
| **Input** | Validated `EvidenceBundle` export (AP-001-facing DTO) + Twin identity + curriculum entity refs |
| **Output** | AP-001 `AssessmentEvent`(s) → Twin `Observation`(s) appended via `ObservationService`; then `StudentReasoningService.reason(...)` invoked by the lawful pipeline |
| **Authority** | Assessment Pipeline (AP-001) as **ingress orchestrator**; Reasoning as **inference authority** |
| **Responsibilities** | Map bundle items → pipeline events/observations without loss of provenance; set `triggered_by` to `assessment_pipeline:…` (engine session id in metadata); pass observation ids into Reasoning; never reinterpret educational policy |
| **Forbidden** | Assessment Engine calling Twin mastery/gap/recommendation mutators directly; Assessment Engine invoking Educational Reasoning Engine as a private bypass; fabricating observations to fill gaps |

**Ingress rule:** AP-001 remains the preferred observation ingress. AP-002D wires Evidence Bundle export into that path. It does not invent a second Twin-write channel.

See [`EVIDENCE_BOUNDARY.md`](EVIDENCE_BOUNDARY.md) and [`REASONING_CONTRACT.md`](REASONING_CONTRACT.md).

---

### 3.4 StudentReasoningService → Educational Decisions

| Aspect | Contract |
|---|---|
| **Input** | Twin aggregate (prior inferences + new observations), observation ids, `triggered_by`, curriculum evidence via Retrieval, Learning Graph structure (relationships only) |
| **Output** | `ReasoningResult`: mastery map, confidence state, learning state, knowledge gaps, recommendations, educational decisions, explanations, rule executions, run id, engine version |
| **Authority** | `StudentReasoningService` → Educational Reasoning Engine (`RuleRegistry`) |
| **Responsibilities** | Deterministic inference from evidence + prior Twin state; record reasoning history; refuse LLM in core path; honour evidence-before-inference and thin-evidence honesty |
| **Forbidden** | Fabricating observations; inventing curriculum without Retrieval; accepting soft signals alone as high-mastery authority; silently ignoring evidence-strength gates |

---

### 3.5 Educational Decisions → Student Digital Twin

| Aspect | Contract |
|---|---|
| **Input** | `ReasoningResult` from StudentReasoningService |
| **Output** | Twin with updated inference fields + `ReasoningRecord` + timeline events |
| **Authority** | Twin aggregate (storage of learner educational belief); writes applied **only** through Reasoning orchestration |
| **Responsibilities** | Persist mastery, gaps, confidence, recommendations, learning-state snapshot as reasoned belief; retain append-only observations |
| **Forbidden** | Assessment, Mission, Tutor, or Graph writing inference fields; overwriting observations; treating Evidence Bundle as Twin SoT |

See [`DIGITAL_TWIN_UPDATE_RULES.md`](DIGITAL_TWIN_UPDATE_RULES.md).

---

### 3.6 Student Digital Twin → Learning Graph

| Aspect | Contract |
|---|---|
| **Input** | Updated Twin inferences (especially mastery / gap projections relevant to structure) |
| **Output** | Refreshed Graph **projections** of relationships conditioned on current Twin belief |
| **Authority** | Learning Graph Service (structure + projections); Twin remains SoT for learner belief |
| **Responsibilities** | Update prerequisite / recovery / related-concept projections so Mission can traverse structure honestly |
| **Forbidden** | Storing a competing mastery SoT; inventing recommendations; mutating Twin inferences |

See [`LEARNING_GRAPH_IMPACT.md`](LEARNING_GRAPH_IMPACT.md).

---

### 3.7 Learning Graph → Mission Engine

| Aspect | Contract |
|---|---|
| **Input** | Twin decisions / recommendations / gaps; Graph recovery & prerequisite paths; workload / Learning Mode constraints |
| **Output** | Mission plan / activities (may include future assessment intents — AP-002E) |
| **Authority** | Adaptive Mission Engine (scheduling only) |
| **Responsibilities** | Schedule **what to do** from already-reasoned decisions; respect eligibility gates; remain explainable |
| **Forbidden** | Inventing educational recommendations; writing Twin mastery; re-scoring assessment evidence |

See [`MISSION_IMPACT_MODEL.md`](MISSION_IMPACT_MODEL.md).

---

### 3.8 Mission Engine → Tutor

| Aspect | Contract |
|---|---|
| **Input** | Mission context, Twin state, Reasoning explanations, Learning Feedback / Assessment Result summaries, Retrieval excerpts |
| **Output** | Student-facing explanation / encouragement / next-action narration |
| **Authority** | Intelligent Tutor (explanation only) |
| **Responsibilities** | Explain decisions already made; assemble evidence for conversation; keep psychological safety |
| **Forbidden** | Grading; alternate mastery conclusions; Twin writes; silent re-scoring |

---

## 4. End-to-end authority chain (non-negotiable)

| Step | Owner |
|---|---|
| Produce observations | Assessment Engine |
| Package evidence | Assessment Engine (AP-002C) |
| Ingress facts into Twin | AP-001 Pipeline + ObservationService |
| Infer educational meaning | StudentReasoningService only |
| Store learner belief | Student Digital Twin |
| Relate concepts | Learning Graph |
| Schedule activity | Mission Engine |
| Explain | Tutor |

---

## 5. Compatibility constraints

1. No architecture redesign of Twin, Reasoning, Mission, Graph, or Tutor.
2. Curriculum V1 and V2 remain loadable; curriculum evidence only via Retrieval.
3. Legacy `StudyAttempt` / LXP practice paths coexist until deliberate cutover.
4. AP-002D may extend observation **metadata contracts** and Reasoning **rule consumption** of new dimensions — not authority boundaries.
5. Feature flags / opt-in wiring preferred where student-visible behaviour changes.

---

## 6. Success criteria (design)

AP-002D is correctly designed when:

1. Evidence Bundle can reach Reasoning without Assessment owning inference.
2. Same bundle + same Twin state → same educational decisions.
3. Every Twin update from assessment is reconstructable (see [`TRACEABILITY_MODEL.md`](TRACEABILITY_MODEL.md)).
4. Architecture tests can forbid direct Engine → Twin mastery writes.
