# V1SP-001A — Learning Lifecycle Completion

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-001A  
**Status:** Implementation complete  
**Date:** 2026-07-17  
**Commit:** `b9340b6` — `feat(lifecycle): complete Version 1 learning lifecycle with Revision (V1SP-001A)`  

---

## Summary

V1SP-001A completes the Version 1 educational lifecycle by recognising syllabus completion and transitioning students into an explicit **Revision** stage.

Before this milestone, students who completed every syllabus topic remained in Learning Mode. Mission generation fell back to `current_stage` (often “Chapter 1”), so daily work incorrectly restarted at Topic 1.

Now the authoritative lifecycle is:

```
Not Started → Learning → Revision
```

**Exam Ready** is reserved for Version 2 and is never assigned.

Revision is not a separate course or navigation module. The student remains in the same application; the objective changes from acquiring syllabus coverage to consolidating for the examination. No Version 2 educational intelligence (spaced repetition engines, Bayesian mastery, adaptive AI, Learning Object Model) was introduced.

---

## Lifecycle

### Authority

`LearningLifecycleService` (`app/services/learning_lifecycle_service.py`) is the single authoritative resolver.

| Stage | Condition |
|---|---|
| Not Started | No active study plan / curriculum |
| Learning | Active plan with at least one incomplete syllabus leaf |
| Revision | Every required syllabus leaf has Study Progress `completed=True` |

Lifecycle stage is **derived** from Study Progress + active study context (DP-001). It is not a competing enum that can drift from coverage truth.

### Persistence (presentation only)

On `StudyPlan`:

- `revision_entered_at` — stamped on first Revision detection (legacy-safe)
- `revision_acknowledged` — one-time celebration dismiss flag

Alembic: `migrations/versions/202607170001_add_revision_lifecycle_fields.py`.

---

## Dashboard

When Revision is active:

- Eyebrow becomes **Revision Workspace** (brand constant `REVISION_WORKSPACE_LABEL`)
- Primary session card becomes **Today's Revision Session**
- Progress card becomes **Revision Progress** with **100%** syllabus complete retained
- “Topics remaining” learning copy is replaced by revision metrics:
  - Topics Completed
  - Revision Sessions
  - Practice Questions Completed
  - Revision Streak
  - Mixed Quiz Attempts
- Missing instrumentation shows an em dash (`—`) — never fabricated activity
- One-time understated acknowledgement:

  > ✓ Syllabus Complete  
  > Congratulations. You have completed the syllabus. Your focus is now revision and examination readiness.  
  > You have now entered Revision Mode.

Dismiss via `POST /dashboard/revision/acknowledge`.

No new navigation items. No separate Revision module.

---

## Missions

`PlanningService.generate_today_mission` resolves lifecycle before generation.

### Learning (unchanged)

Today’s mission follows Current Learning Topic (IA-004 Learning Mode).

### Revision

Deterministic rotation by calendar date ordinal across five kinds:

1. Complete 20 practice questions  
2. Attempt one mixed-topic quiz  
3. Review weakest topic (from observed TopicProgress; else generic completed-topic wording)  
4. Recall important formulae  
5. Complete one timed practice session  

Unfinished Learning Mode missions are replaced when the student enters Revision. Completed missions are preserved. Mission titles never fall back to Topic 1 / `current_stage` learning copy.

Mission completion in Revision increments `revision_count` / `last_reviewed` when a topic is identifiable; it does **not** advance Study Progress coverage or invent mastery.

---

## Student Digital Twin

The Twin model was not redesigned.

Deterministic recommendation consumers (`RecommendationService`, advisory `MissionOptimizer` progression slot) switch behaviour when lifecycle is Revision:

- Suppress unread-topic / syllabus-progression recommendations
- Prefer revision consolidation activities (weak completed topic, mixed practice, formulae, timed practice)
- No adaptive AI or opaque scoring

---

## Migration

No manual data migration is required.

Existing students who already completed every syllabus leaf enter Revision automatically on first `LearningLifecycleService.resolve` / dashboard or mission load. `revision_entered_at` is stamped idempotently.

Tests use `create_all()`; production applies Alembic revision `202607170001`.

