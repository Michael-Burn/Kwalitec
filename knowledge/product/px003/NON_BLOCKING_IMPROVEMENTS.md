# PX-003 — Non-Blocking Improvements

These are real, code-verified findings that do **not**, individually, meet this review's bar for blocking the Stage 1 external pilot render. They are documented so they are not lost, and so a future implementation programme does not have to re-discover them. None are recommendations to redesign; all are narrow, cite-able gaps against the product's own existing standard.

Ordering is roughly by severity, not by screen.

---

## N1 — Six or more distinct verbs for the same "start/resume a study session" action

Collected across the product: "Start Session" (`app/application/student_experience/dto/home_snapshot.py:25`), "Start Today's Session" (`app/presentation/student/view_models.py:341`), "Start Today's Mission" / "Continue Mission" (`app/application/unified_journey/daily_mission_assembler.py:143-144`), "Start Study Session" (`app/templates/mission/index.html:197`, `app/templates/dashboard/index.html:100`), "Resume Study Session" (`mission/index.html:188`, `dashboard/index.html:96`), "Begin Session" (`app/templates/session/overview.html:52`), "Begin Revision" (`app/templates/student/revision.html:41`). A student moving between Home, Mission, Dashboard (if reached), and Revision encounters a different verb each time for conceptually the same commitment. Low individual friction, but a real, fixable consistency gap against the product's own copy-standardization work in PX-002A.

## N2 — Home hero can still stack up to ~10–14 conditional copy blocks before the primary CTA

`app/templates/student/home.html` contains distinct conditional sections for status, duration, purpose, why-now, expected benefit, readiness bridge, suggested next action, plan coherence, commitment state, confidence, expected outcome, and progress summary (lines ~46–207), most of which are mutually exclusive per state but the template supports stacking a large subset simultaneously. This was flagged by PX-001 as the one place the "Mission" ideal (one heading, one duration, one reason, one button) is not consistently met, and remains structurally true today. Not blocking on its own because the most common single state is materially shorter than the theoretical maximum, but worth a scoped simplification pass.

## N3 — Analytics still shows one-decimal-place hour figures ("11.4h"-style precision)

`app/templates/analytics/index.html:255,356` render `weekly_report.study_hours` / `lifetime.total_hours`, both rounded to one decimal in `app/services/analytics_service.py:404,546`. This is modelled/estimated time, not a stopwatch measurement, and reads as false precision — the same category of issue PX-002B correctly fixed on the Study Plan roadmap (`format_minutes` filter) but did not extend to Analytics.

## N4 — Analytics zero-value KPI tiles use warning/danger text color without new-account framing

Day-streak and review-backlog tiles can render `0` in `text-danger`/`text-warning` (`app/templates/analytics/index.html`, KPI row) with no accompanying "you're just getting started" framing of the kind the "Areas for Improvement" section below already uses correctly for new accounts (`analytics/index.html:322-333`). Inconsistent application of a pattern the same screen already gets right elsewhere.

## N5 — Journey and History populated states are structurally correct but thin on secondary information

`student/journey.html` and `student/history.html` populated states (verified current copy, not the pre-PX-002B placeholder text) are calm and no longer read as broken, but carry limited information density relative to Home/Mission — e.g. Journey topic entries show a title and an optional prerequisite note with no duration or explicit "why this is next." This is a legitimate product-content decision, not a defect; flagged only as a difference in polish level relative to the strongest screens (Mission, Study Session Feedback).

## N6 — Confirmation modal has no explicit `role="dialog"`/`aria-modal` in markup and depends entirely on Bootstrap's runtime injection

