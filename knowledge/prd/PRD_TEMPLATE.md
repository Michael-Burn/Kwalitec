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

Activity vanity metrics are not sufficient on their own.

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
