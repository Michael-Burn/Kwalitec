# PX-001 — Screen-by-Screen Review

**Status:** Analysis only. No code changed.
**Evidence:** Live templates in `app/templates/`, routes in `app/*/routes.py` and `app/presentation/**`, and the 70-screenshot `knowledge/reviews/V1_REVIEW_PACKAGE/screens/` set (desktop 1440×900, one dark-theme capture). Screenshot filenames are cited so findings can be re-verified visually.

Legend: **Severity** — Critical / High / Medium / Low. Screens are grouped by feature area in the order a student would encounter them.

---

## 1. Authentication

### 1.1 Sign in — `/auth/login` (`auth/login.html`, `01-login.png`)

- **Works well:** single clear primary action; honest "invite-only" framing; correct dark-panel brand usage.
- **Medium** — Duplicate brand presentation: logo lockup + separate "Kwalitec" headline + two more "Kwalitec coordinator" mentions in one screen (see `PREMIUM_UI_AUDIT.md` §5 for full sign-in audit).
- **Medium** — "Education Operating System" descriptor is jargon-toned for a first-touch screen (see `COPY_REVIEW.md` §1).
- **Low** — Footer shows internal build metadata ("Kwalitec v2.0.0 · Internal Alpha · Founding Cohort · Build RC2") on the public, unauthenticated sign-in screen — appropriate for Alpha, worth revisiting for external pilot framing.

### 1.2 Sign in — invalid credentials (`01b-login-invalid.png`)

- Not directly reviewed in this pass; `login.html` renders WTForms field errors inline (`role="alert"`, lines 90/97), which is the correct accessible pattern. No screen-specific issue identified beyond §1.1.

### 1.3 After logout (`60-after-logout.png`)

- Returns cleanly to Sign in. No issues identified beyond §1.1 (same screen).

### 1.4 Registration

- **Does not exist** (by design — invite-only Alpha). Sign-in copy correctly explains this. No action needed for Stage 1 scope.

---

## 2. Home / Dashboard (the dual-home cluster)

This cluster is the most consequential in the audit; full architecture and PR-001 cross-reference lives in `PR001_ALIGNMENT_REPORT.md`.

### 2.1 Dashboard (legacy) — `/dashboard/` (`dashboard/index.html`, `03-dashboard-legacy.png`, dark: `51-theme-dark.png`)

- **Works well:** clear "Today's Study Session" hero card with one primary CTA; sensible card grouping (Progress, Estimated Knowledge, Recommendations, Exam, Time Status, Study Tip); dark theme renders correctly.
- **Critical** — Shares the page concept "home" with the canonical `/student/` Home under a different chrome, different data source, and the same word "Dashboard" (see §2.2 and `CONSISTENCY_AUDIT.md` §1).
- **Low** — "Estimated Knowledge" and "Progress through Study Plan" both carry a defensive disclaimer explaining what they are *not* ("This is Learning Progress from Study Progress — not Estimated Knowledge"). Good transparency intent, but the pattern repeats near-verbatim on multiple cards/screens (see `COPY_REVIEW.md` §3).

### 2.2 Home (canonical) — `/student/` (`student/home.html`, `04-dashboard-student.png`, Coach panel: `27-coach-panel-on-dashboard.png`, empty: `44-empty-student-home.png`)

- **Works well:** "Today's Mission" hero with duration, one-line reason, one button — this is the strongest single pattern in the product when it renders in its simplest state.
- **Critical** — Page title/nav pill both read "Dashboard" (screenshot `04`), not "Home," even though every internal document (`SCREEN_INVENTORY.md`, `NAVIGATION_AUDIT.md`) calls this route "Home." The label collision with §2.1's "Student Dashboard" is direct and screen-visible, not just an internal-docs mismatch.
- **High** — The hero section's template (`student/home.html` lines 23–314) can stack up to ten conditional copy blocks (greeting, eyebrow, title, status, duration, purpose, "why," "why now," expected benefit, readiness bridge, suggested next action, plan coherence, commitment state, confidence, expected outcome, progress summary) ahead of the CTA depending on flags/state. Only a subset renders in the screenshots captured, but the template supports a materially busier version of this screen than the "Mission" ideal it is meant to express.
- **Medium** — Secondary panels (Readiness, Learning journey, Coach insight, Upcoming milestones, Quick actions) are populated with placeholder/encouragement copy on a new account (`44-empty-student-home.png`) rather than being hidden or condensed until there is real content — acceptable per UX-001 §16 (empty states must explain, not blank) but denser than necessary for a first session.
- **Resolved since capture** — Screenshots `42`, `44`, `54`, and `45` show an "Open Version 2 Learning Experience" link and/or a "Back to Dashboard" footer link on canonical/legacy screens. Both strings were searched in the current `app/templates/` tree and **no longer exist** (confirmed via direct grep, cross-checked against `docs/architecture/PHASE_1_CONSOLIDATION_REPORT.md`, which records their removal). The screenshot package predates this fix — see `PR001_ALIGNMENT_REPORT.md` §2.

