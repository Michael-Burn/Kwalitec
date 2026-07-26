# EP-001.2 — Planner Discovery Report

**Milestone:** EP-001.2 — Adaptive Study Planner (Consumer of the Canonical Learner State)  
**Phase:** 1 — Architecture Discovery (read-only)  
**Date:** 2026-07-26

---

## 1. Sources reviewed

| Source | Role |
|---|---|
| `knowledge/architecture/ep001_1_student_digital_twin_foundation/*` | EP-001.1 Foundation — `CanonicalLearnerState` consumer contract |
| `app/infrastructure/adapters/digital_twin/foundation.py` | Canonical learner-state read model |
| `STUDENT_DIGITAL_TWIN.md` | Constitutional Twin; Planning Engine as **consumer** |
| `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` | MS-004 synthesis; Twin is **not** a planner |
| `knowledge/architecture/DIGITAL_TWIN_DATA_MODEL.md` | Logical learner profile facets |
| `knowledge/subsystems/study-planning.md` | Runtime A planning subsystem |
| `app/services/planning_service.py` | Production daily mission generation |
| `app/services/study_plan_service.py` | Study plan / week plan CRUD |
| `app/services/time_engine_service.py` | Capacity vs remaining curriculum hours |
| `app/services/mission_optimizer.py` | Balanced review / weak / progression selection |
| `app/services/mission_service.py` | Mission ORM lifecycle |
| `app/services/recommendation_service.py` | Deterministic recommendations |
| `app/services/readiness_service.py` | Readiness + streaks (facts Twin pass-through) |
| `app/services/adaptive_learning_service.py` | Mastery / review dates / weak topics |
| `app/services/learning_lifecycle_service.py` | Learning vs Revision stage |
| Journey / mission engine stacks | Parallel DTO generators (not syllabus planner authority) |
| Education OS revision / mission pipelines (`src/`) | Deterministic OS planners — not Runtime A production authority |
| Strategy Engine planners | Advisory MS-005 — must not become a second study planner |

---

## 2. Student Digital Twin Foundation (EP-001.1) — consumer contract

**Canonical read API:** `StudentDigitalTwinFoundation.assemble(student_id) → CanonicalLearnerState`

Planner-relevant dimensions (envelope: availability / authority / payload):

| Dimension | Planner use |
|---|---|
| `topic_mastery` | Weak / revision prioritisation |
| `topic_progress` | Topic ordering / progression / completed leaves |
| `learning_evidence` | Evidence-backed explainability (attempt refs) |
| `practice_performance` | Workload / practice intensity context |
| `study_behaviour` | Rhythm / habits / persistence facets |
| `study_consistency` | Consistency facet for workload guardrails |
| `streaks` | Continuity signal for workload / rationale |
| `study_state` | Lifecycle, exam countdown, preferences (weekly hours / session minutes) |
| `mission_completion` | Recent mission adherence context |
| `mock_performance` | Must remain honest `unavailable` — never fabricate |

**Available study time today** is only partially on Foundation (`planned_weekly_hours`, `preferred_session_minutes`). Daily weekday/weekend minutes remain a **Planning / StudyPlan** artefact (`TimeEngineService` / `StudyPlan`).

**Flags:** `KWALITEC_DIGITAL_TWIN` enables Foundation; Authority cutover is separate and default OFF.

---

## 3. MS-004 synthesis (binding for consumers)

- Runtime A = SoT for educational **transaction facts**.
- Twin / Foundation = SoT for **learner-state claims** consumers should read.
- Twin synthesises; it does **not** generate or mutate study plans / missions.
- Planning / StudyPlanService own plan generation and mutation.

---

## 4. Existing planning functionality (Runtime A — production)

```
Wizard → StudyPlanService → WeekPlan rows
                ↓
PlanningService.generate_today_mission
                ↓
MissionService.create_mission (ORM Mission + MissionTask)
```

