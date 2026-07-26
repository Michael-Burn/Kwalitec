# P-004.1 — KSI Dimension Breakdown

**Programme:** P-004.1 — KSI Gap Analysis & Improvement Roadmap  
**Date:** 2026-07-26  
**Status:** Analysis only  
**Authority board:** EP-007.2 validated W-PROD scores (DR-051)  
**Target composite:** KSI ≥ **80**  
**Desired per-category posture for V1 portfolio:** Strong band (≥70), with several pillars mid-Strong (≥75) so the weighted sum can clear 80  
**Does not:** Re-score validated KSI (planning gaps only)

---

## 1. How to read this document

For each category K1–K8:

| Field | Meaning |
|---|---|
| **Current score** | Validated W-PROD category score (0–100) |
| **Desired score** | Planning target for Version 1 portfolio path (not a new validated claim) |
| **Gap** | Desired − current (category points) |
| **Weighted gap** | (weight/100) × gap ≈ composite KSI points if desired score achieved |
| **Confidence** | Confidence in the *current* validated score |
| **Evidence** | Primary paths / IDs supporting the current score |
| **Blockers** | What prevents the desired score today |

**Desired scores are planning anchors**, chosen so a realistic portfolio can reach composite ≥80 without requiring every category to be Excellent. Prefer-lower still applies at re-validation.

---

## 2. Composite snapshot

| ID | Category | Weight | Current | Desired | Gap | Weighted gap | Band now | Confidence |
|---|---|---:|---:|---:|---:|---:|---|---|
| K1 | Planning usefulness | 15 | 72 | 78 | +6 | +0.90 | Strong floor | Medium |
| K2 | Recommendation usefulness | 15 | 55 | 75 | +20 | **+3.00** | Partial | Medium |
| K3 | Readiness usefulness | 12 | 65 | 75 | +10 | +1.20 | Partial | Medium |
| K4 | Personalisation | 12 | 55 | 72 | +17 | **+2.04** | Partial | High (Δ=0 while OFF) |
| K5 | Motivation | 10 | 63 | 72 | +9 | +0.90 | Partial | Medium |
| K6 | Learning analytics | 10 | 50 | 70 | +20 | **+2.00** | Partial floor | High (Δ=0 while OFF) |
| K7 | Revision support | 12 | 58 | 72 | +14 | **+1.68** | Partial | Medium |
| K8 | Explainability | 14 | 70 | 78 | +8 | +1.12 | Strong floor | Medium |
| | **KSI** | **100** | **62** | **≈76*** | | **≈12.8*** | | Medium |

\* If *all* desired scores were achieved simultaneously and validated, illustrative composite ≈ **76** — still short of 80. Closing the last ~4 points requires either deeper lifts (e.g. K2→80, K4→78, K1→80) or additional Strong-band depth. See [`EXPECTED_KSI_IMPACT.md`](EXPECTED_KSI_IMPACT.md).

---

## 3. Category cards

### K1 — Planning usefulness (weight 15)

| Field | Value |
|---|---|
| **Current** | **72** |
| **Desired** | **78** |
| **Gap** | +6 category · ≈ +0.90 KSI |
| **Confidence (current)** | Medium |
| **Evidence** | EP-003.3 planning quality contract + Explainability Review Pass; EP-007.1 sole-runtime Home + unified duration; EP-007.2 Tier B N=9 (entry discoverability Pass; duration mismatch cleared on W-PROD); K1_REVALIDATION.md |
| **Scoring rationale** | Single coherent “what tonight” path is now student-perceivable on production sole-runtime. Prefer-lower stops mid-Strong; topic *selection quality* and sparse-content nights not Strong-validated; external N=0. |
| **Blockers to desired** | RC-11 topic quality unproven; JRN-PERC-02 sparse nights; dual-run Alpha residual (out of W-PROD); no Stage 1 M2/M4 adherence |
| **Related decisions / risks** | DR-027 prefer-lower; PA-007 Supported; PA-037 Supported; PR-008 confidence ceiling |
| **Highest-leverage next** | Do **not** rebuild Home. Improve sparse-content honesty + later personalisation of plan (gated). K1 is supporting, not P0 for the 18-pt gap. |

---

### K2 — Recommendation usefulness (weight 15)

