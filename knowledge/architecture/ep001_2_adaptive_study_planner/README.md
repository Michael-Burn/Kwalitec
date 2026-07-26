# EP-001.2 — Adaptive Study Planner

**Milestone:** EP-001.2 — Adaptive Study Planner (Consumer of the Canonical Learner State)  
**Status:** Implemented  
**Authority:** Extends Runtime A planning; consumes EP-001.1 Foundation — does not redesign Twin  
**Package:** `app/infrastructure/adapters/adaptive_study_planner/` + `PlanningService` / `MissionOptimizer`

---

## Deliverables

| Artefact | Path |
|---|---|
| Planner Discovery Report | [`PLANNER_DISCOVERY_REPORT.md`](PLANNER_DISCOVERY_REPORT.md) |
| Gap Analysis | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) |
| Implementation Plan | [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) |
| Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) |

---

## Canonical decision (binding)

| Concern | Canonical owner |
|---|---|
| Learner state (mastery, progress, evidence, behaviour, consistency, streaks) | EP-001.1 `CanonicalLearnerState` / Foundation |
| Planning, scheduling, mission persistence, workload recommendation | `PlanningService` (+ StudyPlan / TimeEngine / Mission) |
| Syllabus structure / topic order | `CurriculumService` |
| OS / Journey / Strategy planners | Parallel non-authority stacks |

**Rule:** Prefer extend / integrate. Never introduce a parallel Adaptive Study Planner that replaces `PlanningService` or a fourth learner-state model.

---

## Feature flags

| Env | Flag | Default | Effect |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | Foundation available → adaptive daily plan from CLS |

No separate planner flag — planner consumes Twin when Twin is ON (fail-open to legacy planning when OFF).

---

## Governing documents

- EP-001.1 Foundation README
- `STUDENT_DIGITAL_TWIN.md` (Planning Engine as consumer)
- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
- `knowledge/subsystems/study-planning.md`
