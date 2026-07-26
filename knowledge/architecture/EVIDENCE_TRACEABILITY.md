# MS-006 — Evidence Traceability

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Contracts:** `EVIDENCE_MODEL.md`, `POLICY_EVALUATION.md`, `EXPERIMENT_FRAMEWORK.md`  
**Related:** MS-002 Journey traceability; MS-003 Adaptive traceability; MS-004 Twin traceability; MS-005 Strategy traceability

---

## 1. Purpose

Link the full observational chain:

```
Runtime A Evidence
    → Twin Interpretation (optional)
    → Adaptive Recommendation (optional)
    → Strategy Intervention (optional)
    → Experience Delivery
    → Student Outcome (Runtime A)
    → Evidence Platform Observation
    → Outcome / Experiment Measurement
    → Policy Evaluation
    → Governance Decision
```

Traceability answers: *which facts and deliveries produced which measured outcomes and policy recommendations* — without the Evidence Platform writing educational history or deciding tonight’s study.

---

## 2. Chain stage authorities

| Stage | Artefact | Authority |
|---|---|---|
| Evidence (facts) | Attempts, missions, progress, goals | **Runtime A** |
| Twin | Snapshot / facets | Twin (interpretation) |
| Adaptive | DecisionTrace / decision_id | Adaptive (advice) |
| Strategy | StrategyTrace / intervention | Strategy (orchestration) |
| Delivery | Projection / authority_status | Experience serving path |
| Outcome (facts) | Subsequent Runtime A events | **Runtime A** |
| Measurement | EvidenceItem / Bundle / OutcomeObservation | Evidence Platform (observational) |
| Evaluation | EvaluationRecord | Evidence Platform (observational) |
| Decision | Governance decision log | Governance (human) |

---

## 3. Traceability matrix

| Link | What is recorded | Required fields | Forbidden |
|---|---|---|---|
| Facts → Twin | Twin provenance (existing) | `twin_snapshot_ref` | Evidence Platform inventing Twin claims |
| Twin → Adaptive | Adaptive attach (existing) | Adaptive twin ref when used | Rewriting Adaptive inputs |
| Adaptive → Strategy | Strategy consume (existing) | `adaptive_decision_id` | Re-ranking via measurement |
| Upstream → Delivery | What was shown | `decision_id` / `strategy_decision_id` / authority_status | Fabricating delivery history |
| Delivery → Outcome | Observational linkage | subject + window + outcome refs + linkage_strength | Invented causation |
| Outcome → EvidenceItem | Intake normalisation | ObservationRefs + claim_boundary | Replacing Runtime A SoT |
| Evidence → OutcomeObservation | Metric derivation | `outcome_definition_id`, bundle id | Boundary leakage |
| Bundle → Evaluation | Policy evaluation inputs | policy version, statistical plan, explanation | Hidden reasoning |
| Evaluation → Governance | Decision linkage | `evaluation_id`, decision, rollback_map executed? | Auto-apply flags from evaluation |
| Full chain | End-to-end audit | Reconstructable lineage artefact | Claiming measurement caused mastery |

---

## 4. `EvidencePlatformTrace` (design)

Every shadow or promote-grade evaluation/measurement run can produce a reconstructable trace — observational (in-memory + telemetry initially); no educational tables; not student-facing SoT.

| Field | Meaning |
|---|---|
| `trace_id` | Deterministic when possible |
| `correlation_id` | Prefer continue upstream correlation when measuring a delivery |
| `platform_version` | Intake / evaluator version |
| `feature_flag_state` | Evidence Platform + relevant upstream flags |
| `runtime_a_snapshot_id` | Fingerprint of material Runtime A block when used |
| `twin_snapshot_ref` | or `unavailable` |
| `adaptive_decision_id` | or `unavailable` |
| `strategy_decision_id` | or `unavailable` |
| `delivery_ref` | Experience delivery / authority_status ref or `unavailable` |
| `assignment_id` | When experiment-backed |
| `evidence_bundle_id` | |
| `outcome_observation_ids[]` | |
| `evaluation_id` | When evaluation emitted |
| `explainability_gate_result` | Gate canonical dict |
| `authority_status` | `shadow_only` \| `measurement_only` \| `gate_ineligible` \| `failed` — **never** educational Authority |
| `executed_at` | Observational wall-clock |

