# EP-002.8 — Student Impact Assessment

**Milestone:** EP-002.8  
**Date:** 2026-07-26

---

## 1. Blast radius

| Cohort | Env | Flags | Student-visible change from EP-002.8 alone |
|---|---|---|---|
| Production (default) | production | Twin OFF, cutovers OFF | **None** — still legacy EIP-003 via facade |
| Non-prod, Twin OFF | any | defaults | **None** |
| Non-prod, Twin ON, cutovers OFF | non-prod | Dual-run only | **None** — HTTP still legacy |
| Non-prod, Twin ON + Insights cutover | non-prod | Insights ON | Same Insight copy as EP-002.5; selection centralised |
| Non-prod, Twin ON + Readiness cutover | non-prod | Readiness ON | Composite narrative sourced from Twin drivers/confidence (closes double-narration) |
| Non-prod, Twin ON + Daily Plan cutover | non-prod | Daily Plan ON | Same Twin mission reason; structured `MissionNarrative` |
| EI Stage A ON | any | EI flags | Mutual exclusion unchanged |
| SOLE_RUNTIME ON | any | Sole runtime | Redirect to `/student/*` unchanged |

---

## 2. Educational honesty

| Risk | Mitigation |
|---|---|
| Twin narrative invents certainty | Adapter only maps authorised surface fields; estimate language retained |
| Students see conflicting Twin + EIP-003 copy | Selection facade prevents dual speech on same concern |
| Fail-open cohort sees different copy | Expected and honest — legacy EIP-003 |

---

## 3. Student Impact Scope

**Scope rating:** **Low / presentation-only.**  
No change to who is eligible for Twin payloads. No production activation. Behaviour outside eligible cohorts identical to pre-EP-002.8.

---

## 4. Accessibility impact

No structural template rewrite. Macro and ARIA attributes preserved. Accessibility regressions expected: **none**.
