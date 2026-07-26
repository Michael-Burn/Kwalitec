# EP-005.1 — Validated KSI Report

**Programme:** EP-005.1 — KSI Validation & Evidence Collection  
**Version:** 1.0  
**Status:** Active validated assessment (W-PROD)  
**Assessment date:** 2026-07-26  
**Method:** [`VALIDATION_METHODOLOGY.md`](VALIDATION_METHODOLOGY.md)  
**Evidence:** [`KSI_EVIDENCE_REGISTER.md`](KSI_EVIDENCE_REGISTER.md)  
**Confidence:** [`CONFIDENCE_ASSESSMENT.md`](CONFIDENCE_ASSESSMENT.md)  
**Baseline authority:** `../p001_1_ksi_baseline/BASELINE_KSI_ASSESSMENT.md` (KSI **58**)  
**Does not:** Claim exam pass-rate proof; does not change product behaviour; does not declare Version 1 production-ready  

---

## 1. Executive summary

| Measure | Value |
|---|---|
| Baseline KSI | **58** |
| Naive sum of programme estimated ΔKSI (EP-003.1–004.3) | **≈ +12.0** → ~70 (**not claimable** — double-count + gated flags) |
| De-duplicated estimated KSI (W-PROD only) | **≈ 60** |
| De-duplicated estimated KSI (W-GATED optimistic stack) | **≈ 66** (still estimate) |
| **Validated KSI (W-PROD)** | **59** |
| Version 1 target | **≥ 80** |
| Gap remaining | **21 points** |
| Composite confidence | **Medium** (structural Medium; student-perception Low — see confidence report) |
| Largest validated residual risks | K8 &lt; 70; no Tier B post-change perception; personalisation/feedback OFF |

**Verdict:** EP-003.1–.3 delivered **partially validated structural usefulness** on recommendation, planning, readiness, and explainability contracts. EP-003.4 and EP-004.1–.3 estimated personalisation / feedback gains are **unsupported in production defaults**. Validated educational usefulness remains **far below** Version 1 KSI ≥ 80. Gate G1 **FAIL** — see [`VERSION_1_G1_STATUS.md`](VERSION_1_G1_STATUS.md).

---

## 2. Estimated inventory (inputs only)

| Programme | Primary categories | Estimated weighted ΔKSI | Production activation |
|---|---|---:|---|
| EP-003.1 | K2, K8 | +1.7 | Runtime A path (no new flag) |
| EP-003.2 | K3, K8 | +1.9 | Runtime A path (no new flag) |
| EP-003.3 | K1, K8 | +2.0 | Runtime A path (no new flag) |
| EP-003.4 | K6, K4 | +0.8 | Flag OFF default |
| EP-004.1 | K4 | +1.1 | Flag OFF default |
| EP-004.2 | K4, K2 | +2.2 | Flag OFF default |
| EP-004.3 | K4, K1 | +2.3 | Flag OFF default |
| **Naive total** | | **≈ +12.0** | Mixed |

**Reconciliation notes:**

1. Each programme measured largely against the **same baseline** — summing ΔKSI double-counts K4/K8 and overstates composite movement.  
2. EP-003.1’s KSI table listed K3 baseline 60 vs published baseline **52** — documentation inconsistency; validation uses P-001.1 published baseline.  
3. Programmes themselves labelled live re-score **Pending**.

### 2.1 De-duplicated estimated category posture (planning aid)

| ID | Baseline | W-PROD de-dup est. | W-GATED add (est.) | Notes |
|---|---:|---:|---:|---|
| K1 | 62 | 69 | +5 → 74 | Primary from EP-003.3; EP-004.3 gated |
| K2 | 48 | 54 | +4 → 58 | Primary from EP-003.1; EP-004.2 gated |
| K3 | 52 | 60 | 0 | EP-003.2 only |
| K4 | 55 | 57 | +11 → ~68 | Prod: minor EP-003 spill only; gated closed-loop |
| K5 | 60 | 60 | 0 | No direct programme claim |
| K6 | 50 | 50 | +6 → 56 | Feedback OFF in W-PROD |
| K7 | 58 | 60 | +3 → 63 | Weak estimate trail |
| K8 | 55 | 63 | +2 → 65 | De-duped MES lifts; still estimate |
| **KSI** | **58** | **≈ 60** | **≈ 66** | Estimates only |

