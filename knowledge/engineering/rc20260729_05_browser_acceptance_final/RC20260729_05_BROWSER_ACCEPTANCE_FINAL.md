# RC20260729_05_BROWSER_ACCEPTANCE_FINAL

## Executive Summary

Live Playwright Chromium acceptance was executed against the restarted local Flask process on `http://127.0.0.1:5055` after RC-2026.07.29-04 cleared the stale-template HTTP 500. The previously blocked Student journey phases completed: Study Plan wizard → calibration → Study Session, plus navigation continuity, Founder regression, refresh, responsive, and logout checks.

EOS Student shell continuity held across Home, Choose Exam / study-plan, and Study Session. Founder Console chrome remained separate (no `.student-shell` leakage). No console errors, page errors, or HTTP ≥400 network failures were recorded during the successful run.

Residual Medium findings remain: Student Home content still shows an empty “No exam selected” state after a successful wizard+mission creation (mission/session available on `/missions/`), and Study Session measures a ~5px horizontal overflow at tested viewports.

**Final Recommendation: GO WITH CONDITIONS**

---

## Environment

| Item | Value |
|---|---|
| Base URL | `http://127.0.0.1:5055` |
| Browser | Playwright Chromium (headless) |
| Viewport (desktop) | 1366 × 768 |
| Student account | `rc05.accept2@kwalitec.example` |
| Founder account | `cq008.founder@kwalitec.example` |
| Started (UTC) | `2026-07-29T09:55:51.946797+00:00` |
| Finished (UTC) | `2026-07-29T09:56:16.383182+00:00` |
| Server note | Flask on `:5055` was down at RC-05 start; restarted with the same RC-04 V2 feature flags before evidence collection. **No application code was modified.** |

Evidence artefacts:

- Runner: `_evidence/browser_acceptance/rc20260729_05_playwright_run.py`
- Machine log: `_evidence/browser_acceptance/evidence.json`
- Screenshots: `_evidence/browser_acceptance/0{1-8}_*.png`

---

## Journey Log

Observed main-path sequence (authenticated Student):

1. Login → `/alpha/onboarding` (completed)
2. `/study-plan/wizard/1` — Choose Exam (Step 1)
3. `/study-plan/wizard/2` — When is your exam? (Step 2)
4. `/study-plan/wizard/3` — How much time can you study? (Step 3)
5. `/study-plan/review` — Begin Learning / review
6. `/calibration/after-plan/20` — Confirm your educational history
7. `/dashboard/?welcome=1` — welcome modal → missions hub
8. `/missions/` — Today's Study Session (start CTA)
9. `/missions/23/session` — **Study Session reached**
10. Navigation: Session → `/student/` → `/study-plan/20` → Session
11. Founder: `/console/` → `/console/studio/subjects` → `/console/studio/`
12. Logout → `/auth/login`

Phase 1 checklist (live):

- [x] Step 1 loads
- [x] Step 2 loads
- [x] Step 3 loads
- [x] Review loads
- [x] Calibration loads
- [x] Transition to Study Session succeeds (`/missions/23/session`)

---

## Evidence Summary

| Phase | Screenshot | URL | H1 | `.student-shell` |
|---|---|---|---|---|
| Wizard complete / Home | `01_wizard_complete.png` | `/student/` | Home | True |
| Study Session | `02_study_session.png` | `/missions/23/session` | Study 1.1 Relationship Between Economics And Business — Wednesday, Jul 29 | True |
| Navigation continuity | `03_navigation_continuity.png` | `/missions/23/session` | Study 1.1 … | True |
| Founder Home | `04_founder_home.png` | `/console/` | Home | False |
| Founder Subjects | `05_founder_subjects.png` | `/console/studio/subjects` | Subjects | False |
| Founder Workspace | `06_founder_workspace.png` | `/console/studio/` | Curriculum Studio | False |
| Responsive (tablet) | `07_responsive.png` | `/missions/23/session` | Study 1.1 … | True |
| Logout | `08_logout.png` | `/auth/login` | Sign in | False |

---

## Screenshots

### 01_wizard_complete.png

![01_wizard_complete.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/01_wizard_complete.png)

Captured on `/student/` after wizard + calibration. EOS header/footer present. **Content note:** Home shows “No exam selected yet…” even though study plan 20 and mission 23 were created in the same session (see Issues).

