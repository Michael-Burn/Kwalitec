# Vision

**Status:** Active  
**Owner:** Product / Architecture Office  

## Purpose

This folder holds the **Executive Product Constitution** — the permanent statement of why Kwalitec exists and how product excellence is judged through 2030.

## Hierarchy

```
PRODUCT_VISION_2030.md     ← highest product-philosophy authority
        ↓ constrains
PRODUCT_SUCCESS_FRAMEWORK  ← KSI measurement; Version 1 usefulness ≥ 80
(knowledge/product/p001_1_ksi_baseline/)
        ↓ informs prioritisation of
EXPLAINABILITY_STANDARD    ← student-facing explanation contracts (K8)
(knowledge/product/p001_2_explainability_standard/)
        ↓ complements
RECOMMENDATION_QUALITY_STANDARD ← student-facing recommendation quality (K2)
(knowledge/product/p001_3_recommendation_quality_standard/)
        ↓ informs declaration readiness via
VERSION_1_RELEASE_FRAMEWORK ← when Version 1 may be declared production-ready
(knowledge/product/p002_1_version_1_release_framework/)
        ↓ board synthesis via
VERSION_1_RELEASE_DOSSIER  ← P-003.1 board evidence pack (does not amend gates)
(knowledge/product/p003_1_version1_release_dossier/)
        ↓ informs
PRODUCT_BLUEPRINT.md       ← product strategy, model, roadmap (repo root)
        ↓ constrains
Educational Constitution   ← educational law (knowledge/educational/)
        ↓ constrains
Architecture / ADRs        ← structural decisions
        ↓ constrains
PRDs / features            ← delivery artefacts
```

Full decision hierarchy: [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md).

## Contents

| Document | Role |
|---|---|
| [`PRODUCT_VISION_2030.md`](PRODUCT_VISION_2030.md) | Executive Product Constitution — why, north star, philosophies, never-build list, final test |

KSI measurement (not a second constitution): [`../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`](../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md).

Explainability Standard (product schema / review gate; subordinate to EIP-003 + Architecture Art. IV): [`../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`](../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md).

Recommendation Quality Standard (product principles / decision frame / scorecard / review gate; subordinate to Educational Recommendation Model; complementary to P-001.2): [`../p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md`](../p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md).

Version 1 Release Framework (production-ready gates G1–G12; validated KSI + constitutional + quality + operational evidence; go / no-go): [`../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md`](../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md).

Version 1 Release Dossier (P-003.1 — Product Board synthesis of programme history, KSI, gates, risks; current recommendation **NO GO**): [`../p003_1_version1_release_dossier/`](../p003_1_version1_release_dossier/).

## Relationship with Product Blueprint

| | Vision 2030 | Product Blueprint |
|---|---|---|
| **Answers** | Why we exist; what success means; what we refuse | How we operate; who we serve; what we ship next |
| **Owns** | Philosophy, north star, design/experience/AI principles | Audiences, educational model pillars, Digital Twin role, roadmap, product promise |
| **Does not own** | Release dates, epic backlogs, API shapes | Restated philosophy that would duplicate Vision |

If Vision and Blueprint appear to conflict: **Vision wins on philosophy**; amend Blueprint to align. If educational law conflicts with either: stop and amend via the Educational Constitution process (EGI).

**KSI:** Measures educational usefulness toward the north star. Does not invent a second north star. Version 1 product-success claims require KSI ≥ 80.

## When to use each document

| Situation | Use |
|---|---|
| “Should we build this at all?” | Vision 2030 — Final Test + Never Build |
| “Does this improve pass probability / learning?” | Vision 2030 — North Star + Product Philosophy |
| “How useful is the product / are we at Version 1 usefulness?” | Product Success Framework (KSI) + Baseline Assessment |
| “May we declare Version 1 production-ready?” | Version 1 Release Framework (P-002.1) + Evidence Package + Go / No-Go |
| “What is the board-level Version 1 status / history?” | Version 1 Release Dossier (P-003.1) |
| “What student value will this programme move?” | Student Impact Assessment Template + KSI categories |
| “Who is this for and how does it fit the model?” | Product Blueprint |
| “Is this on the current roadmap?” | Product Blueprint — Product Roadmap |
| “Is this educationally lawful?” | Educational Constitution |
| “Where does this live in the codebase?” | `ARCHITECTURE.md` / ADRs |
| “How do we write a feature proposal?” | `knowledge/prd/` + Vision alignment section |

## Rules

1. Do not duplicate Vision philosophy into Blueprint, ADRs, or PRDs — **link** instead.
2. Do not invent a second north star. Trust and next-action language are expressions of the single north star (pass probability through better learning decisions). KSI is a usefulness index, not a north star.
3. Update Vision only through deliberate product strategy discussion (see Governance review process).
