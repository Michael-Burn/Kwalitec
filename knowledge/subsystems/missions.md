# Daily Missions

## Purpose

Daily missions reduce the student’s decision load: given an active study plan, progress, and constraints, Kwalitec produces a prioritised set of tasks for the session (“what should I do today?”).

Owners:

- `MissionService` — mission lifecycle, persistence, completion
- `MissionOptimizer` — task prioritisation from urgency, readiness, and workload
- `mission` blueprint — `/missions` HTTP surface
- Related: `BurnoutMonitor` (intensity flags), adaptive learning for review pressure

Missions are **optimizer outputs**, not a second syllabus. Topic identity and syllabus order still come from the curriculum layer.

## Responsibilities

| Concern | Owner |
|---|---|
| Create / fetch / complete missions and tasks | `MissionService` |
| Rank candidate tasks for a day | `MissionOptimizer` |
| Auth, forms, mission UI | `mission` blueprint + `mission.js` |
| Canonical topic universe | `CurriculumService` |
| Plan context | `StudyPlanService` / active plan |

Prioritisation may rank tasks by urgency or mastery need **after** resolving topics through canonical helpers — ranking is not a substitute for syllabus traversal ([ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)).

## Dependencies

```
mission blueprint
        ↓
MissionService / MissionOptimizer
        ↓
StudyPlan + TopicProgress + readiness/adaptive signals
        ↓
CurriculumService (topic identity / next incomplete)
        ↓
ORM Mission / MissionTask
```

```
Active Study Plan ──┐
Progress / mastery ─┼──▶ MissionOptimizer ──▶ Mission + MissionTasks
Burnout / time ─────┘           │
                                ▼
                     MissionService.persist / complete
```

## Data Flow

1. User opens missions (authenticated).
2. Service loads active plan and learner state.
3. Candidates derived from plan + incomplete topics (canonical order / next incomplete).
4. Optimizer assigns priority and builds tasks.
5. User completes tasks → progress / attempts update → future missions and readiness shift.

## Extension Points

- New task types: extend optimizer + `MissionTask` usage carefully with migrations if schema changes.
- New priority signals: add explicit factors in `MissionOptimizer`; keep them logged/explainable where shown in UI.
- Client interactions: keep `app/static/js/mission.js` progressive; core completion must work server-side.

## Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Generating missions from unordered topic queries | Skips syllabus sequence / V2 sections |
| Duplicating “next topic” logic outside `CurriculumService` | Drift from planning and readiness |
| Putting optimizer math in routes | Violates thin blueprints ([ADR-002](../architecture/ADR-002-blueprint-architecture.md)) |
| Ignoring burnout signals entirely when extending workload | Unsustainable intensity |
| Non-deterministic random task picks | Breaks reproducibility |

## Future Improvements

- Stronger explainability strings per task (“why this mission”).
- Closer integration with recommendation accept/dismiss history.
- V2-aware section focus modes without breaking V1 mission generation.

**See also:** [study-planning.md](study-planning.md), [readiness.md](readiness.md), [ADR-001](../architecture/ADR-001-service-layer.md).
