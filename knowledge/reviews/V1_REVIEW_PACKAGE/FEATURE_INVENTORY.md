# Feature Inventory

Every student-visible capability currently present in Kwalitec. Internal systems are omitted.

---

## 1. Sign in

| | |
|---|---|
| **Purpose** | Authenticate an invited student and open the learning workspace. |
| **Where accessed** | `/auth/login` (also the landing page when signed out). |
| **Typical workflow** | Enter email and password → optional Remember me → Sign in. |
| **Dependencies visible to student** | Valid invite credentials from a Kwalitec coordinator. There is no public sign-up on this screen. |

---

## 2. Sign out

| | |
|---|---|
| **Purpose** | End the signed-in session. |
| **Where accessed** | Sidebar **Sign out** (Learning Workspace). |
| **Typical workflow** | Click Sign out → returned to Sign in. |
| **Dependencies visible to student** | Must be signed in. |

---

## 3. Internal Alpha onboarding

| | |
|---|---|
| **Purpose** | Short product orientation for first-time Alpha participants. |
| **Where accessed** | `/alpha/onboarding` (may appear before the dashboard for new participants); also from Help. |
| **Typical workflow** | Step through orientation → Continue or Skip. |
| **Dependencies visible to student** | Signed-in Alpha account. |

---

## 4. Welcome modal

| | |
|---|---|
| **Purpose** | One-time welcome after plan setup / first dashboard visit. |
| **Where accessed** | Student Dashboard (`/dashboard/`) when welcome is eligible. |
| **Typical workflow** | Read welcome → Start studying / Explore dashboard / dismiss. |
| **Dependencies visible to student** | Signed-in student; welcome eligibility. |

---

## 5. Study Plan Wizard

| | |
|---|---|
| **Purpose** | Create a personal study plan for a chosen exam sitting. |
| **Where accessed** | `/study-plan/wizard/1` … `/wizard/7`, then `/study-plan/review`. Also “Create Study Plan” empty-state CTAs. |
| **Typical workflow** | Choose exam body → paper → sitting/date → current position → weekly minutes → learning preference → target grade → review → create. |
| **Dependencies visible to student** | Supported paper required to finish. Coming Soon / Not Supported subjects show an explanation and block plan creation. |

---

## 6. Educational history (after plan)

| | |
|---|---|
| **Purpose** | Capture prior educational history before entering the workspace, or skip as beginner. |
| **Where accessed** | `/calibration/after-plan/<plan_id>` after plan creation. |
| **Typical workflow** | Confirm history → Continue; or Skip beginner; or Abandon. |
| **Dependencies visible to student** | Newly created (or eligible) study plan. |

---

## 7. Study Plan view / list / edit

| | |
|---|---|
| **Purpose** | Inspect, edit, activate, archive, or delete study plans. |
| **Where accessed** | Sidebar **Study Plan**; `/study-plan/<id>`; `/study-plan/plans/all`; edit form. |
| **Typical workflow** | Open plan → review roadmap → Edit / Set active / Archive / Delete. |
| **Dependencies visible to student** | At least one plan. Roadmap outcomes may show “Not available yet”. |

---

## 8. Student Dashboard (Learning Workspace)

| | |
|---|---|
| **Purpose** | Home view: today’s study session, progress, estimated knowledge, recommendations, exam timeline. |
| **Where accessed** | `/dashboard/` · sidebar **Dashboard**. Default home after sign-in in this release. |
| **Typical workflow** | Review today’s topic → Start / Resume Study Session → optionally open Study Plan or Analytics. |
| **Dependencies visible to student** | Active study plan for full content; otherwise Create Study Plan empty state. |

---

## 9. Home (Student Experience)

| | |
|---|---|
| **Purpose** | Decision screen for “what to do next”: today’s mission, readiness, journey story, coach insight, milestones, quick actions. |
| **Where accessed** | `/student/` · top nav **Home**. |
| **Typical workflow** | Read today’s mission → Start Session (when enabled) → open Journey / Revision / History from nav or quick actions. |
| **Dependencies visible to student** | Signed-in student; mission/readiness/coach panels fill as study evidence accumulates. |

---

## 10. Today’s Mission / Study Session (Session list)

| | |
|---|---|
| **Purpose** | Present today’s focused study objective, success criteria, and recommended activities. |
| **Where accessed** | `/missions/` · sidebar **Session**. Also linked from Dashboard “Start Study Session”. |
| **Typical workflow** | Read briefing → Start Study Session → work → Finish. |
| **Dependencies visible to student** | Active study plan; today’s mission. Empty state prompts plan creation when missing. |

---

## 11. Active Study Session

| | |
|---|---|
| **Purpose** | Timed workspace for today’s topic with activity checklist and finish controls. |
| **Where accessed** | `/missions/<id>/session`. |
| **Typical workflow** | Tick recommended activities → Pause or Finish Study Session. |
| **Dependencies visible to student** | Started mission session owned by the student. |

---

## 12. Practice outcome capture

| | |
|---|---|
| **Purpose** | Record how practice went after the session (questions attempted/correct, optional duration and notes). |
| **Where accessed** | `/missions/<id>/session/finish`. |
| **Typical workflow** | Enter results → submit → continue to session feedback. |
| **Dependencies visible to student** | Finished study session. |

---

## 13. Study session feedback

