# PX-003 — Release Blockers

**Programme:** PX-003 — Independent Release Candidate Design Review
**Reviewer stance:** Independent Head of Product Design / Principal UX Researcher / Accessibility Specialist / Release Approval Reviewer. Not involved in building Kwalitec. No ownership of PX-001/PX-002A/PX-002B decisions. Mandate is to reject if warranted, not to improve.
**Method:** Direct, current-state inspection of `app/templates/**`, `app/static/css/**`, `app/static/js/**`, `app/*/routes.py`, `app/presentation/**`, `app/application/**`, `app/infrastructure/adapters/**`, `render.yaml`, and `tests/presentation/student/test_accessibility.py`. Every item below is cited to a specific file and line, verified against the live code as of this review — not against a prior report's claim of what was fixed. Where a prior programme (PX-001/PX-002A/PX-002B) claimed an item as "Resolved" and this review found it is not resolved, or is only partially resolved, that is stated explicitly.

A "blocker" here means: this defect would, on its own, cause a first-time external Stage 1 student to lose trust, feel confused, feel anxious, encounter an inconsistent or broken workflow, or be excluded from using the product with a keyboard or screen reader — on the canonical path an external pilot student will actually take.

---

## B1 — The Reflection note a student writes is silently discarded, contradicting the screen's own promise

**Screens:** Session Reflection (`/session/<id>/reflection`)
**Category:** Trust / honesty / data integrity

The Reflection card tells the student, verbatim:

> "One minute, closes the loop: this keeps tomorrow's guidance honest and **stays with your session record**."

— `app/templates/session/components/reflection_card.html:10-11`

The form on the same screen collects a free-text "Optional note" (`app/templates/session/reflection.html:12-13`, backed by `reflection_note = StringField(...)` at `app/presentation/session/forms.py:41`). The POST handler for this exact form, `reflection_continue`, calls `continue_reflection(session_id=session_id)` with **no reference to the submitted note anywhere in the call** (`app/presentation/session/routes.py:208-215`; confirmed by grep — `reflection_note` appears nowhere else in `app/` outside the template and the form field definition). `continue_reflection` in `app/presentation/session/views.py:132-134` takes no note parameter either.

**What actually happens:** a student writes a personal reflection, is told it "stays with your session record," submits it, and it is discarded before it reaches any service, database, or downstream recommendation logic.

**Why this blocks release:** this is not a vague tone problem — it is a verifiable, specific factual claim made to a student that is false. It is exactly the class of defect this review's brief calls "unexplained internal language" and "factual contradictions," described by a prior audit as the most trust-damaging pattern in the product. Shipping a screen that lies about what happens to a student's own words to real external students on their first pilot session is not a polish issue; it is a broken promise on the one screen in the product explicitly built to demonstrate honesty ("keeps tomorrow's guidance honest").

**Fix scope (not authorized here):** either wire `reflection_note` through to `continue_reflection`/the reflection persistence path, or remove the "stays with your session record" claim until it is true. This is a small, well-scoped fix, not a redesign.

---

## B2 — A student's own Profile can show "Current Examination: Not set" while every other screen shows an active plan

**Screens:** Profile (`/student/profile`) vs. Dashboard (legacy), Study Plan, Settings → Internal Alpha
**Category:** Trust / data consistency

`student/profile.html:8-12` renders `profile.examination_label or 'Not set'`. That label is sourced exclusively from the Digital Twin projection (`app/application/student_experience/profile_service.py:105-109`), which has at least one path that **hardcodes an empty string** for `examination_label` (`app/infrastructure/adapters/digital_twin/experience_projection.py:390-392`) regardless of whether the student has an active plan.

Meanwhile, the same account's exam is correctly shown from a different, direct source on: the legacy Dashboard (`active_study_plan.exam_name`, `app/templates/dashboard/index.html:88,421`), the Study Plan list (`plan.exam_name`, `app/templates/study_plan/list.html:26`), and Settings → Internal Alpha (`StudyPlanService.get_user_active_plan()`, `app/services/internal_alpha_status_service.py:44-52`).

**Why this blocks release:** this is the single most direct, screen-visible answer to this review's own test question — "would any screen reduce trust?" — that this review found. A student with a live, weeks-old IFoA study plan can open their own Profile and be told, in the same product, in the same session, that no exam is set. This was already flagged as a known limitation before PX-001 and remains unfixed in the code today; three completed design programmes did not close it. It directly damages confidence in every other number the product shows that student, not just this one field.

---

## B3 — Estimated study time is not provably the same number across Home, Mission, and the Study Plan roadmap

