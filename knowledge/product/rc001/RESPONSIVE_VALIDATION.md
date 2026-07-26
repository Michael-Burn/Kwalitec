# RC-001 — Responsive Validation (B7)

**Method:** Live Playwright (Chromium) rendering of the running Flask dev server against a seeded evidence database, at all 9 required breakpoints. Two capture pipelines were used:

1. `knowledge/product/rc001/_evidence/capture_rc001.py` — 11 static screens × 9 breakpoints = 99 renders, driven directly against live routes with a real logged-in session.
2. `knowledge/product/rc001/_evidence/capture_session_flow.py` — 5 session-flow screens × 9 breakpoints = 45 renders. The live activity engine in the seeded environment cannot resolve `has_explanation` for a placeholder answer (no real question bank behind the seeded curriculum topics), so a genuine click-through never reaches Reflection reliably; this script instead drives the same real `ReflectionService`/`SessionRuntimeAdapter`/template stack via Flask's test client with the `FakeActivityEnginePort` already used by `tests/presentation/session/test_routes.py::test_answer_and_advance_to_reflection`, then screenshots the resulting HTML with a `<base>` tag pointing at the live dev server so CSS/JS resolve identically to a real request.

**Overflow metric:** `document.documentElement.scrollWidth − document.documentElement.clientWidth`, evaluated in-page immediately after each screenshot. A value `> 1px` is treated as a horizontal-overflow failure requiring a fix (sub-pixel rounding noise below 2px is not actionable).

**Total renders:** 144 (99 + 45). **Failures found:** 1 (touch-target sizing, not overflow — see below). **Overflow failures:** 0.

---

## Breakpoints reviewed

| Breakpoint | Viewport (px) | Tier | Screens | Max overflow |
|---|---|---|---|---|
| 320px | 320×844 | Mobile | 16 (11 static + 5 session) | 0px |
| 375px | 375×812 | Mobile | 16 | 0px |
| 390px | 390×844 | Mobile | 16 | 0px |
| 414px | 414×896 | Mobile | 16 | 0px |
| 768px | 768×1024 | Tablet | 16 | 0px |
| 820px | 820×1180 | Tablet | 16 | 0px |
| 1024px | 1024×1366 | Desktop | 16 | 0px |
| 1280px | 1280×800 | Desktop | 16 | 0px |
| 1440px | 1440×900 | Desktop | 16 | 0px |

## Screens reviewed at every breakpoint

| Screen | Route | Shell |
|---|---|---|
| Home | `/student/` | Canonical (student) |
| Journey | `/student/journey` | Canonical (student) |
| Revision | `/student/revision` | Canonical (student) |
| History | `/student/history` | Canonical (student) |
| Profile | `/student/profile` | Canonical (student) |
| Study Plan | `/study-plan/` | Legacy (`layouts/base.html`) |
| Settings → Profile | `/settings/profile` | Legacy |
| Settings → Preferences | `/settings/preferences` | Legacy |
| Settings → Data | `/settings/data` | Legacy |
| Settings → Account Status | `/settings/internal-alpha` | Legacy |
| Help | `/alpha/help` | Legacy |
| Session Overview | `/session/<id>/overview` | Session |
| Session Activity | `/session/<id>/activity` (before + after answer) | Session |
| Session Reflection | `/session/<id>/reflection` | Session |
| Session Summary | `/session/<id>/summary` | Session |

Plus, at 1440px only (representative desktop, additional states not required at every breakpoint per the brief): Empty-state Home/Journey/Revision/History/Profile (`empty` account with no active plan), Onboarding, and a 404 error page.

---

## Findings

### Confirmed and fixed: appearance-switcher touch target below minimum (≤575.98px)

PX-003's B7 finding named this as a *candidate* it could not confirm from static CSS inspection alone ("appearance-switcher icon-only buttons at ≤575.98px, whose padding-plus-icon math comes to roughly 34px — short of the ~44px target the product's own `--touch-target-min` token defines... a token that is in any case not applied to this control at all").

- **Live measurement before fix** (375×812 viewport, Playwright `boundingBox()`): all three `.appearance-option` buttons rendered at **36.375px × 36.375px**.
- **Fix:** `app/static/css/app.css` — added `min-width: var(--touch-target-min, 2.75rem)` and `min-height: var(--touch-target-min, 2.75rem)` (plus `justify-content: center` to keep the icon centred in the larger box) to `.appearance-option` inside its existing `@media (max-width:575.98px)` rule.
- **Live measurement after fix:** all three buttons render at **44px × 44px** exactly.
- **Regression test:** `tests/test_rc001_accessibility.py::TestTouchTargets::test_appearance_option_meets_touch_target_min_at_mobile_width`.
- **Re-verified visually:** `mobile-375px-settings-preferences.png`.

### Investigated and disproven: `.mission-grid` on a 320px viewport

PX-003's second candidate — `.mission-grid{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}` possibly exceeding available width on a 320px phone after container padding — was directly tested. **Result: `overflow_px: 0` at 320px** across every captured screen. The grid's `minmax(320px, 1fr)` track does not force overflow at exactly 320px viewport width because the container itself has no competing horizontal padding wide enough to push the single-column track past the viewport edge in the current layout. Disproven with live evidence, not re-asserted from inspection.

### No other horizontal-overflow failures

Across all 144 renders (16 screens × 9 breakpoints), `overflow_px` was `0` in every case, both before and after the touch-target fix (the fix does not affect horizontal layout width). See `knowledge/product/rc001/_evidence/results.json` for the complete per-screen, per-breakpoint machine-readable record.

---

## Representative screenshots by breakpoint

Full index with every file: `SCREENSHOT_INDEX.md`. Selected examples to demonstrate the range:

**320px (smallest required, iPhone SE class):**
- `screens/mobile-320px-home.png`
- `screens/mobile-320px-session-reflection.png` — B1's on-screen promise text and the note field it now persists, fully legible with no overflow at the narrowest required width.
- `screens/mobile-320px-settings-preferences.png` — appearance switcher post-fix.

**768px / 820px (tablet):**
- `screens/tablet-768px-home.png`
- `screens/tablet-820px-study-plan.png`

**1440px (largest desktop):**
- `screens/desktop-1440px-home.png`
- `screens/desktop-1440px-session-reflection.png`

---

## Conclusion

B7's evidence gap — "zero image files exist anywhere under `knowledge/`... nobody has opened this product on a phone or tablet, in a real browser or an emulator, at any point in its documented design-review history" — is closed. 161 screenshots now exist under `knowledge/product/rc001/screens/`, covering all 9 required breakpoints for every student-facing screen, plus empty/onboarding/error states at representative widths. Both concrete failure candidates PX-003's static analysis raised were directly tested; one was real and is fixed, one was investigated and found not to reproduce.
