# Programme IV — Controlled Educational Effectiveness Trial

**Milestone:** P4-MS001 — Controlled Educational Effectiveness Trial  
**Directive:** Engineering Directive 001 (Controlled Educational Effectiveness Trial)  
**Status:** Implemented (operational trial framework)  
**Package:** `app/infrastructure/adapters/educational_trial/`  
**Service:** `EducationalTrialService`  
**Feature flag:** `KWALITEC_EDUCATIONAL_TRIALS` → `ENABLE_EDUCATIONAL_TRIALS` (**default OFF**)  
**Contract version:** `p4.ms001.1` (`EDUCATIONAL_TRIAL_VERSION`)  
**Approved advisory field (only):** `consistency_summary`  
**Companions:** `POLICY_WEIGHT_APPLICATION.md`, `RECOMMENDATION_POLICY_ARCHITECTURE.md`, `ADVISORY_OUTCOME_MEASUREMENT.md`

---

## 0. Purpose

Introduce an operational trial framework that compares **baseline recommendations** with **policy-weighted recommendations** under controlled, deterministic rollout.

> Every future behavioural expansion must be justified by measurable educational benefit.

This milestone measures educational-effectiveness *signals* at the operational layer (acceptance, completion, activation). It does **not** expand behavioural capability, advisory fields, or educational authority.

| In scope | Out of scope |
|---|---|
| Immutable `EducationalTrial` DTO | Additional advisory fields |
| Deterministic cohort assignment | Larger weighting bounds |
| Operational trial metrics | Adaptive Engine changes |
| Immutable trial summaries | Recovery optimisation |
| `ENABLE_EDUCATIONAL_TRIALS` | Autonomous policy updates |
| Treatment-cohort Runtime A gating | AI coaching / mastery inference |

**Stop condition:** Stop after Controlled Educational Effectiveness Trial. Await architecture review before expanding advisory influence beyond `consistency_summary`.

---

## 1. Trial lifecycle

```
Author / ops define EducationalTrial (immutable; versioned)
        │
        ▼
ENABLE_EDUCATIONAL_TRIALS (default OFF)
        │
        ▼
EducationalTrialService
        │
        ├── validate trial (advisory_field locked to consistency_summary)
        ├── assign_cohort(student) → baseline | treatment | unassigned
        │     └── treatment alone authorises policy weighting under trial gate
        │
        ├── Runtime A RecommendationService
        │     ├── treatment → may apply P3-MS004 policy weighting
        │     └── baseline  → retain baseline recommendations (no weight)
        │
        ├── record_metric / record_policy_activation
        │     (acceptance, mission / session / reflection completion, activation)
        │
        └── generate_summary → TrialSummary (immutable; educational review)
```

Lifecycle rules:

1. Trial configuration is immutable once constructed (`EducationalTrial`).
2. Only `status=active` trials assign baseline / treatment cohorts.
3. Draft / paused / completed / cancelled trials leave students `unassigned` (no Runtime A change via the trial gate).
4. Disabling `KWALITEC_EDUCATIONAL_TRIALS` removes DI and restores prior behaviour immediately.
5. Runtime A remains sole educational authority for what the student should do next.

---

## 2. Cohort assignment

### Mechanism

| Property | Behaviour |
|---|---|
| Stability | Same `(trial_id, salt, student_id)` → same bucket forever |
| Rollout | `bucket = SHA256(salt:trial_id:student_id)[:8] % 100` |
| Treatment | `bucket < rollout_percentage` (0 → none; 100 → all non-empty ids) |
| Baseline | Active trial members not in treatment |
| Unassigned | Inactive trial, empty student id, or flag OFF path |

Artefacts use an opaque `student_key` (`trialstu-…`) — raw personal identifiers are not stored on trial observation / summary DTOs.

### Student-visible differences

The only authorised behavioural difference is the existing P3-MS004 bounded policy weighting on `consistency_summary` for **treatment** cohorts. No UI labels, messaging, or additional advisory fields distinguish cohorts.

### Nested gates

When both `ENABLE_EDUCATIONAL_TRIALS` and `ENABLE_POLICY_WEIGHTING` are ON:

1. Trial gate: student must be treatment-authorised.
2. Policy engine gates: freshness, policy validity, and policy-weighting rollout still apply.

When the trial flag is OFF, the trial service is not constructed and does not interpose — existing policy-weighting rollout behaves as before.

---

## 3. Trial metrics

Operational metrics only. **Do not** infer mastery or examination success in this milestone.

| Metric | Meaning |
|---|---|
| `recommendation_acceptance` | Student accepted / started a recommendation |
| `mission_completion` | Daily mission completed in observation window |
| `study_session_completion` | Guided study session completed |
| `reflection_completion` | Reflection step completed |
| `policy_activation` | Policy weighting activated for an authorised path |

