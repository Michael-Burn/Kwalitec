# Programme III — Controlled Advisory Activation

**Milestone:** P3-MS001 — Controlled Advisory Activation  
**Directive:** Engineering Directive 001 (Controlled Advisory Activation)  
**Status:** Implemented (single-field utilisation under governance)  
**Package:** `app/infrastructure/adapters/controlled_advisory/`  
**Runtime A hook:** `RecommendationService.generate_recommendations(..., controlled_advisory=)`  
**Feature flag:** `KWALITEC_CONTROLLED_ADVISORY` → `ENABLE_CONTROLLED_ADVISORY` (**default OFF**)  
**Rollout:** `KWALITEC_CONTROLLED_ADVISORY_ROLLOUT_PERCENTAGE` (0–100, **default 0**)  
**Contract version:** `p3.ms001.1` (`CONTROLLED_ADVISORY_VERSION`)  
**Approved field (only):** `consistency_summary`  
**Companions:** `EVIDENCE_ADVISORY_ARCHITECTURE.md`, `DECISION_SIMULATION_ARCHITECTURE.md`, `ADVISORY_EVALUATION_ARCHITECTURE.md`, `ADVISORY_OUTCOME_MEASUREMENT.md`

---

## 0. Purpose

Permit Runtime A to **consume** a single, explicitly approved Evidence Advisory field under strict governance while preserving explainability, reversibility, and measurable comparison.

> Move from advisory availability to advisory utilisation in the safest possible manner.

| In scope | Out of scope |
|---|---|
| Immutable `AdvisoryPolicy` | Recovery activation |
| Runtime Policy Evaluator (allow/deny only) | Adaptive Engine changes |
| Single-field Runtime A consumption | Strategy Engine modifications |
| Explainability on every activation / rejection | Multiple advisory fields |
| Simulation comparison retained | AI-generated coaching |
| `ENABLE_CONTROLLED_ADVISORY` + rollout % | Autonomous optimisation |

**Stop condition:** Stop after Controlled Advisory Activation. Await architecture review before expanding advisory influence or enabling additional advisory fields.

---

## 1. Activation lifecycle

```
EvidenceAdvisory (via EvidenceAdvisoryPort / P2-MS009 injection)
        │
        ▼
AdvisoryPolicy (immutable; exactly one enabled field)
        │
        ▼
ControlledAdvisoryPolicyEvaluator
        │
        ├── validate policy
        ├── validate feature flag
        ├── validate rollout percentage (deterministic student bucket)
        ├── validate advisory freshness / availability / field presence
        └── AdvisoryActivationDecision (allow | deny + reason)
                │
                ▼
ControlledAdvisoryActivation.apply_to_recommendations
        │
        ├── ALLOW → annotate recommendation reason with consistency_summary
        │            + attach advisory_activation explainability
        └── DENY  → leave ranking unchanged
                     + attach rejection_reason explainability
                │
                ▼
DecisionSimulationService (optional, P2-MS011)
        │
        └── compare policy-driven production vs simulation artefacts
```

Influence is intentionally minimal:

1. **Never** changes priority, title, category, or sort order.
2. **Only** annotates `reason` with the factual `consistency_summary` observation.
3. **Ignores** all other advisory fields (`engagement_summary`, `observed_patterns`, `factual_constraints`, …).

---

## 2. Policy model

### `AdvisoryPolicy` (immutable)

| Field | Meaning |
|---|---|
| `policy_id` | Stable policy identity (`controlled-advisory-p3-ms001`) |
| `enabled_advisory_fields` | Exactly one field; additional fields forbidden |
| `activation_conditions` | Freshness / presence / rollout salt gates |
| `rollout_percentage` | 0–100 staged deployment bucket |
| `policy_version` | Policy revision (`p3.ms001.1`) |
| `effective_from` | ISO timestamp; future policies deny until effective |

### Approved field

| Field | Why chosen for P3-MS001 |
|---|---|
| `consistency_summary` | Smallest factual scalar surface (`active_streak`); lowest ranking risk |

`validate_advisory_policy` rejects:

- empty / missing identity or version
- more than one enabled field (`multiple_advisory_fields_forbidden`)
- any field outside the approved allow-list (`advisory_field_not_approved`)

### Environment resolution

| Environment | Role | Default |
|---|---|---|
| `KWALITEC_CONTROLLED_ADVISORY` | Master enable | OFF |
| `KWALITEC_CONTROLLED_ADVISORY_ROLLOUT_PERCENTAGE` | Staged % | `0` |
| `KWALITEC_CONTROLLED_ADVISORY_MAX_AGE_HOURS` | Freshness window | `168` |
| `KWALITEC_CONTROLLED_ADVISORY_EFFECTIVE_FROM` | Policy effective time | epoch (always effective) |

---

## 3. Runtime Policy Evaluator

