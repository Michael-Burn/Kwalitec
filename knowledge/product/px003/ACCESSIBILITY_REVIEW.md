# PX-003 — Accessibility Review

**Method:** Manual code inspection of templates, CSS, and JavaScript. No automated tooling (axe-core, Lighthouse, WAVE) and no live screen-reader session (VoiceOver/NVDA/JAWS) was run — this review has the same tooling limitation as PX-001 and PX-002B before it, and that limitation is treated here as a finding in its own right (see "Verification gap," below), not hidden as an assumption.

Findings are organized by the seven lenses named in the review brief. Where a finding also appears in `RELEASE_BLOCKERS.md`, its blocker ID is cited; those are not repeated in full here.

---

## 1. Keyboard

| Area | Finding | Status |
|---|---|---|
| Confirmation modal (`confirm_modal.html`/`confirm-modal.js`) | Delegates to Bootstrap 5 `Modal`, which provides focus trap, Escape-to-close, and focus restore by default when its JS bundle loads successfully. Verified present in the shared modal used for Study Plan archive/delete and Settings restore. | **Pass, conditionally** — fails silently if Bootstrap fails to load (N6). |
| Mobile navigation drawer (`app.js:4-53`) | Toggle, backdrop-click, and Escape-to-close all work. **No focus trap** — Tab can move focus behind the visually-hidden backdrop into inert content. | **Fail — see Blocker B5.** |
| Welcome modal (`welcome_modal.html`, `app.js:56-97`) | Escape closes it; clicking a `[data-welcome-dismiss]` element closes it. **No initial focus move into the dialog, no focus trap, no focus restore.** | **Fail — see Blocker B4.** |
| Appearance switcher (3-button toggle) | Real `<button>` elements, `aria-pressed`, individually labelled (post-PX-002B fix, verified still present). Fully keyboard-operable. | **Pass.** |
| Session flow step navigation (`session/components/navigation.html`) | Steps are rendered as plain `<li>`/`<span>` — not links, not tabbable, and not intended to be (it is a progress indicator, not a jump-to-step control). Correct as a design choice; flagged only because inactive step numbers carry no accessible name (see §3 ARIA). | **Pass** as a non-interactive indicator. |
| "Finish Study Session" (`mission/session.html:106-111`) | A plain link, fully keyboard-operable, but with no confirmation step — an accidental Enter-key activation ends the session with no undo. | **Pass** (keyboard-operable) / **Note** — see N14. |
| Reflection choice previews (`student/home.html:210-284`, `data-presentation-only="true"`) | Deliberately non-interactive status text, not styled or marked as controls, with comments in the template explaining the rationale. Correctly *not* reachable by keyboard, because they are not actionable. | **Pass** — correct by design, not an oversight. |

