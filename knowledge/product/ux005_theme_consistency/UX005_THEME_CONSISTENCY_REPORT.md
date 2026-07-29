# UX-005 — Theme Consistency & Accessibility Audit Report

**Programme:** Premium Product Experience  
**Status:** Complete (foundation pass)  
**Date:** 2026-07-29  
**Scope:** Establish a canonical visual theme foundation for Light, Dark, and System appearance across Student OS, Founder Console, Authentication, Assessment/Quick Check chrome, and shared components. No workflow, routing, or data-model changes.

---

## Summary

Kwalitec already had a solid token core (`brand.css` + `tokens.css` + `theme.js`), but siloed shells and static brand colours used as **text** caused Dark Mode readability failures and broken Assessment/Quick Check chrome after `session.css` was retired. UX-005 restores Assessment/QC session chrome via `session_chrome.css` (without reviving the forbidden `session.css` path), expands semantic design tokens, and fixes root-cause contrast bugs in Student topbar chrome text, Console active navigation, timeline/link colours, and phantom `--color-text-primary` usages. Primary buttons now use `--on-primary` instead of hard-coded white. Empty-state craft gained optional secondary actions. Workflows and business logic were untouched.

---

## Pages audited

| Surface | Route / layout | Theme load | Finding |
|---------|----------------|------------|---------|
| Student OS (Home, Journey, History, Revision, Settings hub) | `layouts/eos_student.html` | tokens + student.css + theme.js | Topbar chrome text tokenised; navy-as-text fixed |
| Study Plan / Wizard | EOS / wizard.css | OK | Token-clean wizard CSS |
| Founder Console | `layouts/console_base.html` | tokens + app + founder CSS | Active nav used static `--brand-midnight` → fixed |
| Authentication / Landing | `layouts/auth_base.html` | tokens + app.css | Appearance switcher OK; landing hero remains intentional dark chrome |
| Assessment Delivery | `student/assessment/base.html` | **was broken** (404 `session.css`) | Restored via `session_chrome.css` |
| Quick Check | `adaptive_assessment/base.html` | **was broken** | Same chrome restore |
| Study Session | `session/base.html` → EOS | design_system.css | Correctly does **not** use legacy `session.css` |
| Product Settings tabs | `/settings/*` | via app/EOS | Appearance control present |
| Dashboard (legacy) | `dashboard/index.html` | app.css | Phantom `--color-text-primary` aliased |
| Analytics / Mission / Console dialogs | various | mixed | Token usage mostly sound; residual inline styles remain debt |

---

## Components audited

Buttons (`.ds-btn*`, `.btn-*`, `.student-btn-*`, `.console-btn-*`, `.session-btn-*`), cards/panels, badges, inputs, tables, navigation (student topbar, console sidebar, appearance switcher), dialogs/modals, empty states, status chips, search, focus rings, scrollbars (browser `color-scheme`), skeleton loaders.

---

## Theme inconsistencies found

| ID | Issue | Severity | Resolution |
|----|-------|----------|------------|
| T1 | Assessment/QC linked deleted `session.css`; `--session-*` undefined | P0 | `session_chrome.css` + token aliases |
| T2 | Console `.is-active` nav used static `--brand-midnight` | P1 | `color: var(--primary)` |
| T3 | Timeline / educational nav used static `--brand-navy` as text | P1 | `--primary` / `--link` |
| T4 | `--color-text-primary` used but undefined | P1 | Alias → `--text-primary` |
| T5 | Topbar notes hard-coded `#fff` mix | P1 | `--chrome-text-muted` |
| T6 | Primary buttons hard-coded `#fff` | P2 | `--on-primary` |
| T7 | Console `--bg` / `#fff` fallbacks | P2 | `--background` / `--surface` |
| T8 | Table hover tint light-only | P2 | Tokenised + dark override |
| T9 | Missing UX-005 semantic aliases (`surface-primary`, etc.) | P2 | Added to `tokens.css` |
| T10 | Parallel button/card/badge systems across shells | P3 | Documented; not fully unified (debt) |

---

## Accessibility findings

