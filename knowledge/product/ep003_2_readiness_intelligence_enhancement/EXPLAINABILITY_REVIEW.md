# EP-003.2 — Explainability Review

**Programme / Milestone ID:** EP-003.2  
**Title:** Readiness Intelligence Enhancement  
**Date:** 2026-07-26  
**Reviewer:** Auto (programme execution)  
**Surfaces / contracts in scope:** Runtime A readiness dashboard/analytics surface; `build_readiness_intelligence` assessment packaging; `RuntimeAPresentationAdapter.readiness_narrative`  
**Default explanation level(s):** L2 (judgement surface)  
**Runtime A surfaces touched:** Dashboard, Analytics  

**Checklist authority:** [`EXPLAINABILITY_REVIEW_CHECKLIST.md`](../p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md)

---

## Mandatory verification items

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | **Pass** | `supporting_evidence` + driver rationales in `readiness_quality.py`; tests in `test_readiness_quality_ep003_2.py` |
| R2 | Confidence communicated appropriately | **Pass** | Student-safe High / Moderate / Low / Cannot yet be estimated; cold-start refusal |
| R3 | Student action is clear | **Pass** | Single `suggested_next_action` |
| R4 | Avoid unnecessary technical detail | **Pass** | Student labels; driver ids not primary speech; presentation uses schema summary |
| R5 | Consistent across Runtime A | **Pass** | Schema attached at ReadinessService; presentation pass-through; coverage remains separate Learning Progress fact |

---

## Schema & level checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Mandatory Explanation Schema fields | **Pass** | `judgement`, `why_this_estimate`, evidence, confidence, benefit, next action, review point |
| S2 | Default level matches surface | **Pass** | L2 for readiness judgement |
| S3 | Reading-time targets | **Pass** | Summary field for primary speech; drivers available for L2 detail |
| S4 | EIP-003 four questions | **Pass** | Facts (evidence), estimate (judgement/confidence), why, next |
| S5 | Facts / estimates / advice distinguishable | **Pass** | Estimate labelled; Mission next action is advice labelling not new plan |
| S6 | Advice does not replace Today’s Mission | **Pass** | Prefers Mission / planner titles; does not generate missions |
| S7 | Pattern catalogue | **Pass** | Readiness assessment non-recommendation guidance (§7.3) |
| S8 | Accessibility | **Pass** | Text confidence + next action; not colour-only |

---

## Verdict

**Pass** — readiness student-facing intelligence complies with P-001.2 for Runtime A surfaces in scope.
