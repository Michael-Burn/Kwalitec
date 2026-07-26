# EP-005.1 — KSI Validation & Evidence Collection

**Programme ID:** EP-005.1  
**Parent programme:** EP-005 — Version 1 Educational Usefulness Validation  
**Status:** COMPLETE (documentation & evidence governance)  
**Started:** 2026-07-26  
**Completed:** 2026-07-26  
**Authority:** Product measurement validation (subordinate to Vision 2030; executes Product Success Framework + Version 1 Release Framework Gate G1)  
**Constraints:** Documentation and evidence only — no runtime, UI, or API changes  

---

## Mission

Validate the **estimated** KSI improvements claimed by EP-003.1–EP-003.4 and EP-004.1–EP-004.3 using objective, traceable evidence under the Product Success Framework, producing a defensible Version 1 educational usefulness assessment for Gate **G1**.

---

## Deliverables

| Artefact | Path | Role |
|---|---|---|
| Validation Methodology | [`VALIDATION_METHODOLOGY.md`](VALIDATION_METHODOLOGY.md) | Cohort, period, sources, confidence, thresholds, insufficient-evidence rules |
| Validated KSI Report | [`VALIDATED_KSI_REPORT.md`](VALIDATED_KSI_REPORT.md) | Evidence-bound re-score; estimated vs validated reconciliation |
| Evidence Register | [`KSI_EVIDENCE_REGISTER.md`](KSI_EVIDENCE_REGISTER.md) | Traceable evidence IDs → claims |
| Confidence Assessment | [`CONFIDENCE_ASSESSMENT.md`](CONFIDENCE_ASSESSMENT.md) | Per-category and composite confidence |
| Version 1 G1 Status | [`VERSION_1_G1_STATUS.md`](VERSION_1_G1_STATUS.md) | Gate G1 PASS / FAIL / HOLD / DEFER |
| Student Impact Assessment | [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Programme SIA (ΔKSI = 0 — measurement only) |
| Programme Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Exit record |

---

## Headline outcomes (non-marketing)

| Measure | Value |
|---|---|
| Baseline KSI (P-001.1) | **58** |
| Naive stacked estimated ΔKSI (EP-003.1–004.3) | **≈ +12** (double-count risk — not claimable) |
| De-duplicated estimated KSI (production defaults) | **≈ 60** |
| **Validated KSI (production defaults)** | **59** |
| Version 1 target | **≥ 80** |
| Gate G1 | **FAIL** — validated KSI &lt; 80; K8 &lt; 70; student-perception evidence insufficient for Strong-band claims |

---

## Governing references

| Authority | Path |
|---|---|
| Product Success Framework | `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` |
| Baseline KSI | `../p001_1_ksi_baseline/BASELINE_KSI_ASSESSMENT.md` |
| Version 1 Release Framework | `../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` |
| Evidence Requirements | `../p002_1_version_1_release_framework/VERSION_1_EVIDENCE_REQUIREMENTS.md` |
| EP-003 / EP-004 programmes | `../ep003_*`, `../ep004_*` |
| Private beta Go / No-Go | `../ep004_private_beta/GO_NO_GO_DECISION.md` |

---

## Quality gates (this programme)

| Gate | Rule |
|---|---|
| Runtime | No application behaviour changes |
| UI | No template / frontend changes |
| API | No route or contract changes |
| Inflate KSI | Forbidden — prefer lower score on conflict |
| Constitutions | Preserve Vision 2030, Educational Constitution, Architecture Constitution, PSF, P-002.1 |

---

**End of README**