| Finding | WCAG concern | Status |
|---------|--------------|--------|
| Static navy/midnight text on dark surfaces | Contrast &lt; AA | **Fixed** (Console active, timeline, educational links) |
| Student topbar / session chrome (white-on-navy) | AA for chrome nav | Preserved; now via `--chrome-text*` tokens (same ratios as RC-001 chrome) |
| Phantom text colour variable | Unpredictable inheritance | **Fixed** via alias |
| Focus indicators | Visible focus required | Retained (`--focus-ring` / chrome focus rings) |
| Colour-alone status | Status chips still colour-forward | Residual — badges keep text labels; no icon-only status change in this pass |
| Placeholder / disabled opacity | `--opacity-disabled` exists | Not fully revalidated page-by-page |
| Keyboard appearance switcher | Present on Student + Auth + Settings | Assessment/QC still lack on-page switcher (theme still applies from stored preference) |

Contrast regression suite `tests/test_rc001_contrast.py` remains green for chrome sidebar ratios.

---

## Design token audit

### Canonical stack

1. `brand.css` — official palette + dark surface/text/status overrides  
2. `tokens.css` — semantic product tokens (single source for shells)  
3. `design_system.css` — token-only `.ds-*` primitives  
4. Shell CSS — aliases only (`--student-*`, `--session-*`)

### Added / formalised in UX-005

| Token | Maps to / value |
|-------|-----------------|
| `--surface-primary` | `--surface` |
| `--surface-secondary` | `--background` |
| `--surface-overlay` | Light/dark scrim |
| `--border-primary` | `--border` |
| `--accent-primary` / `--accent-secondary` | `--primary` / brand muted |
| `--link` / `--link-hover` | Primary action links |
| `--chrome-text` / `--chrome-text-muted` / `--chrome-text-subtle` | Text on permanent navy chrome |
| `--color-text-primary` | Alias of `--text-primary` |
| `--session-*` family | Aliases of shared tokens for Assessment/QC |

### Hard-coded colour policy

Hard-coded hex remains **allowed only** in `brand.css` and `tokens.css` definitions. Component CSS should consume semantic tokens. Residual hard-codes in dormant `.sidebar` / landing hero gradients are intentional brand chrome or legacy dormant styles.

---

## Dark Mode findings

- Surfaces (`--background`, `--surface`, `--surface-elevated`) flip correctly via `data-theme="dark"`.
- Student/Session topbars remain **permanent brand chrome** (navy) in both themes — by design (RC-001); text now uses `--chrome-text*` so it cannot accidentally inherit body `--text-primary` if chrome styling regresses.
- Console sidebar/topbar follow surface tokens; active nav no longer paints near-black midnight text.
- No pure `#000` background (regression test retained).
- Assessment/QC shells render again (were unstyled).
- Residual risk: Bootstrap utilities on pages that omit `app.css` (EOS silo — CQ-006 A01); document for follow-up.

---

## Light Mode findings

- Token light values unchanged in spirit; new aliases do not alter light palette.
- Chrome topbar remains navy with light inverse text (correct).
- Console light mode unaffected except active nav now uses primary blue (clearer, still AA on light tint).
- Landing hero remains dark promotional plane (intentional).

---

## Files Created

- `app/static/css/session/session_chrome.css` — Assessment/Quick Check session chrome (not `session.css`)
- `tests/presentation/test_ux005_theme_consistency.py`
- `knowledge/product/ux005_theme_consistency/UX005_THEME_CONSISTENCY_REPORT.md` (this file)

## Files Modified

