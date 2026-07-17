# V1SP-003 — Performance Optimisation

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-003  
**Status:** Implementation complete  
**Date:** 2026-07-17  
**Nature:** Measured performance optimisation only — no new product functionality or UI changes  
**Build identity:** Product `1.0.0` · Internal Alpha chrome **Build RC2**  
**Commit:** `1ee8a13` — `perf: optimise Version 1 hot paths from measured baselines (V1SP-003)`

---

## Summary

V1SP-003 improves Version 1 responsiveness using a profiled Alpha-scale dataset (12 learners, 30 leaf topics, 20 missions/user, 4 check-ins/user). Baseline metrics were captured before any code change; every optimisation maps to a measured hotspot.

Largest wins:

| Path | Baseline queries | After queries | Change |
|---|---:|---:|---:|
| Student Dashboard render | 397 | 280 | **−29.5%** |
| Analytics compose | 154 | 32 | **−79.2%** |
| Analytics readiness trend (12 weeks) | 36 | 3 | **−91.7%** |
| Operational Health revision-idle rule | 4 | 1 | **−75%** (N+1 removed) |
| First-party CSS | 84 972 B | 63 514 B | **−25.3%** |
| First-party JS | 21 870 B | 20 592 B | **−5.8%** |

Educational formulas, Founder workflows, accessibility affordances, and Version 1 feature surface are unchanged. No educational-data caching was introduced.

Raw measurement artefacts: `knowledge/releases/v1sp003_baseline_metrics.json`, `knowledge/releases/v1sp003_after_metrics.json`.

---

## Baseline

Profiling harness: `tests/perf_v1sp003_harness.py` (wall-clock median of 3 iterations + SQLAlchemy statement counts).

### Application (median)

| Path | ms | Queries |
|---|---:|---:|
| Dashboard render | 75.95 | 397 |
| Founder Overview | 9.10 | 46 |
| Operational Health | 8.42 | 28 |
| Study Session start | 1.75 | 4 |
| Analytics compose | 32.37 | 154 |

### Database findings

| Finding | Evidence |
|---|---|
| Dashboard multi-service fan-out | 397 statements; unused widgets still fetched (`daily_briefing`, `decision_journal`, `learning_snapshot`, `balanced_mission`) |
| Readiness leaf-topic rescans | `get_overall_readiness` called `_get_leaf_topics()` four times |
| Mission completion loaded into Python | `get_review_completion_rate` used `.all()` then counted |
| Analytics 12-week loops | `get_readiness_over_time` issued **36** queries (topics + progress + missions × 12) |
| Operational Health revision N+1 | `_revision_without_sessions_count` = 1 plan query + 1 count **per** revision plan |
| Missing indexes | No indexes on `topic_progress`, `study_attempts(user_id, study_date)`, `missions(status, mission_date)`, or `study_plans(active, archived)` |

### Static assets (baseline)

| Bundle | Bytes |
|---|---:|
| First-party CSS (`app/static/css`) | 84 972 |
| First-party JS (`app/static/js`) | 21 870 |
| Brand pack (`app/static/branding`) | 1 739 297 |

Brand rasters were already reduced in V1SP-001B (~5.3 MB → ~2.1 MB). Further PNG palette quantisation deferred (already optimally zlib-compressed).

### Templates

Dashboard template does not reference `daily_briefing`, `decision_journal`, `decision_summary`, `learning_snapshot`, or `balanced_mission` — confirmed by template search before removal. Burnout notice and core KPIs remain.

---

## Optimisations

