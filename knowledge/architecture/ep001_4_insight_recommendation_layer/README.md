# EP-001.4 — Insight & Recommendation Layer

**Milestone:** EP-001.4 — Insight & Recommendation Layer  
**Status:** Implemented  
**Authority:** Extends Runtime A `RecommendationService`; consumes EP-001.1 Foundation + EP-001.2 planner + EP-001.3 readiness intelligence — does not redesign Twin, Planner, or Readiness  
**Package:** `app/infrastructure/adapters/insight_recommendation/` + `RecommendationService`

---

## Deliverables

| Artefact | Path |
|---|---|
| Insight Discovery Report | [`INSIGHT_DISCOVERY_REPORT.md`](INSIGHT_DISCOVERY_REPORT.md) |
| Existing Implementation Review | [`EXISTING_IMPLEMENTATION_REVIEW.md`](EXISTING_IMPLEMENTATION_REVIEW.md) |
| Gap Analysis | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) |
| Implementation Plan | [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) |
| Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) |

---

## Canonical decision (binding)

| Concern | Canonical owner |
|---|---|
| Learner state | EP-001.1 `CanonicalLearnerState` / Foundation |
| Planning, mission slots, revision priorities, workload | EP-001.2 Adaptive Study Planner / `PlanningService` |
| Readiness evaluation (score, confidence, areas, drivers, next actions) | EP-001.3 `ReadinessService` (+ intelligence consumer) |
| Student-facing insight communication | `RecommendationService` (+ insight consumer) |
| Syllabus structure / topic order | `CurriculumService` |
| EI / OS / V2 / Founder recommendation stacks | Parallel non-authority for this milestone |

**Rule:** Prefer extend / integrate. Never introduce a parallel recommendation engine that replaces `RecommendationService` or duplicates Twin / Planner / Readiness responsibilities.

---

## Feature flags

| Env | Flag | Default | Effect |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | Foundation available → study insights from CLS + planner + readiness intelligence |

No separate insight flag — insight consumes Twin when Twin is ON (fail-open to legacy `generate_recommendations` when OFF).

---

## Governing documents

- EP-001.1 Foundation README
- EP-001.2 Adaptive Study Planner README
- EP-001.3 Readiness Intelligence README
- `knowledge/subsystems/readiness.md`
- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
