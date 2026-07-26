# MS-006 — Risk Analysis (Learning Evidence & Experimentation Platform)

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Migration:** `MIGRATION_PLAN_MS006.md`  
**Related:** MS-001 `RISK_ANALYSIS.md`; MS-003 `RISK_ANALYSIS_MS003.md`; MS-004 `RISK_ANALYSIS_MS004.md`; MS-005 `RISK_ANALYSIS_MS005.md`; EP-004 SP4 / SP8

---

## 1. Risk rating scale

| Level | Meaning |
|---|---|
| **Low** | Contained; flag rollback sufficient |
| **Medium** | Trust or performance impact; needs soak / ADR |
| **High** | Educational integrity or student-trust risk if shipped wrong |
| **Critical** | Could falsely declare Evidence Platform Ready / corrupt educational authority / launder false learning claims |

---

## 2. Required risk themes

### 2.1 Measurement becomes educational authority (authority inversion)

| Dimension | Assessment |
|---|---|
| **Description** | Teams treat EvaluationRecords, scorecards, or experiment wins as educational SoT; Evidence Platform starts writing missions, progress, Twin, or “correcting” Runtime A. |
| **Technical risk** | **Critical** |
| **Educational risk** | **Critical** |
| **Mitigation** | ADR-MS006-001; read/consume-only; write-guard tests; dependency law Experience → Evidence Platform (one-way) |
| **Verification** | Static import / mutation guards; integration checks |
| **Rollback** | Disable all Evidence Platform flags |

### 2.2 False causation / delivery→outcome invention

| Dimension | Assessment |
|---|---|
| **Description** | Ambiguous linkage upgraded to “Strategy/Adaptive caused improvement”; observational association sold as causal proof. |
| **Technical risk** | High |
| **Educational risk** | **High** |
| **Mitigation** | Linkage strength enum; gate fails overclaim; statistical honesty fields; governance review checklist |
| **Verification** | Fixtures with ambiguous windows must not emit causal promote language |
| **Rollback** | Evaluation non-actionable; Assignment OFF |

### 2.3 SP8 collapse (organisation laundered as learning depth)

| Dimension | Assessment |
|---|---|
| **Description** | Session completion / recovery rates reported as “students learned more” or exam readiness. |
| **Technical risk** | Medium |
| **Educational risk** | **Critical** (EP-004 epistemic distrust) |
| **Mitigation** | Claim-boundary types; scorecard separate blocks; gate `CLAIM_BOUNDARY_LEAKAGE`; narrative constraints |
| **Verification** | Contract tests forbid aliasing organisation → learning_depth |
| **Rollback** | Analytics / Evaluation OFF; correct registry |

### 2.4 Experiment writes / balancing corruption

| Dimension | Assessment |
|---|---|
| **Description** | Assignment logic creates attempts/missions or mutates Twin to balance arms. |
| **Technical risk** | **Critical** |
| **Educational risk** | **Critical** |
| **Mitigation** | Flag-mediated arms only; forbidden write list; Experiment Framework laws |
| **Verification** | Mutation tests on Runtime A / Twin during assignment |
| **Rollback** | Abort experiment; Platform OFF |

### 2.5 Auto-promotion of upstream Authority

| Dimension | Assessment |
|---|---|
| **Description** | Evaluation PASS or experiment “prefer_treatment” automatically flips Adaptive/Strategy Authority. |
| **Technical risk** | High |
| **Educational risk** | **High** |
| **Mitigation** | Governance APPLY owned by humans/upstream; evaluation recommends only; Ready ≠ Authority ON |
| **Verification** | No code path from EvaluationRecord to Authority flag setters |
| **Rollback** | Authority flags OFF independently |

### 2.6 Poly-flag / multi-authority complexity

| Dimension | Assessment |
|---|---|
| **Description** | Twin + Adaptive + Strategy Authority + experiment serve-arm combine into uninterpretable outcomes. |
| **Technical risk** | High |
| **Educational risk** | Medium–High |
| **Mitigation** | Migration principle: no simultaneous multi-authority flip; exposure verification; dimension analytics by flags |
| **Verification** | Composition matrix tests; soak matrices |
| **Rollback** | Disable experiment serve-arm first, then Strategy/Adaptive Authority as needed |

### 2.7 Hidden reasoning / incomplete evaluation explainability

| Dimension | Assessment |
|---|---|
| **Description** | Policy kept without evidence/statistics/rationale/version/confidence disclosure. |
| **Technical risk** | Low–Medium |
| **Educational risk** | **High** (DP-005 / DP-009) |
| **Mitigation** | Five-answer ExplanationBundle + gate |
| **Verification** | Gate unit tests; Reviewer checklist |
| **Rollback** | Decisions without gate PASS treated invalid |

### 2.8 Privacy / cross-student leakage

| Dimension | Assessment |
|---|---|
| **Description** | Traces, exports, or aggregates leak identifiers, raw answers, or cross-student payloads. |
| **Technical risk** | Medium |
| **Educational risk** | Medium (trust); **High** compliance |
| **Mitigation** | Refs not payloads; student scope; redaction levels; quality gate privacy_ok |
| **Verification** | Contract tests; security review before any export audience expansion |
| **Rollback** | Analytics / Platform OFF |

