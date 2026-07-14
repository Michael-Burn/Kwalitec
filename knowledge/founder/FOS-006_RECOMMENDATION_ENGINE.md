# FOS-006 — Founder Recommendation Engine

**Document ID:** FOS-006  
**Title:** Founder Recommendation Engine  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure

---

## Purpose

The Founder Recommendation Engine consumes an immutable
`FounderOperationalState` snapshot and produces a deterministic
`RecommendationSet`.

Version 1 is **rule-based**.

It performs **no** AI reasoning, LLM calls, machine learning, or free-form
natural language generation. Recommendation wording comes only from
predefined templates.

Recommendations are **advisory only**. They never authorise releases,
mutate subsystems, or automate delivery.

---

## Architecture

Package root: `app/founder/recommendations/`

```text
app/founder/recommendations/
├── __init__.py              # Public exports
├── config.py                # Thresholds, priorities, template ids
├── models/                  # Recommendation, RecommendationSet, Evidence
├── dto/                     # RuleOutcome + validation cargo
├── rules/                   # Independent RecommendationRule classes
├── evaluators/              # RecommendationEngine
├── templates/               # Predefined wording catalog
├── providers/               # TemplateProvider
├── validators/              # RecommendationSetValidator
├── services/                # FounderRecommendationService
└── tests/                   # Unit tests (mocked Operational State)
```

### Layering

```text
FounderRecommendationService
        ↓
RecommendationEngine + RecommendationSetValidator
        ↓
RecommendationRule(s) → RuleOutcome(s)
        ↓
TemplateProvider → Recommendation wording
        ↓
FounderOperationalState  (sole input)
```

No Flask routes. No HTML templates. Pure application / service layer.

---

## Rule Engine

Each Version 1 rule is an independent class implementing
`RecommendationRule`:

| Rule | Trigger | Priority | Template |
|---|---|---|---|
| `NoInternalAlphaFeedbackRule` | `feedback_count == 0` | High | Wait for Internal Alpha before releasing |
| `ArchiveValidationFailedRule` | `archive_inconsistencies > 0` | Critical | Resolve archive inconsistencies |
| `EngineeringHealthBelowThresholdRule` | `tests_pass` is false **or** validation errors above threshold | Critical | Pause new capabilities; improve engineering quality |
| `HighDuplicateFeedbackRule` | duplicates ≥ absolute threshold **or** ratio ≥ threshold | High | Prioritise recurring user issues |
| `NoActiveCapabilitiesRule` | `active_count == 0` | Medium | Select highest-priority roadmap capability |

Rules return a `RuleOutcome` (template id + evidence + priority). They do
**not** invent wording. The engine renders templates and sorts results.

`RecommendationEngine` responsibilities:

1. Run every registered rule
2. Collect non-null outcomes
3. Resolve templates into `Recommendation` instances
4. Sort by priority
5. Return an immutable `RecommendationSet`

---

## Priority System

Supported priorities (highest → lowest):

1. **Critical**
2. **High**
3. **Medium**
4. **Low**

`overall_status` is derived from the highest priority present:

| Highest priority | overall_status |
|---|---|
| (none) | `healthy` |
| Critical | `critical` |
| High | `attention` |
| Medium / Low | `advisory` |

---

## Recommendation Lifecycle

```text
FounderOperationalState
        ↓
FounderRecommendationService.recommend(state)
        ↓
RecommendationEngine.evaluate(state)
        ↓
RuleOutcome[]  →  TemplateProvider  →  Recommendation[]
        ↓
sort by priority
        ↓
RecommendationSetValidator.validate(...)
        ↓
immutable RecommendationSet
```

Each `Recommendation` cites `RecommendationEvidence` rows
(`source`, `metric`, `value`) taken from the snapshot — never from live
subsystem queries.

The set records the analysed `snapshot_version` so consumers know which
named state was interpreted.

---

## Dependencies

Consume **only**:

- `FounderOperationalState` (FOS-005)

Never call directly:

- Knowledge Engine
- Capability Archive
- Internal Alpha Pipeline

The Operational State is the only input. Dashboard is out of scope.

---

## Validation

`RecommendationSetValidator` checks:

- Unique recommendation ids
- Priority values in the allowed set
- Template existence (Version 1 ids ≡ registered template ids)
- Evidence references (non-empty source/metric; value present)
- Snapshot version and generated_at present
- Non-empty overall_status

Failures raise `RecommendationValidationError` with an explicit
`ValidationReport`.

---

## Future AI Integration

Version 1 intentionally excludes AI. A future FOS capability may:

- Propose additional candidate recommendations from language models
- Rank or cluster advisory text

Any AI path must:

- Remain behind a separate module / feature flag
- Still consume `FounderOperationalState` as the factual base
- Never replace the deterministic rule core for Critical release gates
- Keep generated text clearly labelled as non-authoritative

Until then, only predefined templates are allowed.

---

## Constraints

Version 1 intentionally does **not**:

- Implement AI, OpenAI, or LLMs
- Modify Dashboard, Operational State, Internal Alpha, or Knowledge Engine
- Implement release automation
- Persist recommendations to a database
- Expose HTTP endpoints

---

## Related Paths

| Path | Role |
|------|------|
| `app/founder/recommendations/` | Implementation |
| `knowledge/founder/FOS-006_RECOMMENDATION_ENGINE.md` | This specification |
| `knowledge/founder/FOS-005_OPERATIONAL_STATE.md` | Sole input snapshot |
| `app/founder/operational_state/` | Upstream aggregation |

---

## Owner

Founder Operating System

## Status

Active — Version 1.0
