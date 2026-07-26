# Screen Inventory

Every student-visible screen currently reachable in the application. Titles are as shown in the browser when captured.

---

## Authentication

| Route | Title | Purpose | Actions | Navigation |
|---|---|---|---|---|
| `/auth/login` | Sign in | Invite-only sign-in landing | Email, password, Remember me, Sign in; Appearance | Logo → login; no app nav |
| `/auth/logout` (POST) | — (redirect) | End session | Sign out button | Returns to Sign in |

**Registration screen:** does not exist.

---

## Learning Workspace shell

Sidebar: Dashboard · Study Plan · Session · Analytics · Settings · Share Feedback · Help · Sign out.

| Route | Title | Purpose | Actions | Navigation |
|---|---|---|---|---|
| `/dashboard/` | Student Dashboard | Daily decision home | Start/Resume Study Session; Create Study Plan; revision acknowledgement; welcome dismiss | Full sidebar + top bar |
| `/missions/` | Today's Study Session | Today’s mission briefing | Start Study Session | Sidebar |
| `/missions/<id>/session` | Study Session | Active timed session | Tick activities; Pause; Finish; Back | Sidebar |
| `/missions/<id>/session/finish` | Practice Outcome Capture | Record practice results | Submit results; skip/back where shown | Sidebar / session flow |
| `/missions/<id>/session/recorded` | Study Session Feedback | Post-session confirmation | Feedback links; Dashboard; Session | Sidebar links |
| `/analytics/` | Analytics | Charts and weekly report view | View charts | Sidebar |
| `/settings/` | Settings | General / version / support | Open Help; section links | Settings sections + sidebar |
| `/settings/profile` | Settings | Account / research journey | Save profile; Share Feedback | Settings sections |
| `/settings/preferences` | Settings | Appearance + daily goal | Save preferences | Settings sections |
| `/settings/data` | Settings | Export / backup / restore | Export weekly report; Download backup; Restore | Settings sections |
| `/settings/internal-alpha` | Internal Alpha | Alpha status info | Appearance | Settings sections |

---

## Student Experience shell

Top nav (as rendered): Home · Journey · Revision · History · Profile (plus Study Plan / Help when included in the OS nav tree).

| Route | Title | Purpose | Actions | Navigation |
|---|---|---|---|---|
| `/student/` | Home | What to do next + readiness/journey/coach | Start Session; Review journey; quick actions | Student top nav |
| `/student/journey` | Journey | Progress toward exam readiness | Explore / return Home | Student top nav |
| `/student/revision` | Revision | Revision options | Begin revision (when available); Return Home | Student top nav |
| `/student/history` | History | Progress over time | Return Home | Student top nav |
| `/student/profile` | Profile | Exam / preferences / account summary | Open account settings | Student top nav |

---

## Study Plan

| Route | Title | Purpose | Actions | Navigation |
|---|---|---|---|---|
| `/study-plan/` | (redirect) | Active plan → view; else wizard | — | — |
| `/study-plan/wizard/1` | Study Plan | Exam body | Next | Wizard chrome |
| `/study-plan/wizard/2` | Study Plan | Paper / subject + support gate | Next (blocked if unsupported) | Wizard chrome |
| `/study-plan/wizard/3` | Study Plan | Sitting & exam date | Next | Wizard chrome |
| `/study-plan/wizard/4` | Study Plan | Current position / topics | Next | Wizard chrome |
| `/study-plan/wizard/5` | Study Plan | Study minutes & session length | Next | Wizard chrome |
| `/study-plan/wizard/6` | Study Plan | Learning preference | Next | Wizard chrome |
| `/study-plan/wizard/7` | Study Plan | Target grade | Continue to review | Wizard chrome |
| `/study-plan/review` | Study Plan | Confirm plan | Create / cancel | Wizard chrome |
| `/study-plan/<id>` | Study Plan | Plan detail & roadmap | Edit; set active; archive; delete | Sidebar |
| `/study-plan/<id>/edit` | Edit Study Plan (H1) | Edit plan fields | Save; cancel | Sidebar |
| `/study-plan/plans/all` | Study Plan | All plans list | New plan; per-plan actions | Sidebar |
| `/calibration/after-plan/<id>` | Educational history | Post-plan history capture | Continue; Skip beginner; Abandon | Wizard-style |

---

## Session Experience (linear study flow)

These routes are reachable from Home **Start Session** (Session Overview → Begin Session → later steps). Session Overview may show thinner briefing content than Learning Workspace Session (see Known Limitations).

