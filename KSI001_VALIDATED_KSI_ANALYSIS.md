# KSI-001 — Validated KSI Analysis

**Programme:** KSI-001 — Validated Educational Effectiveness Programme  
**Date:** 2026-08-04  
**Status:** ANALYSIS COMPLETE — AWAITING FOUNDER REVIEW  
**Authority:** `PRODUCT_SUCCESS_FRAMEWORK.md` · `VERSION_1_RELEASE_FRAMEWORK.md` · `P002_1_RELEASE_READINESS_REPORT.md` · EP-005.1 → EP-008.3B chain · PB-017 · Educational Content Freeze · EF-001  

**This programme is validation planning only.** No Runtime, Student Twin, Recommendation Engine, Educational Framework, Curriculum, Educational Package, Premium Experience, or Architecture changes.

---

## 1. Executive answer

| Measure | Value |
|---------|-------|
| Current **validated** KSI (W-PROD) | **64** |
| Version 1 threshold (G1.1 / V1-K1) | **≥ 80** |
| Gap | **16** composite points |
| Composite confidence | **Medium** |
| Assessment chain date | **2026-07-26** (≤ 90 days on 2026-08-04; refresh before ~2026-10-24) |
| Claim window | **W-PROD** (sole-runtime production defaults; Twin cutovers OFF; personalisation / feedback flags OFF) |

**Verdict:** Educational *correctness* (PB-017 Progressive Confidence PASS · 72/72 Approver inventory · Content Freeze) is demonstrated. Educational *usefulness* under P-001.1 remains **validated KSI 64** — far below the Version 1 bar. Progressive Confidence, Premium Conditional PASS, and programme estimated ΔKSI **do not** raise validated KSI.

---

## 2. How validated KSI reached 64 (evolution)

```
P-001.1 estimated baseline              KSI 58
EP-005.1 first validated board          KSI 59
EP-006.3 MES perception                 KSI 60  (K8 → 70; G1.5 PASS)
EP-006.5 readiness perception           KSI 61  (K3 → 65)
EP-007.2 journey perception             KSI 62  (K1 → 72; K5 → 63)
EP-007.3 effectiveness Stage 1 design   KSI 62  (Δ = 0; ops not executed)
EP-008.1B recommendation trust          KSI 64  (K2 → 68; K8 → 72)
EP-008.3B recommendation commitment     KSI 64  (K2 hold 68; K7 → 60; K8 hold 72)
Target                                  KSI ≥ 80
Remaining gap                           16 points
```

**Rule (PSF §5.6):** Do not sum overlapping programme estimates. Prefer the lower score when structural eligibility and student-perception evidence conflict. External N = 0 caps Strong-band claimability.

---

## 3. Category scoreboard (current validated board)

Weights from Product Success Framework. Scores from EP-008.3B (latest published W-PROD revalidation; holds EP-008.1B for K2/K8).

| ID | Category | Weight | Current | Band | Validated? | Confidence | Weighted | Gap to 70 | Gap to Strong mid (~77) | Evidence source |
|----|----------|-------:|--------:|------|------------|------------|---------:|----------:|------------------------:|-----------------|
| K1 | Planning usefulness | 15 | **72** | Strong (floor) | **Yes** | Medium | 10.80 | — | +5 | EP-007.2 Tier B · EP-005.1 → journey chain |
| K2 | Recommendation usefulness | 15 | **68** | Partial (upper) | **Yes** | Medium | 10.20 | +2 | +9 | EP-008.1B Tier B; EP-008.3B **hold** (no rate floors) |
| K3 | Readiness usefulness | 12 | **65** | Partial | **Yes** | Medium | 7.80 | +5 | +12 | EP-006.5 Tier B |
| K4 | Personalisation | 12 | **55** | Partial | **Yes** (Δ=0) | High that no W-PROD lift | 6.60 | +15 | +22 | EP-005.1; flags OFF (DR-038/039) |
| K5 | Motivation | 10 | **63** | Partial | **Yes** | Medium | 6.30 | +7 | +14 | EP-007.2 side-effect; no dedicated programme |
| K6 | Learning analytics | 10 | **50** | Partial (floor) | **Yes** (Δ=0) | High that no W-PROD lift | 5.00 | +20 | +27 | EP-005.1; feedback flag OFF; Journey emit deferred |
| K7 | Revision support | 12 | **60** | Partial | **Yes** | Medium | 7.20 | +10 | +17 | EP-008.3B continuity (+2 from 58) |
| K8 | Explainability | 14 | **72** | Strong (floor) | **Yes** | Medium | 10.08 | — | +5 | EP-006.3 → EP-008.1B |
| | **Validated KSI** | **100** | **64** | Partial | **Yes** | Medium | **64.00** | | | EP-008.1B / EP-008.3B |

