# P-002.1 — Version 1 Release Framework

**Programme ID:** P-002.1  
**Parent programme:** P-002 — Version 1 Release Governance  
**Status:** COMPLETE (documentation & governance)  
**Started:** 2026-07-26  
**Authority:** Product release-readiness law (subordinate to Vision 2030; complementary to KSI / Explainability / Recommendation Quality standards; does not replace EVF Educational Release Gate)  
**Constraints:** Documentation and governance only — no runtime, UI, or API changes  

---

## Mission

Define the permanent, measurable governance framework that decides **when Kwalitec Version 1 may be declared production-ready**.

Version 1 must not ship on estimated KSI alone. Release requires objective educational, architectural, and operational gates with a validated evidence package and an explicit go / no-go decision.

---

## Deliverables

| Artefact | Path | Role |
|---|---|---|
| Version 1 Release Framework | [`VERSION_1_RELEASE_FRAMEWORK.md`](VERSION_1_RELEASE_FRAMEWORK.md) | Permanent gate law — twelve gate families, validation process, sign-off |
| Acceptance Checklist | [`VERSION_1_ACCEPTANCE_CHECKLIST.md`](VERSION_1_ACCEPTANCE_CHECKLIST.md) | Gate-by-gate acceptance criteria |
| Go / No-Go Guide | [`VERSION_1_GO_NO_GO_GUIDE.md`](VERSION_1_GO_NO_GO_GUIDE.md) | Decision outcomes, holds, claim language |
| Evidence Requirements | [`VERSION_1_EVIDENCE_REQUIREMENTS.md`](VERSION_1_EVIDENCE_REQUIREMENTS.md) | Evidence package contents and freshness |
| Student Impact Assessment | [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Programme SIA (ΔKSI = 0) |
| Programme Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Exit record for P-002.1 |

---

## Governing references

| Authority | Path |
|---|---|
| Product Vision 2030 (Product Constitution) | `knowledge/product/vision/PRODUCT_VISION_2030.md` |
| Product Success Framework (KSI) | `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` |
| Explainability Standard | `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` |
| Recommendation Quality Standard | `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md` |
| Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| Educational Release Gate (EVF) | `knowledge/educational_validation/EDUCATIONAL_RELEASE_GATE.md` |
| Architecture Constitution | `docs/ARCHITECTURE_CONSTITUTION.md` |
| Governance hierarchy | `knowledge/GOVERNANCE.md` |
| Release Playbook | `knowledge/RELEASE_PLAYBOOK.md` |
| Version 1 Readiness tracker | `knowledge/VERSION_1_READINESS.md` |
| Planning quality contract | `knowledge/architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md` |
| Readiness quality contract | `knowledge/architecture/READINESS_SERVICE_QUALITY_CONTRACT.md` |

---

## Quality gates (this programme)

| Gate | Rule |
|---|---|
| Runtime | No application behaviour changes |
| UI | No template / frontend changes |
| API | No route or contract changes |
| Twin / Educational State | Untouched |
| Philosophy | Does not replace Vision north star, Final Test, or EVF educational release trust law |
| Conflict rule | If this framework conflicts with Product Constitution → **STOP**; amend higher authority first |

---

## Exit criteria

| Criterion | Status |
|---|---|
| Version 1 release gates objectively defined | COMPLETE |
| Validation process documented | COMPLETE |
| Acceptance checklist, Go/No-Go guide, evidence requirements published | COMPLETE |
| Governance integrated (PSF, GOVERNANCE, reporting) | COMPLETE |
| No constitutional conflicts with Vision 2030 | COMPLETE |
