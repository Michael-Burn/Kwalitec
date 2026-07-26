# Claim Traceability

**Programme:** P-003.5 — Evidence Hierarchy & Claim Standard  
**Version:** 1.0  
**Status:** Active — evidence → claim → decision → risk → gate map  
**Effective:** 2026-07-26  
**Does not:** Amend decisions, risks, assumptions, or release gates — **maps only**  

---

## 1. Purpose

Make the chain explicit:

```
Evidence  →  Claim  →  Decision  →  Risk  →  Release Gate
```

So every public or board claim can be traced without inventing new law.

---

## 2. Chain legend

| Node | Register / artefact |
|---|---|
| Evidence | E1–E5 per this programme; paths under `knowledge/product/` |
| Claim | C-* codes in [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md) |
| Decision | `DR-NNN` in P-003.2 Product Decision Register |
| Risk | `PR-NNN` in P-003.3 Product Risk Register |
| Assumption | `PA-NNN` in P-003.4 Product Assumption Register (epistemic support) |
| Release Gate | P-002.1 G1–G12 / EP-003 educational gates / G1.x subcriteria |

---

## 3. Primary chains (Version 1)

### 3.1 Educational effectiveness

| Node | Current content |
|---|---|
| Evidence | E5 **Unavailable**; EP-007.3 assessment; EP-003 PENDING EVIDENCE |
| Claim | C-EDU **prohibited**; C-BEN outcome **prohibited** |
| Decision | DR-021, DR-022, DR-033, DR-036 |
| Risk | PR-001, PR-006, PR-007 |
| Assumption | PA-025 Rejected (perception≠effectiveness); PA-026 Validated (external required); PA-039 Hypothesis |
| Gate | G1.9 **FAIL**; EP-003 G5/G7/G8 OPEN |

### 3.2 Validated KSI / usefulness bar

| Node | Current content |
|---|---|
| Evidence | E3 validated board KSI **62** Medium; E2 contracts; E4/E5 absent |
| Claim | C-VAL-I bounded OK; C-V1 **prohibited**; KSI ≥ 80 claim **prohibited** |
| Decision | DR-025, DR-026, DR-027, DR-051, DR-041 |
| Risk | PR-002, PR-008, PR-009 |
| Assumption | PA-021 Validated (bar); PA-023 Rejected (estimate stacking) |
| Gate | G1.1 **FAIL**; G1.2 PASS (Medium); G1.5 **PASS**; G1.7 HOLD |

### 3.3 Perception improvements (MES / readiness / journey)

| Node | Current content |
|---|---|
| Evidence | E3 Tier B packs; E2 MES/contracts |
| Claim | C-VAL-I Board-only with N/confidence; C-VAL-E **prohibited**; C-EDU **prohibited** |
| Decision | DR-019, DR-042, DR-007, DR-008, DR-033 |
| Risk | PR-005 (cold-start), PR-008 (confidence ceiling) |
| Assumption | PA-001… supported perception themes; PA-025 Rejected shortcut |
| Gate | G1.5 PASS (K8); G3/G6 structural; G1 overall FAIL |

### 3.4 Version 1 production-ready declaration

| Node | Current content |
|---|---|
| Evidence | Incomplete G1–G12 package; dossier synthesis E1 packaging |
| Claim | C-V1 **No**; C-REC = **NO GO** |
| Decision | DR-030, DR-031, DR-032, DR-041 |
| Risk | PR-004, PR-014, PR-019 |
| Assumption | PA-027 Rejected (GA≠ready) |
| Gate | Hard-gate FAIL → NO-GO; overall **NO GO** |

### 3.5 Recommendation quality vs effectiveness marketing

| Node | Current content |
|---|---|
| Evidence | E2 P-001.3 / EP-003.1 contracts; E3 limited; E5 absent |
| Claim | C-STR OK; C-COM recommendation-effectiveness **Frozen** |
| Decision | DR-029, DR-036, DR-050, DR-002 |
| Risk | PR-001 (overclaim path), related honesty risks |
| Assumption | PA-014 Hypothesis (behaviour change) |
| Gate | G4 structural; G4.5 freeze; EP-003 G9 PASS (freeze active) |

### 3.6 Readiness honesty / Exam Ready ban

| Node | Current content |
|---|---|
| Evidence | E2 refusal paths; E3 readiness perception; E5 absent |
| Claim | C-STR / C-VAL-I bounded; Exam Ready C-COM **Banned** |
| Decision | DR-004, DR-018, DR-035 |
| Risk | PR-005, PR-018 |
| Assumption | Readiness≠Next Action law |
| Gate | G6; G6.3 |

### 3.7 Personalisation / Twin defaults

