# Evidence Classification

**Programme:** P-003.5 — Evidence Hierarchy & Claim Standard  
**Version:** 1.0  
**Status:** Active — classification guide  
**Effective:** 2026-07-26  
**Companion:** [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md)  
**Does not:** Change runtime, governance law, decisions, risks, assumptions, or release gates  

---

## 1. Purpose

Tell any author or Board member **how to classify** a concrete artefact into E1–E5 (or Unavailable / Falsifier / Stale) before attaching a claim.

---

## 2. Classification procedure

```
1. Name the artefact (path or ID)
2. State the claim window (W-PROD / W-GATED / named cohort)
3. Answer the decision questions below → assign level
4. Record freshness date and N (if human evidence)
5. Note falsifiers that apply
6. Only then open CLAIM_STANDARD.md
```

**Rule:** Classify the evidence **for the claim being made**, not for the folder it lives in. The same completion report may contain E2 test logs and E1 estimated ΔKSI — cite each separately.

---

## 3. Decision questions

| # | Question | If Yes → |
|---|---|---|
| Q1 | Is there a filled external cohort outcome scorecard (M1–M9 or successor) meeting sample + duration floors for this claim? | Candidate **E5** |
| Q2 | Else: is there structured perception / interview / acceptance evidence from **external** students meeting floors? | Candidate **E4** |
| Q3 | Else: is there post-change structured internal/persona validation (Tier B pack, Stage 0, validated KSI board) with method + limitations? | Candidate **E3** |
| Q4 | Else: is there engineering verification (tests, checklist Pass, CI, smoke, contract) for the structural claim? | Candidate **E2** |
| Q5 | Else: is there architectural / product reasoning (constitution, ADR, baseline, design, estimate)? | Candidate **E1** |
| Q6 | None of the above with a resolvable path? | **Unavailable** — claim prohibited if it requires evidence |

Always apply:

| Check | Effect |
|---|---|
| Pre-change only / exploratory contradicting lift? | Tag **Falsifier** — may lower, not raise |
| Past freshness window? | Tag **Stale** |
| Flag default OFF while claiming student-visible lift? | Cap W-PROD Δ = 0 (Authority class) |

---

## 4. Artefact catalogue (Version 1 landscape)

### E5 candidates (outcomes)

| Artefact family | Example path | Classification as of 2026-07-26 |
|---|---|---|
| EP-003 educational Go / No-Go | `ep003_educational_effectiveness/GO_NO_GO_REPORT.md` | Framework E1; outcome verdict **Unavailable** (PENDING EVIDENCE) |
| EP-004 effectiveness claims | `ep004_private_beta/GO_NO_GO_DECISION.md` | Programme GO WITH CONDITIONS; effectiveness **Unavailable** |
| EP-007.3 Stage 1 assessment | `ep007_3_.../EDUCATIONAL_EFFECTIVENESS_REPORT.md` | Design E1; effectiveness **NO-GO / Unavailable** |
| Cohort evidence register | `ep007_3_.../COHORT_EVIDENCE_REGISTER.md` | Empty ops → Unavailable |
| Exam pass-rate lift | (none) | **Unavailable** |

### E4 candidates (external perception)

| Artefact family | Example path | Classification as of 2026-07-26 |
|---|---|---|
| Stage 1–2 external interviews | Private beta interview packs | **Unavailable** (N_external = 0) |
| External acceptance KPIs | Instrumentled follow rates | **Unavailable** |

### E3 candidates (internal / persona validation)

| Artefact family | Example path | Level |
|---|---|---|
| MES Tier B | `ep006_3_mes_perception_validation/` | **E3** |
| Readiness Tier B | `ep006_5_readiness_perception_validation/` | **E3** |
| Journey Tier B | `ep007_2_canonical_journey_perception_validation/` | **E3** |
| Validated KSI + confidence | `ep005_1_ksi_validation_evidence/` + revalidations | **E3** (board) + **E2** inputs |
| Stage 0 Week 0 scorecard | `ep004_private_beta/` | **E3** exploratory (insufficient for product-decision KPIs) |
| EP-004 blind corpus SV-001–020 | `ep004_private_beta/blind_reviews/` | **Falsifier / baseline** for post-change lifts; not E3 raise alone |