`ControlledAdvisoryPolicyEvaluator` returns an explicit `AdvisoryActivationDecision`.

**May:** validate policy, flags, rollout, freshness, field presence.  
**Must not:** produce recommendations, rank topics, write educational state.

Denial reasons (non-exhaustive):

| Reason | Meaning |
|---|---|
| `controlled_advisory_flag_off` | Feature flag OFF |
| `policy_invalid` / `multiple_advisory_fields_forbidden` / `advisory_field_not_approved` | Policy governance failure |
| `rollout_percentage_excluded` | Student outside rollout bucket |
| `advisory_unavailable` / `advisory_invalid` / `advisory_stale` | Advisory quality gate |
| `approved_field_missing` | Approved field absent on advisory |
| `policy_not_yet_effective` | `effective_from` in the future |
| `policy_allows_approved_field` | Allow |

Rollout bucketing is deterministic:

```
bucket = sha256("{salt}:{student_id}")[:8] % 100
in_rollout = bucket < rollout_percentage
```

---

## 4. Explainability

Every evaluated recommendation carries `advisory_activation`:

**When activated**

| Key | Content |
|---|---|
| `activated` | `true` |
| `advisory_field_used` | `consistency_summary` |
| `policy_version` | Active policy version |
| `activation_reason` | Allow reason |
| `evidence_provenance` | Advisory id, evidence refs, consistency snapshot |

**When rejected**

| Key | Content |
|---|---|
| `activated` | `false` |
| `rejection_reason` | Explicit deny reason |
| `policy_version` / `policy_id` | When available |
| `evidence_provenance` | Present when advisory was inspected |

Authority remains `runtime_a` for educational decisions. The evaluator authority is `controlled_advisory` on the decision DTO only.

---

## 5. Rollback strategy

| Action | Effect |
|---|---|
| Set `KWALITEC_CONTROLLED_ADVISORY=0` (or unset) | Activation DI not constructed; RecommendationService path identical to pre-P3 |
| Set rollout percentage to `0` | Flag may stay ON for dry-run ops, but all students denied (`rollout_percentage_excluded`) |
| Invalidate policy / freshness | Denials recorded; ranking unchanged |

Rollback is immediate and does not require schema migrations, Adaptive changes, or Strategy changes.

Dual-run ops field: `DualRunStatus.controlled_advisory`.

---

## 6. Simulation comparison

`ENABLE_DECISION_SIMULATION` remains independently available.

After controlled activation (or rejection metadata attachment), Runtime A may still invoke `DecisionSimulationService.simulate_after_recommendations` to compare:

1. **Policy-driven production recommendation** (possibly rationale-annotated)
2. **Simulation recommendation** (`simulation_only=True`)

This validates rollout behaviour without transferring authority to simulation.

---

## 7. Operational safeguards

1. Flag defaults **OFF**; rollout defaults to **0%**.
2. Exactly one approved field — expansion requires architecture review.
3. Evaluator never recommends.
4. Influence limited to rationale annotation.
5. Failures in activation are swallowed so the student path never breaks.
6. Recovery / Adaptive / Strategy / multi-field / AI coaching remain forbidden.
7. Companion Evidence Advisory (`ENABLE_EVIDENCE_ADVISORY`) remains the read path; controlled activation does not bypass `EvidenceAdvisoryPort`.

---

## 8. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `AdvisoryPolicy` | `controlled_advisory/contracts.py` | Immutable policy DTO | Ranking |
| `AdvisoryActivationDecision` | `contracts.py` | Allow/deny + reasons | Recommendations |
| `ControlledAdvisoryExplainability` | `contracts.py` | Activation / rejection record | Authority transfer |
| `ControlledAdvisoryPolicyEvaluator` | `policy_evaluator.py` | Governance evaluation | Producing recommendations |
| `ControlledAdvisoryActivation` | `activation.py` | Minimal Runtime A apply | Multi-field / recovery / Adaptive |
| `RecommendationService._apply_controlled_advisory` | `services/recommendation_service.py` | Runtime A hook | Changing Adaptive / Strategy |

---

## 9. Tests

| Suite | Coverage |
|---|---|
| `tests/.../controlled_advisory/test_contracts.py` | Policy immutability, single-field rules, explainability |
| `tests/.../controlled_advisory/test_policy_evaluator.py` | Allow/deny, freshness, rollout gating |
| `tests/.../controlled_advisory/test_activation.py` | Acceptance/rejection, Runtime A integration, simulation, rollback, field isolation |
| `tests/application/config/test_v2_flags.py` | Flag default OFF + dual-run field |

---

## 10. Explicit non-goals (binding)

- Recovery activation
- Adaptive Engine / Strategy Engine / Twin changes
- Multiple advisory fields
- AI-generated coaching / autonomous optimisation
- Priority / title / category / ranking rewrites
