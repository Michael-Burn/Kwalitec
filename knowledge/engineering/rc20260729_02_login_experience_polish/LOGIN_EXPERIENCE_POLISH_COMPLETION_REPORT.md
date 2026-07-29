# LOGIN_EXPERIENCE_POLISH_COMPLETION_REPORT

**Tag:** RC-2026.07.29-02  
**Surface:** Public Sign In  
**Baseline:** v2.0.0-design-freeze · DX-006B COMPLETE · RC-2026.07.29-01  
**Date:** 2026-07-29  
**Commit:** none (awaiting independent review)

---

## Executive Summary

Presentation-only polish of the public Sign In page so the full experience fits a standard laptop viewport without vertical scrolling. Root cause of overflow was `landing-split { min-height: 100vh }` combined with Appearance and footer chrome stacked *below* the split. Layout now fills remaining viewport height; left-panel and card spacing were tightened on the design-token scale; footer was rebuilt as a single compact chrome row (Appearance · Alpha identity · Version/Build). Authentication, routing, validation, Remember Me, and theme behaviour are unchanged.

**Verdict: GO**

---

## Files Modified

- `app/templates/layouts/auth_base.html` — Appearance moved into compact public footer chrome
- `app/templates/partials/app_footer.html` — `public_chrome` layout (centre alpha, right brand/build); default layout preserved for authenticated shells
- `app/static/css/app.css` — viewport-fit layout, spacing tighten, footer chrome, short-height laptop media query, responsive wrap

## Files Created

- `knowledge/engineering/rc20260729_02_login_experience_polish/LOGIN_EXPERIENCE_POLISH_COMPLETION_REPORT.md` (this report)
- `knowledge/engineering/rc20260729_02_login_experience_polish/_evidence/viewport_audit.json`
- `knowledge/engineering/rc20260729_02_login_experience_polish/_evidence/a11y_behaviour_audit.json`
- `knowledge/engineering/rc20260729_02_login_experience_polish/_evidence/screenshots/*.png`

---

## Spacing Changes

All values from the existing token scale (`space-xs`…`space-4xl`). No one-off spacing invented beyond token usage.

| Region | Before | After |
|---|---|---|
| Hero padding | `space-4xl` (64) all sides | `space-3xl` / `space-4xl` (48 / 64); short laptop → `space-2xl` / `space-3xl` |
| Logo → brand stack | logo margin `space-2xl` + `space-sm` pad | margin `space-xl`, pad `0` |
| Brand stack bottom | `space-xl` | `space-lg` |
| Descriptor → value | descriptor margin `space-md` | `space-sm` |
| Heading/badge block | alpha margin `space-xl` / `space-2xl` | `space-lg` / `space-xl` (short: `space-md` / `space-lg`) |
| Feature bullet gap | `space-md` | `space-sm` (short: `space-xs`) |
| Form-side padding | `space-3xl` vertical | `space-2xl` (short: `space-xl`) |
| Card padding | `space-3xl` (large: `space-4xl`) | `space-2xl` (large: `space-3xl`; short: `space-xl`) |
| Field spacing | `space-xl` | `space-lg` (short: `space-md`) |
| Subtitle / remember / hint | `space-2xl` bottoms | `space-xl` (short: `space-lg`) |
| Onboarding note | margin `space-2xl`, pad `space-lg`/`space-xl` | margin `space-xl`, pad `space-md`/`space-lg` |
| Control sizing | input/button ~0.85rem pad | `min-height: 2.75rem` (44px) retained |

Copy, feature count, form fields, and Internal Alpha messaging were not shortened or removed.

---

## Footer Improvements

Redesigned as lightweight application chrome on public auth surfaces only.

**Desktop structure (single row):**

| Left | Centre | Right |
|---|---|---|
| Appearance (Light / Dark / System) | Internal Alpha · Founding Cohort | Kwalitec v2.0.0 · Build RC2 |

- Appearance relocated from a separate block above the footer into `public-footer-start`
- Vertical padding reduced (`space-lg` → `space-sm`)
- Metadata typography at `font-xs` (12px), muted
- Measured footer height at 1366×768: **57px** (was ~120px+ combined Appearance + footer stack)
- ≤991px: flex-wrap centres chrome items without a forced three-row stack
- Authenticated `app_footer` default layout unchanged