### 2.3 Post-login landing (`02-post-login-landing.png`)

- Routes to whichever home is authoritative per `SOLE_RUNTIME`/onboarding state. No screen-specific defect beyond §2.1/§2.2; the redirect itself is the point of friction, not this screen's content.

---

## 3. Daily Mission / Study Session (strength to preserve)

### 3.1 Today's Study Session — `/missions/` (`mission/index.html`, `09-mission.png`)

- **Works well — reference pattern.** Study tip, status badge, topic, "Estimated Time" + "Syllabus coverage" side by side, collapsible "Why you are studying this," explicit "What success looks like today" checklist, recommended activities, one primary CTA, session history below. This is the clearest, most complete explainability pattern in the product and matches PR-001's highest praise (Daily Mission clarity, mean 6.05 Ease of Learning contribution).
- **High** — Shows "Estimated Time: 90 min" for the exact same topic ("Review CS1-A: Descriptive statistics foundations") that Home (§2.2, screenshot `04`) shows as "30 minutes." This is the single clearest, most citable instance of PR-001's #2 friction finding — see `PR001_ALIGNMENT_REPORT.md` §3.
- **Do not change the layout pattern itself** when addressing the duration conflict — the structure is the benchmark other screens should move toward, not away from.

### 3.2 Active Study Session (`33-mission-session.png`)

- Not deeply sampled in this pass; timer/checklist chrome via `study_session.js`. No new issues beyond the duration-source question already logged in §3.1.

### 3.3 Practice Outcome Capture — `mission/session_practice_outcome.html` (`34-mission-practice-outcome.png`)

