# P-003.4 — Product Assumption Register

**Programme:** P-003.4 — Product Assumption Register  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Runtime / UI / API / governance-law / architecture / release-gate / decision / risk changes:** None  

---

## Purpose

Canonical Product Assumption Register for Version 1.

After reading this folder, a Product Board member should be able to answer:

> What assumptions underpin Kwalitec today, and what evidence supports or challenges them?

And distinguish:

- what is **known**,  
- what is **believed**,  
- what has been **disproved**,  
- what still **requires evidence**.

---

## Documents

| Document | Role |
|---|---|
| [`PRODUCT_ASSUMPTION_REGISTER.md`](PRODUCT_ASSUMPTION_REGISTER.md) | Full assumption cards (PA-001…PA-042) |
| [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) | Index of Validated (known) |
| [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md) | Index of Supported + Hypothesis (believed / needs evidence) |
| [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md) | Index of Rejected + Superseded (disproved / retired) |
| [`ASSUMPTION_TRACEABILITY.md`](ASSUMPTION_TRACEABILITY.md) | Assumption ↔ DR / PR / programme / evidence map |
| [`ASSUMPTION_REVIEW_PROCESS.md`](ASSUMPTION_REVIEW_PROCESS.md) | How to propose, rate status, promote, reject, supersede |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student impact (docs-only; ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion report |

---

## Scope reviewed

- P-001.* · P-002.* · P-003.1 · P-003.2 · P-003.3  
- EP-003.* · EP-004.* · EP-005.* · EP-006.* · EP-007.*  
- Version 1 Release Dossier  
- Product Decision Register · Product Risk Register  
- Validation reports · Student Impact Assessments · completion reports  
- Architecture baselines · GOVERNANCE.md (read-only)  

---

## Constraints (honoured)

- No runtime, services, UI, or API changes  
- No amendments to governance law, architecture baselines, release gates, decisions, or risks  
- No unsupported assumptions invented  
- No commits required by this programme package itself  

---

## Quick start (board)

1. Read [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) (known).  
2. Read [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md) Hypothesis section (requires evidence).  
3. Skim [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md) (do not revive shortcuts).  
4. Open full cards for **PA-001, PA-007, PA-011, PA-014, PA-021, PA-026, PA-039**.  
5. Use [`ASSUMPTION_TRACEABILITY.md`](ASSUMPTION_TRACEABILITY.md) to jump to DR/PR/evidence.  

Upstream companions (do not replace this register):

- Decisions: [`../p003_2_product_decision_register/`](../p003_2_product_decision_register/)  
- Risks: [`../p003_3_product_risk_register/`](../p003_3_product_risk_register/)  
- Dossier: [`../p003_1_version1_release_dossier/`](../p003_1_version1_release_dossier/)  

---

## Counts

| Set | Count |
|---|---:|
| Total assumptions (PA-001…PA-042) | 42 |
| Validated (known) | 15 |
| Supported (believed, evidenced) | 11 |
| Hypothesis (believed, untested) | 4 |
| Rejected (disproved) | 10 |
| Superseded (retired) | 2 |
| Categories used | Educational, Behavioural, Product, Operational, Governance, Architecture, Release, Research |

---

## Board control statement

> Version 1 rests on **validated law and student-experience root causes**, **supported perception/structure evidence**, and **untested behavioural hypotheses**. Several convenient shortcuts are **Rejected**. External educational effectiveness remains **unproven**. Assumptions do not replace gates, decisions, or risks — they make the epistemic status of those artefacts explicit.