| Capability | Owner | Notes |
|---|---|---|
| Plan CRUD / active plan | `StudyPlanService` | Curriculum binding, week plans |
| Daily mission generation | `PlanningService` | Idempotent; Learning vs Revision |
| Learning topic selection | `_select_topic_for_today` | First incomplete syllabus leaf (IA-004) |
| Revision missions | `_generate_revision_mission_for_date` | Deterministic kind rotation + weak label |
| Capacity math | `TimeEngineService` | Hours to exam vs remaining curriculum |
| Balanced topic set (dict) | `MissionOptimizer` | Review + weak + progression — not always persisted |
| Recommendations | `RecommendationService` | Parallel surface; reads Adaptive/Readiness directly |
| Lifecycle stage | `LearningLifecycleService` | Drives Learning vs Revision mission mode |

**Production HTTP entry:** dashboard + mission routes call `PlanningService.generate_today_mission`.

---

## 5. Missions

| Path | Persists? | Authority |
|---|---|---|
| `PlanningService` → `MissionService` | Yes (ORM) | **Production** syllabus planner |
| `MissionOptimizer.generate_balanced_mission` | No (dict) | Helper / advisory balance |
| `app/application/mission_engine*` | DTO | Journey structural — parallel |
| `DailyMissionAssembler` (unified journey) | No | Presentation only |
| OS `AdaptiveMissionGenerator` / `MissionGenerator` | No (pure) | Education OS — not Flask production SoT |

---

## 6. Readiness inputs

| Source | What planner gets today |
|---|---|
| `ReadinessService` | Used by recommendations / Twin collectors — **not** by `PlanningService` mission math |
| Foundation `study_state.readiness_overall` + `streaks` | Available to consumers when Twin ON |
| `ExamTimeline` | Exam proximity for recommendations |

Streaks and readiness composites must be **consumed** via Foundation when Twin is ON — not re-derived in the planner.

---

## 7. Inventory — every planner / scheduling capability

### A. Runtime A (extend these)

1. `PlanningService` — **canonical Adaptive Study Planner host**
2. `StudyPlanService` — plan shell / weeks
3. `TimeEngineService` — capacity
4. `MissionOptimizer` — balanced topic selection helper
5. `RecommendationService` — related but distinct recommendation engine

### B. Twin / adaptive (consume Twin; do not replace PlanningService)

6. `app/application/adaptive_learning/revision_planner.py`
7. `AdaptiveDecisionEngine`
8. `app/infrastructure/adapters/adaptive_engine/twin_input.py` (pattern for Twin consumption)

### C. Parallel stacks (do **not** promote as EP-001.2 planner)

9. Journey `MissionCoordinator` / v2
10. Strategy Engine `StudyPlanner` / `SessionPlanner` / `RevisionPlanner`
11. OS `AdaptiveRevisionPlanner` / domain `StudyPlanner`
12. Recovery planner adapter (advisory)

---

## 8. Discovery conclusion

Kwalitec already has a **production study planner** (`PlanningService` + `StudyPlanService` + `TimeEngineService` + `MissionOptimizer`). What EP-001.2 must add is **not** another planner engine — it is a **Canonical Learner State consumer seam** so daily plan outputs (missions priorities, revision order, topic ordering, workload) are derived from EP-001.1 Foundation instead of each helper re-querying ORM / AdaptiveLearning / Readiness independently.

**Binding decision for EP-001.2**

| Concern | Owner |
|---|---|
| Learner state (mastery, progress, evidence, behaviour, consistency, streaks) | Student Digital Twin Foundation |
| Planning / scheduling / mission persistence | `PlanningService` (+ StudyPlan / Mission / TimeEngine) |
| Syllabus order | `CurriculumService` |
| Parallel OS / Journey / Strategy planners | Remain non-authority for this milestone |

**Rule:** Prefer extend / integrate. Never introduce a parallel Adaptive Study Planner package that replaces `PlanningService`.
