# IAHF-004B — Brand Experience & Application Shell Implementation Report

**Programme:** Product Operations Programme (POP)  
**Sprint:** POP Sprint 1  
**Milestone:** IAHF-004B  
**Status:** Implementation complete  
**Date:** 2026-07-17  

---

## Summary

IAHF-004B applies the canonical brand infrastructure from IAHF-004A across the live application shell so Kwalitec reads as one coherent product — without redesigning layouts, navigation, or educational workflows.

Delivered:

- Ambient **Internal Alpha** identity (gold-accent badge) throughout authenticated chrome, login, and shared footers
- Consistent **canonical logo** usage via existing brand partials
- Official **Founder Command Centre** naming on all Founder user-facing templates (legacy “Founder Dashboard / Operating System / Research Command Centre” labels removed from UI copy)
- Student **Learning Workspace** identity on Dashboard, Study Plan list, Study Session, and Analytics headers
- Shared footer identity: `Kwalitec v{version}` + Internal Alpha · Founding Cohort · Build RC2
- Brand colour tokens aligned to Deep Navy / Royal Blue / Gold for chrome and the Alpha badge only

Governance alignment:

- **DP-007 Consistency** — one terminology and chrome pattern across surfaces
- **DP-002 One Entry Point** — Founder naming reinforces a single Command Centre; student home remains Student Dashboard
- **POP-002** — Founder Command Centre is the sole Founder product name in UI
- **Educational integrity** — no Twin, recommendations, evidence, or curriculum logic changes

---

## Branding Changes

| Area | Change |
|---|---|
| Brand identity module | `app/brand_identity.py` — programme labels (Internal Alpha, Founding Cohort, RC2) and official area names |
| Alpha badge partial | `partials/internal_alpha_badge.html` — compact / full / footer variants |
| Shared footer | `partials/app_footer.html` — version + Alpha identity on authenticated and public layouts |
| Sidebar | Canonical logo retained; compact Alpha badge under wordmark |
| Topnav | Full Alpha badge (Internal Alpha · Founding Cohort) beside appearance controls |
| Login / landing | Full Alpha badge under logo; onboarding note still available when EI Alpha is enabled |
| CSS tokens | `--chrome` / `--brand` → Deep Navy `#0D1B2A`; `--brand-gold` `#D4AF37` for Alpha identity |
| Student Dashboard | Eyebrow **Learning Workspace**; title **Student Dashboard** |
| Study Plan list | Standard `section-header` pattern (removed nested padded container / display-6) |
| Mission / Analytics | Learning Workspace eyebrow for workspace cohesion |
| Founder templates | Eyebrows use **Founder Command Centre / {Section}**; heritage templates renamed |

---

## Pages Reviewed

| Surface | Path / template | Branding result |
|---|---|---|
| Landing / Login | `/auth/login` | Canonical logo + Alpha identity + shared footer |
| Register | N/A (not publicly exposed) | — |
| Student Dashboard | `/dashboard/` | Learning Workspace identity + shell badge |
| Study Plan list | `/study-plan/plans/all` | Section header + Learning Workspace |
| Study Session | `/missions/` | Learning Workspace eyebrow |
| Analytics | `/analytics/` | Learning Workspace eyebrow |
| Settings | `/settings/` | Shell Alpha badge + existing Alpha status section |
| Product Check-in | `/research/checkin` | Shell identity preserved |
| Thank-you / dismiss | research templates | Shared shell via `base.html` |
| Founder Overview | `/founder/` | Founder Command Centre naming + Alpha chrome |
| Attention / Feedback / Findings / Research / Internal Alpha / Participants / Operations / Releases / Settings | `/founder/*` | Consistent Command Centre eyebrows |
| Finding detail / Review | Founder + heritage research templates | Command Centre labelling |
| Heritage FOS index | `founder_dashboard/index.html` | Renamed (not primary HTTP home) |
| Heritage Research Centre | `research/founder_dashboard.html` | Relabelled as Feedback under Command Centre |
| Errors 403/404/500 | error templates | Inherit layout / public chrome where applicable |
| Calibration Alpha | `calibration/alpha.html` | Unchanged educational “Alpha” capability naming (not brand chrome) |

---

## Consistency Improvements

### Branding
- One logo partial, one Alpha badge partial, one footer partial
- Gold accent reserved for Internal Alpha identity (not decorative noise)

### Typography
- Section headers standardised (`section-eyebrow` / `section-title` / `section-description`)
- Study Plan list aligned to the same hierarchy (no competing `display-6`)
- Existing font stack preserved (no typeface redesign)

### Spacing
- Removed double-padding wrapper on Study Plan list
- Alpha badge spacing integrated into sidebar brand block and topnav end cluster
- Main content `py-4` shell spacing unchanged

### Page headers
- Student surfaces: Learning Workspace identity
- Founder surfaces: Founder Command Centre / section breadcrumbs

### Shell
- Sidebar + topnav + footer form a single ambient brand frame on authenticated pages
- Public auth layout shares the same footer identity

