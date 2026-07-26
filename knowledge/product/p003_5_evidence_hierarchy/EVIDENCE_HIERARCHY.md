# Evidence Hierarchy

**Programme:** P-003.5 — Evidence Hierarchy & Claim Standard  
**Version:** 1.0  
**Status:** Active — documentation standard  
**Effective:** 2026-07-26  
**Does not:** Change runtime, governance law, decisions, risks, assumptions, or release gates  

---

## 1. Purpose

Define a single, ordered hierarchy of **product-claim evidence** so the Product Board can answer:

> How strong is this evidence, and what claims does it support?

This hierarchy classifies **evidence used to justify public, board, marketing, or release claims**. It does not replace:

- Educational Constitution evidence models (learning-event truth),  
- Runtime evidence platforms (telemetry / Twin evidence objects),  
- EP-005.1 Tier A–D validation methodology (KSI scoring procedure).

Those remain authoritative in their domains. This hierarchy is the **board claim lens**.

---

## 2. Design principles

| Principle | Rule |
|---|---|
| Prefer lower | When two levels conflict, credit the **lower** claim set (PSF honesty; DR-027) |
| Necessary ≠ sufficient | Higher engineering evidence does not unlock educational claims |
| Freshness | Evidence older than freshness rules in P-002.1 / PSF is **stale** — treat as one level lower for claim purposes, or DEFER |
| Linked paths | Unlinked anecdotes are not evidence |
| Separable verdicts | Programme GO, educational effectiveness GO, and Version 1 production-ready are **three different claim families** (DR-032) |
| No invention | Missing evidence = **Evidence currently unavailable** — never fill with estimates |

---

## 3. Evidence levels (E1 → E5)

Strength increases **upward**. E5 is strongest for educational-outcome claims. E1 is weakest for student-benefit claims but remains valid for architecture and process claims.

| Level | Name | One-line definition |
|---|---|---|
| **E5** | External educational outcome evidence | Measured learning / behaviour outcomes from an external student cohort meeting sample floors |
| **E4** | Structured external perception evidence | Structured perception / interview / acceptance evidence from **external** students |
| **E3** | Structured internal validation | Post-change blind packs, Stage 0 dogfood, validated KSI boards under disclosed internal / persona cohorts |
| **E2** | Engineering verification | Automated tests, quality contracts, checklist Pass, CI, smoke — proves structure / honesty paths |
| **E1** | Architectural / product reasoning | Constitutions, ADRs, baselines, design frameworks, estimated ΔKSI, programme specs |

### Mapping to existing repository tiers

| This hierarchy | EP-005.1 Tier | Typical artefacts |
|---|---|---|
| **E5** | Beyond B (outcome scorecard) | Filled M1–M9 at product-decision N; EP-003 Q1–Q5 Yes; effectiveness GO |
| **E4** | Tier B with **N_external** floors | ≥8 external interviews or Stage 1–2 cohort perception meeting Metrics §4 |
| **E3** | Tier B (persona / internal) + validated boards | EP-006.3 / 006.5 / 007.2 Tier B N=9; Stage 0; Validated KSI Medium |
| **E2** | Tier A | Pytest quality suites; P-001.2 / P-001.3 Pass; architecture contracts |
| **E1** | Tier D + law / design | Estimated ΔKSI; ADRs; baselines; frameworks; SIA estimates |

**Refinement note:** EP-005.1 Tier B bundled “current student perception.” P-003.5 splits **internal/persona perception (E3)** from **external student perception (E4)** because repository practice already treats `N_external = 0` as a hard block on High confidence and product-decision KPIs (GAP-02). Tier C (pre-change / exploratory) is **falsifier evidence** — it may lower claims but cannot alone raise them (see §5).

---

## 4. Level definitions

### E5 — External educational outcome evidence

**What counts**

- External cohort scorecard with M1–M9 (or successor) at sample floors for the claim class  
- Observation window meeting duration floors (≥4 weeks unless framework states otherwise)  
- EP-003 Go / No-Go educational effectiveness **GO** (or CONDITIONAL GO with named holds that do not block the specific claim)  
- Linked interview Final Test / trust codes where required by Q1–Q5  
- No open educational honesty P1 for the claim window  

**What does not count**

- Tier B perception alone  
- Validated KSI movement without outcome scorecard  
- Estimated programme ΔKSI  
- Operational GA / deploy success  

**Current Version 1 posture (2026-07-26):** **Evidence currently unavailable** (EP-007.3; G1.9 FAIL).

---

### E4 — Structured external perception evidence

**What counts**

