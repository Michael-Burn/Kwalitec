# EP-001.2 — Implementation Plan

**Milestone:** EP-001.2 — Adaptive Study Planner  
**Phase:** 3 — Implementation Plan

---

## Goals

1. Make the Adaptive Study Planner a **consumer** of EP-001.1 `CanonicalLearnerState`.
2. Extend existing Runtime A planning (`PlanningService` / `MissionOptimizer` / capacity) — **no parallel planner**.
3. Produce from Canonical Learner State (+ plan capacity):
   - today's study missions (priority slots)
   - revision priorities
   - topic ordering
   - recommended workload
4. Never duplicate learner state (mastery, streaks, consistency, behaviour).

---

## Non-goals

- Redesign Twin / Foundation
- Replace Mission / TopicProgress write paths
- Flip Digital Twin Authority ON
- Rewrite RecommendationService or OS / Journey planners
- Interrupt Learning Mode with review topics (IA-004 preserved)
- Alembic migrations

---

## Work packages

### WP1 — Documentation

Discovery + gap + plan + README under this folder.

### WP2 — Planner consumer contracts

Package: `app/infrastructure/adapters/adaptive_study_planner/`

| Module | Responsibility |
|---|---|
| `contracts.py` | Immutable DTOs: planner inputs projection + `DailyStudyPlanProjection` |
| `consumer.py` | Map `CanonicalLearnerState` → planner inputs (read-only; never invent) |
| `daily_plan.py` | Assemble daily plan outputs from inputs + available study minutes |
| `__init__.py` | Public exports |

### WP3 — Extend PlanningService

- `PlanningService.build_daily_study_plan(user_id, today=...)`  
  - When Twin Foundation enabled → assemble CLS → consumer → daily plan projection  
  - When Twin OFF / unavailable → return `None` (legacy `generate_today_mission` unchanged)
- Revision weak label: prefer CLS revision priorities when available
- Persist missions still via existing `generate_today_mission` / `MissionService`

### WP4 — Extend MissionOptimizer

Prefer Foundation-derived mastery / progress / review due rows when Twin ON; fall back to AdaptiveLearningService.

### WP5 — Tests

- Consumer unit: pass-through, unavailable, determinism
- Daily plan unit: workload + ordering from fixtures
- PlanningService / MissionOptimizer flag isolation

### WP6 — Flags / docs

Reuse `KWALITEC_DIGITAL_TWIN` (no new planner flag). Document in `.env.example` + subsystem note.

---

## Success criteria mapping

| Criterion | How met |
|---|---|
| Daily study plan from Canonical Learner State | `build_daily_study_plan` via Foundation.assemble |
| Extend existing planner | Changes in `PlanningService` / `MissionOptimizer` + thin consumer |
| No duplicate planning engine | Consumer is projection-only; persistence stays PlanningService |
| No duplicate learner-state models | No mastery/streak math in consumer |
| Twin owns state; Planner owns planning | Architecture docs + code boundaries |
