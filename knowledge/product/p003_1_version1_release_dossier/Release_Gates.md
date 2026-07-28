# Release Gates G1–G12 — Board Status

**Programme:** P-003.1 — Version 1 Release Dossier  
**Date:** 2026-07-26  
**Authority:** `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md`  
**Tracker:** `knowledge/VERSION_1_READINESS.md`

Statuses: **PASS** | **FAIL** | **HOLD** | **IN PROGRESS** | **Partially met** | **Not scored**  
Missing declaration artefacts are labelled **Evidence currently unavailable.**

---

## Overall declaration posture

| Question | Answer |
|---|---|
| May Version 1 be declared production-ready? | **No** |
| Hard-gate blocker | **G1 FAIL** (G1.1, G1.9); G1.7 HOLD |
| Evidence package | G1 slice only; full G1–G12 package **incomplete** |
| Board recommendation | **NO GO** |

---

## G1 — Validated KSI

| Field | Value |
|---|---|
| **Current status** | **FAIL** |
| **Evidence** | EP-005.1 board + EP-006.3/006.5/007.2 revalidations; EP-007.3 G1.9; `VALIDATED_KSI_REPORT.md`; `K1_REVALIDATION.md`; `G1_9_STATUS.md` |
| **Outstanding work** | Raise validated KSI to ≥80; clear effectiveness NO-GO; complete G1.7 independent re-score |
| **Risk** | Premature usefulness claim; student harm via overconfidence |
| **Board recommendation** | Treat as **blocking**. Do not declare. |

### G1 criteria detail

| ID | Criterion | Status | Evidence note |
|---|---|---|---|
| G1.1 | KSI ≥ 80 | **FAIL** | Validated **62** |
| G1.2 | Confidence High/Medium | **PASS** | Medium |
| G1.3 | Assessment ≤ 90 days | **PASS** | 2026-07-26 |
| G1.4 | No category &lt; 50 | **PASS** | Min K6 = 50 |
| G1.5 | K8 ≥ 70 | **PASS** | K8 = 70 (EP-006.3) |
| G1.6 | Evidence paths cited | **PASS** | Register + revalidation chain |
| G1.7 | Independent re-score ±3 | **HOLD** | Second assessor not filed — Evidence currently unavailable |
| G1.8 | KSI ≠ pass-rate claim | **PASS** | Claim discipline preserved |
| G1.9 | Effectiveness not NO-GO | **FAIL** | EP-003/004/007.3 |
| G1.10 | No honesty incident | **PASS** | Themes logged, not escalated |

---

## G2 — Constitutional compliance

| Field | Value |
|---|---|
| **Current status** | **IN PROGRESS** — full declaration board **Evidence currently unavailable** |
| **Evidence** | Architecture COMPLETE (`VERSION_1_READINESS`); Vision/Educational/Architecture constitutions active; EVF educational outcome **not APPROVED** for V1 claim class per readiness notes |
| **Outstanding work** | Constitutional compliance memo for claim window; EVF outcome for V1 claim class; SIA currency check (G2.7); ADR currency (G2.8) |
| **Risk** | Declaring readiness while educational trust gate open |
| **Board recommendation** | Do not treat Architecture COMPLETE as G2 PASS for declaration |

---

## G3 — Explainability coverage

| Field | Value |
|---|---|
| **Current status** | **Partially met** |
| **Evidence** | EP-003.1–.3 Explainability Review Checklists Pass; MES delivery + G1.5 PASS (K8 70); Runtime A contracts |
| **Outstanding work** | Declaration spot-check pack across surfaces (G3.4); confirm zero open P1 honesty defects for claim window |
| **Risk** | Checklist Pass without sustained student-visible consistency |
| **Board recommendation** | Credit progress; require packaged evidence before PASS |

---

## G4 — Recommendation Quality compliance

| Field | Value |
|---|---|
| **Current status** | **Partially met** |
| **Evidence** | EP-003.1 Recommendation Review Checklist Pass; K2 validated **55** (floor met); Decision Framework on production defaults |
| **Outstanding work** | Scorecard evaluation for claim window (instrumentation gaps); hard-gate precision sample |
| **Risk** | Marketing freeze lift without scorecard — freeze remains active |
| **Board recommendation** | Keep recommendation-effectiveness marketing frozen |

---

## G5 — Planning Quality compliance