**Screens:** Home (`/student/`), Mission (`/missions/`), Study Plan roadmap (`/study-plan/<id>`)
**Category:** Trust / factual consistency

This is the single most cited finding across all three prior programmes (PR-001 → PX-001 → PX-002A). PX-002A unified the *wording* of durations via `app/presentation/formatting.py`, and this review confirms the wording is now consistent in most cases. But this review also confirms the underlying **numbers are still produced by two different call paths**, not one:

- Home's duration flows through `app/infrastructure/adapters/educational_runtime_bridge/recommendation_adapter.py:306-314` (`resolve_planned_session_minutes(plan)` — called **without** `mission_date`).
- Mission's duration flows through `app/services/study_session_service.py:104-121` → `resolve_planned_session_minutes(study_plan, mission_date=mission.mission_date)` in `app/application/student_experience/session_duration.py:15-53` (called **with** `mission_date`, which selects between `weekday_study_minutes` and `weekend_study_minutes`).

When a student has no `preferred_session_minutes` set on their plan, these two call paths can diverge specifically **on weekend days**, because only one of them knows what day it is. Separately, `mission/index.html:67-82` contains its *own* inline fallback chain duplicating this logic in the template rather than calling the shared resolver at all, and formats the result as `"90 min"` while Home formats the same kind of value as `"90 minutes"` / `"1 hour 30 min"` via `formatting.py`. A third, genuinely different number — the per-topic curriculum estimate (`topic.recommended_minutes`, `study_plan/view.html:147-148,204-205`) — can legitimately show a smaller value (e.g. "30 minutes" for a topic) alongside a larger session-length number on Home/Mission (e.g. "90 minutes") for the same day, because they measure different things, with no on-screen explanation of that distinction.

**Why this blocks release:** this is the exact "two different duration numbers for the same fact" failure mode PR-001's twenty simulated reviewers converged on as their top trust complaint, and it is the one item every prior programme explicitly logged as still open pending "a Runtime-A source-of-truth decision." That decision was never made. Shipping to real external students with this unresolved is shipping the product's most-cited trust defect unfixed, three programmes after it was first identified.

---

## B4 — The Welcome modal is a real accessibility trap: `aria-modal="true"` with no focus management

**Screens:** Welcome modal (first-session dialog shown after Study Plan + Calibration, `app/templates/partials/welcome_modal.html`)
**Category:** Accessibility (keyboard, screen reader) / first impression

The modal is marked `role="dialog" aria-modal="true"` (`welcome_modal.html:4`), which tells assistive technology that everything outside it is inert and focus is contained inside it. In reality:

- `app/static/js/app.js:56-97` never moves focus into the modal when it opens (no `.focus()` call on any element inside it on init).
- There is no focus trap — Tab can move focus out of the dialog into content the user is told is inert.
- There is no focus restoration to the triggering element on dismiss.
- `aria-describedby` is absent, so the body copy ("Your study journey is now personalised... Start today's session to begin.") is not programmatically associated with the dialog title for screen readers.

**Why this blocks release:** this is not a peripheral screen — it is the very first modal dialog a new student sees, immediately after completing onboarding and calibration, at the exact moment the product is making its first impression. A keyboard or screen-reader user encounters a component that *claims* to be a proper modal (correct ARIA role) but does not *behave* like one, which is worse for that user than having no ARIA role at all — it actively mispredicts the correct navigation for their assistive technology at first contact.

---

## B5 — The mobile navigation drawer has no focus trap or ARIA state, and is the only way to reach primary navigation below 992px

**Screens:** Sidebar / mobile navigation, present on every screen that uses `layouts/base.html` (Settings, Help, Study Plan, Onboarding)
**Category:** Accessibility (keyboard, screen reader) — Mobile

`app/static/js/app.js:4-53` implements open/close/backdrop-click/Escape/resize-auto-close for the off-canvas sidebar drawer, but:

- The toggle button has only `aria-label="Toggle navigation"` (`app/templates/partials/topnav.html:5-7`) — no `aria-expanded` or `aria-controls`, so assistive technology cannot tell whether the drawer is currently open.
- There is no focus trap once the drawer is open — Tab can move focus behind the backdrop into content that is visually hidden.
- Closing the drawer does not return focus to the toggle button.

**Why this blocks release:** on a phone (≤991.98px), this drawer is the *only* way to reach Settings, Help, and Study Plan navigation for anyone using `layouts/base.html`-based screens. A screen-reader user on mobile who opens it has no reliable way to know it opened, and no guarantee focus stays where the visible UI implies it should. This is squarely inside the brief's explicit "Mobile" and "Keyboard / Screen reader / Focus order" review requirements, and it fails on the exact interaction (opening primary navigation) a mobile student must use on every page.