| | |
|---|---|
| **Purpose** | Post-session confirmation and links into Alpha feedback / Product Check-in. |
| **Where accessed** | `/missions/<id>/session/recorded`. |
| **Typical workflow** | Read confirmation → optionally give feedback → return to Dashboard or Session. |
| **Dependencies visible to student** | Recorded practice outcome (or completed finish path). |

---

## 14. Journey

| | |
|---|---|
| **Purpose** | Show overall progress and topic path toward exam readiness. |
| **Where accessed** | `/student/journey` · top nav **Journey**. |
| **Typical workflow** | Review progress percentage, current/completed/upcoming topics → return Home. |
| **Dependencies visible to student** | Progress fills as sessions and syllabus progress accumulate; may show 0% early on. |

---

## 15. Coach insight

| | |
|---|---|
| **Purpose** | Short coaching message about the highest-value next step. |
| **Where accessed** | Coach panel on `/student/` (Home). Not a separate page. |
| **Typical workflow** | Read insight on Home while deciding whether to start today’s session. |
| **Dependencies visible to student** | Home surface; insight text updates with learning evidence. |

---

## 16. Revision

| | |
|---|---|
| **Purpose** | Adaptive revision options once syllabus progress supports revision work. |
| **Where accessed** | `/student/revision` · top nav **Revision**. |
| **Typical workflow** | Review revision options → Begin revision (when available) or return Home. |
| **Dependencies visible to student** | Revision options may be empty until enough syllabus progress exists. |

---

## 17. History

| | |
|---|---|
| **Purpose** | Educational progress over time (student History surface). |
| **Where accessed** | `/student/history` · top nav **History**. |
| **Typical workflow** | Review history summary → return Home. |
| **Dependencies visible to student** | History fills after sessions and outcomes are recorded. |

---

## 18. Analytics (Learning Workspace charts)

| | |
|---|---|
| **Purpose** | Charts for readiness, mastery, accuracy, hours, missions, reviews, and weekly report data. |
| **Where accessed** | `/analytics/` · sidebar **Analytics**. |
| **Typical workflow** | Open Analytics → inspect charts → return via sidebar. |
| **Dependencies visible to student** | Active plan and study history for populated charts; empty copy when data is missing. |

---

## 19. Profile / Settings (Student Experience)

| | |
|---|---|
| **Purpose** | Summary of exam, preferences, goals, and account; link into full Settings. |
| **Where accessed** | `/student/profile` · top nav **Profile**. |
| **Typical workflow** | Review summary → Open account settings if needed. |
| **Dependencies visible to student** | Signed-in account. |

---

## 20. Settings

| | |
|---|---|
| **Purpose** | General info, profile, appearance/daily goal, data export/restore, Internal Alpha status. |
| **Where accessed** | `/settings/`, `/settings/profile`, `/settings/preferences`, `/settings/data`, `/settings/internal-alpha`. Sidebar **Settings**. |
| **Typical workflow** | Change appearance or daily goal → Save; optionally export weekly report or download/restore backup. |
| **Dependencies visible to student** | Signed-in account. Email is shown read-only. Weekly “PDF” export downloads as plain text. |

---

## 21. Help & Support

| | |
|---|---|
| **Purpose** | Release info and shortcuts into feedback forms and Product Check-in. |
| **Where accessed** | `/alpha/help` · sidebar / nav **Help**. |
| **Typical workflow** | Open Help → Report a problem / Suggest an improvement / Product Check-in / revisit onboarding. |
| **Dependencies visible to student** | Signed-in Alpha participant. |

---

## 22. Product Check-in (Daily Reflection)

| | |
|---|---|
| **Purpose** | Short (~30s) product and study reflection questionnaire. |
| **Where accessed** | `/research/checkin` · sidebar **Share Feedback**; also after sessions / from Help. |
| **Typical workflow** | Answer prompts → Submit → Thank you; or Not now. |
| **Dependencies visible to student** | Signed-in student; some entry points may be gated by eligibility. |

---

## 23. Alpha feedback forms

| | |
|---|---|
| **Purpose** | Capture targeted Alpha feedback. |
| **Where accessed** | `/alpha/feedback/mission-helpful`, `explanation-clear`, `report-problem`, `suggest`. |
| **Typical workflow** | Answer form → Submit → return to Dashboard / Help. |
| **Dependencies visible to student** | Signed-in student. |

---

## 24. Appearance (Light / Dark / System)

| | |
|---|---|
| **Purpose** | Switch visual theme. |
| **Where accessed** | Top bar / auth footer **Appearance** controls. |
| **Typical workflow** | Choose Light, Dark, or System. |
| **Dependencies visible to student** | None beyond browser support. |

---

## 25. Error pages

| | |
|---|---|
| **Purpose** | Explain Page Not Found (404) and Access Denied (403), with return/help links. |
| **Where accessed** | Any invalid or forbidden URL. |
| **Typical workflow** | Read message → Return home / Sign in / Help. |
| **Dependencies visible to student** | None. |

---

## Features that do **not** exist as student pages

| Expected name | Actual situation |
|---|---|
| **Registration / Sign up** | Not available. Login page states invite-only Alpha with no public sign-up. |
| **Coach (standalone page)** | Coach insight exists only as a panel on Home (`/student/`). |
| **Dedicated Reflection page in Learning Workspace** | Post-session reflection is Practice Outcome + Session Feedback (+ optional Product Check-in). A separate Session Experience Reflection step exists under `/session/.../reflection` but starting that path from Home currently fails (see Known Limitations). |
