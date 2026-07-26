# Exit Traceability

**Programme:** P-003.8 — Version 1 Exit Criteria  
**Version:** 1.0  
**Status:** Active — synthesis map  
**Effective:** 2026-07-26  
**Does not:** Amend decisions, risks, gates, or evidence classifications  

---

## Chain (normative reading order)

```
Criterion (XC-*)
        ↓
Evidence (paths / packs already on file or labelled unavailable)
        ↓
Decision (DR-*)
        ↓
Risk (PR-*)
        ↓
Gate (G1–G12)
        ↓
Board Recommendation (GO | CONDITIONAL GO | NO GO | DEFER)
```

---

## Master map

| Criterion | Evidence (primary) | Decisions | Risks | Gate | Feeds recommendation |
|---|---|---|---|---|---|
| **XC-G1** | EP-007.2 `K1_REVALIDATION.md`; EP-007.3 `G1_9_STATUS.md`; EP-006.3 `G1_5_STATUS.md`; EP-005.1 `VALIDATED_KSI_REPORT.md`; G1 slice `p002_1_…/evidence/2026-07-26_ksi_validation/` | DR-025, DR-026, DR-027, DR-022, DR-033, DR-042, DR-051, DR-031, DR-041 | PR-001, PR-002, PR-006, PR-008, PR-009 | **G1** | **FAIL → NO GO** |
| **XC-G2** | `VERSION_1_READINESS` Architecture COMPLETE; constitutions; EVF gate; full memo **Evidence currently unavailable** | DR-023, DR-024, DR-044, DR-001, DR-011, DR-037, DR-045 | PR-020, PR-022, PR-025 | **G2** | Incomplete / not APPROVED → blocks GO |
| **XC-G3** | EP-003.1–.3 Explainability Review Pass; MES delivery EP-006.2; G1.5 PASS; G3.4 pack incomplete | DR-028, DR-019, DR-042, DR-052 | PR-005 | **G3** | Partially met → not PASS |
| **XC-G4** | EP-003.1 Recommendation Review Pass; K2 55; scorecard gaps; freeze active | DR-029, DR-036, DR-002, DR-050 | PR-001, PR-016 | **G4** | Partially met → not PASS |
| **XC-G5** | EP-003.3 planning tests; EP-007.1 consolidation; K1 72; G5.3 pack incomplete | DR-003, DR-007, DR-008, DR-017, DR-052 | (W-PROD residual cleared; dual-run outside window noted in dossier) | **G5** | Partially met → not PASS |
| **XC-G6** | EP-003.2 / EP-006.4 / EP-006.5; K3 65; Exam Ready ban | DR-004, DR-018, DR-035, DR-052 | PR-005 | **G6** | Partially met → not PASS |
| **XC-G7** | CI perf benchmarks green; production load **NOT STARTED** | DR-030 | PR-010 | **G7** | IN PROGRESS / HOLD path |
| **XC-G8** | Health/smoke; rollback drill packaging incomplete | DR-048 | PR-013 | **G8** | IN PROGRESS / HOLD path |
| **XC-G9** | Analytics EP-002 ops ready; Journey emit deferred | DR-047, DR-043 | PR-011 | **G9** | COMPLETE (flag OFF) if claims honest |
| **XC-G10** | GA `SECURITY_REVIEW.md`; privacy signatures open for Stage 1 | DR-034 | PR-003, PR-007, PR-023 | **G10** | IN PROGRESS |
| **XC-G11** | Broad pytest/GA/quality-contract suites; RC continuous green required | DR-011, DR-052 | PR-019 | **G11** | IN PROGRESS |
| **XC-G12** | Flag defaults OFF; published V1 matrix **Evidence currently unavailable** | DR-009, DR-039, DR-038, DR-043, DR-010 | PR-012, PR-016 | **G12** | Not scored |
| **XC-PKG** | G1 slice only; full `…_v1_declaration/` package absent | DR-030, DR-041 | PR-019, PR-021 | G1–G12 process | Incomplete → blocks GO (DEFER at best if no FAIL; here FAIL already present) |
| **XC-REC** | Dossier §11; DR-041 posture; no GO decision record | DR-032, DR-041, DR-031, DR-040 | PR-004, PR-014 | Consumes all | **NO GO** |

