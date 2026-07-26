# EP-002.9 — Ownership Certification

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Supersedes for surface cutover status:** EP-001.5 Authority Matrix §4 (HTTP cutover was “API only”)

Legend: **O** · **E** · **C** · **R**

---

## 1. Canonical ownership matrix (post EP-002)

| Concern | Canonical owner | Location | Competing / non-authority | Drift? |
|---|---|---|---|---|
| Curriculum / syllabus structure | Curriculum Engine + `CurriculumService` | `app/curriculum/` | None for ordering | **None** |
| Runtime facts (writes) | Runtime A SQL + services | attempts, missions, progress, plans | Bridges may read/project | **None** |
| Learner-state read model | EP-001.1 Foundation / MS-004 | `digital_twin/foundation.py` | Epic / V2 / EOS Twin | **Controlled** (quarantined) |
| Planning outputs | `PlanningService` + EP-001.2 | `planning_service.py`, `adaptive_study_planner/` | MissionOptimizer (quarantined) | **None** |
| Mission ORM persistence | `PlanningService.generate_today_mission` | Runtime A mission models | Twin display proxy | **Accepted tension** (`TD-DP-01`) |
| Readiness evaluation | `ReadinessService` + EP-001.3 | `readiness_service.py`, `readiness_intelligence/` | Epic / V2 readiness | **None** |
| Twin communication / guidance | `RecommendationService` + EP-001.4 | `recommendation_service.py`, `insight_recommendation/` | EI Stage A card (`TD-CO-02`) | **Partial residual** |
| Consumer-chain orchestration | `consumer_chain` | dual-run / cutover / soak / telemetry | Must not own maths | **None** |
| Runtime A presentation selection | `RuntimeAPresentationAdapter` | `app/presentation/intelligence_surface/` | Route-local narration removed | **None** |
| Legacy presentation adapter | `EducationalExplainabilityService` | EIP-003 Outcome B | Peer SoT retired for Twin Runtime A concerns | **Closed for Runtime A HTTP** |
| Experience TwinPort UX | `ExperienceTwinAdapter` (default) | `student_twin/experience_adapter.py` | Foundation Authority when gated | **None** (gated) |
| Experience `/student` explanation | Experience ExplanationService | Out of EP-002 scope | Parallel under dual-run | **Out of scope** (`TD-PC-02`) |

---

## 2. Authority cutover map (post EP-002)

| Surface | Production default authority | Twin-gated alternative | Gate |
|---|---|---|---|
| Dashboard / home recommendations | `generate_recommendations` | `build_study_insights` projection | Twin + `STUDY_INSIGHTS_CUTOVER` + non-prod |
| Dashboard / analytics readiness | Legacy readiness surface | `build_readiness_intelligence` projection | Twin + `READINESS_INTELLIGENCE_CUTOVER` + non-prod |
| Dashboard / missions mission display | `generate_today_mission` | `build_daily_study_plan` display proxy | Twin + `DAILY_PLAN_CUTOVER` + non-prod |
| Collectors / Adaptive TwinInput readiness facts | `get_overall_readiness` | **None** (must remain legacy) | N/A |
| Experience StudentTwinPort | `ExperienceTwinAdapter` | Foundation Authority port | Twin + Authority |
| Experience bridges / Founder recommendations | Legacy Runtime A | Not cut over by EP-002 | N/A |

---

## 3. Ownership rules still encoded in code

**E:**

- `PlanningService`: Twin owns mastery/progress/behaviour; service owns planning outputs and mission persistence.  
- `ReadinessService`: consumes Canonical state; does not invent learner state; does not alter collector-safe getters.  
- `RecommendationService`: communication only; does not invent state, plan missions, or recalculate readiness.  
- Cutover modules: eligibility + projection; fail-open to legacy.  
- Presentation adapter: selects narrator; does not evaluate or plan.  
- MissionOptimizer: soft-deprecated; no production callers.

**C:** Ownership speech matches implementation.

---

## 4. Ownership drift findings (exit)

| ID | Severity | Description | Disposition |
|---|---|---|---|
| OD-01 | Info | Production HTTP still legacy-authoritative by default | **By design** (fail-open) |
| OD-02 | Low | EI Stage A may narrate beside Insight when Stage A flags ON | Accepted residual `TD-CO-02` |
| OD-03 | Medium | Daily Plan Twin display may diverge from ORM session topic | Accepted residual `TD-DP-01` |
| OD-04 | Info | Experience `/student` narrator not under Runtime A facade | Out of scope `TD-PC-02` |
| OD-05 | Info | Multi-Twin stacks remain importable | Quarantine narrative holds |

**C:** No ownership *invention* drift. Residual drift is surface scope, presentation residual, or intentional fail-open.

---

## 5. Ownership certification statement

| Assertion | Certified? |
|---|---|
| Programme ownership matrix unchanged from EP-002 brief | **Yes** |
| Twin / Planner / Readiness / Insight / Curriculum / Runtime A writes boundaries hold | **Yes** |
| Presentation does not own evaluation or planning | **Yes** |
| MissionOptimizer is not a second mission authority | **Yes** |
| Experience consolidation complete | **No** (explicitly out of scope) |

**Verdict: Ownership boundaries are certified intact for EP-002 exit.**

**R:** Do not treat Experience `/student` or EI Stage A residuals as EP-002 ownership failures; track under successor guidance.