- External student interviews meeting floors (≥8 **or** 25% of active cohort — per EP-005.1 / Metrics)  
- External Stage 1–2 blind or structured perception packs with disclosed method  
- Instrument acceptance / follow KPIs on external cohort where claimed  

**What does not count**

- Internal-only Stage 0 (N_external = 0)  
- Persona Tier B packs without external corroboration (those are **E3**)  
- Support tickets alone without structured coding  

**Current Version 1 posture:** **Evidence currently unavailable** for High / product-decision perception claims (GAP-02 open).

---

### E3 — Structured internal validation

**What counts**

- Post-change Tier B blind re-reviews (e.g. SV packs N=9) with methodology + prefer-lower  
- Stage 0 internal private beta scorecards (exploratory; disclose N)  
- Validated KSI assessment with confidence Medium+, limitations, evidence register  
- Structured dogfood checklists post-change  
- Independent KSI re-score within ±3 when filed (G1.7)  

**What does not count as E3 raise**

- Pre-change corpus used as proof of post-change lift (use as **cap / falsifier** only)  
- Programme estimate tables  

**Current Version 1 posture:** **Present** for MES / readiness / journey perception and validated KSI **62** (Medium).

---

### E2 — Engineering verification

**What counts**

- Green pytest quality-contract suites (recommendation / planning / readiness)  
- Explainability / Recommendation review checklist **Pass** (or waiver with claim restriction)  
- Architecture / constitutional verification memos for the change  
- CI (pytest + ruff) for candidate tag; smoke / health for reliability claims  
- Schema / MES pass-through tests; honest-refusal path tests  

**What does not count**

- “Tests will be written”  
- Checklist Pass treated as automatic category +10 without perception rules  

**Current Version 1 posture:** **Present** for Runtime A quality contracts under production defaults (G3–G6 structural inputs).

---

### E1 — Architectural / product reasoning

**What counts**

- Educational / Architecture Constitutions; ADRs; EP-002.9 baseline  
- Product standards (PSF, Explainability, Recommendation Quality, Release Framework)  
- Programme designs, SIAs with estimated ΔKSI, remediation plans  
- Decision / Risk / Assumption register cards (as **citations of prior reasoning**, not new proof)  

**What does not count**

- Slack opinions without artefact  
- Marketing copy drafts  

**Current Version 1 posture:** **Abundant** — necessary for process and architecture claims; **insufficient alone** for student-benefit or release claims.

---

## 5. Special evidence classes (not levels)

| Class | Role | Claim effect |
|---|---|---|
| **Falsifier (Tier C)** | Pre-change themes, honesty incidents, contradicting reviews | May **block or lower** claims; cannot raise |
| **Authority / flag state** | Production default OFF | Forces student-perceived Δ = 0 in W-PROD (E2/E3 cannot invent lift) |
| **Stale** | Past freshness window | DEFER or treat as one level lower |
| **Unavailable** | Explicit gap | Prohibits claims that require that level |

---

## 6. Confidence vs evidence level

Evidence level answers **what kind of proof exists**. Confidence (High / Medium / Low) answers **how certain we are of the score or finding**.

| Rule | Detail |
|---|---|
| E2 alone | Confidence for *student usefulness* ≤ Medium; often Low for Strong-band |
| E3 without E4 | Composite perception confidence typically **Medium**; High blocked while N_external = 0 |
| E4 + E2 agree ±5 | Eligible for High on perception categories if floors met |
| E5 + no honesty P1 | Required for educational-effectiveness **GO** language |
| Composite Low on K1/K2/K3/K8 | Gate G1.2 FAIL path |

---

## 7. Board reading order

1. Classify the artefact → E1…E5 (`EVIDENCE_CLASSIFICATION.md`).  
2. Look up permitted claims → `CLAIM_STANDARD.md`.  
3. Walk the decision tree → `CLAIM_DECISION_TREE.md`.  
4. Trace to DR / PR / gate → `CLAIM_TRACEABILITY.md`.  

---

## 8. Non-goals

This document does **not**:

- Amend P-002.1 gate criteria or evidence package structure  
- Re-score KSI or change validated scores  
- Lift recommendation-effectiveness or Exam Ready freezes  
- Declare Version 1 production-ready  

---

## References

- `knowledge/product/ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md`  
- `knowledge/product/p002_1_version_1_release_framework/VERSION_1_EVIDENCE_REQUIREMENTS.md`  
- `knowledge/product/p003_1_version1_release_dossier/Evidence_Summary.md`  
- `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`  
- `CLAIM_STANDARD.md`, `EVIDENCE_CLASSIFICATION.md` (this folder)

---

**End of EVIDENCE_HIERARCHY**
