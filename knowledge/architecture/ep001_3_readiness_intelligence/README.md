# EP-001.3 — Readiness Intelligence

**Milestone:** EP-001.3 — Readiness Intelligence (Consumer of the Canonical Learner State)  
**Status:** Implemented  
**Authority:** Extends Runtime A `ReadinessService`; consumes EP-001.1 Foundation + EP-001.2 planner outputs — does not redesign Twin or Planner  
**Package:** `app/infrastructure/adapters/readiness_intelligence/` + `ReadinessService`

---

## Deliverables

| Artefact | Path |
|---|---|
| Readiness Discovery Report | [`READINESS_DISCOVERY_REPORT.md`](READINESS_DISCOVERY_REPORT.md) |
| Existing Implementation Review | [`EXISTING_IMPLEMENTATION_REVIEW.md`](EXISTING_IMPLEMENTATION_REVIEW.md) |
| Gap Analysis | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) |
| Implementation Plan | [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) |
| Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) |

---

## Canonical decision (binding)

| Concern | Canonical owner |
|---|---|
| Learner state (mastery, progress, evidence, behaviour, consistency, streaks, missions) | EP-001.1 `CanonicalLearnerState` / Foundation |
| Planning, mission slots, revision priorities, workload | EP-001.2 Adaptive Study Planner / `PlanningService` |
| Readiness evaluation (score, confidence, areas, drivers, next actions) | `ReadinessService` (+ intelligence consumer) |
| Syllabus structure / topic order | `CurriculumService` |
| Epic structural aggregation / V2 / OS readiness stacks | Parallel non-authority for this milestone |

**Rule:** Prefer extend / integrate. Never introduce a parallel readiness engine that replaces `ReadinessService` or duplicates Twin / Planner responsibilities.

---

## Feature flags

| Env | Flag | Default | Effect |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | Foundation available → readiness intelligence from CLS (+ planner when present) |

No separate readiness-intelligence flag — readiness consumes Twin when Twin is ON (fail-open to legacy `get_overall_readiness` / weak/strong topics when OFF).

---

## Governing documents

- EP-001.1 Foundation README
- EP-001.2 Adaptive Study Planner README
- `knowledge/subsystems/readiness.md`
- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
- `docs/architecture/CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md` (Epic structural stack — coexistence only)