| Field | Value |
|---|---|
| **Current status** | **Partially met** |
| **Evidence** | EP-003.3 planning quality tests; K1 validated **72**; EP-007.1 duration/home consolidation |
| **Outstanding work** | Declaration smoke/dogfood pack for conflicting duration (G5.3) filed in evidence package |
| **Risk** | Dual-run environments outside W-PROD still dual-home (noted residual) |
| **Board recommendation** | Accept W-PROD progress; package evidence for PASS |

---

## G6 — Readiness Quality compliance

| Field | Value |
|---|---|
| **Current status** | **Partially met** |
| **Evidence** | EP-003.2 tests; EP-006.4 delivery; K3 **65**; honest refusal path reviewed in programmes |
| **Outstanding work** | Claim-window spot-check pack; keep Exam Ready marketing blocked |
| **Risk** | Overclaiming readiness usefulness from K3 65 alone |
| **Board recommendation** | Credit progress; no Exam Ready claims |

---

## G7 — Performance

| Field | Value |
|---|---|
| **Current status** | **HOLD** (claim-restricted; EI-001.3) |
| **Evidence** | CI soft budgets green (`tests/ga/test_performance_benchmarks.py` / Performance Baseline); formal HOLD `docs/production/G7_PERFORMANCE_HOLD.md` |
| **Outstanding work** | Staging/production operator sample; production load test **NOT STARTED** (required to lift HOLD) |
| **Risk** | High-traffic claims without load evidence — **restricted by HOLD** |
| **Board recommendation** | Accept HOLD for invite-only / low-concurrency claims only; lift before high-traffic marketing |

---

## G8 — Reliability

| Field | Value |
|---|---|
| **Current status** | **Partially met** (EI-001.3 procedure pack filed) |
| **Evidence** | Health/smoke procedures; `docs/production/G8_RELIABILITY_EVIDENCE.md` (G8.4 tabletop rollback drill; G8.5 backup/recovery ack) |
| **Outstanding work** | Tagged-deploy health/smoke fingerprint in Version 1 Evidence Package; optional live restore drill before GA marketing |
| **Risk** | Declaring without tagged-deploy fingerprint |
| **Board recommendation** | Credit procedure pack; require fingerprint at declaration |

---

## G9 — Production telemetry

| Field | Value |
|---|---|
| **Current status** | **COMPLETE (flag OFF)** / claim-safe if not overclaimed |
| **Evidence** | Analytics ops ready; EP-002 go-live checklist; Journey emit deferred (ADR-026) |
| **Outstanding work** | If Version 1 claims live metrics, activate under checklist; else keep OFF in claim language |
| **Risk** | Claiming live Journey KPIs while emit deferred |
| **Board recommendation** | PASS only with honest flag/claim alignment |

---

## G10 — Security and data integrity

| Field | Value |
|---|---|
| **Current status** | **IN PROGRESS** (G10.5 closed EI-001.2; ops ack EI-001.3; privacy residual open) |
| **Evidence** | GA security review; factory SECRET_KEY; hard dependency audit; `docs/production/G10_OPERATIONAL_EVIDENCE.md` |
| **Outstanding work** | Privacy Review signatures for Stage 1; CSP hardening residual |
| **Risk** | Expanding cohort without privacy sign-off |
| **Board recommendation** | Block Stage 1 expansion until C1; do not declare while privacy open for intended claim class |

---

## G11 — Test coverage

| Field | Value |
|---|---|
| **Current status** | **IN PROGRESS** |
| **Evidence** | Broad pytest + GA package; quality-contract suites for EP-003.* |
| **Outstanding work** | Continuous green on release candidate tag; flake quarantine discipline |
| **Risk** | Declaring on stale or red CI |
| **Board recommendation** | Require green release-candidate CI for PASS |

---

## G12 — Production feature-flag readiness

| Field | Value |
|---|---|
| **Current status** | **PASS** (invite-only / engineering claim class; EI-001.3) |
| **Evidence** | Published matrix `docs/production/VERSION_1_FLAG_MATRIX.md`; aligned with `render.yaml` + `.env.example`; RP-001 register |
| **Outstanding work** | Re-score before any production-OFF educational flag is flipped ON; Product/Release acknowledgement at declaration |
| **Risk** | Marketing OFF flags as live; unsafe ON without soak |
| **Board recommendation** | Keep OFF educational flags OFF; refresh matrix on any default change |

---

## Cross-gate board recommendation

1. **NO GO** on Version 1 production-ready declaration while G1 FAIL.  
2. Treat G1.1 and G1.9 as the critical educational path.  
3. Assemble a full Evidence Package before scoring G2–G12 as PASS.  
4. Allow EP-004 Stage 0 continuation under existing conditions — that is **not** a Version 1 GO.
