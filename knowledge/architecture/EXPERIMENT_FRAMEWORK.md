# MS-006 — Experiment Framework

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design (protocol model); **E2 assignment subset — Implemented** (see `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`)  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Companions:** `EVIDENCE_MODEL.md`, `POLICY_EVALUATION.md`, `OUTCOME_ANALYTICS.md`, `GOVERNANCE_MODEL.md`  
**Related:** Upstream shadow strategies (MS-003 A4/A6, MS-004 T6, MS-005 S3/S6)

---

## 1. Purpose

Define how Kwalitec runs **controlled educational experiments** that compare policy / intervention variants while preserving:

- Runtime A as sole educational fact authority  
- No reverse dependency writes  
- Honest claim boundaries (organisation vs learning depth)  
- Reversible, flag-mediated assignment  
- Explainable analysis artefacts for governance  

**E2 implementation (Directive 004):** deterministic assignment of validated `EvidenceRecord` → immutable `ExperimentObservation` via `ExperimentFramework` / `ExperimentAssigner` / `ExperimentDefinitionRegistry`. No statistical analysis, policy evaluation, analytics, persistence, or educational behaviour change.

---

## 2. What an experiment is (and is not)

| Is | Is not |
|---|---|
| A pre-registered protocol comparing arms under declared outcomes | A silent A/B that mutates missions for “data” |
| Measurement + analysis + governance recommendation | Auto-promotion of Adaptive / Strategy Authority |
| Preferentially shadow-first observation | Student-facing coaching experiment theatre |
| Flag-mediated variant exposure | Parallel educational write path owned by Evidence Platform |

---

## 3. Experiment model

### 3.1 `ExperimentProtocol`

| Field | Meaning |
|---|---|
| `experiment_id` | Stable id |
| `title` / `hypothesis` | Human statement (educational, not growth-hack) |
| `policy_under_test` | `policy_id` + baseline / treatment versions |
| `arms[]` | See §3.2 |
| `eligibility` | Population definition (exam, stage, flag matrix, exclusions) |
| `assignment` | Mechanism (§4) |
| `primary_outcomes[]` | Registered `outcome_definition_id`s + claim boundaries |
| `secondary_outcomes[]` | Optional; cannot override primary claim boundary honesty |
| `guardrail_outcomes[]` | Safety / trust / latency metrics that can force stop |
| `window` | Start / end / early-stop rules |
| `pre_registration` | Frozen protocol fingerprint before first assignment |
| `statistical_plan` | Estimator, multiplicity, minimum N, uncertainty policy |
| `educational_rationale` | Principles + EP-004 SP mapping |
| `rollback_map` | Exact flags / knobs to revert each arm |
| `status` | `draft` \| `registered` \| `running` \| `paused` \| `analysed` \| `closed` \| `aborted` |

### 3.2 `ExperimentArm`

| Field | Meaning |
|---|---|
| `arm_id` | Stable within experiment |
| `label` | e.g. `control`, `treatment_a` |
| `exposure` | `shadow_only` \| `flag_mediated_serve` |
| `upstream_flag_snapshot` | Exact flags / policy knobs that define the arm |
| `forbidden_writes` | Explicit empty set for Evidence Platform; documented upstream write owners if any (normally none) |
| `notes` | Human |

**Law:** `flag_mediated_serve` arms may only differ by **already-owned** upstream behaviour behind flags (e.g. Strategy Shadow vs Authority). Evidence Platform does not invent new educational behaviours inside an arm.

---

## 4. Assignment

### 4.1 Principles

1. Assignment is **deterministic** given `(experiment_id, subject_key, salt, arm_weights)` when using hash assignment.  
2. Subject key is typically `student_id` (never email in artefacts).  
3. Assignment records are observational (`AssignmentRecord`) — not educational facts.  
4. Reassignment mid-window requires protocol amendment + governance; default is sticky assignment.  
5. Shadow-only arms assign for **measurement identity** even when UX is unchanged.

### 4.2 `AssignmentRecord`

| Field | Meaning |
|---|---|
| `assignment_id` | Deterministic id |
| `experiment_id` / `arm_id` | |
| `subject_key` | Scoped |
| `assigned_at` | Observational |
| `mechanism` | `hash` \| `manual_allowlist` \| `ops_override` |
| `flag_snapshot` | What the subject should experience if serve-arm |
| `eligibility_result` | pass / fail + reasons |

### 4.3 Forbidden assignment effects

| Forbidden | Why |
|---|---|
| Creating missions / attempts to “balance arms” | Corrupts Runtime A |
| Writing Twin facets “experiment_arm=…” as truth | Interpretation pollution |
| Changing Adaptive primary ranking inside Evidence Platform | Recommendation seizure |
| Serving unexplained interventions to fill an arm | Trust / explainability breach |

---

## 5. Measurement

### 5.1 Pipeline

```
AssignmentRecord
    → Exposure verification (did flags match arm?)
    → Evidence intake (Runtime A + delivery / upstream traces)
    → EvidenceBundle for window
    → OutcomeObservation[] per registered definitions
    → Arm-level aggregates (analytics)
    → ExperimentAnalysis artefact
```