### Arithmetic identity

\[
\begin{align*}
&(72\times0.15)+(68\times0.15)+(65\times0.12)+(55\times0.12)\\
&+(63\times0.10)+(50\times0.10)+(60\times0.12)+(72\times0.14)\\
&=10.80+10.20+7.80+6.60+6.30+5.00+7.20+10.08\\
&=\mathbf{64.00}
\end{align*}
\]

---

## 4. Per-component detail

### K1 — Planning usefulness — **72** (Validated · Medium)

| Field | Value |
|-------|-------|
| Current value | **72** |
| Validated? | **Yes** |
| Evidence source | EP-007.1 / EP-007.2 Tier B (sole-runtime journey; dual-home / duration mismatch closed on W-PROD); planning quality contracts EP-003.3 |
| Confidence | Medium (Tier B N=9; external N=0) |
| Gap to target | Above 70; ~5 pts short of mid-Strong (~77); composite still needs portfolio |
| Status class | **Validated Strong-floor** — residual prefer-lower + topic-selection quality unproven (RC-11) |

### K2 — Recommendation usefulness — **68** (Validated · Medium)

| Field | Value |
|-------|-------|
| Current value | **68** |
| Validated? | **Yes** (perception); Strong-band **unsupported** |
| Evidence source | EP-008.1B Tier B (why-now, benefit, coherence, alternatives, refusal); EP-008.3B hold — commitment chrome perceived, **no** observational acceptance / completion rates |
| Confidence | Medium |
| Gap to target | +2 to 70; +7–12 to Strong (≥75) blocked without behavioural evidence |
| Status class | **Validated Partial upper** — highest remaining weight×gap pillar for Strong-band |

### K3 — Readiness usefulness — **65** (Validated · Medium)

| Field | Value |
|-------|-------|
| Current value | **65** |
| Validated? | **Yes** |
| Evidence source | EP-006.4 / EP-006.5 Tier B unpackability; readiness quality contracts EP-003.2 |
| Confidence | Medium |
| Gap to target | +5 to 70; cold-start / “On Track” residual (RC-04/RC-12) |
| Status class | **Validated Partial** |

### K4 — Personalisation — **55** (Validated Δ=0 · High confidence of no lift)

| Field | Value |
|-------|-------|
| Current value | **55** |
| Validated? | **Yes that Δ=0 in W-PROD** |
| Evidence source | EP-004.1–.3 capability exists gated; `ENABLE_PERSONAL_LEARNING_PROFILE` (and related) default OFF |
| Confidence | High (that production defaults do not deliver personalisation usefulness) |
| Gap to target | +15 to 70; estimated gated stack **unsupported** for G1 until flag-ON dogfood + soak + re-score |
| Status class | **Validated absence of W-PROD lift** — latent estimated value must not be added to 64 |

### K5 — Motivation — **63** (Validated · Medium)

| Field | Value |
|-------|-------|
| Current value | **63** |
| Validated? | **Yes** (retained / minor EP-007.2 lift) |
| Evidence source | EP-007.2 journey side-effect; EP-003 scorecard retention exploratory; restorative motivation backlog (RC-08) |
| Confidence | Medium |
| Gap to target | +7 to 70 |
| Status class | **Validated Partial** — consequence metric; moves with consistency evidence |

### K6 — Learning analytics — **50** (Validated Δ=0 · High confidence of no lift)

| Field | Value |
|-------|-------|
| Current value | **50** (V1-K2 floor) |
| Validated? | **Yes that Δ=0 in W-PROD** |
| Evidence source | EP-003.4 feedback flag OFF; Journey emit deferred; Week 0 scorecard insufficient N |
| Confidence | High (that student-facing decision-grade analytics are not proven in W-PROD) |
| Gap to target | +20 to 70 — **largest category gap** |
| Status class | **Validated floor** — blocks portfolio path to 80 if left untouched |

### K7 — Revision support — **60** (Validated · Medium)

| Field | Value |
|-------|-------|
| Current value | **60** |
| Validated? | **Yes** |
| Evidence source | EP-008.3B continuity / History narrative (+2 from 58); revision workspace depth limited |
| Confidence | Medium |
| Gap to target | +10 to 70 |
| Status class | **Validated Partial** |

### K8 — Explainability — **72** (Validated · Medium)

| Field | Value |
|-------|-------|
| Current value | **72** |
| Validated? | **Yes** |
| Evidence source | EP-006.2/006.3 MES perception; EP-008.1B deepen; P-001.2 checklists Pass |
| Confidence | Medium |
| Gap to target | Meets G1.5 / V1-K3 (≥70); ~5 pts short of mid-Strong |
| Status class | **Validated Strong-floor** — G1.5 **PASS** |

---

## 5. Estimated vs validated vs unsupported

