# EP-001.2 — Gap Analysis

**Milestone:** EP-001.2 — Adaptive Study Planner  
**Phase:** 2 — Gap Analysis  
**Date:** 2026-07-26

Compare existing Runtime A planning vs Adaptive Study Planner success criteria (consume Canonical Learner State; extend existing planner; no duplicate engines / learner-state models).

---

## 1. Capability matrix

| Capability | Status | Evidence | Gap |
|---|---|---|---|
| Study plan CRUD / week distribution | **Implemented** | `StudyPlanService`, `PlanningService.generate_curriculum_week_plans` | None for EP-001.2 |
| Daily mission persistence (Learning) | **Implemented** | `PlanningService.generate_today_mission` → curriculum next incomplete topic | Does not read Foundation |
| Daily mission persistence (Revision) | **Implemented** | Deterministic kind rotation + `weakest_completed_topic_label` | Weak label via AdaptiveLearning / ORM, not CLS |
| Available study time (plan minutes) | **Implemented** | `StudyPlan.weekday/weekend_study_minutes`, `TimeEngineService` | Not composed with CLS preferences / behaviour |
| Balanced review/weak/progression set | **Partially implemented** | `MissionOptimizer` dict helper | Bypasses Foundation; not wired as planner output |
| Revision priorities from learner state | **Partially implemented** | Weak topics + review due dates in AdaptiveLearning | Duplicate learner-state reads outside Twin |
| Topic ordering | **Partially implemented** | Curriculum traversal + TopicProgress completion | Progress re-queried; should prefer CLS `topic_progress` when Twin ON |
| Recommended workload | **Partially implemented** | TimeEngine surplus/deficit; plan minutes size tasks | No CLS consistency/streak/preference composition |
| Recommendations engine | **Implemented** (adjacent) | `RecommendationService` | Out of EP-001.2 scope to rewrite; leave intact |
| Consume `CanonicalLearnerState` | **Missing** | Foundation exists (EP-001.1); no planner consumer | Primary gap |
| Daily study plan projection API | **Missing** | No single planner method returning missions + revision + order + workload from CLS | Primary gap |
| Parallel planner consolidation | **N/A this milestone** | OS / Journey / Strategy stacks remain | Explicitly do **not** delete or replace |

---

## 2. Already implemented

- Wizard → StudyPlan / WeekPlan persistence
- Idempotent `generate_today_mission`
- Learning Mode syllabus fidelity (IA-004)
- Revision Mode deterministic templates
- Curriculum-ordered topic traversal via `CurriculumService`
- Time capacity vs remaining hours
- Mission ORM CRUD

---

## 3. Partially implemented

- MissionOptimizer balance (exists, Foundation-blind)
- Weak / review selection (AdaptiveLearningService, Foundation-blind)
- Workload sizing from plan minutes only
- Preference hints on Foundation `study_state` unused by planner

---

## 4. Missing

1. **Planner consumer** of `StudentDigitalTwinFoundation.assemble` → planning inputs
2. **Daily study plan projection** packaging:
   - today's study missions (priorities / slots)
   - revision priorities
   - topic ordering
   - recommended workload
3. **Fail-open wiring** when Twin flag OFF (legacy path unchanged)
4. **Explainability refs** tying plan outputs to Foundation provenance

---

## 5. What must not be done

| Anti-goal | Why |
|---|---|
| New parallel `AdaptiveStudyPlannerService` that replaces `PlanningService` | Violates “extend existing planner” |
| New learner-state store / mastery map inside planner | Twin owns learner state |
| Recompute streaks / readiness / mastery in planner | Duplicate Twin work |
| Fabricate mock performance | Foundation marks unavailable |
| Promote OS / Strategy / Journey planners to production authority | Scope creep; duplication |
| Change Learning Mode to interrupt with review topics | Violates IA-004 |

---

## 6. Consolidation preference

1. **Extend** `PlanningService` with a Foundation-backed daily plan builder.
2. **Add** a thin infrastructure consumer (`adaptive_study_planner`) that **projects** CLS → planner inputs / outputs — analogous to Adaptive `twin_input`, not a second planner.
3. **Teach** `MissionOptimizer` (and revision weak-label path) to prefer CLS payloads when Twin ON.
4. **Keep** StudyPlan minutes + TimeEngine as capacity authority; merge CLS preferences only as planner-owned workload recommendation.
5. **Leave** RecommendationService / OS / Journey stacks untouched except where they already call PlanningService.

---

## 7. Recommendation

Implement EP-001.2 by extending Runtime A planning to **consume** EP-001.1 `CanonicalLearnerState`, packaging adaptive daily plan outputs without introducing a duplicate planner or learner-state model.
