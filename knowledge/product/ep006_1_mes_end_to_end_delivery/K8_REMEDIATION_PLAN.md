# EP-006.1 — K8 Remediation Plan

**Programme:** EP-006.1 — MES End-to-End Delivery  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Prioritised remediation design (implementation deferred)  
**Validated baseline:** K8 **65** (EP-005.1); G1.5 **FAIL** (floor 70)  
**Constraint:** Presentation delivery only — no educational reasoning changes

---

## 1. Purpose

Convert the MES Delivery Audit into an ordered remediation backlog that clears the path to **validated K8 ≥ 70** (Gate G1.5), while preserving Runtime A service ownership and constitutional boundaries.

This plan **specialises** EP-005.2 REM-01 / REM-05 with field-level and layer-level work packages from [`MES_DELIVERY_SPECIFICATION.md`](MES_DELIVERY_SPECIFICATION.md).

---

## 2. Problem restatement

| Fact | Source |
|---|---|
| Services attach complete MES | EP-003.1–.3; Traceability §4 |
| Canonical Home renders ~4 fields, no evidence card | Traceability §5–§6 |
| `review_point` reaches **no** student surface | Traceability §7.4 |
| Coach re-narrates instead of passing through | `ExplanationService.from_opaque` |
| Validated K8 65 &lt; 70 | EP-005.1 G1.5 |
| Checklist Pass ≠ student-visible Pass | EP-005.2 RC-01 |

---

## 3. Scoring rubric

| Dimension | Scale |
|---|---|
| Est. validated K8 impact | H ≥ +4 cat / M +2–3 / L &lt; +2 (category points) |
| Effort | S / M / L (same as EP-005.2) |
| Evidence confidence | High / Medium / Low |
| Priority | Impact × confidence; then lower effort; constitutional safety gates |

---

## 4. Ranked remediation backlog

| Rank | ID | Issue | Est. K8 impact | Effort | Conf. | Also lifts | Notes |
|---|---|---|---|---|---|---|---|
| 1 | MES-01 | **Widen ExplanationSnapshot + JourneyContext** for next action, review_point, confidence, evidence, drivers slots | **H** (enabler) | S–M | High | K2, K1 | Prerequisite — no UI claim without this |
| 2 | MES-02 | **Pass-through authored MES** in bridge mapper + `ExplanationService` (stop reason-code rewrite when schema-complete) | **H** | M | High | K2, K8 trust | Fixes false Coach speech |
| 3 | MES-03 | **Wire `explanation_card` on Home** + L1 why/next always visible; L2 evidence ≤1 disclosure | **H** (+3–6 cat) | S–M | High | K2 | Closes REM-01 Home gap |
| 4 | MES-04 | **Relax Coach 3-sentence hard clip** when L2 disclosure exists | **M** | S | High | K8 | Clip allowed only with disclosure |
| 5 | MES-05 | **Restore readiness_drivers + review_point + why** on Home/Analytics schema path | **H** (+2–4 cat; also K3) | M | High | K3 | REM-05 |
| 6 | MES-06 | **Restore plan_drivers + review_point + evidence** on Mission / Journey | **M** (+1–3; also K1) | M | High | K1 | Planning branch of REM-01 |
| 7 | MES-07 | **Presentation contract tests** (VM + template smoke for M/D fields) | **L** (protects gains) | S | High | — | Quality gate |
| 8 | MES-08 | **Dual-home MES parity smoke** (same day’s Why/Evidence story) | **M** (P7) | S–M | High | K1, K8 | Until REM-02 consolidates homes |
| 9 | MES-09 | **Tier B perception pack** after MES-01…06 soak | **H** (claimability) | M | High | G1.5 | Does not change product alone |
| 10 | MES-10 | **Personalisation factor disclosure** when flag ON | **L** until activation | S | Med | K4 | Defer content activation to REM-08 |

### Explicit non-remediations

| Rejected | Why |
|---|---|
| Recalibrate readiness / ranking to “feel clearer” | Changes educational reasoning — out of scope |
| Opaque LLM Coach to raise trust | Conflicts with Vision / P9 |
| Declare G1.5 from estimate alone | P-002.1 / EP-005.1 forbid |
| Lower Dashboard MES to match Home | Wrong direction |
| New second educational runtime | Architecture constitution |

