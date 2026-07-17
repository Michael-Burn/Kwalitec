# IAHF-004A — Brand Infrastructure Implementation Report

**Programme:** Product Operations Programme (POP)  
**Sprint:** POP Sprint 1  
**Milestone:** IAHF-004A  
**Status:** Implementation complete  
**Date:** 2026-07-17  
---

## Summary

IAHF-004A establishes the **canonical Kwalitec brand asset system**. All product identity files now live under a single authoritative directory (`app/static/branding/`), with shared template partials for browser metadata and logo rendering.

This milestone does **not** redesign the UI. Login and authenticated chrome continue to use the existing layout; the previous inline layers SVG on the login page is replaced by the official constellation-K mark served from the canonical pack. Application colour tokens and typography are unchanged (deferred to IAHF-004B).

Governance alignment:

- **DP-001 One Source of Truth** — one branding directory; no competing logo copies.
- **PRODUCT_BLUEPRINT / DESIGN_PRINCIPLES** — identity infrastructure only; no educational behaviour change.
- **POP-002** — Founder Command Centre chrome continues to share `layouts/base.html`, so favicon/OG/manifest apply automatically.

---

## Brand Asset Inventory

Canonical directory: `app/static/branding/`

| Asset | Purpose |
|---|---|
| `logo-primary.svg` | Primary vector lockup (mark + wordmark) |
| `logo-primary.png` | Primary raster lockup |
| `logo-icon.svg` | Compact vector mark |
| `logo-icon.png` | Compact raster mark |
| `logo-white.svg` | White vector lockup for dark surfaces |
| `logo-white.png` | White raster lockup |
| `logo-monochrome.svg` | Single-colour (`currentColor`) lockup |
| `favicon.ico` | Browser tab icon (16 + 32 PNG-in-ICO) |
| `apple-touch-icon.png` | Apple touch icon (180×180) |
| `android-chrome-192.png` | Android / PWA icon (192×192) |
| `android-chrome-512.png` | Android / PWA icon (512×512) |
| `social-preview.png` | Open Graph / Twitter social preview |
| `manifest.webmanifest` | Web app manifest |
| `README.md` | In-directory inventory & usage notes |

Template partials:

| Partial | Role |
|---|---|
| `app/templates/partials/brand_meta.html` | Favicon, manifest, theme-color, OG/Twitter |
| `app/templates/partials/brand_logo.html` | Reusable logo `<img>` (variants: icon/primary/white/monochrome) |

Brand colours encoded in logo art / metadata (UI CSS tokens intentionally untouched):

- Deep Navy `#0D1B2A` (theme-color, manifest)
- Royal Blue `#3950A2`
- Soft Light `#F2F4F7`
- Gold Accent `#D4AF37` (social preview tagline only)

---

## Deprecated Assets

| Path | Status |
|---|---|
| Inline layers SVG previously in `app/templates/auth/login.html` | Removed; superseded by `logo-icon.svg` via `brand_logo` partial |
| `app/static/images/` as a brand home | Deprecated for branding — see `app/static/images/DEPRECATED.md`. Folder retained empty (`.gitkeep`) for possible non-brand imagery |
| Duplicate favicons / logos elsewhere under `app/static/` | None found (pre-IAHF-004A vacuum confirmed by POP-001) |

No legacy favicon or OG files were present to delete.

---

## Files Modified

### Created

- `app/static/branding/` (full asset pack listed above)
- `app/templates/partials/brand_meta.html`
- `app/templates/partials/brand_logo.html`
- `app/static/images/DEPRECATED.md`
- `tests/test_iahf004a_brand_infrastructure.py`
- `knowledge/releases/IAHF-004A_IMPLEMENTATION_REPORT.md` (this file)

### Modified

- `app/templates/layouts/base.html` — include brand metadata
- `app/templates/layouts/auth_base.html` — include brand metadata
- `app/templates/auth/login.html` — canonical logo mark (no layout redesign)
- `app/templates/partials/sidebar.html` — canonical logo mark beside existing wordmark
- `app/static/css/app.css` — sizing helpers for logo `<img>` only (`.landing-logo-mark`, `.sidebar-brand-mark`, flex alignment)
- `app/static/images/.gitkeep` — retained; branding redirected via `DEPRECATED.md`

### Unchanged (intentionally)

- Application colour tokens / typography
- Navigation structure and labels
- Internal Alpha badge (IAHF-004B / IAHF-005)
- Educational services, Twin, curriculum, Founder Command Centre logic

---

## Browser Metadata

| Concern | Implementation |
|---|---|
| Application / browser title | `{{ title }} · Kwalitec` (unchanged pattern) |
| Favicon | `branding/favicon.ico` + SVG `logo-icon.svg` |
| Apple touch icon | `branding/apple-touch-icon.png` |
| Web manifest | `branding/manifest.webmanifest` (`name`/`short_name`: Kwalitec) |
| Theme colour | `#0D1B2A` |
| Application name | `Kwalitec` (`application-name`, `apple-mobile-web-app-title`) |
| Open Graph image | `branding/social-preview.png` (`og:image`) |
| Social preview | Same asset via `twitter:image` + `summary_large_image` |
| Description | Existing `product_tagline` injected into `og:description` / `twitter:description` |

Both `layouts/base.html` and `layouts/auth_base.html` include `partials/brand_meta.html`, so Login, Dashboard, Founder Command Centre, and other authenticated pages share one metadata surface.

---

## Regression Testing

### Automated

```
python3 -m pytest tests/test_iahf004a_brand_infrastructure.py -q
```

**Result:** 23 passed (asset inventory, template wiring, HTTP login/dashboard/static serving).

Also run:

```
python3 -m pytest tests/test_iahf004a_brand_infrastructure.py tests/test_auth.py -q
```

### Manual verification checklist

| Check | Expected |
|---|---|
| Login / landing logo | Constellation-K mark + “Kwalitec” wordmark |
| Register | N/A — public registration not exposed |
| Student Dashboard | Sidebar mark loads; favicon in tab |
| Founder Command Centre | Same shell metadata/favicon via `base.html` |
| Favicon | Tab shows Kwalitec icon |
| Manifest | `/static/branding/manifest.webmanifest` serves JSON |
| PWA icons | 192 / 512 PNGs referenced by manifest |
| Static loading | No broken `/static/branding/*` references |
| Console | No missing-asset 404s for brand files |

---

## Known Limitations

Deferred to **IAHF-004B** (and related chrome milestones):

- Visual redesign / repositioning of logos beyond wire-up
- Applying brand colour tokens and Poppins typography to UI chrome
- Internal Alpha badge in navbar / dashboard / footer
- Replacing decorative feature SVGs (e.g. settings list icons) that are not product identity marks
- Full PWA install UX polish beyond standard manifest + icons

Technical note: SVG wordmarks use a system sans stack for portability; raster primary/white/social assets carry the approved mark treatment for contexts where SVG text rendering differs.

---

## Architecture Compliance

- Layering preserved: static assets + templates only; no business-rule changes in services.
- Curriculum V1/V2: **N/A** (untouched).
- No Alembic / schema impact.
- Backwards compatible: existing `url_for('static', …)` pattern; layouts remain the single include points.

---

## Migration Impact

None.

---

## Technical Debt

- Raster PNGs are derived brand renders; future brand refreshes should replace files in `app/static/branding/` only and keep partials unchanged.
- `logo-monochrome.svg` has no PNG twin (SVG `currentColor` is preferred for single-colour contexts).
