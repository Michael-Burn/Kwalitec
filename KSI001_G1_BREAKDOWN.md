# KSI-001 — Gate G1 Breakdown

**Programme:** KSI-001 — Validated Educational Effectiveness Programme  
**Date:** 2026-08-04  
**Status:** ANALYSIS COMPLETE — AWAITING FOUNDER REVIEW  
**Authority:** `VERSION_1_RELEASE_FRAMEWORK.md` §G1 · `P002_1_GATE_SCORECARD.md` · PSF V1-K1…V1-K7 · EP-007.3 `G1_9_STATUS.md` · EP-008.1B / EP-008.3B  

**Overall Gate G1:** **FAIL** (hard blocker for Version 1 production-ready)

---

## 1. Why G1 fails (precise)

Gate G1 fails for **two hard criteria** and one **formality HOLD**:

| # | Criterion | Status | Precise failure |
|---|-----------|--------|-----------------|
| 1 | **G1.1** Validated KSI ≥ 80 | **FAIL** | Published validated composite **64** (gap **16**) |
| 2 | **G1.9** Educational effectiveness not NO-GO | **FAIL** | Effectiveness remains **NO-GO / PENDING EVIDENCE** (external N=0; Privacy Review unsigned; Stage 1 ops not executed) |
| 3 | **G1.7** Independent re-score ±3 | **HOLD** | Second assessor not filed — does not alone cause FAIL but blocks clean declaration |

All other G1 sub-criteria currently **PASS** under the 2026-07-26 assessment chain (as reaffirmed by P-002.1 on 2026-08-04).

**What is *not* the G1 failure mode:** missing educational packages (PB-017 PASS · 72/72), Premium craft residuals, LIVE tip health, Runtime architecture, or Educational Framework gaps. Those domains are educationally complete or operationally residual — **orthogonal** to G1 FAIL.

---

## 2. Criterion-by-criterion board

| ID | Criterion | Measurable rule | Result | Evidence | Gap / residual |
|----|-----------|-----------------|--------|----------|----------------|
| **G1.1** | Composite KSI | ≥ 80 (nearest integer) | **FAIL** | EP-008.1B / EP-008.3B → **64** · `KSI001_VALIDATED_KSI_ANALYSIS.md` | Need **+16** validated points via evidence-bound re-score |
| **G1.2** | Assessment confidence | High or Medium | **PASS** | Medium on composite | Low confidence would FAIL — avoid overclaim that raises confidence falsely |
| **G1.3** | Freshness | ≤ 90 days before declaration | **PASS** (as of 2026-08-04) | Chain dated 2026-07-26 | Refresh required before ~2026-10-24; any new Stage 1 package resets the clock |
| **G1.4** | Category floor | No category &lt; 50 | **PASS** | Min = K6 **50** | Bare floor — K6 regression to &lt;50 would re-FAIL G1.4 |
| **G1.5** | Explainability floor | K8 ≥ 70 | **PASS** | K8 **72** | Hold Strong-floor; do not regress Coach honesty |
| **G1.6** | Evidence package | Paths, rationales, limitations per category | **PASS** | EP-005.1 register + revalidation chain | Next full re-score must refresh register |
| **G1.7** | Independent re-score | Agree within ±3 or Product resolves dispute | **HOLD** | Single-assessor chain | File second-assessor pass before declaration board |
| **G1.8** | Claim language | Distinguish KSI usefulness from exam pass-rate | **PASS** | P-002.1 / PB-017 non-claims held | Continue freeze on pass-rate marketing |
| **G1.9** | Effectiveness Go / No-Go | Not **NO-GO** for claim window (V1-K5) | **FAIL** | `ep007_3_…/G1_9_STATUS.md` | Privacy → Stage 1 ops → Q1–Q5 Yes → update EP-003/004 verdict |
| **G1.10** | Honesty incident | No unresolved educational honesty P1 | **PASS** | No open P1 | Sev-1 honesty → automatic claim freeze |

---

## 3. G1.1 deep dive — composite shortfall

### 3.1 Current vs required

| Measure | Value |
|---------|------:|
| Required | ≥ **80** |
| Validated | **64** |
| Gap | **16** |

### 3.2 Where the 16 points live (weighted)

Using category gaps to mid-Strong (~77) as a planning lens (not a validated forecast):

| ID | Score | Weight | Rough weighted shortfall vs ~77 | Notes |
|----|------:|-------:|--------------------------------:|-------|
| K2 | 68 | 15 | ~1.35 | Strong-band blocked without rates |
| K3 | 65 | 12 | ~1.44 | Perception residual |
| K4 | 55 | 12 | ~2.64 | Flag-OFF; largest latent estimated bucket |
| K5 | 63 | 10 | ~1.40 | Consequence of consistency |
| K6 | 50 | 10 | ~2.70 | Floor risk + decision-grade absence |
| K7 | 60 | 12 | ~2.04 | Continuity only partially lifted |
| K1 | 72 | 15 | ~0.75 | Already Strong-floor |
| K8 | 72 | 14 | ~0.70 | Already Strong-floor / G1.5 clear |
| | | | **~14–16** | Matches composite gap order of magnitude |

