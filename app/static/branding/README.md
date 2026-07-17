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
| `social-preview.png` | Open Graph / Twitter card image |
| `manifest.webmanifest` | Web app manifest |

Brand colours (metadata / logo art — UI chrome tokens unchanged in IAHF-004A):

- Deep Navy `#0D1B2A`
- Royal Blue `#3950A2`
- Soft Light `#F2F4F7`
- Gold Accent `#D4AF37` (social preview tagline only)

## Template usage

- Metadata: `partials/brand_meta.html`
- Logo mark: `partials/brand_logo.html`
