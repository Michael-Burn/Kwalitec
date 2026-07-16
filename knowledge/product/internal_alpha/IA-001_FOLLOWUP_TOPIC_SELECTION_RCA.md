# IA-001 Follow-up — Mission Topic Selection RCA

**Capability ID:** IA-001 follow-up  
**Programme:** Internal Alpha Stabilization  
**Status:** Investigation only — awaiting Architecture Review  
**Date:** 2026-07-15  
**Scope:** Within-plan mission topic selection (study_plan_id binding assumed correct)

---

## Observed behaviour

| Surface | Shown topic |
|---|---|
| Study Plan (CS1) — Current learning | Topic **4.2** (Understand and use generalised linear models) |
| Today's Mission | Topic **2.6** (Sampling distributions — already completed) |
| CM1 | Behaves correctly (plan binding OK) |

Conclusion from observation: `study_plan_id` scoping from IA-001 is not the remaining defect. The defect is **which topic** `PlanningService` chooses **inside** the active CS1 plan.

---

## Root Cause Analysis

### Verdict

Today's Mission selected Topic 2.6 via **`PlanningService._select_topic_for_today` Priority 1 (due-for-review)** and/or **Priority 2 (weak topics)** — adaptive preemption that **ignores** the study plan's current learning pointer (`curriculum_topic_code` / next incomplete = 4.2).

Topic 4.2 was **never evaluated** once Priority 1 or 2 returned a hit. Priority 3 (`CurriculumService.get_next_incomplete_topic`) is the only path that would have returned 4.2; it was short-circuited.

This is **not** produced by `RecommendationService`, MissionIntelligence / Twin / Decision, or a cross-plan legacy mission row.

### Why Topic 2.6 was selected

`_select_topic_for_today` order (unchanged by IA-001):

1. **Priority 1 — due review** → `AdaptiveLearningService.get_topics_due_for_review`, then filter to active `curriculum_id`
2. **Priority 2 — weak** → `AdaptiveLearningService.get_weak_topics(threshold=60)`, then filter to active `curriculum_id`
3. **Priority 3 — next incomplete** → `CurriculumService.get_next_incomplete_topic`

Both Priority 1 and Priority 2 queries **omit** `TopicProgress.completed`:

| Selector | Filters | Omits |
|---|---|---|
| `get_topics_due_for_review` | `next_review_date <= today`, `current_stage != Mastered` | `completed`, `STAGE_COMPLETED` |
| `get_weak_topics` | `revision_count > 0`, `mastery_score < 60` | `completed` |

So a syllabus-**completed** CS1 topic 2.6 remains eligible when:

- **P1 (most likely):** `next_review_date` is still on/before today and stage is not `Mastered`. Mission completion sets `current_stage = Completed` (≠ `Mastered`) and does **not** clear or reschedule `next_review_date` (`_apply_mission_topic_progress`). Prior study attempts that called `update_mastery_after_attempt` leave an overdue review date that **survives** completion.
- **P2 (secondary):** `revision_count > 0` and `mastery_score < 60` even if `completed=True` (e.g. completed flagged without mastery raised to ≥60).

### Why Topic 4.2 was ignored

4.2 is the study plan's **current learning** topic because:

- `StudyPlan.curriculum_topic_code` advanced via `reconcile_current_topic_pointer` past completed leaves, and/or
- TopicProgress for 4.2 has `current_stage == Learning` (Study Plan roadmap badge).

That pointer is **never consulted** by `_select_topic_for_today`. Priority 3 would return 4.2 (`get_next_incomplete_topic`), but only after empty P1 and P2 lists. Once 2.6 wins P1 or P2, 4.2 is skipped by design of the priority cascade.

### Which decision path

| Authority | Involved? |
|---|---|
| `PlanningService._select_topic_for_today` | **Yes — sole mission topic chooser** |
| Review logic (Priority 1) | **Primary suspect** |
| Weak-topic logic (Priority 2) | Possible if mastery still &lt; 60 |
| Next-topic logic (Priority 3) | **No — short-circuited; would have chosen 4.2** |
| `RecommendationService` | **No** — advisory cards / next-incomplete **label** only; does not drive mission persistence |
| Legacy unbound / cross-plan path | **No** — CM1 OK; same-plan CS1 mismatch |
| EI / Twin / MissionIntelligence | **No** — product missions still `PlanningService` → ORM (`ENABLE_EI_MISSIONS=False`) |

