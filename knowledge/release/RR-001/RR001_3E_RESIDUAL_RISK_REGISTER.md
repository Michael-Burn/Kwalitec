# RR-001.3E — Residual Risk Register

**Programme:** RR-001 — Governance-driven Educational Remediation  
**Work Package:** RR-001.3E — Governance Closure & Release Readiness  
**Date:** 2026-07-28  
**Status:** Active — Accepted / Contained operational residuals after educational NCR closure  
**Authority:** Board acceptance via RR-001.3E governance closure  
**Companion:** `ALPHA_REMEDIATION_REGISTER.md` · `RR001_3E_GOVERNANCE_CLOSURE_REPORT.md`

---

## Purpose

Catalogue every residual that remains after RR-001 educational remediation, with **Board justification**, **owner**, and **release discipline**. Residuals here are **not** open educational-copy NCRs.

Status: **Accepted** · **Contained** · **Watch** · **Deferred** (scheduled outside RR-001)

---

## Summary

| Class | Count | Gate impact |
|-------|------:|-------------|
| Contained operational Criticals | 2 | Ops discipline required for Alpha honesty |
| Contained feature-flag / enablement | 6+ | Keep OFF until dedicated recertification |
| Accepted preventive (EGC-R11) | 1 | When notifications educationalise |
| Watch (mitigated density) | 2 | Monitor; no open NCR |
| Deferred experience / polish | 8 | Not RP-002 educational blockers if disclosed |
| Architecture / parallel-stack | 3 | Quarantine / do-not-claim |

---

## A. Contained operational Criticals

| ID | Residual | Owner | Board justification | Release discipline |
|----|----------|-------|---------------------|--------------------|
| **RR-C04 / RR-H01** | Sole-runtime misconfiguration reintroduces competing homes | Release Engineering + Product | Not a code defect on default path; configuration integrity risk | Protect `KWALITEC_V2_SOLE_RUNTIME`; sole-runtime smoke before any Alpha claim |
| **RR-C05** | Public registration accidentally exposed | Security + Product | Auth intentionally login-only for Alpha | Do not add public register; reject accidental route exposure in review |

---

## B. Feature-flag / gated capability residuals

| ID | Residual | Owner | Board justification | Release discipline |
|----|----------|-------|---------------------|--------------------|
| **RR-H03 / XR-14** | Flag-scope honesty if QC / UJ / Runtime C enabled | Product + Educational Governance | Educational speech Contained while OFF; enablement is a new certification event | Keep **OFF** until surface-specific RP/educational review |
| **EGC-R07 enablement** | Runtime C after rename | Engineering + Educational Governance | Rename closed system-narrator NCR; enablement still Contained | No Runtime C ON without Sensei-attribution re-check |
| **RR-H13** | Runtime C dual educational context | Product | Same Contained family | Keep OFF |
| **RR-M17** | Accidental UJ / Experience Feedback enable | Release Engineering | Prefer Contained OFF over silent dual journey | Checklist gate |
| **RR-L06 / RR-L07** | Unified Journey / Deep-Recovery-Confidence flags | Product | Gated surfaces not Alpha default story | Keep OFF / disclosed |
| **NCR-014 ops** | Flag speech residual class | Educational Governance | Copy Closed; ops Contained | Same as H03 |

---

## C. Accepted preventive / future programmes

| ID | Residual | Owner | Board justification | Release discipline |
|----|----------|-------|---------------------|--------------------|
| **EGC-R11 / AC-13 / RR-H06** | Notifications educational mentor risk | Product (notification programme) | Capability not built; preventive residual is correct governance | No educational notification without D08 tagging + EGC-R11 checklist |
| **OQ-04** | Mastery student-facing exposure policy | Educational Governance | Outside assigned RR-001 NCR set | Decide before any Mastery marketing claim |
| **OQ-R01** | Session notes → Decision Journal mirror | Architecture + Educational | Architecture residual; Journal remains sole durable host | Do not invent second memory |

---

## D. Watch (mitigated — no open NCR)

