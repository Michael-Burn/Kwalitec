# PX-002B — Accessibility Report

Scope: accessibility changes made in this programme, plus spot-check
findings from a review pass across focus order, keyboard support, screen
reader compatibility, contrast, touch targets, and motion.

## Changes made

### 1. Help search — live region for the empty-results message

**Before:** `app/templates/alpha/help.html` toggled a `hidden` attribute on
the "No topics match that search" paragraph via `help-search.js`, with no
`role` or `aria-live`. A screen reader user typing a query with zero matches
received no announcement that the topic list had changed.

**After:** `role="status" aria-live="polite"` added to the element. No JS
change needed — the existing `hidden`-toggle logic in `help-search.js`
already produces the DOM change that the live region needs to announce.

### 2. Appearance switcher — distinct accessible name per button

**Before:** in the top-nav variant, all three buttons (Light/Dark/System)
were wired with `aria-labelledby="appearance-label"`, pointing at one shared
"Appearance" caption — meaning all three buttons had the *same* computed
accessible name ("Appearance") for assistive technology, distinguishable
only by `aria-pressed` state and (for sighted users) their visible label. In
the Settings variant, the buttons had no `aria-label`/`title` at all, relying
entirely on their visible `<span>` text — which is hidden via CSS
(`.appearance-option span{display:none}`) below 576px, meaning icon-only
buttons at that width had **no accessible name whatsoever**.

**After:** every button rendered by the shared `appearance_switcher()` macro
now has an explicit `aria-label` ("Light" / "Dark" / "System") and a matching
`title`, independent of whether the visible `<span>` text is shown or hidden
by the narrow-viewport CSS rule. This is a real, pre-existing gap that
existed in both prior implementations; fixing it once in the shared macro
fixes it everywhere the control is used.

## Spot-check review (existing behaviour confirmed, no change needed)

- **Focus order:** `student/base.html` uses a `skip-link` to `#main-content`
  and the sidebar/topnav/main content DOM order matches visual reading
  order on every screen reviewed. No tab-order anomalies found.
- **Keyboard support — confirmation modal:** `data-confirm-trigger` /
  `confirm-modal.js` (from PX-002A) already traps focus within the modal and
  restores focus to the trigger on close; verified still functioning after
  the icon-macro migration touched several buttons that use this pattern
  (e.g. Settings → Data → Restore from Backup).
  `focus-visible` outlines (`box-shadow: var(--focus-ring)`) are present on
  `.appearance-option`, nav links, and buttons — verified present after the
  icon/appearance-switcher consolidation (the macros preserve the classes
  these selectors target).
- **Touch targets:** `.appearance-option` padding (`0.4rem 0.65rem`,
  `0.45rem` at ≤576px) combined with the 20px icon keeps every button above
  the ~44px minimum target guidance once line-height and button chrome are
  included; unchanged by this programme.
- **Motion:** `prefers-reduced-motion: reduce` is already respected for
  `.student-btn-primary` hover/active transforms (`student.css`); no new
  animation was introduced in this programme, so no new motion-preference
  handling was required.
- **Contrast:** `.student-muted` / `text-muted` token colours were spot
  checked against their surface colours in both light and dark themes via
  `tokens.css` — no regressions introduced (this programme did not modify
  any colour token).

## Existing automated coverage (unchanged, still passing)

`tests/presentation/student/test_accessibility.py` continues to verify,
across every student route: `lang="en"`, viewport meta, `aria-current="page"`
on the active nav link, `color-scheme` meta, presence of an `<h1>`, and
`aria-valuenow`/`aria-valuemin`/`aria-valuemax` on any progressbar. All pass
after this programme's changes (see `COMPLETION_REPORT.md` for the full test
run).

## Known limitations

- The appearance switcher's `role="group" aria-label="Appearance"` wrapper
  still gives the *group* one name while each button inside now has its own
  distinct name — this is standard, correct ARIA grouping and was not
  changed further.
- A full automated contrast audit (e.g. axe-core / Lighthouse CI) was not
  run as part of this programme; the contrast spot-check above was manual,
  token-level inspection. Recommended as a follow-up if a dedicated
  accessibility audit is scheduled.