`app/templates/partials/confirm_modal.html:14-27` and `app/static/js/confirm-modal.js` rely on Bootstrap 5's `Modal` class to add `role="dialog"`/`aria-modal="true"` at runtime and to provide focus trap/Escape/focus-restore. This currently works, but the JS fails silently (`if (!el || !window.bootstrap) return`, `confirm-modal.js:12`) if Bootstrap's bundle fails to load — a student attempting a destructive action (delete a study plan, restore a backup) would get an inert trigger with no error shown, rather than a broken-but-visible modal. Recommend an explicit fallback or a visible failure state, not a rewrite of the modal itself, which is otherwise correctly built and a genuine improvement over the native `confirm()` dialogs it replaced.

## N7 — "Education Operating System" descriptor remains verbatim across first-touch surfaces

Confirmed still present, unchanged, in `app/brand_identity.py:26` (pinned by `tests/test_px001_brand_identity.py`) and rendered on: sign-in (`auth/login.html:16`), sign-in meta description (`auth_base.html:6`), legacy-shell meta description (`layouts/base.html:6`), Open Graph/Twitter tags (`partials/brand_meta.html:16,21`), the sidebar tagline (`sidebar.html:16`), Settings "About Kwalitec" (`settings/index.html:114`), Onboarding step 1 body (`app/services/alpha_onboarding_service.py:20`), and the PWA manifest description. This was flagged in PX-001 as jargon-toned for a first-touch screen and explicitly deferred as a single-source, low-effort fix; it remains a single-source, low-effort fix today (one constant, eight render sites). Not blocking because it is honest and consistent, not misleading — but it is the most repeated piece of unresolved copy feedback across three programmes and should not be deferred indefinitely.

## N8 — "Internal Alpha · Founding Cohort" framing is still the production-configured identity for what is now an *external* pilot

`render.yaml` sets `KWALITEC_EI_INTERNAL_ALPHA=1` in the deployed environment (comment: "developer daily use — not public"), which renders the "Internal Alpha · Founding Cohort" badge (`app/templates/partials/internal_alpha_badge.html:28-36`) and the invite-only/"contact your coordinator" copy (`auth/login.html:107-116`) to whoever signs in — including, per the render config as reviewed, the intended Stage 1 external pilot cohort. This is flagged as non-blocking rather than blocking because "invite-only pilot" framing may be an intentional and accurate description of Stage 1 itself; but the specific word "Internal" and the flag name (`KWALITEC_EI_INTERNAL_ALPHA`) both describe something narrower than "our first external users," and this discrepancy should be a deliberate product decision, confirmed before render, not an inherited default. Recommend explicit sign-off from whoever owns the Stage 1 pilot definition on whether this badge/copy is correct for the actual pilot cohort — this review cannot determine that from code alone.

## N9 — No visible rate-limiting or lockout messaging on repeated failed logins; no self-service password reset

`app/auth/routes.py` has no rate limiter and no lockout copy; the only recovery path is "contact your coordinator" (`auth/login.html:111-116`). Consistent with an invite-only model and not a UX defect in itself, but worth confirming this is an accepted operational risk for an external (non-developer) user base before Stage 1, since external users are less likely to have a fast support channel than internal staff.

## N10 — `.btn-*:focus` (not `:focus-visible`) rules apply hover-like styling on click, not a distinct keyboard focus ring

`app/static/css/app.css:133-168` — several primary/outline/ghost button states change background/transform on plain `:focus` (which also fires on mouse click), rather than reserving the visual change for `:focus-visible`. Functionally harmless (buttons remain focus-visible-ringed elsewhere via `app.css:127`), but slightly muddies the "keyboard vs. mouse" focus signal the rest of the system correctly separates.

## N11 — `--touch-target-min` token is defined once but not consistently applied

`tokens.css:127` defines a 44px minimum; it is only actually wired to `.form-control, .form-select, .btn` in `app.css:590-592`. Several icon-only interactive controls — the appearance switcher (`app.css:463-465,543-545`), the contextual-help trigger (`app.css:607-609`, ~24px), sidebar nav links, and the canonical student top-nav links — do not reference the token and, by padding-plus-content arithmetic, land noticeably under it, especially at the narrowest breakpoint. Related to blocker B7's touch-target concern but scoped here to elements that were not part of that blocking finding's minimum evidence.

