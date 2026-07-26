# Version 1 Exit Criteria

**Programme:** P-003.8 — Version 1 Exit Criteria  
**Version:** 1.0  
**Status:** Active — synthesis only  
**Effective:** 2026-07-26  
**Audience:** Product Board  
**Does not:** Introduce new policy, evidence requirements, release gates, or governance rules; amend decisions, risks, assumptions, maturity, dossier bodies, P-002.1 gates, runtime, or services  

---

## One question this pack answers

> **Can Version 1 be released today?**

**Answer (as of 2026-07-26):** **No.** Board recommendation remains **NO GO** (DR-041).

---

## 1. Purpose

These Exit Criteria **consolidate** existing Version 1 production-ready governance into a single Board-facing pack.

| This programme | Does |
|---|---|
| **Does** | Re-state P-002.1 gates G1–G12, evidence-package rules, and Board recommendation outcomes as exit criteria |
| **Does** | Trace each criterion to decisions, risks, gates, and evidence already on file |
| **Does** | Freeze a current assessment aligned with the Release Dossier (**NO GO**) |
| **Does not** | Add gates, raise bars, invent evidence, flip DR-041, or declare Version 1 |

**Authority stack (unchanged):** Vision 2030 → Educational Constitution / EVF → Architecture Constitution → PSF / P-001.2 / P-001.3 → **P-002.1 Release Framework** → Release Dossier (P-003.1) → Product Board Charter (P-003.7) → **this synthesis**.

Binding gate law remains:

- `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md`
- `VERSION_1_ACCEPTANCE_CHECKLIST.md`
- `VERSION_1_GO_NO_GO_GUIDE.md`
- `VERSION_1_EVIDENCE_REQUIREMENTS.md`

Board synthesis remains:

- `knowledge/product/p003_1_version1_release_dossier/`

---

## 2. Current Position

| Field | Value |
|---|---|
| **Board recommendation** | **NO GO** |
| **Decision ID** | DR-041 (ACTIVE posture) |
| **Claim window** | W-PROD |
| **Validated KSI** | **62** (Medium) — DR-051 |
| **Target** | ≥ **80** (DR-025 / G1.1) |
| **Gate G1** | **FAIL** (G1.1, G1.9 blocking; G1.7 HOLD; G1.5 PASS) |
| **Educational effectiveness** | **NO-GO / PENDING EVIDENCE** (G1.9) |
| **Private beta** | **GO WITH CONDITIONS** (DR-040) — Stage 0 only; does **not** clear Version 1 |
| **Evidence package G1–G12** | Incomplete (G1 slice only) |
| **Maturity Release Readiness** | Level 2 / Red (context only; not a gate) |

**Supporting references only (not amended):**

| Artefact | Path |
|---|---|
| Dossier §11 / recommendation | `../p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md` |
| Executive Summary | `../p003_1_version1_release_dossier/Executive_Summary.md` |
| Gate board | `../p003_1_version1_release_dossier/Release_Gates.md` |
| State snapshot | `../p003_1_version1_release_dossier/Version1_State.md` |
| Decision DR-041 | `../p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md` |
| Charter §7.3 | `../p003_7_product_board_charter/PRODUCT_BOARD_CHARTER.md` |
| Readiness tracker | `knowledge/VERSION_1_READINESS.md` |

Detail: [`CURRENT_RELEASE_POSITION.md`](CURRENT_RELEASE_POSITION.md).

---

## 3. Exit Criteria

**Identifier scheme:** `XC-G1` … `XC-G12` map 1:1 to P-002.1 gate families. `XC-PKG` and `XC-REC` restate existing package and signed-record requirements from P-002.1 §5 — they are **not** new gates.

**Status vocabulary:** PASS | FAIL | HOLD | Partially met | IN PROGRESS | Not scored | Incomplete — as used in P-003.1 `Release_Gates.md`.

**Closure rule (existing):** Any hard-gate FAIL → overall **NO GO** (DR-031). HOLDs → **CONDITIONAL GO** / **GO WITH CONDITIONS** at best (P-002.1 Go / No-Go Guide). Incomplete package without proven FAIL → **DEFER** at best.

