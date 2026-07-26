# EP-001.5 — Authority Matrix

**Milestone:** EP-001.5  
**Review area:** Canonical ownership  
**Date:** 2026-07-26

Legend: **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Canonical ownership matrix

| Concern | Canonical owner | Location | Competing stacks (non-authority) | Drift? |
|---|---|---|---|---|
| **Curriculum / syllabus structure** | Curriculum Engine + `CurriculumService` | `app/curriculum/`, `CurriculumService` | None for ordering | **None** |
| **Runtime facts (writes)** | Runtime A SQL + services | attempts, missions, `TopicProgress`, StudyPlan | Bridges may read/project | **None** |
| **Learner-state read model (Runtime A synthesis)** | EP-001.1 `CanonicalLearnerState` / Foundation | `digital_twin/foundation.py` | Epic Twin, V2 student_twin, EOS Twin, Experience demo | **Controlled** — EP-001 extended MS-004; no fourth stack |
| **Constitutional learner-state aggregate (belief structure)** | Epic `app/domain/twin.DigitalTwin` | `app/domain/twin/` | Reference vocabulary; not production writer | **None** (by design) |
| **Planning outputs** | `PlanningService` + EP-001.2 projections | `planning_service.py`, `adaptive_study_planner/` | OS / Journey / Strategy planners | **None** — not promoted |
| **Readiness evaluation** | `ReadinessService` + EP-001.3 | `readiness_service.py`, `readiness_intelligence/` | Epic / V2 / OS readiness | **None** — not promoted |
| **Communication / student guidance** | `RecommendationService` + EP-001.4 | `recommendation_service.py`, `insight_recommendation/` | `EducationalExplainabilityService`, EI/OS/V2 recommenders | **Partial** — dual presentation paths |
| **Experience TwinPort UX** | `ExperienceTwinAdapter` (default) | `student_twin/experience_adapter.py` | Foundation Authority when `KWALITEC_DIGITAL_TWIN_AUTHORITY=1` | **None** — gated |

---

## 2. Ownership rules encoded in code

**E:** Service docstrings bind ownership:

- `PlanningService`: Twin owns mastery/progress/behaviour/streaks; service owns planning outputs and mission persistence.
- `ReadinessService`: consumes Canonical state; does not invent learner state; does not alter `get_overall_readiness`.
- `RecommendationService`: communication only; does not invent state, plan missions, or recalculate readiness.

**E:** Consumer packages are projection-only (`consumer.py` modules across EP-001.2–4).

**C:** Ownership is explicit and consistent across EP-001.1–4.

---

## 3. Authority drift findings

| Finding ID | Severity | Description |
|---|---|---|
| AD-01 | Low | Mock performance remains unavailable on Foundation — honest gap, not ownership drift |
| AD-02 | Medium | Production HTTP still treats legacy Runtime A getters as UX authority while Twin-gated `build_*` APIs exist unused — **authority split by surface**, not by domain invention |
| AD-03 | Medium | `EducationalExplainabilityService` remains a parallel ORM-backed presentation path beside EP-001.4 |
| AD-04 | Low | Epic Twin write pipeline is still not the sole production write path for learner beliefs (pre-existing; EP-001 did not claim to fix this) |
| AD-05 | Info | V2 / EOS Twin stacks remain importable — documented as non-authority; no drift into EP-001 DI |

**C:** No ownership *invention* drift inside EP-001. Residual drift is **surface cutover lag** (AD-02, AD-03) and pre-existing multi-stack coexistence (AD-04, AD-05).

---

## 4. Authority cutover map

| Surface | Current authority | Twin-gated alternative | Flag |
|---|---|---|---|
| Dashboard readiness | `get_overall_readiness` | `build_readiness_intelligence` | Twin ON (API only; no HTTP wiring) |
| Dashboard mission | `generate_today_mission` | `build_daily_study_plan` (+ optional MissionOptimizer) | Twin ON |
| Dashboard recommendations | `generate_recommendations` | `build_study_insights` | Twin ON |
| Experience StudentTwinPort | `ExperienceTwinAdapter` | `StudentTwinFoundationAuthorityPort` | Twin + Authority ON |
| Adaptive enrichment | Runtime A collectors | + `TwinInputAdapter` attachment | Twin ON |

**R:** Do not flip Experience Authority or HTTP cutover without soak evidence. Prefer sequenced cutover milestones (see Updated Recommendations).
