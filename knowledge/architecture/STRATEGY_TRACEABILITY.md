# MS-005 — Strategy Traceability

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Contracts:** `STRATEGY_INTERFACE_SPECIFICATION.md`, `STRATEGY_EXPLAINABILITY.md`  
**Related:** MS-003 `ADAPTIVE_TRACEABILITY.md`; MS-004 `DIGITAL_TWIN_TRACEABILITY.md`; MS-002 `JOURNEY_TRACEABILITY_MATRIX.md`

---

## 1. Purpose

Link the strategy orchestration chain:

```
Runtime A Evidence
    → Twin Interpretation
    → Adaptive Recommendation
    → Strategy Intervention
    → Experience Delivery
    → Student Outcome (Runtime A)
```

Traceability answers: *which facts, Twin factors, and Adaptive advice produced which intervention; what the student was shown; and what authorised Runtime A outcome followed* — without the Strategy Engine writing outcomes.

---

## 2. Chain definitions

| Stage | Artefact | Authority |
|---|---|---|
| **Evidence** | Accepted StudyAttempts, TopicProgress, Missions, Readiness, Goals, Curriculum | Runtime A |
| **Twin Interpretation** | `TwinSnapshot` / facet claims | Digital Twin |
| **Adaptive Recommendation** | `AdaptiveDecisionRecord` / `decision_id` | Adaptive Engine (advice only) |
| **Strategy Intervention** | `StrategyDecisionRecord` / `InterventionPlan` | Strategy Engine (orchestration only) |
| **Experience Delivery** | OpaqueDict / UI projection | Projection (Strategy and/or prior path) |
| **Student Outcome** | Subsequent Mission completion, attempts, progress | Runtime A write paths |

---

## 3. Traceability matrix

| Link | What is recorded | Required fields | Forbidden |
|---|---|---|---|
| Evidence → Twin | Twin provenance already owns this | Twin `snapshot_ref`, evidence version | Strategy inventing Twin provenance |
| Twin → Adaptive | Adaptive Twin attachment (MS-004 T4) | Adaptive input twin ref when used | Strategy rewriting Adaptive inputs |
| Evidence + Twin + Adaptive → Strategy | Input refs that materially shaped intervention | `runtime_a_snapshot_id`, `twin_snapshot_ref`, `adaptive_decision_id`, `input_fingerprint` | Invented refs; citing non-owned evidence |
| Strategy → Delivery | What was shown vs raw Strategy outputs | `strategy_decision_id`, primary kind, mission_aligned, authority_status | Showing unexplained interventions |
| Delivery → Outcome | Observational linkage after student action | `strategy_decision_id` + time window + outcome mission/attempt ids | Claiming Strategy caused mastery; writing outcome from Strategy |
| Full chain | End-to-end audit for Alpha / research | Fixture: evidence → Twin → Adaptive → Strategy → DTO → later SQL outcome | Fabricating intervention history |

---

## 4. `StrategyTrace` (design)

Every shadow or authoritative Strategy execution can produce a reconstructable `StrategyTrace` — observational (in-memory + telemetry initially); no educational tables; no student-facing history as SoT.

| Field | Meaning |
|---|---|
| `strategy_decision_id` | Strategy decision identity (digest of input serialize when available) |
| `correlation_id` | Shared lifecycle id across Strategy + related Adaptive/Twin telemetry |
| `engine_version` | Strategy executor / adapter version |
| `feature_flag_state` | Engine / Shadow / Authority snapshot |
| `runtime_a_snapshot_id` | Fingerprint of Runtime A material block |
| `twin_snapshot_ref` | Twin fingerprint or `unavailable` |
| `adaptive_decision_id` | Adaptive decision id or `unavailable` |
| `input_bundle_ref` | `StrategyInputBundle` fingerprint |
| `output_bundle_ref` | `StrategyDecisionRecord` fingerprint |
| `intervention_plan_ref` | InterventionPlan fingerprint |
| `explainability_gate_result` | Gate canonical dict (or empty when gate not run) |
| `authority_status` | `shadow_only` / `strategy_engine` / `gate_ineligible` / `fallback` / `failed` |
| `executed_at` | Observational wall-clock ISO (not decision material) |