---

### XC-G1 — Validated KSI

| Field | Content |
|---|---|
| **Identifier** | XC-G1 |
| **Description** | Educational usefulness meets the Version 1 bar with **validated** (not estimated) KSI and G1.1–G1.10 criteria under P-002.1 / PSF. |
| **Evidence required** | Validated KSI board ≤ 90 days; per-category rationale; G1.7 independent re-score (±3); EP-003/EP-004 educational Go/No-Go for claim window; honesty-incident clear. Paths per `VERSION_1_EVIDENCE_REQUIREMENTS.md` G1. |
| **Current status** | **FAIL** — G1.1 FAIL (KSI **62** &lt; 80); G1.9 FAIL (effectiveness NO-GO); G1.7 **HOLD**; G1.5 **PASS** (K8 **70**); G1.2/G1.3/G1.4/G1.6/G1.8/G1.10 PASS per dossier |
| **Related Decisions** | DR-025, DR-026, DR-027, DR-022, DR-031, DR-033, DR-041, DR-042, DR-051 |
| **Related Risks** | PR-001, PR-002, PR-006, PR-008, PR-009 |
| **Related Gates** | G1 (hard); criteria G1.1–G1.10 |
| **Closure condition** | Gate G1 scored **PASS** (or approved HOLD path that does not overclaim) under P-002.1 Acceptance Checklist — requires at minimum G1.1 KSI ≥ 80, G1.9 not NO-GO, G1.7 resolved |

---

### XC-G2 — Constitutional compliance

| Field | Content |
|---|---|
| **Identifier** | XC-G2 |
| **Description** | Version 1 claim set passes Vision Final Test, Never-Build, Educational honesty, EVF outcome, Architecture one-runtime / curriculum V1–V2, SIA currency, ADR currency (G2.1–G2.8). |
| **Evidence required** | Constitutional compliance memo for claim window; EVF Educational Release Gate outcome; Architecture / ADR / SIA citations per Evidence Requirements G2. |
| **Current status** | **IN PROGRESS** — Architecture COMPLETE on tracker; full G2 declaration board **Evidence currently unavailable**; EVF educational outcome **not APPROVED** for V1 claim class |
| **Related Decisions** | DR-023, DR-024, DR-044, DR-001, DR-011, DR-037, DR-045 |
| **Related Risks** | PR-020, PR-022, PR-025 |
| **Related Gates** | G2 (hard) |
| **Closure condition** | G2 **PASS** (or HOLD with named claim restrictions) with EVF APPROVED / CONDITIONAL holds cleared for claim class (G2.4) |

---

### XC-G3 — Explainability coverage

| Field | Content |
|---|---|
| **Identifier** | XC-G3 |
| **Description** | Student-facing intelligence explains itself under P-001.2 (schema, checklist Pass, K8 ≥ 70, consistency spot-check, no open P1 honesty defects). |
| **Evidence required** | Explainability coverage pack: EP-003.1–.3 checklists; declaration spot-check (G3.4); K8 board linkage (G1.5 / G3.3). |
| **Current status** | **Partially met** — programme checklists Pass; G1.5 PASS; declaration spot-check pack incomplete |
| **Related Decisions** | DR-028, DR-019, DR-042, DR-052 |
| **Related Risks** | PR-005 (cold-start honesty adjacent) |
| **Related Gates** | G3 (hard); links G1.5 |
| **Closure condition** | G3 **PASS** with packaged claim-window evidence including G3.4 spot-check |

---

### XC-G4 — Recommendation Quality compliance

| Field | Content |
|---|---|
| **Identifier** | XC-G4 |
| **Description** | Student-facing recommendations meet P-001.3 (checklist, K2 floor, Decision Framework, scorecard / precision sample, marketing freeze honesty). |
| **Evidence required** | Recommendation quality pack; scorecard evaluation for claim window; freeze status (DR-036) until lifted by approved evidence. |
| **Current status** | **Partially met** — EP-003.1 checklist Pass; K2 **55** (floor met); scorecard / hard-gate precision sample for declaration incomplete; marketing freeze **active** |
| **Related Decisions** | DR-029, DR-036, DR-002, DR-050 |
| **Related Risks** | PR-001 (effectiveness claims), PR-016 |
| **Related Gates** | G4 (hard) |
| **Closure condition** | G4 **PASS**; freeze remains unless EP-001 O8 / approved evidence lifts it (G4.5) |

