# FV-001B Final — Navigation Audit

**Date:** 2026-07-29  
**Subject:** CS1F  
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
| Docs Ready | Validate | NEXT STEP still “Upload…”; Validate button present | **No** (stale) |
| After validate fail | Fix findings | Flash says review findings; Overview 0 errors | **No** |
| After preview | Approve if ready | Success flash vs not_ready card | **No** |
| After approve fail | Unclear | Publish refusal on Approve | **No** |
| After publish fail | Unclear | Same refusal; Subjects still Content Sources | **No** |

---

## NEXT STEP fidelity

| Workspace state | NEXT STEP text | Faithful? |
|---|---|---|
| Fresh workspace | Confirm subject / advance | Acceptable |
| Both docs Ready, stage Content Sources | Upload Official CMP and Official Syllabus… | **Stale** |
| After Validate refusal | Upload Official CMP and Official Syllabus… | **Stale** |
| After Preview success flash | Upload Official CMP and Official Syllabus… | **Stale** |
| After Approve / Publish refusal | Upload Official CMP and Official Syllabus… | **Stale** |

---

## Action ordering

All of the following appear together on the workspace Actions strip:

- Advance to Next Stage  
- Validate Curriculum  
- Build Preview  
- Approve Curriculum  
- Publish Verified Curriculum  

**Impact:** Navigation of *which* control to press next relies on NEXT STEP + mental model. When NEXT STEP is stale, the Founder must guess. Combined with wrong-verb refusals, this is a critical navigation failure for the happy path.

---

## Subjects hub after publish attempt

| Signal | Visible for CS1F? |
|---|---|
| Ready | No (`Content Sources`) |
| Current Version | Partial (`2026.1`) |
| Published Date | No |

Navigation back to Subjects works; outcome navigation fails because the published state never appears.

---

## Summary

Discoverability of Founder surfaces is strong. **In-workflow next-action navigation fails** from document Ready onward because NEXT STEP, status cards, and action results disagree. That is sufficient to prevent unassisted completion.
