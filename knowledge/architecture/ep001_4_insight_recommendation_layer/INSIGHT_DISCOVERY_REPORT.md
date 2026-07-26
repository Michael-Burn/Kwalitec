# EP-001.4 — Insight Discovery Report

**Milestone:** EP-001.4 — Insight & Recommendation Layer  
**Phase:** 1 — Architecture Discovery (read-only)  
**Date:** 2026-07-26

---

## 1. Sources reviewed

| Source | Role |
|---|---|
| `knowledge/architecture/ep001_1_student_digital_twin_foundation/*` | EP-001.1 Foundation — `CanonicalLearnerState` consumer contract |
| `knowledge/architecture/ep001_2_adaptive_study_planner/*` | EP-001.2 Planner — daily plan / workload consumer pattern |
| `knowledge/architecture/ep001_3_readiness_intelligence/*` | EP-001.3 Readiness — assessment packaging pattern to mirror |
| `app/infrastructure/adapters/digital_twin/foundation.py` | Canonical learner-state read model |
| `app/infrastructure/adapters/adaptive_study_planner/` | Planner consumer / daily plan projection |
| `app/infrastructure/adapters/readiness_intelligence/` | Readiness intelligence assessment |
| `app/services/recommendation_service.py` | Production recommendation rule engine |
| `app/services/educational_explainability_service.py` | EIP-003 presentation narrators |
| `app/application/dashboard/` | Dashboard recommendation card builders |
| `app/dashboard/routes.py` / `student` home | HTTP student surfaces for advice |
| Founder / OS / EI / V2 recommendation stacks | Parallel — inventory only |

---

## 2. Student Digital Twin Foundation (EP-001.1) — consumer contract

**Canonical read API:** `StudentDigitalTwinFoundation.assemble(student_id) → CanonicalLearnerState`

Insight-relevant dimensions (envelope: availability / authority / payload):

| Dimension | Insight use |
|---|---|
| `study_state` | Lifecycle, exam context, readiness pass-through for progress framing |
| `topic_mastery` | Strongest / risk framing (prefer readiness packaging when present) |
| `topic_progress` | Coverage / completion for progress summary |
| `learning_evidence` | Honesty about evidence density |
| `practice_performance` | Practice context for motivational copy |
| `study_behaviour` / `study_consistency` | Behavioural honesty in summaries |
| `streaks` | Continuity for motivational progress |
| `mission_completion` | Adherence framing |
| `mock_performance` | Must remain honest `unavailable` — never fabricate |

**Flags:** `KWALITEC_DIGITAL_TWIN` enables Foundation; Authority cutover is separate and default OFF.

---

## 3. Adaptive Study Planner (EP-001.2) — planner outputs for insights

When Twin is ON, `PlanningService.build_daily_study_plan` returns a projection with:

| Planner output | Insight use |
|---|---|
| `today_missions` | Today's key focus + recommended next action titles/reasons |
| `revision_priorities` | Risk / focus alternatives when missions empty |
| `recommended_workload` | Workload explanation (minutes + rationale) |
| `topic_ordering` | Progression context (cite, do not re-order) |

Insight **communicates**; Planner **plans**. The layer must not re-plan missions or invent workload minutes.

---

## 4. Readiness Intelligence (EP-001.3) — evaluation outputs for insights

When Twin is ON, `ReadinessService.build_readiness_intelligence` returns:

| Readiness output | Insight use |
|---|---|
| `readiness_score` / `confidence_level` | Readiness explanation |
| `strongest_areas` | Strongest area guidance |
| `weakest_areas` | Greatest risk guidance |
| `readiness_drivers` | Supporting readiness explanation |
| `recommended_next_actions` | Preferred next-action text when planner-grounded |

Insight **explains**; Readiness **evaluates**. The layer must not invent a second readiness score or confidence band.

---

## 5. MS-004 / EP-001 ownership (binding)