| ID | Residual | Owner | Board justification | Release discipline |
|----|----------|-------|---------------------|--------------------|
| **AC-09** | MI + MES hero density | Product Design + Educational | RR-001.2 disclosure mitigated dual-brief feel | Monitor Home cognitive load in RP-002 dogfood |
| **OQ-01** | PX docs vs `product_language.py` reconciliation | Engineering + Educational | In-scope lexicon Closed; doc drift is maintenance | Prefer `product_language.py` as runtime authority |
| **RR-H08 / XR-20** | Cohort UX validation not executed | Product Research | Implementation evidence exists; cohort perception not yet validated | Required input for **validated** KSI / RP-002 perception claims — not a blocker for *starting* RP-002 |
| **Naming density dogfood** | Home Sensei density tuning | Product Design | OQ-02 policy Closed; cohort may refine | Adjust only under DG-001.1 naming policy |

---

## E. Deferred experience / polish (not educational NCR blockers)

| ID | Residual | Owner | Board justification |
|----|----------|-------|---------------------|
| RR-M02 | Welcome CTA extra click under sole runtime | Product | Mild journey friction; disclosed |
| RR-M03 | Onboarding skip under-orients | Product | Skip path residual |
| RR-M05 | History ≠ legacy analytics charts | Product | Epistemology bridge Closed; chart story Deferred |
| RR-M07 | Sparse Journal / Timeline / History early | Product | Honesty empties Closed; content density Deferred |
| RR-M09 | Sensei voice inconsistent on chrome | Product / Design | Partial polish; core narrator Closed |
| RR-M10 | Orphan `/assessment` vs QC story | Product | Contained / Deferred; not default Mission path |
| RR-M11 | Export omits Decision Journal | Product | Data export completeness Deferred |
| RR-L03 | Assessment flash brands Kwalitec | Product | Low polish |
| RR-L08 | Telemetry without closed student loop | Product / Privacy | Research honesty Deferred |

---

## F. Architecture / parallel-stack residuals

| ID | Residual | Owner | Board justification | Release discipline |
|----|----------|-------|---------------------|--------------------|
| **AC-17** | Latent MissionOptimizer as mission-shaped authority | Architecture | Unrendered; quarantine residual | Do not rewire templates to surface dual Mission generators |
| **DG-001.3-D08** | Parallel reflection stacks | Architecture | Law names residual; student map Closed | Future consolidation programme |
| **`src/` Education OS labels** | Legacy quick-action lexicon lag | Engineering | Parallel stack; sole runtime is `/student` | Do not claim `src/` path as Alpha sole story |
| **RR-H14** | Curriculum V1/V2 breakage via unrelated change | Architecture + CI | Invariant Contained by process | Keep V1/V2 loadable; CI green |
| **RR-H07** | ILE-005 migration discipline | Release Engineering | Migration Contained | Checklist before reflection migration claims |
| **RR-H09** | Defer ≠ ranking change | Product | By-design preference-only | Keep disclosure |
| **RR-H10** | Thin Revision without adaptive authority | Product | Adaptive OFF disclosed; primacy Closed | Do not claim adaptive Revision |
| **RR-M04 / M08 / M18 / M19 / M20 / M21** | Soft-fail / orphaning / CAP conditions / forbidden terms | Various | Contained / disclosed inventory | Inventory honesty; no silent enable |

---

## Board acceptance statement

The Product Board accepts the residuals in sections A–F as **operational / programme residuals**, not as open educational-copy Non-Compliances under the RR-001 assigned NCR set.

Acceptance does **not**:

- authorise enabling Contained flags without recertification  
- authorise unqualified “educationally governed Alpha” marketing  
- substitute for independent **RP-002** educational re-score  
- close Version 1 production-ready gates (G1–G12)

Acceptance **does**:

- allow RP-002 to treat educational-copy NCR-001–022 as remediated inputs  
- require every residual above to retain a named owner  
- require Contained Criticals to remain in release checklists

---

## Residual ownership roster

| Owner | Residuals |
|-------|-----------|
| Release Engineering | RR-C04, RR-C05 (ops with Security), RR-H07, RR-M17, sole-runtime smoke |
| Product | Flag enablement family, Deferred polish, RR-H06/H08, AC-09 monitor |
| Educational Governance | EGC-R11 intake, OQ-04, flag educational re-cert, RP-002 scope |
| Architecture | AC-17 quarantine, D08 parallel stacks, V1/V2 invariant (with CI) |
| Security | RR-C05 registration posture |
| Engineering | OQ-01 maintenance, `src/` lexicon lag, CI |

---

**End of RR001_3E_RESIDUAL_RISK_REGISTER**
