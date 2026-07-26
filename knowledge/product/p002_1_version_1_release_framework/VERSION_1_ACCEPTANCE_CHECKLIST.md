# Version 1 Acceptance Checklist

**Programme:** P-002.1 — Version 1 Release Framework  
**Version:** 1.0  
**Status:** Active — operational checklist for Version 1 production-ready declaration  
**Effective:** 2026-07-26  
**Companion:** [`VERSION_1_RELEASE_FRAMEWORK.md`](VERSION_1_RELEASE_FRAMEWORK.md)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## How to use

1. Freeze the **claim window** and **candidate version / tag**.
2. For each criterion: mark **PASS** / **FAIL** / **HOLD** / **N/A** (N/A only where explicitly allowed).
3. Link evidence paths in the Evidence column (see [`VERSION_1_EVIDENCE_REQUIREMENTS.md`](VERSION_1_EVIDENCE_REQUIREMENTS.md)).
4. Any **FAIL** on a hard gate → overall **NO-GO**.
5. File the completed checklist inside the Version 1 Evidence Package.

**Header**

| Field | Value |
|---|---|
| Candidate version / tag | |
| Claim window (dates) | |
| Assessor | |
| Date | |
| Overall recommendation | GO / GO WITH CONDITIONS / NO-GO / DEFER |

---

## G1 — Validated KSI

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G1.1 | Published KSI ≥ 80 | | |
| G1.2 | Confidence High or Medium | | |
| G1.3 | Assessment ≤ 90 days old | | |
| G1.4 | No category below 50 | | |
| G1.5 | K8 ≥ 70 | | |
| G1.6 | Per-category evidence + rationale + limitations | | |
| G1.7 | Re-score tolerance ±3 resolved | | |
| G1.8 | Claim language distinguishes KSI from pass-rate proof | | |
| G1.9 | EP-003 / EP-004 educational Go / No-Go not NO-GO | | |
| G1.10 | No unresolved educational honesty incident | | |

**G1 gate result:** PASS / FAIL / HOLD  

---

## G2 — Constitutional compliance

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G2.1 | Vision Final Test Pass for claim set | | |
| G2.2 | No Never-Build violation in production defaults | | |
| G2.3 | Educational claim honesty (no dual truth / false certainty) | | |
| G2.4 | EVF Educational Release Gate APPROVED or CONDITIONAL with holds cleared | | |
| G2.5 | One Education OS runtime; no second educational brain | | |
| G2.6 | Curriculum V1 and V2 loadable / traversable | | |
| G2.7 | SIA filed for material EP/P since P-001.1 effective date | | |
| G2.8 | ADR index current for claim-window boundary changes | | |

**G2 gate result:** PASS / FAIL / HOLD  

---

## G3 — Explainability coverage

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G3.1 | Mandatory Explanation Schema on Rec / Plan / Readiness production defaults | | |
| G3.2 | Explainability Review Checklist Pass (or waiver) for in-scope programmes | | |
| G3.3 | K8 ≥ 70 checklist-backed | | |
| G3.4 | Runtime A explanation consistency spot-check pack | | |
| G3.5 | Zero open P1 explainability honesty defects | | |

**G3 gate result:** PASS / FAIL / HOLD  

---

## G4 — Recommendation Quality compliance

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G4.1 | Recommendation Review Checklist Pass (or waiver) for in-scope programmes | | |
| G4.2 | K2 ≥ 50 | | |
| G4.3 | Decision Framework / plan-coherence on production-default primary tips | | |
| G4.4 | Scorecard evaluation filed; 0 hard-gate precision failures in production defaults | | |
| G4.5 | Effectiveness marketing freeze respected (or formally lifted) | | |

**G4 gate result:** PASS / FAIL / HOLD  

---

## G5 — Planning Quality compliance

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G5.1 | Schema-complete daily plan / mission surfaces on production defaults | | |
| G5.2 | Planning quality automated tests green | | |
| G5.3 | No conflicting “today” / duration directives in smoke / dogfood pack | | |
| G5.4 | Personalisation flag posture honest (ON only if fail-open rules met; else OFF + not marketed) | | |
| G5.5 | No open planning honesty incidents | | |

**G5 gate result:** PASS / FAIL / HOLD  

