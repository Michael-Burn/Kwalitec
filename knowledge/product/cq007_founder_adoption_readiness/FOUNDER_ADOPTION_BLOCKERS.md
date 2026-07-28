# CQ-007 — Founder Adoption Blockers

**Programme:** CQ-007 — Founder Adoption Readiness  
**Date:** 2026-07-28  
**Rule:** Only **Critical** and **Major** blockers prevent adoption.  
**Adoption test:** Would this realistically stop the founder from using Kwalitec every day?

---

## Classification

| Class | Meaning | Adoption effect |
|---|---|---|
| **Critical** | Breaks the daily loop or destroys trust | Prevents adoption until fixed |
| **Major** | Repeatedly derails daily use under scarce time | Prevents adoption until fixed or explicitly accepted |
| **Minor** | Friction / polish | Does not prevent adoption |
| **Constraint** | Known V1 limitation or operational precondition | Must be accepted for GO WITH CONSTRAINTS; not an engineering fix in CQ-007 |

---

## Prioritised table

| ID | Severity | Founder impact | CRI domain(s) | Est. effort | Recommendation |
|---|---|---|---|---|---|
| **C-01** | **Constraint** | Session practice is topic-threaded reflective scaffold — not syllabus-authored CS1 item banks. Exclusive *content* preparation still needs ActEd/CMP/past papers. | CR4, CR8 | N/A (V2 / out of CQ-007 scope) | **Accept for Version 1.** Document on Board. Do not invent item banks in CQ-007. |
| **C-02** | **Constraint** | All Engineering CRI gains (43→53) are provisional; Strong-band CR1–CR6 claims need founder dogfood. | CR1–CR6, CR8 | Founder Validation window | **Accept.** Open Founder Validated CRI after Board acceptance of CQ-007. |
| **C-03** | **Constraint** | Founder Console landing ≠ Student Home; dogfood must use student path under sole runtime. | CR5, CR7 | Ops setup minutes | **Accept.** Dogfood as student role / student account. |
| **C-04** | **Constraint** | Production must remain `KWALITEC_V2_SOLE_RUNTIME=1`; dual-run reintroduces competing homes. | CR5, CR1 | Ops vigilance | **Accept / maintain.** Do not disable sole runtime for founder adoption. |
| **B-01** | **Minor** | Fresh-start Home hero density slows scarce-time “what now?” | CR1, CR2 | Medium (risks redesign) | Defer to Founder Validation observations; no CQ-007 redesign. |
| **B-02** | **Minor** | Continue resume hops via Overview then redirects to active surface. | CR2 | Small | Optional later polish; not adoption-blocking. |
| **B-03** | **Minor** | Brand Home link mid-session has no confirm (recoverable via Continue). | CR2 | Small | Optional later polish. |
| **B-04** | **Minor** | `preferred_session_minutes` not echoed at Home entry. | CR2 | Small–Med | Defer; duration label already present. |
| **B-05** | **Minor** | Two-POST activity advance feels mechanical. | CR4 | Med (UX) | Defer; no redesign in CQ-007. |
| **B-06** | **Minor** | History defers “why it mattered” to Journal/Timeline. | CR3, CR5 | Small | Defer; not on daily critical path. |
| **B-07** | **Minor** | Residual craft (empty-state macros, auth login primitives). | CR6, CR5 | Small–Med | Defer; CQ-006 Critical craft closed. |

---

## Critical and Major blockers

**None.**

CQ-002–CQ-006 closed the Critical/Major items that previously blocked daily adoption (extra Begin, dual Next, empty dead-ends, Start-on-resume, re-commitment POST, generic activity copy without topic thread, guidance “evidence” jargon, unfinished stylesheet boundaries).

Remaining substance-depth and validation gaps are **Constraints**, not fixable engineering blockers under CQ-007 rules (no educational engine changes, no redesign, no V2 capabilities).

---

## Implementation decision

| Question | Answer |
|---|---|
| Critical/Major blockers present? | **No** |
| CQ-007 implementation required? | **No** |
| Commit type for programme delivery | `docs(cq-007)` only |

---

**End of Founder Adoption Blockers**
