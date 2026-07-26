# EP-002.7 — Eligibility Matrix

**Milestone:** EP-002.7  
**Date:** 2026-07-26  
**Binding:** Yes

---

## 1. Dual-run matrix

| Twin | Cutover | `APP_ENV` | Dual-run? | Student response |
|---|---|---|---|---|
| OFF | * | any | No | Legacy |
| ON | OFF | non-prod | **Yes** | Legacy |
| ON | OFF | production | No | Legacy |
| ON | ON | non-prod | No (cutover owns Twin call) | See cutover |
| ON | ON | production | No | Legacy |

---

## 2. Cutover matrix

| Twin | Cutover | Authority | `APP_ENV` | Attempt? | Student response |
|---|---|---|---|---|---|
| OFF | * | * | any | No | Legacy |
| ON | OFF | * | non-prod | No | Legacy (+ dual-run) |
| ON | ON | OFF | non-prod | **Yes** | Twin projection if success; else legacy |
| ON | ON | ON | non-prod | **Yes** | Same (Authority recorded only) |
| ON | ON | * | production / prod | No | Legacy |

---

## 3. Post-attempt serving

| Twin result | Blocking? | Student response |
|---|---|---|
| Exception / `None` | — | Legacy |
| Dict | Yes | Legacy |
| Dict | No; no legacy mission anchor | Legacy (`projection_empty`) |
| Dict | No; slots present + legacy anchor | **Daily plan projection** |

---

## 4. Surface scope

| Surface | Dual-run | Cutover |
|---|---|---|
| Dashboard today mission | Yes | Yes |
| `/missions` today mission | Yes | Yes |
| Experience MissionStartAdapter | No | No |
| StudyPlanService sync | No | No |

---

## 5. Kill switches

1. Unset `KWALITEC_DAILY_PLAN_CUTOVER`  
2. Unset `KWALITEC_DIGITAL_TWIN`  
3. Ensure production processes never enable cutover
