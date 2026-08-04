# OP-001 — Risk Register

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · KSI-003 enrollment failure lessons · Privacy Review · EF-001

**Operational risks only.** Does not authorise product redesign to “mitigate” educational preference risks.

---

## 1. Scoring

| Field | Scale |
|-------|-------|
| Likelihood | L1 Rare · L2 Possible · L3 Likely · L4 Almost certain (without controls) |
| Impact | I1 Low · I2 Moderate · I3 High · I4 Critical (study/trust/safety) |
| Priority | Likelihood × Impact (qualitative: Low / Medium / High / Critical) |

---

## 2. Register

### R-01 — Low recruitment

| Field | Content |
|-------|---------|
| **Risk** | Cannot recruit enough eligible candidates; accepted N stays below 5 |
| **Evidence** | KSI-003: accepted external N = 0; only 3 invite-pending |
| **Likelihood** | L3 |
| **Impact** | I4 (blocks Stage 1 evidence; G1.9 remains NO-GO) |
| **Priority** | Critical |
| **Controls** | Expand selection before send; invite buffer ≥8–12; warm network + referrals; Founder time-box for screening; track funnel daily |
| **Owner** | Founder / operator |
| **Trigger** | Accepted &lt;5 after planned invite window |
| **Response** | Extend recruitment; do not invent N; do not reopen EF; record stop rationale if abandoned |

---

### R-02 — Invites never sent (process stall)

| Field | Content |
|-------|---------|
| **Risk** | Package approved but invites remain pending indefinitely (KSI-003 pattern) |
| **Likelihood** | L3 without checklist discipline |
| **Impact** | I4 |
| **Priority** | Critical |
| **Controls** | Separate Founder **invite-send** decision dated; `OP001_EXECUTION_CHECKLIST.md` Pre-flight + Invite sections; dashboard Invited must move from 0 |
| **Owner** | Founder |
| **Trigger** | &gt;7 days after invite authorisation with Invited = 0 |
| **Response** | Founder escalation; unblock provisioning; or formally revoke authorisation |

---

### R-03 — Participant drop-off / never-activated

| Field | Content |
|-------|---------|
| **Risk** | Accepted students never complete a Session, or go dormant |
| **Likelihood** | L3 |
| **Impact** | I3 (hollow cohort; Active-Evaluable fails later) |
| **Priority** | High |
| **Controls** | Onboarding protocol day-0/7 chase; Reminder template; P1 support for login; do not silently drop inactives from ITT honesty |
| **Owner** | Operator |
| **Trigger** | Never-activated at day 7; dormant ≥14 days |
| **Response** | Support outreach; document; keep ITT counts honest |

---

### R-04 — Exam timing conflict

| Field | Content |
|-------|---------|
| **Risk** | Participants hit exam week and withdraw or pause mid-window |
| **Likelihood** | L2–L3 |
| **Impact** | I2–I3 |
| **Priority** | Medium–High |
| **Controls** | Screen for exam dates; prefer known proximity when possible but do not require it; allow measurement withdrawal without blame; note exam window in limitations |
| **Owner** | Operator |
| **Trigger** | Cluster of withdrawals near known exam dates |
| **Response** | Adjust expectations; do not pressure; preserve evidence honesty |

---

### R-05 — Support overload

| Field | Content |
|-------|---------|
| **Risk** | Founder/operator cannot meet SLAs as cohort grows |
| **Likelihood** | L2 at N≤10; L3 if uncontrolled expansion |
| **Impact** | I3 |
| **Priority** | High |
| **Controls** | Cap concurrent accepted near target 5–10; severity triage; P3 weekly batch; pause new invites if P1 backlog &gt;48h |
| **Owner** | Founder |
| **Trigger** | Open P1 &gt;3 or any P0 uncontained |
| **Response** | Pause invites; Founder surge; temporary access freeze if safety |

---

### R-06 — Privacy incidents

| Field | Content |
|-------|---------|
| **Risk** | Unlawful disclosure, cross-student data visibility, consent mishandling, PII committed to git |
| **Likelihood** | L2 without discipline |
| **Impact** | I4 |
| **Priority** | Critical |
| **Controls** | OR-01 held; consent checkpoints; P0 immediate escalation; no PII in git; identity verify before export/delete; Stage 1 notice attached to invites |
| **Owner** | Founder (Privacy Owner capacity) |
| **Trigger** | Any suspected disclosure or consent without record |
| **Response** | Contain; notify Founder; incident log; pause invites; Privacy Review update if needed |

