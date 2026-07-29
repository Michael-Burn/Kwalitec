# FV-001B Final — Navigation Audit

**Programme:** FV-001B (Final)  
**Release Candidate:** RC-2026.07.29-01  
**Date:** 2026-07-29  
**Subject:** CS1V  
**Evidence:** `_evidence/screenshots/`, `phases.json`

---

## Global navigation

| Destination | Discoverability | Notes |
|---|---|---|
| Subjects | High | Sidebar item #2 |
| Curriculum Studio | High | Sidebar item #3; also from Subjects |
| Review Queue / Publishing / Versions / Quality | High | Sidebar; secondary for this journey |
| Students | Present | Not required for publish path |
| Back to Curriculum Studio | High | Workspace footer link |

**Verdict:** Global navigation is intuitive. Founder environment is recognisable from login onward.

---

## Primary action clarity by phase

| Phase | Expected next action | What UI pointed to | Clear? |
|---|---|---|---|
| Enter Console | Open Subjects / Studio | Sidebar; home CTA is attention queue | Partial |
| Subjects | Create Subject | Create Subject card | Yes |
| After create | Open Workspace | Open Workspace card | Yes |
| After open | Upload CMP + Syllabus | Slots + NEXT STEP | Yes initially |
| Docs Ready | Validate | Validate button present; NEXT STEP still “Upload…” | Partial |
| After validate pass | Build Preview | Build Preview present; Preview ready card | Yes |
| After preview | Approve | Approve Curriculum present + success flash | Yes |
| After approve | Publish | Publish Verified Curriculum present + success flash | Yes |
| After publish | Confirm Ready on Subjects | Subjects row Ready · Version · Date | Yes |

---

## NEXT STEP fidelity

| Lifecycle state | NEXT STEP shown | Faithful? |
|---|---|---|
| Empty workspace | Confirm subject / advance | Yes initially |
| Both documents Ready | Still “Upload Official CMP and Syllabus…” | **No** |
| Validation passed | Same upload copy | **No** |
| Preview ready / approved | Same upload copy | **No** |
| Published | Same upload copy | **No** |
| Subjects hub after Ready | “Open a workspace… or create a subject” | Acceptable for hub |

---

## Dead ends / traps

| Item | Observed? |
|---|---|
| Lost after create | No |
| Wrong upload slot | No |
| Approve returns publish refusal | **No** (cleared vs prior Final) |
| Publish with no Subjects Ready | **No** |
| Cannot return to Subjects | No |

---

## Navigation verdict

Navigation supports a complete Founder publish journey without assistance. Residual weakness is **in-workspace NEXT STEP / stage chrome fidelity**, not discoverability of Subjects or Studio.
