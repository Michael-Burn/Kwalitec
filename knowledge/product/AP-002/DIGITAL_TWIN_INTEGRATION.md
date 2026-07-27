# AP-002 — Digital Twin Integration

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Authority reminder

Per `ARCHITECTURE_INVARIANTS.md`:

- Student Digital Twin is the sole learner-state SoT
- Assessment produces observations
- Twin updates from assessment flow through the lawful Reasoning path
- Tutor / Mission must not maintain competing learner stores

---

## 2. End-to-end chain

```
Assessment
    ↓
Observation
    ↓
Twin Update
    ↓
Reasoning
    ↓
Learning Graph
    ↓
Mission Engine
    ↓
Tutor
```

Each transition is explained below. Note: **Reasoning performs Twin inference updates**; the Twin stores the resulting state. Ordering in product speech sometimes says “Twin Update” after Reasoning — both mean: observations land, then Reasoning revises Twin-owned inferences.

Canonical operational order (aligned with AP-001):

```
Assessment Engine session/response
        ↓
AP-001 Assessment Event (immutable)
        ↓
Observation append (SDT-001 fact)
        ↓
StudentReasoningService → Educational Reasoning Engine
        ↓
Twin inference fields updated (mastery, gaps, confidence, recommendations, …)
        ↓
Learning Graph mastery projection refresh
        ↓
Adaptive Mission Engine consumes decisions (optional refresh)
        ↓
Intelligent Tutor explains outcomes (optional)
```

---

## 3. Transition explanations

### Assessment → Observation

The Engine captures responses and evaluates evidence dimensions (correctness, hints, misconceptions, …). It does **not** conclude mastery. Through AP-001, an Assessment Event becomes an Observation with provenance `assessment_pipeline:…` plus Engine session metadata.

**Guarantee:** append-only facts; no Twin inference writes here.

### Observation → Twin Update (via Reasoning)

Observations are attached to the Twin aggregate via `ObservationService`. Inference fields change only when `StudentReasoningService.reason` runs. Assessment must not call Twin mutators for mastery/gaps/recommendations directly.

**Guarantee:** Evidence before inference; deterministic rules; curriculum via Retrieval only.

### Twin Update → Reasoning

In practice Reasoning *is* the update mechanism for inferences. After a reasoning run, Twin holds revised educational belief and a reasoning history entry for audit (MS-004 traceability).

### Reasoning → Learning Graph

Graph stores relationships, not a second SoT. After Twin mastery/gap changes, Graph projections refresh so prerequisite/recovery structure reflects current belief without owning it.

### Learning Graph → Mission Engine

Mission Engine reads Twin decisions and Graph recovery/prerequisite paths to schedule activities — including future assessment intents. It never invents educational recommendations.

### Mission Engine → Tutor

Tutor explains mission and assessment-related decisions using assembled evidence. Conversation memory stays session-scoped; long-term belief remains Twin-owned.

---

## 4. What the Twin receives from Assessment

| Input | Form |
|---|---|
| Facts | ObservationKind + metadata evidence dimensions |
| Links | Assessment Result / event ids for audit |
| Soft signals | Confidence, timing (non-authoritative alone) |
| Intent context | diagnostic / checkpoint / verification / … |

| Twin must not receive from Assessment | |
|---|---|
| Precomputed mastery percentages as authority | |
| Tutor prose as fact | |
| Mission priority overrides | |
| Fabricated curriculum claims | |

---

## 5. Observation kind strategy

Prefer mapping Engine outcomes onto existing `ObservationKind` values (AP-001 table) to avoid Twin schema churn in early milestones.

If new kinds are truly required (e.g. `concept_link_assessed`), they belong to a Twin/Observation additive milestone with Reasoning rule updates — not a silent Engine fork.

---

## 6. Uncertainty reduction contract

Assessment succeeds for the Twin when it:

1. Adds observations where evidence was thin
2. Clarifies misconception categories on open gaps
3. Improves calibration data (confidence vs correctness)
4. Supports spaced stability checks

Assessment fails educationally when it:

1. Floods Twin with low-value noise
2. Creates false certainty from single lucky items
3. Bypasses Reasoning
4. Over-assesses and erodes trust

---

## 7. Compatibility

- SDT-001 → SDT-003 remain intact
- AP-001 remains the preferred observation ingress
- Legacy `StudyAttempt` paths coexist until a deliberate cutover
- No architecture redesign of Twin aggregates in AP-002 design
