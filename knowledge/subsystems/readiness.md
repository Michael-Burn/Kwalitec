# Exam Readiness

## Purpose

Exam readiness analytics estimate how prepared a learner is relative to the syllabus, their progress, and time remaining until the exam. Outputs must be **explainable**: coverage, projected pace, and pass-risk style signals should trace to curriculum weights and recorded learning data — not to a black-box score.

Primary owner: `ReadinessService` (with `ReadinessSummary` and related structures). Closely related: `RecommendationService` (next-step suggestions), `AdaptiveLearningService` (mastery / spaced repetition), `LearningService` (attempts and mistakes).

HTTP surface: primarily `analytics` and `dashboard` blueprints consuming service summaries.

## Responsibilities

| Concern | Owner |
|---|---|
| Aggregate readiness metrics for a user/plan/curriculum | `ReadinessService` |
| Mastery and review scheduling inputs | `AdaptiveLearningService` |
| Attempt / mistake records | `LearningService` |
| Explainable “study next” suggestions | `RecommendationService` |
| Syllabus order and coverage denominator | `CurriculumService` canonical traversal |

Readiness must work for **both** V1 (topic weights) and V2 (section weights) without requiring sections globally ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md)).

## Dependencies

```
dashboard / analytics blueprints
        ↓
ReadinessService / RecommendationService
        ↓
TopicProgress, StudyAttempt, Mistake, StudyPlan
        ↓
CurriculumService.get_all_topics_ordered()  (+ sections when V2)
```

- **Depends on:** progress and attempt data, curriculum structure, exam date / plan context.
- **Does not depend on:** external LLM APIs or random sampling in the core path.
- **Must not:** invent a second topic order for “coverage %.”

## Data Flow

```
Canonical topics (CurriculumService)
    + TopicProgress / attempts / mastery
    + time remaining (plan / exam timeline)
        → ReadinessService computes summary
        → RecommendationService may suggest next actions
        → blueprint renders analytics / dashboard widgets
```

Typical signals (conceptual):

| Signal | Grounded in |
|---|---|
| Coverage | Completed vs canonical topic list / weights |
| Pace | Progress vs days remaining |
| Risk / gaps | Low mastery or incomplete high-weight areas |
| Next step | Incomplete topics in canonical order + urgency |

## Extension Points

- New readiness dimensions: add fields on `ReadinessSummary` and compute in `ReadinessService`.
- New recommendation reasons: attach explicit reason codes/strings in `RecommendationService` (Decision Journal may record accept/dismiss).
- Weight handling: branch on V1 topic weights vs V2 section weights inside readiness helpers — do not fork traversal.

## Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Coverage over `Topic.query.all()` unordered | Wrong % and wrong “remaining” list |
| Hard-requiring `Section` rows | Breaks V1 readiness |
| Opaque composite scores without factors | Violates explainability thesis |
| Mixing HTTP session into readiness math | Untestable; layer violation |
| Changing formulas without regression tests | Silent plan/mission mismatch |

## Future Improvements

- Richer section-level readiness views for V2 syllabuses.
- Tighter coupling of burnout monitor signals to readiness pacing advice.
- Expanded Decision Journal linkage for recommendation outcomes.

**See also:** [analytics.md](analytics.md), [study-planning.md](study-planning.md), [ADR-005](../architecture/ADR-005-testing-strategy.md).