### E2 candidates (engineering)

| Artefact family | Example path | Level |
|---|---|---|
| Recommendation / planning / readiness contract tests | `tests/services/test_*_quality_ep003_*.py` | **E2** |
| Explainability checklist Pass | Programme `EXPLAINABILITY_REVIEW.md` | **E2** |
| Recommendation checklist Pass | Programme `RECOMMENDATION_REVIEW*.md` | **E2** |
| MES delivery implementation tests | EP-006.2 completion + tests | **E2** |
| CI pytest + ruff | CI logs for candidate | **E2** |
| Security / smoke / health | `docs/ga/`, production smoke | **E2** (ops claims) |

### E1 candidates (reasoning)

| Artefact family | Example path | Level |
|---|---|---|
| Vision / Constitutions / ADRs | `PRODUCT_VISION_2030.md`; Educational Constitution; `docs/adr/` | **E1** (law) |
| PSF / P-001.2 / P-001.3 / P-002.1 | Product standards folders | **E1** (law) — gates require higher for declaration |
| Estimated ΔKSI in completion reports | EP/P `COMPLETION_REPORT.md` / SIA §5 | **E1** (planning only) |
| Remediation designs | EP-005.2 REM plans; EP-006.1 specs | **E1** until implemented + verified |
| Decision / Risk / Assumption registers | P-003.2 / P-003.3 / P-003.4 | **E1** citations of prior status — not new proof |
| Release Dossier synthesis | P-003.1 | **E1** board packaging of cited higher evidence |

---

## 5. Multi-level packages

Many programmes ship **mixed** evidence. Classify each claim line separately.

| Example claim | Required minimum | Typical package |
|---|---|---|
| “MES pass-through is implemented on Home” | E2 | EP-006.2 tests |
| “Students perceive better explainability (K8 ≥ 70)” | E3 | EP-006.3 Tier B + E2 contracts |
| “External students trust recommendations enough to follow” | E4 | External interviews / acceptance |
| “Product improves learning outcomes” | E5 | Scorecard + effectiveness GO |
| “Version 1 is production-ready” | Per-gate mix (P-002.1); G1 needs validated KSI ≥ 80 + G1.9 not NO-GO | Full evidence package |

---

## 6. Classification worksheet (copy per claim)

| Field | Value |
|---|---|
| Claim statement | |
| Claim window | W-PROD / W-GATED / other |
| Artefact path(s) | |
| Assigned level | E5 / E4 / E3 / E2 / E1 / Unavailable |
| N / cohort | |
| Freshness date | |
| Falsifiers | |
| Confidence (if scored) | High / Medium / Low |
| Permitted claim codes | (from CLAIM_STANDARD) |
| Prohibited if over-reach | |

---

## 7. Common misclassification traps

| Trap | Correct treatment |
|---|---|
| Checklist Pass = educational effectiveness | E2 only |
| Tier B persona pack = external validation | E3, not E4 |
| Validated KSI 62 = Version 1 ready | E3 board ≠ G1 PASS |
| Programme GO WITH CONDITIONS = effectiveness GO | Separable verdicts (DR-032) |
| Estimated ΔKSI sum = validated KSI | E1 only; stacking Rejected (PA-023) |
| Perception lift = outcome lift | E3 ≠ E5 (DR-033 / PA-025) |
| GA operational certification = educational ready | Ops E2 ≠ educational E5 |
| Dossier **NO GO** ignored because deploy works | DR-041 posture stands |

---

## 8. References

- [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md)  
- [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md)  
- `knowledge/product/p003_1_version1_release_dossier/Evidence_Summary.md`

---

**End of EVIDENCE_CLASSIFICATION**