## N12 — Canonical student top navigation does not collapse into a drawer on mobile; it wraps

`app/templates/student/base.html` + `student/components/navigation.html` render a horizontal link row with `flex-wrap` (`student.css:117-121`) rather than the collapse-to-drawer pattern used by the legacy shell (`sidebar.html`/`topnav.html`). This is not necessarily wrong — a short, wrapping nav can be an acceptable mobile pattern — but it means the two shells a student can encounter in one session (see B9) recompose completely differently on the same phone, which is an inconsistency worth a deliberate decision rather than an artifact of two shells evolving independently.

## N13 — `session_practice_outcome.html` eyebrow ("Practice Outcome Capture") reads as internal terminology

Already identified and deliberately deferred by PX-002B as a test-pinned capability name (LXP-003) requiring coordinated engineering + test changes outside a copy-only pass. This review confirms that assessment is still accurate and does not add new urgency to it.

## N14 — Study Session "Finish" is a bare link with no confirmation, inconsistent with the app's own confirm-modal pattern elsewhere

`app/templates/mission/session.html:106-111` — "Finish Study Session" navigates immediately on click with no styled confirmation, unlike the Study Plan archive/delete and Settings restore actions, which now correctly use the shared confirm modal. An accidental tap ends an active session with no undo path. Not blocking because finishing a session is recoverable (data is still recorded up to that point) and is a lower-stakes action than deleting a plan, but it is a real inconsistency in when the product asks "are you sure?"

## N15 — Two structurally different "study session" experiences exist in parallel (`session/*` linear flow vs. `mission/*` flow) with no shared reflection/summary step

The canonical Session Experience (`overview → activity → reflection → summary/complete`) and the Mission flow (`mission/index → session → practice outcome → session_recorded`) are both real, both reachable, and use different verbs, different structures, and different completion semantics (only `session/*` has a "Reflection" step by that name). A first-time student's mental model of "how a study session ends" may not transfer between the two if they experience both. This is an architecture-adjacent observation, not a template-level defect, and this review does not have standing to resolve which flow is authoritative — it is noted here as a scoped, future-programme question, consistent with PX-001's precedent of deferring architecture-scope questions it cannot resolve within a design review.

## N16 — `session/complete.html` exists, is well-written, but the happy path never renders it

`session/summary.html`'s primary CTA ("Return Home") posts directly to `session.finish`, which redirects to Student Home — it does not route through `complete.html`, even though the step navigation (`session/components/navigation.html:3-11`) advertises "Complete" as a fifth step. The screen itself (a reassurance line plus the same completion card) is fine; the step indicator is technically inaccurate for the default path. Low effort to align once someone decides whether `complete.html` should be shown or the step indicator should drop the phantom step.

## N17 — Live mission timer updates with no `aria-live` region

`app/static/js/study_session.js:176-187` updates elapsed time in the DOM every second with no `aria-live`/`role="status"` wrapper — a screen-reader user gets no periodic sense of elapsed time during an active session. Not blocking because the information is supplementary (the session does not depend on the student tracking elapsed time precisely), but a real, easily fixed gap.

## N18 — Internal alpha / research feedback instrumentation is visible on the student-facing Study Session Feedback screen

`app/templates/mission/session_recorded.html:57-73` — "Quick Internal Alpha feedback (optional)" and Product Check-in links sit directly on the screen praised elsewhere in this review as the best-written completion moment in the product. This is arguably intentional and consented-to instrumentation for a pilot cohort, and is clearly labelled as optional, so it is not treated as blocking — but it does visibly dilute what is otherwise the calmest, most confident screen in the product with developer-programme framing, and is worth revisiting once Stage 1's own feedback-collection strategy is decided.

---

Nothing in this document requires a decision before render. Everything in `RELEASE_BLOCKERS.md` does.