---

## B6 — A visible navigation label fails contrast so severely it is close to unreadable, on screens real Stage 1 students will actually use

**Screens:** Sidebar section labels ("STUDY", "ACCOUNT," etc. — whatever the deployed section groupings are), present on Settings, Help, Study Plan, Onboarding (`layouts/base.html`-based screens, confirmed still reachable under `SOLE_RUNTIME=1` — see B9)
**Category:** Accessibility (contrast)

`.sidebar .nav-section-label{color:rgba(255,255,255,0.35);...}` on a `#0D1B2A` dark-navy sidebar background (`app/static/css/app.css:51`, background `app/static/css/app.css:43` / `tokens.css` chrome token). Blending 35%-opacity white onto `#0D1B2A` produces an effective foreground of roughly `rgb(97,107,117)` against a `rgb(13,27,42)` background — a contrast ratio well below the 4.5:1 (or even 3:1) WCAG AA thresholds for any text size. This is materially worse than the adjacent `.sidebar-signout` (55% opacity) and `.sidebar-brand-descriptor` (55% opacity) labels on the same page, which are themselves borderline.

**Why this blocks release:** this was flagged as a category-level concern in PX-001's accessibility section but never remediated with a concrete token check. It is not a dead legacy-only style — this review independently confirmed (see B9) that `layouts/base.html` + `partials/sidebar.html` remain the live shell for Settings, Help, Study Plan, and Onboarding even with `KWALITEC_V2_SOLE_RUNTIME=1` set in production. A low-vision student navigating Settings or Help on the actual deployed pilot will encounter this.

---

## B7 — No mobile or tablet screen has ever been rendered and looked at, across three completed design programmes and this review

**Screens:** All — Desktop / Tablet / Mobile is an explicit, named requirement of this review
**Category:** Process / evidence gap that is itself release-blocking

This review confirms, by direct search, that **zero image files exist anywhere under `knowledge/`** (`glob **/*.png|jpg|jpeg|webp|gif` returns nothing), and the screenshot directory referenced by PX-001 (`knowledge/reviews/V1_REVIEW_PACKAGE/screens/`) does not exist in the current tree. Every responsive/mobile finding in PX-001, PX-002A, PX-002B, and this review is, and states itself to be, **CSS and template inspection only** — nobody has opened this product on a phone or tablet, in a real browser or an emulator, at any point in its documented design-review history.

Static analysis in this review independently surfaced concrete, plausible mobile failure candidates that inspection alone cannot confirm or rule out — most importantly `.mission-grid{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}` (`app/static/css/app.css:312`), which can exceed available content width on a 320px-wide phone viewport (iPhone SE class devices) after container padding is subtracted, and the appearance-switcher icon-only buttons at ≤575.98px, whose padding-plus-icon math (`app/static/css/app.css:463-465,543-545`) comes to roughly 34px — short of the ~44px target the product's own `--touch-target-min` token defines (`tokens.css:127`), a token that is in any case not applied to this control at all.

**Why this blocks release:** the review brief explicitly and separately lists Desktop, Tablet, and Mobile as required review surfaces, for a product about to run its *first external pilot* — a population highly likely to include phone usage during study breaks, on the exact commute/break pattern this product's own value proposition targets. Approving a release candidate for that population without a single confirmed live rendering on a real or emulated small screen is not a defensible position for a release-approval reviewer to take, independent of whether the specific candidate defects above turn out to be real once tested. This item is blocking on its own, even if every other item on this list were resolved.

---

## B8 — First-time orientation (Onboarding) is not guaranteed to run on the path a normal external pilot student will actually take

**Screens:** Post-login landing, Onboarding
**Category:** Workflow consistency / "where am I, what should I do next"

The only place `AlphaOnboardingService.should_show(current_user)` is checked and used to redirect a first-time user into onboarding is `dashboard.index` (`app/dashboard/routes.py:114-115`). Under `KWALITEC_V2_SOLE_RUNTIME=1` (the production configuration per `render.yaml:45-47`), a successful login instead routes directly to `canonical_home_url()` → `student.home` (`app/auth/routes.py:46`, `app/presentation/consolidation.py:35-36`), and `student.home`'s own route (`app/presentation/student/routes.py:78-119`) contains no equivalent onboarding-gate check.

