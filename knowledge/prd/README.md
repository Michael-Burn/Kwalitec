# Product Requirements Documents (PRD)

**Status:** Active  
**Authority:** Feature proposals (subordinate to Vision 2030 and Product Blueprint)  
**Governance:** `knowledge/GOVERNANCE.md` §4  

## Purpose

Every significant future feature requires a PRD before implementation.

PRDs ensure alignment with:

- [`PRODUCT_VISION_2030`](../product/vision/PRODUCT_VISION_2030.md)
- [`PRODUCT_BLUEPRINT`](../../PRODUCT_BLUEPRINT.md)
- Educational Constitution (when educational meaning is affected)

## Contents

| Document | Role |
|---|---|
| [`PRD_TEMPLATE.md`](PRD_TEMPLATE.md) | Mandatory template for new features |
| [`PRD-001_LEARNING_ANALYTICS_PHASE1.md`](PRD-001_LEARNING_ANALYTICS_PHASE1.md) | EP-001 WS2 — Phase 1 learning analytics events (**Approved** v1.1) |
| [`PRD_001_REVIEW.md`](PRD_001_REVIEW.md) | Mandatory design review — APPROVE WITH CHANGES |
| [`PRD_001_REVISION_SUMMARY.md`](PRD_001_REVISION_SUMMARY.md) | Revision actions vs review findings |
| `PRD-NNN-*.md` | Individual feature PRDs (create as needed) |

## Process

1. Copy the template to `PRD-NNN-short-slug.md` (increment NNN).
2. Complete every section — do not leave Vision Alignment empty.
3. Product + Architecture review per Governance.
4. Link the PRD from the implementation PR.

## Exceptions

Hotfixes, pure documentation, and pure chores with no behaviour change may use a short review note instead of a full PRD. When uncertain, write a PRD.