### 02_study_session.png

![02_study_session.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/02_study_session.png)

### 03_navigation_continuity.png

![03_navigation_continuity.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/03_navigation_continuity.png)

### 04_founder_home.png

![04_founder_home.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/04_founder_home.png)

### 05_founder_subjects.png

![05_founder_subjects.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/05_founder_subjects.png)

### 06_founder_workspace.png

![06_founder_workspace.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/06_founder_workspace.png)

### 07_responsive.png

![07_responsive.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/07_responsive.png)

### 08_logout.png

![08_logout.png](/Users/kwalitec/Developer/kwalitec/knowledge/engineering/rc20260729_05_browser_acceptance_final/_evidence/browser_acceptance/08_logout.png)

---

## Study Session Verification

| Check | Result |
|---|---|
| Correct H1 | Yes — `Study 1.1 Relationship Between Economics And Business — Wednesday, Jul 29` |
| EOS shell retained | Yes — `.student-shell` present |
| Navigation correct | Yes — Home · Journey · Revision · History · Settings · Choose Exam · Help |
| Header consistent | Yes — `student-topbar` |
| Footer consistent | Yes — `Reduce decisions. Increase learning.` |
| Typography / spacing / buttons | Consistent with EOS Student chrome in screenshots |
| No visual reset to legacy workspace | Yes — no legacy sidebar chrome observed |
| Session URL under current flag posture | `/missions/23/session` (EOS-hosted mission session; not `/session/<id>/`) |

**Does the Study Session feel like a continuation of the previous pages?**

**YES**

Evidence:

- Home and Session both have `.student-shell = True` and `header = student-topbar`
- Identical footer text on Home and Session
- Same brand mark, appearance switcher, and Sign out control
- Screenshot `02_study_session.png` shows the same top chrome as `01_wizard_complete.png`

---

## Navigation Continuity

Path executed: **Study Session → Student Home → Choose Exam (study-plan/20) → Study Session**

| Check | Result |
|---|---|
| Header unchanged | Yes (`student-topbar` throughout) |
| Navigation unchanged | Yes (same nav labels) |
| Footer unchanged | Yes |
| Active navigation correct | Partial — after return to Session, “Choose Exam” remained highlighted in `03_navigation_continuity.png` (shell unchanged; active-state quirk) |
| No shell change | Yes |
| No identity change | Yes (Kwalitec Student brand retained) |

---

## Founder Regression

| Page | URL | `.student-shell` | Header |
|---|---|---|---|
| Founder Home | `/console/` | False | `console-topbar` |
| Founder Subjects | `/console/studio/subjects` | False | `console-topbar` |
| Founder Workspace | `/console/studio/` | False | `console-topbar` |

| Check | Result |
|---|---|
| Founder chrome intact | Yes — Kwalitec Console / Curriculum Authority |
| Student shell not leaking | Yes |
| Navigation correct | Yes — Console sidebar destinations |
| Branding correct | Yes |
| Layout correct | Yes |

---

## Refresh Behaviour

| Page | Before | After | Auth preserved |
|---|---|---|---|
| Student Home | `/student/` | `/student/` | Yes |
| Choose Exam | `/study-plan/20` | `/study-plan/20` | Yes |
| Study Session | `/missions/23/session` | `/missions/23/session` | Yes |

| Check | Result |
|---|---|
| Session preserved | Yes |
| No logout | Yes |
| No redirect to login | Yes |
| Correct reload | Yes |

---

## Responsive Behaviour

Viewports tested on Study Session: 1366 → 1100 → 900 → tablet (768×1024) → desktop.

| Viewport | scrollWidth − clientWidth | Visible clipping / overlap in screenshot |
|---|---|---|
| 1366 | 5px | No obvious clipping in `02` / `07` |
| 1100 | 5px (measured class) | Not separately shot |
| 900 | 5px (measured class) | Not separately shot |
| Tablet | 5px (measured class) | `07_responsive.png` — layout stacks; chrome readable |
| Desktop restore | 5px | OK |

| Check | Result |
|---|---|
| Navigation adapts | Yes at tablet capture |
| No overlap | No overlap observed in screenshots |
| No clipping | No hard clipping observed |
| No horizontal scroll | **Fail (instrumented)** — ~5px overflow |
| Footer remains correct | Yes |

---

