# EP-001.3 — Readiness Discovery Report

**Milestone:** EP-001.3 — Readiness Intelligence (Consumer of the Canonical Learner State)  
**Phase:** 1 — Architecture Discovery (read-only)  
**Date:** 2026-07-26

---

## 1. Sources reviewed

| Source | Role |
|---|---|
| `knowledge/architecture/ep001_1_student_digital_twin_foundation/*` | EP-001.1 Foundation — `CanonicalLearnerState` consumer contract |
| `knowledge/architecture/ep001_2_adaptive_study_planner/*` | EP-001.2 Planner — CLS consumer pattern to mirror |
| `app/infrastructure/adapters/digital_twin/foundation.py` | Canonical learner-state read model |
| `app/infrastructure/adapters/adaptive_study_planner/` | Planner consumer / daily plan projection |
| `knowledge/subsystems/readiness.md` | Runtime A readiness subsystem charter |
| `app/services/readiness_service.py` | Production readiness calculations |
| `app/infrastructure/adapters/adaptive_engine/collectors.py` | `ReadinessCollector` (pass-through into Twin) |
| `app/domain/readiness/` | Epic Capability 2.7 structural aggregation (posture / warrant; no %) |
| `app/application/student_twin/readiness_estimator.py` | V2 Twin readiness blend (parallel) |
| `src/application/student_experience/readiness/` | Education OS Exam Readiness Experience (presentation) |
| `app/services/analytics_service.py` / dashboard / analytics routes | HTTP / dashboard consumers |
| `app/services/recommendation_service.py` | Adjacent consumer of readiness signals |
| `app/services/database_readiness_service.py` | Unrelated DB migration readiness (exclude) |
| `docs/architecture/CAPABILITY_2_7_*` | Structural readiness architecture (coexistence) |

---

## 2. Student Digital Twin Foundation (EP-001.1) — consumer contract

**Canonical read API:** `StudentDigitalTwinFoundation.assemble(student_id) → CanonicalLearnerState`

Readiness-relevant dimensions (envelope: availability / authority / payload):

| Dimension | Readiness use |
|---|---|
| `study_state.readiness_overall` | Pass-through Runtime A composite score (via `ReadinessCollector`) |
| `topic_mastery` | Strongest / weakest areas; mastery influence |
| `topic_progress` | Coverage / completion influence |
| `learning_evidence` | Evidence density → confidence / warrant |
| `practice_performance` | Practice influence on drivers |
| `study_behaviour` | Behaviour reliability driver |
| `study_consistency` | Consistency driver / confidence |
| `streaks` | Continuity driver |
| `mission_completion` | Mission adherence / review-discipline proxy |
| `mock_performance` | Must remain honest `unavailable` — never fabricate |

**Flags:** `KWALITEC_DIGITAL_TWIN` enables Foundation; Authority cutover is separate and default OFF.

---

## 3. Adaptive Study Planner (EP-001.2) — planner outputs for readiness

When Twin is ON, `PlanningService.build_daily_study_plan` returns a projection with:

| Planner output | Readiness use |
|---|---|
| `today_missions` | Recommended next actions (mission slots) |
| `revision_priorities` | Next-action revision focus |
| `topic_ordering` | Progression context for actions |
| `recommended_workload` | Workload-aware next-action framing |

Readiness **evaluates**; Planner **plans**. Readiness may cite planner outputs as recommended next actions — it must not re-plan missions or invent learner state.

---

## 4. MS-004 / EP-001 ownership (binding)

- Runtime A = SoT for educational **transaction facts**.
- Twin / Foundation = SoT for **learner-state claims** consumers should read.
- Planner = SoT for **planning outputs**.
- Readiness = SoT for **readiness evaluation** (composites, confidence, drivers, areas, action suggestions grounded in Twin + Planner).

**Circular-dependency constraint:** `ReadinessCollector` already calls `ReadinessService.get_overall_readiness` to feed Foundation `study_state`. EP-001.3 must **not** make `get_overall_readiness` call Foundation (would recurse). Intelligence is an additive method that **consumes** Foundation after collection has already produced CLS.

---

## 5. Existing readiness functionality (Runtime A — production)

```
TopicProgress / Mission / StudyAttempt / Curriculum leaves
                ↓
ReadinessService.get_overall_readiness  (Coverage 50% + Mastery 30% + Review 20%)
ReadinessService.get_curriculum_coverage
ReadinessService.get_review_* / streaks / weakest / strongest
ReadinessService.calculate_readiness    (weighted syllabus progress only)
                ↓
dashboard / analytics / settings / recommendation / exam_timeline
                ↓
ReadinessCollector → Twin Foundation study_state.readiness_overall
```

| Capability | Owner | Notes |
|---|---|---|
| Overall composite score | `ReadinessService.get_overall_readiness` | Deterministic; ORM-backed |
| Curriculum coverage | `get_curriculum_coverage` | Leaf topics started |
| Review discipline / backlog | `get_review_*` | Mission completion + due dates |
| Streaks | `get_current_streak` / `get_longest_streak` | StudyAttempt dates |
| Weakest / strongest topics | `get_weakest_topics` / `get_strongest_topics` | Evidence-backed mastery |
| Weighted syllabus readiness | `calculate_readiness` | Progress % only (IA-004 language) |
| Twin pass-through | `ReadinessCollector` | No private formula |

**Production HTTP entry:** `dashboard`, `analytics`, `settings`, `mission` routes; `AnalyticsService`, `RecommendationService`, `ExamTimeline`.

---

## 6. Inventory — every readiness-contributing component

### A. Runtime A (extend these)

1. `ReadinessService` — **canonical Readiness Intelligence host**
2. `ReadinessCollector` — Twin evidence pass-through (leave formula-free)
3. Dashboard / analytics consumers of readiness dicts

### B. Twin / planner (consume; do not replace ReadinessService)

4. EP-001.1 `CanonicalLearnerState` / Foundation
5. EP-001.2 `DailyStudyPlanProjection` / `PlanningService.build_daily_study_plan`
6. Adaptive `twin_input` pattern (prior art for Twin consumption)

### C. Parallel stacks (do **not** promote as EP-001.3 readiness engine)

7. Epic `app/domain/readiness/ReadinessAggregation` — structural posture/warrant (no %)
8. V2 `ReadinessEstimator` (`app/application/student_twin`)
9. Education OS `ExamReadinessService` / readiness composer (`src/`)
10. Evidence Platform `shadow_readiness` — observational gate readiness
11. `DatabaseReadinessService` — Alembic/ops (unrelated)

---

## 7. Discovery conclusion

Kwalitec already has a **production readiness engine** (`ReadinessService` + collector + dashboard consumers). What EP-001.3 must add is **not** another readiness service — it is a **Canonical Learner State (+ Planner) consumer seam** so readiness outputs (score, confidence, strongest/weakest areas, drivers, recommended next actions) are derived from EP-001.1 Foundation and EP-001.2 planner projections instead of each surface re-querying ORM independently for intelligence enrichment.

**Binding decision for EP-001.3**

| Concern | Owner |
|---|---|
| Learner state | Student Digital Twin Foundation |
| Planning outputs | Adaptive Study Planner / `PlanningService` |
| Readiness evaluation | `ReadinessService` (+ thin intelligence consumer) |
| Parallel Epic / V2 / OS stacks | Remain non-authority for this milestone |

**Rule:** Prefer extend / integrate. Never introduce a parallel Readiness Intelligence package that replaces `ReadinessService`.
