# Kwalitec Official Brand Pack (BI-000 / BI-001)

Permanent master brand assets.

## Display logo (single source of truth)

| Need | Use |
|---|---|
| **Any in-app logo** | `approved-kwalitec-logo.png` |
| Historical archive copy | `original/Approved-Kwalitec-Logo.png` (same bytes) |

The application must render `approved-kwalitec-logo.png` directly.
Do not recreate, redraw, approximate, or typeset the logo in SVG/CSS/HTML.

## Other pack contents

| Need | Use |
|---|---|
| Favicon / PWA icons | `icons/` (runtime copies under `app/static/branding/`) |
| Social preview | `social/og-logo.png` |
| Print / embroidery | `print/` (legacy derivatives — not for live UI) |
| Legacy vector experiments | `svg/` (obsolete for app display — do not wire into templates) |

## Specs

- Colours → `COLOUR_SPECIFICATION.md`
- Assets → `ASSET_INVENTORY.md`
- Exports → `EXPORT_INVENTORY.md`
- Guidelines → `knowledge/design/BRAND_GUIDELINES.md`
- App theme → `app/static/css/brand.css`

## Rules

- Live UI logo = `approved-kwalitec-logo.png` only.
- Do not apply CSS filters, tints, or aspect-ratio distortion to the logo.
- Runtime colour tokens come from `brand.css` / `app.css` — never hard-code Bootstrap blue.
