# Kwalitec Brand Assets (IAHF-004A)

Canonical product identity lives in this directory only.

Do **not** add logo, favicon, PWA, or social-preview assets under `app/static/images/` or elsewhere.

## Variants

| File | Role |
|---|---|
| `logo-primary.svg` / `.png` | Primary lockup (mark + wordmark) |
| `logo-icon.svg` / `.png` | Compact mark |
| `logo-white.svg` / `.png` | White lockup for dark surfaces |
| `logo-monochrome.svg` | Single-colour (`currentColor`) lockup |
| `favicon.ico` | Browser tab icon |
| `apple-touch-icon.png` | iOS home-screen icon |
| `android-chrome-192.png` / `512.png` | Android / PWA icons |
| `social-preview.png` | Open Graph / Twitter card image (**1200×630**) |
| `manifest.webmanifest` | Web app manifest |

**Runtime default:** templates prefer **SVG** via `brand_logo.html`. PNG rasters are fallback / PWA / social only and were compressed in V1SP-001B (resized lockups; OG crop 1200×630).

Brand colours (metadata / logo art / IAHF-004B chrome tokens):

- Deep Navy `#0D1B2A` (`--chrome`, `--brand` in light theme)
- Royal Blue `#3950A2` (`--brand-muted` / accent soft)
- Soft Light `#F2F4F7`
- Gold Accent `#D4AF37` (`--brand-gold` — Internal Alpha identity badge)

## Template usage

- Metadata: `partials/brand_meta.html`
- Logo mark: `partials/brand_logo.html`
- Internal Alpha badge: `partials/internal_alpha_badge.html`
- Shared footer: `partials/app_footer.html`
