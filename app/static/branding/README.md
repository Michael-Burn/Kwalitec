# Kwalitec Runtime Brand Assets (PX-001)

Served at `/static/branding/` (icons / PWA) and `/static/assets/branding/`
(approved logo master).

## Display logo (single source of truth)

| File | Use |
|---|---|
| `../assets/branding/approved-kwalitec-logo.png` | **Only** logo used in app UI (navbar, login, student shell, etc.) |
| `../assets/branding/original/Final-Approved-Kwalitec-Logo.png` | Unaltered Final Approved master archive |

The display PNG originates from the Final Approved master. Navy canvas is keyed
for transparent layout integration — the mark itself is never redrawn or recoloured.

Do not recreate this mark with SVG, CSS, or separate wordmark text.
Replace from the Final Approved master to update the logo everywhere.

## Browser / PWA chrome

| File | Use |
|---|---|
| `favicon.*` / `apple-touch-icon.png` / `android-chrome-*.png` | Browser & PWA — derived from the approved mark |
| `social-preview.png` | Open Graph / Twitter |
| `manifest.webmanifest` | PWA manifest |

Canonical colour tokens: `../assets/branding/COLOUR_SPECIFICATION.md`
Template helper: `partials/brand_logo.html` + `app.brand_identity.APPROVED_LOGO_STATIC_PATH`

## Brand hierarchy (PX-001)

1. **Kwalitec** (logo / name)
2. **Education Operating System** (descriptor)
3. Supporting value proposition
4. Supporting copy
