# Kwalitec Official Brand Pack (BI-000 / BI-001)

Permanent master brand assets. **Vector-first.** Hand-built SVG geometry from the approved logo (visual reference only — not auto-traced).

**BI-001** wires these masters into the live application via `app/static/branding/` (runtime copies) and `app/static/css/brand.css` (tokens).

## Quick start

| Need | Use |
|---|---|
| App header on dark chrome | `svg/logo-primary-dark.svg` |
| App header on light chrome | `svg/logo-primary-light.svg` |
| Compact mark | `svg/logo-icon-dark.svg` or `logo-icon-light.svg` |
| Favicon | `icons/favicon.svg` / `favicon.ico` |
| Social preview | `social/og-logo.png` |
| Approved master PNG | `original/Approved-Kwalitec-Logo.png` |
| Print / embroidery | `print/` mono SVG or PNG |

## Specs

- Colours → `COLOUR_SPECIFICATION.md`
- Assets → `ASSET_INVENTORY.md`
- Exports → `EXPORT_INVENTORY.md`
- Guidelines → `knowledge/design/BRAND_GUIDELINES.md`
- App theme → `app/static/css/brand.css`

## Rules

- Do not embed PNG/JPG inside SVG masters.
- Prefer live Inter for wordmarks in product UI; gold i-dot is a brand accent.
- Runtime UI should consume tokens from `brand.css` / `app.css` — never hard-code Bootstrap blue.
