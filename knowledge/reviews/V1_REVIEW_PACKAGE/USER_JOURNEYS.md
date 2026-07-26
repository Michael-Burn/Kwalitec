# User Journeys

Numbered steps for every major student journey in the current product.

---

## 1. First visit

1. Open the application URL.
2. Land on **Sign in** (`/auth/login`).
3. Read the left-hand brand panel (Kwalitec · Education Operating System · “Know exactly what to study next.”).
4. Note the **Internal Alpha · Founding Cohort** badge and the invite-only notice (no public sign-up).
5. Optionally switch Appearance (Light / Dark / System) in the footer.
6. Stop — further use requires credentials from a Kwalitec coordinator.

---

## 2. Registration

**This journey does not exist in the current product.**

1. There is no Register / Sign up link on Sign in.
2. Accounts are created offline by a Kwalitec coordinator.
3. The student receives email and password out of band.
4. The student proceeds to **Login**.

---

## 3. Login

1. Open `/auth/login`.
2. Enter email and password.
3. Optionally check **Remember me**.
4. Click **Sign in**.
5. On failure: remain on Sign in with an error (invalid email/password).
6. On success:
   - If Alpha onboarding is incomplete → Onboarding.
   - If no active study plan → Study Plan Wizard step 1.
   - Otherwise → Student Dashboard (`/dashboard/`).

---

## 4. Dashboard

### Learning Workspace Dashboard

1. Arrive at `/dashboard/` (default home after sign-in).
2. If no plan: see **Create your study plan** and open the wizard.
3. If plan exists: review **Today’s Study Session**, progress, estimated knowledge, recommendations, and timeline.
4. Primary action: **Start / Resume Study Session** → Session list (`/missions/`).
5. Use sidebar to reach Study Plan, Session, Analytics, Settings, Share Feedback, Help, or Sign out.

### Student Experience Home

1. Open `/student/` (nav label **Home**).
2. Read greeting, **Today’s Mission**, duration, and purpose.
3. Review **Readiness**, **Journey**, and **Coach** panels.
4. Review milestones and quick actions.
5. Click **Start Session** when enabled (opens Session Overview; see Known Limitations for thin Overview copy vs Learning Workspace briefing).

---

## 5. Study Session (Learning Workspace path — working daily path)

1. From Dashboard click **Start Study Session**, or open sidebar **Session**.
2. On `/missions/`, read today’s topic, estimated time, success criteria, and recommended activities.
3. Click **Start Study Session**.
4. On the active session screen, tick activities as work proceeds; watch elapsed time.
5. Click **Finish Study Session**.
6. Continue to Practice Outcome Capture.

---

## 6. Mission

1. Open `/missions/` (sidebar **Session**).
2. Confirm status (Pending / In Progress / Completed), date, and topic title.
3. Read “Why you are studying this” and success criteria.
4. Start or resume the session.
5. After finishing, review Session History on the same area when available.

---

## 7. Reflection

Reflection is spread across post-session surfaces (there is no separate “Reflection” sidebar item):

1. Finish the study session.
2. On **Practice Outcome Capture**, enter questions attempted / correct (optional duration and notes).
3. Submit results.
4. Land on **Study Session Feedback**.
5. Optionally open Product Check-in or Alpha feedback forms.
6. Return to Dashboard or Session.

Optional parallel reflection: **Product Check-in** from Share Feedback / Help (~30 seconds).

---

## 8. Journey

1. From Student Experience nav, open **Journey** (`/student/journey`).
2. Review overall progress (may show 0% early).
3. Review current / completed / upcoming topics when present.
4. Use the primary CTA to return toward Home / continue journey.
5. Optionally use **Back to Dashboard** footer link.

---

## 9. Coach

1. Open Home (`/student/`).
2. Locate the **Coach** panel (“Coach insight”).
3. Read the guidance about the highest-value next step.
4. Act on it by starting today’s session or opening Journey.

There is no separate Coach route.

---

## 10. History

1. From Student Experience nav, open **History** (`/student/history`).
2. Review educational progress over time.
3. Return Home via nav or footer.

For chart-heavy history in the Learning Workspace shell, open sidebar **Analytics** (`/analytics/`).

---

## 11. Settings

1. Open sidebar **Settings** (`/settings/`) or Student Experience **Profile** (`/student/profile`).
2. From Profile, optionally **Open account settings**.
3. In Settings, move between General / Profile / Preferences / Data / Internal Alpha.
4. Adjust appearance or daily goal hours → Save.
5. Optionally export weekly report, download backup, or restore from backup (destructive confirm).
6. Return via sidebar.

---

## 12. Logout

1. From the Learning Workspace sidebar, click **Sign out**.
2. Session ends.
3. Land on Sign in (`/auth/login`).
4. Protected URLs now redirect back to Sign in with “Please sign in to continue.”

---

## Supporting journeys

### Create first study plan

1. After login without a plan → Wizard step 1 (or Dashboard empty-state CTA).
2. Complete steps 1–7.
3. Review and create.
4. Complete or skip Educational history.
5. Arrive at Dashboard (welcome may appear).

### Give Alpha feedback

1. Open Help or post-session feedback links.
2. Choose Mission helpful / Explanation clear / Report problem / Suggest improvement.
3. Submit → return to Dashboard or Help.

### Switch theme

1. Use Appearance control (Light / Dark / System) on Sign in footer or signed-in top bar.
2. UI theme updates immediately.
