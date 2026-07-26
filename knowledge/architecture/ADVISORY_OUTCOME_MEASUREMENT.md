# Programme III — Advisory Outcome Measurement

**Milestone:** P3-MS002 — Advisory Outcome Measurement  
**Directive:** Engineering Directive 001 (Advisory Outcome Measurement)  
**Status:** Implemented (operational measurement only)  
**Package:** `app/infrastructure/adapters/advisory_outcome/`  
**Service:** `AdvisoryOutcomeMeasurementService`  
**Feature flag:** `KWALITEC_ADVISORY_OUTCOME_MEASUREMENT` → `ENABLE_ADVISORY_OUTCOME_MEASUREMENT` (**default OFF**)  
**Contract version:** `p3.ms002.1` (`OUTCOME_MEASUREMENT_VERSION`)  
**Companions:** `CONTROLLED_ADVISORY_ACTIVATION.md`, `ADVISORY_EVALUATION_ARCHITECTURE.md`, `DECISION_SIMULATION_ARCHITECTURE.md`

---

## 0. Purpose

Measure the **behavioural impact** of Controlled Advisory Activation during rollout using operational observations only.

> Every behavioural change must justify its continued existence with evidence.

| In scope | Out of scope |
|---|---|
| Immutable `AdvisoryOutcome` | Additional advisory fields |
| `AdvisoryOutcomeMeasurementService` | Recommendation ranking changes |
| Activation statistics aggregation | Recovery activation |
| Operational rollout metrics | Adaptive / Strategy changes |
| Action ↔ activation correlation | Automatic optimisation |
| `ENABLE_ADVISORY_OUTCOME_MEASUREMENT` | AI coaching / educational scoring |
| Explainable provenance on every outcome | Runtime A behavioural changes |

**Stop condition:** Stop after Advisory Outcome Measurement. Await architecture review before expanding advisory influence.

---

## 1. Outcome lifecycle

```
Controlled Advisory Activation decision / explainability
        │
        ▼ (optional observation of student action)
AdvisoryOutcomeMeasurementService.record_outcome
        │  or record_from_activation(...)
        │
        ├── AdvisoryOutcome (immutable; no personal identifiers)
        │
        ├── aggregate_activation_statistics → ActivationStatistics
        │
        ├── correlate_actions → ActionCorrelation
        │
        ├── aggregate_rollout_metrics → RolloutMetrics
        │
        └── generate_summary → OutcomeMeasurementSummary
```

Lifecycle rules:

1. Collect observations only — never rewrite production recommendations.
2. Preserve explainability on every recorded outcome.
3. Aggregate rates and counts over an in-memory cohort (process-local for this milestone).
4. Report behavioural co-occurrence — do **not** infer learning quality or mastery.
5. Disabling the flag removes construction / service use immediately (same process restart / DI path as other V2 flags).

---

## 2. Measurement methodology

### `AdvisoryOutcome` (immutable)

| Field | Meaning |
|---|---|
| `outcome_id` | Deterministic operational id (`advout-…`) |
| `policy_version` | Controlled advisory policy version observed |
| `advisory_field` | Advisory field under measurement |
| `activation_status` | `activated` / `rejected` / `failed` / `rolled_back` |
| `recommendation_id` | Recommendation artefact id (not a person id) |
| `student_action_observed` | Operational action taxonomy (see below) |
| `observation_window` | Window label (default `session`) |
| `generated_at` | ISO timestamp when recorded |
| `rollout_cohort` | `in_rollout` / `excluded` / `unknown` |
| `activation_decision` | Allow / deny / failure / rollback reason |
| `provenance` | Frozen explainability / source metadata |

**Forbidden on the DTO surface:** personal identifiers (`student_id`, `user_id`, `email`), educational scores, mastery estimates, ranking mutations.

### Observed actions (operational)

| Action | Meaning |
|---|---|
| `not_observed` | No behavioural signal collected |
| `viewed` | Recommendation surfaced / viewed |
| `accepted` | Student accepted / started the recommendation |
| `interacted` | Further interaction beyond accept |
| `ignored` | No engagement observed in window |
| `dismissed` | Explicit dismiss |

### Rollout metrics

| Metric | Definition |
|---|---|
| `activation_rate` | `activated / outcome_count` |
| `acceptance_rate` | `accepted / activated` (0 when no activations) |
| `recommendation_interaction_rate` | `(viewed ∪ accepted ∪ interacted) / activated` |
| `rollback_count` | Outcomes with status `rolled_back` |
| `activation_failures` | Outcomes with status `failed` |
| `rejection_count` | Outcomes with status `rejected` |

