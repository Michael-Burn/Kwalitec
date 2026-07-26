# Risk Traceability

**Programme:** P-003.3 — Product Risk Register  
**Date:** 2026-07-26  
**Status:** Traceability map  
**Canonical cards:** [`PRODUCT_RISK_REGISTER.md`](PRODUCT_RISK_REGISTER.md)

Maps every `PR-NNN` to prior R IDs, decisions, programmes, and evidence paths. Unsupported mappings are omitted.

---

## A. Prior Risk_Summary (R1–R14) → PR map

| Prior ID | Risk_Summary title (short) | PR ID | Notes |
|---|---|---|---|
| R1 | Educational effectiveness unproven | PR-001 | |
| R2 | Validated KSI 62 &lt; 80 | PR-002 | |
| R3 | Privacy / Stage 1 blocked | PR-003 | |
| R4 | Premature V1 declaration | PR-004 | |
| R5 | Cold-start / sparse-evidence | PR-005 | |
| R6 | External evidence floors unmet | PR-006 | |
| R7 | Operational load / perf | PR-010 | |
| R8 | Telemetry overclaim | PR-011 | |
| R9 | Feature-flag / rollback unreadiness | PR-012 | G8 packaging companion → PR-013 |
| R10 | Confidence Medium ceiling | PR-008 | |
| R11 | Deployment vs declaration confusion | PR-014 | |
| R12 | Support / commercial unreadiness | PR-015 | |
| R13 | Independent KSI re-score G1.7 | PR-009 | |
| R14 | Personalisation marketed while OFF | PR-016 | |

**Dossier §8 note:** `Version_1_RELEASE_DOSSIER.md` §8 uses an older R1–R10 embedding that does not match `Risk_Summary.md` R1–R14. Authority for prior IDs = **Risk_Summary.md**. Drift tracked as **PR-021**.

---

## B. Evidence-backed companions (no prior R ID)

| PR ID | Title | Primary evidence |
|---|---|---|
| PR-007 | Stage 1/2 recruitment blocked on privacy | `BETA_COHORT.md`; `GO_NO_GO_DECISION.md` C1/C4 |
| PR-013 | Rollback drill / G8 packaging | `Release_Gates.md` G8 |
| PR-017 | Sparse onboarding / orientation | `FEEDBACK_REGISTER.md` FB-008 |
| PR-018 | Coach/Session naming & Twin trust | FB-001, FB-003 |
| PR-019 | Gate package incompleteness | `Release_Gates.md` |
| PR-020 | G2 EVF/constitutional | `Release_Gates.md` G2 |
| PR-021 | Documentation drift | Dossier §8 vs Risk_Summary; TD-ARCH-06 |
| PR-022 | Shadow constitution / bypass pressure | DR-023, DR-024 Risks fields |
| PR-023 | Security CSP / G10 residuals | `Release_Gates.md` G10; `VERSION_1_READINESS.md` |
| PR-024 | Pass-rate methodology undefined | `VERSION_1_READINESS.md`; DR-046 |
| PR-025 | Second educational brain creep | EP-003.4 / EP-004 RISK_ASSESSMENT |
| PR-026 | Process-local state loss | EP-004.1 R9 |

---

## C. Risk ↔ Decision map

| PR ID | Related Decisions |
|---|---|
| PR-001 | DR-021, DR-022, DR-033, DR-036, DR-041 |
| PR-002 | DR-025, DR-026, DR-027, DR-051, DR-041 |
| PR-003 | DR-034, DR-040 |
| PR-004 | DR-030, DR-031, DR-032, DR-041 |
| PR-005 | DR-004, DR-018, DR-035 |
| PR-006 | DR-022, DR-040 |
| PR-007 | DR-034, DR-040 |
| PR-008 | DR-027, DR-051 |
| PR-009 | DR-051, DR-030 |
| PR-010 | DR-030, DR-034 |
| PR-011 | DR-047 |
| PR-012 | DR-009, DR-010, DR-039, DR-043 |
| PR-013 | DR-009, DR-030 |
| PR-014 | DR-032, DR-041 |
| PR-015 | DR-034, DR-041 |
| PR-016 | DR-006, DR-009, DR-039, DR-043 |
| PR-017 | DR-007, DR-020 |
| PR-018 | DR-001, DR-004, DR-035 |
| PR-019 | DR-030, DR-031, DR-041 |
| PR-020 | DR-024, DR-045, DR-030 |
| PR-021 | DR-023 |
| PR-022 | DR-023, DR-024, DR-037 |
| PR-023 | DR-030 |
| PR-024 | DR-046, DR-021 |
| PR-025 | DR-001, DR-006, DR-015, DR-016, DR-038, DR-049 |
| PR-026 | DR-039, DR-006 |

