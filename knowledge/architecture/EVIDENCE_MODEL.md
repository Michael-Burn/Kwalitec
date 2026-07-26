# MS-006 — Evidence Model

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Related:** MS-002 `JOURNEY_DATA_MODEL.md`; MS-003 `ADAPTIVE_TRACEABILITY.md`; MS-004 `DIGITAL_TWIN_DATA_MODEL.md`; MS-005 `STRATEGY_TRACEABILITY.md`; EP-004 SP4 / SP8

---

## 1. Purpose

Define the **logical evidence model** for observational measurement: what counts as evidence, how it is lifecycle-managed, how claim boundaries are tagged, and what must never be invented or promoted to educational source of truth.

This model is **logical only**. No schema / Alembic changes in this directive.

---

## 2. Core distinction

| Concept | Authority | Meaning |
|---|---|---|
| **Educational fact** | Runtime A | What the student did / what the system recorded as educational history |
| **Interpretation claim** | Twin | Longitudinal statements about the learner (not facts) |
| **Recommendation** | Adaptive | Advice artefacts |
| **Intervention** | Strategy | Orchestrated action structure |
| **Delivery observation** | Experience traces | What was shown / which authority path served |
| **Measurement evidence** | Evidence Platform | Observational artefacts used for outcomes, experiments, and policy evaluation |

**Invariant:** Measurement evidence **references** educational facts; it does not replace them.

---

## 3. Claim boundaries (binding)

Every evidence artefact and outcome metric must carry a **claim boundary** tag.

| Boundary | May claim | Must not claim |
|---|---|---|
| `organisation` | Start/continue reliability, session completion, recovery success, checklist adherence, director clarity proxies | Learning improvement, mastery gain, exam readiness |
| `learning_signal` | Attempt honesty logged, practice outcome recorded, within-topic attempt patterns (observational) | Causal learning depth without pre-registered design |
| `learning_depth` | Pre-registered constructs with explicit limitations | Exam-mark transfer; “student learned X” from completion alone |
| `transfer` | Explicitly deferred unless separate evidence programme | Any product-facing exam-mark guarantee |
| `trust_inspectability` | Explanation completeness rates, empty-vs-theatre incidents (ops) | Student psychological trust as measured fact without instrument |

EP-004 SP8 is encoded here: **organisation success ≠ learning-depth success**.

---

## 4. Evidence artefact types

### 4.1 `ObservationRef`

Minimal pointer into an upstream authority (prefer ids / fingerprints over payloads).

| Field | Meaning |
|---|---|
| `ref_kind` | `runtime_a` \| `twin` \| `adaptive` \| `strategy` \| `experience` \| `telemetry` |
| `entity_kind` | e.g. `StudyAttempt`, `Mission`, `DecisionTrace`, `StrategyTrace` |
| `entity_id` | Stable id when available |
| `fingerprint` | Content digest when id unavailable |
| `observed_at` | Wall-clock observation time (observational) |
| `as_of` | Educational as-of when material (from upstream snapshot) |
| `student_id` | Scoped; never cross-student |
| `claim_boundary` | Per §3 |

### 4.2 `EvidenceItem`

Normalised observational unit after intake.

| Field | Meaning |
|---|---|
| `evidence_id` | Deterministic id from normalised serialize when possible |
| `source_refs[]` | One or more `ObservationRef` |
| `evidence_class` | See §5 |
| `quality` | `EvidenceQuality` (§7) |
| `payload_summary` | Non-authoritative summary fields allowed for analysis (no raw answers) |
| `limitations[]` | Codes when incomplete / stale / ambiguous |
| `engine_version` | Intake / normaliser version |

### 4.3 `EvidenceBundle`

Frozen set of `EvidenceItem`s for an evaluation or experiment measurement window.

| Field | Meaning |
|---|---|
| `bundle_id` | Fingerprint of membership + window |
| `policy_id` / `policy_version` | When assembled for policy evaluation |
| `experiment_id` / `arm_id` | When assembled for experiment measurement |
| `window` | `{ start, end, timezone_policy }` |
| `population_ref` | Cohort / eligibility definition id |
| `items[]` | EvidenceItem ids |
| `claim_boundary_mix` | Counts per boundary (detect SP8 leakage) |
| `quality_summary` | Aggregate gate result |

### 4.4 `OutcomeObservation`

Typed outcome instance derived from an EvidenceBundle (see also `OUTCOME_ANALYTICS.md`).

| Field | Meaning |
|---|---|
| `outcome_id` | Deterministic from definition + subject + window |
| `outcome_definition_id` | Registered outcome definition |
| `claim_boundary` | Must match definition |
| `subject_scope` | `student` \| `cohort` \| `system` |
| `value` | Typed scalar / categorical / distribution handle |
| `uncertainty` | Interval / band / `not_estimable` |
| `evidence_bundle_id` | Provenance |
| `limitations[]` | Required when thin |

---

## 5. Evidence classes

| Class | Typical sources | Role |
|---|---|---|
| `FACT_EVENT` | Runtime A attempts, mission complete/abandon, progress deltas | Primary educational observation |
| `DELIVERY_EVENT` | Experience projection authority_status, served intervention/recommendation ids | What the student was shown |
| `ADVICE_EVENT` | Adaptive DecisionTrace (shadow or served) | Advice lineage |
| `ORCHESTRATION_EVENT` | StrategyTrace | Intervention lineage |
| `INTERPRETATION_EVENT` | Twin snapshot refs / facet availability | Interpretation lineage (not fact) |
| `OPS_EVENT` | Gate failures, flag snapshots, soak monitor alerts | Governance / reliability |
| `RESEARCH_EVENT` | Blind-review / protocol artefacts (external corpus ids) | Qualitative programme linkage — not Runtime A |

