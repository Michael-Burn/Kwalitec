# EP-002.7 — Architecture Discovery Report

**Milestone:** EP-002.7 — Daily Plan & Mission Dual-Run and Gated HTTP Cutover  
**Date:** 2026-07-26  
**Nature:** Mandatory discovery before implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Scope of discovery

Reviewed:

| Artefact | Path / location |
|---|---|
| EP-001.5 Architectural Integration Review | `knowledge/architecture/ep001_5_architectural_integration_review/` |
| EP-002 Programme Brief | `knowledge/architecture/ep002_student_intelligence_surface/PROGRAMME_BRIEF.md` |
| EP-002.1–6 Completion Reports | `knowledge/architecture/ep002_* /COMPLETION_REPORT.md` |
| MissionOptimizer decision | `ep002_2_shared_foundation_di/MISSION_OPTIMIZER_DECISION.md` |
| `PlanningService` | `app/services/planning_service.py` |
| Adaptive Study Planner | `app/infrastructure/adapters/adaptive_study_planner/` |
| Dashboard / mission surfaces | `app/dashboard/routes.py`, `app/mission/routes.py` |
| Consumer-chain cutover pattern | `consumer_chain/cutover.py`, `readiness_cutover.py` |
| Feature flags | `app/application/config/v2_flags.py` |
| Constitutional docs | Twin architecture, authority matrix, quarantine note |

---

## 2. Authority and product surface today

| Concern | Authoritative path | Twin path (pre-EP-002.7) |
|---|---|---|
| Today’s mission ORM | `PlanningService.generate_today_mission` | — |
| Adaptive daily plan projection | — | `build_daily_study_plan` (observability / soak / Insight+Readiness grounding) |
| Dashboard / `/missions` HTTP | Direct `generate_today_mission` + `MissionService.get_today_mission` | **No dual-run / cutover** |
| Balanced mission helper | Quarantined `MissionOptimizer` | Delegates to `build_daily_study_plan` when Twin ON |
| Experience MissionStartAdapter | `generate_today_mission` | Unchanged requirement |
| Production defaults | Twin OFF / Cutover OFF | Plan unavailable to students |

**O:** Programme cutover order is recommendations → readiness → mission/plan (WS6).  
**E:** EP-002.6 exit recommends EP-002.7; MissionOptimizer decision forbids wiring the orphan API.  
**C:** EP-002.7 may dual-run and gate-cutover `build_daily_study_plan` vs `generate_today_mission` only.

---

## 3. PlanningService entry points

| API | Role | Student influence (pre-EP-002.7) |
|---|---|---|
| `generate_today_mission(user_id)` | Legacy ORM create/fetch | **Yes — authoritative** |
| `build_daily_study_plan(user_id, …)` | Twin-gated plan projection (no ORM write) | No HTTP authority yet |
| MissionOptimizer.generate_balanced_mission | Soft-deprecated orphan | **None** (no production callers) |

**O:** Templates expect Mission ORM fields (`title`, `status`, `tasks`, `id`).  
**E:** `dashboard/index.html`, `mission/index.html`.  
**C:** Cutover must project Twin plan into a mission surface DTO that duck-types Mission for templates **without Twin writing ORM**.

**O:** EP-001.2 explicitly separated plan projection from mission persistence.  
**C / R:** Cutover must preserve `generate_today_mission` as Runtime A write authority for session continuity; Twin may overlay display title/slots only.

---

## 4. Inheritance from EP-002.5 / EP-002.6

| Component | Behaviour | Implication for daily plan |
|---|---|---|
| Dual-run eligibility | Twin ON ∧ non-prod | Reuse env gate; no dual-run flag |
| Cutover eligibility | Twin ON ∧ cutover flag ∧ non-prod | Add `KWALITEC_DAILY_PLAN_CUTOVER` |
| Fail-open | Twin None / exception / blocking → legacy | Copy verbatim |
| Semantic alignment | Not fingerprints | Topic / objective / sequencing / workload |
| Skip dual-run when cutover active | Avoid double Twin assemble | Daily-plan ContextVar |
| Facade-not-mutate-legacy | Protect bridges / collectors | Do not wrap `generate_today_mission` body |

---

## 5. Feature flags

| Env | Flag | Default | Role |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | Required for Twin path |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF | Recorded; not required for Runtime A |
| `KWALITEC_DAILY_PLAN_CUTOVER` | `ENABLE_DAILY_PLAN_CUTOVER` | OFF | **New** — student-payload flip gate |
| `APP_ENV` / `FLASK_ENV` | — | development | Must not be `production` / `prod` |

**C / R:** Add dedicated cutover flag (requires Twin). Dual-run needs no new flag.

---

## 6. Projection requirement

| Dimension | Legacy HTTP | Twin Daily Study Plan |
|---|---|---|
| Title | `Mission.title` | Primary `today_missions[]` slot → display title |
| Status / id / tasks | ORM Mission | Proxied from legacy ORM (session CTA) |
| Workload | Absent | `recommended_workload` |
| Sequencing | Implicit syllabus next topic | `topic_ordering` / slots |
| Authority marker | — | `source_authority="daily_study_plan"` |

---

## 7. Constitutional constraints (binding)

1. MissionOptimizer remains quarantined — **no calls**.  
2. PlanningService remains sole owner of study planning.  
3. No duplicate planning authority / parallel mission engine.  
4. No collector recursion (N/A for planning collectors; Experience bridges stay on legacy).  
5. Twin must not write Runtime A mission rows.  
6. Production defaults remain fail-open / OFF.  
7. Do not claim Twin Ready (T7).

**O:** No constitutional conflict requiring STOP — projection-only cutover with legacy persistence satisfies ownership.  
**E:** EP-001.2 + EP-002.2 MissionOptimizer decision + programme WS6.  
**C:** Implementation authorised under consumer_chain + PlanningService facade.

---

## 8. Insertion point

| Layer | Change |
|---|---|
| `consumer_chain/daily_plan_dual_run.py` | Diagnostic compare |
| `consumer_chain/daily_plan_cutover.py` | Eligibility, projection, orchestration |
| `PlanningService.get_dashboard_mission_surface` | HTTP facade |
| `dashboard/routes.py`, `mission/routes.py` | Call facade |
| Experience MissionStartAdapter | **Unchanged** |

---

## 9. Discovery conclusion

**R:** Proceed to Constitutional Impact Assessment + Cutover Design, then implement dual-run + gated cutover mirroring EP-002.5/6. Hard-delete of MissionOptimizer remains optional / deferred (code quarantine already sufficient).