### Correlation rules

1. Explicit `correlation_id` argument wins.  
2. Else reuse current `CorrelationContext` (may already bind Adaptive decision).  
3. Else mint a new id and bind it for the Strategy lifecycle.  
4. Prefer continuing Adaptive correlation when Strategy consumes that Adaptive decision in the same request.

### Reconstruction workflow

```
Evidence (Runtime A)
    ↓
TwinSnapshot
    ↓
AdaptiveDecisionRecord
    ↓
StrategyInputBundle
    ↓
StrategyDecisionRecord / InterventionPlan
    ↓
Explainability Result
    ↓
Routing Decision
    ↓
Intervention Delivered (or Shadow Only)
    ↓
Runtime A Outcome (observational link)
```

`StrategyTraceabilityService.reconstruct_lineage(strategy_decision_id)` rebuilds lineage deterministically from the stored trace (identical serialize on repeat).

---

## 5. Outcome linkage (observational)

| Rule | Meaning |
|---|---|
| Window | Link outcomes occurring after `executed_at` within a documented window (e.g. same night / next session) |
| Match keys | Same `student_id` + mission/attempt topic overlap with intervention topic_refs |
| Strength | `linked` / `ambiguous` / `none` — never invent causation |
| Authority | Outcomes remain Runtime A facts; StrategyTrace only references them |

**Forbidden:** Writing Journey/History events from Strategy; claiming intervention “improved mastery.”

---

## 6. Per-intervention-kind trace expectations

| Kind | Must cite | Typical outcome link |
|---|---|---|
| `SESSION_PLAN` | Mission (if any) + Adaptive decision + principle `ep.director.nightly_topic` | Mission start/complete |
| `REVISION_PLAN` | Adaptive revision_priority + TopicProgress refs | Revision session attempts |
| `RECOVERY_PLAN` | Trigger attempt/mission refs + Twin persistence | Subsequent mission resume/complete |
| `FATIGUE_MANAGEMENT` | Twin cognitive_load + recent activity refs | Shortened session / no start (observational) |
| `CONFIDENCE_INTERVENTION` | Twin confidence_trend + attempt performance refs | Practice-close attempt honesty |
| `STUDY_PLAN` | Goals + Adaptive topic set | Multi-day mission sequence (loose link) |

---

## 7. Privacy / governance

| Rule | Binding |
|---|---|
| Refs not payloads | Trace stores ids / fingerprints, not raw answers |
| Student scope | Traces never cross student_id |
| Telemetry minimal | No secrets, full DB URLs, or session cookies |
| Retention | Observational store policy deferred (ADR-MS005-002) — not educational SoT |

---

## 8. Relationship to Adaptive / Twin traces

| Trace | Owns |
|---|---|
| TwinTrace (MS-004) | Evidence → Twin claims → projection |
| DecisionTrace (MS-003) | Evidence → Adaptive decision → recommendation delivery |
| StrategyTrace (MS-005) | Evidence + Twin + Adaptive → intervention → delivery → outcome |

StrategyTrace **references** Twin and Adaptive ids; it does not duplicate their internal lineage stages unless needed for reconstruction convenience. Prefer foreign refs over copy.

---

## 9. Acceptance checks (future implementation)

| Id | Check |
|---|---|
| ST-1 | Every Authority-delivered intervention has StrategyTrace with Adaptive + Runtime A refs (or documented unavailable) |
| ST-2 | Twin unavailable still yields reconstructable trace with explicit twin unavailable |
| ST-3 | Gate FAIL produces trace with `gate_ineligible` and no UX delivery |
| ST-4 | Identical input bundle → identical strategy_decision_id |
| ST-5 | Outcome linkage never mutates Runtime A |
| ST-6 | Correlation id shared with Adaptive when consumed in-request |