---

## 3. Validated category scores (W-PROD)

| ID | Category | Weight | Baseline | Validated | Δ | Weighted | Band | Confidence |
|---|---|---:|---:|---:|---:|---:|---|---|
| K1 | Planning usefulness | 15 | 62 | **68** | +6 | 10.20 | Partial | Medium |
| K2 | Recommendation usefulness | 15 | 48 | **53** | +5 | 7.95 | Partial | Medium |
| K3 | Readiness usefulness | 12 | 52 | **57** | +5 | 6.84 | Partial | Medium |
| K4 | Personalisation | 12 | 55 | **55** | 0 | 6.60 | Partial | High |
| K5 | Motivation | 10 | 60 | **60** | 0 | 6.00 | Partial | Medium |
| K6 | Learning analytics | 10 | 50 | **50** | 0 | 5.00 | Partial | High |
| K7 | Revision support | 12 | 58 | **58** | 0 | 6.96 | Partial | Medium |
| K8 | Explainability | 14 | 55 | **65** | +10 | 9.10 | Partial | Medium |
| | **Validated KSI** | **100** | **58** | **59** | **+1** | **58.65 → 59** | Partial | Medium |

\*K4/K6 “High” confidence means high confidence that **no W-PROD lift** is justified (flag OFF / no student analytics UX) — not high confidence of excellence.

### 3.1 Scoring rationales

**K1 Planning usefulness — 68 (Partial; Medium)**  
Tier A: planning quality contract, schema completeness, recovery paths, Explainability Review Pass (EV-PLAN-001…003). Estimated +7 → 69. Validated +6 (≤50% haircut not needed fully because contract tests are strong, but Tier C dual-home / duration mismatch themes remain un-retested — EV-PLAN-006). Remains below Strong band and below estimated 69.

**K2 Recommendation usefulness — 53 (Partial; Medium)**  
Tier A: Decision Framework, plan-coherence labelling, refusal, Recommendation + Explainability checklist Pass (EV-REC-001…003). Estimated +6 → 54. Validated +5. Clears V1-K2 floor (≥50) structurally. Does **not** validate acceptance/effectiveness; marketing freeze intact; Coach opacity corpus (EV-PERC-002) not re-measured post-change.

**K3 Readiness usefulness — 57 (Partial; Medium)**  
Tier A: drivers, confidence labels, honest refusal, checklist Pass (EV-RDY-001…003). Estimated +8 → 60. Validated +5 (≤50% of estimated Δ under methodology §7 given missing Tier B and unpackability themes EV-RDY-005). Integrity preserved more than Strong-band usefulness proven.

**K4 Personalisation — 55 (Partial; High that Δ=0)**  
Profile + closed-loop personalisation exist as gated capability (EV-PERS-001…003) but `ENABLE_PERSONAL_LEARNING_PROFILE` default OFF (EV-PERS-005). W-PROD validated Δ = **0**. W-GATED estimates remain **unsupported** for G1.

**K5 Motivation — 60 (Partial; Medium)**  
No direct EP-003/004 motivation programme. Retained at baseline. Consequence metric; may move after K1/K2/K8 perception re-test.

**K6 Learning analytics — 50 (Partial; High that Δ=0)**  
Learning Feedback Loop implemented but flag OFF (EV-FB-001, EV-FB-004); Journey emit deferred; Week 0 scorecard insufficient N (EV-PERC-003). W-PROD validated Δ = **0**. Estimated K6 +6 unsupported for production defaults.

**K7 Revision support — 58 (Partial; Medium)**  
Minor estimated lifts from planning/personalisation programmes lack Tier B and are partly gated. Validated Δ = **0** in W-PROD.

**K8 Explainability — 65 (Partial; Medium)**  
Tier A: Mandatory Explanation Schema on Rec / Plan / Readiness with checklist Pass (EV-EXP-001). De-duplicated estimated ~63–65. Validated **65** credits structural MES delivery. Remains **below V1-K3 floor of 70** because Near-Universal Coach opacity themes (EV-EXP-003) have no post-change Tier B clearance.

---

## 4. Estimated vs validated vs unsupported

