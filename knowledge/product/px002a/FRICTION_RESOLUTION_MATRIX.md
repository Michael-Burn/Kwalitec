# PX-002A — Friction Resolution Matrix

**Programme:** PX-002A — Trust & Friction Resolution
**Input:** `knowledge/product/px001/HIGH_PRIORITY_BACKLOG.md` (14 items: T1-1–T1-4, T2-1–T2-10)
**Rule:** Every backlog item is accounted for below as **Resolved**, **Partially Resolved**, **Deferred**, or **Rejected** — nothing disappears silently.

---

## Tier 1 — Cohesion & trust (mandatory)

### T1-1. Resolve the shared "Dashboard" label across both navigation stacks

**Status: Resolved**

- Canonical Student Experience home and history now render **"Home"** and **"History"** — no longer "Dashboard" / "Analytics" — independent of `SOLE_RUNTIME` state.
- Changed: `app/domain/student_experience/experience_workspace.py` (`SURFACE_LABELS`), `app/presentation/product_language.py` (`STUDENT_NAV_LABELS`), `app/presentation/student/view_models.py` (page titles), `app/templates/partials/sidebar.html`, plus CTA labels in `mission/session_recorded.html`, `research/thank_you.html`, `alpha/onboarding.html`, `study_plan/view.html`.
- The **legacy** Learning Workspace home (`dashboard/index.html`, gated off when `SOLE_RUNTIME=1`) still says "Dashboard." Per T1-1's own recommended solution — "retire 'Dashboard' as the label for **this screen** [the canonical home]" — the collision that PR-001's reviewers actually hit (both homes calling themselves "Dashboard" in the *same session*) is removed. Renaming the legacy screen too was out of scope: it is a structurally different, pre-`SOLE_RUNTIME` surface, and T1-4 already confirms production never renders it.
- Tests updated: `tests/presentation/student/test_navigation.py`, `test_routes.py`, `test_view_models.py`, `test_terminology.py`, `tests/presentation/workflows/test_workflow_consistency.py`, `test_workflow_student_session.py`, `tests/application/unified_journey/test_navigation.py`, `test_feature_flags.py`.

### T1-2. Establish one authoritative session-duration label

**Status: Resolved**

- Created `app/presentation/formatting.py` — one shared module (`format_minutes`, `format_duration_estimate`, `format_remaining_minutes`) — as the single formatting authority for study-duration wording.
- `app/presentation/session/view_models.py` and `app/presentation/student/view_models.py` now format every duration through this shared module rather than ad hoc per-view-model string building.
- This resolves the *wording* half of T1-2 directly (one phrase style, one rounding rule, everywhere a duration is rendered) as scoped: T1-2's own recommended solution separates a **content/consistency decision** (in scope here) from **the deeper two-computation architecture** (`SOURCE_OF_TRUTH_ANALYSIS.md` — explicitly flagged by PX-001 as "a separate, larger effort outside this programme's scope").
- **Partially Resolved** on the *numeric* half: if Home's plan-derived estimate and Mission's engine estimate still compute different minute counts for the same topic, they will now be *worded* identically but could still *disagree numerically*. Closing that requires picking one authoritative data source per `SOURCE_OF_TRUTH_ANALYSIS.md`, which is a Runtime A/data-model decision explicitly excluded by this programme's "No Runtime A changes" constraint. Logged as Technical Debt.

### T1-3. Add value framing to the Reflection screen

**Status: Resolved**

- `app/templates/session/components/reflection_card.html` now carries a value-framing sentence (reusing the tone already proven in Onboarding step 4 / Study Session Feedback) at the point reflection is submitted — not only in onboarding, days earlier.
- Accessibility defect found while implementing this item was also fixed: `student-reflection-controls` on `student/home.html` were previously styled as buttons with `role="status"` despite being presentation-only preview text; both the button styling and the incorrect role were removed in favour of plain, correctly-semantic text (new `.student-reflection-preview` CSS class in `app/static/css/student/student.css`).

### T1-4. Confirm no non-production dual-home exposure ahead of Stage 1

**Status: Resolved (operational verification, no code change)**

- Verified `render.yaml` sets `KWALITEC_V2_SOLE_RUNTIME=1` for the Render production service (line ~46), confirming the canonical single-home experience is what Stage 1 pilot participants will reach.
- Verified `.env.example` documents `KWALITEC_V2_SOLE_RUNTIME` as an explicit opt-in (commented out by default), meaning local/dev/CI environments default to dual-run unless a developer opts in — this is expected and does not affect the production/pilot path.
- This item was explicitly scoped by PX-001 as "not a code change — an operational verification," and no code change was made for it. If any future environment (support demo, QA) is used with a real or prospective student, this file should be re-checked before that session.

---

## Tier 2 — Premium polish (implemented where they naturally fell within scope)

### T2-1. Remove technical/build metadata from student-facing Settings

**Status: Resolved (Settings) / Partially Resolved (footer badge)**

- `app/templates/settings/index.html`: build date, environment string, build number, commit hash, and raw user ID (General and Internal Alpha sections) moved into a collapsed `<details>` "Diagnostic information" disclosure, used only if a student is asked for it by support. Build number and application version also moved out of the plain "Internal Alpha Status" block into the same disclosure pattern.
- A separately-noted duplicate appearance/theme switcher (`CONSISTENCY_AUDIT.md` §6) was identified but **not** removed — see `CONSISTENCY_DECISIONS.md` Decision 6 for why (it is pinned by two existing tests and not itemised in this backlog).
- The "Build RC2" badge in the footer/topnav brand chrome was **not** removed — it is an intentional, tested brand element (`tests/test_bi001_brand_identity.py`) rather than a stray debug artefact, and removing it was outside this item's described scope ("Settings, Internal Alpha sections," `alpha/help.html`). Logged as Partially Resolved / Known Limitation: if a future review decides the RC2 badge itself is implementation leakage rather than intentional pre-launch signalling, that is a product decision for a separate item, not a silent T2-1 close-out.