**Section verdict:** Two genuine keyboard-trap-adjacent failures (B4, B5) on the two screens where they matter most (first modal a new student sees; the only way to reach primary navigation on mobile for half the product's screens).

---

## 2. Screen reader

| Area | Finding | Status |
|---|---|---|
| Skip links | `layouts/base.html:22` → `#main-content` (exists, `base.html:27`) and `student/base.html:21` → `#student-main` (exists, `:34`) both resolve correctly and are the first focusable element in their respective shells. | **Pass.** |
| Skip link — auth shell | `layouts/auth_base.html` has **no skip link at all.** Low practical impact (auth pages are short), but it is the one shell that omits a pattern present everywhere else. | **Gap — non-blocking (see N — folded into general accessibility debt, not separately numbered as it is low-impact).** |
| Landmark roles | `layouts/base.html`: `<aside>` sidebar (implicit complementary), `<nav aria-label="Primary">` (`sidebar.html:18`), `<main role="main">`, `<footer role="contentinfo">`. Topnav `<header>` has **no explicit `role="banner"`** and its `<nav>` has no `aria-label`. `student/base.html`: `role="banner"` present, `<nav aria-label="Student experience">`, `role="main"`, and a dedicated live region `#student-live-region` (`:46`). | **Mostly pass**, one minor gap (legacy topnav banner/nav labelling). |
| Reflection value-framing copy | Present and read normally by assistive tech as static text (`reflection_card.html:10-11`) — but see Blocker B1: the *content* of the promise it makes is false, which is a trust defect, not a screen-reader defect. | **Screen-reader-mechanically fine; content is not.** |
| Help search empty-state | `role="status" aria-live="polite"` correctly added post-PX-002B (`alpha/help.html`). Verified still present. | **Pass.** |
| Help search — non-empty filtered results | No live region announces "N topics shown" when a search narrows (but does not zero) the result list — only the zero-results case is announced. | **Gap — non-blocking**, minor relative to the zero-results fix already shipped. |
| Live mission timer | Updates every second in the DOM with no `aria-live`/`role="status"` — screen-reader users get no periodic elapsed-time announcement during an active session. | **Gap — non-blocking (N17).** |
| Flash messages | `role="alert"` on the flash container (`partials/flash_messages.html`), included in both shells. Correct pattern for transient, important messages (login errors, form validation, action confirmations). | **Pass.** |
| Error pages (403/404/500) | Clear, calm copy; `error_reference_id` explained with guidance ("include this if you contact support"). No screen-reader-specific defect found. | **Pass.** |
| Icons | All decorative SVGs in the shared `icons.html` macro (post-PX-002B centralization) are `aria-hidden="true"`, correctly paired with visible or `aria-label`led text everywhere sampled. | **Pass.** |

**Section verdict:** The mechanics of screen-reader support (landmarks, live regions, alert roles) are, on balance, well-implemented where they exist. The most serious screen-reader-relevant failures in this product right now are not missing ARIA — they are ARIA that is present but not backed by correct behavior (B4's `aria-modal` with no focus management) or correct content (B1's reflection promise).

---

## 3. Focus order

| Area | Finding | Status |
|---|---|---|
| General DOM order vs. visual order | Sidebar → topnav/topbar → main content → footer, consistently, in every shell sampled. No tab-order anomalies found in any template reviewed. | **Pass.** |
| `#main-content` / `#student-main` skip targets | Both have `tabindex="-1"` so they are legitimately focusable skip destinations, and both are followed immediately by real page content. | **Pass.** |
| Welcome modal | Present in the DOM after main content (loaded via a shell include, not moved to the top of `<body>`); since focus is never explicitly moved into it (B4), a keyboard user tabbing from the top of the page reaches it only in its natural DOM position, not immediately — compounding B4 rather than being a separate defect. | **Dependent on B4 fix.** |
| Session step indicator | Non-interactive `<span>`/`<li>` elements are correctly skipped in tab order (they are not `tabindex`-added), so they do not create a false stop. | **Pass.** |

**Section verdict:** Focus *order*, where focus actually lands, is solid. The defects in this review are about focus *management at transition points* (opening a modal, opening a drawer) — a narrower and more fixable problem than a systemic tab-order issue would be.

---

## 4. Contrast

| Pair | Values | Verdict |
|---|---|---|
| `.sidebar .nav-section-label` on chrome background | `rgba(255,255,255,0.35)` on `#0D1B2A` (`app.css:51`) — effective ≈ `rgb(97,107,117)` on `rgb(13,27,42)` | **Fail — see Blocker B6.** Well below AA for any text size. |
| `.sidebar-signout` / `.sidebar-brand-descriptor` | `rgba(255,255,255,0.55)` on `#0D1B2A` (`app.css:45,63,561`) | **Borderline** — noticeably better than the 35% label but should be verified with a real contrast tool before being called a pass; not independently blocking, but adjacent to B6's failure on the same page. |
| `--text-muted` on `--surface` | Light: `#5c6570` on `#ffffff`; Dark: `#a8b0bd` on `#1c222d` (`tokens.css:23,145`) | **Plausible AA risk at small sizes** (captions, `.type-meta`, error "Reference ID" text) — not confirmed as a fail, flagged for verification with an actual contrast checker rather than asserted as compliant, which is the more conservative posture given three prior programmes never ran one either. |
| `.alert-warning` text on `.alert-warning` background | `#A16207` on `rgba(161,98,7,0.12)` (light), `#D97706` on `rgba(217,119,6,0.18)` (dark) | **Plausible AA risk** — amber-on-pale-amber-tint is a common failure pattern; not confirmed, flagged for verification. |
| `.alert-success` text on background | `#0f766e` on `#e6f7f5` (light) | **Plausible AA risk**, same reasoning as above. |
| Body / secondary / link text on surface | All sampled pairs in `tokens.css` for primary body copy, secondary copy, and links | **Pass by inspection** — sufficiently dark-on-light / light-on-dark that failure is implausible without a scanner, in both themes. |

**Section verdict:** One confirmed, severe failure (B6). Several plausible-but-unconfirmed risks on alert/badge backgrounds and muted text, which this review — consistent with its own standard of not asserting what it has not verified — records as open risk requiring a real contrast tool, not as a pass and not as an additional hard blocker beyond B6, where the arithmetic is unambiguous even without a scanner.

---

## 5. ARIA

| Area | Finding | Status |
|---|---|---|
| Appearance switcher | `role="group" aria-label="Appearance"`, individually labelled buttons with distinct `aria-label`/`title` per option (PX-002B fix, verified present in the shared macro). | **Pass.** |
| Confirm modal | `aria-labelledby` wired to a real heading; relies on Bootstrap to inject `role="dialog"`/`aria-modal` at show-time rather than declaring them in markup. Works when Bootstrap loads (see N6); no `aria-describedby` linking the body text. | **Mostly pass, minor gap.** |
| Welcome modal | Declares `role="dialog" aria-modal="true"` directly in markup (not runtime-injected) but has no behavior to back the contract it declares. This is a worse pattern than the confirm modal's approach, because the ARIA promise is made without any of the supporting mechanics. | **Fail — see Blocker B4.** |
| Progress bars | `role="progressbar"` with `aria-valuenow`/`aria-valuemin`/`aria-valuemax` present everywhere sampled (Journey, Analytics, Mission). Directly covered by `tests/presentation/student/test_accessibility.py`. | **Pass, and automatically verified.** |
| `data-presentation-only` elements | Four instances on Home, all plain text/status, none carrying a false `role="button"`. Correctly documented in adjacent template comments as an intentional accessibility decision from PX-002A. | **Pass.** |
| Session step indicator | Active step has no `aria-current="step"`; inactive step numbers are `aria-hidden="true"` with no visible label alternative at narrow widths (`session.css:358-364` hides labels on mobile except the active step). A screen-reader user gets numbered pills with no announced meaning for the non-active steps. | **Gap — non-blocking**, but worth closing given how cheap `aria-current` is to add. |
| `role="status"` usage (empty states, skeletons, alpha badge) | Consistently used for non-interactive, informational content; none carry stray `tabindex`. | **Pass.** |

**Section verdict:** The product's ARIA authorship is generally competent and intentional (multiple templates carry comments explaining *why* an element is or is not interactive — a genuinely good practice this review has no basis to criticize). The one place ARIA is authored but not backed by real behavior is the single highest-visibility place it could be: the first-session Welcome modal.

---

## 6. Touch targets

| Control | Effective size (padding + content, by CSS arithmetic) | Meets `--touch-target-min` (44px)? |
|---|---|---|
| `.btn`, `.form-control`, `.form-select` | Explicitly wired to `--touch-target-min: 2.75rem` (`app.css:590-592`) | **Yes.** |
| `.student-btn-primary` | Hardcoded `min-height: 2.75rem` (`student.css:860`) — meets the size but duplicates rather than references the token | **Yes**, by coincidence of a matching hardcoded value. |
| Appearance switcher buttons (icon-only, ≤575.98px) | `padding: 0.45rem` + 20px icon ≈ 34px | **No — contributes to Blocker B7.** |
| `.ctx-help-trigger` ("Why this estimate?" style disclosure triggers) | `min-height/min-width: 1.5rem` (24px) | **No.** |
| `.sidebar .nav-link` | `padding: 0.65rem`, no explicit min-height | **Marginal — likely under 44px depending on line-height.** |
| `.student-nav-link` | `padding: 0.5rem 0.75rem`, no explicit min-height, text-only | **Marginal — estimated ~38px.** |

**Section verdict:** The product correctly defines a touch-target token and correctly applies it to its most common controls (buttons, form fields). It does not apply that same discipline to several icon-only or text-only navigation controls, most concretely the mobile appearance switcher, which is the smallest, most icon-dependent control in the whole system and the one most likely to be mis-tapped on an actual phone.

---

## 7. Motion

| Area | Finding | Status |
|---|---|---|
| Global reduced-motion rule | `app.css:540-542` applies a universal `*, *::before, *::after { transition/animation-duration: 0.01ms; ... }` under `prefers-reduced-motion: reduce`, plus targeted rules for skeletons, flash alerts, and page-enter animations (`tokens.css:251-256,283-288`, `app.css:584-588`). | **Pass — but only for shells that load `app.css`.** |
| Student shell (`student/base.html`) | Loads `student.css` + `tokens.css` **only** — does not load `app.css`, and therefore does not receive the universal reduced-motion rule. `student.css` has its own targeted reduced-motion blocks (`:762-767,799-810,914-918`) covering most, but confirmed **not all**, of its own transitions — e.g. `.student-nav-link`'s `transition` (`student.css:132`) and `.student-form input/select/textarea`'s `transition` (`student.css:897`) are not inside any reduced-motion query. | **Partial gap** — the canonical student experience (the primary path for an external pilot student) has narrower reduced-motion coverage than the legacy shell, for a small number of specific transitions. Not blocking on its own (the missed transitions are minor hover/focus effects, not vestibular-trigger-scale motion), but inconsistent with the product's own stated commitment to respecting this preference. |
| Session shell (`session/base.html` / `session.css`) | Has its own reduced-motion block (`session.css:412-423`) covering its main animated elements. | **Pass, scoped correctly to its own file.** |
| High-contrast (`prefers-contrast: more`) | Only referenced once, for KPI status panel border widths (`app.css:307-311`) — not a system-wide affordance. | **Minimal coverage, non-blocking** — flagged as a gap relative to the breadth of the reduced-motion handling, not as a defect in itself since no explicit high-contrast requirement was set for this review. |

**Section verdict:** No blocking motion issue. The gap between the legacy shell's comprehensive, universal reduced-motion rule and the canonical student shell's narrower, per-selector coverage is a real inconsistency worth closing, but the missed transitions are cosmetic (hover color/shadow changes), not the kind of large-scale, vestibular-trigger motion `prefers-reduced-motion` exists to prevent.

---

## Verification gap (recorded, not assumed away)

No axe-core, Lighthouse, WAVE, or equivalent automated accessibility scan has been run against this product at any point in its documented design-review history (PR-001, PX-001, PX-002A, PX-002B, or this review). No live screen-reader session (VoiceOver, NVDA, JAWS, TalkBack) has been recorded either. `tests/presentation/student/test_accessibility.py` — the only automated accessibility coverage that exists — checks seven narrow string-presence assertions (`lang="en"`, a viewport meta tag, `aria-current="page"` on the active nav link, a `color-scheme` meta tag, presence of an `<h1>`, a weak CSRF/copy proxy check, and `aria-valuenow`/`min`/`max` *if* a progress bar is present) across five student routes. It does not check contrast, focus order, keyboard operability, ARIA correctness on custom widgets, motion handling, or touch target size — every finding in sections 1–6 above was found by manual inspection, not by anything CI currently runs.

This is recorded here as its own finding because it means **this document, like the two accessibility passes before it, cannot certify WCAG conformance** — it can only report what manual code inspection found, and manual inspection reliably under-counts real defects relative to a tool plus a real assistive-technology session. Combined with Blocker B7 (no live mobile/tablet rendering has ever occurred either), the honest position for a release-approval reviewer is that the accessibility posture of this product, going into its first external pilot, has never been verified by anything other than reading source code.
