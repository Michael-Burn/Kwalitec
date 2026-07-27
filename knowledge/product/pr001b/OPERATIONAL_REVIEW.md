# Operational Review — PR-001B

**Programme:** PR-001B — Student Pilot Journey  
**Date:** 2026-07-27  

Assesses empty states, loading, errors, unexpected exits, and session recovery for the Runtime C pilot path.

---

## Empty states

| State | Behaviour | Pilot assessment |
|---|---|---|
| Runtime A student, no insights | Existing empty copy on Home/Journey | Unchanged; coexistence preserved |
| Runtime C, mission open | Full educational panel + complete CTA | Ready |
| Runtime C, mission complete today | Day-complete message + next guidance | Ready |
| Runtime C, syllabus complete | Enrolment completed; experience still projects complete state | Ready (PR-001B load includes completed enrolments) |
| Runtime C artefacts missing | Experience returns `None`; fail-open to Runtime A | Ops issue — Common Issues Guide |

## Loading states

| Path | Behaviour |
|---|---|
| Home/Journey | Synchronous server render; no separate skeleton |
| Mission generate | Idempotent on page load via `ensure_mission` |

**Assessment:** Acceptable for alpha pilot; no premium loading redesign (out of scope).

## Error handling

| Failure | User-facing recovery |
|---|---|
| Complete with missing mission id | Warning flash → Home |
| Mission not found | Warning flash → Home |
| Already completed | Info flash — progress saved |
| Illegal runtime state | Warning with Journey hint |
| Unexpected exception | Warning — try again shortly |
| Runtime C page projection failure | Fail-open to Runtime A (logged) |

## Unexpected exits

| Exit | Recovery |
|---|---|
| Close browser mid-study | Same open mission on return (same day) |
| Logout | Sign in → Home if Runtime C enrolled |
| Double-submit complete | Idempotent recoverable message |

## Session recovery

| Scenario | Result | Certified |
|---|---|---|
| Interrupted same day | Mission remains `generated` | Yes |
| Missed day(s) | Current topic unchanged until complete | Yes |
| Next calendar day after complete | New mission for next topic | Yes |
| Login without StudyPlan | Home (not wizard) when Runtime C enrolled | Yes |

## Gaps accepted for this programme

- No Guided Session / Session Experience write path for Runtime C (intentional pilot model).  
- Revision/History not Runtime C-native.  
- No client-side loading skeleton.

**Operational verdict:** Pilot-complete for first-week independent study with documentation.