### T2-2. Rebuild Help & Support as an actual help centre

**Status: Resolved**

- `app/templates/alpha/help.html` rebuilt as a guidance-first page: a client-side search box (new `app/static/js/help-search.js`) filtering a "Popular topics" list; topics rendered as expandable accordions using the existing `learn_more` contextual-help macro pattern (reinforcing, not duplicating, contextual help elsewhere in the product); quick-action buttons preserved.
- Release/build information demoted to a collapsed "Diagnostic information" disclosure at the bottom of the page, consistent with T2-1's treatment in Settings.

### T2-3. Bring Analytics within the product's own dashboard rules

**Status: Resolved**

- `app/templates/analytics/index.html`: six KPI tiles in one row regrouped into rows of four or fewer, matching UX-001 §22.
- `app/services/analytics_service.py`: `generate_weekly_report` now returns `is_new_account` and suppresses the per-metric "needs improvement" checks entirely for a zero-history week (previously they still ran and could read as a list of day-one failures); a brand-new account instead sees one encouraging, action-oriented message. Zero-history "Areas for improvement" now render with a neutral lightbulb icon rather than a warning triangle.

### T2-4. Replace native `confirm()` dialogs with the existing styled modal pattern

**Status: Resolved**

- New reusable `app/templates/partials/confirm_modal.html` (Bootstrap modal, included once in `layouts/base.html`) and `app/static/js/confirm-modal.js` (wires `[data-confirm-trigger]` buttons to populate and submit the modal's parent form).
- Applied to both call sites named in the backlog item: Study Plan archive/delete (`study_plan/view.html`, `study_plan/list.html`) and Settings → Restore from Backup (`settings/index.html`). No more native `window.confirm()` for a destructive action anywhere in the student- or settings-facing surface.

### T2-5. Fix the sign-in screen's brand redundancy

**Status: Resolved**

- `app/templates/auth/login.html`: removed the duplicate "Kwalitec" headline text beneath the logo lockup; the onboarding note now states "Kwalitec coordinator" once instead of twice.

### T2-6. Reduce repeated boilerplate and numeric false precision

**Status: Resolved**

- `app/templates/study_plan/view.html`: "Learning Outcomes: Not available yet," previously repeated on all 14 topic cards, replaced with one top-level roadmap note.
- `app/templates/dashboard/index.html`: Time Status card's `remaining_hours` and surplus/deficit hours rounded to whole numbers for display (was showing two-decimal false precision, e.g. "199.98").

### T2-7. Correct the off-palette error-page "Reference ID" colour

**Status: Resolved**

- `app/static/css/app.css`: `.error-page .error-reference code` restyled using the existing muted/neutral design token instead of the unrecognised pink/magenta colour.
- `app/templates/errors/404.html`, `403.html`, `500.html`: added one sentence of guidance on what to do with the reference ID (quote it to support), per the item's recommended solution.

### T2-8. Give Coach a reason to exist beyond restating the Mission card

**Status: Resolved**

- `app/templates/student/home.html`: Coach panel now checks whether the Mission card above is currently showing its own Why / Why now / Next / Benefit explanation (true whenever the student is not in an active guided session or reflection). When it is, Coach no longer repeats that same structured list — it instead shows commitment status (`coach_status_line`) if available, or a short pointer back to the Mission card. The full structured explanation still renders in Coach during guided-session/reflection states, when the Mission card is not showing it and Coach is the only place carrying that information.
- This follows the recommended solution's first option ("only surface it when it has evidence the Mission card does not already show... or a pointer") rather than removing Coach outright, since commitment status is information the Mission card does not carry.

### T2-9. Add a minimal brand asset set (favicon, PWA icon, share-preview image)

**Status: Already Resolved (pre-existing, outside PX-002A)**

- Verified `app/static/branding/` already contains a full asset set — `favicon.ico`, `favicon.svg`, `favicon-16/32/48.png`, `apple-touch-icon.png`, `android-chrome-192/512.png`, `maskable-icon.png`, `manifest.webmanifest`, `social-preview.png` — wired into `layouts/base.html`. This predates PX-002A (filesystem timestamps and version-query strings show it landed under a separate, already-completed PX-001-referencing effort). No PX-002A action was needed or taken.

### T2-10. Centralize icon sourcing

**Status: Deferred**

- Not attempted under PX-002A. The backlog item itself scores this Low severity and states explicitly: "not currently visible as inconsistency... not urgent for Stage 1." It is also the single largest-effort Tier 2 item (M, "mechanical but touches many files") and is a structural/drift-prevention concern rather than a student-visible trust or navigation defect — it does not fit this programme's brief of resolving *confirmed* friction without adding scope. Deferred to a future, separately-scoped implementation pass, per the backlog's own sequencing note that Tier 2 items "should not compete... for the same implementation window" as higher-priority work.

---

## Summary

| Status | Count | Items |
|---|---|---|
| Resolved | 10 | T1-1, T1-3, T1-4, T2-2, T2-3, T2-4, T2-5, T2-6, T2-7, T2-8 |
| Partially Resolved | 2 | T1-2 (wording unified; numeric source-of-truth still architecture-gated), T2-1 (Settings/Help leakage removed; RC2 footer badge intentionally kept) |
| Already Resolved (pre-existing) | 1 | T2-9 |
| Deferred | 1 | T2-10 |
| Rejected | 0 | — |

No backlog item was rejected outright; all 14 have a documented, evidence-backed disposition above.