---

### XC-G5 — Planning Quality compliance

| Field | Content |
|---|---|
| **Identifier** | XC-G5 |
| **Description** | Daily plan / mission surfaces satisfy PlanningService Quality Contract (schema-complete, tests green, no conflicting durations, personalisation fail-open if ON). |
| **Evidence required** | Planning quality tests; claim-window smoke/dogfood pack for duration honesty (G5.3). |
| **Current status** | **Partially met** — EP-003.3 tests; K1 **72**; EP-007.1 W-PROD consolidation; declaration smoke pack filing incomplete |
| **Related Decisions** | DR-003, DR-007, DR-008, DR-017, DR-052 |
| **Related Risks** | (Journey residual noted outside W-PROD in dossier; not a separate PR ID for dual-home on W-PROD) |
| **Related Gates** | G5 (hard) |
| **Closure condition** | G5 **PASS** with G5.3 pack filed for claim window |

---

### XC-G6 — Readiness Quality compliance

| Field | Content |
|---|---|
| **Identifier** | XC-G6 |
| **Description** | Readiness surfaces satisfy ReadinessService Quality Contract without false certainty; Exam Ready marketing remains gated (DR-035). |
| **Evidence required** | Readiness quality tests; drivers / confidence / next; honest refusal path; claim-window spot-check. |
| **Current status** | **Partially met** — EP-003.2 / EP-006.4 delivery; K3 **65**; claim-window pack incomplete; Exam Ready blocked |
| **Related Decisions** | DR-004, DR-018, DR-035, DR-052 |
| **Related Risks** | PR-005 |
| **Related Gates** | G6 (hard) |
| **Closure condition** | G6 **PASS**; no Exam Ready claims without readiness gates |

---

### XC-G7 — Performance

| Field | Content |
|---|---|
| **Identifier** | XC-G7 |
| **Description** | Student-critical surfaces meet published budgets (CI soft budgets + operator sample, or HOLD with no high-traffic claim). |
| **Evidence required** | `tests/ga/test_performance_benchmarks.py` / Performance Baseline; staging/production operator sample or HOLD record. |
| **Current status** | **IN PROGRESS** — CI soft budgets green; production load test **NOT STARTED** |
| **Related Decisions** | DR-030 (gate family required) |
| **Related Risks** | PR-010 |
| **Related Gates** | G7 (hard\*; HOLD allowed under P-002.1 claim restrictions) |
| **Closure condition** | G7 **PASS** or approved **HOLD** with forbidden high-traffic claims named |

---

### XC-G8 — Reliability

| Field | Content |
|---|---|
| **Identifier** | XC-G8 |
| **Description** | Production posture stable for declared cohort (health, smoke, Sev-1 clear, rollback verified, backup acknowledgement). |
| **Evidence required** | Health live/ready; smoke pack; rollback drill note; backup/recovery acknowledgement per Evidence Requirements G8. |
| **Current status** | **IN PROGRESS** — health/smoke posture; claim-window Sev-1 / rollback drill packaging incomplete |
| **Related Decisions** | DR-048 (bootstrap safety adjacent) |
| **Related Risks** | PR-013 |
| **Related Gates** | G8 (hard\*; HOLD allowed under P-002.1 rules) |
| **Closure condition** | G8 **PASS** or approved **HOLD** with claim restrictions |

---

### XC-G9 — Production telemetry

| Field | Content |
|---|---|
| **Identifier** | XC-G9 |
| **Description** | Operators observe learning-relevant and operational signals without inventing educational scores; live-metric claims match flag state. |
| **Evidence required** | Analytics go-live checklist alignment; foundational logs; dual-run/soak telemetry if flags ON; privacy / EVENT_CATALOGUE constraints. |
| **Current status** | **COMPLETE (flag OFF)** / claim-safe if not overclaimed — Journey emit deferred (ADR-026 / DR-047) |
| **Related Decisions** | DR-047, DR-043 |
| **Related Risks** | PR-011 |
| **Related Gates** | G9 (hard\*) |
| **Closure condition** | G9 **PASS** with honest flag/claim alignment (OFF remains acceptable if claims exclude live Journey KPIs) |

