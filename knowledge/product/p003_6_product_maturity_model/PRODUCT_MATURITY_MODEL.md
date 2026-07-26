# Product Maturity Model

**Programme:** P-003.6 — Product Maturity Model  
**Version:** 1.0  
**Status:** Active — documentation standard  
**Effective:** 2026-07-26  
**Claim window freeze:** Aligns with P-003.1–P-003.5 evidence as of 2026-07-26  
**Does not:** Change runtime, governance law, decisions, risks, assumptions, or release gates  

---

## 1. Purpose

Canonical **Product Maturity Model** for Kwalitec.

The Product Board uses this model to answer, from evidence only:

> Where is Kwalitec organisationally mature, where is it emerging, where is it experimental, and where should investment focus after Version 1?

This model evaluates **organisational maturity of major capabilities** — not implementation completeness, feature count, or estimated ΔKSI.

---

## 2. What this is / is not

| This is | This is not |
|---|---|
| Organisational capability maturity | Code-completion checklist |
| Evidence-bound levels (prefer lower) | Inference from “programmes exist” |
| Companion to Release Dossier / Decision / Risk / Assumption / Evidence Hierarchy | Replacement for P-002.1 gates or P-003.1 go/no-go |
| Board investment lens after Version 1 | A Version 1 production-ready declaration |

**Hard rule:** Never raise a level without cited evidence. Missing evidence = do not invent maturity. Prefer lower when conflicted (P-003.5 / PSF honesty).

---

## 3. Maturity scale

Repository evidence supports the programme’s five-level scale without adjustment. No Level 4 or Level 5 ratings are justified as of 2026-07-26 (`N_external = 0`; effectiveness **NO-GO**; Version 1 **NO GO**).

| Level | Name | Organisational meaning |
|---:|---|---|
| **1** | **Concept** | Capability is designed, specified, or framed in law/docs. Operating practice for that capability’s purpose has not started, or existence is documentary only relative to the purpose. |
| **2** | **Implemented** | Capability exists in code and/or process and can be operated, but lacks structured internal validation that it achieves its organisational purpose under production-relevant conditions. |
| **3** | **Internally Validated** | Structured internal validation (engineering verification and/or internal perception / Stage 0 / validated boards — P-003.5 **E2/E3**) confirms the capability works as intended under disclosed internal, persona, or production-default conditions. External corroboration absent. |
| **4** | **Externally Validated** | Structured external student/cohort evidence (P-003.5 **E4+**) confirms the capability’s purpose at sample floors. |
| **5** | **Operationally Mature** | Sustained production operation with release-class evidence complete, repeatable ops, and no open blocking residuals for that capability’s declared purpose. |

### Mapping to evidence hierarchy (P-003.5)

| Maturity level | Typical evidence ceiling |
|---|---|
| 1 Concept | **E1** reasoning / frameworks without operating practice |
| 2 Implemented | Code/process present; may include partial **E2** without purpose validation |
| 3 Internally Validated | **E2** + **E3** under disclosed cohorts / W-PROD |
| 4 Externally Validated | **E4** (and outcome **E5** where purpose is educational effectiveness) |
| 5 Operationally Mature | Sustained **E4/E5** + release-class ops evidence (G2–G12 class) |

---

## 4. Board heatmap (one page)

**As of:** 2026-07-26  
**Ceiling:** No capability is Level 4 or Level 5. “Green” means **strongest internal organisational maturity**, not external or operationally mature.

| Colour | Board meaning | Rule used here |
|---|---|---|
| **Green** | Mature *for Version 1 organisational purpose within the Level 3 ceiling* | Level 3 with strong contracts / boards and clear operating authority |
| **Amber** | Emerging | Level 3 with thin floors / incomplete packs, or solid Level 2 |
| **Red** | Experimental / investment focus / claim-blocking gap | Level 1, or Level 2 with production defaults OFF / purpose unproven |

| Capability | Level | Heat |
|---|---:|---|
| Architecture | 3 | Green |
| Runtime A | 3 | Green |
| Recommendation | 3 | Amber |
| Planning | 3 | Green |
| Readiness | 3 | Amber |
| Explainability | 3 | Green |
| Journey | 3 | Amber |
| Personalisation | 2 | Red |
| Learning Twin | 2 | Red |
| Validation | 3 | Amber |
| Governance | 3 | Green |
| Operational Readiness | 2 | Amber |
| Release Readiness | 2 | Red |
| Educational Effectiveness | 1 | Red |
| Commercial Readiness | 1 | Red |
| Knowledge Base | 3 | Green |
| Documentation | 3 | Amber |
| Product Board | 3 | Green |
| Evidence | 3 | Amber |
| Research | 2 | Amber |