| # | Change | Why (evidence) |
|---|---|---|
| 1 | Removed unused Dashboard service calls and template kwargs | Dead work on every Dashboard render (RC2 M-14 / PTP-004 follow-up) |
| 2 | Batched leaf progress inside `ReadinessService.get_overall_readiness` | Eliminated repeated Topic / TopicProgress scans |
| 3 | `get_review_completion_rate` → SQL `GROUP BY status` | Avoid loading all Mission rows |
| 4 | `get_review_backlog` → single filtered fetch + in-memory buckets | 3 COUNT queries → 1 |
| 5 | Analytics time-series: load topics/progress/missions/attempts **once**, bucket in memory | 12-week loops were O(weeks) queries |
| 6 | Operational Health revision-idle → single `NOT EXISTS` aggregate | True N+1 under revision cohort growth |
| 7 | Consecutive negative sentiment → `ROW_NUMBER()` window (latest 2/user) | Full-table ordered pull bounded to two rows per user |
| 8 | Founder Overview recent feedback → `joinedload(User)` | Removed per-row `User` lookups |
| 9 | `MissionService.get_today_mission` → `selectinload(Mission.tasks)` | Avoid lazy task loads during completion repair |
| 10 | Alembic `202607170003` + matching model `__table_args__` indexes | Support OH / analytics / readiness filters |
| 11 | Minify first-party CSS/JS (comments + whitespace; calc/strings preserved) | Payload reduction without CDN/UI changes |

---

## Before / After

Seed held constant. Medians from harness (3 iterations).

| Path | Before ms | After ms | Before q | After q | Query Δ |
|---|---:|---:|---:|---:|---:|
| Dashboard render | 75.95 | 53.76 | 397 | 280 | −29.5% |
| Founder Overview | 9.10 | 8.32 | 46 | 38 | −17.4% |
| Operational Health | 8.42 | 4.72 | 28 | 25 | −10.7% |
| Study Session start | 1.75 | 1.51 | 4 | 4 | 0% (already thin) |
| Analytics compose | 32.37 | 7.25 | 154 | 32 | −79.2% |
| Analytics readiness trend | 8.66 | 0.87 | 36 | 3 | −91.7% |
| OH revision idle | 0.54 | 0.25 | 4 | 1 | −75.0% |

| Asset class | Before | After | Δ |
|---|---:|---:|---:|
| CSS | 84 972 B | 63 514 B | −25.3% |
| JS | 21 870 B | 20 592 B | −5.8% |
| Brand | 1 739 297 B | 1 739 297 B | 0% (already optimised in 001B) |

Wall-clock gains on SQLite/CI are secondary to query-count reductions; query budgets are the durable Alpha signal as cohort size grows.

---

## Database

### Query improvements

- Dashboard: removed five unused service invocations; readiness/review paths batched.
- Analytics: constant query count for readiness trend regardless of week window (asserted ≤ 5).
- Operational Health: revision-idle is one statement; sentiment uses window ranking.

### Indexes added (`202607170003`)

| Index | Columns |
|---|---|
| `ix_missions_status_mission_date` | `missions(status, mission_date)` |
| `ix_study_attempts_user_study_date` | `study_attempts(user_id, study_date)` |
| `ix_study_plans_active_archived` | `study_plans(active, archived)` |
| `ix_study_plans_user_active_archived` | `study_plans(user_id, active, archived)` |
| `ix_topic_progress_user_topic` | `topic_progress(user_id, topic_id)` |
| `ix_topic_progress_user_next_review` | `topic_progress(user_id, next_review_date)` |
| `ix_topic_progress_user_stage` | `topic_progress(user_id, current_stage)` |
| `ix_mission_tasks_mission_id` | `mission_tasks(mission_id)` |

### Aggregations

Mission status tallies and revision-idle detection now use SQL aggregates / `EXISTS` rather than Python loops over ORM collections.

---

## Static Assets

| File | Before → After |
|---|---|
| `app/static/css/app.css` | 75 491 → 54 112 (−28.3%) |
| `app/static/css/wizard.css` | 9 481 → 9 402 |
| `app/founder/dashboard/static/css/founder_dashboard.css` | 10 244 → 8 206 |
| `app/static/js/*.js` + founder JS | modest comment/blank-line trim |

Static cache headers from V1SP-001B (`public, max-age=1y, immutable` + `v=` fingerprint) remain in force. SVG logos remain the runtime canonical brand format.

---

## Regression Testing

### Automated

```bash
python -m pytest tests/test_v1sp003_performance.py -q
python -m pytest tests/test_v1sp001c_operational_health.py tests/test_v1sp001a_learning_lifecycle.py tests/test_v1sp001b_operational_fixes.py -q
python -m pytest tests/test_readiness_aggregation.py tests/test_founder_dashboard.py tests/test_services.py -k "readiness or analytics or review_completion or learning_snapshot or decision_journal or dashboard" -q
```

