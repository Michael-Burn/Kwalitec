# Programme III — Policy-Governed Weight Application

**Milestone:** P3-MS004 — Policy-Governed Weight Application  
**Directive:** Engineering Directive 001 (Policy-Governed Weight Application)  
**Status:** Implemented (single-field bounded weight under governance)  
**Package:** `app/infrastructure/adapters/recommendation_policy/`  
**Artefact:** `WeightApplication`  
**Engine:** `RecommendationPolicyEngine.resolve_weight_application` / `apply_weight_to_recommendations`  
**Runtime A hook:** `RecommendationService.generate_recommendations(..., recommendation_policy=)`  
**Feature flag:** `KWALITEC_POLICY_WEIGHTING` → `ENABLE_POLICY_WEIGHTING` (**default OFF**)  
**Rollout:** `KWALITEC_POLICY_WEIGHTING_ROLLOUT_PERCENTAGE` (0–100, **default 0**)  
**Contract version:** `p3.ms004.1` (`POLICY_WEIGHT_APPLICATION_VERSION`)  
**Approved field (only):** `consistency_summary`  
**Companions:** `RECOMMENDATION_POLICY_ARCHITECTURE.md`, `CONTROLLED_ADVISORY_ACTIVATION.md`, `DECISION_SIMULATION_ARCHITECTURE.md`

---

## 0. Purpose

Permit Runtime A to **apply** a single approved weighting rule from the Recommendation Policy Framework to recommendation scoring under controlled rollout.

> Educational optimisation should emerge through governed policy rather than implicit algorithms.

This is the first milestone where advisory information may alter recommendation ordering. The change is minimal, explainable, measurable, and fully reversible.

| In scope | Out of scope |
|---|---|
| Immutable `WeightApplication` DTO | Multiple advisory fields |
| Policy weight resolver (one rule) | Adaptive Engine changes |
| Bounded adjustment (±5% default) | Recovery weighting |
| Runtime A apply + reorder | Autonomous optimisation |
| Explainability on every path | Dynamic policy generation |
| Simulation consistency check | AI-generated educational decisions |
| `ENABLE_POLICY_WEIGHTING` + rollout % | |

**Stop condition:** Stop after Policy-Governed Weight Application. Await architecture review before expanding weighting scope or enabling additional advisory fields.

---

## 1. Weighting lifecycle

```
RecommendationPolicy (versioned; one enabled apply_to_ranking WeightingRule)
        │
        ▼
ENABLE_POLICY_WEIGHTING (default OFF) + staged rollout %
        │
        ▼
RecommendationPolicyEngine.resolve_weight_application
        │
        ├── validate policy
        ├── validate weighting feature flag
        ├── validate rollout percentage (deterministic student bucket)
        ├── validate advisory freshness / field presence
        └── WeightApplication (applied | denied + reason)
                │
                ▼
Runtime A RecommendationService
        │
        ├── produces recommendations (sole educational authority)
        ├── apply_weight_to_recommendations
        │     ├── ALLOW → scoring_weight = priority_base × adjusted/base
        │     │            optional reorder by scoring_weight
        │     │            + attach policy_weight_application explainability
        │     └── DENY  → leave order unchanged
        │                  + record why no adjustment occurred
        └── DecisionSimulationService (optional)
              + compare_weight_simulation (flag divergence > tolerance)
```

Lifecycle rules:

1. Policy declares at most **one** ranking weight rule for `consistency_summary`.
2. Engine resolves an immutable `WeightApplication` — never invents recommendations.
3. Runtime A applies the adjustment and retains final authority.
4. Every adjusted (and denied) path records explainability.
5. Disabling `KWALITEC_POLICY_WEIGHTING` restores prior behaviour immediately.

---

## 2. `WeightApplication` (immutable)

| Field | Meaning |
|---|---|
| `application_id` | Deterministic id from material inputs |
| `policy_version` | Policy revision that authorised the adjustment |
| `rule_id` | Weighting rule identifier |
| `advisory_field` | Always `consistency_summary` in P3-MS004 |
| `base_weight` | Declared rule weight (default `1.0`) |
| `adjusted_weight` | Bounded result after advisory delta |
| `adjustment_reason` | Why applied or denied |
| `provenance` | Advisory / evidence provenance snapshot |
| `generated_at` | Resolution timestamp |
| `applied` | Whether Runtime A may use the adjustment |

---

## 3. Bounded adjustment rules

