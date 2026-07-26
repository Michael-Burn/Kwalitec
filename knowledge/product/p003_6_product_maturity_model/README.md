# P-003.6 — Product Maturity Model

**Programme:** P-003.6 — Product Maturity Model  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Runtime / UI / API / governance-law / architecture / release-gate / decision / risk / assumption changes:** None  

---

## Purpose

Canonical Product Maturity Model for Version 1 Product Board use.

After reading this folder, a Product Board member should immediately understand:

- where Kwalitec is **mature** (strongest internal organisational maturity),  
- where it is **emerging**,  
- where it remains **experimental**,  
- where investment should focus **after Version 1** — especially where **evidence**, not code, is required.

---

## Documents

| Document | Role |
|---|---|
| [`PRODUCT_MATURITY_MODEL.md`](PRODUCT_MATURITY_MODEL.md) | Scale, rules, **one-page executive heatmap** |
| [`CAPABILITY_MATURITY.md`](CAPABILITY_MATURITY.md) | Capability catalogue and raise/do-not-raise rules |
| [`MATURITY_ASSESSMENT.md`](MATURITY_ASSESSMENT.md) | Level / Evidence / Confidence / Outstanding / Next trigger per capability |
| [`MATURITY_TRACEABILITY.md`](MATURITY_TRACEABILITY.md) | Capability → evidence → claims → gates |
| [`ROADMAP_IMPLICATIONS.md`](ROADMAP_IMPLICATIONS.md) | Post–Version 1 investment lens (non-binding) |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student impact (docs-only; ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion report |

---

## Maturity scale (summary)

| Level | Name |
|---:|---|
| 1 | Concept |
| 2 | Implemented |
| 3 | Internally Validated |
| 4 | Externally Validated |
| 5 | Operationally Mature |

**As of 2026-07-26:** no capability is Level 4 or Level 5 (`N_external = 0`; effectiveness **NO-GO**; Version 1 **NO GO**).

---

## Heatmap (summary)

| Heat | Meaning | Examples |
|---|---|---|
| **Green** | Mature within Level 3 ceiling | Architecture, Runtime A, Planning, Explainability, Governance, Knowledge Base, Product Board |
| **Amber** | Emerging | Recommendation, Readiness, Journey, Validation, Evidence, Documentation, Operational Readiness, Research |
| **Red** | Experimental / evidence focus | Personalisation, Learning Twin, Release Readiness, Educational Effectiveness, Commercial Readiness |

Full table: [`PRODUCT_MATURITY_MODEL.md`](PRODUCT_MATURITY_MODEL.md) §4.

---

## Scope reviewed

- Entire Product Board series P-003.1–P-003.5  
- Validation / delivery programmes EP-003.*–EP-007.*  
- Architecture baseline EP-002.9; Twin T7 assessment; flag defaults  
- `knowledge/VERSION_1_READINESS.md`; GA docs; GOVERNANCE hierarchy  
- Knowledge base, research (RIP + blind review), commercial tracker  
- Claim/evidence hierarchy P-003.5  

---

## Constraints (honoured)

- No runtime, services, UI, or API changes  
- No amendments to governance law, architecture baselines, release gates, decisions, risks, or assumptions  
- No commits required by this programme package itself  

---

## Quick start (board)

1. Open [`PRODUCT_MATURITY_MODEL.md`](PRODUCT_MATURITY_MODEL.md) §4 heatmap.  
2. Drill any cell in [`MATURITY_ASSESSMENT.md`](MATURITY_ASSESSMENT.md).  
3. Plan post–V1 focus with [`ROADMAP_IMPLICATIONS.md`](ROADMAP_IMPLICATIONS.md).  
4. Keep claims under [`../p003_5_evidence_hierarchy/`](../p003_5_evidence_hierarchy/) — Level 3 ≠ C-V1 / C-EDU.

Upstream companions:

- Dossier: [`../p003_1_version1_release_dossier/`](../p003_1_version1_release_dossier/)  
- Decisions / Risks / Assumptions / Evidence: `../p003_2_*` … `../p003_5_*`  
- Gates: [`../p002_1_version_1_release_framework/`](../p002_1_version_1_release_framework/)  

---

## Board control statement

> No major capability is Externally Validated or Operationally Mature as of 2026-07-26. Green means strongest **internal** organisational maturity. Version 1 production-ready remains **NO GO**. Red cells mark where additional evidence—not necessarily additional code—is required.
