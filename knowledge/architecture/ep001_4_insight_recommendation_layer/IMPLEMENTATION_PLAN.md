# EP-001.4 — Implementation Plan

**Milestone:** EP-001.4 — Insight & Recommendation Layer  
**Phase:** 4 — Implementation Plan

---

## Goals

1. Make the Insight & Recommendation Layer a **presentation consumer** of EP-001.1 `CanonicalLearnerState`, EP-001.2 planner outputs, and EP-001.3 readiness intelligence.
2. Extend existing Runtime A `RecommendationService` — **no parallel recommendation engine**.
3. Produce student-facing guidance:
   - today's key focus
   - strongest area
   - greatest risk
   - recommended next action
   - workload explanation
   - readiness explanation
   - motivational progress summary
4. Never duplicate Twin learner state, Planner scheduling, or Readiness evaluation.

---

## Non-goals

- Redesign Twin / Foundation / Planner / Readiness
- Rewrite `generate_recommendations` ranking rules
- Flip Digital Twin Authority ON
- Dashboard / Student Home HTTP cutover (additive API only)
- Promote EI / OS / V2 / Founder recommendation stacks
- Alembic migrations
- Fabricate mock performance

---

## Work packages

### WP1 — Documentation

Discovery + existing review + gap + plan + README under this folder.

### WP2 — Insight contracts

Package: `app/infrastructure/adapters/insight_recommendation/`

| Module | Responsibility |
|---|---|
| `contracts.py` | Immutable DTOs: inputs projection + `StudyInsightGuidance` |
| `consumer.py` | Map CLS + optional planner dict + optional readiness dict → insight inputs |
| `assembler.py` | Compose student-facing guidance strings (communication only) |
| `__init__.py` | Public exports |

### WP3 — Extend RecommendationService

- `RecommendationService.build_study_insights(user_id, *, foundation=..., daily_plan=..., readiness_intelligence=...)`  
  - When Twin Foundation enabled → assemble CLS → resolve planner + readiness → guidance  
  - When Twin OFF / unavailable → return `None` (legacy `generate_recommendations` unchanged)
- Do not alter ranking engine behaviour

### WP4 — Tests

- Consumer unit: pass-through, unavailable, determinism
- Assembler unit: each guidance field sourced from Twin/Planner/Readiness
- RecommendationService Twin flag isolation

### WP5 — Flags / docs

Reuse `KWALITEC_DIGITAL_TWIN` (no new insight flag). Document in `.env.example` + Twin architecture note + subsystem readiness/recommendations adjacency.

---

## Composition rules (binding)

| Output | Source rule |
|---|---|
| Today's key focus | Planner `today_missions[0]` title/reason; else first revision priority; else readiness next action |
| Strongest area | Readiness `strongest_areas[0]` (topic + reason) |
| Greatest risk | Readiness `weakest_areas[0]` (topic + reason) |
| Recommended next action | Readiness `recommended_next_actions[0]`; else planner mission slot |
| Workload explanation | Planner `recommended_workload` minutes + rationale |
| Readiness explanation | Readiness score + confidence + up to two drivers |
| Motivational progress | CLS streaks + mission completion + lifecycle stage — observational language only |

Missing upstream data → empty guidance field + limitation code (never invent).

---

## Success criteria mapping

| Criterion | How met |
|---|---|
| Consume Canonical Learner State | Consumer projects CLS → insight inputs |
| Consume Planner outputs | Optional daily plan → focus / workload / next action fallback |
| Consume Readiness Intelligence | Optional assessment → strongest / risk / readiness / next action |
| No new recommendation engine | Assembler is presentation composition only |
| Twin owns state; Planner owns planning; Readiness owns evaluation; Insight owns communication | Architecture docs + code boundaries |
