# EP-002.7 — Student Impact Assessment

**Milestone:** EP-002.7  
**Date:** 2026-07-26

| Cohort | Student-visible impact |
|---|---|
| Production | **None** — production always ineligible |
| Non-prod Twin OFF | **None** |
| Non-prod Twin ON + Cutover OFF | **None visible** (dual-run diagnostic only) |
| Non-prod Twin ON + Cutover ON + success | Dashboard / `/missions` today-mission title/narrative may reflect Twin plan slots |
| Eligible but Twin failure / blocking | **None vs legacy** — fail-open |

## Surfaces

| Surface | In scope? |
|---|---|
| `/dashboard` today mission card | **Yes** |
| `/missions` today mission + narrative | **Yes** |
| Mission session start / tasks | ORM mission retained (legacy persistence) |
| Experience MissionStartAdapter | **No** |
| StudyPlanService.synchronize_student_surfaces | **No** (still `generate_today_mission`) |
| Analytics | **No** |

**O:** Blast radius bounded to Runtime A dashboard + missions under explicit non-prod gates.  
**E:** Route wiring; Experience adapter unchanged.  
**C:** Matches programme WS6 intent.  
**R:** Keep production OFF; soak staging before broader discussion.