### Board read in one breath

- **Mature (Green):** Architecture, Runtime A, Planning, Explainability, Governance, Knowledge Base, Product Board — internally validated organisational capabilities under production defaults / active board law.  
- **Emerging (Amber):** Recommendation, Readiness, Journey, Validation, Evidence, Documentation, Operational Readiness, Research — present and partly validated; thin floors, incomplete declaration packs, or process not yet release-class.  
- **Experimental / focus (Red):** Personalisation, Learning Twin, Release Readiness, Educational Effectiveness, Commercial Readiness — gated OFF, T7 not declared, Version 1 **NO GO**, effectiveness **NO-GO**, or commercial **NOT STARTED**.

**Version 1 is not organisationally mature as a release.** Strongest maturity is **internal educational-runtime and governance** maturity, not external educational proof or commercial launch readiness.

Detail: [`MATURITY_ASSESSMENT.md`](MATURITY_ASSESSMENT.md). Capability definitions: [`CAPABILITY_MATURITY.md`](CAPABILITY_MATURITY.md). Investment lens: [`ROADMAP_IMPLICATIONS.md`](ROADMAP_IMPLICATIONS.md).

---

## 5. Scoreboard freeze (context, not maturity itself)

| Measure | Value | Source |
|---|---|---|
| Validated KSI (W-PROD) | **62** | EP-007.2 `K1_REVALIDATION.md` |
| Target | **≥ 80** | Product Success Framework |
| Gate G1 | **FAIL** | P-003.1 `Release_Gates.md` |
| Gate G1.5 (K8) | **PASS** (70) | EP-006.3 |
| Educational effectiveness | **NO-GO / PENDING EVIDENCE** | EP-007.3 |
| `N_external` | **0** | EP-007.3 / P-003.5 |
| Version 1 board recommendation | **NO GO** | P-003.1 |
| Twin Ready (T7) | **Not declared** | EP-002.9 Twin Readiness Assessment |
| Commercial readiness | **NOT STARTED** | `knowledge/VERSION_1_READINESS.md` |

Category board (EP-007.2): K1 **72**, K2 **55**, K3 **65**, K4 **55**, K5 **63**, K6 **50**, K7 **58**, K8 **70**.

---

## 6. How to use

1. Open this heatmap (§4).  
2. For any capability, open [`MATURITY_ASSESSMENT.md`](MATURITY_ASSESSMENT.md) — Current Level, Evidence, Confidence, Outstanding Work, Next Review Trigger.  
3. Trace evidence paths in [`MATURITY_TRACEABILITY.md`](MATURITY_TRACEABILITY.md).  
4. Prioritise post–Version 1 investment with [`ROADMAP_IMPLICATIONS.md`](ROADMAP_IMPLICATIONS.md) — **evidence first**, not code first, where Red is claim-blocking.  
5. Classify claim language with P-003.5 — maturity Level 3 does **not** unlock C-EDU, C-VAL-E, C-V1, or C-COM freezes.

---

## 7. Authority and companions

| Companion | Path | Relationship |
|---|---|---|
| Version 1 Release Dossier | `../p003_1_version1_release_dossier/` | Release synthesis; **NO GO** — not replaced |
| Decision Register | `../p003_2_product_decision_register/` | Decisions unchanged |
| Risk Register | `../p003_3_product_risk_register/` | Risks unchanged |
| Assumption Register | `../p003_4_product_assumption_register/` | Assumptions unchanged |
| Evidence Hierarchy | `../p003_5_evidence_hierarchy/` | Claim evidence lens; maturity maps to E1–E5 |
| Release Framework | `../p002_1_version_1_release_framework/` | Gates G1–G12 unchanged |
| Readiness tracker | `../../VERSION_1_READINESS.md` | Operational statuses |

---

## 8. Control statement

> Organisational maturity is not Version 1 production-ready. As of 2026-07-26, no major capability is Externally Validated (Level 4) or Operationally Mature (Level 5). Green cells are strongest **internal** maturity. Red cells mark where additional **evidence**—not necessarily additional code—is required before honesty permits stronger claims.
