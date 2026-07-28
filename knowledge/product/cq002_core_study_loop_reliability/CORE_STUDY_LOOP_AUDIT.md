# CQ-002 — Core Study Loop Audit

**Programme:** CQ-002 — Core Study Loop Reliability  
**Date:** 2026-07-28  
**Path audited:** Production sole-runtime (`KWALITEC_V2_SOLE_RUNTIME=1`) canonical student journey  
**Method:** Code + template inspection; prior RP-001 / PX-003 / PR-001 evidence; live route/service map

---

## 1. End-to-end journey map

```
Auth login
  → Alpha onboarding (first time)
  → Study Plan wizard (no plan)
  → Calibration
  → Student Home (/student/) — today's priority + primary CTA
  → POST /student/session/start — commitment + session create
  → Session Overview (/session/<id>/overview) — Begin CTA   ← friction
  → Activity → Reflection → Summary → POST finish
  → Home — commitment reflection / day complete / next mission
```

**Parallel / flag-gated paths (not default Alpha):** Unified Journey presentation controls; Runtime C “Mark mission complete”; legacy `/missions/*` (redirected under sole runtime).

---

## 2. Friction inventory

| ID | Friction | Surface | Category | Severity | Notes |
|---|---|---|---|---|---|
| F01 | Home Start creates session then Overview requires a second Begin | Home → Session | Unnecessary click | **Critical** | Student already committed; Overview re-asks |
| F02 | Hero “Next” and Readiness “Next” can both render; readiness falls back to hero text | Home | Inconsistency | **Critical** | Violates single primary next-step feel (DR-050 spirit) |
| F03 | Empty Home: “session will be ready…” with no Journey/Plan link | Home | Empty state / what now? | **Major** | RP-001 Conditional Pass residual |
| F04 | Session step chrome lists Complete; happy path Summary → Home skips it | Session | Inconsistency | **Major** | PX-003 N16 |
| F05 | Unified Journey Finish is presentation-only (no control) when enabled | Home | Workflow break | **Major** | Flag-gated; still a loop dead-end when on |
| F06 | “Start Session” (Home) vs “Begin Session” (Overview) | Home / Session | Inconsistency | **Minor** | PX-003 N1 |
| F07 | Profile examination can read empty while Study Plan has exam | Profile | Trust inconsistency | **Major** | PX-003 B2; CR5 |
| F08 | Home hero can stack many conditional blocks before CTA | Home | Cognitive load | **Minor** | Deferred — structural density; not fixed in CQ-002 |
| F09 | Dual session paradigms (session/* vs mission/*) | Cross | Cohesion | **Minor** | Sole runtime redirects mission hub; architecture deferral |
| F10 | Guided Reflection preview on Home is explicitly non-recording | Home | Placeholder honesty | **Minor** | Already honest; leave as-is |

---

## 3. What already works

- Linear sole-runtime path exists and is certifiable (RP-001 Conditional Pass).
- Commitment confirm / defer / post-session reflection arc wired on V2 finish (RR-001.1).
- Duration resolver is shared and Home bridge passes `mission_date` (B3 closed).
- Session reflection notes persist via runtime port (B1 closed).
- Syllabus-complete acknowledgement restored on Home.

---

## 4. Audit verdict

The core loop is **usable but not yet Strong for CR1**. Critical friction is concentrated at **start handoff** (extra Begin) and **Home next-step cohesion** (dual Next). Closing those plus empty-state forward path and session-step honesty should move CR1 within Emerging toward Strong without expanding Version 1 scope.

---

**End of Core Study Loop Audit**