| Class | Definition | Current inventory |
|-------|------------|-------------------|
| **Validated** | Evidence-bound W-PROD re-score ≤ 90 days | Composite **64**; categories above |
| **Estimated (provisional)** | Programme ΔKSI for planning — **not** G1 input | PX-003…007 craft ΔKSI (provisional +3…+7 each); gated EP-003.4 / EP-004.1–.3 stack (~+6–7); naive EP sum historically falsified |
| **Unsupported** | Would require absent evidence or contradict prefer-lower | “KSI ≈ 70+ from summing estimates”; “PB-017 PASS ⇒ G1”; “Premium Conditional PASS ⇒ usefulness ≥80”; “K2 ≥75 without rates”; “effectiveness GO with N_external=0”; exam pass-rate proof |

### What PB / Premium / Founder evidence does *not* do

| Artefact | What it proves | What it does **not** prove |
|----------|----------------|----------------------------|
| PB-017 Progressive Confidence PASS (9.00/9) | Diligent students can complete LIVE-certified Approver packages with CMP partnership | Validated KSI ≥ 80; multi-week usefulness; recommendation acceptance; G1.9 GO |
| Educational Content Freeze / 72/72 | Educational volume complete for Approver inventory | Educational effectiveness |
| PX-007 Conditional PASS | Premium experience craft Conditional | Validated category lifts |
| P-002.1 Founder walkthrough 0 Crit / 0 Major | No Critical/Major product defects in walkthrough | Usefulness index |
| EP-006–008 Tier B packs | Perception trust on targeted surfaces | Sustained study behaviour (M1–M9 external) |

---

## 6. Math reality for reaching ≥ 80

| Scenario (illustrative planning only) | Approx. KSI | Notes |
|---------------------------------------|------------:|-------|
| Current validated | **64** | Board |
| All categories = 70 | **~70** | Still **short of 80** |
| Raise K2/K4/K6/K7 to ~77; hold K1/K3/K5/K8 | **~74–76** | Still short without broader Strong portfolio |
| Several pillars mid-Strong (75–82) + floors cleared | **≥80** | Required shape — not a single-feature lift |

**Implication:** Closing the 16-point gap requires a **portfolio of Strong-band pillars** *and* evidence that makes those scores *claimable* (Stage 1 / behavioural rates / interviews). Perception-only packs cannot finish the job.

---

## 7. Version 1 KSI-lens check (informational)

| Criterion | Required | Result | Met? |
|-----------|----------|--------|------|
| V1-K1 | KSI ≥ 80 | **64** | **No** |
| V1-K2 | No category &lt; 50 | Min K6 = **50** | **Yes (bare)** |
| V1-K3 | K8 ≥ 70 | **72** | **Yes** |
| V1-K4 | SIAs filed for material EP/P | Prior programmes filed; this programme files SIA | Process OK |
| V1-K5 | Effectiveness not NO-GO | **NO-GO / PENDING EVIDENCE** | **No** |
| V1-K6 | No honesty incident | Clear | **Yes** |
| V1-K7 | Distinguish KSI vs pass-rate | Held | **Yes** |

---

## 8. Honest recommendation (how KSI should be raised)

**Not** “improve the software.”

Raise validated KSI by **collecting and scoring evidence** that proves educational usefulness:

1. **Clear G1.9 first as claimability law** — Privacy Review → Stage 1 external ops → M1–M9 + interviews → move effectiveness away from NO-GO. Without this, even a hypothetical KSI 80 perception package fails G1.  
2. **Re-score W-PROD from behavioural + interview evidence**, not from stacking PX/PB estimates. Prefer-lower when N is thin.  
3. **Prioritise evidence against the largest weighted gaps:** K6 (floor), K4 (flag-OFF absence), K7, then Strong-band K2 (acceptance / commitment rates), then incremental K3/K5.  
4. **Treat existing gated capabilities as validation subjects** (controlled flag-ON dogfood → soak → G12 honesty) — only if Founder authorises; do not invent new ranking brains or Educational Framework law.  
5. **File G1.7 independent re-score** on the next full package before any declaration board.  
6. **Do not** declare Version 1 production-ready on this analysis.

Detail: `KSI001_VALIDATION_ROADMAP.md` · `KSI001_EVIDENCE_GAP_ANALYSIS.md`.

---

## 9. Non-claims

This analysis does **not** claim:

- Version 1 production-ready  
- Validated KSI ≥ 80  
- Educational effectiveness GO  
- Exam pass-rate improvement  
- Until-exam trust  
- That Premium or Progressive Confidence substituted for Gate G1  

---

## 10. Exit

**STOP.** Await Founder review of this document before commissioning Stage 1 ops or any further G1 claim language.

Signed: KSI-001 Validated KSI Analysis · 2026-08-04
