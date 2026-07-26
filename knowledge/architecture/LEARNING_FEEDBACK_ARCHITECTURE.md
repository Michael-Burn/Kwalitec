# Learning Feedback Architecture (EP-003.4)

**Programme:** EP-003.4 — Learning Feedback Loop  
**Status:** Implemented  
**Package:** `app/infrastructure/adapters/learning_feedback/`  
**Feature flag:** `KWALITEC_LEARNING_FEEDBACK` → `ENABLE_LEARNING_FEEDBACK` (**default OFF**)  
**Contract version:** `ep003.4.1`  
**Companions:** `EXPERIENCE_FEEDBACK_ARCHITECTURE.md`, `EXPERIENCE_OBSERVATION_ARCHITECTURE.md`, `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`, `STUDENT_DIGITAL_TWIN.md`

---

## 0. Purpose

Record **observed student behavioural evidence** about interactions with plans, recommendations, and study activities — so future adaptive intelligence can be grounded in lawful observations.

> Feedback records evidence.  
> Feedback does not draw educational conclusions.

| In scope | Out of scope |
|---|---|
| Immutable `LearningFeedbackEvent` | Educational adaptation |
| Process-local recorder + fail-open emitters | Twin Knowledge State writes |
| Runtime A service emission hooks | Recommendation re-ranking |
| Claim boundaries + forbidden inference keys | Readiness score mutation |
| `ENABLE_LEARNING_FEEDBACK` | Presentation speech / UX copy |
| Schema / ownership / fail-open tests | Durable persistence (follow-on) |

**Stop condition:** Do not introduce Evidence-informed behavioural adaptation from these events without a separate architecture review (same gate as P2-MS008 §9).

---

## 1. Distinction from related systems

| System | Records | Adapts? |
|---|---|---|
| **Learning Feedback (this)** | Plan / recommendation / study interaction evidence from Runtime A | No |
| Experience Feedback (P2-MS008) | Factual Evidence counts for Home display | No |
| Experience Observation (P2-MS006) | Journey delivery events → Evidence | No |
| Alpha / Research feedback | Product research responses | No |
| LXP-004 session feedback | Post-session narration | No |

---

## 2. Evidence model

### 2.1 Observable event types

| Event | Source authority | Claim boundary |
|---|---|---|
| `plan_completed` | `planning_service` | `plan_interaction` |
| `recommendation_accepted` | `recommendation_service` | `preference_journal` |
| `recommendation_dismissed` | `recommendation_service` | `preference_journal` |
| `session_missed` | `planning_service` | `observed_behaviour` |
| `recovery_applied` | `planning_service` | `plan_interaction` |
| `revision_adhered` | `planning_service` | `plan_interaction` |
| `revision_deferred` | `planning_service` | `plan_interaction` |
| `study_consistency_observed` | `readiness_service` | `study_habit_signal` |

### 2.2 Observed vs inferred

| May record | Must not record / infer |
|---|---|
| Mission completed | Mastery / estimated knowledge gain |
| Tip accepted or dismissed | Tip was “correct” educationally |
| Missed-session count signal | Student is “unmotivated” as fact |
| Recovery mode applied | Recovery “fixed” the deficit |
| Streak integers | Streak proves learning quality |

`evidence_kind` is always `observed_evidence`. Payload keys in `FORBIDDEN_INFERENCE_KEYS` are rejected at schema validation.

---

## 3. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `LearningFeedbackEvent` | `contracts.py` | Immutable observed event | Conclusions |
| `LearningFeedbackRecorder` | `recorder.py` | Process-local buffer | Persistence / decisions |
| Emit helpers | `emitter.py` | Fail-open service API | Ranking / planning |
| Service hooks | Recommendation / Planning / Readiness | Emit within ownership | Cross-authority maths |

---

## 4. Emission lifecycle

```
Student interaction / service observation
        │
        ▼
Runtime A owner (Recommendation | Planning | Readiness)
        │  fail-open emit_*
        ▼
LearningFeedbackRecorder.record   ← ENABLE_LEARNING_FEEDBACK
        │
        ▼
process-local buffer (analytics follow-on)
```

Flag OFF or recorder unbound → `skipped` result; student path continues.

---

## 5. Integration ownership

| Service | Emits when |
|---|---|
| `RecommendationService.record_decision` | Accept / dismiss preference |
| `PlanningService._build_daily_study_plan_body` | Missed + recovery signals on plan |
| `PlanningService.record_plan_completion_feedback` | Mission completion (via MissionService) |
| `ReadinessService.get_dashboard_readiness_surface` | Study consistency (streaks) |

`ReadinessService.get_overall_readiness` does **not** emit (collector-safe).  
`RuntimeAPresentationAdapter` does **not** emit.

---

## 6. Feature flags

Independently controllable from `ENABLE_EXPERIENCE_FEEDBACK`, `ENABLE_EXPERIENCE_OBSERVATION`, and `ENABLE_EVIDENCE_PLATFORM`.

Production default: **OFF**.

---

## 7. Constitutional rules

1. No service may infer educational conclusions outside its authority via feedback.
2. Recommendation accept/dismiss ≠ Educational Evidence of understanding (Art. V §2).
3. Feedback infrastructure never ranks, plans, or scores.
4. Twin Knowledge State is not updated by this programme.
5. Trust > optimisation — fail open; under-claim.

---

## 8. Downstream: Personal Learning Profile (EP-004.1)

Learning Feedback events are the primary observed-evidence input for the
Personal Learning Profile aggregator (`PERSONAL_LEARNING_PROFILE_ARCHITECTURE.md`).
The profile summarises behavioural attributes with confidence and provenance;
it does **not** write back into this recorder, Twin Knowledge State, or
Runtime A educational decisions.

