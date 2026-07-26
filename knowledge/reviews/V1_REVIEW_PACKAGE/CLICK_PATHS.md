# Click Paths

Exact click paths a student uses to reach major features. Arrows mean “student clicks / continues to”.

---

## Sign in → Dashboard

```
Sign in (/auth/login)
↓  enter credentials → Sign in
Dashboard (/dashboard/)
```

If onboarding is required:

```
Sign in
↓
Onboarding (/alpha/onboarding)
↓  Continue or Skip
Dashboard
```

If no study plan:

```
Sign in
↓
Study Plan Wizard step 1
```

---

## Dashboard → Mission → Study Session → Reflection → Dashboard

```
Dashboard (/dashboard/)
↓  Start Study Session
Today's Study Session (/missions/)
↓  Start Study Session
Active Study Session (/missions/<id>/session)
↓  Finish Study Session
Practice Outcome Capture (/missions/<id>/session/finish)
↓  submit results
Study Session Feedback (/missions/<id>/session/recorded)
↓  Dashboard
Dashboard
```

---

## Home → Coach → Journey

```
Home (/student/)
↓  read Coach panel (same page)
Home (Coach insight)
↓  Review journey
Journey (/student/journey)
↓  primary CTA / Back to Dashboard
Home
```

---

## Home → History

```
Home
↓  History (top nav)  — or Quick action “Review Reflection”
History (/student/history)
↓  Home
Home
```

---

## Home → Revision

```
Home
↓  Revision (top nav)
Revision (/student/revision)
↓  Begin revision (when available)  or  Return Home
Home / Session flow
```

---

## Dashboard → Study Plan

```
Dashboard
↓  Study Plan (sidebar)
Active Study Plan view  — or —  Wizard if none
↓  Edit / All plans / New plan
Study Plan list or edit form
```

Create plan from empty Dashboard:

```
Dashboard (no plan)
↓  Create Study Plan
Wizard 1 → 2 → 3 → 4 → 5 → 6 → 7
↓
Review
↓  Create
Educational history
↓  Continue / Skip
Dashboard (+ optional Welcome)
```

---

## Dashboard → Analytics

```
Dashboard
↓  Analytics (sidebar)
Analytics (/analytics/)
```

---

## Any page → Settings

```
Sidebar Settings
↓
Settings General (/settings/)
↓  Profile / Preferences / Data / Internal Alpha
Corresponding settings section
```

From Student Experience:

```
Profile (/student/profile)
↓  Open account settings
Settings (/settings/…)
```

---

## Any page → Help / Feedback

```
Help (sidebar or nav)
↓
Help & Support (/alpha/help)
↓  Report a problem / Suggest / Product Check-in / Onboarding
Feedback form or Check-in
```

Share Feedback shortcut:

```
Share Feedback (sidebar)
↓
Product Check-in (/research/checkin)
↓  Submit
Thank you (/research/thank-you)
↓  Return to Dashboard
Dashboard
```

---

## Appearance

```
Top bar / Sign-in footer → Appearance
↓  Light | Dark | System
Same page (theme changes)
```

---

## Logout

```
Any Learning Workspace page
↓  Sign out (sidebar)
Sign in (/auth/login)
```

---

## Error recovery

```
Unknown URL
↓
Page Not Found
↓  Return to Dashboard / Sign In  or  Help
```

```
Forbidden area (e.g. Console as student)
↓
Access Denied
↓  Return Home / Help
```

---

## Session Experience path (exists; currently fragile)

Intended path from Home:

```
Home
↓  Start Session
Session Overview
↓  Begin
Activity
↓  Advance
Reflection
↓  Continue
Summary
↓  Finish
Complete
↓  Finish
Home
```

**Current behaviour (re-verified):** Home → Start Session opens Session Overview (`/session/<id>/overview`). The Learning Workspace Session path (`/missions/`) still provides the fuller day’s briefing (topic title, why this session, activity checklist). Session Overview may show thinner copy than the Learning Workspace briefing.
