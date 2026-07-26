# P-004.1 — KSI Gap Analysis

**Programme:** P-004.1 — KSI Gap Analysis & Improvement Roadmap  
**Date:** 2026-07-26  
**Status:** Analysis only (no runtime / governance / architecture changes)  
**Claim window:** W-PROD  
**Authority scores:** EP-007.2 validated board (DR-051)  
**Target:** KSI ≥ **80** (Product Success Framework; DR-025)  
**Current:** Validated KSI **62** (Medium confidence)  
**Gap:** **18** composite points  
**Board posture:** **NO GO** (DR-041)

---

## 1. Executive answer

### Why is KSI 62 instead of 80?

Validated educational usefulness is **62** because:

1. **Structural quality is ahead of student-proven Strong-band usefulness.** EP-003.1–.3 quality contracts and MES schemas raised usefulness structurally, but Strong-band scores (70+) require Tier B / cohort corroboration that only partially exists.
2. **Perception remediation closed the largest *presentation* failures** (invisible MES, dual homes, duration mismatch, unpackable readiness) and moved KSI **59 → 62**, clearing **G1.5** (K8 ≥ 70). That work bought **+3** validated points — not enough for Version 1.
3. **The largest remaining weighted deficits sit in weak pillars:** K2 (**55**), K4 (**55**), K6 (**50** floor), K7 (**58**), with K3 (**65**) still short of Strong mid-band and K1 (**72**) capped by prefer-lower + external N=0.
4. **Gated personalisation and learning-feedback value is invisible in production defaults** (DR-038, DR-039). Estimated ~+6–7 KSI from EP-003.4 / EP-004.1–.3 **must not be added** to 62.
5. **External cohort evidence is absent** (N_external = 0; privacy unsigned). Without Stage 1, Strong-band claims and G1.9 effectiveness remain blocked even if surfaces improve further.
6. **Math reality:** lifting every category only to **70** yields KSI ≈ **70**, still **short of 80**. Version 1 requires a **portfolio of Strong-band pillars**, not a single feature.

### What are the highest-leverage improvements?

| Priority | Improvement class | Why |
|---|---|---|
| **P0** | Recommendation trust surfaces + acceptance instrumentation (REM-06 successor) | Highest remaining weight×gap pillar (K2=55); speech/inspectability, not a new ranking brain |
| **P0** | Stage 1 cohort ops (privacy → invites → M1–M9) | Unlocks claimable Strong-band + G1.9; without this, G1 cannot PASS even at KSI 80 |
| **P1** | Controlled flag-ON dogfood → soak → G12 for profile / personalisation / feedback | Unlocks latent K4/K6 (and secondary K1/K2) estimated value currently Δ=0 in W-PROD |
| **P1** | Decision-grade analytics + revision usefulness | Required portfolio fillers (K6 floor risk; K7 lag) |
| **P2** | Restorative motivation / cold-start honesty / sparse-content nights | Consequence and residual friction; smaller ΔKSI |

### What does *not* close the gap?

| Temptation | Why rejected |
|---|---|
| Another recommendation algorithm / “smarter Twin” | Contracts Pass; residual failure is trust, acceptance, and evidence — not ranking absence |
| Opaque LLM coach copy | Constitution / Art. IV / P-001.2; corpus distrusts unverifiable intelligence speech |
| Stacking estimated ΔKSI programmes into “current KSI ≈ 70” | EP-005.1 / DR-026 falsified |
| Turning all personalisation flags ON immediately | G12 + honesty risk (PR-012, PR-016, PA-033) |
| Declaring V1 from perception packs alone | DR-033: perception ≠ effectiveness |
| Operational GA / architecture cutover alone | Orthogonal; insufficient for G1 |

---

## 2. Scoreboard

| ID | Category | Weight | Score | Band | Weighted | Gap to 70 | Gap to Strong mid (~77) | Weighted gap to 70 |
|---|---|---:|---:|---|---:|---:|---:|---:|
| K1 | Planning usefulness | 15 | **72** | Strong (floor) | 10.80 | — (above) | +5 | — |
| K2 | Recommendation usefulness | 15 | **55** | Partial | 8.25 | +15 | +22 | **+2.25** |
| K3 | Readiness usefulness | 12 | **65** | Partial | 7.80 | +5 | +12 | +0.60 |
| K4 | Personalisation | 12 | **55** | Partial | 6.60 | +15 | +22 | **+1.80** |
| K5 | Motivation | 10 | **63** | Partial | 6.30 | +7 | +14 | +0.70 |
| K6 | Learning analytics | 10 | **50** | Partial (floor) | 5.00 | +20 | +27 | **+2.00** |
| K7 | Revision support | 12 | **58** | Partial | 6.96 | +12 | +19 | **+1.44** |
| K8 | Explainability | 14 | **70** | Strong (floor) | 9.80 | — | +7 | — |
| | **KSI** | **100** | **62** | Partial | **61.51 → 62** | | | |