---

## Criterion → Board recommendation (current)

```
XC-G1 FAIL ──┐
XC-PKG Incomplete ──┼──► Hard rule DR-031 / P-002.1 §3
XC-G2…G12 not all PASS ──┤
XC-REC NO GO posture ──┘
                │
                ▼
         Board Recommendation
              NO GO
```

CONDITIONAL GO is **unavailable** while any hard-gate FAIL remains.  
DEFER is **not** the correct label today because G1 FAIL is already proven.

---

## Decision → exit criterion (release-critical)

| Decision | Exit criterion | Note |
|---|---|---|
| DR-025 / DR-051 | XC-G1 | KSI bar vs current 62 |
| DR-022 / DR-033 | XC-G1 (G1.9) | Effectiveness ≠ perception |
| DR-042 | XC-G1 (G1.5) / XC-G3 | K8 floor met |
| DR-030 / DR-031 | All XC-G* + XC-PKG | Gates required; FAIL → NO GO |
| DR-041 | XC-REC | Current recommendation posture |
| DR-040 / DR-032 | XC-REC (separable) | Beta ≠ V1 GO |
| DR-036 / DR-035 / DR-021 | XC-G4 / XC-G6 / claims | Freezes |
| DR-043 / DR-009 / DR-039 | XC-G12 | Flag honesty |
| DR-047 | XC-G9 | Telemetry OFF honesty |

---

## Risk → exit criterion (declaration-critical)

| Risk | Exit criterion | Closure posture (register) |
|---|---|---|
| PR-001 | XC-G1 (G1.9) | ACTIVE Red |
| PR-002 | XC-G1 (G1.1) | ACTIVE Red |
| PR-003 / PR-007 | XC-G10 → Stage 1 → G1.9 path | ACTIVE Red |
| PR-006 | XC-G1 (G1.9) | ACTIVE Red |
| PR-009 | XC-G1 (G1.7) | ACTIVE Red |
| PR-019 | XC-PKG / G2–G12 | ACTIVE Red |
| PR-020 | XC-G2 | ACTIVE Red |
| PR-004 / PR-014 | XC-REC | Controlled while NO GO held |
| PR-010 | XC-G7 | ACTIVE Amber |
| PR-012 / PR-016 | XC-G12 | ACTIVE |
| PR-013 | XC-G8 | ACTIVE Amber |
| PR-011 | XC-G9 | Controlled |
| PR-023 | XC-G10 | ACTIVE Amber |

Full cards: `../p003_3_product_risk_register/`.

---

## Evidence programme → criterion

| Programme | Contributes to |
|---|---|
| P-001.1 / P-001.2 / P-001.3 | Law behind XC-G1 / XC-G3 / XC-G4 |
| P-002.1 | Gate law for all XC-G*; XC-PKG; XC-REC template |
| P-003.1 | Synthesis statuses consumed here |
| P-003.2–P-003.7 | Decisions, risks, assumptions, evidence hierarchy, maturity context, Board procedure |
| EP-003.* | Quality contracts → XC-G3–G6; effectiveness framework → G1.9 |
| EP-004.* | Private beta / privacy → G1.9 path; personalisation flags → XC-G12 |
| EP-005.* | Validated KSI honesty → XC-G1 |
| EP-006.* | MES / readiness perception → G1.5 / K3 / XC-G3 / XC-G6 |
| EP-007.* | Journey K1; effectiveness Stage 1 design → XC-G1 / XC-G5 |

---

## Claim / evidence hierarchy (P-003.5) — reminder

| Claim family | Minimum evidence class | Current Version 1 posture |
|---|---|---|
| C-V1 production-ready | Full P-002.1 package + Board GO | **Not permitted** (NO GO) |
| Educational effectiveness | E4/E5 cohort outcomes | **Unavailable** (`N_external = 0`) |
| Perception / Tier B | E2/E3 internal | Used for KSI movement; **not** G1.9 substitute (DR-033) |

---

**End of EXIT_TRACEABILITY**
