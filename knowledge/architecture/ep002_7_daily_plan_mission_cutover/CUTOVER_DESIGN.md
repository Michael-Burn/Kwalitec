# EP-002.7 — Cutover Design

**Milestone:** EP-002.7 — Daily Plan & Mission Dual-Run and Gated HTTP Cutover  
**Date:** 2026-07-26  
**Status:** Binding design for implementation

---

## 1. Intent

```
Dashboard / Missions request
        │
        ▼
PlanningService.get_dashboard_mission_surface()
        │
        ├─ cutover ineligible
        │       ├─ generate_today_mission (legacy)
        │       └─ dual-run side-car when Twin ON ∧ non-prod
        │
        └─ cutover eligible
                │
                ├─ compute legacy mission (fail-open + alignment baseline + ORM anchor)
                ├─ build_daily_study_plan()  (fail-open)
                │
                ├─ Twin None / exception / blocking limitation
                │         └──► return legacy surface
                │
                └─ Twin success + non-blocking
                          └──► project → mission surface DTO
                               (MissionDisplayProxy title overlay)
                               record semantic alignment
                               return projection (influences_student=True)
```

Student always receives a valid surface (legacy or projected). Dual-run never changes student payloads. MissionOptimizer is never called.

---

## 2. Dual-run (diagnostic)

| Rule | Behaviour |
|---|---|
| Eligibility | Twin ON ∧ non-production `APP_ENV` |
| Host | Surface facade when cutover **not** eligible/active |
| Compare | Legacy mission vs `build_daily_study_plan` |
| Capture | Topic / objective / sequencing / workload agreement, fingerprints, latencies |
| Influence | `influences_student=False` always |
| Fail-open | Twin exceptions swallowed |
| Skip when | Daily plan cutover eligible or active |

---

## 3. Cutover eligibility

| Condition | Required |
|---|---|
| `ENABLE_DIGITAL_TWIN` | True |
| `ENABLE_DAILY_PLAN_CUTOVER` | True |
| `APP_ENV` / `FLASK_ENV` | Not `production` / `prod` |

Post-Twin serving gates: non-`None` dict; no exception; no blocking limitation; non-empty `today_missions`; legacy ORM mission present for projection anchor.

---

## 4. Fallback rules

| Trigger | Reason code |
|---|---|
| Twin OFF | `twin_off` |
| Cutover flag OFF | `cutover_flag_off` |
| Production env | `production_env` |
| Config failure | `configuration_failure` |
| Twin `None` | `twin_unavailable` |
| Twin raises | `twin_exception` |
| Blocking limitation | `blocking_limitation` |
| Empty / unanchored projection | `projection_empty` |

---

## 5. Blocking limitations

```
BLOCKING_CODES = {
  twin_foundation_flag_off,
  canonical_learner_state_unavailable,
  invalid_student_id,
}
```

Also blocking when `availability` present and not `available`, or `today_missions` empty.

---

## 6. Projection contract

| Twin field | Surface field |
|---|---|
| Primary `today_missions` slot | `today_mission.title` via `MissionDisplayProxy` |
| Legacy Mission ORM | `id` / `status` / `tasks` / `mission_date` proxied |
| `today_missions` | `today_missions_slots` |
| `recommended_workload` | `recommended_workload` |
| `topic_ordering` / `revision_priorities` | passthrough |
| `limitations_codes` / `explainability` | passthrough |
| constant | `source_authority="daily_study_plan"` |

---

## 7. Semantic alignment

| Status | Meaning |
|---|---|
| `aligned` | Topic ∧ objective ∧ sequencing ∧ workload agreement |
| `mismatched` | Twin served but one or more dimensions disagree |
| `twin_unavailable` | Pre-attempt or Twin failure fallback |
| `limitation_fallback` | Blocking / empty projection |

---

## 8. Module layout

| Module | Role |
|---|---|
| `daily_plan_dual_run.py` | Side-car compare |
| `daily_plan_cutover.py` | Eligibility, projection, orchestration |
| `daily_plan_*_health.py` | Metrics |
| `v2_flags.py` | `ENABLE_DAILY_PLAN_CUTOVER` |

---

## 9. Rollback

Kill switches: Cutover OFF → Twin OFF → production env. See `ROLLBACK_PLAN.md`.
