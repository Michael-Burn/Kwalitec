# EP-008.2A — Risk Review (Stage 1 Operational)

**Programme:** EP-008.2A — Stage 1 Operational Readiness  
**Date:** 2026-07-26  
**Status:** Review COMPLETE  
**Canonical risks:** `../p003_3_product_risk_register/`  
**Companion:** [`OPERATIONAL_READINESS_REPORT.md`](OPERATIONAL_READINESS_REPORT.md) gap table OR-01…OR-12  
**Does not:** Close or mutate PR IDs; invent new product features  

---

## 1. Purpose

Answer for the Product Board:

> What operational risks remain for a controlled Stage 1 external pilot, and which block enrollment vs interpretation?

---

## 2. Enrollment-blocking risks (must clear before invites)

| OR | Linked PR / condition | Severity | Current posture | Required control before invite |
|---|---|---|---|---|
| OR-01 | **PR-003** Privacy Review unsigned; EP-004 **C1**; EFF-02 | **Critical** | ACTIVE / OPEN | Signed Privacy Review |
| OR-02 | EP-004 **C2**; EFF-06; Pilot go-live | **Critical** | OPEN | Pilot checklist + dry-run + kill-switch rehearsal |
| OR-03 | Protocol privacy notice | **High** | OPEN | Finalized notice on invite pack |
| OR-04 | Consent capture / BETA_COHORT fields | **High** | Process only | Live capture before measurement inclusion |
| OR-05 | Pilot export/delete owners | **High** | Interim founder | Named owners on activation log |
| OR-06 | **PR-011** / analytics Pilot HOLD | **High** | HOLD | Flag ON authorised **or** manual-measure decision |

**Board line:** Stage 1 **cannot begin safely** while OR-01 or OR-02 remain open. OR-03–OR-06 are High enrollment controls for an honest, supportable pilot.

---

## 3. Active register risks relevant to Stage 1

### 3.1 Still Critical to Version 1 (not Stage 1 start alone)

| PR | Title | Stage 1 implication |
|---|---|---|
| **PR-001** | Educational effectiveness unproven | Pilot collects evidence; does **not** clear by starting |
| **PR-002** | Validated KSI 64 &lt; 80 | Orthogonal to ops start; G1.1 remains FAIL |

### 3.2 High — evidence / adoption chain

| PR | Title | Stage 1 implication |
|---|---|---|
| **PR-006** | External cohort floors unmet | N=0 today; Stage 1 starts path but not C5 N≥20 |
| **PR-007** | Recruitment blocked on privacy | Cleared only when OR-01 done — not a failed campaign |
| **PR-019** | Gate package incompleteness | Unrelated to small pilot start; still blocks C-V1 |
| **PR-020** | G2 EVF not APPROVED for V1 claim class | Do not treat Stage 1 as V1 declaration |

### 3.3 Medium — operate carefully during pilot

| PR | Title | Control during Stage 1 |
|---|---|---|
| **PR-008** | Confidence Medium ceiling | Disclose N; prefer-lower claims |
| **PR-011** | Telemetry overclaim while gated | Align flag state with scorecard method labels |
| **PR-017** | Sparse onboarding / orientation | Week-1 check-ins; no UI redesign in 008.2A |
| **PR-010** | Production load unverified | Acceptable for N 5–10; watch latency if flag ON |
| **PR-013** | Rollback drill packaging | Kill switch rehearsed for Pilot env (OR-02) |
| **PR-023** | CSP / G10 residuals | Accepted residual; monitor security P0 |
| **PR-005** | Cold-start overconfidence | Honesty paths; interview preparedness theme |

### 3.4 Controlled / accepted for invite-only Stage 1

| PR | Title | Why acceptable for Stage 1 |
|---|---|---|
| **PR-004** | Premature V1 declaration | Held by NO GO / claim freezes |
| **PR-015** | Support / commercial unreadiness | Founder-operated OK for N≤10 (OR-10 Low) |
| **PR-016** | Twin marketed while OFF | Enforce flag honesty with cohort |
| **PR-014** | Ship ≠ declare confusion | Explicit: pilot ≠ Version 1 GO |

### 3.5 Watch

| PR | Title | Stage 1 watch |
|---|---|---|
| **PR-018** | Coach/Session naming & Twin trust | Interview codes; no Twin default ON |
| **PR-025** | Second educational brain creep | Experiment Framework hard gate |

---

## 4. Residual risks **after** enrollment clearance

Assuming OR-01…OR-06 closed:

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Low activation (orientation) | Medium | Medium | Week-1 ops; PR-017 watch |
| Measurement consent withdrawal | Low–Medium | Low–Medium | Exclude numerators; keep study access |
| Analytics SEV / backlog | Low–Medium | Medium | Kill switch; runbooks |
| Overclaim from small N | High if undisciplined | High (governance) | Claim Standard; exploratory labels |
| Stage 1 mistaken for educational GO | Medium | Critical | Board script: Stage 1 ≠ C5–C6 |
| Privacy incident | Low | Critical | Pause invites; incident D |

---

## 5. Risks explicitly **not** treated as Stage 1 blockers

| Item | Rationale |
|---|---|
| KSI ≥ 80 (G1.1) | Parallel portfolio; not required to invite |
| Strong-band K2 behavioural rates | Research observation; not enrollment gate |
| Production marketing load test | N 5–10 invite-only |
| Multi-country DPA automation | Prefer single regime; Vision 2030 later |
| Staffed 24/7 support function | Founder rota accepted for Stage 1 |
| UI redesign for orientation | Speculative; out of programme constraints |

---

## 6. Review triggers (re-open this review)

Re-run Stage 1 operational risk review when **any** of:

1. Privacy Review signed (expect OR-01 → closed).  
2. First external invite sent.  
3. First Pilot analytics enable.  
4. P0 / privacy incident.  
5. Educational honesty P1.  
6. Proposal to claim C-EDU or C-V1 from Stage 1 data alone.

---

## 7. Board summary table

| Question | Answer |
|---|---|
| Can Stage 1 start safely today? | **No** — Critical OR-01 / OR-02 open |
| Top operational risks if rushed? | Privacy non-compliance; unconsented measurement; analytics without Pilot hygiene; claim overreach |
| Top risks even after safe start? | Small-N overclaim; onboarding friction; effectiveness still unproven |
| New speculative product work required? | **No** |

---

## 8. Sign-off

| Role | Note | Date |
|---|---|---|
| Product (risk review) | Enrollment HOLD; residual interpretation risks documented | 2026-07-26 |

---

**End of RISK_REVIEW**
