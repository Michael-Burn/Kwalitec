# PX-002B — Branding Implementation Report

The brief asks this programme to implement favicon, Apple touch icon, Open
Graph image, social preview image, manifest, consistent logo usage,
consistent lockup, and consistent page titles. This report verifies each
item against the current codebase and records the one gap that was found
and fixed.

## Verified already implemented (BI-001, prior work)

`app/templates/partials/brand_meta.html` is included from every root layout
(`layouts/base.html`, `student/base.html`, `layouts/console_base.html`,
`layouts/auth_base.html`, `session/base.html`) and provides:

| Requirement | Implementation | Asset |
|---|---|---|
| Favicon | `<link rel="icon">` for `.ico`, `.svg`, 32×32 and 16×16 PNG | `app/static/branding/favicon.ico`, `favicon.svg`, `favicon-32.png`, `favicon-16.png` |
| Apple touch icon | `<link rel="apple-touch-icon">` | `app/static/branding/apple-touch-icon.png` |
| Web app manifest | `<link rel="manifest">`, referencing 192/512/maskable icons | `app/static/branding/manifest.webmanifest` |
| Open Graph image | `og:image`, `og:title`, `og:description`, `og:type`, `og:site_name` | `app/static/branding/social-preview.png` |
| Social preview / Twitter card | `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image` | Same `social-preview.png` |
| Theme colour | `theme-color`, `application-name`, `apple-mobile-web-app-title` | — |
| Consistent logo usage | `partials/brand_logo.html`, included wherever the wordmark/icon appears (sidebar brand, auth pages) | `app/static/branding/*` |

All referenced asset files exist and are non-trivial in size (`favicon.ico`
647B, `apple-touch-icon.png` 17KB, `social-preview.png` 87KB, etc.) —
spot-checked via `ls -la app/static/branding/`. No missing or placeholder
assets were found. `tests/test_bi001_brand_identity.py` covers this surface
area; the one failing test in that file
(`test_approved_logo_is_single_display_source`) fails on `ModuleNotFoundError:
No module named 'PIL'` — a missing test dependency in this environment,
unrelated to any change in this programme (confirmed failing on `HEAD`
before this session touched anything).

## Gap found and fixed: page titles on student surfaces

**Before:** `layouts/base.html` and `student/base.html` both render
`<title>{{ title ~ ' · ' if title else '' }}Kwalitec</title>` — a
`title` variable set per-template. Legacy pages (`study_plan/*.html`, etc.)
already did this (`{% set title = 'Study Plan' %}`), but none of the five
canonical student templates (`journey.html`, `revision.html`, `history.html`,
`home.html`, `profile.html`) set it — every student page's browser tab
showed the bare fallback, "Kwalitec", regardless of which screen was open.

**After:** each of those five templates now sets
`{% set title = page.shell.page_title %}` immediately after `{% extends %}`,
reusing the same canonical title already computed for the on-page `<h1>`
(`page.shell.page_title`) — no new title strings were invented, and no
naming inconsistency was introduced between the tab title and the on-page
heading. Verified by rendering each route and inspecting the `<title>` tag:

| Route | `<title>` before | `<title>` after |
|---|---|---|
| `/student/` | Kwalitec | Home · Kwalitec |
| `/student/journey` | Kwalitec | Journey · Kwalitec |
| `/student/revision` | Kwalitec | Revision · Kwalitec |
| `/student/history` | Kwalitec | History · Kwalitec |
| `/student/profile` | Kwalitec | Settings · Kwalitec |

(The Profile route's canonical title is "Settings" — this is the existing,
already-correct value computed by `page.shell.page_title` for that surface;
this programme did not introduce or alter that naming, only surfaced it in
the browser tab.)

## Consistent lockup

The wordmark/icon lockup (`partials/brand_logo.html`) was reviewed across
sidebar, auth, and settings contexts — one component, parameterised by a
`brand_class` variable for sizing, used consistently everywhere the logo
appears. No duplicate or drifted logo markup was found; no change was
needed here.

## Summary

Branding infrastructure (favicon, touch icon, manifest, OG/social image) was
already complete and correctly wired from a prior initiative (BI-001); this
programme's contribution was verifying that implementation against the
PX-002B brief and closing the one real gap found — missing, inconsistent
page titles on the canonical student-facing routes.
