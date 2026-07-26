# Personal Learning Profile Architecture (EP-004.1)

**Programme:** EP-004.1 — Personal Learning Profile  
**Status:** Implemented  
**Package:** `app/infrastructure/adapters/personal_learning_profile/`  
**Feature flag:** `KWALITEC_PERSONAL_LEARNING_PROFILE` → `ENABLE_PERSONAL_LEARNING_PROFILE` (**default OFF**)  
**Contract version:** `ep004.1.1`  
**Companions:** `LEARNING_FEEDBACK_ARCHITECTURE.md`, `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`, `STUDENT_DIGITAL_TWIN.md`

---

## 0. Purpose

Transform accumulated Learning Feedback observations into a **stable, explainable Personal Learning Profile** that summarises long-term observed behaviours and preferences — without introducing a new educational authority.

> The profile summarises evidence.  
> The profile does not make educational decisions.

| In scope | Out of scope |
|---|---|
| Immutable `PersonalLearningProfile` + attributes | Ranking / readiness / planning maths owned by the profile |
| Incremental process-local store | Twin Knowledge State writes |
| Confidence + evidence provenance per attribute | Presentation speech / UX copy |
| Fail-open consumer Port for Runtime A | Durable cross-process persistence (follow-on) |
| Evidence input to RecommendationService (EP-004.2) and PlanningService (EP-004.3) | Profile-owned decisions |

**Stop condition:** Do not let Recommendation, Readiness, or Planning delegate constitutional authority to the profile. Do not invent attributes without evidence.

**EP-004.2 note:** `RecommendationService` may consume available, confidence-gated attributes as **evidence** for bounded tie-breaks, session sizing, and tip cadence. The profile still does not rank, plan, or score readiness. See `../product/ep004_2_adaptive_recommendation_personalisation/PERSONALISATION_RULES.md`.

**EP-004.3 note:** `PlanningService` may consume available, confidence-gated attributes as **evidence** for bounded pacing, duration, recovery/revision emphasis, and equivalent repair-topic selection — without changing educational slot order. See `../product/ep004_3_adaptive_planning_personalisation/PERSONALISATION_RULES.md`.

---

## 1. Distinction from related systems

| System | Role | Decides educationally? |
|---|---|---|
| **Personal Learning Profile (this)** | Long-term behavioural summary from observed evidence | No |
| Learning Feedback (EP-003.4) | Immutable interaction events | No |
| Student Digital Twin / Foundation | Learner-state read model | No (consumers decide) |
| Recommendation / Readiness / Planning | Constitutional educational authorities | Yes |
| Experience ProfileProjection | Settings / goals presentation | No |

---

## 2. Attribute model

### 2.1 Candidate attributes

| Attribute key | Epistemic kind | Evidence source | Notes |
|---|---|---|---|
| `preferred_study_session_duration` | Observed fact **or** unsupported | Declared minutes (settings) when supplied; otherwise unsupported (feedback has no duration) | Never invent minutes |
| `consistency_trend` | Derived indicator | `study_consistency_observed` streaks | Habit signal, not learning quality |
| `recovery_effectiveness` | Derived indicator | `recovery_applied` + later `plan_completed` | Follow-through proxy — not “recovery fixed deficit” |
| `revision_adherence` | Derived indicator | `revision_adhered` / `revision_deferred` | Plan interaction, not mastery |
| `recommendation_responsiveness` | Derived indicator | accept / dismiss preference journal | Accept ≠ mastery (Art. V §2) |
| `planning_completion_rate` | Derived indicator | `plan_completed` vs `session_missed` | Behavioural proxy |
| `preferred_study_windows` | Unsupported | None lawful today | Wall-clock emit time ≠ preference |

Every attribute carries: `kind`, `status`, `claim_boundary`, `value`, `confidence`, `sample_size`, `explanation`, `evidence_refs`, `limitations`.

### 2.2 Observed vs derived vs unsupported

| Kind | Meaning |
|---|---|
| `observed_fact` | Directly recorded declaration or countable observation |
| `derived_indicator` | Deterministic summary of observations (rate / trend) |
| `unsupported` | No lawful evidence — must not be invented by consumers |

Forbidden inference keys mirror Learning Feedback (`mastery`, `readiness_score`, `learning_gain`, …) plus decision keys (`next_action`, `plan_slots`).

### 2.3 Confidence

`confidence = min(1.0, sample_size / 10)` — deterministic, documented, never a readiness or mastery score.

---

## 3. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| Contracts | `contracts.py` | Immutable profile / attribute / Port | Decisions |
| Aggregator | `aggregator.py` | Evidence → attributes + provenance | Persistence / ranking |
| Store | `store.py` | Incremental immutable snapshot replace | Educational maths |
| Consumer | `consumer.py` | Fail-open resolve for Runtime A | Authority transfer |
| Adapter | `adapter.py` | DI / Port wrapper | HTTP / Twin writes |

---

## 4. Lifecycle

```
Learning Feedback events (EP-003.4)
        │
        ▼
PersonalLearningProfileAggregator
        │  label kind + confidence + evidence_refs
        ▼
PersonalLearningProfileStore (process-local)
        │
        ▼
PersonalLearningProfilePort / consume_personal_learning_profile
        │  fail-open
        ▼
RecommendationService | ReadinessService | PlanningService
   (optional inputs — authorities unchanged)
```

Flag OFF or store unbound → `skipped` / `None`; student path continues.

---

## 5. Integration ownership

| Service | May consume via | Must not |
|---|---|---|
| `RecommendationService` | `consume_personal_learning_profile` | Delegate ranking authority to the profile (EP-004.2 may apply bounded evidence-based tie-breaks only) |
| `ReadinessService` | `consume_personal_learning_profile` (dashboard/intelligence only) | Call from `get_overall_readiness` |
| `PlanningService` | `consume_personal_learning_profile` | Delegate educational priorities / mission invention to profile (EP-004.3 may apply bounded evidence-based pacing and equivalent repair selection only) |
| `RuntimeAPresentationAdapter` | — | Own or invent profile attributes / personalise ranking |

Services depend on **`PersonalLearningProfilePort`** / consumer helpers — never on aggregator internals.

---

## 6. Feature flags

Independently controllable from `ENABLE_LEARNING_FEEDBACK`, Twin, and Evidence flags.

Production default: **OFF**.

Profile may resolve with an empty event set (all attributes unavailable/unsupported). When Learning Feedback is also ON, consumer loads the process-local feedback buffer automatically.

---

## 7. Constitutional rules

1. Profile summarises evidence; it does not make educational decisions.
2. No service may delegate its constitutional authority to the profile.
3. Attributes remain explainable and traceable to observed evidence (or explicitly unsupported).
4. Fail-open; under-claim; never invent missing attributes.
5. Twin Knowledge State is not updated by this programme.
6. Trust > optimisation — preference journal never becomes mastery evidence.