Rates are clamped to `[0.0, 1.0]`. Empty cohorts yield `0.0`. Aggregation is deterministic for identical observation inputs.

---

## 4. Reporting methodology

`TrialSummary` is an immutable educational-review artefact containing:

| Section | Contents |
|---|---|
| Trial config | `trial_id`, `policy_version`, advisory field, rollout %, status, dates |
| Cohort statistics | Baseline / treatment / unassigned counts |
| Activation statistics | Policy activation counts by cohort; metric counts |
| Trial metrics | Operational rates overall and by cohort |
| Observation period | `start_date` / `end_date` from the trial |
| Notes | Explicit non-claims (no mastery inference; await review) |

Summaries are reproducible: identical observation / assignment inputs and `generated_at` produce identical `summary_id` and canonical serialization.

Process-local in-memory buffers are used for this milestone — not a durable analytics warehouse.

---

## 5. Governance

| Role | Responsibility |
|---|---|
| Ops / educational review | Author trial config, set rollout %, observation window, exit review |
| `EducationalTrialService` | Validate trial; assign cohorts; collect metrics; emit summaries |
| Runtime A (`RecommendationService`) | Produce recommendations; apply weighting only when trial-authorised |
| Policy engine (P3-MS004) | Resolve / bound weight application for `consistency_summary` only |

Invariants:

1. Exactly one advisory field may participate (`consistency_summary`).
2. Trial cohorts are deterministic and reproducible.
3. Rollout is reversible by flag or by setting trial rollout to `0` / pausing the trial.
4. Runtime A remains final educational authority.
5. Feature flag is independent from all prior Programme II / III flags.

---

## 6. Feature flag & rollback

| Environment | Flag field | Default |
|---|---|---|
| `KWALITEC_EDUCATIONAL_TRIALS` | `ENABLE_EDUCATIONAL_TRIALS` | OFF |
| `KWALITEC_EDUCATIONAL_TRIAL_ID` | trial id | `educational-trial-p4-ms001` |
| `KWALITEC_EDUCATIONAL_TRIAL_POLICY_VERSION` | policy version | `p3.ms004.1` |
| `KWALITEC_EDUCATIONAL_TRIAL_ROLLOUT_PERCENTAGE` | treatment % | `0` |
| `KWALITEC_EDUCATIONAL_TRIAL_STATUS` | lifecycle | `active` (when flag ON) |
| `KWALITEC_EDUCATIONAL_TRIAL_START_DATE` | observation start | empty |
| `KWALITEC_EDUCATIONAL_TRIAL_END_DATE` | observation end | empty |
| `KWALITEC_EDUCATIONAL_TRIAL_ROLLOUT_SALT` | hash salt | fixed default |

### Immediate rollback

| Action | Effect |
|---|---|
| Unset / set `KWALITEC_EDUCATIONAL_TRIALS=0` | Trial DI not constructed; prior Runtime A behaviour restored |
| Set trial rollout to `0` | All students baseline under an active trial |
| Pause / cancel trial status | Students unassigned; trial gate denies weighting |

Dual-run ops field: `DualRunStatus.educational_trials`.

---

## 7. Exit criteria

A trial may exit (complete / cancel) only after educational review of a reproducible `TrialSummary` that includes:

1. Cohort statistics for the observation period.
2. Policy activation frequency by cohort.
3. Operational completion / acceptance rates (no mastery claims).
4. Explicit confirmation that advisory scope remained `consistency_summary`.
5. A GO / NO-GO decision on whether policy weighting remains justified.

Exit does **not** autonomously promote policy, expand fields, or alter Adaptive / Recovery / Strategy systems.

---

## 8. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `EducationalTrial` | `contracts.py` | Immutable trial config | Expanding advisory fields |
| `CohortAssignment` | `contracts.py` / `cohort.py` | Stable baseline / treatment allocation | Student-visible labelling |
| `TrialMetricObservation` | `contracts.py` | Operational observation | Mastery / exam scoring |
| `TrialMetrics` / `TrialSummary` | `contracts.py` | Review artefacts | Persistence (this milestone) |
| `EducationalTrialService` | `service.py` | Configure → assign → measure → report | Mutating Adaptive / Recovery |

---

## 9. Acceptance mapping

| Criterion | How satisfied |
|---|---|
| Trial cohorts are deterministic | Stable hash assignment; covered by cohort stability tests |
| Rollout remains reversible | Flag OFF / rollout 0 / inactive status |
| Trial reporting is reproducible | Canonical `TrialSummary` serialization |
| Runtime A changes only for authorised cohorts | Treatment gate in `RecommendationService` |
| Educational authority unchanged | Runtime A still produces recommendations |
| All tests pass | `tests/infrastructure/adapters/educational_trial/` + flag tests |