---

### R-07 — Data loss

| Field | Content |
|-------|---------|
| **Risk** | Loss of enrollment register, consent log, or study evidence |
| **Likelihood** | L2 |
| **Impact** | I3–I4 |
| **Priority** | High |
| **Controls** | Ops store backup; empty evidence tree ready; snapshot dashboard regularly; dual copy of consent log |
| **Owner** | Operator |
| **Trigger** | Missing register or unrestorable backup |
| **Response** | Reconstruct from mail/sent log where possible; disclose missingness; do not fabricate |

---

### R-08 — Negative feedback

| Field | Content |
|-------|---------|
| **Risk** | Strong negative student feedback about usefulness, trust, or bugs |
| **Likelihood** | L2–L3 |
| **Impact** | I2 (ops) / I3 if mishandled into false claims |
| **Priority** | Medium–High |
| **Controls** | Welcome honesty; Q10-style openness in interviews; log negatives in evidence; prefer-lower in later scoring; no defensive redesign under OP-001 |
| **Owner** | Operator / Founder |
| **Trigger** | Repeated P2 trust themes or interview Final Test = No |
| **Response** | Document; EF-001 review only if framework insufficiency evidenced; do not unfreeze for polish |

---

### R-09 — Misunderstood expectations

| Field | Content |
|-------|---------|
| **Risk** | Students expect pass guarantees, public product polish, or paid tutoring |
| **Likelihood** | L3 if copy drifts |
| **Impact** | I3 (trust + withdrawal + claim risk) |
| **Priority** | High |
| **Controls** | Locked templates; Stage 1 invite pack claims discipline; orientation checklist; no marketing language |
| **Owner** | Operator |
| **Trigger** | Support questions implying guarantee / launch |
| **Response** | Correct expectations in writing; update FAQ note; do not change templates toward hype |

---

### R-10 — Consent incomplete but studying

| Field | Content |
|-------|---------|
| **Risk** | Students use product without privacy/measurement consent captured → invalid KPI inclusion or privacy breach of process |
| **Likelihood** | L2 |
| **Impact** | I3–I4 |
| **Priority** | High |
| **Controls** | Acceptance email consent checklist; no numerator inclusion without C1+C2; dashboard note “consent pending” |
| **Owner** | Operator |
| **Trigger** | Activated with consent pending |
| **Response** | Pause KPI tagging; chase consent; exclude from numerators until fixed |

---

### R-11 — Scope creep into product / EF changes

| Field | Content |
|-------|---------|
| **Risk** | Ops pressure becomes UX redesign, package edits, Recommendation/Twin/Runtime changes, or EF unfreeze |
| **Likelihood** | L3 historically for product orgs |
| **Impact** | I3 (violates OP-001 / EF-001 / Content Freeze) |
| **Priority** | High |
| **Controls** | Programme hard constraints; support escalation STOP on algorithm change; EF-001 template |
| **Owner** | Founder |
| **Trigger** | Any PR touching Runtime/Recommendation/Twin/packages under “Early Access” |
| **Response** | Reject scope; open separate programme only if justified |

---

### R-12 — False effectiveness / KSI narration

| Field | Content |
|-------|---------|
| **Risk** | Treating ops readiness, invites sent, or Premium PASS as educational GO or KSI lift |
| **Likelihood** | L2 |
| **Impact** | I4 (governance failure) |
| **Priority** | Critical |
| **Controls** | KSI-003 prefer-lower lessons; OP-001 non-claims; no KSI recalculation in this programme |
| **Owner** | Founder |
| **Trigger** | Draft copy claiming GO / KSI≥80 / V1 released from OP-001 |
| **Response** | Delete claim; reaffirm NO-GO / Pending Evidence until study evidence exists |

---

## 3. Residual acceptance

Early Access with N≈5–10 remains **non-representative**, warm-network biased, and insufficient alone for commercial launch. These residuals are accepted for Stage 1 ops learning — not for Version 1 production-ready declaration.

---

## 4. STOP

Risk controls do not authorise invite send. Founder approval required.

Signed: OP-001 Risk Register · 2026-08-04
