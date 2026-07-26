# P-003.5 — Evidence Hierarchy & Claim Standard

**Programme:** P-003.5 — Evidence Hierarchy & Claim Standard  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Runtime / UI / API / governance-law / architecture / release-gate / decision / risk / assumption changes:** None  

---

## Purpose

Canonical Evidence Hierarchy and Claim Standard for Version 1.

After reading this folder, a Product Board member should be able to answer:

> What claims are we allowed to make?

And never again need to ask tribally:

> Can we say this publicly?

---

## Documents

| Document | Role |
|---|---|
| [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md) | E1–E5 levels, strength rules, repo tier mapping |
| [`EVIDENCE_CLASSIFICATION.md`](EVIDENCE_CLASSIFICATION.md) | How to classify artefacts; traps; worksheet |
| [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md) | Claim codes, minima, freezes, Version 1 posture card |
| [`CLAIM_DECISION_TREE.md`](CLAIM_DECISION_TREE.md) | Board tree: Question → Evidence → Claim → Approval → Public |
| [`CLAIM_TRACEABILITY.md`](CLAIM_TRACEABILITY.md) | Evidence → Claim → Decision → Risk → Gate |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student impact (docs-only; ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion report |

---

## Evidence levels (summary)

| Level | Name |
|---|---|
| **E5** | External educational outcome evidence |
| **E4** | Structured external perception evidence |
| **E3** | Structured internal validation |
| **E2** | Engineering verification |
| **E1** | Architectural / product reasoning |

Refinement vs EP-005.1 Tier A–D: this hierarchy splits internal perception (**E3**) from external perception (**E4**) and places outcome scorecards at **E5**, matching repository practice that `N_external = 0` blocks High / effectiveness claims.

---

## Claim codes (summary)

| Code | Family |
|---|---|
| C-IMP | Implementation complete |
| C-STR | Structural / quality verified |
| C-VAL-I | Validated internal improvement |
| C-VAL-E | Validated external perception |
| C-EDU | Educational effectiveness |
| C-BEN | Student benefit (outcome / Final Test) |
| C-REL | Release readiness (ops) |
| C-V1 | Version 1 production-ready |
| C-COM | Commercial / marketing |
| C-REC | Board Version 1 recommendation |

---

## Scope reviewed

- Entire governance history (GOVERNANCE.md read-only)  
- Validation programmes EP-001…EP-007.*  
- Version 1 Release Dossier (P-003.1)  
- Product Decision Register (P-003.2)  
- Product Risk Register (P-003.3)  
- Product Assumption Register (P-003.4)  
- Student Impact Assessments & completion reports  
- Version 1 readiness / P-002.1 evidence requirements  
- PSF / Explainability / Recommendation standards  

---

## Constraints (honoured)

- No runtime, services, UI, or API changes  
- No amendments to governance law, architecture baselines, release gates, decisions, risks, or assumptions  
- No commits required by this programme package itself  

---

## Quick start (board)

1. Open [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md) §7 posture card (what is allowed **today**).  
2. For a new sentence, walk [`CLAIM_DECISION_TREE.md`](CLAIM_DECISION_TREE.md).  
3. Classify evidence with [`EVIDENCE_CLASSIFICATION.md`](EVIDENCE_CLASSIFICATION.md).  
4. Trace consequences in [`CLAIM_TRACEABILITY.md`](CLAIM_TRACEABILITY.md).  

Upstream companions (do not replace this standard):

- Dossier: [`../p003_1_version1_release_dossier/`](../p003_1_version1_release_dossier/)  
- Decisions: [`../p003_2_product_decision_register/`](../p003_2_product_decision_register/)  
- Risks: [`../p003_3_product_risk_register/`](../p003_3_product_risk_register/)  
- Assumptions: [`../p003_4_product_assumption_register/`](../p003_4_product_assumption_register/)  
- Gates: [`../p002_1_version_1_release_framework/`](../p002_1_version_1_release_framework/)  

---

## Board control statement

> Claims require classified evidence. Engineering verification (E2) and internal perception (E3) do not unlock educational effectiveness (E5), external validation (E4), commercial educational marketing (C-COM freezes), or Version 1 production-ready (C-V1). As of 2026-07-26 the Board recommendation remains **NO GO**; public educational outcome claims remain **prohibited**.
