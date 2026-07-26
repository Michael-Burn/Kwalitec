# Validated Assumptions

**Programme:** P-003.4 — Product Assumption Register  
**Date:** 2026-07-26  
**Status:** VALIDATED index  
**Canonical cards:** [`PRODUCT_ASSUMPTION_REGISTER.md`](PRODUCT_ASSUMPTION_REGISTER.md)

This index lists assumptions the Product Board may treat as **known** for the stated claim window (2026-07-26 evidence freeze). Validated ≠ Version 1 production-ready.

**Board question answered here:** *What do we know?*

---

## Board reading order (10 minutes)

1. **PA-026 → PA-021 → PA-022** (effectiveness / KSI law)  
2. **PA-029 → PA-030 → PA-031 → PA-034** (who owns educational truth)  
3. **PA-002 → PA-006 → PA-008** (validated student-experience root causes)  
4. **PA-020 → PA-040 → PA-035** (honesty, beta posture, research method)  
5. **PA-028 → PA-032** (determinism + curriculum invariants)  

---

## Validated cards

| ID | Title | Category | Confidence | Primary evidence |
|---|---|---|---|---|
| [PA-002](PRODUCT_ASSUMPTION_REGISTER.md#pa-002--schema-complete-mes-at-service-layer-is-insufficient-without-render-pass-through) | Service-layer MES ≠ student-visible explainability | Product | High | EP-005.2 RC-01; EP-006.1/006.2 |
| [PA-006](PRODUCT_ASSUMPTION_REGISTER.md#pa-006--dual-home-increases-decision-burden-and-caps-planning-trust) | Dual-home increases decision burden | Product | High | EP-005.2 RC-02; EP-006.3 unsupported “MES cures dual-home” |
| [PA-008](PRODUCT_ASSUMPTION_REGISTER.md#pa-008--same-day-duration-mismatch-undermines-planning-usefulness) | Same-day duration mismatch harms planning | Educational | High | EP-005.2 RC-03; DR-008 |
| [PA-020](PRODUCT_ASSUMPTION_REGISTER.md#pa-020--absence-of-evidence-must-remain-unknown-no-mastery--exam-ready-theatre) | Absence of evidence must remain unknown | Governance | High | Constitution; DR-024/035; EP-006.5 |
| [PA-021](PRODUCT_ASSUMPTION_REGISTER.md#pa-021--ksi--80-is-the-binding-usefulness-bar-for-version-1-product-success-claims) | KSI ≥ 80 required for V1 product-success claims | Release | High | PSF; G1.1; DR-025/051 |
| [PA-022](PRODUCT_ASSUMPTION_REGISTER.md#pa-022--ksi-is-a-usefulness-index-not-vision-2030s-north-star) | KSI ≠ Vision north star | Governance | High | DR-046; GOVERNANCE.md |
| [PA-026](PRODUCT_ASSUMPTION_REGISTER.md#pa-026--external-cohort-evidence-is-required-for-educational-effectiveness-clearance) | External validation required for effectiveness | Release | High | G1.9; EP-007.3; DR-022 |
| [PA-028](PRODUCT_ASSUMPTION_REGISTER.md#pa-028--planning-readiness-and-recommendations-must-be-deterministic) | Deterministic educational cores | Architecture | High | DR-013 |
| [PA-029](PRODUCT_ASSUMPTION_REGISTER.md#pa-029--runtime-a-is-sole-student-visible-educational-authority-under-w-prod) | Runtime A sole W-PROD authority | Architecture | High | DR-001; EP-002.9 |
| [PA-030](PRODUCT_ASSUMPTION_REGISTER.md#pa-030--twin--cutover-flags-default-off-fail-open-to-legacy) | Twin/cutover flags default OFF | Operational | High | DR-009/010 |
| [PA-031](PRODUCT_ASSUMPTION_REGISTER.md#pa-031--sole-runtime-unifies-chromejourney-not-twin-educational-truth) | Sole runtime ≠ Twin cutover | Architecture | High | DR-020 |
| [PA-032](PRODUCT_ASSUMPTION_REGISTER.md#pa-032--curriculum-v1-and-v2-must-both-remain-loadable) | Curriculum V1/V2 dual-loadability | Architecture | High | DR-011; G2.6 |
| [PA-034](PRODUCT_ASSUMPTION_REGISTER.md#pa-034--presentation-must-not-generate-educational-reasoning) | Presentation must not invent reasoning | Architecture | High | DR-005/019; EP-006.2 |
| [PA-035](PRODUCT_ASSUMPTION_REGISTER.md#pa-035--blind-student-only-reviews-yield-credible-qualitative-evidence) | Blind SV reviews are credible method | Research | High | EP-004 protocol; EP-005.1 |
| [PA-040](PRODUCT_ASSUMPTION_REGISTER.md#pa-040--invite-only-private-beta-with-privacy-review-protects-students-while-evidence-is-incomplete) | Invite-only + Privacy Review posture | Operational | High | DR-034/040 |

**Count:** 15

---

## What Validated does *not* mean

- Does **not** mean educational effectiveness is proven (see Rejected PA-025; Hypothesis PA-039).  
- Does **not** mean validated KSI ≥ 80 (bar is Validated as law; current score 62 is a risk — PR-002).  
- Does **not** authorise marketing claims beyond evidence (DR-021, DR-036).  

For believed-but-unproven items, see [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md).  
For disproved shortcuts, see [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md).
