# P-003.3 — Product Risk Register

**Programme:** P-003.3 — Product Risk Register  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Runtime / UI / API / governance-law / architecture / release-gate / decision changes:** None  

---

## Purpose

Canonical Product Risk Register for Version 1.

After reading this folder, a Product Board member should be able to answer:

> What could prevent Version 1 from being released successfully?

---

## Documents

| Document | Role |
|---|---|
| [`PRODUCT_RISK_REGISTER.md`](PRODUCT_RISK_REGISTER.md) | Full risk cards (PR-001…PR-026) + rating matrix |
| [`ACTIVE_RISKS.md`](ACTIVE_RISKS.md) | Index of risks that remain material now |
| [`CLOSED_RISKS.md`](CLOSED_RISKS.md) | Fixed / mitigated history (CR-001…CR-005) |
| [`RISK_TRACEABILITY.md`](RISK_TRACEABILITY.md) | Risk ↔ R/DR/programme/gate/evidence map |
| [`RISK_REVIEW_PROCESS.md`](RISK_REVIEW_PROCESS.md) | How to propose, rate, review, close, re-open |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student impact (docs-only; ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion report |

---

## Scope reviewed

- P-001.* · P-002.* · P-003.1 · P-003.2  
- EP-003.* · EP-004.* · EP-005.* · EP-006.* · EP-007.*  
- Version 1 Release Dossier (incl. `Risk_Summary.md`, `Release_Gates.md`)  
- Product Decision Register  
- Student Impact Assessments · validation / Go-No-Go · completion reports  
- `VERSION_1_READINESS.md` · private beta Privacy Review / cohort / feedback  
- Architecture exit / RISK_ASSESSMENT artefacts (read-only)  

---

## Constraints (honoured)

- No runtime, services, UI, or API changes  
- No amendments to governance law, architecture baselines, release gates, or decisions  
- No unsupported risks invented  
- No commits required by this programme package itself  

---

## Quick start (board)

1. Read [`ACTIVE_RISKS.md`](ACTIVE_RISKS.md) board reading order (15 minutes).  
2. Open full cards for **PR-001, PR-002, PR-003, PR-006, PR-019**.  
3. Use [`RISK_TRACEABILITY.md`](RISK_TRACEABILITY.md) to jump to evidence and decisions.  
4. For fixed incidents, see [`CLOSED_RISKS.md`](CLOSED_RISKS.md).  

Upstream synthesis (does not replace this register): [`../p003_1_version1_release_dossier/Risk_Summary.md`](../p003_1_version1_release_dossier/Risk_Summary.md).  
Controls memory: [`../p003_2_product_decision_register/ACTIVE_DECISIONS.md`](../p003_2_product_decision_register/ACTIVE_DECISIONS.md).

---

## Counts

| Set | Count |
|---|---:|
| Product risks (PR-001…PR-026) | 26 |
| Red Overall | 9 |
| Closed / mitigated (CR-001…CR-005) | 5 |
| Categories used | Educational, Operational, Release, Governance, Evidence, Privacy, Technical, Product, Adoption, Deployment |

---

## Board control statement

> Release risk is dominated by **unproven educational effectiveness** and **sub-bar validated KSI (62 &lt; 80)**, compounded by **privacy-blocked external evidence** (external N = 0). Under P-002.1, these force **NO GO** on Version 1 production-ready declaration.
