# Unvalidated Assumptions

**Programme:** P-003.4 — Product Assumption Register  
**Date:** 2026-07-26  
**Status:** UNVALIDATED index (Hypothesis + Supported)  
**Canonical cards:** [`PRODUCT_ASSUMPTION_REGISTER.md`](PRODUCT_ASSUMPTION_REGISTER.md)

This index lists assumptions that are **believed** or **partially evidenced** but are **not** yet outcome-validated for the claim class. Product Board must not treat these as closed knowledge for Version 1 declaration.

**Board question answered here:** *What do we believe, and what still requires evidence?*

---

## Board reading order (15 minutes)

1. **Hypothesis first (must not overclaim):** PA-039 → PA-014 → PA-011 → PA-010  
2. **Supported educational usefulness:** PA-001 → PA-017 → PA-018 → PA-037 → PA-038  
3. **Supported product / journey:** PA-007 → PA-004 → PA-016  
4. **Supported ops / research:** PA-033 → PA-036 → PA-013  

---

## A. Hypothesis — believed; insufficient evidence

| ID | Title | Category | Confidence | What would validate / falsify |
|---|---|---|---|---|
| [PA-010](PRODUCT_ASSUMPTION_REGISTER.md#pa-010--linear-session-stages-aid-clear-progression-perception) | Linear session stages aid progression perception | Product | Low | Stage 1 interviews + completion telemetry |
| [PA-011](PRODUCT_ASSUMPTION_REGISTER.md#pa-011--personalisation-improves-educational-usefulness-when-tertiary-and-visible) | Personalisation improves educational usefulness | Educational | Low | Flags ON + dogfood + cohort + G12; else stays Δ = 0 |
| [PA-014](PRODUCT_ASSUMPTION_REGISTER.md#pa-014--runtime-a-recommendations-improve-study-behaviour-when-accepted) | Runtime A recommendations improve study behaviour | Behavioural | Low | Stage 1 uptake + M-series; DR-036 freeze until then |
| [PA-039](PRODUCT_ASSUMPTION_REGISTER.md#pa-039--perception-gains-cause-better-study-behaviour-over-time) | Perception gains → better study behaviour | Behavioural | Low | EP-007.3 Stage 1 ops; never from Tier B alone |

**Count:** 4

---

## B. Supported — credible evidence; not outcome-validated

| ID | Title | Category | Confidence | Evidence class | Gap to Validated |
|---|---|---|---|---|---|
| [PA-001](PRODUCT_ASSUMPTION_REGISTER.md#pa-001--better-explanations-improve-student-trust) | Better explanations improve trust | Educational | Medium | Tier B + K8 70 | External trust↔uptake link |
| [PA-004](PRODUCT_ASSUMPTION_REGISTER.md#pa-004--students-trust-falsifiable-syllabus-rules-more-than-composite-intelligence-speech) | Falsifiable rules beat composite speech | Behavioural | Medium | Blind SV-014 | Stage 1 comparison |
| [PA-007](PRODUCT_ASSUMPTION_REGISTER.md#pa-007--canonical-home-under-sole-runtime-reduces-organisational-friction) | Canonical Home reduces friction | Behavioural | Medium | Tier B EP-007.2; K1 72 | External corroboration; not topic quality |
| [PA-013](PRODUCT_ASSUMPTION_REGISTER.md#pa-013--record-only-learning-feedback-enables-trustworthy-future-adaptation) | Record-only feedback enables future adaptation | Architecture | Medium / Low* | Structural EP-003.4 | K6 outcome under emit ON |
| [PA-016](PRODUCT_ASSUMPTION_REGISTER.md#pa-016--single-primary-recommendation-cta-reduces-decision-burden) | Single primary CTA reduces burden | Product | Medium | DR-050 + dual-home contrast | Isolated CTA perception pack |
| [PA-017](PRODUCT_ASSUMPTION_REGISTER.md#pa-017--students-understand-readiness-drivers-and-provisional-confidence-when-mes-rendered-on-home) | Students understand readiness drivers/confidence | Educational | Medium | Tier B EP-006.5; K3 65 | Stage 1 calibration interviews |
| [PA-018](PRODUCT_ASSUMPTION_REGISTER.md#pa-018--bare-readiness-percentage-without-drivers-risks-false-precision) | Bare % risks false precision | Educational | Medium–High | RC-04; PR-005; SV-013 | Durable W-PROD spot-checks |
| [PA-033](PRODUCT_ASSUMPTION_REGISTER.md#pa-033--feature-flag-matrix-discipline-g12-is-required-before-educational-flags-on) | G12 discipline before flags ON | Operational | Medium | DR-043; PR-012 | G12 PASS package |
| [PA-036](PRODUCT_ASSUMPTION_REGISTER.md#pa-036--tier-b-perception-packs-can-raise-specific-ksi-categories-without-clearing-g1) | Tier B can raise categories without clearing G1 | Research | Medium | KSI 59→62 path | Next board + G1.7 |
| [PA-037](PRODUCT_ASSUMPTION_REGISTER.md#pa-037--planning-usefulness-requires-one-coherent-tonight-plan-without-conflicts) | One coherent tonight-plan for K1 | Educational | Medium | K1 72; REM-02/03 | Topic quality + external N |
| [PA-038](PRODUCT_ASSUMPTION_REGISTER.md#pa-038--readiness-usefulness-depends-on-unpackable-drivers-and-honest-refusal) | Readiness needs drivers + honesty | Educational | Medium | K3 65; EP-006.5 | External corroboration |

\* Structural support Medium; K6 student-outcome claim Low.

**Count:** 11

---

## Combined unvalidated total

| Set | Count |
|---|---:|
| Hypothesis | 4 |
| Supported | 11 |
| **Unvalidated total** | **15** |

---

## Claim discipline

| Temptation | Correct handling |
|---|---|
| “K8 70 proves students trust us enough to ship V1” | PA-001 Supported only; PA-021 bar unmet; PA-025 Rejected |
| “Personalisation will lift K4” | PA-011 Hypothesis; W-PROD Δ = 0 while OFF |
| “Recommendations work” | PA-014 Hypothesis; DR-036 freeze |
| “Journey Pass proves consistency” | PA-039 Hypothesis; EP-007.3 unsupported if claimed |
| “G12 is done enough to flip flags” | PA-033 Supported; PR-012 still open |

Known / disproved: [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) · [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md)