---

## Decision flow

```
StudyPlanService.get_user_active_plan(user)
        │  curriculum_topic_code / Learning badge → 4.2  (display only for roadmap)
        ▼
PlanningService.generate_today_mission
        ▼
PlanningService._generate_mission_for_date
        ▼
PlanningService._select_topic_for_today(user, active_plan, today)
        │
        ├─ P1  AdaptiveLearningService.get_topics_due_for_review(user)
        │      filter topic.curriculum_id == active curriculum
        │      ✗ does not exclude completed / STAGE_COMPLETED
        │      → if 2.6 due → RETURN 2.6   ← observed outcome (likely)
        │
        ├─ P2  AdaptiveLearningService.get_weak_topics(user, 60)
        │      filter topic.curriculum_id == active curriculum
        │      ✗ does not exclude completed
        │      → if 2.6 weak → RETURN 2.6
        │
        └─ P3  CurriculumService.get_next_incomplete_topic
               → would RETURN 4.2  (never reached)
        ▼
Mission title / tasks built from selected topic (2.6)
MissionService.create_mission(..., study_plan_id=active_plan.id)
```

---

## Relevant code path

| Step | Location |
|---|---|
| Mission generation entry | `PlanningService.generate_today_mission` |
| Topic choose | `PlanningService._select_topic_for_today` (~L692–829) |
| Due-review query | `AdaptiveLearningService.get_topics_due_for_review` (~L312–334) |
| Weak query | `AdaptiveLearningService.get_weak_topics` (~L268–288) |
| Next incomplete (unused here) | `CurriculumService.get_next_incomplete_topic` |
| Completion leaves overdue review | `app/mission/routes.py` `_apply_mission_topic_progress` (sets `completed` / `STAGE_COMPLETED`, calls `mark_reviewed`, **does not** update `next_review_date`) |
| Learning pointer (4.2) | `StudyPlanService.reconcile_current_topic_pointer` + Study Plan template `current_stage == 'Learning'` |
| IA-001 scope note | Priorities intentionally unchanged; only curriculum filter added to P1/P2 |

---

## Recommended fix (do not implement until Architecture Review)

Architecture Review should choose product policy first, then implement:

### Preferred (integrity with Study Plan “Current learning”)

1. **Exclude syllabus-completed progress from mission P1 and P2**  
   In `_select_topic_for_today` (or in the AdaptiveLearning helpers when used for mission selection): require `completed == False` (and/or exclude `STAGE_COMPLETED`).
2. **On syllabus completion** (`_apply_mission_topic_progress`): clear `next_review_date` or reschedule from post-completion mastery so completed leaves do not remain perpetually “due.”
3. **Regression:** CS1 plan with 4.2 Learning, 2.6 `completed=True` + overdue `next_review_date` and/or weak mastery → mission topic must be **4.2**, not 2.6. Cross-curriculum IA-001 guards remain.

### Alternative (keep spaced-repetition preemption)

If review of completed topics remains desired:

- Mission title/UI must label the session as **Review** of 2.6 (not conflicting with “Current learning 4.2”), **or**
- Demote review/weak below next-incomplete for weekday “learning” missions, and expose review as a separate card.

Do **not** treat this as another `study_plan_id` binding bug. Do **not** redesign Twin/Decision for this defect.

---

## Known limitations of this investigation

- No live Internal Alpha DB dump was queried; attribution to P1 vs P2 for the specific tester depends on that user's `TopicProgress` for 2.6 (`next_review_date`, `mastery_score`, `completed`, `current_stage`). Both paths share the same structural flaw (completed topics still selectable).
- `RecommendationService` weak lists remain user-global (IA-001 known limitation) but were not the ORM mission chooser for this report.
