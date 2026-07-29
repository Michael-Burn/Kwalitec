# FV-001A — Journey Timeline

**Date:** 2026-07-28  
**Clock:** Wall time from first Playwright capture (~74s automated + follow-up precise pass). Human elapsed for the same path would be ~45–90 minutes with hesitation.

---

## Timeline

| t (approx) | Phase | URL / surface | What happened | Outcome |
|---|---|---|---|---|
| 0:00 | 1 | `/` → `/auth/login` | Read landing + Sign in | Understood student OS pitch |
| 0:02 | 2 | `/auth/register` etc. | All 404 | **Stuck** — no registration |
| 0:05 | 2* | Login with provisioned account | Methodological exception | Entered product |
| 0:06 | 3 | `/console/` | Console Home ops pulse | Confused what to click for CS1 |
| 0:08 | 3→4 | Content / Manage content | Reached Curriculum Studio | Path found |
| 0:10 | 4 | Studio Create Subject | Created **CS1X** | Success flash |
| 0:12 | 4→5 | Open Workspace `ws-cs1x` | Stage Subject → Content Sources | Validation blockers shown |
| 0:15 | 5–6 | Upload dummy PDFs | Files appear; **STATUS Failed** | No trust |
| 0:20 | 7 | Preview / validation | **0 nodes**, checklist incomplete | Cannot review curriculum |
| 0:25 | 8 | Publish click | Refused — needs approval/version | Publish not completed |
| 0:28 | 9 | `/student/`, onboarding, wizard | Welcome + IFoA/CS1 cards | Enrolment partial |
| 0:35 | 10–11 | Student Home Mission | 30 min · Start Session | Action clear; topic unclear |
| 0:40 | 12 | `/session/sess-1/activity` | Free-text “Core methods” activity | Session started; felt hollow |
| 0:50 | 13 | — | Did not reach Reflection/Summary | Incomplete |
| 0:55 | 14 | `/student/revision` | Empty state → return to Mission | Clear |
| 1:00 | 15 | `/alpha/help` | Help, not Coach chat | Coach fail |
| 1:05 | 16 | Logout / login / Home | Auth works; resume weak | Partial continuity |

\*Provisioned login is **not** a product Pass for Phase 2.

---

## Hesitation points (founder behaviour)

1. Stared at login looking for Sign up.  
2. On Console Home, hesitated between Attention Center vs Content.  
3. After Create Subject, hesitated because workspaces still empty.  
4. On upload Failed, would stop and email support.  
5. On Mission “this topic,” would open Explain / Help before studying.  
6. On free-text Core methods prompt, would question product fitness for IFoA.

---

## Paths not taken (ground rules)

- No database inspection  
- No admin CLI during the persona walk (admin was only used to *provision* the invite-style account after Phase 2 failure was documented)  
- No deliberate deep links except natural 404 guesses for register/coach and Content→Studio discovery  

---

## Journey success curve

```
Phase:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Score:  6  2  4  8  4  4  2  3  5  5  4  4  1  7  2  5
```

Peak: Create Subject (8). Troughs: Registration (2), Curriculum Review (2), Session Completion (1), Coach (2).

---

**End of Journey Timeline**