| Route | Title (intended) | Purpose | Actions | Navigation |
|---|---|---|---|---|
| `/session/<id>/overview` | Session Overview | Session objective | Begin | Step bar · brand → Home |
| `/session/<id>/activity` | Learning Activity | Answer / advance activities | Submit answer; Advance | Step bar |
| `/session/<id>/reflection` | Reflection | Guidance checkpoint + optional note | Continue | Step bar |
| `/session/<id>/summary` | Session Summary | Outcomes | Finish | Step bar |
| `/session/<id>/complete` | Complete | Return-home surface | Finish → Home | Step bar |

---

## Alpha / feedback / research

| Route | Title | Purpose | Actions | Navigation |
|---|---|---|---|---|
| `/alpha/onboarding` | Welcome to Kwalitec | Product orientation | Continue; Skip; Help | Sidebar |
| `/alpha/help` | Help & Support | Help centre | Feedback links; Check-in; Onboarding | Sidebar |
| `/alpha/feedback/mission-helpful` | Was this mission helpful? | Mission feedback | Submit; Cancel | Back to Dashboard |
| `/alpha/feedback/explanation-clear` | Was this explanation clear? | Clarity feedback | Submit; Cancel | Back to Dashboard |
| `/alpha/feedback/report-problem` | Report a problem | Problem report | Submit; Cancel | Help |
| `/alpha/feedback/suggest` | Suggest an improvement | Idea capture | Submit; Cancel | Help |
| `/research/checkin` | Product Check-in | Daily reflection questionnaire | Submit; Not now | Sidebar / Help |
| `/research/thank-you` | Thank you | Post check-in confirmation | Return to Dashboard; View Research Journey | Links on page |

---

## Errors

| Route / trigger | Title | Purpose | Actions | Navigation |
|---|---|---|---|---|
| Unknown URL | Page Not Found | 404 | Return to Dashboard / Sign In; Help | Error CTAs |
| Forbidden area (e.g. `/console/` as student) | Access Denied | 403 | Return Home; Help & Support | Error CTAs |
| Unhandled server failure (e.g. Home → Start Session) | Internal Server Error (raw) or branded Error | 500 | Try again / Return home / Report (when branded) | Varies |

---

## Screenshot index

Screenshots live in `screens/`. Key files:

| File | Screen |
|---|---|
| `01-login.png` | Sign in |
| `01b-login-invalid.png` | Sign in with validation error |
| `02-post-login-landing.png` | Post-login landing |
| `03-dashboard-legacy.png` | Student Dashboard |
| `04-dashboard-student.png` | Home (incl. Coach panel) |
| `05-journey.png` | Journey |
| `06-revision.png` | Revision |
| `07-history-analytics.png` | History |
| `08-settings-profile-student.png` | Profile |
| `09-mission.png` | Today's Study Session |
| `10-analytics-legacy.png` | Analytics |
| `11`–`15-settings-*.png` | Settings sections |
| `16`–`17`, `30`–`31` | Study Plan view/list/edit |
| `18-help.png` | Help |
| `19-onboarding.png` | Onboarding |
| `20-product-checkin.png` | Product Check-in |
| `21`–`24-feedback-*.png` | Alpha feedback forms |
| `25-navigation-sidebar.png` | Sidebar navigation |
| `26-navigation-student.png` | Student navigation |
| `27-coach-panel-on-dashboard.png` | Coach on Home |
| `28-wizard-step-1.png` | Wizard step 1 |
| `32-calibration.png` | Educational history |
| `33-mission-session.png` | Active Study Session |
| `34-mission-practice-outcome.png` | Practice Outcome Capture |
| `35-session-overview.png` / `fix-home-start-session-overview.png` | Home → Start Session Overview (working) |
| `35-session-overview-error.png` / `58-error-500-raw.png` | Historical Start Session failure capture (superseded; path works in current app) |
| `42`–`49-empty-*.png` | Empty states |
| `51-theme-dark.png` | Dark appearance |
| `52-research-thank-you.png` | Thank you |
| `53-mission-session-recorded.png` | Study Session Feedback |
| `54-welcome-modal.png` | Dashboard welcome |
| `57-student-session-start-get.png` | Method Not Allowed on GET start |
| `60-after-logout.png` | After logout (Sign in) |
| `error-404.png` | Page Not Found |
| `error-403-or-denied.png` | Access Denied |

**Not included as screenshots (absent or unreliable to capture honestly):** Registration; wizard steps 2–7 as distinct pages while an active plan exists; Session Experience happy-path Overview/Activity/Reflection/Summary/Complete; durable loading screen; styled confirm dialogs.