- Runtime A = SoT for educational **transaction facts**.
- Twin / Foundation = SoT for **learner-state claims** consumers should read.
- Planner = SoT for **planning outputs**.
- Readiness = SoT for **readiness evaluation**.
- Insight Layer = SoT for **student-facing communication** that composes Twin + Planner + Readiness.

**Constraint:** Do not introduce a fifth recommendation formula. Do not move ownership away from Twin, Planner, or Readiness.

---

## 6. Existing recommendation / advice functionality (Runtime A — production)

```
ORM facts / Adaptive / Readiness getters
                ↓
RecommendationService.generate_recommendations  (rule engine)
                ↓
dashboard (legacy) / RecommendationAdapter → Student Home
                ↓
EducationalExplainabilityService  (narratives over existing dicts)
```

| Capability | Owner | Notes |
|---|---|---|
| Ranked study recommendations | `RecommendationService` | Deterministic rule engine; ORM-backed |
| Today's single recommendation | `generate_today_recommendation` | Top-1 of same engine |
| EIP-003 narratives | `EducationalExplainabilityService` | Presentation only; not Twin-aware |
| Mission coach copy | Mission narrative builders | Mission + lifecycle facts |
| Study tips | `StudyTipsService` | Rotating non-intelligence tips |
| Burnout / rest advice | `BurnoutMonitor` → Rest category | ORM patterns |
| Twin-gated plan / readiness APIs | EP-001.2 / EP-001.3 | Implemented; **not on HTTP cutover** |

**Production HTTP entry:** dashboard, student home, mission, analytics.

---

## 7. Inventory — every study-advice contributing component

### A. Runtime A (extend / compose these)

1. `RecommendationService` — **canonical Insight host** (additive presentation API)
2. `EducationalExplainabilityService` — existing presentation narrators (adjacent; remain)
3. Dashboard / Student Home consumers of recommendation dicts
4. EP-001.1 Foundation / EP-001.2 planner / EP-001.3 readiness intelligence

### B. Twin / planner / readiness (consume; do not replace)

5. `CanonicalLearnerState` / Foundation
6. `DailyStudyPlanProjection` / `PlanningService.build_daily_study_plan`
7. `ReadinessIntelligenceAssessment` / `ReadinessService.build_readiness_intelligence`

### C. Parallel stacks (do **not** promote as EP-001.4 insight authority)

8. Structural EI `DecisionEngine` → `RecommendationEngine` (flag-gated)
9. Education OS recommendation / learning insight composers (`src/`)
10. V2 `app/application/student_twin/recommendation_service.py`
11. Founder `FounderRecommendationService` (non-student)
12. Adaptive Engine shadow/soak recommendation fallbacks

---

## 8. Discovery conclusion

Kwalitec already has a **production recommendation engine** (`RecommendationService`) plus fragmented presentation narrators. EP-001.1–3 already produce Twin-grounded plan and readiness artefacts that are **not yet packaged as student-facing insight guidance**.

What EP-001.4 must add is **not** another recommendation engine — it is a **presentation-focused consumer seam** that translates Canonical Learner State + Adaptive Study Planner + Readiness Intelligence into clear, personalised, actionable study guidance (today's focus, strongest area, greatest risk, next action, workload/readiness explanations, motivational progress).

**Binding decision for EP-001.4**

| Concern | Owner |
|---|---|
| Learner state | Student Digital Twin Foundation |
| Planning outputs | Adaptive Study Planner / `PlanningService` |
| Readiness evaluation | `ReadinessService` (+ intelligence consumer) |
| Student-facing insight communication | `RecommendationService` (+ insight consumer) |
| Parallel EI / OS / V2 / Founder stacks | Remain non-authority for this milestone |

**Rule:** Prefer extend / integrate. Never introduce a parallel recommendation architecture that re-calculates learner state, plans, or readiness.

**No code was modified during Phase 1.**