Decision cards: [`../p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md`](../p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md)

---

## D. Risk ↔ Programme map

| Programme family | Risks |
|---|---|
| P-001.* | PR-002, PR-022, PR-024 (PSF / standards / north star) |
| P-002.1 | PR-004, PR-009, PR-012, PR-014, PR-019, PR-020 |
| P-003.1 | All R1–R14 mapped risks; PR-019; PR-021 |
| P-003.2 | Decision linkages (all PR with Related Decisions) |
| EP-003.* | PR-001, PR-005, PR-025; CR-004 |
| EP-004.* / private beta | PR-003, PR-006, PR-007, PR-015, PR-017, PR-018, PR-026; CR-001, CR-005 |
| EP-005.* | PR-002, PR-008, PR-016 |
| EP-006.* | PR-005, PR-008, PR-018 |
| EP-007.* | PR-001, PR-002, PR-006, PR-008, PR-009 |
| EP-002.* / architecture | PR-012, PR-013, PR-025; CR-003 |

---

## E. Gate ↔ Risk map (P-002.1 / P-003.1)

| Gate | Status (2026-07-26) | Primary risks |
|---|---|---|
| G1.1 KSI ≥ 80 | FAIL | PR-002 |
| G1.7 Independent re-score | HOLD | PR-009 |
| G1.9 Effectiveness not NO-GO | FAIL | PR-001, PR-006, PR-007, PR-003 |
| G2 Constitutional / EVF | IN PROGRESS | PR-020, PR-019 |
| G3 Explainability pack | Partially met | PR-019 (detail under dossier G3) |
| G4 Recommendation quality | Partially met | PR-019 |
| G5 Planning quality | Partially met | PR-019 |
| G6 Readiness quality | Partially met | PR-005, PR-019 |
| G7 Performance | IN PROGRESS | PR-010 |
| G8 Reliability | IN PROGRESS | PR-013 |
| G9 Telemetry | COMPLETE (flag OFF) | PR-011 |
| G10 Security | IN PROGRESS | PR-023, PR-003 |
| G12 Flag readiness | Not scored | PR-012, PR-016 |

---

## F. Brief example themes — evidence check

| Brief example | Register treatment | Evidence? |
|---|---|---|
| External cohort unavailable | PR-006 | Yes |
| Educational effectiveness not validated | PR-001 | Yes |
| Privacy review unsigned | PR-003 | Yes |
| Cold-start experience | PR-005 | Yes |
| Sparse onboarding content | PR-017 | Yes (FB-008) |
| External evidence confidence | PR-008 | Yes |
| Deployment rollback | PR-012, PR-013; CR-001 class | Yes |
| Feature flag misuse | PR-012, PR-016 | Yes |
| Release gate incompleteness | PR-019 (+ PR-020, G7/G8/G10/G12) | Yes |
| Beta recruitment failure | **Not registered as failure** — PR-007 = blocked HOLD | No failure event |
| Documentation drift | PR-021 | Yes |
| Governance drift | PR-022 = WATCH residual (DR forward risk), not observed incident | Partial |

---

## G. Closed risk traceability

| Closed ID | Evidence | Related open PR |
|---|---|---|
| CR-001 | `ep004_private_beta/ROOT_CAUSE_ANALYSIS.md` | PR-013, PR-025 |
| CR-002 | RC2 operational readiness (critical CSP fixed) | PR-023 |
| CR-003 | EP-002.9 exit certification | PR-012, PR-025 |
| CR-004 | EP-003.* RISK_ASSESSMENT Acceptable | PR-001, PR-002, PR-025 |
| CR-005 | EP-004.* RISK_ASSESSMENT mitigated OFF | PR-012, PR-016, PR-025, PR-026 |

---

## H. Primary evidence roots (read-only)

| Artefact | Path |
|---|---|
| Risk Summary | `knowledge/product/p003_1_version1_release_dossier/Risk_Summary.md` |
| Release Gates | `knowledge/product/p003_1_version1_release_dossier/Release_Gates.md` |
| Release Dossier | `knowledge/product/p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md` |
| Decision Register | `knowledge/product/p003_2_product_decision_register/` |
| Privacy Review | `knowledge/product/private_beta/PRIVACY_REVIEW.md` |
| Beta cohort | `knowledge/product/ep004_private_beta/BETA_COHORT.md` |
| Cohort evidence | `knowledge/product/ep007_3_educational_effectiveness_validation_stage1/COHORT_EVIDENCE_REGISTER.md` |
| G1.9 status | `knowledge/product/ep007_3_educational_effectiveness_validation_stage1/G1_9_STATUS.md` |
| Version 1 readiness | `knowledge/VERSION_1_READINESS.md` |
| Release Framework | `knowledge/product/p002_1_version_1_release_framework/` |
