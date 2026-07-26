# Release Decision Template — Version Approval Report

**Framework ID:** EVF-041  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Official educational approval artefact template  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## Instructions

Copy this template into:

`knowledge/educational_validation/release_reports/VAR_<version>_<YYYYMMDD>.md`

Fill every section. Do not delete outcome fields. Cite evidence paths. This document becomes the official educational approval artefact for the version.

---

```markdown
# Version Approval Report — <VERSION>

**Framework:** Educational Validation Framework (EVF)  
**Document type:** Official Educational Approval Artefact  
**Candidate version:**  
**Baseline ID / commit / review package:**  
**Report date:**  
**Educational Gate Owner:**  
**Validators / facilitators:**  
**EVF document versions:** Constitution 1.0 · Release Standard 1.0 · Gate 1.0  

---

## 1. Executive educational decision

| Field | Value |
|---|---|
| **Release Decision** | APPROVED \| CONDITIONAL APPROVAL \| REJECTED |
| **Overall Educational Trust** | __% |
| **Educational Recommendation** | (1–3 sentences) |
| **Claim freeze status** | Frozen / Partial release under holds / Lifted for approved claims |

---

## 2. Prerequisites

| Prerequisite | Status | Evidence path |
|---|---|---|
| EGI-001 Educational Constitution compliance | Pass / Fail | |
| EGI-003 Educational Governance Review APPROVED | Pass / Fail | |
| Blind Review subsystem intact (not mutated for this gate) | Pass / Fail | |
| Baseline frozen | Pass / Fail | |

Prerequisite failures → decision must be REJECTED (or halt before scoring).

---

## 3. Educational Capability Results (Layer 1)

| Capability | ID | Trust verdict | Report path |
|---|---|---|---|
| Master Planner | EC-01 | | |
| Daily Coach | EC-02 | | |
| Learning Coach | EC-03 | | |
| Recovery Coach | EC-04 | | |
| Revision Coach | EC-05 | | |
| Exam Coach | EC-06 | | |

**Capability Trust Index:** __ / 100

### Capability notes
-

---

## 4. Blind Comparative Results (Layer 2)

| Field | Value |
|---|---|
| Comparative mode | sealed_blind / corpus_mapped / mixed |
| Tasks covered | CT-01 … |
| Benchmarks used | BM-01 … |
| Report / mapping path | |

### Preference summary
| Task | Winner (unblinded) | Educational reasoning (short) |
|---|---|---|
| CT-01 | | |
| CT-02 | | |
| CT-03 | | |
| CT-04 | | |
| CT-05 | | |
| CT-06 | | |

**Comparative Preference Index:** __ / 100

---

## 5. Benchmark Comparison

| Benchmark | Relative strength vs Kwalitec | Notes |
|---|---|---|
| BM-01 Experienced IFoA Tutor | | |
| BM-02 Experienced Self-Study Student | | |
| BM-03 Commercial Planning Solution | | |

---

## 6. Educational Dimensions Summary (Layer 3)

| Dimension | Version synthesis (strengths / weaknesses) |
|---|---|
| ED-01 Educational Soundness | |
| ED-02 Exam Readiness | |
| ED-03 Practicality | |
| ED-04 Personalisation | |
| ED-05 Explainability | |
| ED-06 Motivation | |
| ED-07 Consistency | |
| ED-08 Confidence | |

**Dimension Quality Index:** __ / 100

---

## 7. Supporting Educational Evidence

| Evidence family | Path | Currency |
|---|---|---|
| Blind Review corpus / meta-analysis | | |
| Capability reviews | | |
| Comparative reports | | |
| Other educational evidence | | |

**Supporting Evidence Integrity:** __ / 100

---

## 8. Educational Strengths

1.  
2.  
3.  

---

## 9. Educational Weaknesses

1.  
2.  
3.  

---

## 10. Outstanding Risks

| Risk | Severity | Mitigation / hold |
|---|---|---|
| | | |

---

## 11. Overall Educational Trust (worksheet)

| Component | Weight | Score | Weighted |
|---|---:|---:|---:|
| Capability Trust Index | 40% | | |
| Comparative Preference Index | 25% | | |
| Dimension Quality Index | 25% | | |
| Supporting Evidence Integrity | 10% | | |
| **Overall Educational Trust** | 100% | — | **__%** |

Explain decisive factors:

-

---

## 12. Educational Recommendation

(Advise Product / Release: ship educationally, ship with holds, or do not release educationally.)

-

---

## 13. Release Decision

**Decision:** APPROVED / CONDITIONAL APPROVAL / REJECTED

### Holds (required if CONDITIONAL APPROVAL)

| Hold ID | Scope | Student-facing honesty | Expiry / re-validation trigger | Owner |
|---|---|---|---|---|
| H-01 | | | | |

### Forbidden claims under this decision

-

---

## 14. Sign-off

| Role | Name | Date | Signature / attestation |
|---|---|---|---|
| Educational Gate Owner | | | |
| Educational Validator lead | | | |
| Release Operator (acknowledged) | | | |

---

## 15. Appendix — Evidence index

-  
```

---

## Cross references

- `EDUCATIONAL_RELEASE_GATE.md`  
- `VERSION_APPROVAL_WORKFLOW.md`  
- `release_reports/README.md`  