| Claim class | Definition | Examples this window |
|---|---|---|
| **Validated improvement** | Tier A (+ conservative credit) supports W-PROD score &gt; baseline | K1 +6; K2 +5; K3 +5; K8 +10 |
| **Partially validated** | Structural eligibility proven; student perception not re-proven | All four lifts above |
| **Estimated only (retained as forecast)** | Programme Δ still useful for roadmap; not G1 input | W-GATED K4/K1/K2/K6/K7/K8 add-ons; naive +12 stack |
| **Unsupported assumption** | Would require evidence that does not exist or contradicts rules | “KSI ≈ 70 from summing EP reports”; “personalisation useful in production defaults”; “K8 ≥ 70 from checklist Pass alone”; “educational effectiveness GO” |

### 4.1 Dimension evaluation summary

| Dimension | Estimated | Validated (W-PROD) | Unsupported |
|---|---|---|---|
| Recommendation usefulness | K2 → 54 (+ EP-004.2) | **53** | Acceptance KPIs; marketing effectiveness |
| Planning usefulness | K1 → 69 (+ EP-004.3) | **68** | Dual-home/duration fixed for students |
| Readiness usefulness | K3 → 60 | **57** | Unpackability resolved |
| Explainability | K8 → 63–65 | **65** (&lt;70) | Coach trust cured |
| Personalisation usefulness | K4 → 62–68 | **55** (no lift) | Flag-OFF closed-loop value |
| Learning feedback quality | K6 → 56 | **50** (no lift) | Student analytics UX from feedback events |

---

## 5. Comparison to Version 1 KSI-lens criteria (informational)

| Criterion | Required | Validated result | Met? |
|---|---|---|---|
| V1-K1 KSI ≥ 80 | ≥ 80 | **59** | **No** |
| V1-K2 No category &lt; 50 | Floor 50 | Min = K2 **53**, K6 **50** | **Yes** (bare) |
| V1-K3 K8 ≥ 70 | ≥ 70 | **65** | **No** |
| V1-K5 EP-003/004 not NO-GO | Not effectiveness NO-GO | Effectiveness **NO-GO** / PENDING EVIDENCE | **No** |
| V1-K7 Distinguish KSI vs pass-rate | Claim language | This report complies | **Yes** |

Full Gate G1 board: [`VERSION_1_G1_STATUS.md`](VERSION_1_G1_STATUS.md).

---

## 6. What would move validated KSI next

Ordered by expected validated (not estimated) contribution:

1. **Post-change blind re-review / interviews** after MES surfaces (clears Tier B for K8/K2/K3).  
2. **Close dual-home / duration mismatch** perception gaps (unlocks K1 Strong).  
3. **Stage 1 external cohort** with filled M1–M9 (raises confidence; enables ≥70 claims).  
4. **Controlled flag-ON dogfood** for feedback + profile + personalisation, then re-score W-GATED → candidate W-PROD only after soak.  
5. **Do not** declare Version 1 production-ready on estimated stacks.

---

## 7. Non-claims

This validated assessment does **not** claim:

- measured exam pass-rate improvement;  
- Twin Ready / production Twin authority;  
- recommendation-effectiveness marketing clearance;  
- that KSI 59 is a live telemetry readout;  
- that EP-004 personalisation is student-visible under production defaults;  
- Version 1 production-ready.

---

## 8. Independent re-score note (G1.7)

Procedure: a second Product assessor may re-score this package using the same Evidence Register. Divergence &gt; ±3 KSI → STOP and escalate per PSF §5.5.  
**Status this window:** Single assembled assessment; second-assessor pass **optional until declaration board** (GAP-05). For G1 scoring, treat as **HOLD on G1.7 formality** but not as a reason to raise scores.

---

## References

- [`VALIDATION_METHODOLOGY.md`](VALIDATION_METHODOLOGY.md)  
- [`KSI_EVIDENCE_REGISTER.md`](KSI_EVIDENCE_REGISTER.md)  
- [`CONFIDENCE_ASSESSMENT.md`](CONFIDENCE_ASSESSMENT.md)  
- [`VERSION_1_G1_STATUS.md`](VERSION_1_G1_STATUS.md)  
- `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`  
- `../p001_1_ksi_baseline/BASELINE_KSI_ASSESSMENT.md`  

---

**End of VALIDATED_KSI_REPORT**
