# CQ-002 — CRI Intake Assessment

**Programme:** CQ-002 — Core Study Loop Reliability  
**Owner capacity:** Founder — Product Owner  
**Date:** 2026-07-28  
**Authority:** [`TASK_INTAKE_TEMPLATE.md`](../cq001_commercial_readiness/TASK_INTAKE_TEMPLATE.md) · [`COMMERCIAL_READINESS_FRAMEWORK.md`](../cq001_commercial_readiness/COMMERCIAL_READINESS_FRAMEWORK.md)

---

## Task

| Field | Value |
|---|---|
| Task / programme ID | CQ-002 |
| Title | Core Study Loop Reliability |
| Owner capacity | Founder — Product Owner |
| Date | 2026-07-28 |

---

## CRI intake (mandatory)

| Field | Value |
|---|---|
| **CRI domains affected** | **CR1** (primary); **CR2**, **CR5** (secondary, natural only) |
| **Expected CRI increase** | **+2 provisional points** (43% → **45%** provisional) if CR1 rises ~+6–8 and CR2/CR5 move slightly |
| **Founder benefit** | Daily Open → priorities → session → progress → next-step loop runs with fewer dead ends, duplicate “Next” cues, and unnecessary clicks |
| **Release risk** | **Low** — polish/reliability only; no V2 capability; no Twin/recommendation ranking changes; claim class unchanged |

---

## Current CR1 blockers (intake)

| ID | Blocker | Severity | Expected CRI impact | Est. ΔCRI share |
|---|---|---|---|---|
| B-CR1-01a | Extra click: Home “Start” → Session Overview → “Begin” before activity | Critical | Removes commitment friction after start | +0.7–1.0 |
| B-CR1-01b | Dual “Next” on Home (hero MES + Readiness panel, including fallback copy of the same action) | Critical | One primary next-step authority on Home | +0.5–0.7 |
| B-CR1-01c | Empty Home (no mission CTA) has no forward path | Major | Restores “what now?” when mission absent | +0.3–0.4 |
| B-CR1-01d | Session chrome advertises a fifth “Complete” step the happy path never visits | Major | Honest loop progress; fewer “where am I?” moments | +0.2–0.3 |
| B-CR1-01e | Unified-journey “Finish” on Home can be presentation-only with no resume link | Major (flag-gated) | Closes dead-end when journey chrome is on | +0.1–0.2 |
| B-CR1-01f | Profile can show examination “Not set” while plan is active | Major (CR5) | Trust that Profile matches Study Plan | +0.2–0.3 (CR5) |
| B-CR1-01g | CTA verb split (“Start Session” vs “Begin Session”) | Minor | Same commitment language across surfaces | +0.1 |

**Already closed (verified live; not reworked in CQ-002):** duration single-source with `mission_date` (PX-003 B3), session `reflection_note` persistence (PX-003 B1), syllabus-complete ack on Home (RR-001.1).

---

## Priority check

| Question | Answer |
|---|---|
| Is the primary domain at or above current Board priority target? | **Yes** — CR1 is Board #1 |
| If No, is there Founder Review to work lower on the ladder? | N/A |
| Does this introduce Version 2 capability? | **No** |
| If Yes, does it **directly** improve current CRI? | N/A |

---

## Decision

- [x] **Start** — measurable CRI improvement; priority OK  
- [ ] Defer  
- [ ] Stop  

**Scope discipline:** Refinement only. No architecture expansion. No `cri-*` tag on provisional-only movement.

---

**End of CRI Intake**
