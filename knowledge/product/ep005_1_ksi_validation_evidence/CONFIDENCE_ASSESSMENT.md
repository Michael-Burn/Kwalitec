# EP-005.1 — Confidence Assessment

**Programme:** EP-005.1 — KSI Validation & Evidence Collection  
**Version:** 1.0  
**Assessment date:** 2026-07-26  
**Companion:** [`VALIDATED_KSI_REPORT.md`](VALIDATED_KSI_REPORT.md)  
**Method:** [`VALIDATION_METHODOLOGY.md`](VALIDATION_METHODOLOGY.md) §6  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

Record **High / Medium / Low** confidence for every KSI dimension (K1–K8) and the composite validated KSI, with explicit drivers and falsifiers. Confidence here is about **measurement certainty**, not product quality praise.

---

## 2. Per-category confidence

| ID | Category | Validated score | Confidence | Dominant evidence tier | Why this confidence |
|---|---|---:|---|---|---|
| K1 | Planning usefulness | 68 | **Medium** | A + C | Contract tests + checklist Pass are strong; dual-home / duration themes (Tier C) un-retested post-change |
| K2 | Recommendation usefulness | 53 | **Medium** | A + C | Quality contract + P-001.3 Pass; no acceptance KPI; Coach opacity corpus not re-measured |
| K3 | Readiness usefulness | 57 | **Medium** | A + C | Schema / refusal Tier A; unpackability / overconfidence themes still open without Tier B |
| K4 | Personalisation | 55 | **High** | Auth (flag OFF) | High certainty that W-PROD student-perceived lift is **zero** while profile flag defaults OFF |
| K5 | Motivation | 60 | **Medium** | C | Baseline retained; no dedicated post-change motivation evidence |
| K6 | Learning analytics | 50 | **High** | Auth (flag OFF) + C | High certainty W-PROD Δ = 0 (feedback OFF; Journey emit deferred; Week 0 insufficient N) |
| K7 | Revision support | 58 | **Medium** | C / D | No Tier B; estimated micro-lifts unsupported for validation |
| K8 | Explainability | 65 | **Medium** | A + C | MES Tier A on Rec/Plan/Readiness; Near-Universal Coach opacity without post-change clearance |

---

## 3. Composite confidence

| Field | Value |
|---|---|
| **Composite confidence** | **Medium** |
| Rule applied | Lowest among Version 1 pillars K1/K2/K3/K8 (all Medium) |
| Student-perception sub-score | **Low** (no Tier B post-change; external N=0) |
| Structural sub-score | **Medium–High** for EP-003.1–.3 contracts |
| G1.2 interpretation | Medium satisfies “not Low” formally; **limitations forbid Strong-band / KSI≥80 claims** |

**Important:** Composite Medium does **not** mean the product is Version 1 ready. It means the **validated score of 59** is a defensible under-claim given structural evidence and missing perception re-tests — not that usefulness is Strong.

---

## 4. Confidence by evaluation dimension

| Dimension | Confidence | Notes |
|---|---|---|
| Recommendation usefulness | Medium | Structural Pass; effectiveness unproven |
| Planning usefulness | Medium | Structural Pass; friction themes open |
| Readiness usefulness | Medium | Structural Pass; interpretability open |
| Explainability | Medium | MES delivered; Coach trust not re-validated; **below floor 70** |
| Personalisation usefulness | High (Δ=0 in W-PROD) | Gated OFF — do not confuse with high usefulness |
| Learning feedback quality | High (Δ=0 in W-PROD) | Record-only + flag OFF |

---

## 5. What would raise confidence

| To reach | Required evidence |
|---|---|
| High on K1/K2/K3/K8 | Post-change blind re-review or ≥8 interviews agreeing with structural scores within ±5; no P1 honesty defects |
| High composite | Pillar High **and** Stage 1 directional scorecard (N≥10, ≥2 weeks) without contradiction |
| Enable KSI ≥ 70 claim language | Above + no category &lt; 50 + K8 ≥ 70 with Tier B |
| Enable KSI ≥ 80 / G1 pass path | PSF V1-K1…V1-K7 + filled evidence package; educational Go / No-Go not effectiveness NO-GO |

---

## 6. What would lower confidence / scores

| Trigger | Action |
|---|---|
| Post-change reviews still show Coach opacity Near Universal | Lower K8 (and possibly K2); may fall toward baseline 55 |
| Duration / dual-home unresolved in Stage 1 | Cap or reduce K1 |
| Honesty incident (dual truth / false readiness) | Freeze categories; G1.10 FAIL |
| Flag-ON personalisation without explainability disclosure | Do not raise K4; investigate K8 |

---

## 7. Insufficient-evidence log

| Gap | Confidence impact |
|---|---|
| GAP-01 No post-change perception pack | Caps all pillar confidence at Medium; blocks High |
| GAP-02 External N=0 | Blocks product-decision KPI confidence |
| GAP-04 W-GATED not dogfooded | W-GATED estimates remain Low confidence / unsupported for G1 |
| GAP-05 No second assessor yet | G1.7 formality HOLD |

---

## 8. Sign-off

| Role | Statement | Date |
|---|---|---|
| Product measurement (EP-005.1) | Confidence table filed; composite **Medium**; validated KSI **59** under-claimed vs naive estimates | 2026-07-26 |

---

**End of CONFIDENCE_ASSESSMENT**
