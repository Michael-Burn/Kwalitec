# Programme III — Recommendation Policy Framework

**Milestone:** P3-MS003 — Recommendation Policy Framework  
**Directive:** Engineering Directive 001 (Recommendation Policy Framework)  
**Status:** Implemented (framework scaffolding; weighting not applied)  
**Package:** `app/infrastructure/adapters/recommendation_policy/`  
**Engine:** `RecommendationPolicyEngine`  
**Runtime A hook:** `RecommendationService.generate_recommendations(..., recommendation_policy=)`  
**Feature flag:** `KWALITEC_RECOMMENDATION_POLICY` → `ENABLE_RECOMMENDATION_POLICY` (**default OFF**)  
**Contract version:** `p3.ms003.1` (`RECOMMENDATION_POLICY_VERSION`)  
**Companions:** `CONTROLLED_ADVISORY_ACTIVATION.md`, `ADVISORY_OUTCOME_MEASUREMENT.md`, `ADVISORY_EVALUATION_ARCHITECTURE.md`

---

## 0. Purpose

Introduce a **declarative, versioned policy framework** that defines when and how approved advisory information may influence Runtime A recommendations.

> Educational behaviour should evolve through explicit, versioned policy rather than embedded code.

| In scope | Out of scope |
|---|---|
| Immutable `RecommendationPolicy` DTO | Policy-driven weighting / ranking changes |
| `RecommendationPolicyEngine` (validate / resolve / expose) | Automatic optimisation |
| Runtime A policy consultation + explainability | Adaptive Engine modifications |
| Independent policy versioning | Recovery behaviour |
| `ENABLE_RECOMMENDATION_POLICY` | AI-generated educational decisions |
| Governance documentation | Autonomous policy updates |
| | Additional advisory fields |

**Stop condition:** Stop after the Recommendation Policy Framework. Await architecture review before introducing policy-driven weighting or expanded advisory influence.

---

## 1. Policy lifecycle

```
Author / ops define RecommendationPolicy (immutable; versioned)
        │
        ▼
validate_recommendation_policy
        │
        ├── invalid → PolicyDecision(applicable=False, reason=…)
        └── valid
                │
                ▼
RecommendationPolicyEngine.resolve / resolve_for_recommendation
        │
        ├── feature flag OFF → deny (REASON_FLAG_OFF)
        ├── effective_from future → deny
        ├── resolve advisory_rules
        ├── resolve weighting_rules (exposed; never applied to ranking)
        └── PolicyDecision (advisory to Runtime A)
                │
                ▼
Runtime A RecommendationService
        │
        ├── produces recommendations (sole educational authority)
        └── attach RecommendationPolicyExplainability
             (policy version, rule ids, advisory inputs, rationale)
```

Lifecycle rules:

1. Policy is authored and versioned **outside** recommendation math.
2. Engine validates and resolves — never generates recommendations.
3. Runtime A may request applicable policy **before** producing recommendations.
4. Policy outputs are **advisory**; Runtime A retains final authority.
5. Every policy-influenced recommendation path records explainability.
6. Disabling the flag removes DI construction and restores prior behaviour.

---

## 2. Policy model

### `RecommendationPolicy` (immutable)

| Field | Meaning |
|---|---|
| `policy_id` | Stable policy identity (`recommendation-policy-p3-ms003`) |
| `version` | Independent policy revision (`p3.ms003.1`) |
| `effective_from` | ISO timestamp; future policies deny until effective |
| `advisory_rules` | Declared advisory influence rules |
| `weighting_rules` | Declared weighting factors (**resolved, not applied**) |
| `activation_constraints` | Flag / effective_from and related gates |
| `explainability_requirements` | Required explainability fields |

### `AdvisoryRule`

| Field | Meaning |
|---|---|
| `rule_id` | Stable rule identifier |
| `advisory_field` | Advisory field the rule concerns |
| `influence_mode` | `annotate` \| `permit` (declarative only) |
| `enabled` | Whether the rule may resolve as applicable |
| `rationale` | Human-readable reason for rule application |
| `conditions` | Simple declarative gates (e.g. require advisory present) |

### `WeightingRule`

| Field | Meaning |
|---|---|
| `rule_id` | Stable rule identifier |
| `factor` | Named weighting factor |
| `weight` | Declared numeric weight |
| `enabled` | Whether the rule may resolve as applicable |
| `rationale` | Why the factor exists |
| `conditions` | Declarative gates |

**P3-MS003 binding:** weighting resolutions always set `applied_to_ranking=False` and `PolicyDecision.weighting_applied=False`. Applying weights to Runtime A ranking requires a later reviewed milestone.

### Default policy

The default policy permits Runtime A to **consider** `consistency_summary` under Controlled Advisory alignment (annotate mode) and includes a **disabled** reserved weighting placeholder so the surface is ready without behavioural ranking change.

---

## 3. Versioning strategy

1. Every policy carries an explicit `version` string independent of package / Adaptive / Twin flags.
2. Framework contract version (`RECOMMENDATION_POLICY_VERSION` / `p3.ms003.1`) versions the DTO surface.
3. Environment overrides:
   - `KWALITEC_RECOMMENDATION_POLICY_ID`
   - `KWALITEC_RECOMMENDATION_POLICY_VERSION`
   - `KWALITEC_RECOMMENDATION_POLICY_EFFECTIVE_FROM`
4. Explainability always records the **policy version** that was resolved, not only the framework version.
5. Changing educational governance requires a new policy version — not silent code edits inside `RecommendationService` ranking helpers.