Rates are clamped to `[0.0, 1.0]`. Empty cohorts yield `0.0`.

These metrics measure **rollout behaviour**, not learning quality.

### Correlation

`ActionCorrelation` counts observed actions partitioned by activation status. It supports ops review of whether activated recommendations are accepted or ignored. It does **not** claim causal educational benefit.

---

## 3. Explainability

Every recorded outcome must preserve:

| Field | Source |
|---|---|
| Policy version | Controlled advisory policy / decision |
| Advisory field | Approved field under activation |
| Rollout cohort | Deterministic rollout membership label |
| Activation decision | Allow / deny / failure / rollback reason |
| Provenance | Advisory id, policy id, evidence refs, service metadata |

`explainability_fields_present(outcome)` encodes this invariant for tests and ops checks.

Authority remains:

- `runtime_a` for educational decisions
- `controlled_advisory` for activation governance
- `advisory_outcome_measurement` for observation artefacts

---

## 4. Feature flag & rollback

| Environment | Flag field | Default |
|---|---|---|
| `KWALITEC_ADVISORY_OUTCOME_MEASUREMENT` | `ENABLE_ADVISORY_OUTCOME_MEASUREMENT` | OFF |

Independently controllable from:

- `ENABLE_CONTROLLED_ADVISORY`
- `ENABLE_ADVISORY_EVALUATION`
- `ENABLE_DECISION_SIMULATION`
- all prior Programme II / Adaptive / Twin / Strategy / Evidence flags

### Immediate rollback

| Action | Effect |
|---|---|
| Unset / set `KWALITEC_ADVISORY_OUTCOME_MEASUREMENT=0` | Measurement DI not constructed; Runtime A path untouched |
| Keep Controlled Advisory OFF | No advisory utilisation; measurement may still be enabled for dry-run ingestion of historical observations if callers supply them |

Measurement does not gate or delay Controlled Advisory rollback. Disabling `ENABLE_CONTROLLED_ADVISORY` remains the immediate utilisation rollback.

Dual-run ops field: `DualRunStatus.advisory_outcome_measurement`.

---

## 5. Operational safeguards

1. Flag defaults **OFF**.
2. Service reports observations only — never interprets educational success.
3. No personal identifiers on outcome artefacts.
4. No recommendation ranking / priority / title / category changes.
5. No additional advisory fields, Recovery activation, Adaptive, Strategy, or AI coaching.
6. Failures in recording return `INVALID_STATE` / `UNAVAILABLE` envelopes; they must not break student paths (measurement is side-channel / DI-isolated).
7. Process-local in-memory buffer for this milestone — not a durable analytics warehouse.

---

## 6. Future evaluation process

After architecture review, outcome measurement may inform (but does not itself perform):

1. Whether Controlled Advisory Activation remains justified under observed acceptance / interaction rates.
2. Whether rollout percentage expansion is warranted.
3. Whether additional advisory fields deserve a separate governed activation milestone.
4. Whether educational evaluation (distinct from operational rates) should be designed.

Binding constraint for this milestone: **measurement ≠ optimisation**. Automatic policy tuning, ranking rewrites, and coaching remain forbidden until a later reviewed programme step.

---

## 7. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `AdvisoryOutcome` | `advisory_outcome/contracts.py` | Immutable observation DTO | Personal ids / scores |
| `ActivationStatistics` | `contracts.py` | Activation count aggregates | Educational interpretation |
| `ActionCorrelation` | `contracts.py` | Action × status co-occurrence | Causal claims |
| `RolloutMetrics` | `contracts.py` | Operational rates & counters | Learning quality |
| `OutcomeMeasurementSummary` | `contracts.py` | Ops review envelope | Persistence (this milestone) |
| `AdvisoryOutcomeMeasurementService` | `advisory_outcome/service.py` | Collect → aggregate → correlate | Mutating Runtime A |

---

## 8. Tests

| Suite | Coverage |
|---|---|
| `tests/.../advisory_outcome/test_contracts.py` | Outcome immutability, explainability, metrics clamps |
| `tests/.../advisory_outcome/test_service.py` | Aggregation, correlation, rollout metrics, flag isolation, provenance, Runtime A isolation |
| `tests/application/config/test_v2_flags.py` | Flag default OFF + dual-run field |

---

## 9. Explicit non-goals (binding)

- Additional advisory fields
- Recommendation ranking changes
- Recovery activation
- Adaptive Engine / Strategy Engine / Twin behavioural changes
- Automatic optimisation / AI coaching
- Educational scoring or mastery inference
- Runtime A behavioural changes