- `app/static/css/tokens.css`
- `app/static/css/app.css`
- `app/static/css/student/student.css`
- `app/static/css/assessment/assessment.css`
- `app/static/css/adaptive_assessment/quick_check.css`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/templates/student/assessment/base.html`
- `app/templates/adaptive_assessment/base.html`
- `app/templates/partials/empty_state.html`
- `tests/test_theme_system.py`

### Components consolidated

- Session chrome for Assessment/QC restored as one shared stylesheet.
- Empty-state macro: optional secondary action + shared action row.
- Primary button text colour: `--on-primary` across student, console, session chrome.
- Semantic token aliases prevent duplicate ad-hoc colour invention for surfaces/links/chrome text.

Full unification of `.ds-btn` / `.student-btn` / `.console-btn` / Bootstrap `.btn` into one class tree was **not** completed (see debt).

---

## Performance improvements

- Avoided restoring full duplicate `session.css` on Study Session (EOS path remains lean).
- Removed obsolete Assessment/QC dependency on a 404 stylesheet.
- Prefer token aliases over per-component hex overrides (fewer competing cascade layers for colour).
- Did not delete dormant `.sidebar` / `.topnav` blocks in `app.css` in this pass (safe follow-up purge).

---

## Tests Executed

```text
python3 -m pytest \
  tests/test_theme_system.py \
  tests/presentation/test_ux005_theme_consistency.py \
  tests/presentation/session/test_templates.py \
  tests/test_rc001_contrast.py -q
```

**Outcome:** 41 passed.

Manual verification checklist (Light / Dark / System): Student Home topbar + appearance control; Founder Console active sidebar; Assessment or QC entry chrome; Auth login appearance switcher. Screenshots were not checked into the repo in this pass — capture recommended before release dogfood.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved: presentation CSS only; no service/route/model changes.
- Curriculum V1/V2 traversal: N/A (visual only).
- DX-006B / CQ-006 invariant retained: `app/static/css/session/session.css` must **not** exist; Study Session stays on EOS + `design_system.css`.
- Theme bootstrap (`theme.js` → `data-theme` / `data-bs-theme` / `data-appearance`) unchanged in behaviour.

---

## Technical Debt

1. Parallel button/card/badge systems across DS / Bootstrap / Student / Console remain.
2. Dormant legacy `.sidebar` / `.topnav` styles in `app.css` still hard-code white rgba.
3. `dashboard/index.html` still has many inline styles (now with a valid text token).
4. Assessment/QC lack an in-flow appearance switcher UI.
5. EOS vs `app.css` stylesheet silo (CQ-006) — some Bootstrap remaps only apply when `app.css` loads.
6. Full page-by-page WCAG AA measurement with tooling (axe / Lighthouse) not run in CI here.
7. Founder empty states partially standardised (CSS) but not all templates use a single macro.

---

## Known Limitations

- This is a **foundation** pass, not a pixel-perfect redesign of every surface.
- Responsive ultra-wide polish and scrollbar theming beyond `color-scheme` were not exhaustively retuned.
- No product workflow copy or IA changes (those belong to UX-003/004 and educational programmes).
- Screenshot before/after gallery not committed.

---

## Remaining technical debt

See Technical Debt above. Highest follow-ups: (1) migrate Assessment/QC onto EOS shell like Study Session, (2) route shell buttons through `.ds-btn--*`, (3) purge dormant sidebar CSS, (4) axe CI smoke on key routes in light+dark.

---

## Recommendations

1. Treat `tokens.css` as the only place new colours may be introduced; PR checklist: “no new hex outside tokens/brand”.
2. Prefer `--chrome-text*` for any text sitting on permanent navy chrome; never `--text-primary` or `--brand-navy` for that job.
3. Prefer `--primary` / `--link` for emphasis on themed surfaces; never static `--brand-navy` / `--brand-midnight` as foreground.
4. Next craft milestone: collapse shell button variants onto `.ds-btn` with thin aliases.
5. Capture Light/Dark/System screenshots into `_evidence/` before Premium certification dogfood.

---

## Success criteria

| Criterion | Status |
|-----------|--------|
| Every page renders correctly in Light Mode | Pass for audited shells; residual silo risk noted |
| Every page renders correctly in Dark Mode | Pass for fixed root causes; Assessment/QC restored |
| No unreadable text (known nav/header cases) | Pass for Console active, timeline, chrome notes, phantom token |
| No inconsistent navigation (tokenised chrome) | Improved — topbar chrome tokens shared |
| No hard-coded colour conflicts (foundation) | Major conflicts fixed; dormant legacy remains |
| Shared design tokens used consistently | Expanded aliases; enforcement via tests |
| WCAG AA where practical | Chrome RC-001 suite green; navy-as-text bugs fixed |
| Premium visual consistency | Foundation established for future UI work |