| Field | Value |
|---|---|
| **Current** | **55** |
| **Desired** | **75** |
| **Gap** | +20 category · ≈ **+3.00 KSI** |
| **Confidence (current)** | Medium |
| **Evidence** | EP-003.1 Decision Framework + Recommendation/Explainability checklist Pass; EP-005.1 validated 53 → post-MES board 55; DR-050 single primary CTA; DR-036 effectiveness marketing freeze; no acceptance KPI; blind corpus historically Coach opacity (partially mitigated by EP-006.3) |
| **Scoring rationale** | Clears V1-K2 floor (≥50). Students can see a primary tip, but trust and follow-through remain Partial. Effectiveness unproven (PA-014 Hypothesis). |
| **Blockers to desired** | **RC-05** trust surfaces incomplete; no instrumented acceptance; personalisation OFF (EP-004.2); Stage 1 uptake absent; marketing freeze correct until evidence |
| **Related decisions / risks** | DR-036, DR-050, DR-052; PA-014 Hypothesis; PR-001; REM-06 open |
| **Highest-leverage next** | **P0** — recommendation trust presentation + acceptance instrumentation under approved PRD. Ranking changes only if precision defects evidenced. |

---

### K3 — Readiness usefulness (weight 12)

| Field | Value |
|---|---|
| **Current** | **65** |
| **Desired** | **75** |
| **Gap** | +10 category · ≈ +1.20 KSI |
| **Confidence (current)** | Medium |
| **Evidence** | EP-003.2 readiness quality contract; EP-006.4 Home drivers/confidence/review/next; EP-006.5 Tier B N=9; K3_REVALIDATION.md; PA-017 / PA-018 Supported |
| **Scoring rationale** | Unpackability largely fixed on schema-complete Home. Cold-start absence and “On Track” chrome residuals remain. Exam Ready marketing blocked (correct). |
| **Blockers to desired** | RC-04 residual; RC-12 cold-start / overconfidence; external calibration interviews absent; PR-005 |
| **Related decisions / risks** | PA-018; PR-005; RDY-PERC-01/02 |
| **Highest-leverage next** | Cold-start honesty + claim-window spot-checks; raise usefulness without soothing theatre. Supporting after K2/K4/K6. |

---

### K4 — Personalisation (weight 12)

| Field | Value |
|---|---|
| **Current** | **55** |
| **Desired** | **72** |
| **Gap** | +17 category · ≈ **+2.04 KSI** |
| **Confidence (current)** | **High that Δ=0 is correct while flags OFF** |
| **Evidence** | EP-004.1–.3 Complete structurally; `ENABLE_PERSONAL_LEARNING_PROFILE` (and related) default OFF; EP-005.1 W-PROD Δ=0; DR-039; PA-011 Hypothesis |
| **Scoring rationale** | Substrate exists; students do not perceive durable adaptation under production defaults. Cosmetic “personal” speech without evidence would be harmful. |
| **Blockers to desired** | **RC-06** flags OFF; G12 unscored (PR-012); no dogfood pack; visible provenance not student-proven when ON |
| **Related decisions / risks** | DR-039, DR-043; PR-012, PR-016; PA-011, PA-033 |
| **Highest-leverage next** | **P1** controlled dogfood → soak → intentional default change with visible factors. Do not market while OFF. |

---

### K5 — Motivation (weight 10)

| Field | Value |
|---|---|
| **Current** | **63** |
| **Desired** | **72** |
| **Gap** | +9 category · ≈ +0.90 KSI |
| **Confidence (current)** | Medium |
| **Evidence** | EP-007.2 continuity / cognitive-load Pass majority (+3 from 60); baseline habit themes; no dedicated motivation programme; Never-Build constraints on gamification |
| **Scoring rationale** | Consequence metric of clarity and recoverability. Protective tone valued; restorative restart after miss/fail still weak (RC-08). |
| **Blockers to desired** | RC-08; sparse onboarding (PR-017); no smaller restart that “counts” |
| **Related decisions / risks** | PR-017; REM-09 open |
| **Highest-leverage next** | Restorative restart narrative after K1/K2 trust work — not streaks or hype. |

---

### K6 — Learning analytics (weight 10)

| Field | Value |
|---|---|
| **Current** | **50** |
| **Desired** | **70** |
| **Gap** | +20 category · ≈ **+2.00 KSI** |
| **Confidence (current)** | **High that score should not rise while feedback emit OFF** |
| **Evidence** | EP-003.4 record-only loop flag OFF (DR-038); Journey emit deferred (DR-047 / PR-011); Week 0 scorecard N=0; analytics surfaces exist but not decision-grade |
| **Scoring rationale** | Bare V1-K2-style floor for the category set (min=50). Vanity dashboards would be a regression. |
| **Blockers to desired** | **RC-09**; RC-06 feedback OFF; no decision-linked next-action from trends |
| **Related decisions / risks** | DR-038, DR-047; PR-011; PA-013 Supported (structural only) |
| **Highest-leverage next** | Decision-grade history UX **with** lawful evidence activation — not more charts. P1 after / parallel to dogfood. |