| Node | Current content |
|---|---|
| Evidence | E2 flag OFF authority; E3/E4 usefulness **unsupported** in W-PROD |
| Claim | Student-perceived personalisation lift **Δ=0**; no C-COM |
| Decision | DR-006, DR-009, DR-010, DR-039, DR-043 |
| Risk | PR-012, PR-016, PR-025 |
| Assumption | PA-011 Hypothesis |
| Gate | G12 |

### 3.8 Operational release vs educational release

| Node | Current content |
|---|---|
| Evidence | E2 ops artefacts (partial); E5 educational absent |
| Claim | C-REL possible with pack; ≠ C-EDU ≠ C-V1 |
| Decision | DR-032, DR-040, DR-041 |
| Risk | PR-010, PR-011, PR-014, PR-015 |
| Assumption | PA-027 Rejected shortcut |
| Gate | G7–G11 vs G1.9 separable |

---

## 4. Evidence level → typical claim → gate touchpoints

| Evidence | Typical allowed claims | Typical blocked claims | Gates most implicated |
|---|---|---|---|
| E1 | Process, law, estimates | Any student-benefit / V1 ready | None alone |
| E2 | C-IMP, C-STR, partial C-REL | C-VAL-*, C-EDU, C-V1 | G3–G6, G7–G11 structural |
| E3 | C-VAL-I (Board) | C-VAL-E, C-EDU, C-V1, public C-BEN | G1 category boards; G1.5 |
| E4 | C-VAL-E; stronger C-BEN perception | C-EDU until E5; C-V1 alone | G1 High confidence path |
| E5 | C-EDU, C-BEN outcome | Claims beyond metrics; C-V1 alone | G1.9; EP-003 Go |

---

## 5. Claim code → decision / risk quick index

| Claim code | Primary decisions | Primary risks if over-claimed |
|---|---|---|
| C-IMP | DR-001…DR-020 (architecture delivery) | PR-021 drift if docs diverge |
| C-STR | DR-028, DR-029, DR-052 | Honesty / quality regressions |
| C-VAL-I | DR-027, DR-042, DR-051 | PR-008 overconfidence |
| C-VAL-E | DR-022 (floors), DR-027 | PR-006 |
| C-EDU | DR-021, DR-022, DR-033 | PR-001 |
| C-BEN | DR-044 Final Test; DR-021 | PR-001, PR-004 |
| C-REL | DR-030 (partial), ops decisions | PR-010, PR-014 |
| C-V1 | DR-030, DR-031, DR-041 | PR-004, PR-019 |
| C-COM | DR-035, DR-036 + freezes | PR-001, PR-016 |
| C-REC | DR-041, DR-032 | PR-004 |

---

## 6. Programme evidence map (read-only citations)

| Programme | Highest evidence contributed | Claims unlocked (bounded) |
|---|---|---|
| EP-003.1–.3 | E2 | C-STR |
| EP-003.4 / EP-004.1–.3 | E1–E2 (flags OFF) | C-IMP gated; no W-PROD usefulness |
| EP-004 Stage 0 | E3 exploratory | Process; not C-EDU |
| EP-005.1 | E3 KSI board | C-VAL-I under-claim; G1 FAIL honesty |
| EP-005.2 | E1 remediation | Direction only |
| EP-006.2 | E2 MES delivery | C-IMP / C-STR |
| EP-006.3 | E3 K8 | C-VAL-I; G1.5 |
| EP-006.4 | E2 readiness UX | C-IMP (lift deferred) |
| EP-006.5 | E3 K3 | C-VAL-I |
| EP-007.1 | E2 journey consolidation | C-IMP / C-STR |
| EP-007.2 | E3 K1 / KSI 62 | C-VAL-I |
| EP-007.3 | E1 design; E5 absent | C-EDU still prohibited |
| P-003.1 | E1 synthesis | C-REC = NO GO |
| P-003.2–.4 | E1 registers | Traceability only |
| P-003.5 (this) | E1 standard | Claim discipline; ΔKSI = 0 |

---

## 7. How to extend the map

When new evidence arrives:

1. Classify (E1–E5).  
2. Update allowed C-* in Board posture card (`CLAIM_STANDARD.md` §7) — via future programme, not silent edit of decisions.  
3. Link DR/PR/PA already filed; **do not** invent new DR/PR here.  
4. Re-check gates in P-002.1 evidence package — this file does not flip gates.

---

## 8. References

- [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md)  
- [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md)  
- `../p003_2_product_decision_register/DECISION_TRACEABILITY.md`  
- `../p003_3_product_risk_register/RISK_TRACEABILITY.md`  
- `../p003_4_product_assumption_register/ASSUMPTION_TRACEABILITY.md`  
- `../p003_1_version1_release_dossier/Release_Gates.md`

---

**End of CLAIM_TRACEABILITY**
