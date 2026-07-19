# Kwalitec Runtime Brand Assets (BI-001)

Served at `/static/branding/` (icons / PWA) and `/static/assets/branding/`
(approved logo master).

## Display logo (single source of truth)

| File | Use |
|---|---|
| `../assets/branding/approved-kwalitec-logo.png` | **Only** logo used in app UI (navbar, login, student shell, etc.) |

Do not recreate this mark with SVG, CSS, or separate wordmark text.
Replace that one PNG to update the logo everywhere.

## Browser / PWA chrome

| File | Use |
|---|---|
| `favicon.*` / `apple-touch-icon.png` / `android-chrome-*.png` | Browser & PWA |
| `social-preview.png` | Open Graph / Twitter |
| `manifest.webmanifest` | PWA manifest |

Canonical colour tokens: `../assets/branding/COLOUR_SPECIFICATION.md`
Template helper: `partials/brand_logo.html` + `app.brand_identity.APPROVED_LOGO_STATIC_PATH`
