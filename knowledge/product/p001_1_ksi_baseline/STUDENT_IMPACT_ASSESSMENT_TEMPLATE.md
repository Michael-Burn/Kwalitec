# Student Impact Assessment Template

**Programme:** P-001.1 — KSI Baseline & Version 1 Success Framework  
**Version:** 1.0  
**Status:** Mandatory template for future EP / P programme completion  
**Effective:** 2026-07-26  
**Canonical path:** `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`  

---

## How to use

1. Copy this template into the programme folder as `STUDENT_IMPACT_ASSESSMENT.md` (or embed equivalent sections in the programme completion report with a link here).
2. Complete **all** sections. Use `N/A — rationale` only where a section genuinely does not apply (e.g. pure docs/governance with zero student-visible change).
3. Estimate KSI contribution using category IDs **K1–K8** from [`PRODUCT_SUCCESS_FRAMEWORK.md`](PRODUCT_SUCCESS_FRAMEWORK.md).
4. Prefer under-claiming. Do not invent cohort outcomes.
5. Architectural blast-radius notes (who sees what under which flags) may be added as an appendix; they do **not** replace the student-value sections below.

**Authority:** Required by `knowledge/GOVERNANCE.md` and `.cursor/rules/07-reporting.mdc` for every future EP/P programme completion report.

---

## Document header (fill)

| Field | Value |
|---|---|
| **Programme / Milestone ID** | |
| **Title** | |
| **Date** | |
| **Author** | |
| **Student-visible change?** | Yes / No / Gated (describe) |
| **Production activation?** | None / Gated / Yes |
| **Related KSI categories** | K1–K8 (list) |

---

## 1. Student problem

What student problem exists today?

- State the problem in student language (not engineering language).
- Cite evidence (blind reviews, interviews, support, scorecards, dogfood, prior SIA).
- If no student problem (infra-only), say so explicitly and skip benefit inflation.

**Student problem:**

>

**Evidence:**

>

---

## 2. Student benefit

How does the student’s daily experience improve if this work succeeds?

Map to Vision design questions where relevant:

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes / No / N/A | |
| How am I progressing? | Yes / No / N/A | |
| What is stopping me? | Yes / No / N/A | |
| What happens next? | Yes / No / N/A | |

**Student benefit summary:**

>

**Final Test:** Does this help students become better professionals? **Yes / No** — explain.

---

## 3. Learning benefit

How does this improve **learning** (not activity)?

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | |
| Risks rewarding activity vanity? | Yes / No — mitigate |
| Educational Constitution / honesty risks? | |

**Learning benefit summary:**

>

---

## 4. Success metrics

| Metric | Baseline | Target | How measured | Owner |
|---|---|---|---|---|
| | | | | |

Prefer EP-003 Educational Metrics (M1–M9), Vision success metrics, or interview codes. Activity vanity metrics alone are insufficient.

---

## 5. Estimated KSI contribution

Use weights and category definitions from the Product Success Framework.

| Category | ID | Weight | Estimated delta (points on 0–100 category scale) | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | | |
| Recommendation usefulness | K2 | 15 | | |
| Readiness usefulness | K3 | 12 | | |
| Personalisation | K4 | 12 | | |
| Motivation | K5 | 10 | | |
| Learning analytics | K6 | 10 | | |
| Revision support | K7 | 12 | | |
| Explainability | K8 | 14 | | |

**Net estimated KSI contribution** (weighted):

\[
\Delta \mathrm{KSI} \approx \sum_i \frac{w_i}{100} \times \Delta s_i
\]

| Estimate | Value |
|---|---|
| **Net ΔKSI (points)** | |
| **Confidence** | High / Medium / Low |
| **Assumes production / flag state** | |

Rules:

- Infra-only / docs-only programmes may record **ΔKSI = 0** with rationale.
- Do not claim category gains without a validation plan (§6).
- Negative deltas are allowed and must be disclosed (regressions).

---

## 6. Validation plan

How will the estimated benefit be confirmed or falsified?

| Method | When | Success signal | Failure signal |
|---|---|---|---|
| | | | |

Include at least one of: interview / blind-review theme, KPI movement, dogfood checklist, support-theme watch — unless ΔKSI = 0.

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| | | | | |

Always consider: educational honesty, dual messaging, false confidence, overwhelm, privacy, accessibility.

---

## 8. Assumptions

List assumptions that, if false, invalidate the student benefit or KSI estimate.

1.
2.
3.

---

## 9. Evidence collected (exit)

Fill at programme completion (may be empty at programme start).

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| | | |

---

## 10. Lessons learned for student value (exit)

What did this programme teach about educational usefulness?

- What improved student value?
- What failed to move perceived usefulness?
- What should the next programme measure differently?

>

---

## Appendix A — Optional blast-radius table

Use when flags / cohorts bound visibility (common for architecture cutovers).

| Cohort / flag state | Student-visible change |
|---|---|
| Production defaults | |
| Non-prod gated | |

---

## Appendix B — Completion-report checklist

Programme completion reports must include or link:

- [ ] This Student Impact Assessment (sections 1–8 at start; 9–10 at exit)
- [ ] Estimated KSI contribution (§5)
- [ ] Evidence collected (§9)
- [ ] Lessons learned for student value (§10)
- [ ] Explainability Review when in scope (P-001.2; else N/A)
- [ ] Recommendation Quality Review when in scope (P-001.3; else N/A)
- [ ] Version 1 readiness residual gates when claiming V1 production-ready progress (P-002.1; else N/A)

**Version 1 declaration:** Declaring Version 1 production-ready is **not** a normal programme completion step. It requires the full P-002.1 evidence package and go / no-go board (`knowledge/product/p002_1_version_1_release_framework/`).

---

**End of template**