---

## Viewport Results

Playwright Chromium, light + dark, networkidle. Source: `_evidence/viewport_audit.json`.

| Viewport | Vertical scrollbar | docScrollHeight | clientHeight | Footer H |
|---|---|---:|---:|---:|
| **1366×768** | **None** | 768 | 768 | 57 |
| **1440×900** | **None** | 900 | 900 | 57 |
| **1920×1080** | **None** | 1080 | 1080 | 57 |
| Tablet 768×1024 | Expected (stacked) | 1235 | 1024 | 49 |
| Mobile 390×844 | Expected (stacked) | 1184 | 844 | 102 |

Desktop success criteria met in both light and dark themes.

---

## Accessibility

Evidence: `_evidence/a11y_behaviour_audit.json`.

| Check | Result |
|---|---|
| Landmarks (`main`, `footer[role=contentinfo]`) | Present |
| Single H1 | Yes (“Sign in”) |
| Form labels | Present for email/password |
| Focus order | Logo → Email → Password → Remember me → Submit → Appearance Light/Dark/System |
| Appearance `role="group"` + `aria-label` | Preserved |
| Alpha identity `role="status"` | Preserved (full variant in centre) |
| Primary control height | Submit ≥ 44px; inputs ~50px |
| Appearance options | ~32px (chrome metadata; prior parity) |
| Contrast samples | Title/subtitle/footer muted text on surface; primary CTA on brand blue |

No ARIA or semantics removed. Keyboard navigation intact.

---

## Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop ≥992 | Split layout; page fits height; short-height (`max-height: 820px`) further tightens spacing |
| Tablet ≤991 | Column stack preserved; footer wraps; page scrolls as content requires |
| Mobile ≤575 | Existing mobile padding/logo scale retained; no regression of stacked flow |

Tablet/mobile still scroll — inherent to stacked hero + card + chrome. No desktop scroll regression introduced on small screens.

---

## Behaviour Verification

| Behaviour | Result |
|---|---|
| Theme Light/Dark/System toggle | Works (`data-theme` switches) |
| Invalid credentials stay on login + feedback | Confirmed |
| Remember Me field present | Unchanged |
| Routing `/auth/login` | Unchanged |
| Version string `Kwalitec v{APP_VERSION}` | Present (`2.0.0`) |
| Build RC2 | Present in footer end |
| Regression tests | 29 passed (`iahf004b`, theme surface, QS-001 version identity, PX-001) |

---

## Before/After Measurements

### Page chrome (1366×768, CSS-derived before vs measured after)

| Metric | Before (approx.) | After (measured) |
|---|---:|---:|
| Split min-height | 100vh (768) + chrome below | flex fill of remaining viewport |
| Appearance block | ~64px separate band | in footer |
| Footer band | ~56–72px | 57px chrome row |
| Total page height | ~900–940px → **scrolls** | **768px → no scroll** |
| Overflow delta | ~130–170px | **0** |

### Card / hero (after, light)

| Viewport | Card H | Hero inner H |
|---|---:|---:|
| 1366×768 | 581 | 354 |
| 1440×900 | 669 | 410 |

Screenshots: `_evidence/screenshots/`.

---

## Known Issues

1. **Tablet/mobile still scroll** — expected for stacked marketing + form; not a desktop regression.
2. **Appearance option hit area ~32px** — below ideal 44px touch target; matches prior chrome control sizing; acceptable for metadata chrome on desktop.
3. **Short-height media query** (`max-height: 820px`) slightly densifies spacing on short laptops; still token-based and readable at 1366×768.
4. **Cross-browser** validated in Chromium only (Playwright); Safari/Firefox visual parity assumed via shared CSS — spot-check recommended in review.

---

## Recommendation

### GO

Ship after independent visual review. Desktop laptop fit criteria are met; behaviour and accessibility surface are unchanged; footer matches the specified chrome structure; tablet/mobile stacking behaviour is preserved.

**Conditions for reviewer:** confirm premium feel at 1366×768 in light and dark; confirm footer chrome does not feel cramped on Safari.

---

## Architecture / Migration

- **Migration impact:** None  
- **Curriculum V1/V2:** N/A (presentation-only public auth surface)  
- **Auth/API contracts:** Unchanged