**Composite confidence:** Medium (Tier B packs exist for K1/K3/K8; external N=0; prefer-lower).

**Version 1 KSI-lens check:**

| Criterion | Required | Result | Met? |
|---|---|---|---|
| V1-K1 | KSI ≥ 80 | 62 | **No** |
| V1-K2 | No category &lt; 50 | Min K6 = 50 | **Yes (bare)** |
| V1-K3 | K8 ≥ 70 | 70 | **Yes** |
| V1-K5 | Effectiveness not NO-GO | NO-GO | **No** |

---

## 3. How we got here (evolution, not estimate stack)

```
Estimated baseline (P-001.1)     KSI 58
EP-005.1 first validated board   KSI 59   (+1; rejected naive ~70 stack)
EP-006.3 MES perception          KSI 60   (K8 65→70; G1.5 PASS)
EP-006.5 readiness perception    KSI 61   (K3→65)
EP-007.2 journey perception      KSI 62   (K1 68→72; K5 60→63)
EP-007.3 effectiveness Stage 1   KSI 62   (Δ = 0; design only)
Target                           KSI ≥ 80
Remaining gap                    18 points
```

Source: `../p003_1_version1_release_dossier/KSI_Evolution.md`.

### What already closed (do not re-solve as P0)

| Closed theme | Programme | Validated effect |
|---|---|---|
| Invisible MES / Coach opacity (primary) | EP-006.2 + EP-006.3 | K8 → 70; G1.5 PASS |
| Home readiness drivers empty | EP-006.4 + EP-006.5 | K3 → 65 |
| Dual-home / dual-start on W-PROD | EP-007.1 + EP-007.2 | K1 → 72 |
| Same-day 30-vs-90 duration on W-PROD | EP-007.1 + EP-007.2 | Planning honesty on sole-runtime |
| V1-K2 floor (&lt;50) | EP-003.1 + EP-005.1 | K2 ≥ 50 |

### Unsupported estimated gains (do not add to 62)

| Programme | Est. ΔKSI | W-PROD status |
|---|---:|---|
| EP-003.4 Learning Feedback | ≈ +0.8 | Flag OFF (DR-038) |
| EP-004.1 Profile | ≈ +1.1 | Flag OFF (DR-039) |
| EP-004.2 Reco personalisation | ≈ +2.2 | Flag OFF |
| EP-004.3 Plan personalisation | ≈ +2.3 | Flag OFF |

---

## 4. Root-cause catalogue (current, post EP-007)

Root causes below supersede EP-005.2 RC-01…RC-03 / RC-04-primary where those were remediated on W-PROD. Retained IDs keep continuity with EP-005.2 where still open.

| ID | Root cause | Status | Affects | Evidence confidence |
|---|---|---|---|---|
| **RC-01** | Explanation pipeline drop (MES → student) | **Mostly closed** on daily path; residuals: cold-start copy, sparse nights | K8 residual, K2 | High (closed primary); Medium residual |
| **RC-02** | Dual home / dual start | **Closed on W-PROD**; open on dual-run Alpha | K1 residual | High |
| **RC-03** | Same-day duration mismatch | **Closed on W-PROD** | K1 residual | High |
| **RC-04** | Readiness unpackability | **Mostly closed** when schema-complete; cold-start / “On Track” chrome residual | K3 | High / Medium residual |
| **RC-05** | Recommendation trust limited by speech & missing acceptance KPI | **Open — primary KSI lever** | K2, K8 | High |
| **RC-06** | Closed-loop capabilities invisible (flags OFF) | **Open — primary latent lift** | K4, K6, K1, K2 | High |
| **RC-07** | Missing Stage 1 / external cohort / M1–M9 | **Open — blocks G1.9 & Strong-band claimability** | All / G1.9 | High |
| **RC-08** | Motivation protective, not restorative | **Open** | K5, K1 | Medium |
| **RC-09** | Analytics not decision-grade | **Open** (floor K6=50) | K6 | High |
| **RC-10** | Revision support stagnant | **Open** | K7 | Medium |
| **RC-11** | Topic *selection quality* unproven (plan coherence ≠ best topic) | **Open** | K1 mid-Strong, K2 | Medium |
| **RC-12** | Cold-start / sparse-evidence overconfidence risk | **Open** | K3, K8, PR-005 | Medium–High |
| **RC-13** | G1.7 second-assessor formality unfinished | **Open (process)** | Declaration | High |

