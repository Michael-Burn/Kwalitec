# Analytics

## Purpose

Analytics present learning performance and progress aggregations so students (and eventually coaches/admins) can see patterns: activity, mastery trends, coverage, and related dashboard widgets. Aggregation logic lives in `AnalyticsService`; HTTP lives in the `analytics` blueprint (`/analytics`) and portions of `dashboard`.

Analytics is a **read-mostly projection** over learning data. It must not become a second source of syllabus truth or a place to reimplement readiness formulas in incompatible ways — prefer calling `ReadinessService` / `CurriculumService` where those domains already own the definition.

## Responsibilities

| Concern | Owner |
|---|---|
| Aggregate charts/tables for analytics views | `AnalyticsService` |
| Exam readiness summaries | `ReadinessService` (consume, don’t fork) |
| Route auth + template rendering | `analytics` / `dashboard` blueprints |
| Underlying events | `LearningService`, attempts, mistakes, progress |

## Dependencies

```
analytics / dashboard blueprints
        ↓
AnalyticsService (+ ReadinessService as needed)
        ↓
StudyAttempt, Mistake, TopicProgress, Mission history, StudyPlan
        ↓
CurriculumService for topic/section labels and canonical sets
```

- **Depends on:** persisted learning events and curriculum metadata.
- **Does not own:** curriculum import, plan distribution, or auth policy.
- **Should not:** issue writes that change pedagogical state except where explicitly designed (prefer learning/mission services for writes).

## Data Flow

```
Learning events (attempts, missions, progress)
        → AnalyticsService queries / aggregates
        → optional ReadinessService summary
        → blueprint template context
        → Jinja analytics / dashboard views
```

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│ Attempts /  │────▶│ AnalyticsService │────▶│ Templates   │
│ Progress    │     │ (+ Readiness)    │     │ analytics/* │
└─────────────┘     └────────┬─────────┘     └─────────────┘
                             │
                             ▼
                    CurriculumService
                    (labels, ordered topics)
```

## Extension Points

- New dashboard widgets: add service methods returning plain dicts/dataclasses; keep routes thin.
- New dimensions (e.g. per-section V2 breakdown): use `get_sections` / `get_topics_for_section` rather than custom SQL ordering.
- Export/backup adjacent features may live under `settings`; keep analytics focused on insight, not account management.

## Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Recomputing readiness with a different formula in analytics | Conflicting numbers in UI |
| Grouping by `Topic.order` globally on V2 data | Wrong section chronology |
| Heavy aggregation in Jinja | Untestable; move to service |
| Unscoped queries across users | Security / privacy bug |
| N+1 query patterns in new widgets | Slow analytics pages |

## Future Improvements

- Section-level analytics for V2 curricula.
- Clearer shared DTO between readiness and analytics to guarantee one definition of coverage.
- Performance indexes / pre-aggregation if event volume grows.

**See also:** [readiness.md](readiness.md), [authentication.md](authentication.md), [ADR-002](../architecture/ADR-002-blueprint-architecture.md).
