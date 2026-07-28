# CQ-003 — CRI Intake Assessment

**Programme:** CQ-003 — Daily Habit Fit  
**Owner capacity:** Founder — Product Owner  
**Date:** 2026-07-28  
**Authority:** [`TASK_INTAKE_TEMPLATE.md`](../cq001_commercial_readiness/TASK_INTAKE_TEMPLATE.md) · [`COMMERCIAL_READINESS_FRAMEWORK.md`](../cq001_commercial_readiness/COMMERCIAL_READINESS_FRAMEWORK.md)

---

## Task

| Field | Value |
|---|---|
| Task / programme ID | CQ-003 |
| Title | Daily Habit Fit |
| Owner capacity | Founder — Product Owner |
| Date | 2026-07-28 |

---

## CRI intake (mandatory)

| Field | Value |
|---|---|
| **CRI domains affected** | **CR2** (primary); **CR1**, **CR5** (secondary, natural only) |
| **Expected CRI increase** | **+2 provisional points** (45% → **47%** provisional) if CR2 rises ~+6–8 and CR1/CR5 move slightly |
| **Founder benefit** | Scarce evening study starts and resumes with lower operational friction — Continue returns mid-session without re-commitment theatre |
| **Release risk** | **Low** — presentation polish only; no V2 habit gamification; no Twin/ranking changes; claim class unchanged |

---

## Current CR2 blockers (intake)

| ID | Blocker | Severity | Expected CRI impact | Est. ΔCRI share |
|---|---|---|---|---|
| B-CR2-01a | Home without Unified Journey still says “Start” when a session is already in progress | Critical | Honest return-to-study language | +0.6–0.8 |
| B-CR2-01b | Resume requires POST start (re-commitment) instead of deep-link into open session | Critical | One-tap interrupt recovery | +0.5–0.7 |
| B-CR2-01c | Resume path still shows start-time MES / commitment density | Major | Lower cognitive load on return | +0.3–0.4 |
| B-CR2-01d | Revision begin lands on Overview (extra click vs Home auto-begin) | Major | Consistent one-click into Activity | +0.2–0.3 |
| B-CR2-01e | Quick action “Resume” points at `/student/` not the open session | Minor | Faster recovery from History/nav habits | +0.1–0.2 |

**Already closed (CQ-002; not reworked):** Home auto-begin to Activity; dual Next suppression; empty Home forward paths; phantom Complete chrome; Finish resume when `session_id` present.

---

## Priority check

| Question | Answer |
|---|---|
| Is the primary domain at or above current Board priority target? | **Yes** — CR2 is Board #2 (next after CQ-002) |
| If No, is there Founder Review to work lower on the ladder? | N/A |
| Does this introduce Version 2 capability? | **No** |
| If Yes, does it **directly** improve current CRI? | N/A |

---

## Decision

- [x] **Start** — measurable CRI improvement; priority OK  
- [ ] Defer  
- [ ] Stop  

**Scope discipline:** Refinement only. No streak/habit gamification. No architecture expansion. No `cri-*` tag on provisional-only movement.

---

**End of CRI Intake**