**Critical math:** lifting every category only to **70** yields KSI ≈ **70** — still **10 points short** of 80. G1.1 cannot be satisfied by “everyone to Partial-upper.” Several pillars must enter **mid-Strong**, with evidence that justifies the band.

### 3.3 What must *not* be used to close G1.1

| Temptation | Why rejected |
|------------|--------------|
| Sum PX provisional ΔKSI | Estimated; PSF §5.6 forbids |
| Treat PB-017 9.00/9 as KSI | Progressive Confidence ≠ KSI categories |
| Count gated EP-004 personalisation as live | Flags OFF — Δ=0 validated |
| Inflate K2 to ≥75 from Tier B alone | EP-008.3B explicitly forbids without behavioural floors |
| Re-label estimated baseline ~58 + naive programme stack | EP-005.1 falsified |

---

## 4. G1.9 deep dive — effectiveness NO-GO

### 4.1 Criterion text

> EP-003 / EP-004 educational Go / No-Go not **NO-GO** for the same claim window (V1-K5).

### 4.2 Current educational verdict

| Field | Value |
|-------|-------|
| Effectiveness verdict | **NO-GO / PENDING EVIDENCE** |
| Stage 1 design | Complete (EP-007.3) |
| Stage 1 ops | **Not executed** |
| External N | **0** |
| Privacy Review | **Unsigned** (blocks invites) |
| M1–M9 external | Absent / insufficient N |
| Perception packs | Favourable (MES / readiness / journey / reco trust) — **not substituted** for Stage 1 |

### 4.3 Why perception / PB cannot clear G1.9

| Evidence type | Proves | Does not prove |
|---------------|--------|----------------|
| Tier B perception (N≈9 internal) | Surfaces understood / conditionally trusted | Multi-week study behaviour |
| Stage 0 dogfood | Staff / founder can operate product | External educational effectiveness |
| PB-001…PB-017 Progressive Confidence | Package + CMP diligence confidence | Recommendation uptake, retention M6, usefulness over weeks |
| EP-007.3 design docs | Measurement plan ready | Outcomes |

Authority: EP-007.3 correctly refused substituting Tier B for Stage 1 N.

### 4.4 Minimum path to clear G1.9

Aligned with EP-007.3 §4 / EP-004 C5–C6 / EP-003 Q1–Q5:

1. Privacy Review **signed**.  
2. Stage 1+ invites under Private Beta Protocol.  
3. Measurement window: ≥4 weeks for ≥20 active **or** Product + Educational **written waiver** with claim restrictions (not granted as of 2026-08-04).  
4. Interview sample ≥8 or 25% of active.  
5. Q1–Q5 all **Yes** with linked evidence paths.  
6. Update EP-003 / EP-004 educational verdict away from NO-GO / PENDING for the claim window.  
7. Re-file `G1_9_STATUS.md` as **PASS**.

Stage 1 alone (N 5–10) may produce **directional** scorecards and support a later CONDITIONAL path, but does **not** by itself meet C5’s N≥20 product-decision floor without waiver.

---

## 5. Interaction: G1.1 × G1.9

```
                    ┌─────────────────────┐
                    │   Gate G1 PASS?     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                                 ▼
        G1.1 KSI ≥ 80                     G1.9 not NO-GO
              │                                 │
   Needs Strong-band                   Needs Stage 1+
   portfolio + re-score                behavioural evidence
              │                                 │
              └────────────────┬────────────────┘
                               ▼
              Both required. Either FAIL → overall G1 FAIL.
              Clearing only one is insufficient for declaration.
```

**Claimability rule:** Without G1.9, Strong-band KSI claims remain capped (prefer-lower / Medium confidence / effectiveness freeze). Without G1.1, G1.9 alone cannot declare Version 1 educational success under P-001.

---

## 6. Relationship to other gates (context only)

| Gate | P-002.1 posture | Relationship to G1 |
|------|-----------------|--------------------|
| G2–G6, G8–G12 | PASS WITH RESIDUAL (mostly) | Necessary companions; **do not** override G1 FAIL |
| G7 | HOLD | Separate claim restriction (high-traffic); not the G1 story |
| EVF / PB-017 | Package-path trust held | Feeds honesty / inventory — **not** G1.1 |

KSI-001 does **not** re-litigate G2–G12. Focus remains G1 evidence.

---

## 7. Defensible board statement

> As of 2026-08-04, Gate **G1 FAIL**. Validated KSI is **64** (G1.1 FAIL; gap 16 to ≥80). Educational effectiveness remains **NO-GO / PENDING EVIDENCE** (G1.9 FAIL; external N=0; Privacy Review unsigned). G1.7 independent re-score is **HOLD**. Progressive Confidence (PB-017) and Premium Conditional PASS (PX-007) do not satisfy G1. Do **not** declare Version 1 production-ready.

---

## 8. Exit

Await Founder review of `KSI001_VALIDATED_KSI_ANALYSIS.md`. Do not recommend Version 1 release.

Signed: KSI-001 G1 Breakdown · 2026-08-04