---

## G6 — Readiness Quality compliance

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G6.1 | Schema-complete readiness surfaces on production defaults | | |
| G6.2 | Readiness quality automated tests green | | |
| G6.3 | Honest refusal / cannot-yet-be-estimated path verified | | |
| G6.4 | Drivers, confidence, next action present on reviewed surfaces | | |
| G6.5 | No Exam Ready / overclaim incidents open | | |

**G6 gate result:** PASS / FAIL / HOLD  

---

## G7 — Performance

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G7.1 | CI soft budgets green (`tests/ga/test_performance_benchmarks.py`) | | |
| G7.2 | Staging/production operator sample recorded **or** HOLD filed | | |
| G7.3 | No unexplained P1 latency regression without debt + HOLD | | |

**G7 gate result:** PASS / FAIL / HOLD  

---

## G8 — Reliability

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G8.1 | Health live + ready on tagged fingerprint | | |
| G8.2 | Production smoke pack pass | | |
| G8.3 | No unresolved Sev-1 production incidents | | |
| G8.4 | Rollback path documented / verified | | |
| G8.5 | Backup / recovery posture acknowledged for release class | | |

**G8 gate result:** PASS / FAIL / HOLD  

---

## G9 — Production telemetry

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G9.1 | Analytics posture honest (active under go-live **or** gated OFF without overclaim) | | |
| G9.2 | Operational request/error/slow logs available for tag | | |
| G9.3 | Dual-run / soak / cutover telemetry healthy for flags intended ON | | |
| G9.4 | Privacy / catalogue constraints respected | | |

**G9 gate result:** PASS / FAIL / HOLD  

---

## G10 — Security and data integrity

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G10.1 | GA security review current; residuals acknowledged; no new criticals | | |
| G10.2 | Production SECRET_KEY validation intact | | |
| G10.3 | CSRF / session / headers behaviour preserved | | |
| G10.4 | Ownership scoping intact for personal resources | | |
| G10.5 | Dependency audit reviewed for tag | | |
| G10.6 | No secrets in release artefacts | | |
| G10.7 | Migrations / StartupService / data integrity posture OK | | |

**G10 gate result:** PASS / FAIL / HOLD  

---

## G11 — Test coverage

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G11.1 | Required pytest suites green | | |
| G11.2 | Ruff policy green | | |
| G11.3 | Architecture / curriculum V1/V2 invariant tests green | | |
| G11.4 | GA package green as required for release class | | |
| G11.5 | Quality-contract suites green for production-default surfaces | | |
| G11.6 | Flake quarantine listed; no silent skip of hard-gate suites | | |

**G11 gate result:** PASS / FAIL / HOLD  

---

## G12 — Production feature-flag readiness

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| G12.1 | Version 1 flag matrix published | | |
| G12.2 | Flags claimed as V1 behaviour are ON (or claims exclude them) | | |
| G12.3 | OFF flags not marketed as live | | |
| G12.4 | Cutover / dual-run / soak prerequisites met for ON flags | | |
| G12.5 | `.env.example` / config docs match matrix | | |
| G12.6 | Emergency flag OFF / kill-switch path documented | | |

**G12 gate result:** PASS / FAIL / HOLD  

---

## Founder Review (sign-off)

Under GP-001, each capacity requires its own Founder Review. Leave blank until completed. Evidence packs above are unchanged. G1.7 still requires an independent second assessor where applicable.

| Founder Review | Reviewer | Date | Capacity | Decision | Notes |
|---|---|---|---|---|---|
| G1 / claim language / overall draft | | | Product Owner | | |
| G2.3–G2.4 / G3–G4 educational honesty | | | Educational Gate Owner | | |
| G2.5–G2.6 / G2.8 architecture | | | Engineering Owner (architecture lens) | | |
| G5–G9 / G11–G12 technical | | | Engineering Owner | | |
| G10 security / data integrity | | | Privacy Owner (security lens) | | |
| Deploy fingerprint / smoke / rollback | | | Operations Owner (release lens) | | |
| Overall GO / NO GO recommendation record | | | Product Board Chair | | |

Authority: `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`.

---

**End of VERSION_1_ACCEPTANCE_CHECKLIST**
