# Assumption Traceability

**Programme:** P-003.4 — Product Assumption Register  
**Date:** 2026-07-26  
**Status:** Traceability map  
**Canonical cards:** [`PRODUCT_ASSUMPTION_REGISTER.md`](PRODUCT_ASSUMPTION_REGISTER.md)

Maps every `PA-NNN` to decisions, risks, programmes, and evidence. Unsupported mappings are omitted.

---

## A. Assumption ↔ Decision map

| PA ID | Related Decisions |
|---|---|
| PA-001 | DR-028, DR-019, DR-042 |
| PA-002 | DR-019, DR-005 |
| PA-003 | DR-026, DR-027, DR-042 |
| PA-004 | DR-017, DR-028 |
| PA-005 | DR-013, DR-028, DR-005 |
| PA-006 | DR-007, DR-020 |
| PA-007 | DR-007, DR-008, DR-020 |
| PA-008 | DR-008, DR-003 |
| PA-009 | DR-003, DR-007 |
| PA-010 | DR-007 |
| PA-011 | DR-006, DR-039 |
| PA-012 | DR-039, DR-043, DR-038 |
| PA-013 | DR-038, DR-047 |
| PA-014 | DR-002, DR-029, DR-036, DR-050 |
| PA-015 | DR-002, DR-029 |
| PA-016 | DR-050, DR-002, DR-029 |
| PA-017 | DR-004, DR-018 |
| PA-018 | DR-018, DR-035 |
| PA-019 | DR-004, DR-013 |
| PA-020 | DR-024, DR-035, DR-018 |
| PA-021 | DR-025, DR-051, DR-041 |
| PA-022 | DR-046, DR-021 |
| PA-023 | DR-026, DR-027 |
| PA-024 | DR-021, DR-033 |
| PA-025 | DR-033, DR-022 |
| PA-026 | DR-022, DR-040, DR-033 |
| PA-027 | DR-030, DR-031, DR-032, DR-041 |
| PA-028 | DR-013, DR-005 |
| PA-029 | DR-001, DR-002, DR-003, DR-004, DR-053 |
| PA-030 | DR-009, DR-010, DR-016 |
| PA-031 | DR-020, DR-007, DR-001 |
| PA-032 | DR-011, DR-012 |
| PA-033 | DR-043, DR-009, DR-039 |
| PA-034 | DR-005, DR-019 |
| PA-035 | DR-027 |
| PA-036 | DR-042, DR-051, DR-027 |
| PA-037 | DR-003, DR-008, DR-007 |
| PA-038 | DR-004, DR-018 |
| PA-039 | DR-033, DR-022 |
| PA-040 | DR-034, DR-040, DR-041 |
| PA-041 | DR-007, DR-004, DR-018 |
| PA-042 | DR-020, DR-001, DR-009 |

Decision cards: [`../p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md`](../p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md)

---

## B. Assumption ↔ Risk map

| PA ID | Related Risks |
|---|---|
| PA-001 | PR-018 |
| PA-002 | PR-011, PR-018 |
| PA-003 | PR-002, PR-008 |
| PA-004 | PR-018, PR-025 |
| PA-005 | PR-025 |
| PA-006 | PR-017 |
| PA-007 | PR-017, PR-021 |
| PA-008 | PR-005 |
| PA-009 | PR-002 |
| PA-010 | PR-017 |
| PA-011 | PR-016, PR-012 |
| PA-012 | PR-012, PR-016 |
| PA-013 | PR-011 |
| PA-014 | PR-001, PR-024 |
| PA-015 | PR-018 |
| PA-016 | PR-017 |
| PA-017 | PR-005 |
| PA-018 | PR-005 |
| PA-019 | PR-005, PR-025 |
| PA-020 | PR-005, PR-020 |
| PA-021 | PR-002 |
| PA-022 | PR-024 |
| PA-023 | PR-002, PR-008 |
| PA-024 | PR-001 |
| PA-025 | PR-001, PR-006 |
| PA-026 | PR-001, PR-003, PR-006, PR-007 |
| PA-027 | PR-004, PR-014 |
| PA-028 | PR-025 |
| PA-029 | PR-025, PR-012 |
| PA-030 | PR-012, PR-016 |
| PA-031 | PR-016, PR-025 |
| PA-032 | — (architecture invariant; no dedicated PR) |
| PA-033 | PR-012, PR-013 |
| PA-034 | PR-025 |
| PA-035 | PR-008 |
| PA-036 | PR-002, PR-008, PR-009 |
| PA-037 | PR-005, PR-017 |
| PA-038 | PR-005 |
| PA-039 | PR-001 |
| PA-040 | PR-003, PR-006, PR-007, PR-015 |
| PA-041 | PR-017 |
| PA-042 | PR-016, PR-025 |