### 2.9 Stale / skewed measurement windows

| Dimension | Assessment |
|---|---|
| **Description** | Outcomes assembled on stale snapshots or biased eligibility; soak looks green falsely. |
| **Technical risk** | Medium |
| **Educational risk** | High |
| **Mitigation** | Freshness codes; exposure verification; limitations mandatory; sensitivity before promote |
| **Verification** | Stale fixtures → gate limitations / fail promote |
| **Rollback** | Expand soak / inconclusive |

### 2.10 Demo / theatrical metrics under promote

| Dimension | Assessment |
|---|---|
| **Description** | Seeded learners or demo markers inflate scorecards used for keep decisions. |
| **Technical risk** | Medium |
| **Educational risk** | **High** |
| **Mitigation** | Demo markers fail quality gate; Alpha checklist |
| **Verification** | Contract tests forbid demo in promote-grade bundles |
| **Rollback** | Invalidate evaluation; Platform OFF |

### 2.11 Feedback loops via analytics→product copy

| Dimension | Assessment |
|---|---|
| **Description** | Evaluation confidence fed into Coach / Home as “learning evidence” theatre (EP-004 failure mode). |
| **Technical risk** | Medium |
| **Educational risk** | **Critical** |
| **Mitigation** | Analytics audience excludes student_coaching; Experience must not consume EvaluationRecords as educational authority |
| **Verification** | Boundary tests: Experience serving path does not import Evidence evaluation as decision input |
| **Rollback** | Remove wiring; Platform OFF |

### 2.12 Performance / measurement path load

| Dimension | Assessment |
|---|---|
| **Description** | Intake/evaluation on request path stacks with Twin+Adaptive+Strategy → latency or DB load. |
| **Technical risk** | Medium |
| **Educational risk** | Low–Medium (abandonment) |
| **Mitigation** | Prefer async/observational off-request assembly; fail open (skip measurement); latency budgets |
| **Verification** | Soak p95; measurement never blocks Start Session |
| **Rollback** | Shadow/Platform OFF |

### 2.13 Premature Evidence Platform Ready / “proven policy” declaration

| Dimension | Assessment |
|---|---|
| **Description** | Ready declared after docs or partial E0–E2; or policies called proven from thin descriptive soak. |
| **Technical risk** | Medium |
| **Educational risk** | **Critical** programme risk |
| **Mitigation** | Migration Ready checklist; architecture stop condition; governance bars; `what_this_does_not_prove` mandatory |
| **Verification** | Readiness report required before Ready; no Ready in this directive |
| **Rollback** | N/A — do not declare Ready |

### 2.14 Transfer / exam overclaim via metrics registry

| Dimension | Assessment |
|---|---|
| **Description** | `transfer` outcomes activated as product claims without separate evidence programme. |
| **Technical risk** | Low |
| **Educational risk** | **Critical** |
| **Mitigation** | Transfer default `not_in_programme`; ADR-MS006-004; governance change class |
| **Verification** | Registry tests; product review |
| **Rollback** | Disable transfer metrics; correct messaging |

---

## 3. Risk by migration phase

| Phase | Top risks | Residual after mitigations |
|---|---|---|
| Docs / review | Premature implementation | Low if stop condition held |
| E0 | Contract drift vs upstream traces | Low |
| E1 | Estimating missing Runtime A; privacy | Medium → Low with gates |
| E2 | SP8 aliasing in analytics | High → Medium with types/tests |
| E3 | Gate bypass / overclaim | Medium → Low |
| E4 | Accidental serve exposure | High → Medium with exposure checks |
| E5 | Fabricated linkage edges | Medium → Low |
| E6 | False confidence from soak | Medium |
| E7 | Poly-flag; auto-promote pressure; Coach feed | High → Medium with checklist |

---

## 4. Educational risk summary

| Theme | Residual posture |
|---|---|
| Authority inversion | Tolerable only if write-guards + ADR hold |
| False learning claims | Highest residual product risk — monitors + SP8 mandatory |
| Experiment integrity | Tolerable if flag-mediated + no educational writes |
| Trust (EP-004) | Measurement must not recreate Coach evidence theatre |

---

## 5. Rollback posture

| Severity | Action |
|---|---|
| Measurement bug / gate noise | Disable Evaluation / Analytics; keep educational serving |
| Exposure violation | Pause Assignment; execute experiment rollback_map |
| Suspected Runtime A corruption from experiment | **Critical stop**; Platform OFF; incident EvaluationRecord; do not “repair” via Platform writes |
| Authority polyphony incident | Disable serve-arm + narrowest upstream Authority first |

Disabling `ENABLE_EVIDENCE_PLATFORM` must restore prior educational behaviour with **zero** dependence on Evidence Platform.

---

## 6. Architecture review gate

PASS architecture review only if this risk analysis is accepted and mitigations are binding for E0+.

---

## 7. Non-claims

This document does not assert that any current Adaptive/Strategy/Twin policy is effective or ineffective. It defines risks of building a measurement platform incorrectly.
