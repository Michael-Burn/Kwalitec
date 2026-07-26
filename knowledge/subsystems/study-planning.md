# Study Planning

## Purpose

Study planning turns an exam date, available study days, and a chosen curriculum into a structured plan the student can follow. It answers “what should I cover by when?” without requiring the student to invent a syllabus schedule.

Core services:

- `StudyPlanService` — plan CRUD, wizard persistence, active plan
- `PlanningService` — exam-date distribution and rebalancing
- `TimeEngineService` — available study time calculations
- `ExaminationCatalogue` / `ExamTimeline` — exam metadata and sitting dates

The multi-step wizard lives under the `study_plan` blueprint (`/study-plan`).

## Responsibilities

| Concern | Owner |
|---|---|
| HTTP wizard steps, forms, redirects | `study_plan` blueprint |
| Persist plans / week plans / active selection | `StudyPlanService` |
| Distribute topics across available days to exam | `PlanningService` |
| Compute available study capacity | `TimeEngineService` |
| Ordered topic list for distribution | `CurriculumService.get_all_topics_ordered()` |

Planning must remain **deterministic**: same curriculum, dates, and constraints → same distribution.

## Dependencies

```
study_plan blueprint
        ↓
StudyPlanService / PlanningService / TimeEngineService
        ↓
CurriculumService (canonical topics) + ORM StudyPlan / WeekPlan / Curriculum
```

- **Upstream:** authenticated user, selected curriculum (V1 or V2), exam timeline inputs.
- **Downstream consumers:** missions (work from active plan), readiness (pace vs plan), dashboard.
- **Must not:** reimplement topic ordering; call [canonical traversal](../architecture/ADR-004-canonical-topic-traversal.md).

## Data Flow

```
Wizard input (exam, availability, curriculum)
    → validate in blueprint (WTForms)
    → StudyPlanService persists plan shell
    → PlanningService pulls canonical topics via CurriculumService
    → distribute across available days / weeks
    → WeekPlan (and related) rows
    → active plan used by MissionService / dashboard
```

```
                    ┌─────────────────┐
                    │  Curriculum     │
                    │  (V1 or V2)     │
                    └────────┬────────┘
                             │ get_all_topics_ordered
                             ▼
┌──────────────┐     ┌───────────────┐     ┌─────────────┐
│ TimeEngine   │────▶│ Planning      │────▶│ StudyPlan / │
│ (capacity)   │     │ Service       │     │ WeekPlan    │
└──────────────┘     └───────────────┘     └─────────────┘
```

## Extension Points

- New wizard steps: thin blueprint route + `StudyPlanService` / `PlanningService` methods.
- New distribution heuristics: keep them in `PlanningService`, document explainability (why a topic landed in a week).
- Catalogue / sitting updates: `examination_catalogue.py` / `exam_timeline.py`.
- Rebalancing after progress changes: extend `PlanningService` without touching route math.
- **EP-001.2 Adaptive Study Planner:** when `KWALITEC_DIGITAL_TWIN=1`,
  `PlanningService.build_daily_study_plan` consumes EP-001.1
  `CanonicalLearnerState` (via `adaptive_study_planner` consumer) for today's
  mission slots, revision priorities, topic ordering, and recommended workload.
  Learner state remains Twin-owned — do not add mastery/streak stores here.
  Legacy `generate_today_mission` remains the ORM persistence path.
- **EP-003.3 Planning quality contract:** `PlanningService` applies
  `planning_quality` (mandatory explanation schema, readiness-informed
  workload notes, recommendation-aware coherence labels, recovery framing)
  to daily plans and dashboard mission surfaces. See
  [`PLANNING_SERVICE_QUALITY_CONTRACT.md`](../architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md)
  and [`ep003_3_adaptive_planning_enhancement/`](../product/ep003_3_adaptive_planning_enhancement/).
  Presentation must pass through schema-complete plans — never invent planning
  rationale.
- **EP-004.3 Planning personalisation:** when Personal Learning Profile is
  enabled, `PlanningService` may apply bounded, explainable adaptations
  (session duration, pacing, recovery/revision emphasis, equivalent repair
  topic) from profile evidence — educational slot order unchanged. See
  [`ep004_3_adaptive_planning_personalisation/`](../product/ep004_3_adaptive_planning_personalisation/)
  and the personalisation section of the planning quality contract.
  Presentation must pass through personalisation fields — never inspect the
  profile.

## Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Ordering topics with ad-hoc queries | Breaks V1/V2 and mission alignment |
| Planning math in wizard routes | Untestable; violates [ADR-001](../architecture/ADR-001-service-layer.md) |
| Assuming section weights on V1 curricula | Flat curricula weight topics differently |
| Non-deterministic “shuffle” for variety | Violates product determinism |
| Ignoring inactive topics inconsistently | Plans diverge from traversal helpers |

## Future Improvements

- Richer rebalancing when mastery or burnout signals change.
- Clearer week-level explainability in the UI (trace to service outputs).
- Stronger tests for V2 section-weighted distribution vs V1 topic weights.

**See also:** [missions.md](missions.md), [readiness.md](readiness.md), [ADR-001](../architecture/ADR-001-service-layer.md).