| Parameter | Default | Env / policy |
|---|---|---|
| Max absolute adjustment | **±5%** (`0.05`) | `KWALITEC_POLICY_WEIGHTING_MAX_ADJUSTMENT` / rule `max_adjustment` |
| Hard safety ceiling | ±25% | Policy validation rejects larger bounds |
| Streak scale | 7 days → full +max | `DEFAULT_STREAK_SCALE` |
| Formula | `delta = clamp((streak / 7) × max_adj, ±max_adj)` | Deterministic; streak `0` → `0` |
| Priority base weights | Critical `1.0`, High `0.75`, Medium `0.50`, Low `0.25` | Runtime A scoring surface |
| Scoring | `scoring_weight = priority_base × (adjusted / base)` | Applied by Runtime A |

Only `consistency_summary.active_streak` influences the delta. Engagement and other advisory fields are ignored.

---

## 4. Governance

| Role | Responsibility |
|---|---|
| Policy author / ops | Version policy, set bounds, rollout %, freshness window |
| `RecommendationPolicyEngine` | Validate policy / rollout / freshness; resolve `WeightApplication` |
| Runtime A (`RecommendationService`) | Produce recommendations; apply at most one weight; attach explainability |
| Decision Simulation (P2-MS011) | Continue parallel simulation; weight mirror compared for divergence |

Invariants:

1. Exactly one advisory field may influence weight (`consistency_summary`).
2. Weight adjustment is bounded and policy-controlled.
3. Runtime A remains the final decision authority.
4. Feature flag is independent from all prior Programme II / III flags.
5. Immediate rollback by disabling `KWALITEC_POLICY_WEIGHTING`.

---

## 5. Feature flag & rollback

| Environment | Flag field | Default |
|---|---|---|
| `KWALITEC_POLICY_WEIGHTING` | `ENABLE_POLICY_WEIGHTING` | OFF |
| `KWALITEC_POLICY_WEIGHTING_ROLLOUT_PERCENTAGE` | staged % | `0` |
| `KWALITEC_POLICY_WEIGHTING_MAX_AGE_HOURS` | freshness | `168` |
| `KWALITEC_POLICY_WEIGHTING_MAX_ADJUSTMENT` | bound | `0.05` |
| `KWALITEC_POLICY_WEIGHTING_DIVERGENCE_TOLERANCE` | sim compare | `0.001` |

### Immediate rollback

| Action | Effect |
|---|---|
| Unset / set `KWALITEC_POLICY_WEIGHTING=0` | Weighting not applied; DI may still build engine for policy-only mode |
| Set rollout to `0` | All students denied with `weight_rollout_percentage_excluded` |

---

## 6. Explainability

Attachment key: `policy_weight_application`.

Every adjusted recommendation records:

| Field | Source |
|---|---|
| Original weight | `base_weight` / `scoring_weight_original` |
| Adjusted weight | `adjusted_weight` / `scoring_weight_adjusted` |
| Policy version | `WeightApplication.policy_version` |
| Rule identifier | `rule_id` |
| Advisory provenance | Advisory snapshot used for the delta |
| Adjustment reason | Applied reason or denial reason |

If no adjustment occurs, the same attachment records **why** (`policy_weighting_flag_off`, rollout excluded, stale advisory, missing field, …).

---

## 7. Simulation & monitoring

1. Decision Simulation continues to generate parallel artefacts (unchanged student path).
2. After weight application, Runtime A mirrors the same weight resolve/apply on a stripped copy.
3. `compare_weight_simulation` flags any `scoring_weight` divergence beyond configured tolerance.
4. Ops can inspect `RecommendationPolicyEngine.last_weight_application` and `last_simulation_divergence`.
5. Dual-run status exposes `policy_weighting`.

---

## 8. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `WeightApplication` | `contracts.py` | Immutable weight artefact | Generating recommendations |
| `WeightingRule` | `contracts.py` | Declared bounds + field | Autonomous tuning |
| `resolve_weight_application` | `engine.py` | Validate + resolve one rule | Writing educational state |
| `apply_weight_to_recommendations` | `engine.py` | Runtime A apply helper | Adaptive / recovery changes |
| `RecommendationService` hook | `services/recommendation_service.py` | Authority + simulation compare | Embedding opaque AI scores |

---

## 9. Tests

| Suite | Coverage |
|---|---|
| `test_contracts.py` | WeightApplication immutability, bounds helpers, validation |
| `test_weight_application.py` | Resolver, bounded apply, denial reasons, simulation compare |
| `test_weight_runtime_integration.py` | Runtime A, flag isolation, composition DI, rollback |
| `test_v2_flags.py` | `ENABLE_POLICY_WEIGHTING` default OFF + dual-run |

---

## 10. Explicit non-goals (binding)

- Multiple advisory fields
- Adaptive Engine / Strategy / Twin behavioural changes
- Recovery weighting
- Autonomous optimisation / dynamic policy generation
- AI-generated educational decisions
- Expanding beyond ± configured bounds without a new policy version
