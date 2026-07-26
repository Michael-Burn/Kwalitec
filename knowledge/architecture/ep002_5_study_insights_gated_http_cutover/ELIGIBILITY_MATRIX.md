# EP-002.5 — Eligibility Matrix

**Milestone:** EP-002.5 — Study Insights Gated HTTP Cutover  
**Date:** 2026-07-26  
**Binding:** Yes

---

## 1. Flag × environment matrix

| Twin | Cutover | Authority | `APP_ENV` | Attempt cutover? | Student response |
|---|---|---|---|---|---|
| OFF | * | * | any | No | Legacy |
| ON | OFF | * | non-prod | No | Legacy (+ dual-run diagnostic) |
| ON | OFF | * | production | No | Legacy |
| ON | ON | OFF | non-prod | **Yes** | Twin projection if Twin success + non-blocking; else legacy |
| ON | ON | ON | non-prod | **Yes** | Same (Authority recorded only) |
| ON | ON | * | production / prod | No | Legacy |
| OFF | ON | * | any | No | Legacy |

---

## 2. Post-attempt serving matrix

| Twin result | Blocking limitation? | Student response | Alignment status |
|---|---|---|---|
| Exception | — | Legacy | `twin_unavailable` |
| `None` | — | Legacy | `twin_unavailable` |
| Dict | Yes | Legacy | `limitation_fallback` |
| Dict | No; projection empty | Legacy | `limitation_fallback` |
| Dict | No; projection non-empty | **Study Insights projection** | `aligned` or `mismatched` |

---

## 3. Blocking limitation codes

| Code | Blocking? |
|---|---|
| `twin_foundation_flag_off` | Yes |
| `canonical_learner_state_unavailable` | Yes |
| `invalid_student_id` | Yes |
| `todays_key_focus_unavailable` **and** `recommended_next_action_unavailable` | Yes |
| Both focus + next-action fields `None` | Yes |
| `sparse_evidence` alone | No |
| `planner_outputs_unavailable` alone | No |
| `readiness_intelligence_unavailable` alone | No |
| Single field `*_unavailable` with other actionable field present | No |

---

## 4. Surface scope

| Surface | In EP-002.5 cutover scope? |
|---|---|
| Dashboard / Home recommendation list (`/dashboard`) | **Yes** |
| Educational Intelligence recommendation card path | No (unchanged mutual exclusion) |
| Experience Recommendation Bridge | No (still calls legacy `generate_recommendations`) |
| Founder recommendation providers | No |

---

## 5. Kill switches (immediate legacy)

1. Unset / falsy `KWALITEC_STUDY_INSIGHTS_CUTOVER`  
2. Unset / falsy `KWALITEC_DIGITAL_TWIN`  
3. Set `APP_ENV=production` (or `prod`)  