Risk cards: [`../p003_3_product_risk_register/PRODUCT_RISK_REGISTER.md`](../p003_3_product_risk_register/PRODUCT_RISK_REGISTER.md)

---

## C. Assumption ↔ Programme map

| Programme family | Assumptions |
|---|---|
| P-001.1 (PSF / KSI) | PA-011, PA-021, PA-022, PA-037, PA-038 |
| P-001.2 (Explainability) | PA-001, PA-003, PA-005, PA-034 |
| P-001.3 (Recommendation quality) | PA-014, PA-015, PA-016 |
| P-002.1 (Release Framework) | PA-021, PA-026, PA-027, PA-032, PA-033 |
| P-003.1 (Release Dossier) | PA-020, PA-021, PA-026, PA-027, PA-029, PA-040 |
| P-003.2 (Decision Register) | Cross-links via Related Decisions (all PA) |
| P-003.3 (Risk Register) | Cross-links via Related Risks |
| EP-003.1 | PA-014, PA-015, PA-016 |
| EP-003.2 | PA-017, PA-018, PA-038, PA-041 |
| EP-003.3 | PA-008, PA-037 |
| EP-003.4 | PA-013 |
| EP-004.* / private beta | PA-004, PA-011, PA-012, PA-026, PA-033, PA-035, PA-040 |
| EP-005.1 | PA-003, PA-023, PA-024, PA-035, PA-036 |
| EP-005.2 | PA-002, PA-004, PA-006, PA-008, PA-012, PA-015, PA-018, PA-024, PA-027 |
| EP-006.1–006.2 | PA-002, PA-005, PA-019, PA-034 |
| EP-006.3 | PA-001, PA-003, PA-004, PA-006 |
| EP-006.4–006.5 | PA-017, PA-018, PA-020, PA-038, PA-041 |
| EP-007.1 | PA-007, PA-008, PA-010, PA-031, PA-041 |
| EP-007.2 | PA-007, PA-009, PA-036, PA-037 |
| EP-007.3 | PA-014, PA-025, PA-026, PA-039 |
| EP-002.9 / architecture | PA-028, PA-029, PA-030, PA-031, PA-032, PA-034, PA-042 |

---

## D. Brief example themes → PA map

| Brief example theme | Primary PA | Status |
|---|---|---|
| Better explanations improve trust | PA-001 | Supported |
| Canonical Home reduces cognitive load | PA-006 (problem), PA-007 (remedy) | Validated / Supported |
| Personalisation improves educational usefulness | PA-011 | Hypothesis |
| Runtime A recommendations improve study behaviour | PA-014 | Hypothesis |
| External validation required for educational effectiveness | PA-026 | Validated |
| Students understand readiness confidence | PA-017 | Supported |
| KSI is a useful release metric | PA-021 (bar), PA-022 (scope) | Validated |

---

## E. Primary evidence paths (by theme)

| Theme | Primary paths |
|---|---|
| Explainability / MES | `p001_2_explainability_standard/`; `ep005_2_*/KSI_GAP_ANALYSIS.md`; `ep006_3_*/MES_PERCEPTION_REPORT.md` |
| Journey / Home | `ep005_2_*`; `ep007_1_*/STUDENT_JOURNEY_CONSOLIDATION.md`; `ep007_2_*/JOURNEY_PERCEPTION_REPORT.md` |
| Personalisation | `ep004_*/`; `ep005_1_*/VALIDATED_KSI_REPORT.md`; DR-006/039 |
| Effectiveness | `ep007_3_*/EDUCATIONAL_EFFECTIVENESS_REPORT.md`; `G1_9_STATUS.md`; `COHORT_EVIDENCE_REGISTER.md` |
| KSI / release | `p001_1_*/PRODUCT_SUCCESS_FRAMEWORK.md`; `p002_1_*/`; `p003_1_*/Release_Gates.md` |
| Architecture | `ep002_9_*/AUTHORITATIVE_ARCHITECTURE_BASELINE.md`; P-003.2 DR-001–DR-020 |
| Decisions / risks | `p003_2_*/PRODUCT_DECISION_REGISTER.md`; `p003_3_*/PRODUCT_RISK_REGISTER.md` |

---

## F. Status × register role

| Status | Board use | Companion index |
|---|---|---|
| Validated | Treat as known within claim window | [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) |
| Supported / Hypothesis | Believe carefully; require evidence plan | [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md) |
| Rejected / Superseded | Do not claim; remember history | [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md) |

---

**End of Assumption Traceability**
