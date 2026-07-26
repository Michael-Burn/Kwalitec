# Version 1 Release Dossier — Executive Summary

**Programme:** P-003.1  
**Audience:** Product Board  
**Date:** 2026-07-26  
**Length target:** ≤ 2 pages  

---

## What Kwalitec is

Kwalitec is an adaptive learning companion for students preparing for professional qualification examinations (IFoA, SOA, CAA, CAS, and related bodies). It exists to improve study decisions — structure, consistency, objective feedback, personalised guidance, and confidence — not to replace teachers or textbooks.

**North star (Vision 2030):** Students who consistently use Kwalitec should have a materially higher probability of passing their examinations than students who do not.

**Daily product question:** What is the highest-value thing this student should do next?

---

## Educational philosophy

- Measure **learning**, not activity (time-on-site and question counts are not success).  
- AI improves judgement; it does not replace it. Every recommendation must be transparent, explainable, evidence-based, and educationally defensible.  
- Absence of evidence remains **unknown** — no mastery theatre, no dual educational truths, no opaque AI as educational fact.  
- Curriculum-first, deterministic cores: planning, readiness, and recommendations must be reproducible from the same inputs.

Full text: `knowledge/product/vision/PRODUCT_VISION_2030.md`. Educational law: `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`.

---

## Target users

| Audience | Role |
|---|---|
| **Primary** | Serious candidates for professional actuarial / related qualifications |
| **Secondary** | Training providers and employers supporting qualification programmes |

Public registration is **not** exposed. Version 1 context is invite-only / private beta, not public launch.

---

## Runtime A (what students use)

**Runtime A** is the Education OS student product path: login → Student Home → Mission / Session → review → tomorrow. Under **production defaults**, legacy Runtime A services remain the student-visible educational authority. Twin / consumer-chain cutover flags default **OFF**.

Three educational authorities (quality-contracted; not replaced by presentation):

| Concern | Owner |
|---|---|
| What to study next (recommendations) | RecommendationService |
| Today’s mission / plan | PlanningService |
| Readiness / progress honesty | ReadinessService |

Presentation delivers authored explanations (MES) to Home, Coach, Mission, and Analytics. Presentation must not invent evaluation or planning.

Architecture baseline: `knowledge/architecture/ep002_9_programme_exit_certification/AUTHORITATIVE_ARCHITECTURE_BASELINE.md`.

---

## Educational authority (governance)

| Layer | Owns |
|---|---|
| Vision 2030 | Why; Final Test; Never-Build |
| Product Success Framework (KSI) | Educational usefulness measurement; Version 1 usefulness bar **KSI ≥ 80** |
| Explainability / Recommendation Quality Standards | Student-facing explanation and recommendation law |
| Version 1 Release Framework (P-002.1) | When Version 1 may be declared **production-ready** (gates G1–G12) |
| Educational Constitution + EVF | Educational meaning and educational trust to release |
| Architecture Constitution | One runtime; no second educational brain in production defaults |

---

## Current release status (evidence-bound)

| Measure | Value | Source |
|---|---|---|
| Validated KSI (W-PROD) | **62** | EP-007.2 `K1_REVALIDATION.md` |
| Version 1 target | **≥ 80** | Product Success Framework |
| Gap | **18 points** | — |
| Gate G1 overall | **FAIL** | G1.1 (KSI), G1.9 (effectiveness); G1.7 HOLD |
| Gate G1.5 (K8 ≥ 70) | **PASS** (K8 = **70**) | EP-006.3 |
| Educational effectiveness | **NO-GO / PENDING EVIDENCE** | EP-003; EP-007.3 G1.9 |
| Private beta execution | **GO WITH CONDITIONS** | EP-004 (Stage 1 ops blocked on privacy) |
| Full G1–G12 evidence package | **Incomplete** | G1 slice only; G2–G12 boards not assembled for declaration |
| Version 1 production-ready declaration | **Not permitted** | P-002.1 |

---

## Why Version 1 is not released

1. **Validated educational usefulness is below bar** — KSI **62** vs required **≥ 80** (Gate G1.1 FAIL).  
2. **Educational effectiveness is unproven** — external cohort N = **0**; Privacy Review unsigned; effectiveness **NO-GO** (Gate G1.9 FAIL).  
3. **Declaration package incomplete** — G2–G12 lack a full assembled evidence board for a production-ready claim.

Operational GA and architecture consolidation are **necessary but insufficient**. Perception improvements (MES, readiness unpackability, single Home) raised validated KSI from **59 → 62** and cleared G1.5; they do **not** clear G1.1 or G1.9.

---

## Board recommendation

# NO GO

Do not declare Kwalitec Version 1 production-ready. Continue private-beta Stage 0 under EP-004 conditions; clear Privacy Review before Stage 1; assemble remaining gate evidence before any future declaration board.

Detail: [`Version_1_RELEASE_DOSSIER.md`](Version_1_RELEASE_DOSSIER.md) §11; [`Release_Gates.md`](Release_Gates.md); [`Version1_State.md`](Version1_State.md).
