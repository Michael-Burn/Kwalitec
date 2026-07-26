# Student Impact Assessment — EP-005.1

**Template:** `../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-005.1 |
| **Title** | KSI Validation & Evidence Collection |
| **Date** | 2026-07-26 |
| **Author** | Product measurement validation |
| **Student-visible change?** | No |
| **Production activation?** | None |
| **Related KSI categories** | K1–K8 (measurement of all; no score inflation) |

---

## 1. Student problem

**Student problem:**

> Students (and Product) cannot tell whether recent educational programmes actually made Kwalitec more useful for learning, because estimated ΔKSI from EP-003/EP-004 can be stacked optimistically while private-beta perception and KPI evidence remain thin. Without a validated assessment, Version 1 usefulness claims risk overstating benefit.

**Evidence:**

> Baseline KSI 58 (`BASELINE_KSI_ASSESSMENT.md`); programme estimated stacks ~+12 naive; EP-004 Week 0 external N=0; educational effectiveness NO-GO / PENDING EVIDENCE; P-002.1 requires validated KSI for Gate G1.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A | Measurement only — no guidance change |
| How am I progressing? | Indirect | Honest KSI status prevents false “ready” narratives |
| What is stopping me? | Indirect | Names residual gaps (explainability floor, gated personalisation) |
| What happens next? | Indirect | Clarifies evidence still required before V1 claims |

**Student benefit summary:**

> No direct daily-loop change. Benefit is **claim honesty**: students are not told Version 1 educational usefulness is achieved when validated KSI is 59.

**Final Test:** Does this help students become better professionals? **Indirectly Yes** — by blocking overclaim and focusing the roadmap on evidence-backed gaps (K8, perception re-test, cohort measurement).

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | Reinforces **honest confidence** about product readiness — not study mechanics |
| Risks rewarding activity vanity? | No — forbids vanity stacking of estimates |
| Educational Constitution / honesty risks? | Mitigated — prefers under-claim; preserves freeze |

**Learning benefit summary:**

> Protects learning trust by refusing to inflate usefulness scores without Tier A/B evidence.

---

## 4. Success metrics

| Metric | Baseline | Target | How measured | Owner |
|---|---|---|---|---|
| Validated KSI published | Estimated-only boards | Evidence-bound score + register | EP-005.1 artefacts | Product |
| Per-category confidence filed | Incomplete | K1–K8 High/Med/Low | `CONFIDENCE_ASSESSMENT.md` | Product |
| G1 status objective | Unknown / estimated | PASS/FAIL/HOLD with criteria | `VERSION_1_G1_STATUS.md` | Product |
| No KSI inflation | Risk of ~70 naive stack | Validated ≤ de-dup estimate | Reconciliation table | Product |

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Estimated delta | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | 0 | Docs/measurement only |
| Recommendation usefulness | K2 | 15 | 0 | Docs/measurement only |
| Readiness usefulness | K3 | 12 | 0 | Docs/measurement only |
| Personalisation | K4 | 12 | 0 | Docs/measurement only |
| Motivation | K5 | 10 | 0 | Docs/measurement only |
| Learning analytics | K6 | 10 | 0 | Docs/measurement only |
| Revision support | K7 | 12 | 0 | Docs/measurement only |
| Explainability | K8 | 14 | 0 | Docs/measurement only |

| Estimate | Value |
|---|---|
| **Net ΔKSI (points)** | **0** |
| **Confidence** | High |
| **Assumes production / flag state** | N/A — no behaviour change |

This programme **records** validated KSI = 59 (+1 vs baseline as an assessment outcome of prior work). That +1 is attributed to prior EP-003.1–.3 structural delivery under EP-005.1 validation rules — **not** to EP-005.1 itself.

---

## 6. Validation plan

| Method | When | Success signal | Failure signal |
|---|---|---|---|
| Evidence register completeness | This programme | Every validated score cites IDs | Orphan scores |
| Conservative reconciliation | This programme | Validated ≤ de-dup estimate; gated OFF → Δ0 | Inflated stack used as G1 |
| G1 board | This programme | Objective FAIL/PASS | Soft-pass on estimates |
| Future Tier B pack | Next programmes | Raises confidence / scores with evidence | Still Low perception |

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| Stakeholders treat validated 59 as “almost 80” | Medium | High | Premature trust | Explicit gap 21; G1 FAIL banner |
| Stakeholders reject validation as “too harsh” | Medium | Medium | Pressure to inflate | Cite methodology + PSF prefer-lower rule |
| Confusion between W-PROD and W-GATED | Medium | High | False personalisation claims | Dual claim windows |

---

## 8. Assumptions

1. Runtime A EP-003.1–.3 quality contracts are on the student-visible production path without a new OFF flag.  
2. `ENABLE_LEARNING_FEEDBACK` and `ENABLE_PERSONAL_LEARNING_PROFILE` remain default OFF.  
3. Blind-review corpus remains pre-change for perception.  
4. No open Sev-1 educational honesty incident exists in the claim window.

---

## 9. Evidence collected (exit)

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| Validation methodology | `VALIDATION_METHODOLOGY.md` | Process integrity |
| Evidence register | `KSI_EVIDENCE_REGISTER.md` | Traceability |
| Validated KSI report | `VALIDATED_KSI_REPORT.md` | KSI 59; reconciliation |
| Confidence assessment | `CONFIDENCE_ASSESSMENT.md` | Per-dimension confidence |
| G1 status | `VERSION_1_G1_STATUS.md` | Gate FAIL |
| Evidence package index | `../p002_1_version_1_release_framework/evidence/2026-07-26_ksi_validation/` | G1 package slice |

---

## 10. Lessons learned for student value (exit)

- Estimated stacked ΔKSI (~+12) **dramatically overstates** production-default usefulness once double-counting and flag-OFF rules apply.  
- Checklist Pass proves **structural eligibility**, not student-perceived Strong-band usefulness — especially for K8.  
- Personalisation programmes cannot move validated K4 while defaults are OFF.  
- Next student-value work must buy **Tier B evidence** (re-review + cohort), not more estimated ΔKSI slides.

---

## Appendix B — Completion-report checklist

- [x] Student Impact Assessment (sections 1–10)  
- [x] Estimated KSI contribution = 0  
- [x] Evidence collected  
- [x] Lessons learned for student value  
- [x] Explainability Review — **N/A** (no student-facing intelligence change)  
- [x] Recommendation Quality Review — **N/A** (no recommendation behaviour change)  
- [x] Version 1 readiness residual — G1 FAIL documented; G2–G12 not claimed  

---

**End of STUDENT_IMPACT_ASSESSMENT**