### 5.2 Exposure verification

| Check | Result |
|---|---|
| Flag snapshot matches arm | `exposed` |
| Flags drifted / Authority flipped outside protocol | `exposure_violation` → exclude or abort per plan |
| Shadow arm but Authority accidentally ON | Guardrail abort candidate |

### 5.3 Windows

| Window type | Use |
|---|---|
| `same_night` | Organisation loop outcomes |
| `next_session` | Recovery / resume |
| `fixed_calendar` | Cohort soaks |
| `event_bounded` | Post-delivery → outcome linkage |

Linkage strength (`linked` / `ambiguous` / `none`) follows Evidence Model rules — **never invent causation**.

---

## 6. Analysis artefact

### 6.1 `ExperimentAnalysis`

| Field | Meaning |
|---|---|
| `analysis_id` | Deterministic from protocol + data freeze |
| `experiment_id` | |
| `data_freeze_ref` | EvidenceBundle set fingerprint |
| `per_arm_metrics[]` | Outcome aggregates + uncertainty |
| `comparisons[]` | Treatment vs control per primary outcome |
| `guardrail_status` | pass / fail / inconclusive |
| `claim_boundary_audit` | Detected leakage codes |
| `limitations[]` | Sample, bias, exposure, seasonality |
| `recommendation` | `keep_control` \| `prefer_treatment` \| `inconclusive` \| `abort` \| `expand_soak` |
| `explanation` | Mandatory five-answer bundle (same family as policy evaluation) |

### 6.2 Statistical honesty (minimum)

| Rule | Binding |
|---|---|
| Pre-register primary outcomes | No post-hoc primary swap without amendment |
| Report uncertainty | Point estimates alone insufficient for promote |
| Multiplicity | Declared when multiple primaries |
| Thin N | Force `inconclusive` rather than theatrical significance |
| SP8 | Organisation lift must not be narrated as learning-depth lift |

Exact estimators are implementation concerns; architecture requires the **fields and honesty rules**, not a specific library.

---

## 7. Experiment classes (allowed)

| Class | Typical question | Default exposure |
|---|---|---|
| `shadow_parity` | Does new pipeline produce stable observational metrics vs baseline? | `shadow_only` |
| `policy_flag` | Does flag-mediated policy B change organisation outcomes vs A? | Prefer shadow, then limited serve |
| `explainability_ops` | Does gate failure rate improve under policy B? | `shadow_only` or ops |
| `orchestration_structure` | Does Strategy intervention structure change completion (organisation)? | Only after Strategy shadow soak |
| `learning_depth` | Pre-registered depth construct | Rare; high governance bar; never default |

**Disallowed class:** `exam_mark_promise` experiments as product claims without separate evidence programme.

---

## 8. Relationship to upstream shadows

| Layer | Shadow owner | Experiment use |
|---|---|---|
| Adaptive | MS-003 | Arms may set Adaptive Shadow ON; Evidence Platform measures outcomes |
| Twin | MS-004 | Arms may observe Twin availability; must not write Twin |
| Strategy | MS-005 | Arms may set Strategy Shadow / (later) Authority per governance |
| Evidence Platform | MS-006 | Owns cross-layer measurement shadow; does not replace upstream shadows |

**Composition rule:** Do not flip Adaptive Authority + Strategy Authority + experiment serve-arm in one change set (`RISK_ANALYSIS_MS006.md`).

---

## 9. Feature flags (experiment-related, design)

| Flag | Role |
|---|---|
| `ENABLE_EVIDENCE_PLATFORM` | Master |
| `ENABLE_EVIDENCE_SHADOW` | Measurement without learner effects |
| `ENABLE_EXPERIMENT_ASSIGNMENT` | Emit / honour AssignmentRecords |
| Upstream engine flags | Define arm exposure (owned upstream) |

Disabling Evidence Platform flags stops measurement participation; upstream educational serving continues unchanged.

---

## 10. Abort & rollback

| Trigger | Action |
|---|---|
| Guardrail fail (trust / latency / exposure violation) | Pause assignment; roll flags per `rollback_map` |
| Claim-boundary leakage in analysis narrative | Analysis `gate_ineligible`; no promote |
| Runtime A integrity incident | Abort experiment; Evidence Platform does not “repair” by writing facts |
| Governance decide roll back | Execute rollback_map; close experiment |

---

## 11. Non-goals

- Growth / marketing A/B as educational experiments without educational rationale  
- Personalisation that bypasses Adaptive / Strategy ownership  
- Auto-merging winning arms into default Authority  
- Student-visible “you are in an experiment” theatre unless product explicitly designs consent UX later (out of scope here)

---

## 12. Acceptance hooks

Architecture PASS requires experiments to remain:

- Observational at the Evidence Platform boundary  
- Flag-mediated for any learner-visible difference  
- Claim-boundary honest  
- Non-authoritative for educational writes