---

## 4. Governance model

| Role | Responsibility |
|---|---|
| Policy author / ops | Define immutable policy versions and effective dates |
| `RecommendationPolicyEngine` | Validate, resolve applicable rules, expose decisions |
| Runtime A (`RecommendationService`) | Produce final recommendations; consult policy; attach explainability |
| Controlled Advisory (P3-MS001) | Gate utilisation of the single approved advisory field |
| Outcome Measurement (P3-MS002) | Observe activation outcomes (orthogonal) |

Authority labels:

- `recommendation_policy` — policy decision artefacts
- `runtime_a` — educational recommendations and attached explainability

Governance invariants:

1. Policy never bypasses Runtime A.
2. Policy never writes mastery / readiness / schedule state.
3. Policy never autonomously updates itself.
4. Feature flag isolation from all prior Programme II / III flags.
5. Immediate rollback by disabling `KWALITEC_RECOMMENDATION_POLICY`.

---

## 5. Runtime integration

```
RecommendationService.generate_recommendations(..., recommendation_policy=engine)
        │
        ├── (optional) engine.resolve_for_recommendation(user_id, advisory=…)
        ├── Runtime A ranking / selection (unchanged)
        ├── Controlled Advisory applicator (optional, separate flag)
        └── engine.apply_to_recommendations → attach explainability only
```

Influence in this milestone:

1. **Never** changes priority, title, category, or sort order.
2. **Only** attaches `recommendation_policy` explainability when the engine is enabled.
3. Weighting rules may appear in the decision as applicable / not applicable, but are **not** used to reweight.

DI: `build_production_experience` constructs `RecommendationPolicyEngine` only when `ENABLE_RECOMMENDATION_POLICY` is ON.

Dual-run ops field: `DualRunStatus.recommendation_policy`.

---

## 6. Explainability

Every recommendation influenced by policy records:

| Field | Source |
|---|---|
| Policy version | `RecommendationPolicy.version` |
| Rule identifiers | Applicable `rule_id` values |
| Advisory inputs considered | Snapshot of advisory metadata consulted |
| Rationale | Why rules applied (or why not) |

Attachment key on recommendation dicts: `recommendation_policy`.

`explainability_fields_present(...)` encodes the invariant for tests and ops checks.

---

## 7. Feature flag & rollback

| Environment | Flag field | Default |
|---|---|---|
| `KWALITEC_RECOMMENDATION_POLICY` | `ENABLE_RECOMMENDATION_POLICY` | OFF |

Independently controllable from:

- `ENABLE_CONTROLLED_ADVISORY`
- `ENABLE_ADVISORY_OUTCOME_MEASUREMENT`
- `ENABLE_ADVISORY_EVALUATION`
- `ENABLE_DECISION_SIMULATION`
- `ENABLE_EVIDENCE_ADVISORY`
- all prior Programme II / Adaptive / Twin / Strategy / Evidence flags

### Immediate rollback

| Action | Effect |
|---|---|
| Unset / set `KWALITEC_RECOMMENDATION_POLICY=0` | Engine DI not constructed; Runtime A path untouched |
| Keep Controlled Advisory OFF | No advisory field utilisation; policy may still resolve for explainability |

---

## 8. Future extension points

After architecture review, this framework may be extended to:

1. **Expanded advisory influence** — additional fields beyond Controlled Advisory’s / weight application’s single approved field (separate milestone).
2. **Policy registry / promotion** — durable multi-version registry with signed promotion (not autonomous updates).
3. **Simulation coupling** — compare policy versions in Decision Simulation / Advisory Evaluation.
4. **Outcome-informed review** — human review using P3-MS002 metrics to decide whether to promote a new policy version.

**P3-MS004 delivered** policy-driven bounded weighting for `consistency_summary` under `ENABLE_POLICY_WEIGHTING`. See `POLICY_WEIGHT_APPLICATION.md`.

Binding constraint: **framework ≠ unbounded optimisation**. Automatic tuning beyond declared bounds, ranking rewrites outside Runtime A, and AI coaching remain forbidden.

---

## 9. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `RecommendationPolicy` | `recommendation_policy/contracts.py` | Immutable versioned policy DTO | Generating recommendations |
| `AdvisoryRule` / `WeightingRule` | `contracts.py` | Declared rule surfaces | Ranking mutation |
| `PolicyDecision` | `contracts.py` | Advisory decision for Runtime A | Educational authority |
| `RecommendationPolicyExplainability` | `contracts.py` | Explainability record | Scoring / mastery |
| `RecommendationPolicyEngine` | `recommendation_policy/engine.py` | Validate / resolve / expose | Building recommendations |
| `RecommendationService` hook | `services/recommendation_service.py` | Consult + attach explainability | Embedding policy math |

---

## 10. Tests

| Suite | Coverage |
|---|---|
| `tests/.../recommendation_policy/test_contracts.py` | Policy immutability, versioning, validation, explainability |
| `tests/.../recommendation_policy/test_engine.py` | Rule resolution, effective_from, weighting not applied, attach |
| `tests/.../recommendation_policy/test_runtime_integration.py` | Runtime A integration, flag isolation, composition DI, authority |
| `tests/application/config/test_v2_flags.py` | Flag default OFF + dual-run field |

---

## 11. Explicit non-goals (binding)

- Policy-driven weighting / ranking changes
- Additional advisory fields
- Automatic optimisation
- Adaptive Engine / Strategy / Twin behavioural changes
- Recovery behaviour
- AI-generated educational decisions
- Autonomous policy updates
