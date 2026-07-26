# EP-002.7 — Constitutional Impact Assessment

**Milestone:** EP-002.7  
**Date:** 2026-07-26  
**Legend:** **O** · **E** · **C** · **R**

---

## 1. Ownership matrix (pre → post)

| Concern | Owner (binding) | Pre-EP-002.7 | Post-EP-002.7 | Evidence |
|---|---|---|---|---|
| Learner-state read model | Twin Foundation | Unchanged | Unchanged | No Twin package redesign |
| Daily plan slots / workload | PlanningService + EP-001.2 | `build_daily_study_plan` observability only | Same API; gated HTTP projection | `daily_plan_cutover.py` calls PlanningService only |
| Mission ORM persistence | PlanningService | `generate_today_mission` | **Unchanged** (still sole writer) | Facade always computes legacy; Twin overlays display |
| MissionOptimizer | Quarantined | Soft-deprecated | Soft-deprecated | No imports in cutover/dual-run; decision tests pass |
| Readiness evaluation | ReadinessService | Unchanged | Unchanged | Independent flag |
| Insight communication | RecommendationService | Unchanged | Unchanged | Independent flag |
| Curriculum order | CurriculumService | Unchanged | Unchanged | No curriculum diffs |
| Runtime A writes | SQL services | Unchanged | Unchanged | Twin does not `db.session` mission rows |

**O:** Cutover changes **who narrates today’s focus on eligible HTTP surfaces**, not who owns planning maths or ORM writes.  
**E:** `MissionDisplayProxy` overrides title only; `generate_today_mission` source has no cutover import.  
**C:** Ownership matrix preserved.  
**R:** Reject any follow-up that lets Twin persist missions or re-wires MissionOptimizer.

---

## 2. Constraints verified

| Constraint | Status | Evidence |
|---|---|---|
| MissionOptimizer quarantined | **Pass** | Source guards; EP-002.2 decision tests |
| PlanningService sole planning owner | **Pass** | Cutover invokes `build_daily_study_plan` / `generate_today_mission` only |
| No duplicate planning authority | **Pass** | Single facade; Optimizer unused |
| No collector recursion | **Pass** | N/A — planning has no readiness-style collector wrap; bridges untouched |
| No ownership drift | **Pass** | Authority matrix unchanged |
| No parallel mission engine | **Pass** | No new engine package |
| Fail-open legacy | **Pass** | Unit tests for Twin OFF / flag OFF / production / None / exception / blocking |
| Production ineligible | **Pass** | Eligibility helper + tests |

---

## 3. Accepted constitutional posture for display vs persistence

**O:** Twin plan is regenerable and does not write missions (EP-001.2).  
**E:** Session start requires Mission.id; templates need ORM tasks.  
**C:** Eligible cutover serves Twin **display** projection over a legacy ORM mission anchor. Session execution topic may still follow legacy generation until a later PlanningService-owned generation milestone.  
**R:** Track as known limitation TD-DP-01; do not treat as ownership violation because Twin never writes and PlanningService still owns both APIs.

---

## 4. Recommendation

**Accept** constitutional posture for EP-002.7 implementation. No STOP condition triggered.