---

### XC-G10 — Security and data integrity

| Field | Content |
|---|---|
| **Identifier** | XC-G10 |
| **Description** | Authentication, authorization, secrets, CSP/session posture, dependency criticals, and data integrity meet GA bar for Version 1 claim class. |
| **Evidence required** | GA security review; factory SECRET_KEY validation; dependency audit; Privacy Review signatures when Stage 1 / claim class requires them. |
| **Current status** | **IN PROGRESS** — GA review pass with CSP residual; Stage 1 privacy signatures **open** |
| **Related Decisions** | DR-034 (invite-only reduces public-launch exposure) |
| **Related Risks** | PR-003, PR-007, PR-023 |
| **Related Gates** | G10 (hard) |
| **Closure condition** | G10 **PASS** (or Security HOLD on non-criticals); privacy signatures complete for intended claim class / Stage 1 path |

---

### XC-G11 — Test coverage

| Field | Content |
|---|---|
| **Identifier** | XC-G11 |
| **Description** | Automated verification covers architecture, GA, and Version 1 quality contracts for the release-candidate tag. |
| **Evidence required** | Green CI pytest/ruff; architecture / curriculum V1–V2 tests; GA package; quality-contract suites; flake quarantine list. |
| **Current status** | **IN PROGRESS** — broad suite green historically; continuous green on release-candidate tag required for PASS |
| **Related Decisions** | DR-011, DR-052 |
| **Related Risks** | PR-019 (package incompleteness includes test-tag discipline) |
| **Related Gates** | G11 (hard) |
| **Closure condition** | G11 **PASS** on release-candidate tag |

---

### XC-G12 — Production feature-flag readiness

| Field | Content |
|---|---|
| **Identifier** | XC-G12 |
| **Description** | Version 1 production defaults are intentional, documented, and reversible (flag matrix, claim honesty for OFF flags, soak for ON, kill-switch). |
| **Evidence required** | Published Version 1 flag matrix with owners/rollback; `.env.example` alignment; kill-switch docs. |
| **Current status** | **Not scored** — declaration matrix **Evidence currently unavailable**; personalisation/feedback OFF in W-PROD (acceptable if claimed as gated) |
| **Related Decisions** | DR-009, DR-039, DR-038, DR-043, DR-010 |
| **Related Risks** | PR-012, PR-016 |
| **Related Gates** | G12 (hard) |
| **Closure condition** | G12 **PASS** before any flag-ON Version 1 student-visible defaults (or claim language excludes OFF capabilities) |

---

### XC-PKG — Version 1 Evidence Package completeness

| Field | Content |
|---|---|
| **Identifier** | XC-PKG |
| **Description** | Dated Evidence Package (or equivalent index) links immutable paths for every hard gate per P-002.1 §5.2 / Evidence Requirements. Incomplete package blocks GO. |
| **Evidence required** | Package under `…/p002_1_version_1_release_framework/evidence/<date>_v1_declaration/` (or indexed equivalent) covering G1–G12 packs + signed decision record slot. |
| **Current status** | **Incomplete** — G1 slice exists (`evidence/2026-07-26_ksi_validation/`); full G2–G12 declaration package not assembled |
| **Related Decisions** | DR-030, DR-041 |
| **Related Risks** | PR-019, PR-021 |
| **Related Gates** | All G1–G12 (process requirement from P-002.1 §5) |
| **Closure condition** | Package complete and current for claim window; every hard gate has linked evidence |

---

### XC-REC — Signed Product Board Go / No-Go record

