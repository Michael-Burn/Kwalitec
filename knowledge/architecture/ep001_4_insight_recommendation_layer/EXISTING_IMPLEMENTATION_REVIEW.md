# EP-001.4 — Existing Implementation Review

**Milestone:** EP-001.4 — Insight & Recommendation Layer  
**Phase:** 2 — Existing Implementation Review  
**Date:** 2026-07-26

---

## 1. Review dimensions

| Dimension | Current behaviour | Category |
|---|---|---|
| Today's key focus | Student Home / EOS focus cards from recommendation title or mission title; no Twin+Planner packaged focus | **Partially implemented** |
| Strongest area | ORM `get_strongest_topics` + EP-001.3 `strongest_areas` (API only) | **Partially implemented** |
| Greatest risk / weakest | ORM weak topics + rec Weak Topic rules + EP-001.3 `weakest_areas` (API only) | **Partially implemented** |
| Recommended next action | `RecommendationService` rule engine; readiness `recommended_next_actions` (API only); mission narrative `next_action` | **Partially implemented** |
| Workload explanation | Planner `recommended_workload.rationale` (API only); KPI schedule labels on dashboard | **Partially implemented** |
| Readiness explanation | `EducationalExplainabilityService` over legacy readiness dicts; EP-001.3 drivers unused on HTTP | **Partially implemented** |
| Motivational progress summary | Streak/momentum copy fragmented (EOS composer, tips, weekly report) | **Partially implemented** |
| Unified insight packaging Twin+Planner+Readiness | Does not exist | **Missing** |
| Consume Canonical Learner State for guidance copy | Opaque learning insights exist; not a study-guidance layer | **Missing** |
| Avoid new recommendation formula | Constraint | **Constraint** |

---

## 2. Existing recommendation logic

### 2.1 `RecommendationService` (production authority)

- Deterministic ranked list: Review, Weak Topic, New Topic, Mock, Rest, Revision, Exam Technique.
- Inputs: `ReadinessService` ORM getters, lifecycle, burnout, exam timeline, curriculum next topic.
- **Not** Twin / EP-001.2 / EP-001.3 aware.
- Hosts Decision Journal CRUD for accept/dismiss.

### 2.2 Flag-gated structural EI path

- `DecisionEngine` → `RecommendationEngine` → `RecommendationCardBuilder`.
- Parallel selection logic; default OFF. Must not become EP-001.4 formula authority.

### 2.3 Parallel OS / V2 / Founder engines

- Education OS recommendation engine + home insight cards.
- V2 Twin recommendation service.
- Founder operational recommendations.
- Inventory only for this milestone.

---

## 3. Dashboard insights

| Surface | What students see today |
|---|---|
| `GET /dashboard/` | Legacy recommendation list (+ explainability enrich) **or** EI card; readiness %, weak/strong topics; mission narrative; study tip; burnout; exam timeline |
| `GET /student/` | Bridge recommendation card; coach insight from rec title/explanation |
| `GET /analytics/` | Readiness narratives; weak/strong; weekly highlights / areas for improvement |
| Mission / session | Mission narrative; post-session feedback; optional Twin learning insight strings |

**Finding:** Advice is assembled per-route from legacy services. Twin-gated plan/readiness intelligence are not the student-facing source.

---

## 4. Planner messages

| Output | Status |
|---|---|
| Persisted mission title/copy via `generate_today_mission` | **Already implemented** (ORM) |
| Daily plan `today_missions` / revision reasons | **Already implemented** (API) |
| Workload rationale on student surfaces | **Missing** on HTTP |
| Insight layer citing planner slots as focus/next action | **Missing** |

---

## 5. Readiness summaries

| Output | Status |
|---|---|
| Legacy composite + coverage narratives | **Already implemented** |
| EP-001.3 score / confidence / drivers / areas | **Already implemented** (API) |
| Student-facing readiness explanation from intelligence assessment | **Missing** |

---

## 6. Mission explanations

| Output | Status |
|---|---|
| `EducationalExplainabilityService.build_mission_narrative` | **Already implemented** (presentation) |
| Session feedback / what-next | **Already implemented** |
| Twin+Planner-grounded single next-action insight | **Missing** as unified package |

---

## 7. Categorisation summary

### Already implemented

- Production `RecommendationService` ranking engine
- EIP-003 narrators over legacy dicts
- Dashboard / Student Home / analytics advice wiring
- EP-001.1 CLS, EP-001.2 daily plan, EP-001.3 readiness intelligence APIs
- Mission narratives and study tips

### Partially implemented

- Today's focus (multiple competing sources; not Twin+Planner packaged)
- Strongest / greatest risk (ORM + intelligence API; not unified insight copy)
- Next action (engine vs planner vs readiness vs mission narrative)
- Workload / readiness explanations (exist in pieces; not composed)
- Motivational progress (streaks/tips/weekly; not one insight summary)

### Missing

1. Single **Insight & Recommendation Layer** that consumes Twin + Planner + Readiness
2. Student-facing package: key focus, strongest area, greatest risk, next action, workload explanation, readiness explanation, motivational progress
3. Twin-gated host API on Runtime A recommendation surface (`build_study_insights`) fail-open when Twin OFF
4. Explicit ownership: communication only — no duplicated calculations / state / parallel engine

---

## 8. What must remain untouched in this review’s conclusion

- Do not rewrite Twin / Planner / Readiness ownership
- Do not replace `generate_recommendations` in this milestone (HTTP cutover optional later)
- Do not promote EI / OS / V2 / Founder engines to EP-001.4 authority
- Do not invent mastery, readiness scores, or mission plans inside the insight layer
