# MS-004 — Risk Analysis (Student Digital Twin)

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Migration:** `MIGRATION_PLAN_MS004.md`  
**Related:** MS-001 `RISK_ANALYSIS.md`; MS-002 `RISK_ANALYSIS_MS002.md`; MS-003 `RISK_ANALYSIS_MS003.md`

---

## 1. Risk rating scale

| Level | Meaning |
|---|---|
| **Low** | Contained; flag rollback sufficient |
| **Medium** | Trust or performance impact; needs soak / ADR |
| **High** | Educational integrity or student-trust risk if shipped wrong |
| **Critical** | Could falsely declare Twin Ready / corrupt educational authority |

---

## 2. Required risk themes

### 2.1 Twin replaces Runtime A (authority inversion)

| Dimension | Assessment |
|---|---|
| **Description** | Teams treat Twin as educational SoT; Twin estimates overwrite or bypass Evidence / TopicProgress / Missions. |
| **Technical risk** | **Critical** |
| **Educational risk** | **Critical** |
| **Mitigation** | ADR-MS004-001; Twin read-only; Runtime A wins conflicts; architecture gates / reviews; no Twin write APIs |
| **Verification** | Static write guards; integration mutation checks; conflict fixtures |
| **Rollback** | Disable all Twin flags |

### 2.2 Invented mastery / readiness

| Dimension | Assessment |
|---|---|
| **Description** | Twin invents mastery beliefs or readiness maths diverging from Runtime A. |
| **Technical risk** | High |
| **Educational risk** | **High** (DP-008, DP-009) |
| **Mitigation** | Pass-through TopicProgress / ReadinessService; estimate rules deferred (ADR-MS004-004); explainability limitations |
| **Verification** | Golden parity vs ReadinessService / TopicProgress |
| **Rollback** | Authority OFF |

### 2.3 Adaptive owns Twin / feedback loops

| Dimension | Assessment |
|---|---|
| **Description** | Adaptive Engine updates Twin or Twin short-circuits evidence by absorbing Adaptive advice as profile “truth.” |
| **Technical risk** | High |
| **Educational risk** | **High** — opaque self-reinforcing loops |
| **Mitigation** | Consume-only Adaptive attachment; separate flags; Twin updates only from Runtime A triggers |
| **Verification** | Tests: Adaptive output does not change Twin snapshot without new Runtime A evidence |
| **Rollback** | Disable Adaptive Twin-input and/or Twin flags |

### 2.4 Demo Twin under Authority

| Dimension | Assessment |
|---|---|
| **Description** | Seeded readiness (~0.58) / fabricated insights remain when Twin Authority ON. |
| **Technical risk** | Medium |
| **Educational risk** | **High** (EP-004 epistemic distrust) |
| **Mitigation** | Empty authentic contracts; Alpha demo-eradication checklist; dual-run compare |
| **Verification** | Contract tests forbid demo markers under Authority |
| **Rollback** | Authority OFF |

### 2.5 Stale Twin insights

| Dimension | Assessment |
|---|---|
| **Description** | Twin snapshot lags completed session; Profile/Home contradict Journey/History. |
| **Technical risk** | Medium |
| **Educational risk** | **High** |
| **Mitigation** | Freshness windows; recompute-after-completion preference; `stale_snapshot` limitations |
| **Verification** | Complete → Twin assemble includes new attempt or stale flag |
| **Rollback** | Flag off; force recompute |

### 2.6 Explainability failures

| Dimension | Assessment |
|---|---|
| **Description** | Insights shown without TwinExplanationBundle; narrative invents causation. |
| **Technical risk** | Low–Medium |
| **Educational risk** | **High** |
| **Mitigation** | Twin Explainability Gate; fallback; structured refs only |
| **Verification** | TE-1…TE-5; gate unit tests |
| **Rollback** | Authority OFF |

### 2.7 Privacy / governance leakage

| Dimension | Assessment |
|---|---|
| **Description** | Twin DTOs or telemetry include raw answers, cross-student data, or secrets. |
| **Technical risk** | Medium |
| **Educational risk** | Medium (trust); **High** compliance |
| **Mitigation** | Refs not payloads; student scope; telemetry minimal fields; ban event dumps |
| **Verification** | Contract tests on DTO shape; security review before Authority |
| **Rollback** | Flag off |

### 2.8 Narrative contradiction (Journey / History / Twin)