Results: **8/8** V1SP-003 tests passed; **63** V1SP-001A/B/C tests passed; **61** readiness/founder/service subset passed.

Coverage in `tests/test_v1sp003_performance.py`:

- query budgets (readiness trend, revision idle, overall readiness)
- Dashboard still renders without dead widgets
- CSS/JS size budgets
- index declarations present
- educational parity for review-completion rates and negative-sentiment rule

### Manual checklist

| Check | Expected |
|---|---|
| Authentication login/logout | Unchanged |
| Learning Workspace / Dashboard | Same layout; burnout notice still shows when applicable |
| Study Session start | Remains fast; status → In Progress |
| Revision lifecycle | OH + dashboard revision behaviour unchanged |
| Analytics charts | Same series length (12 weeks); values preserved |
| Founder Overview | Recent feedback labels still resolve to emails |
| Operational Health | Same rule IDs and card semantics |
| Vision Journal / Feedback / Internal Alpha | Untouched workflows |
| Branding / Navigation | SVG wordmark; static `Cache-Control` + fingerprint |
| Accessibility | Focus rings, loading patterns, and reduced-motion hooks retained |

---

## Remaining Opportunities

Explicitly deferred to Version 2 (non-essential for RC2):

1. Further Dashboard coalescing of overlapping readiness / curriculum / recommendation paths while Educational Orchestrator is on (still ~280 queries).
2. Founder Participants page N+1 (RC2 M-9) — out of V1SP-003 hot-path set.
3. Operational State filesystem scan cost outside `TESTING`.
4. PNG palette quantisation / WebP variants for brand rasters.
5. Vendoring Bootstrap / Chart.js off CDN.
6. Request-scoped leaf-topic cache across multiple services in one HTTP request.
7. CSP nonces + moving remaining inline scripts to static files (security follow-up, not perf-primary).

---

## Files Created

- `migrations/versions/202607170003_add_v1sp003_performance_indexes.py`
- `tests/perf_v1sp003_harness.py`
- `tests/test_v1sp003_performance.py`
- `knowledge/releases/v1sp003_baseline_metrics.json`
- `knowledge/releases/v1sp003_after_metrics.json`
- `knowledge/releases/V1SP-003_PERFORMANCE_OPTIMISATION.md`

## Files Modified

- `app/dashboard/routes.py`
- `app/services/readiness_service.py`
- `app/services/analytics_service.py`
- `app/services/mission_service.py`
- `app/founder/dashboard/services/operational_health_service.py`
- `app/founder/dashboard/services/command_centre_service.py`
- `app/models/mission.py`
- `app/models/topic_progress.py`
- `app/models/learning.py`
- `app/models/study_plan.py`
- `app/static/css/app.css`
- `app/static/css/wizard.css`
- `app/static/js/app.js`
- `app/static/js/mission.js`
- `app/static/js/study_session.js`
- `app/static/js/theme.js`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/founder/dashboard/static/js/founder_dashboard.js`

## Migration Impact

Additive index-only Alembic revision `202607170003` (revises `202607170002`). No column changes. Safe to apply on Internal Alpha SQLite/Postgres. `db.create_all()` in tests picks up matching model `__table_args__`.

## Architecture Compliance

- Layering preserved (routes → services → models).
- No educational formula changes; readiness weights and OH rule definitions unchanged.
- Curriculum V1/V2 traversal untouched.
- No stale educational caches introduced.

## Technical Debt

Dashboard remains a sequential multi-service composition (~280 queries with orchestrator fallback). Acceptable for Alpha cohort size; Version 2 should introduce a request-scoped progress snapshot rather than further ad-hoc removals.

## Known Limitations

- Benchmarks use SQLite + Flask test client; production Postgres timings will differ, but relative query reductions transfer.
- Study Session start was already lean (4 queries) — no further gain targeted.
- Brand raster byte size unchanged in this milestone (001B already met resize budgets).

---

*End of V1SP-003 Performance Optimisation report.*
