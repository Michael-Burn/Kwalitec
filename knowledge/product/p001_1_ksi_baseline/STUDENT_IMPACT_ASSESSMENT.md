# P-001.1 — Student Impact Assessment

**Programme / Milestone ID:** P-001.1  
**Title:** KSI Baseline & Version 1 Success Framework  
**Date:** 2026-07-26  
**Author:** Product / Architecture Office (programme delivery)  
**Student-visible change?** No  
**Production activation?** None  
**Related KSI categories:** Framework defines K1–K8 (no runtime score change)

---

## 1. Student problem

Students and product teams lacked a permanent, shared definition of “educational usefulness” and a Version 1 usefulness bar. Prior evaluation (~58%) was not encoded as governing measurement law, so roadmap work could proceed without mandatory student-value accounting.

**Evidence:** Programme brief; EP-003/EP-004 measurement artefacts without a composite KSI; completion reports historically strong on architecture blast radius but inconsistent on student-value / KSI contribution.

---

## 2. Student benefit

No immediate student-visible change. Indirect benefit: future programmes must estimate and report KSI contribution, improving the odds that engineering effort closes the gap from KSI 58 → 80.

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A (governance) | Future work prioritised toward K1 planning usefulness |
| How am I progressing? | N/A | Framework measures K3/K6 progress usefulness |
| What is stopping me? | N/A | Baseline names blocking categories |
| What happens next? | N/A | Roadmap entry/exit gates require KSI estimates |

**Final Test:** Yes — establishing measurement that forces future work to serve professional learning improves long-run student outcomes even though this milestone ships no UI.

---

## 3. Learning benefit

Improves organisational learning about usefulness; does not change student learning algorithms. Risks of activity vanity are explicitly forbidden in the framework scoring rules.

---

## 4. Success metrics

| Metric | Baseline | Target | How measured | Owner |
|---|---|---|---|---|
| Framework published | Absent | Active | Docs present | Product |
| Governance mandate | Absent | Mandatory EP/P SIA + KSI | GOVERNANCE / 07-reporting | Product |
| Baseline KSI | Informal ~58% | Formal KSI = 58 | BASELINE_KSI_ASSESSMENT | Product |

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Estimated delta | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | 0 | Docs/governance only |
| Recommendation usefulness | K2 | 15 | 0 | Docs/governance only |
| Readiness usefulness | K3 | 12 | 0 | Docs/governance only |
| Personalisation | K4 | 12 | 0 | Docs/governance only |
| Motivation | K5 | 10 | 0 | Docs/governance only |
| Learning analytics | K6 | 10 | 0 | Docs/governance only |
| Revision support | K7 | 12 | 0 | Docs/governance only |
| Explainability | K8 | 14 | 0 | Docs/governance only |

| Estimate | Value |
|---|---|
| **Net ΔKSI (points)** | **0** |
| **Confidence** | High |
| **Assumes production / flag state** | N/A — no runtime change |

Governance enables future ΔKSI; it does not itself move student-perceived usefulness.

---

## 6. Validation plan

| Method | When | Success signal | Failure signal |
|---|---|---|---|
| Governance compliance check | Next EP/P completion | SIA + KSI sections present | Missing sections |
| Baseline citation | Roadmap planning | Priority order references K8/K2/K1/K3 | Feature work ignores baseline gaps |

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| Teams treat KSI as vanity composite | Medium | High | Mis-prioritisation | Evidence requirements; constitutions override greenwashing |
| Docs-only work claims ΔKSI > 0 | Low | Medium | False progress | Explicit ΔKSI = 0 rule for infra/docs |
| Second north star confusion | Medium | High | Philosophy drift | Framework states KSI serves Vision north star |

---

## 8. Assumptions

1. Prior ~58% evaluation remains a fair composite anchor until a filled cohort re-score.
2. EP/P programmes will obey the new completion-report mandate.
3. Weightings remain stable until an explicit amendment.

---

## 9. Evidence collected (exit)

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| Product Success Framework | `PRODUCT_SUCCESS_FRAMEWORK.md` | KSI defined; V1 ≥ 80 |
| Baseline assessment | `BASELINE_KSI_ASSESSMENT.md` | KSI = 58; priority order |
| SIA template | `STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` | Mandatory template |
| Governance updates | `knowledge/GOVERNANCE.md` §1, §2, §4.1; `.cursor/rules/07-reporting.mdc` | Mandate enforceable |

---

## 10. Lessons learned for student value

- Architectural completion reports already tracked blast radius; student-value accounting was the missing permanent gate.
- Blind-review corpus justifies elevating explainability and recommendation trust above feature expansion.
- Publishing ΔKSI = 0 for governance work is healthier than inventing usefulness gains.