| Dimension | Assessment |
|---|---|
| **Description** | Twin insights invent sessions or contradict History Bridge mission lists. |
| **Technical risk** | Medium |
| **Educational risk** | **High** |
| **Mitigation** | Shared Mission/Attempt ids; Twin must not own timeline; prefer History for session cards |
| **Verification** | Narrative consistency fixtures (MS-002 style) |
| **Rollback** | Twin Authority OFF; History Bridge remains |

### 2.9 Performance

| Dimension | Assessment |
|---|---|
| **Description** | Assembling full Twin on every Home load increases latency / DB load. |
| **Technical risk** | **Medium–High** |
| **Educational risk** | Low directly; Medium if timeouts cause fallback churn |
| **Mitigation** | Caps on attempts/missions; recompute budgets; shadow async where safe; latency telemetry |
| **Verification** | Load tests on History-sized users |
| **Rollback** | Flag off; reduce caps |

### 2.10 V1 / V2 curriculum skew

| Dimension | Assessment |
|---|---|
| **Description** | Twin topic slots break on flat vs hierarchical curricula. |
| **Technical risk** | Medium |
| **Educational risk** | High if topics invented |
| **Mitigation** | CurriculumService only (ADR-003 / ADR-004); dual fixtures |
| **Verification** | V1 + V2 golden learners |
| **Rollback** | Flag off |

### 2.11 Premature estimate / ML promotion

| Dimension | Assessment |
|---|---|
| **Description** | Shipping opaque ML Twin scores as Authority without ADR. |
| **Technical risk** | Medium |
| **Educational risk** | **Critical** for trust |
| **Mitigation** | ADR-MS004-004 gate; registry bans `twin.estimate.*` under Authority until accepted |
| **Verification** | Architecture review checklist |
| **Rollback** | Pin twin_version; Authority OFF |

---

## 3. Phase risks

### T0 — Contracts / ADRs

| Dimension | Assessment |
|---|---|
| Technical | Low |
| Educational | Low |
| Rollback | N/A |

### T1 — Assembler

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — query shapes, V1/V2 |
| **Educational risk** | High if assembler invents readiness/progress |
| **Mitigation** | Pass-through services; forbid local formulae |
| **Rollback** | Unused / flag off |

### T2 — Lifecycle / freshness

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — trigger races vs Evidence Before Completion |
| **Educational risk** | High if Twin updates pre-evidence |
| **Mitigation** | Post-completion ordering invariant; tests |
| **Rollback** | Shadow off |

### T3 — Explainability gate

| Dimension | Assessment |
|---|---|
| Technical | Low |
| Educational | Low if Authority OFF; High if bypassed under Authority |
| Mitigation | Hard gate before Authority serve |
| Rollback | Authority off |

### T4 — Experience cutover

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — DTO mapping |
| **Educational risk** | **High** — demo leakage / wrong insights |
| **Mitigation** | Empty authentic; fallback; soak |
| **Rollback** | Authority OFF |

### T5 — Traceability

| Dimension | Assessment |
|---|---|
| Technical | Low–Medium |
| Educational | Low (observational) |
| Rollback | Flag off |

### T6 — Adaptive Twin-input

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium |
| **Educational risk** | High if Twin required or Adaptive writes Twin |
| **Mitigation** | Fail-open; consume-only; ADR-MS004-003 |
| **Rollback** | Adaptive Twin-input OFF |

### T7 — Soak / Alpha / Ready

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium |
| **Educational risk** | **Critical** if Ready declared with Authority inversion |
| **Mitigation** | DT-1…DT-10 checklist; dual sign-off |
| **Rollback** | All Twin flags OFF |

---

## 4. Residual risks after Twin Ready

| Residual | Notes |
|---|---|
| Classic docs still say “Twin is learner SoT” | Communication risk — MS-004 narrows to derived profile facets |
| Durable Twin store later | ADR-MS004-002 must preserve Runtime A fact primacy |
| Estimate algorithms later | High educational risk until explainable and calibrated |
| Experience still has dual chrome paths | Sole Runtime orthogonal; do not couple |

---

## 5. Risk acceptance for Directive 001

Architecture-only delivery introduces **documentation governance risk** (misread Twin as immediate implementation mandate) — mitigated by explicit stop condition and “no production code” constraint.

**No production educational risk is introduced by this directive** because no implementation artefacts ship.