| Field | Content |
|---|---|
| **Identifier** | XC-REC |
| **Description** | Only the Product Board may recommend Version 1 production-ready GO or NO GO (Charter §7.2). A signed Go/No-Go record per P-002.1 template must accompany any claim-language change. |
| **Evidence required** | `VERSION_1_GO_NO_GO_DECISION.md` (or equivalent) with gate summary, holds, claim language, role sign-offs; `VERSION_1_READINESS.md` aligned same day. |
| **Current status** | **NO GO posture active** (DR-041 / dossier §11) — no GO record filed; private-beta GO WITH CONDITIONS (DR-040) is a **separate** verdict |
| **Related Decisions** | DR-032, DR-041, DR-031, DR-040 |
| **Related Risks** | PR-004, PR-014 |
| **Related Gates** | Consumes G1–G12 outcomes |
| **Closure condition** | Board records **GO** or **CONDITIONAL GO** under existing outcome rules — **not** met today |

---

## 4. Board Release Checklist

Concise meeting checklist: [`BOARD_RELEASE_CHECKLIST.md`](BOARD_RELEASE_CHECKLIST.md).  
Every item traces to existing governance (P-002.1 Acceptance Checklist, Charter Release Decision Process §10, dossier).

---

## 5. GO / NO GO Matrix

Definitions: [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md).  
Outcomes **GO**, **CONDITIONAL GO** (synonym: **GO WITH CONDITIONS**), **NO GO**, **DEFER** — from P-002.1 Go / No-Go Guide and P-003.7 Release Decision Process only.

---

## 6. Traceability

Full maps: [`EXIT_TRACEABILITY.md`](EXIT_TRACEABILITY.md).

```
Criterion (XC-*)
        ↓
Evidence (paths / packs)
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

## 7. Current Assessment

| Criterion | Status | Blocks GO today? |
|---|---|---|
| XC-G1 | **FAIL** | **Yes** (hard-gate FAIL) |
| XC-G2 | IN PROGRESS / incomplete board | Yes (package / G2.4) |
| XC-G3 | Partially met | Yes until PASS pack |
| XC-G4 | Partially met | Yes until PASS pack |
| XC-G5 | Partially met | Yes until PASS pack |
| XC-G6 | Partially met | Yes until PASS pack |
| XC-G7 | IN PROGRESS | Yes unless approved HOLD |
| XC-G8 | IN PROGRESS | Yes unless approved HOLD |
| XC-G9 | COMPLETE (flag OFF) if claims honest | No if claim language stays aligned |
| XC-G10 | IN PROGRESS | Yes for intended Stage 1 / claim class |
| XC-G11 | IN PROGRESS | Yes for RC tag |
| XC-G12 | Not scored | Yes before ON defaults / for matrix honesty |
| XC-PKG | Incomplete | **Yes** |
| XC-REC | NO GO posture | **Yes** — recommendation remains NO GO |

### Verdict

# NO GO

**Can Version 1 be released today?** **No.**

Hard-gate FAIL on **XC-G1** alone forces overall **NO GO** (DR-031). Incomplete **XC-PKG** and open G2–G12 boards reinforce the same outcome. This assessment **does not** alter DR-041, Release Gates, or any register.

Detail: [`CURRENT_RELEASE_POSITION.md`](CURRENT_RELEASE_POSITION.md) · [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md).

---

## Companion documents

| Document | Role |
|---|---|
| [`BOARD_RELEASE_CHECKLIST.md`](BOARD_RELEASE_CHECKLIST.md) | Meeting checklist |
| [`EXIT_TRACEABILITY.md`](EXIT_TRACEABILITY.md) | Criterion → evidence → decision → risk → gate → recommendation |
| [`CURRENT_RELEASE_POSITION.md`](CURRENT_RELEASE_POSITION.md) | Freeze-date scoreboard |
| [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md) | Outcome definitions |
| [`README.md`](README.md) | Folder index |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Docs-only SIA (ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion |

---

## Control statement

> P-003.8 consolidates existing exit conditions for Version 1 production-ready declaration. It introduces no new bars. As of 2026-07-26 the Product Board recommendation remains **NO GO**. Private-beta Stage 0 may continue under DR-040. Public “Version 1 production-ready” claim language remains forbidden until XC-G1–XC-G12, XC-PKG, and XC-REC close under P-002.1.

---

**End of VERSION1_EXIT_CRITERIA**