**Forbidden class:** `AUTHORITATIVE_MASTERY` invented by Evidence Platform.

---

## 6. Evidence lifecycle

```
1. INTAKE
   Read-only collection of ObservationRefs from allowed sources.
        │
2. NORMALISE
   Map to EvidenceItem; tag claim_boundary; strip raw answer payloads;
   attach provenance fingerprints.
        │
3. QUALITY GATE
   Completeness, freshness, scope, SP8 separation, privacy checks.
        │
4. ASSEMBLE
   Build EvidenceBundle for window / population / policy / experiment.
        │
5. USE
   Outcome assembly, experiment measurement, policy evaluation,
   analytics export (governance-facing).
        │
6. RETAIN / EXPIRE
   Observational retention per ADR-MS006-002 (deferred); never
   becomes educational SoT; purge rules must not delete Runtime A.
```

### 6.1 Lifecycle states

| State | Meaning |
|---|---|
| `raw_ref` | Intake pointer only |
| `normalised` | EvidenceItem created |
| `gate_passed` | Usable for evaluation |
| `gate_failed` | Retained for ops diagnosis; excluded from promote-grade evaluation |
| `bundled` | Member of EvidenceBundle |
| `consumed` | Referenced by EvaluationRecord / OutcomeObservation |
| `expired` | Past retention; reconstruct via Runtime A when needed |

### 6.2 Triggers (observational)

| Trigger | Effect |
|---|---|
| Runtime A evidence accepted / mission terminal | May enqueue FACT_EVENT intake (when flags on) |
| Adaptive / Strategy / Twin shadow or serve telemetry | May enqueue advice / orchestration / interpretation refs |
| Experience delivery telemetry | May enqueue DELIVERY_EVENT |
| Scheduled window close | Assemble bundles for open experiments / evaluations |
| Governance request | On-demand re-assemble from frozen refs |

**Forbidden trigger effects:** writing missions, mutating Twin, re-ranking Adaptive, changing Strategy plans, flipping Experience Authority.

---

## 7. Evidence quality

### 7.1 `EvidenceQuality`

| Field | Meaning |
|---|---|
| `completeness` | `complete` \| `partial` \| `empty` |
| `freshness` | `fresh` \| `stale` \| `unknown` relative to `as_of` policy |
| `linkage_strength` | `linked` \| `ambiguous` \| `none` (for delivery→outcome) |
| `privacy_ok` | boolean; fail closed |
| `claim_boundary_ok` | boolean; fail if organisation metrics tagged as learning_depth |
| `codes[]` | Machine codes (`MISSING_RUNTIME_A`, `STALE_TWIN`, `CROSS_STUDENT_FORBIDDEN`, …) |

### 7.2 Quality gate rules (minimum)

1. Every promote-grade EvidenceItem must include at least one Runtime A `ObservationRef` **or** an explicit `OPS_EVENT` / `RESEARCH_EVENT` class with limitations — never silent substitution of Twin for facts.  
2. Twin / Adaptive / Strategy refs are **supporting**, never sole proof of educational facts.  
3. Raw answers, secrets, cookies, full DB URLs forbidden in artefacts.  
4. Cross-student aggregation only via registered population definitions — never by joining unrelated student payloads into one item.  
5. Claim-boundary mismatches fail the gate.

---

## 8. Outcome definition registry (logical)

Outcomes are registered definitions, not ad-hoc dashboard fields.

| Field | Meaning |
|---|---|
| `outcome_definition_id` | Stable id |
| `name` / `description` | Human label |
| `claim_boundary` | Required |
| `unit` / `value_type` | e.g. rate, count, categorical |
| `primary_for` | Which experiment / policy classes may use as primary |
| `minimum_evidence` | Quality thresholds |
| `aggregation` | student / night / cohort rules |
| `forbidden_interpretations[]` | Explicit “must not mean” list |

### 8.1 Example definitions (illustrative, not production metrics)

| Id | Boundary | Intent |
|---|---|---|
| `out.org.session_completed_same_night` | organisation | Director loop completion |
| `out.org.recovery_resume_success` | organisation | Recoverability after abandon |
| `out.org.single_path_start` | organisation | Start-path consistency proxy (ops) |
| `out.signal.practice_outcome_logged` | learning_signal | Honesty ritual executed |
| `out.depth.within_topic_attempt_gain` | learning_depth | Only with pre-registered construct + limitations |
| `out.transfer.exam_mark` | transfer | Deferred — registry may exist as `not_in_programme` |

---

## 9. Provenance rules

| Rule | Binding |
|---|---|
| Refs not payloads | Prefer ids / fingerprints |
| Determinism | Same refs + normaliser version → same `evidence_id` |
| Unavailable honesty | Missing upstream → `unavailable` + reason; never invent |
| Runtime A wins | Fact conflicts resolve by re-reading Runtime A, not Evidence store |
| No demo theatre | Demo / seed markers fail quality gate under evaluation promote |

---

## 10. Privacy & retention (design)

| Rule | Binding |
|---|---|
| Student scope | Artefacts never cross `student_id` without aggregation definition |
| Minimal telemetry | Ops events exclude secrets |
| Retention | ADR-MS006-002 Observational Retention (draft at E0) — observational store ≠ educational SoT |
| Right-sizing | Prefer recompute from Runtime A over long retention of derived depth claims |

---

## 11. Non-goals

- Replacing Journey / History as student-facing continuity  
- Persisting educational SoT tables  
- Estimating mastery when Runtime A progress is empty  
- Using blind-review qualitative corpus as Runtime A substitute (may link as `RESEARCH_EVENT` only)

---

## 12. Acceptance hooks

Architecture PASS requires this model to keep:

- Measurement separate from educational authority  
- Claim boundaries enforceable  
- Lifecycle free of upstream writes
