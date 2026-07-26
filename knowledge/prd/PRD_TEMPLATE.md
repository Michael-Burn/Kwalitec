# PRD Template

**PRD ID:** PRD-NNN  
**Title:**  
**Status:** Draft | Review | Approved | Deferred | Rejected | Shipped  
**Author:**  
**Date:**  
**Owners:** Product / Engineering / Educational (as applicable)  

---

## 1. Problem Statement

What student or operational problem exists today?

What evidence shows it is real (feedback, metrics, support, dogfooding)?

---

## 2. Student Benefit

How does the student’s daily experience improve?

Which Vision design questions does this help answer?

1. What should I do now?  
2. How am I progressing?  
3. What is stopping me?  
4. What happens next?  

---

## 3. Educational Benefit

How does this improve learning (not activity)?

Which Educational Principles does it reinforce (consistency, feedback, reflection, revision, confidence, understanding mistakes)?

---

## 4. Vision Alignment

| Check | Answer |
|---|---|
| Final Test: helps students become better professionals? | Yes / No — explain |
| North Star: contributes to pass probability via better learning decisions? | |
| Violates Never Build list? | Yes / No |
| AI recommendations explainable / evidence-based? | Yes / No / N/A |
| Aligns with Explainability Standard (levels + schema)? | Yes / No / N/A — see P-001.2 |
| Aligns with Recommendation Quality Standard (principles + decision frame)? | Yes / No / N/A — see P-001.3 |
| Affects Version 1 production-ready gates (P-002.1 G1–G12)? | Yes / No / N/A — cite residual gates if claiming V1 progress |
| Links | Vision 2030 §… ; Blueprint §… |

If Final Test is No → **do not build**.

---

## 5. Architecture Impact

| Area | Impact | Notes |
|---|---|---|
| Educational OS (`src/`) | None / Read / Write | |
| Flask `app/` presentation | | |
| Digital Twin | **Forbidden unless explicit programme authority** | |
| EducationalStateService | **Forbidden unless explicit programme authority** | |
| Educational algorithms | **Forbidden unless explicit programme authority** | |
| One Runtime / Navigation / Educational State | | |
| Curriculum V1/V2 | | |
| Persistence / Alembic | | |
| New ADR required? | Yes / No | Link draft ADR |

---

## 6. Acceptance Criteria

List testable criteria. Prefer observable student or system outcomes.

- [ ] …
- [ ] …
- [ ] …

---

## 7. Metrics

| Metric | Baseline | Target | How measured |
|---|---|---|---|
| (from Vision success metrics where applicable) | | | |
| Estimated KSI contribution (ΔKSI; categories K1–K8) | | | See Product Success Framework |
| Explainability Review required? | Yes / No / N/A | | See P-001.2 checklist if student-facing intelligence |
| Recommendation Quality Review required? | Yes / No / N/A | | See P-001.3 checklist if student-facing recommendations |
| Version 1 gate impact (P-002.1)? | None / Cite G# | | See Version 1 Release Framework if claiming V1 readiness progress |

Activity vanity metrics are not sufficient on their own.

Reference: `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`.  
Explainability: `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`.  
Recommendation quality: `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md`.  
Version 1 production-ready gates: `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md`.

---

## 8. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| | | | |

Include privacy, educational honesty, performance, and dual-truth risks where relevant.

---

## 9. Definition of Done

This feature is Done when:

- [ ] Acceptance criteria met
- [ ] Engineering Standards PR checklist satisfied
- [ ] Tests green (list suites)
- [ ] Documentation updated
- [ ] Accessibility / security / performance gates met (or N/A)
- [ ] No unexplained recommendations introduced
- [ ] New technical debt recorded (or none)
- [ ] Product Language Guide respected for learner copy

---

## 10. Out of scope

Explicit non-goals for this PRD.

---

## 11. Dependencies / references

- Related PRDs / ADRs / issues
- Design mocks (if any)
- Analytics events (design reference only until analytics programme implements)

---

**Approval**

| Role | Name | Date | Decision |
|---|---|---|---|
| Product | | | |
| Architecture | | | |
| Educational governance (if required) | | | |
