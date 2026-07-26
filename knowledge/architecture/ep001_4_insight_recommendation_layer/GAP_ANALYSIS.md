# EP-001.4 — Gap Analysis

**Milestone:** EP-001.4 — Insight & Recommendation Layer  
**Phase:** 3 — Gap Analysis  
**Date:** 2026-07-26

Compare current recommendation / advice surfaces vs Insight Layer success criteria (compose Twin + Planner + Readiness; own communication only; no new intelligence sources).

---

## 1. Capability matrix

| Capability | Status | Evidence | Gap |
|---|---|---|---|
| Today's key focus | **Partial** | Home/dashboard titles from rec or mission | Not composed from planner mission slots when Twin ON |
| Strongest area | **Partial** | ORM + EP-001.3 areas | No student guidance string from readiness intelligence |
| Greatest risk | **Partial** | Weak topics / Weak Topic recs | No unified risk insight from readiness weakest areas |
| Recommended next action | **Partial** | Rec engine + readiness actions + mission next_action | Fragmented; should cite planner/readiness when Twin ON |
| Workload explanation | **Partial** | Planner rationale API; KPI labels | Not packaged in insight guidance |
| Readiness explanation | **Partial** | Explainability over legacy %; EP-001.3 drivers unused | Need communication over intelligence assessment |
| Motivational progress summary | **Partial** | Tips / streaks / weekly report | Need one CLS-grounded progress summary |
| Consume CLS | **Missing** for insight packaging | Foundation exists | Primary gap |
| Consume Planner | **Missing** for insight packaging | Daily plan exists | Primary gap |
| Consume Readiness Intelligence | **Missing** for insight packaging | Assessment exists | Primary gap |
| No new recommendation engine | **Constraint** | Multiple parallel engines already | Must compose, not recalculate |
| Ownership preserved | **Constraint** | Twin / Planner / Readiness SoTs | Insight owns communication only |

---

## 2. Duplicated calculations (must not add another)

| Calculation | Locations | Rule for EP-001.4 |
|---|---|---|
| Recommendation ranking | `RecommendationService`, EI Decision, OS engines, V2 Twin | Insight layer **does not** re-rank; may cite planner/readiness next actions |
| Readiness score / confidence | `ReadinessService` / EP-001.3 | Insight **explains** assessment fields; never invents score/confidence |
| Workload minutes | Planner `recommended_workload` | Insight **explains** rationale; never recomputes capacity |
| Strongest / weakest areas | ORM getters vs EP-001.3 areas | Prefer readiness intelligence areas when Twin ON |

---

## 3. Duplicated state

| State | Owners today | Rule |
|---|---|---|
| Learner state | Twin Foundation (claims); Runtime A (facts) | Insight must not invent mastery/streaks/mocks |
| Planning slots | Planner | Insight must not re-plan |
| Readiness evaluation | Readiness | Insight must not re-evaluate |
| Advice copy | Fragmented narrators | Consolidate packaging in insight consumer; leave legacy narrators for now |

---

## 4. Consolidation opportunities

1. **Extend** `RecommendationService` with `build_study_insights` — Twin-gated, fail-open to `None` (legacy `generate_recommendations` unchanged).
2. **Add** thin infrastructure consumer (`insight_recommendation`) projecting CLS + daily plan dict + readiness intelligence dict → guidance DTOs.
3. **Compose** student-facing fields from existing intelligence only:
   - focus ← planner `today_missions[0]` (else revision priority / readiness next action)
   - strongest ← readiness `strongest_areas[0]`
   - greatest risk ← readiness `weakest_areas[0]`
   - next action ← readiness `recommended_next_actions[0]` else planner mission
   - workload explanation ← planner `recommended_workload`
   - readiness explanation ← score + confidence + top drivers
   - motivational progress ← streaks + mission completion + lifecycle from CLS
4. **Leave** `generate_recommendations` and dashboard HTTP cutover for a later soak (mirror EP-001.3).
5. **Leave** EI / OS / V2 / Founder stacks untouched.

---

## 5. What must not be done

| Anti-goal | Why |
|---|---|
| New parallel recommendation engine replacing `RecommendationService` | Violates “no parallel recommendation architecture” |
| New learner-state or readiness formula inside insight | Twin / Readiness ownership |
| New planner inside insight | Planner ownership |
| Averaging or inventing scores for “insight quality” | Forbidden new intelligence |
| Fabricate mock performance | Foundation marks unavailable |
| Force dashboard cutover this milestone | Out of scope (additive API first) |
| Promote Education OS / EI Decision as Runtime A insight authority | Parallel non-authority |

---

## 6. Recommendation

Implement EP-001.4 by extending Runtime A `RecommendationService` with a Twin-gated insight API that **consumes** EP-001.1 Canonical Learner State, EP-001.2 planner outputs, and EP-001.3 readiness intelligence, packaging personalised study guidance without introducing a duplicate recommendation engine or moving ownership away from Twin, Planner, or Readiness.