### Correlation rules

1. Explicit `correlation_id` argument wins.  
2. Else reuse upstream `CorrelationContext` when measuring a known Adaptive/Strategy delivery.  
3. Else mint a new id for the measurement lifecycle.  
4. Governance decision ids link by reference; they are not educational correlation.

### Reconstruction workflow

```
Runtime A Evidence
    ↓
(optional) Twin / Adaptive / Strategy traces
    ↓
Experience Delivery
    ↓
Runtime A Outcome (windowed)
    ↓
ObservationRefs → EvidenceItems → EvidenceBundle
    ↓
OutcomeObservations
    ↓
EvaluationRecord + ExplanationBundle
    ↓
Governance Decision (reference)
```

`EvidenceTraceabilityService.reconstruct_lineage(trace_id | evaluation_id)` (design name) rebuilds lineage deterministically from the stored trace.

---

## 5. Outcome linkage (observational)

| Rule | Meaning |
|---|---|
| Window | Documented per outcome definition / experiment |
| Match keys | `student_id` + topic/mission overlap + time order |
| Strength | `linked` / `ambiguous` / `none` |
| Authority | Outcomes remain Runtime A facts; traces only reference them |
| Causation language | Analysis may discuss association under design; must not claim Engine “wrote” mastery |

**Forbidden:** Writing Journey/History from Evidence Platform; claiming evaluation improved student understanding.

---

## 6. Per-artefact expectations

| Artefact | Must cite | Typical next link |
|---|---|---|
| EvidenceItem (FACT_EVENT) | Runtime A entity ids | Bundle / outcome |
| EvidenceItem (DELIVERY_EVENT) | Upstream decision/intervention ids + authority_status | Outcome linkage |
| OutcomeObservation | Bundle + definition + boundary | Evaluation / scorecard |
| ExperimentAnalysis | Assignments + exposures + outcomes | Evaluation |
| EvaluationRecord | Policy version + evidence + statistics + explanation | Governance |
| Governance decision | Evaluation id + rollback_map | Flag apply verification (ops) |

---

## 7. Relationship to upstream traces

| Trace | Owns | Evidence Platform |
|---|---|---|
| Journey / History (MS-002) | Student-facing continuity of Runtime A | May reference event ids; must not replace |
| DecisionTrace (MS-003) | Advice lineage | Consume for delivery/advice linkage |
| TwinTrace (MS-004) | Interpretation lineage | Consume as supporting |
| StrategyTrace (MS-005) | Orchestration lineage | Consume for intervention delivery |
| EvidencePlatformTrace (MS-006) | Measurement → evaluation lineage | Owns this layer only |

**Composition:** Full-chain audits may join by `correlation_id` / decision ids; join failures yield `ambiguous`, never fabricated edges.

---

## 8. Privacy / governance

| Rule | Binding |
|---|---|
| Refs not payloads | No raw answers in traces |
| Student scope | No cross-student leakage |
| Telemetry minimal | No secrets / cookies / credentialed DB URLs |
| Retention | ADR-MS006-002 — observational; not educational SoT |
| Demo markers | Fail promote-grade reconstruction consumers |

---

## 9. Telemetry (design names)

| Event | When |
|---|---|
| `EVIDENCE_TRACE_CREATED` | Trace recorded |
| `EVIDENCE_TRACE_FAILED` | Trace with error / miss |
| `EVIDENCE_TRACE_RECONSTRUCTED` | Lineage rebuild |
| `EVIDENCE_EVAL_GATED` | Explainability gate result |
| `EVIDENCE_LINKAGE_AMBIGUOUS` | Delivery→outcome ambiguous (rate monitor) |

---

## 10. Non-goals

- Student-facing “why the experiment chose you” UX in this directive  
- Durable educational audit warehouse (optional later ADR)  
- Using traces as Planning inputs  

---

## 11. Acceptance hooks

Architecture PASS requires:

- Reconstructable observational lineage  
- No Evidence Platform educational writes  
- Honest linkage strength  
- Clear separation from upstream authority traces
