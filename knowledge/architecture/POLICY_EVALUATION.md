# MS-006 — Policy Evaluation

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Companions:** `EVIDENCE_MODEL.md`, `EXPERIMENT_FRAMEWORK.md`, `GOVERNANCE_MODEL.md`, `EVIDENCE_TRACEABILITY.md`  
**Principles:** DP-005 Explainability, DP-009 Evidence Before Opinion; EP-004 SP1–SP8

---

## 1. Purpose

Define how educational **policies** are versioned, evaluated against observational evidence, and explained without hidden reasoning — while remaining **non-authoritative** for student-facing educational decisions.

---

## 2. What a policy is

A **policy** is a declared, versioned rule set that shapes educational behaviour in an upstream layer (Adaptive ranking rules, Strategy composition rules, Experience routing precedence, flag defaults, explainability gate thresholds, etc.).

| Is | Is not |
|---|---|
| Versioned behavioural contract with owner layer | Runtime A educational fact |
| Subject to evaluation & governance | Auto-applied rewrite of missions / Twin |
| Explainable when evaluated | Opaque “model said so” |

### 2.1 `EducationalPolicy`

| Field | Meaning |
|---|---|
| `policy_id` | Stable id |
| `owner_layer` | `adaptive` \| `strategy` \| `experience_routing` \| `twin_projection` \| `cross_cutting` \| `ops_gate` |
| `title` / `intent` | Educational purpose |
| `claim_boundary_intent` | What success would mean (organisation / signal / depth / …) |
| `principles[]` | Registered educational principle ids |
| `sp_mapping[]` | EP-004 strategic principles affected |
| `upstream_controls` | Flags / knobs / config keys that instantiate the policy |
| `versions[]` | `PolicyVersion` |
| `status` | `proposed` \| `active` \| `deprecated` \| `rolled_back` |

### 2.2 `PolicyVersion`

| Field | Meaning |
|---|---|
| `policy_version` | Semver or monotonic id |
| `spec_ref` | Document / ADR / config fingerprint |
| `changelog` | Human delta vs prior |
| `introduced_at` | Observational |
| `evaluation_eligibility` | When this version may be evaluated |
| `rollback_to` | Prior version id |

**Law:** Evidence Platform **records and evaluates** policy versions; it does not own the upstream control plane that applies them (except future observational config mirrors).

---

## 3. Evaluation workflow

```
1. DECLARE
   PolicyVersion registered; evaluation questions & outcomes pre-declared.
        │
2. SCOPE
   Population, window, eligible flag matrix, exclusions.
        │
3. COLLECT
   EvidenceBundle(s) via Evidence Model intake (read-only).
        │
4. MEASURE
   OutcomeObservation[] for registered definitions.
        │
5. ANALYSE
   Statistical summary per pre-registered plan (or descriptive soak summary).
        │
6. EXPLAIN
   PolicyEvaluationExplanationBundle (five mandatory answers).
        │
7. GATE
   Explainability + claim-boundary + quality gates.
        │
8. EMIT
   EvaluationRecord → governance sink (recommendation only).
        │
9. DECIDE (governance)
   keep / revise / roll back / expand soak — human-owned.
```

**Forbidden after gate PASS:** automatic Authority promotion; automatic Twin/Adaptive/Strategy mutation.

---

## 4. `EvaluationRecord`

| Field | Meaning |
|---|---|
| `evaluation_id` | Deterministic from policy version + freeze + plan |
| `policy_id` / `policy_version` | Under test |
| `baseline_policy_version` | Comparator when applicable |
| `experiment_id?` | When evaluation is experiment-backed |
| `evidence_bundle_ids[]` | |
| `outcome_observations[]` | Typed results |
| `statistical_summary` | See §5 |
| `explanation` | §6 bundle |
| `gate_result` | `passed` \| `failed` \| `ineligible` |
| `recommendation` | `keep` \| `revise` \| `roll_back` \| `expand_soak` \| `inconclusive` |
| `limitations[]` | Required |
| `confidence` | Band + rationale |
| `created_at` | Observational |
| `engine_version` | Evaluator version |

---

## 5. Statistical basis (required fields)

Architecture does not mandate a single estimator. It mandates **honest disclosure**:

| Field | Meaning |
|---|---|
| `design` | `descriptive_soak` \| `pre_registered_compare` \| `interrupted_time` \| `other` (+ note) |
| `sample` | N subjects / nights / events; eligibility |
| `estimator` | Named method or `descriptive_only` |
| `effect` | Point summary per primary outcome |
| `uncertainty` | Interval / credible band / `not_estimable` |
| `multiplicity` | How multiple outcomes handled |
| `pre_registration_id` | Protocol / plan fingerprint |
| `sensitivity` | Optional; required before promote when thin |
| `failure_modes` | What would flip the conclusion |