---

## 5. Gap decomposition (18 points)

Illustrative **planning** allocation of the 18-point gap (not a validated forecast; prefer under-claim):

| Bucket | Est. share of gap | Mechanism |
|---|---:|---|
| Weak pillars below Strong (K2/K4/K6/K7 primarily) | ~10–12 | Category scores must move into mid-Strong, not merely to 70 |
| Prefer-lower + Medium confidence ceiling | ~2–3 | External N=0 caps claimable lifts (PR-008) |
| Portfolio shortfall beyond “all = 70” | ~3–4 | Even universal 70 → KSI ~70; need several pillars ≥75–80 |
| Evidence / effectiveness gate (orthogonal but mandatory) | Claimability | G1.9 FAIL independent of composite math |

**Implication:** Fixing only K2 to 70 (+2.25 KSI) is necessary but nowhere near sufficient. Reaching 80 requires coordinated lifts across K2, K4, K6, K7 (and incremental K3/K1/K5), **plus** evidence programmes that make those lifts *validated*.

---

## 6. Runtime A analysis (student-facing educational loop)

| Capability | Structural state | Student-perceived state (W-PROD) | KSI link | Verdict |
|---|---|---|---|---|
| **Recommendations** | Decision Framework + MES + quality contract Pass | Primary CTA exists (DR-050); trust still Partial (K2=55); no acceptance KPI; effectiveness freeze (DR-036) | K2 primary | **Highest open usefulness gap** |
| **Planning** | Quality contract Pass; sole-runtime Home; unified duration | K1=72 Strong floor; topic quality / sparse nights residual | K1 | Strong enough for V1 floor; not the main 18-pt lever |
| **Readiness** | Drivers/confidence/review/next delivered | K3=65; cold-start / chrome residuals; no Exam Ready | K3 | Partial→Strong path; honesty-sensitive |
| **Explainability** | MES rendered on daily path | K8=70 floor met; residual cold-start / Coach caveats | K8 | Floor cleared; deepen with K2 trust, not new law |
| **Mission generation** | Syllabus-bound missions via Runtime A | Useful as workflow director; not proven adaptive coach | K1/K2 | Keep; do not overclaim intelligence |
| **Educational reasoning** | Deterministic services; presentation narrates only | Students need inspectable why→next; opaque AI rejected | K8/K2 | Presentation + provenance, not second brain |
| **Confidence presentation** | Provisional labels on readiness | Risk of soothing “On Track” chrome (RDY-PERC-02) | K3/K8 | Prefer honest provisional over calm theatre |
| **Educational usefulness** | Contracts Pass ≠ usefulness Pass | Validated 62; effectiveness NO-GO | Composite | Capability ≠ validated value |

---

## 7. Implications for Product Board

1. **Do not reopen MES / dual-home / duration as primary engineering** on W-PROD — those themes are closed; residuals are secondary.
2. **Authorise recommendation-trust + Stage 1 cohort programmes next** — they attack the largest remaining usefulness and claimability blockers.
3. **Treat personalisation activation as a gated value realisation programme**, not a marketing flip.
4. **Refuse estimate stacking and LLM-coach shortcuts.**
5. **Expect portfolio programmes**, not a single silver bullet, to approach KSI 80.
6. **Keep NO GO** until G1.1 and G1.9 evidence exists (DR-041 intact).

Detail catalogues: [`STUDENT_PAIN_POINTS.md`](STUDENT_PAIN_POINTS.md) · [`HIGH_LEVERAGE_IMPROVEMENTS.md`](HIGH_LEVERAGE_IMPROVEMENTS.md) · [`EXPECTED_KSI_IMPACT.md`](EXPECTED_KSI_IMPACT.md) · [`ENGINEERING_PRIORITIES.md`](ENGINEERING_PRIORITIES.md) · [`ROADMAP.md`](ROADMAP.md).

---

## References

- `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`
- `../p001_1_ksi_baseline/BASELINE_KSI_ASSESSMENT.md`
- `../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`
- `../ep005_2_educational_experience_validation/KSI_GAP_ANALYSIS.md`
- `../p003_1_version1_release_dossier/KSI_Evolution.md`
- `../p003_8_version1_exit_criteria/CURRENT_RELEASE_POSITION.md`
- `../ep004_private_beta/BLIND_REVIEW_META_ANALYSIS_V2.md`
- `../p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md` (DR-025, DR-026, DR-033, DR-036, DR-038, DR-039, DR-041, DR-042, DR-050, DR-051)
- `../p003_3_product_risk_register/ACTIVE_RISKS.md` (PR-001, PR-002, PR-006)

---

**End of KSI_GAP_ANALYSIS**
