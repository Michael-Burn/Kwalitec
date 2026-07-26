# P-003.8 — Version 1 Exit Criteria

**Programme:** P-003.8 — Version 1 Exit Criteria  
**Date:** 2026-07-26  
**Status:** Complete — documentation synthesis only  
**Runtime / UI / API / governance-law / architecture / release-gate / decision / risk / assumption / maturity / dossier body changes:** None  

---

## Purpose

Canonical Version 1 Exit Criteria pack.

After reading this folder (and following its links into existing governance), a Product Board member should be able to conduct a complete Version 1 release meeting and answer:

> **Can Version 1 be released today?**

**Current answer:** **No** — Board recommendation remains **NO GO** (DR-041).

This programme **consolidates** existing requirements. It introduces **no** new policy, evidence bar, release gate, or governance rule.

---

## Documents

| Document | Role |
|---|---|
| [`VERSION1_EXIT_CRITERIA.md`](VERSION1_EXIT_CRITERIA.md) | Definitive exit criteria (XC-G1…XC-G12, XC-PKG, XC-REC) + purpose / position / assessment |
| [`BOARD_RELEASE_CHECKLIST.md`](BOARD_RELEASE_CHECKLIST.md) | Concise checklist for a release meeting |
| [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md) | GO / CONDITIONAL GO / NO GO / DEFER definitions |
| [`CURRENT_RELEASE_POSITION.md`](CURRENT_RELEASE_POSITION.md) | Freeze-date scoreboard |
| [`EXIT_TRACEABILITY.md`](EXIT_TRACEABILITY.md) | Criterion → evidence → decision → risk → gate → recommendation |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student impact (docs-only; ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion report |

---

## Board control statement

> As of 2026-07-26, Version 1 may **not** be declared production-ready. Exit criteria restating P-002.1 remain unmet on hard Gate G1 (validated KSI **62** &lt; **80**; effectiveness **NO-GO**) and on Evidence Package completeness. Private-beta Stage 0 may continue under DR-040. This pack does not flip DR-041.

---

## Quick start (release meeting)

1. Open [`CURRENT_RELEASE_POSITION.md`](CURRENT_RELEASE_POSITION.md) — confirm freeze-date **NO GO**.  
2. Walk [`BOARD_RELEASE_CHECKLIST.md`](BOARD_RELEASE_CHECKLIST.md).  
3. Score each criterion in [`VERSION1_EXIT_CRITERIA.md`](VERSION1_EXIT_CRITERIA.md) §3 against linked evidence.  
4. Apply [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md) — any hard-gate FAIL → **NO GO**.  
5. Trace disputes via [`EXIT_TRACEABILITY.md`](EXIT_TRACEABILITY.md) into DR / PR / gate artefacts.  

Deep law (execute from, do not rewrite):

| Need | Path |
|---|---|
| Gates G1–G12 | `../p002_1_version_1_release_framework/` |
| Dossier | `../p003_1_version1_release_dossier/` |
| Decisions | `../p003_2_product_decision_register/` |
| Risks | `../p003_3_product_risk_register/` |
| Assumptions | `../p003_4_product_assumption_register/` |
| Evidence / claims | `../p003_5_evidence_hierarchy/` |
| Maturity | `../p003_6_product_maturity_model/` |
| Board Charter | `../p003_7_product_board_charter/` |
| Hierarchy | `knowledge/GOVERNANCE.md` |
| Tracker | `knowledge/VERSION_1_READINESS.md` |

---

## Scope reviewed

- P-001.* · P-002.* · P-003.1–P-003.7  
- EP-003.* · EP-004.* · EP-005.* · EP-006.* · EP-007.*  
- Release Dossier; Decision / Risk / Assumption registers; Evidence Hierarchy; Product Maturity Model; Product Board Charter  
- Version 1 Readiness; Student Impact Assessments; Completion Reports; governance indexes  

---

## Constraints (honoured)

- No new release criteria beyond consolidation of existing gates / package / sign-off rules  
- No modifications to release gates, decisions, risks, assumptions, maturity, governance indexes, runtime, or services  
- No documentation edits outside this programme folder  
- No commits  

---

## Success criteria (programme)

A Product Board member can conduct a complete Version 1 release meeting using only this folder and its referenced governance artefacts — and correctly conclude **NO GO** on the 2026-07-26 evidence freeze.