---

### K7 — Revision support (weight 12)

| Field | Value |
|---|---|
| **Current** | **58** |
| **Desired** | **72** |
| **Gap** | +14 category · ≈ **+1.68 KSI** |
| **Confidence (current)** | Medium |
| **Evidence** | Blueprint Revision Workspace ships; advanced optimisation deferred; blind-review late-crunch / exam-transfer weakness (SV-006 class); EP-005.1 validated Δ=0 |
| **Scoring rationale** | Presence ≠ intelligent weak-topic / spaced return. External stacks still carry revision for many personas. |
| **Blockers to desired** | **RC-10**; personalisation-gated timing unsupported in W-PROD; REM-11 open |
| **Related decisions / risks** | Blueprint V1/V2 scope split; REM-11 |
| **Highest-leverage next** | Revision inspectability tied to evidenced gaps — after daily-loop trust (K2) and preferably with personalisation ON. Medium-term portfolio. |

---

### K8 — Explainability (weight 14)

| Field | Value |
|---|---|
| **Current** | **70** |
| **Desired** | **78** |
| **Gap** | +8 category · ≈ +1.12 KSI |
| **Confidence (current)** | Medium |
| **Evidence** | EP-006.2 MES delivery; EP-006.3 Tier B N=9; K8_REVALIDATION.md; G1.5 PASS (DR-042); P-001.2 standard + checklist Pass trail |
| **Scoring rationale** | Constitutional floor met. Residual cold-start / sparse MES nights and recommendation-trust coupling keep mid-Strong unclaimed. |
| **Blockers to desired** | RC-01 residual; RC-05 coupling; PERC-02 cold-start copy |
| **Related decisions / risks** | DR-042; PA-001 Supported (trust link not outcome-validated) |
| **Highest-leverage next** | Deepen via recommendation trust surfaces and cold-start honesty — not a new explainability law. |

---

## 4. Ranked opportunity by weighted gap to desired

| Rank | ID | Weighted gap to desired | Why board should care |
|---|---|---:|---|
| 1 | **K2** | +3.00 | Largest remaining weight×gap; daily next-action trust |
| 2 | **K4** | +2.04 | Latent gated value; currently zero in W-PROD |
| 3 | **K6** | +2.00 | Floor risk + decision-grade void |
| 4 | **K7** | +1.68 | Exam companion promise incomplete |
| 5 | **K3** | +1.20 | Honesty-sensitive Strong path |
| 6 | **K8** | +1.12 | Floor met; deepen with trust |
| 7 | **K1** | +0.90 | Already Strong floor; supporting |
| 8 | **K5** | +0.90 | Consequence of P0/P1 |

---

## 5. Evidence confidence map

| Category | Structural (Tier A) | Perception (Tier B) | Cohort (Tier E / M-series) | Overall confidence on current score |
|---|---|---|---|---|
| K1 | Strong | EP-007.2 N=9 | Absent | Medium |
| K2 | Strong | Partial (MES helps; acceptance absent) | Absent | Medium |
| K3 | Strong | EP-006.5 N=9 | Absent | Medium |
| K4 | Exists gated | None in W-PROD | Absent | High that 55/Δ=0 correct |
| K5 | Indirect | EP-007.2 continuity | Absent | Medium |
| K6 | Exists gated | Weak | Absent | High that 50 correct |
| K7 | Workspace present | Weak | Absent | Medium |
| K8 | Strong | EP-006.3 N=9 | Absent | Medium |

---

## 6. Non-claims

This breakdown does **not**:

- Amend the validated EP-007.2 board
- Claim desired scores as current
- Authorize Exam Ready, recommendation-effectiveness marketing, or personalisation-ON claims
- Replace Gate G1 evidence requirements

---

## References

- `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`
- `../p003_1_version1_release_dossier/KSI_Evolution.md`
- `../ep007_2_canonical_journey_perception_validation/K1_REVALIDATION.md`
- `../ep006_5_readiness_perception_validation/K3_REVALIDATION.md`
- `../ep006_3_mes_perception_validation/K8_REVALIDATION.md`
- `../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`

---

**End of KSI_DIMENSION_BREAKDOWN**