### Navigation
- Labels and destinations unchanged (Dashboard, Study Plan, Study Session, Founder, Settings, Share Feedback)
- No new nav items; no route changes

---

## Accessibility Checks

| Check | Result |
|---|---|
| Colour contrast — Alpha badge on light surfaces | Gold border + dark text on soft gold wash; readable at `font-xs` |
| Colour contrast — Alpha badge on sidebar / landing (dark) | Light text on translucent gold wash; gold mark retained |
| Logo visibility | Canonical SVG mark on dark chrome and landing hero |
| Focus indicators | Existing `--focus-ring` and `:focus-visible` rules unchanged |
| Keyboard navigation | No new interactive controls; badge is `role="status"` (non-focus-trapping) |
| Responsive | Topnav full badge hidden below `md`; compact sidebar badge remains; footer wraps |
| Screen-reader title | Badge `title` includes full Internal Alpha · Founding Cohort · Build RC2 |

No accessibility regressions introduced intentionally; focus and sidebar toggle behaviour preserved.

---

## Tests Executed

### Automated

```bash
python3 -m pytest \
  tests/test_iahf004b_brand_experience.py \
  tests/test_iahf004a_brand_infrastructure.py \
  tests/test_qs001_ptp005_cohesion.py \
  tests/test_auth.py \
  tests/test_iahf003_founder_command_centre.py \
  -q
```

**Result:** 69 passed

Coverage includes: identity constants, template wiring, login/dashboard/settings/check-in shell HTML, Founder naming, Study Plan header pattern, prior brand infrastructure, version footer cohesion, auth, Command Centre routes.

### Manual verification

| Viewport | Checks |
|---|---|
| Desktop | Shell logo, Alpha badge in sidebar + topnav + footer, Student Dashboard header, Founder Overview eyebrow |
| Tablet | Topnav full badge visible at `md+`; section headers wrap cleanly |
| Mobile | Compact sidebar badge; topnav full badge hidden; footer wraps; hamburger nav intact |

### Responsive verification

- Sidebar sticky/off-canvas behaviour unchanged
- Footer flex wrap for version + Alpha line
- Landing Alpha identity sits under logo without layout redesign

---

## Known Limitations

- Poppins / full brand typeface swap deferred — existing Segoe/system stack retained to avoid a visual redesign
- Primary interactive blue (`--primary`) intentionally unchanged for familiarity; brand Royal Blue applied to chrome soft accents
- Heritage FOS / Research templates remain in tree for compatibility but are not Founder homes (IAHF-003)
- Full multi-device visual QA on physical devices remains a release-gate recommendation beyond automated HTML assertions
- Calibration page “Alpha” language is educational capability naming, not Internal Alpha chrome

---

## Files Created

- `app/brand_identity.py`
- `app/templates/partials/internal_alpha_badge.html`
- `app/templates/partials/app_footer.html`
- `tests/test_iahf004b_brand_experience.py`
- `knowledge/releases/IAHF-004B_IMPLEMENTATION_REPORT.md` (this file)

## Files Modified

- `app/__init__.py` — inject brand identity into template context
- `app/dashboard/routes.py` — page title Student Dashboard
- `app/static/css/app.css` — brand tokens, Alpha badge, footer, topnav-end, landing identity
- `app/static/branding/README.md` — document chrome token usage
- `app/templates/layouts/base.html` — shared footer
- `app/templates/layouts/auth_base.html` — shared footer
- `app/templates/partials/sidebar.html` — Alpha badge
- `app/templates/partials/topnav.html` — Alpha badge cluster
- `app/templates/auth/login.html` — landing Alpha identity
- `app/templates/dashboard/index.html` — Learning Workspace / Student Dashboard
- `app/templates/study_plan/list.html` — section header consistency
- `app/templates/mission/index.html` — Learning Workspace eyebrow
- `app/templates/analytics/index.html` — Learning Workspace eyebrow
- Founder Command Centre templates (eyebrows / heritage naming)
- Heritage research Founder templates (naming)

## Migration Impact

None.

## Architecture Compliance

- Layering preserved: presentation/templates/CSS only; no service maths or educational writes
- Curriculum V1/V2: **N/A** (untouched)
- Founder IA (POP-002): naming and ambient Alpha chrome only; section tree unchanged
- No business-logic or Twin changes

## Technical Debt

- Duplicate historical CSS blocks for `.topnav .navbar` remain pre-existing; not cleaned in this milestone to limit scope
- Raster vs SVG wordmark differences noted in IAHF-004A still apply

---

## Acceptance Criteria

| Criterion | Status |
|---|---|
| One consistent visual identity | Met |
| Canonical logo appears consistently | Met |
| Internal Alpha identity throughout authenticated areas | Met |
| Founder Command Centre terminology consistent | Met |
| Student experience feels cohesive | Met |
| No functionality / educational logic changes | Met |
| No regressions in covered automated suites | Met |
