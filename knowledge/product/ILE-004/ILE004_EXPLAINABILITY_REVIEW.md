# ILE-004 — Explainability Review

**Programme / Milestone ID:** ILE-004  
**Title:** Daily Mission Intelligence  
**Date:** 2026-07-28  
**Reviewer:** Implementation (completion gate)  
**Surfaces / contracts in scope:** Student Home mission intelligence panel; `DailyMissionBrief` / snapshot DTOs  
**Default explanation level(s):** L1 (hero + purpose) with L2 disclosure (mission explanation details)  
**Runtime A surfaces touched:** Home primary Mission  

---

## Mandatory verification

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | **Pass** | Brief fields pass through MES / recommendation evidence; empty when honest refusal |
| R2 | Confidence communicated appropriately | **Pass** | `mission_confidence` + optional `uncertainty`; qualitative band mapped |
| R3 | Student action is clear | **Pass** | Home CTA remains Start / Defer; skip consequence stated |
| R4 | Avoid unnecessary technical detail | **Pass** | Forbidden student + engagement terms enforced in domain invariants |
| R5 | Consistent across Runtime A | **Pass** | Composes from same Home/MES tip; does not invent alternate ranking |

## Schema & level checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Schema fields at declared level | **Pass** | Purpose, why today, evidence, benefit, after, confidence, uncertainty, explanation |
| S2 | Default level matches surface job | **Pass** | Home answers “what today / why / benefit” at L1 |
| S3 | Reading-time / length targets | **Pass** | Evidence capped in journal summary; explanation in details |
| S4 | EIP-003 four questions | **Pass** | Why today; why not else; evidence; benefit; skip consequence |
| S5 | Facts, estimates, advice distinguishable | **Pass** | Labels separate evidence vs expected benefit vs confidence |
| S6 | Advice does not replace Mission authority | **Pass** | Composition does not re-select; operationalises authorised tip |
| S7 | Pattern catalogue | **Pass** | Aligns with Mission microcopy patterns (ILE-001C0) |
| S8 | Accessibility | **Pass** | `ACCESSIBILITY.md` + presentation tests |

## Verdict

**Pass** — explainability complete for ILE-004 scope (primary daily mission brief).