---

## 5. Phased execution

```
Phase 0 — Contract freeze (this programme)
  Delivery spec + traceability + this plan published
        ↓
Phase 1 — Data path (MES-01, MES-02, MES-07)
  DTOs + pass-through + contract tests
        ↓
Phase 2 — Default daily path (MES-03, MES-04, MES-08)
  Home L1/L2; clip policy; dual-home parity
        ↓
Phase 3 — Judgement unpackability (MES-05, MES-06)
  Readiness + planning drivers / review_point
        ↓
Phase 4 — Prove perception (MES-09)
  Tier B → validated KSI re-score targeting K8 ≥ 70
```

**Success thresholds**

| Milestone | Signal | Still not allowed |
|---|---|---|
| Phase 1 done | Schema-complete payload keys present on Home VM | Claiming K8 ≥ 70 |
| Phase 2 done | Dogfood: why + next visible without expand; evidence ≤1 click | Claiming G1.5 |
| Phase 3 done | Drivers + review_point unpackable on readiness/plan | Skipping Tier B |
| Phase 4 done | Validated K8 ≥ 70; opacity theme cleared or minority | Claiming full G1 without G1.1/G1.9 etc. |

---

## 6. Expected K8 / KSI contribution (forecast)

| Category | Current validated | Forecast after Phases 1–4 | Rationale |
|---|---:|---:|---|
| K8 Explainability | 65 | **70–75** | Visibility + consistency + unpackability |
| K2 Recommendation | 53 | **55–58** | Trust/speech without ranking change |
| K3 Readiness | 57 | **59–62** | Drivers / review (MES-05) |
| K1 Planning | 68 | **69–71** | Plan why/drivers inspectable |

| Estimate | Value |
|---|---|
| **Net ΔKSI (weighted, if validated)** | ≈ **+1.0 to +2.0** |
| **Confidence** | Medium (depends on Tier B) |
| **This programme ΔKSI** | **0** (design only) |
| **Assumes** | Production defaults; personalisation still OFF; no dual-home consolidation yet |

Illustrative K8 math: +5 category × 0.14 weight ≈ **+0.7** KSI — enough to clear G1.5 if validated, not enough alone for KSI ≥ 80.

---

## 7. Evidence prepared for post-change validation

| Evidence artefact | Status after EP-006.1 | Used by |
|---|---|---|
| Full omission inventory | **Ready** — Traceability §7 | MES-01…06 scope |
| Delivery contract (M/D/O) | **Ready** — Specification §3 | Acceptance tests |
| Dogfood checklist criteria | **Ready** — Specification §6.1 | Phase 2 exit |
| Tier B success/fail signals | **Ready** — Specification §6.2 | MES-09 / EP-005.2 REM-04 |
| Automated test intents | **Specified** — MES-07 | Successor PR |
| Baseline K8 / G1.5 | EP-005.1 package | Re-score comparison |
| Blind corpus (pre-change) | EP-004 SV-001–020 | Contrast after MES-09 |

Successor programmes must attach new evidence paths to a fresh validated KSI assessment — estimates above are **not** Gate G1 evidence.

---

## 8. Relationship to Version 1 gates

| Gate | Effect of this plan |
|---|---|
| G1.5 K8 ≥ 70 | **Critical path** — Phases 1–4 |
| G1.1 KSI ≥ 80 | Necessary but insufficient — still need REM-02/03/07/08 portfolio |
| G1.9 effectiveness | Not cleared by MES presentation alone |
| G2–G12 | Untouched |

---

## 9. Suggested successor programme title

**Educational Explainability Presentation (EP-006.2 or equivalent)** — implement MES-01…08 per this plan; schedule MES-09 with KSI re-validation.

Each successor must file SIA, estimated ΔKSI, and Explainability Review Checklist for changed surfaces.

---

## References

- [`MES_TRACEABILITY_REPORT.md`](MES_TRACEABILITY_REPORT.md)  
- [`MES_DELIVERY_SPECIFICATION.md`](MES_DELIVERY_SPECIFICATION.md)  
- `../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md`  
- `../ep005_1_ksi_validation_evidence/VERSION_1_G1_STATUS.md`  
- `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` (K8)  

---

**End of K8_REMEDIATION_PLAN**