## Logout Behaviour

| Check | Result |
|---|---|
| Sign In page shown | Yes — `/auth/login`, H1 “Sign in” |
| Branding preserved | Yes — Kwalitec Education Operating System split layout |
| Theme preserved | Yes — appearance control present (`System` selected in shot) |
| Footer correct | Yes — Appearance · Internal Alpha · Kwalitec v2.0.0 · Build RC2 |

---

## Console Errors

None detected (no `error` / `warning` console messages; no `pageerror` events).

---

## Network Errors

None detected (no request failures; no HTTP ≥400 responses recorded in the successful run).

---

## Issues

### Issue 1

- **Severity:** Medium
- **Page:** Student Home (`/student/`) after wizard + calibration + mission creation
- **Expected:** Home reflects the active exam / mission after Begin Learning
- **Actual:** Home shows empty state: “No exam selected yet. Choose an exam to begin studying.” while `/missions/` and `/missions/23/session` correctly expose Today’s Study Session
- **Screenshot:** `01_wizard_complete.png`

### Issue 2

- **Severity:** Medium
- **Page:** Study Session (all tested viewports)
- **Expected:** No horizontal overflow (`scrollWidth ≤ clientWidth + 2`)
- **Actual:** `scrollWidth − clientWidth = 5` on `/missions/23/session`
- **Screenshot:** `07_responsive.png`

### Issue 3

- **Severity:** Low
- **Page:** Study Session after navigation return
- **Expected:** Active nav reflects Session / Home appropriately
- **Actual:** “Choose Exam” remained visually active on Session in `03_navigation_continuity.png`
- **Screenshot:** `03_navigation_continuity.png`

### Issue 4 (observational / posture)

- **Severity:** Low (informational)
- **Page:** Session entry
- **Expected:** Under sole-runtime posture, Student Home POST `/student/session/start` is canonical
- **Actual:** Live flag posture entered Study Session via `/missions/` → `/missions/<id>/session`, still under EOS `.student-shell`
- **Screenshot:** `02_study_session.png`

---

## Pass / Fail

| Gate | Status |
|---|---|
| Wizard complete through calibration | Pass |
| Study Session reached | Pass |
| EOS shell continuity (Home ↔ Session) | Pass |
| Navigation continuity (shell) | Pass |
| Founder regression (no Student shell leak) | Pass |
| Refresh preserves auth | Pass |
| Responsive (no horizontal overflow) | Fail (5px) |
| Logout → Sign In | Pass |
| Runtime failures (JS / 5xx) | Pass (none) |

---

## Final Certification Questions

Answered only from observed evidence.

### 1

**Did the Student journey remain inside one consistent application?**

**YES**

Evidence: `.student-shell` + `student-topbar` + identical footer across Home, study-plan, and Study Session. No return to legacy workspace chrome.

### 2

**Did Study Session feel like a natural continuation of Home and Choose Exam?**

**YES**

Evidence: same EOS chrome markers and footer; screenshot comparison `01` ↔ `02`.

### 3

**Did any shell changes occur?**

**NO**

Evidence: `navigation_continuity.shell_retained = true`, `header_unchanged = true`.

### 4

**Did Founder pages remain unaffected?**

**YES**

Evidence: Console chrome on `/console/` family; `.student-shell` false on all three Founder shots.

### 5

**Were any runtime failures encountered?**

**NO**

Evidence: empty console error/warning set; empty page_errors; empty network ≥400 set on the successful run. (Earlier blocked RC-03 500 was already cleared by RC-04 restart; not reproduced here.)

### 6

**Would you certify this Release Candidate for CQ-008 recertification?**

**YES** — with the Medium conditions below tracked into recertification (not blockers for attempting CQ-008 review).

---

## Final Recommendation

**GO WITH CONDITIONS**

Conditions:

1. Track Issue 1 — Student Home empty projection after successful study-plan creation while missions/session are live (content continuity gap under current runtime posture).
2. Track Issue 2 — ~5px horizontal overflow on Study Session.
3. Note Issue 4 — session entry path is `/missions/<id>/session` under the live flag posture; shell continuity still holds.

RC-2026.07.29-03 remaining acceptance phases that were blocked by the stale Flask template process are now executed successfully on the restarted server. Proceed to **CQ-008 Premium Product Recertification** with the conditions above visible to reviewers.
