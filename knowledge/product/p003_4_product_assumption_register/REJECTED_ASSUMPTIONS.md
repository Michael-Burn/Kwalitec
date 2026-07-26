# Rejected and Superseded Assumptions

**Programme:** P-003.4 — Product Assumption Register  
**Date:** 2026-07-26  
**Status:** REJECTED / SUPERSEDED index  
**Canonical cards:** [`PRODUCT_ASSUMPTION_REGISTER.md`](PRODUCT_ASSUMPTION_REGISTER.md)

This index lists assumptions that are **disproved**, **explicitly unsupported as claims**, or **historically replaced**. Product Board must not revive these as release, marketing, or scoring shortcuts.

**Board question answered here:** *What has been disproved (or retired)?*

---

## Board reading order (10 minutes)

1. **Release / scoring shortcuts:** PA-023 → PA-024 → PA-025 → PA-027  
2. **False remediations:** PA-003 → PA-005 → PA-012 → PA-015 → PA-019 → PA-009  
3. **Superseded misconceptions:** PA-041 → PA-042  

---

## A. Rejected — falsified or forbidden as claims

| ID | Title | Category | Why rejected | Key evidence |
|---|---|---|---|---|
| [PA-003](PRODUCT_ASSUMPTION_REGISTER.md#pa-003--checklist-pass-alone-raises-validated-k8--70) | Checklist Pass alone → K8 ≥ 70 | Governance | Scoring law forbids | EP-006.3 unsupported log; EP-005.1 methodology |
| [PA-005](PRODUCT_ASSUMPTION_REGISTER.md#pa-005--opaque-llm-coach-copy-raises-explainability-and-trust) | Opaque LLM Coach raises trust | Educational | Conflicts with P9 / Constitution | EP-006.1; P-001.2 P9 |
| [PA-009](PRODUCT_ASSUMPTION_REGISTER.md#pa-009--journey-consolidation-alone-improves-planning-topic-selection-quality) | Journey consolidation improves topic selection | Product | Not measured; unchanged | EP-007.2 unsupported log |
| [PA-012](PRODUCT_ASSUMPTION_REGISTER.md#pa-012--turning-personalisationfeedback-flags-on-immediately-raises-validated-ksi) | Flip personalisation flags ON now | Operational | Honesty / G12 risk | EP-005.2 §6 |
| [PA-015](PRODUCT_ASSUMPTION_REGISTER.md#pa-015--recommendation-ranking-quality-is-the-primary-k2-gap) | Ranking quality is primary K2 gap | Product | Inspectability is primary | EP-005.2; EP-003.1 Pass |
| [PA-019](PRODUCT_ASSUMPTION_REGISTER.md#pa-019--recalibrating-readiness-weights-to-feel-clearer-fixes-unpackability) | Recalibrate readiness weights for clarity | Educational | Changes educational reasoning | EP-006.1 non-remediation |
| [PA-023](PRODUCT_ASSUMPTION_REGISTER.md#pa-023--estimated-programme-ksi-can-be-summed-to-infer-validated-ksi) | Naive ΔKSI stacking → claimable KSI | Governance | Falsified | EP-005.1 Validated KSI Report; DR-026 |
| [PA-024](PRODUCT_ASSUMPTION_REGISTER.md#pa-024--structural--quality-contract-pass-equals-validated-student-educational-value) | Tier A Pass = student educational value | Research | Capability ≠ value | EP-005.1/005.2; DR-021 |
| [PA-025](PRODUCT_ASSUMPTION_REGISTER.md#pa-025--perception-validation-confirms-educational-effectiveness-g19) | Perception Pass → G1.9 / effectiveness | Research | Perception ≠ effectiveness | DR-033; EP-007.3 G1.9 FAIL |
| [PA-027](PRODUCT_ASSUMPTION_REGISTER.md#pa-027--operational-ga--architecture-cutover-implies-version-1-educational-readiness) | GA / cutover ⇒ V1 ready | Release | Three separable verdicts | P-002.1; DR-030–032; DR-041 |

**Count:** 10

---

## B. Superseded — replaced by later knowledge

| ID | Title | Category | Superseded by | Notes |
|---|---|---|---|---|
| [PA-041](PRODUCT_ASSUMPTION_REGISTER.md#pa-041--dashboard--analytics-is-the-primary-readiness-surface-for-student-value) | Dashboard/Analytics is primary readiness surface | Product | PA-017, PA-038, DR-007 | Home-centric W-PROD sole-runtime path |
| [PA-042](PRODUCT_ASSUMPTION_REGISTER.md#pa-042--sole-runtime-means-twin-educational-cutover-is-live) | Sole runtime = Twin cutover live | Architecture | PA-031, DR-020 | Chrome/journey ≠ educational authority |

**Count:** 2

---

## Combined rejected / superseded total

| Set | Count |
|---|---:|
| Rejected | 10 |
| Superseded | 2 |
| **Total** | **12** |

---

## Anti-patterns these cards block

- Declaring Version 1 ready from GA, perception, or estimate stacks  
- Marketing personalisation / Twin while flags OFF, or flipping flags without G12  
- Treating LLM opacity or weight tweaks as explainability fixes  
- Claiming journey work improved PlanningService topic quality without measurement  
- Substituting checklist Pass for validated K8  

Known / believed: [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) · [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md)
