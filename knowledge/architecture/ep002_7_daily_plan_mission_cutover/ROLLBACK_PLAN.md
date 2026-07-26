# EP-002.7 — Rollback Plan

**Milestone:** EP-002.7  
**Date:** 2026-07-26  
**Kill-switch first:** Yes

---

## 1. Intent

Restore legacy-only mission surfaces on dashboard/missions within one process
restart (or immediate env flip + restart), without schema rollback.

---

## 2. Primary kill switches (preferred order)

| Order | Action | Effect |
|---|---|---|
| 1 | `KWALITEC_DAILY_PLAN_CUTOVER=0` | Cutover attempts stop; dual-run may continue if Twin ON non-prod |
| 2 | `KWALITEC_DIGITAL_TWIN=0` | Twin OFF; cutover ineligible |
| 3 | Ensure production never has cutover ON | Production ineligible by design |

---

## 3. Verification checklist

1. Flag resolve: `ENABLE_DAILY_PLAN_CUTOVER is False` (and/or Twin OFF).  
2. Hit `/dashboard` and `/missions` → mission title matches legacy path.  
3. Cutover telemetry shows `cutover_served=False` (or no daily-plan cutover events).  
4. MissionOptimizer still unwired.  
5. Experience mission start still uses `generate_today_mission`.

---

## 4. What not to do

- Do not drop tables / reverse migrations (none).  
- Do not delete Twin / planner packages as “rollback.”  
- Do not un-quarantine MissionOptimizer during incident response.  
- Do not enable production Twin/Cutover to “test rollback.”