---

## Tests

### Automated

```bash
python -m pytest tests/test_v1sp001a_learning_lifecycle.py -v
python -m pytest tests/test_ia004_truthful_learning_progress.py -q
```

`tests/test_v1sp001a_learning_lifecycle.py` covers:

- Lifecycle transitions (Not Started / Learning / Revision)
- Syllabus completion detection
- Revision mission generation (no Topic 1 restart)
- Learning regression (incomplete students unchanged)
- Deterministic revision mission kinds
- Replacement of unfinished learning missions
- Recommendation changes in Revision
- Legacy completed-student auto-transition
- Acknowledgement dismiss
- Progress retained at 100%
- Dashboard Revision Workspace rendering
- Honest metrics (no fabricated activity)
- Edge cases (idempotency, outside week window, select-topic None)

### Manual

1. Complete final syllabus topic → dashboard shows Revision Workspace + acknowledgement  
2. Confirm today’s mission title starts with `Revision:` and does not name Topic 1  
3. Dismiss acknowledgement → does not reappear  
4. Incomplete student still sees Learning Workspace and Current Learning Topic missions  

---

## Known Limitations

- Exam Ready lifecycle is intentionally unimplemented (Version 2)
- Spaced repetition scheduling, Bayesian mastery, and adaptive interruption remain out of scope
- Practice-question and mixed-quiz metrics depend on recorded Study Attempts / mission titles; absent data shows `—`
- Revision mission “practice questions” / “quiz” are study prompts (same honesty model as Learning Mode session prompts), not a new scored assessment engine
- Educational Intelligence Twin-first dashboard flags remain optional; legacy RecommendationService path is lifecycle-aware

---

## Files Created

- `app/services/learning_lifecycle_service.py`
- `migrations/versions/202607170001_add_revision_lifecycle_fields.py`
- `tests/test_v1sp001a_learning_lifecycle.py`
- `knowledge/releases/V1SP-001A_LEARNING_LIFECYCLE_COMPLETION.md` (this file)

## Files Modified

- `app/models/study_plan.py` — revision presentation fields
- `app/brand_identity.py` — `REVISION_WORKSPACE_LABEL`
- `app/__init__.py` — inject revision workspace label
- `app/services/planning_service.py` — revision mission generation / replace learning missions
- `app/services/recommendation_service.py` — revision recommendation path
- `app/services/mission_optimizer.py` — no Topic 1 progression in Revision
- `app/services/educational_explainability_service.py` — revision mission narrative
- `app/services/study_session_service.py` — revision session copy
- `app/dashboard/routes.py` — lifecycle context + acknowledge endpoint
- `app/mission/routes.py` — lifecycle-aware progress + workspace context
- `app/templates/dashboard/index.html` — Revision Workspace UI
- `app/templates/mission/index.html` — Revision session identity

## Migration Impact

Additive Alembic revision `202607170001` on `study_plans`:

- `revision_entered_at` (nullable DateTime)
- `revision_acknowledged` (Boolean, default false)

No educational evidence or Twin schema changes. No destructive operations.

## Architecture Compliance

- Layering preserved: routes → services → models; no mission maths in templates
- Curriculum V1/V2 traversal unchanged (`CurriculumService` remains authority)
- Learning Mode behaviour for incomplete students preserved (IA-004)
- Constitution Article VI Revision Mode activated only when syllabus completion warrants it and is disclosed as Revision
- No Version 2 intelligence introduced

## Technical Debt

- Dual mission stacks (product PlanningService vs optional EI Mission path) remain; EI path was not redesigned for Revision
- Pre-existing ruff line-length noise in older planning/recommendation modules untouched

## Acceptance Criteria

| Criterion | Status |
|---|---|
| Students never restart Topic 1 after completing the syllabus | Met |
| Revision becomes the active lifecycle state | Met |
| Dashboard transitions into Revision Workspace | Met |
| Revision missions replace learning missions | Met |
| Progress remains at 100% | Met |
| Existing completed students migrate automatically | Met |
| No regression for students still studying | Met |
| No Version 2 educational intelligence introduced | Met |

---

*End of V1SP-001A Learning Lifecycle Completion report.*