**Rule:** `descriptive_only` may support `expand_soak` / `inconclusive`; it must not alone justify `keep` of a learner-visible Authority flip without governance exception logged.

---

## 6. Explainability (binding)

Every policy evaluation must answer:

| # | Question | Contract field |
|---|---|---|
| 1 | What **evidence** was considered? | `evidence_considered` |
| 2 | What is the **statistical basis**? | `statistical_basis` |
| 3 | What is the **educational rationale**? | `educational_rationale` |
| 4 | Which **policy version** was evaluated? | `policy_version` |
| 5 | What is the **confidence level**? | `confidence` |

No hidden reasoning. Missing any answer → `gate_result = failed` / `ineligible`.

### 6.1 `PolicyEvaluationExplanationBundle`

```
PolicyEvaluationExplanationBundle {
  evidence_considered: {
    summary,                    # plain language, operator-safe
    evidence_bundle_ids[],
    runtime_a_ref_count,
    supporting_upstream_refs[], # twin / adaptive / strategy / experience
    quality_codes[],
    claim_boundaries_present[]
  },

  statistical_basis: {
    design,
    sample_summary,
    estimator,
    effect_summary,
    uncertainty_summary,
    pre_registration_id?,
    not_proven[]                # explicit non-claims
  },

  educational_rationale: {
    intent_summary,
    principles[]: [{ principle_id, version, how_relevant }],
    sp_mapping[],               # EP-004 SP ids
    student_impact_hypothesis,  # careful language; not served to students here
    organisation_vs_learning_note  # SP8 separation statement
  },

  policy_version: {
    policy_id,
    policy_version,
    owner_layer,
    upstream_flag_snapshot,
    baseline_policy_version?,
    spec_ref
  },

  confidence: {
    band,                       # high | medium | low | insufficient
    rationale,
    limitations[],
    what_this_does_not_prove[]  # mandatory non-empty for promote-grade
  }
}
```

### 6.2 Gate rules

| Condition | Gate |
|---|---|
| All five sections complete | Eligible for `passed` if quality also OK |
| Organisation lift narrated as learning depth | **Fail** (`CLAIM_BOUNDARY_LEAKAGE`) |
| No Runtime A evidence for educational-outcome claims | **Fail** (`MISSING_RUNTIME_A`) |
| Uncertainty missing on promote recommendation | **Fail** (`STATISTICS_INCOMPLETE`) |
| `what_this_does_not_prove` empty on promote | **Fail** (`OVERCLAIM`) |
| Demo / seed markers in evidence | **Fail** (`DEMO_THEATRE`) |

---

## 7. Evaluation kinds

| Kind | Typical use | Promote bar |
|---|---|---|
| `shadow_descriptive` | Pipeline health, stability | Expand soak / ops only |
| `shadow_compare` | Arm metrics without UX difference | Inconclusive / expand; rarely keep |
| `flag_mediated_compare` | Limited serve difference | Governance required; soak + guardrails |
| `post_hoc_incident` | After trust / integrity incident | Roll back biased; not for celebration metrics |
| `research_linkage` | Tie EP-004 qualitative themes to ops metrics | Never upgrades qualitative → Runtime A fact |

---

## 8. Relationship to experiments

| When | Artefact |
|---|---|
| Evaluation backed by experiment | `EvaluationRecord.experiment_id` set; analysis may be reused |
| Evaluation without experiment | Allowed for descriptive soaks / incident reviews |
| Experiment without evaluation | Incomplete for governance promote |

Governance promote of learner-visible policy requires EvaluationRecord with gate `passed` (see `GOVERNANCE_MODEL.md`).

---

## 9. Outputs & sinks

| Output | Consumer | Must not |
|---|---|---|
| EvaluationRecord | Governance / ops | Drive Home topic |
| ExplanationBundle | Reviewers | Appear as Coach “evidence” theatre without inspectability redesign (out of scope) |
| Telemetry `EVIDENCE_EVAL_*` | Ops monitors | Contain secrets / raw answers |
| Analytics export | Outcome analytics | Student-facing mastery claims |

---

## 10. Non-goals

- Replacing Adaptive / Strategy explainability bundles for student UX  
- Declaring pedagogical truth from p-values  
- Auto-merging winning PolicyVersion into production Authority  
- Using evaluation confidence as Twin mastery  

---

## 11. Acceptance hooks

Architecture PASS requires:

- Five mandatory explanation answers  
- Measurement ≠ educational authority  
- Gate blocks overclaim / claim-boundary leakage
