# EP-001.3 — Implementation Plan

**Milestone:** EP-001.3 — Readiness Intelligence  
**Phase:** 4 — Implementation Plan

---

## Goals

1. Make Readiness Intelligence a **consumer** of EP-001.1 `CanonicalLearnerState` and EP-001.2 planner outputs.
2. Extend existing Runtime A `ReadinessService` — **no parallel readiness engine**.
3. Produce from Canonical Learner State (+ optional daily plan):
   - readiness score
   - confidence level
   - strongest areas
   - weakest areas
   - readiness drivers
   - recommended next actions
4. Never duplicate Twin learner state or Planner scheduling ownership.

---

## Non-goals

- Redesign Twin / Foundation / Planner
- Change `get_overall_readiness` internals to call Foundation (collector recursion)
- Flip Digital Twin Authority ON
- Rewrite RecommendationService, Epic aggregation, V2 estimator, or OS ExamReadiness
- Alembic migrations
- Fabricate mock performance

---

## Work packages

### WP1 — Documentation

Discovery + existing review + gap + plan + README under this folder.

### WP2 — Readiness intelligence contracts

Package: `app/infrastructure/adapters/readiness_intelligence/`

| Module | Responsibility |
|---|---|
| `contracts.py` | Immutable DTOs: inputs projection + `ReadinessIntelligenceAssessment` |
| `consumer.py` | Map `CanonicalLearnerState` (+ optional planner dict) → intelligence inputs |
| `assessment.py` | Assemble score / confidence / areas / drivers / next actions |
| `__init__.py` | Public exports |

### WP3 — Extend ReadinessService

- `ReadinessService.build_readiness_intelligence(user_id, *, foundation=..., daily_plan=...)`  
  - When Twin Foundation enabled → assemble CLS → optional planner plan → assessment  
  - When Twin OFF / unavailable → return `None` (legacy getters unchanged)
- Do not alter `get_overall_readiness` / collector contracts

### WP4 — Tests

- Consumer unit: pass-through, unavailable, determinism
- Assessment unit: score reuse, confidence bands, areas, drivers, actions
- ReadinessService Twin flag isolation

### WP5 — Flags / docs

Reuse `KWALITEC_DIGITAL_TWIN` (no new readiness flag). Document in `.env.example` + subsystem note + Twin architecture note.

---

## Score / confidence rules (binding)

| Output | Rule |
|---|---|
| Score | Prefer CLS `study_state.readiness_overall.score` (Runtime A pass-through). If absent, compose Coverage/Mastery/Review from CLS progress/mastery/mission using the **same** 50/30/20 weights — never invent a third formula. |
| Confidence | Deterministic band from evidence attempt count, mastery topic coverage, and mission history density (`very_low` → `high`). |
| Areas | Top/bottom CLS mastery topics with scores (deterministic sort). |
| Drivers | Named contributions: coverage, mastery, review/mission, behaviour, consistency, streaks, time pressure — each with source tag. |
| Next actions | From planner `today_missions` / `revision_priorities` when provided; else empty with limitation code. |

---

## Success criteria mapping

| Criterion | How met |
|---|---|
| Consume Canonical Learner State | Consumer projects CLS → intelligence inputs |
| Consume Planner outputs | Optional daily plan → next actions |
| Extend existing readiness | Changes in `ReadinessService` + thin consumer |
| No parallel readiness architecture | Consumer is projection/assembly only |
| Twin owns state; Planner owns planning; Readiness owns evaluation | Architecture docs + code boundaries |