**Why this blocks release:** onboarding is the one screen in the product this review found to be genuinely well-written and specifically designed to answer this review's own release-blocking questions ("What Kwalitec is," "How missions work," "Why recommendations are explainable," "How reflection works" — `app/templates/alpha/onboarding.html`, praised in PX-001 as one of the better-written screens). If the production login path does not reliably route a brand-new external student through it, that student's very first screen is Home in whatever state it happens to be in (see B10 for how dense that can be) with no orientation at all — for a product whose central design philosophy is explaining "why" before asking for trust.

---

## B9 — A different, legacy Settings experience remains fully reachable and un-redirected under the production flag configuration

**Screens:** `/settings/` (legacy shell) vs. the canonical Profile/Settings surfaces
**Category:** Workflow inconsistency

`app/dashboard/routes.py`, `app/analytics/routes.py`, and `app/mission/routes.py` all correctly redirect their legacy index routes to canonical equivalents when `SOLE_RUNTIME=1` (confirmed via `redirect_if_sole_runtime(...)` calls at `app/dashboard/routes.py:117-119`, `app/analytics/routes.py:26-28`, `app/mission/routes.py:239-241`). **`app/settings/routes.py:81-85` has no equivalent guard** — `GET /settings/` renders `settings/index.html` unconditionally, using the legacy `layouts/base.html` shell and sidebar, in the same session where the canonical nav points to `student.profile` for the same concept (`app/templates/partials/sidebar.html:46-48`).

**Why this blocks release:** this is a live, reachable duplicate-experience path of exactly the kind PR-001 and PX-001 identified as the product's single most critical finding for the *Home* screen (two "Dashboard" concepts) — and it was supposedly closed by PX-002A for Home/Analytics/Mission, but the same class of gap remains open, unnoticed, for Settings. A student who reaches `/settings/` via an old link, browser autocomplete, or a support-ticket screenshot gets a visually and structurally different settings experience (including the contrast failure in B6 and the exposed internal-status label in B10) than the one the canonical nav sends them to.

---

## B10 — Internal engine-state language ("Learning profile status") remains directly exposed to any logged-in student

**Screens:** Settings → Internal Alpha (`/settings/`)
**Category:** Trust / unexplained internal language

`app/templates/settings/index.html:327-329` renders a field labelled "Learning profile status" whose value is `alpha_status.twin_status` — an internal Digital Twin engine-state field, mapped to student-readable strings ("Ready," "Not yet set up," etc. per `app/services/internal_alpha_status_service.py:67-79`) but still surfaced under a label ("Learning profile status") that describes an internal system concept ("profile"/twin readiness), not a student concern. The route rendering this (`/settings/`, confirmed reachable per B9) is not admin- or flag-gated — any authenticated student can view it, not only internal alpha testers, despite the section header "Internal Alpha."

**Why this blocks release:** this is precisely the category of finding ("unexplained internal engine-state labels reaching students") that PX-001 identified as one of the two most trust-damaging defect classes in the product (alongside the duration contradiction), explicitly targeted for remediation by PX-002A's "diagnostics disclosure" work — and the disclosure pattern was correctly applied to build/commit/user-ID metadata, but this specific field was left outside it, in a section that any student — not just alpha participants — can currently open.

---

## Summary

| # | Finding | Screens affected | Category |
|---|---|---|---|
| B1 | Reflection note collected but never saved, contradicting on-screen promise | Session Reflection | Trust / honesty |
| B2 | Profile shows "Not set" exam while other screens show an active plan | Profile vs. Dashboard/Study Plan/Settings | Trust / data consistency |
| B3 | Duration numbers can still diverge across Home / Mission / Study Plan | Home, Mission, Study Plan | Trust / factual consistency |
| B4 | Welcome modal claims `aria-modal` with no focus management | Welcome modal (first session) | Accessibility |
| B5 | Mobile nav drawer has no focus trap / ARIA expanded state | All `layouts/base.html` screens, mobile | Accessibility / Mobile |
| B6 | Sidebar section-label contrast is far below WCAG AA | Settings, Help, Study Plan, Onboarding | Accessibility |
| B7 | Zero mobile/tablet screens have ever been rendered and reviewed live | All | Process / evidence gap |
| B8 | Onboarding not guaranteed on the production login path | Post-login landing | Workflow / orientation |
| B9 | Legacy `/settings/` reachable and un-redirected under production flags | Settings | Workflow inconsistency |
| B10 | "Learning profile status" internal label exposed to any student | Settings → Internal Alpha | Trust / jargon |

None of these ten items require a redesign. Each is a specific, cited, fixable defect. But each independently answers one of this review's release-blocking questions in the negative for at least one real screen a Stage 1 external student will reach, and B7 is blocking as a matter of missing evidence regardless of any individual code fix.