- **Works well:** clear framing ("These results reflect the answers you recorded... This is not Estimated Knowledge"), simple 4-field form, explicit "I didn't practise today" honest opt-out instead of forcing fabricated numbers.
- **Low** — Three-tier button stack (Record Study Session / didn't-practise-today / Back to Study Session) — acceptable given the choices are genuinely different, but the ghost-styled options are visually close in weight to the primary action.

### 3.4 Study Session Feedback — `mission/session_recorded.html` (`53-mission-session-recorded.png`)

- **Works well — reference pattern for explainability copy.** "What happened today? / What did Kwalitec observe? / What can Kwalitec honestly conclude? / What happens next?" is calm, honest, and non-judgmental even in a "not completed" state ("Nothing from today changes your practice-based guidance"). This is the best-written screen in the product and should inform the Reflection rewrite (see `COPY_REVIEW.md` §5).
- **Low** — Three stacked CTAs again (Continue / Return to Dashboard / Back to Today's Study Session) at the end of a screen whose main job is already done — minor decision load at a point where the student has just finished.

---

## 4. Session Experience (canonical linear flow)

Routes: `/session/<id>/overview → activity → reflection → summary → complete`. No screenshots of the full happy path exist beyond Overview (`35-session-overview.png`); this is a **known gap in the evidence base**, not a claim that the screens do not work.

### 4.1 Session Overview — `session/overview.html`

- **Medium** — Per `KNOWN_LIMITATIONS.md` #12, this surface can show thinner content (placeholder topic labels, "No activities listed") than the equivalent Learning Workspace Mission screen (§3.1) for the same underlying day, because it is served by a different data source (opaque/demo projection vs. real `PlanningService`/SQL `Mission`, per `NAVIGATION_AUDIT.md` §4). This is a UI-visible symptom of a data-architecture gap that this analysis-only programme does not attempt to fix, but it is the direct mechanism behind PR-001's "thin Overview vs. full Session" complaint.
- Template structure itself (`session/overview.html`) is clean: objective, why-studying, learning goal, duration/activities/readiness meta row, topic list, one CTA, timer card. The content-thinness problem is a data-wiring issue surfacing through good UI, not a UI design defect.

### 4.2 Learning Activity — `session/activity.html`

- Not sampled directly; step-bar chrome via `session/base.html`. No new findings beyond the general "Session" stack review.

### 4.3 Reflection — `session/reflection.html`, `session/components/reflection_card.html`

- **High** — The reflection card renders a title ("Reflection"), optional topic/insight/confidence/improvement fields if present, a generic "reflection prompt," an optional free-text note, and a "Continue" button. At no point does it explain *why* reflection matters, what happens to the note, or how it will be used. This directly explains PR-001's lowest category score (Reflection Workflow, mean 4.55/10) — see `PR001_ALIGNMENT_REPORT.md` §4 and `COPY_REVIEW.md` §5 for a rewrite direction modeled on the strong Study Session Feedback pattern (§3.4).
- **Medium** — No nav destination exists for "Reflection" as a concept (confirmed absent from both sidebar trees) — reflection is reachable only as a forced step inside an active session, which reinforces the "forgettable, low-value chore" perception rather than "a valued part of the loop."

### 4.4 Session Summary / Complete — `session/summary.html`, `session/complete.html`

- Not sampled directly in this pass. Flagged for inclusion in a future live-browser pass (see `PREMIUM_UI_AUDIT.md` §3.11 on the evidence gap).

---

## 5. Journey, Revision, History/Analytics (canonical + legacy)

### 5.1 Journey — `/student/journey` (`student/journey.html`, `05-journey.png`, empty: `45-empty-journey.png`)

- **Medium** — Single card ("Overall Progress," a percentage, a progress bar) plus one CTA, followed by 60–70% of viewport height as flat background. Reads as an unfinished page rather than a calm one (see `PREMIUM_UI_AUDIT.md` §3.2). "0% complete" with no supporting context (e.g., "why," "what changes this") on a new account is technically accurate but not reassuring.
- Stale "Back to Dashboard" footer link visible in `45-empty-journey.png` — confirmed removed from current code (see §2.2 resolved note).

### 5.2 Revision — `/student/revision` (`student/revision.html`, `06-revision.png`)

- **Medium** — Same pattern as Journey: one card ("No revision focus yet"), one CTA ("Return Home"), large empty canvas below. Copy itself ("No revision is recommended right now. Keep going with today's session.") is calm and appropriately honest — the issue is purely the amount of unused space around it, not the wording.

### 5.3 History — `/student/history` (`07-history-analytics.png`)

- Not deeply sampled; expected to share the Journey/Revision density pattern based on route family and `SCREEN_INVENTORY.md` description ("Progress over time"). Flagged for the same "sparse canonical shell" pattern as §5.1–5.2.

### 5.4 Analytics (legacy) — `/analytics/` (`analytics/index.html`, `10-analytics-legacy.png`)

- **High** — Six KPI tiles in one row (Estimated readiness, Syllabus coverage, Topics Started, Review Backlog, Day Streak, Study Sessions Done), directly against the product's own "maximum four KPI cards per row" rule (UX-001 §22).
- **High** — On a zero-history account, every chart is a flat line at 0%, every KPI reads 0, and the "Areas for improvement" section uses warning-triangle iconography for statements like "Only studied 0 days — try for at least 5 days" on what may be day one. This reads as reproach, not encouragement, and works directly against the "calm the student" philosophy pillar.
- **Low** — "Weekly Report" export is labelled as a report but downloads as plain text per `KNOWN_LIMITATIONS.md` #14 — not verified against a screenshot in this pass, logged for completeness.

---

## 6. Study Plan

### 6.1 Wizard Step 1 — `/study-plan/wizard/1` (`study_plan/wizard_step_1.html`, `28-wizard-step-1.png`)

- **Works well:** clean 2-column card grid, progress-dot stepper, honest "Not Supported" / "Partially Supported" badges instead of hiding options.
- **Medium** — Presents 8 exam-body cards with equal visual weight when only 1 (IFoA) can currently produce a Version 1 plan, and only 3 papers within IFoA are supported. A student spends attention parsing 7 dead ends before finding the 1 live path. Honest, but not yet "reduce decision fatigue" — the supported path could be visually promoted rather than alphabetically/categorically equal to unsupported ones.

### 6.2 Wizard steps 2–7, Review

- Not captured as distinct screenshots (an active plan short-circuits the wizard in the review environment, per `V1_REVIEW_PACKAGE/REVIEW_PACKAGE_REPORT.md`). No independent findings; inherits the general card/stepper pattern of step 1.

### 6.3 Study Plan view — `/study-plan/<id>` (`study_plan/view.html`, `30-study-plan-view.png`)

- **Works well:** clear roadmap structure by syllabus section with weighting percentages — genuinely useful information architecture for "where am I in the syllabus."
- **Medium** — "Learning Outcomes Not available yet" is repeated verbatim on all 14 topic cards in the screenshot. At roadmap scale this reads as broken/incomplete content rather than a deliberate, single, top-level disclaimer (see `COPY_REVIEW.md` §4).
- **Low** — Per-topic hour estimates carry two-decimal precision ("11.4h," "7.3h," "30.0h") — false precision for what are modelled estimates, not measurements.

### 6.4 Study Plan list / edit (`17-study-plan-list.png`, `31-study-plan-edit.png`, `41-study-plan-list-actions.png`)

- **Medium** — Archive/Delete actions use native browser `confirm()` dialogs per `KNOWN_LIMITATIONS.md` #19, breaking the product's own visual system for its two most destructive actions.

### 6.5 Educational history / calibration — `/calibration/after-plan/<id>` (`calibration/alpha.html`, `32-calibration.png`)

- Not deeply sampled; wizard-style chrome consistent with the plan wizard. No new findings beyond general wizard-family consistency notes in `CONSISTENCY_AUDIT.md`.

---

## 7. Settings, Profile, Account

### 7.1 Settings → General — `/settings/` (`settings/index.html`, screenshots `11`–`15`)

- **Critical (trust/premium violation)** — Surfaces raw build/release engineering data directly to students: Version, Build date, Environment ("development"/"production"), Build number, Commit hash (`<code>{{ release_info.commit }}</code>`), and a numeric `User ID`. None of this serves a student decision; all of it reads as an internal admin panel rather than a premium consumer settings screen. See `COPY_REVIEW.md` §2.
- **Medium** — Settings → Internal Alpha repeats similar build metadata plus "Learning profile status: {{ alpha_status.twin_status }}" — an internal engine-state label ("twin") exposed verbatim to the student.
- **Medium** — "Restore from Backup" uses `onclick="return confirm(...)"` (native dialog) for the single most destructive action in Settings ("This will replace all existing data").
- **Low** — Profile email field is correctly read-only with an explanation ("cannot be changed here") — good pattern, just needs a path forward (contact coordinator), which is documented, but not linked from this specific field.

### 7.2 Profile (canonical) — `/student/profile` (`08-settings-profile-student.png`)

- **High (data/trust visible in UI)** — Screenshot shows "Current Examination: Not set" while the same account's Dashboard and Study Plan clearly show an active IFoA CS1 plan — a direct, screen-visible confirmation of `KNOWN_LIMITATIONS.md` #15.
- **Medium (naming)** — The page renders with H1 "Settings" and highlights the "Settings" nav pill, not a "Profile" pill — the canonical nav has no distinct "Profile" tab despite `SCREEN_INVENTORY.md` describing `/student/profile` as a "Profile" destination reached via "Student top nav." This should be verified against current routing (it may indicate Profile has been folded into Settings, which is a reasonable simplification, but the naming should then be made consistent everywhere it is described).
- **Low** — "Total Study Time: Less than a minute" alongside "Current Examination: Not set" for an account with an active, weeks-old study plan reads as internally inconsistent even before any UI polish — recommend confirming this is a display/caching issue rather than an intended state before Stage 1.

---

## 8. Help, Onboarding, Feedback, Research

### 8.1 Help & Support — `/alpha/help` (`alpha/help.html`, `18-help.png`)

- Full audit in `PREMIUM_UI_AUDIT.md` §6. Summary: **High** — this is a release-info table plus four feedback buttons, not a help centre. No search, topics, FAQ, or contextual guidance.

### 8.2 Onboarding — `/alpha/onboarding` (`alpha/onboarding.html`, `19-onboarding.png`)

- **Works well:** four short, well-written steps ("What Kwalitec is," "How missions work," "Why recommendations are explainable," "How reflection works") — calm tone, no walls of text, honest framing of explainability. One of the better-written screens in the product.
- **Medium** — Step 1 repeats "Education Operating System" again — reinforcing rather than diluting the jargon-tone finding from Sign in (§1.1), since this is the same single source string (`app/brand_identity.py`).
- **Note:** Step 4 ("How reflection works") promises reflection "helps Kwalitec understand how the session felt and keeps tomorrow's guidance honest" — this is exactly the value framing missing from the actual Reflection screen (§4.3). The explanatory copy exists; it simply is not present at the point of the task itself.

### 8.3 Alpha feedback forms — `alpha/feedback_*.html` (`21`–`24`)

- Not deeply sampled; short single-purpose forms per `SCREEN_INVENTORY.md`. Per `KNOWN_LIMITATIONS.md` #17, entry points to these forms are reachable mainly from post-session/Help paths rather than primary navigation — a discoverability note, not a screen-quality defect.

### 8.4 Product Check-in / Thank you — `research/checkin.html`, `research/thank_you.html` (`20-product-checkin.png`, `52-research-thank-you.png`)

- Not deeply sampled in this pass.

---

## 9. Errors, empty, loading, dialogs

### 9.1 404 — `errors/404.html` (`error-404.png`)

- **Works well:** on-brand, calm, one primary + one secondary CTA, correct conditional routing (authenticated → canonical home, anonymous → Sign in).
- **Medium** — "Reference ID" renders in an off-palette pink/magenta monospace colour not found in `tokens.css` or `COLOUR_SPECIFICATION.md` (see `CONSISTENCY_AUDIT.md` §4). No guidance on what to do with the reference ID (e.g., "quote this if you contact support").

### 9.2 403 — `errors/403.html` (`error-403-or-denied.png`)

- Same pattern and same colour issue as §9.1. Copy is clear and non-technical ("You do not have permission to view this page...").

### 9.3 500 (`58-error-500-raw.png`)

- `SCREEN_INVENTORY.md` notes this may render as a raw, unbranded server error rather than the styled `errors/500.html` template depending on failure point — flagged as a residual risk to verify before Stage 1, not confirmed as a current defect in this analysis-only pass.

### 9.4 Empty states (`42`–`49`)

- Legacy empty Dashboard (`42-empty-dashboard.png`) is a genuinely good example of the pattern: clear "Create your study plan" banner CTA, and every card explains why it is empty in its own words rather than showing blank space. This should be the reference pattern.
- Canonical empty states (Journey `45`, Revision implied, Mission `43`, History `47`, Analytics `48`) tend toward the sparser "one card, mostly blank canvas" pattern described in §5.1–5.3.

### 9.5 Loading

- No durable loading screen exists to capture (`KNOWN_LIMITATIONS.md` #20); `tokens.css` implements skeleton primitives correctly (`.skeleton`, `.skeleton--card`, etc., lines 184–249) and `session/overview.html` uses a skeleton card while a session is preparing (line 60) — the mechanism exists and is well-built, but its real-world timing/visibility was not verified in this evidence base.

### 9.6 Dialogs — Welcome modal (`partials/welcome_modal.html`, `54-welcome-modal.png`)

- **Works well:** styled, on-brand modal with a clear primary action and a dismiss option.
- **Resolved since capture** — the underlying dashboard screenshot behind this modal still shows the stale "Open Version 2 Learning Experience" link (§2.2 resolved note); the modal itself is unaffected.
- **Medium** — Native browser `confirm()` dialogs remain the only *other* dialog pattern in the product (Study Plan archive/delete, Settings restore) — the styled welcome-modal pattern exists and works, so extending it to destructive confirmations is a matter of reuse, not new design work.

---

## 10. Desktop vs. mobile

Every screenshot in the evidence base is captured at 1440×900 desktop. **No mobile or tablet screenshots exist** in `V1_REVIEW_PACKAGE/screens/`, and PR-001 reviewers judged the desktop package only. `sidebar.html` and `topnav.html` both implement a collapse/toggle affordance (`data-sidebar-toggle`, backdrop dismiss) consistent with UX-001 §19's "navigation may collapse" guidance, but neither this audit nor PR-001 can confirm real mobile behaviour, breakpoint quality, or touch-target sizing (UX-001 mandates `--touch-target-min: 2.75rem`, defined in `tokens.css` line 127, but not verified in situ). **This is logged as an explicit evidence gap**, not a pass, ahead of a public pilot.
