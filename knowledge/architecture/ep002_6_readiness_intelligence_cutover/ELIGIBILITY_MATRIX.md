# EP-002.6 — Eligibility Matrix

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
**Date:** 2026-07-26  
**Binding:** Yes

---

## 1. Dual-run matrix (diagnostic only)

| Twin | Cutover | `APP_ENV` | Dual-run? | Student response |
|---|---|---|---|---|
| OFF | * | any | No | Legacy |
| ON | OFF | non-prod | **Yes** (side-car) | Legacy |
| ON | OFF | production | No | Legacy |
| ON | ON | non-prod | No (cutover owns Twin call) | See cutover matrix |
| ON | ON | production | No | Legacy |

---

## 2. Flag × environment cutover matrix

| Twin | Cutover | Authority | `APP_ENV` | Attempt cutover? | Student response |
|---|---|---|---|---|---|
| OFF | * | * | any | No | Legacy |
| ON | OFF | * | non-prod | No | Legacy (+ dual-run) |
| ON | OFF | * | production | No | Legacy |
| ON | ON | OFF | non-prod | **Yes** | Twin projection if success + non-blocking; else legacy |
| ON | ON | ON | non-prod | **Yes** | Same (Authority recorded only) |
| ON | ON | * | production / prod | No | Legacy |
| OFF | ON | * | any | No | Legacy |

---

## 3. Post-attempt serving matrix

| Twin result | Blocking limitation? | Student response | Alignment status |
|---|---|---|---|
| Exception | — | Legacy | `twin_unavailable` |
| `None` | — | Legacy | `twin_unavailable` |
| Dict | Yes | Legacy | `limitation_fallback` |
| Dict | No; score missing | Legacy | `limitation_fallback` |
| Dict | No; score present | **Readiness Intelligence projection** | `aligned` or `mismatched` |

---

## 4. Blocking limitation codes

| Code / condition | Blocking? |
|---|---|
| `twin_foundation_flag_off` | Yes |
| `canonical_learner_state_unavailable` | Yes |
| `invalid_student_id` | Yes |
| `readiness_score is None` | Yes |
| `availability` present and not `available` | Yes |
| `planner_outputs_unavailable` alone | No |

---

## 5. Surface scope

| Surface | Dual-run | Cutover |
|---|---|---|
| Dashboard readiness score + weak/strong | Yes | Yes |
| Analytics readiness score + weak/strong | Yes | Yes |
| Collectors / Adaptive TwinInput | No | No |
| Settings export | No | No |
| Experience `/student` TwinPort | No | No |
| Review backlog / streaks widgets | No | No |

---

## 6. Kill switches (immediate legacy)

1. Unset / falsy `KWALITEC_READINESS_INTELLIGENCE_CUTOVER`  
2. Unset / falsy `KWALITEC_DIGITAL_TWIN`  
3. Set `APP_ENV=production` (or `prod`)
