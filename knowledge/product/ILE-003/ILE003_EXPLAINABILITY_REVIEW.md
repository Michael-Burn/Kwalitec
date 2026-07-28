# ILE-003 — Explainability Review

**Programme / Milestone ID:** ILE-003  
**Title:** Educational Timeline  
**Date:** 2026-07-28  
**Reviewer:** Implementation (completion gate)  
**Surfaces / contracts in scope:** `/student/educational-timeline`; narrative DTOs from Decision Journal evidence  
**Default explanation level(s):** L2 (reflective judgement surface)  
**Runtime A surfaces touched:** History-adjacent student presentation only (no Coach/Insights ranking)

---

## Mandatory verification

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | **Pass** | Moments cite `evidence_decision_ids`; Observation drawn from journal fields |
| R2 | Confidence communicated appropriately | **Pass** | `NarrativeCertainty` + student certainty status line; hedged pattern language |
| R3 | Student action is clear | **N/A** | Timeline is retrospective reflection — no new primary next-action tip |
| R4 | Avoid unnecessary technical detail | **Pass** | Forbidden terms enforced; presentation tests assert no Twin/orchestrator leakage |
| R5 | Consistent across Runtime A | **Pass** | Interprets same journal memory as Decision Journal; does not invent alternate Why |

## Schema & level checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Schema fields at declared level | **Pass** | Observation / Pattern / Meaning / Reflection arc |
| S2 | Default level matches surface job | **Pass** | L2 reflective reading |
| S3 | Reading-time / length targets | **Pass** | Journey sample capped; sections omit when empty |
| S4 | EIP-003 four questions | **Pass** (adapted) | Retrospective Know/Estimate/Why/Next → Observation/Pattern/Meaning/Reflection |
| S5 | Facts, estimates, advice distinguishable | **Pass** | Certainty labels + hedged “pattern” vs observation |
| S6 | Advice does not replace Mission authority | **Pass** | No recommendation ranking or Mission override |
| S7 | Pattern catalogue | **N/A** | Reflective chronology, not tip-type catalogue speech |
| S8 | Accessibility | **Pass** | `ACCESSIBILITY.md` + a11y tests |

## Verdict

**Pass** — explainability complete for ILE-003 scope (reflective narrative over journal evidence).
