# Kwalitec Brand Export Inventory

**Programme:** BI-000  
**Root:** `app/static/assets/branding/`

## PNG lockups & marks (`png/`)

| File | Sizes |
|---|---|
| `logo-primary-{64,128,256,512,1024}.png` | Transparent; dark-surface colour lockup |
| `logo-icon-{64,128,256,512,1024}.png` | Transparent; colour symbol |
| `logo-wordmark-{64,128,256,512,1024}.png` | Transparent; wordmark + gold i-dot |
| `logo-primary.png` | Alias of 512 |
| `logo-icon.png` | Alias of 512 |
| `logo-wordmark.png` | Alias of 512 |

## Application icons (`icons/`)

| File | Spec |
|---|---|
| `favicon.ico` | Multi-size 16 / 32 / 48 |
| `favicon.svg` | Vector favicon (light variant) |
| `favicon-16.png` | 16×16 |
| `favicon-32.png` | 32×32 |
| `favicon-48.png` | 48×48 |
| `apple-touch-icon.png` | 180×180 on midnight |
| `android-192.png` | 192×192 on midnight |
| `android-512.png` | 512×512 on midnight |
| `maskable-icon.png` | 512×512 maskable safe zone |
| `mstile-150.png` | 150×150 on primary dark |

## Social (`social/`)

| File | Spec |
|---|---|
| `og-logo.png` | 1200×630 Open Graph |
| `twitter-x-logo.png` | 1200×600 Twitter/X |
| `linkedin-square.png` | 400×400 LinkedIn |
| `github-profile.png` | 500×500 GitHub |

All social assets use the master symbol on midnight.

## Print (`print/`)

| File | Spec |
|---|---|
| `logo-primary-print.png` | Large transparent lockup |
| `logo-icon-print.png` | Large transparent icon |
| `logo-icon-mono-print.png` | Large mono icon |
| `logo-wordmark-print.png` | Large wordmark |
| `*-print.svg` | SVG copies with CMYK conversion notes |

Transparent backgrounds throughout. CMYK values are approximate targets for RIP conversion (see colour spec). Suitable for business cards, apparel/embroidery (mono), roll-ups, stickers, and slides after professional colour management.

## Validation checklist

- [x] SVGs render without embedded raster  
- [x] Transparent PNG backgrounds (non-canvas exports)  
- [x] Colour tokens consistent across masters  
- [x] Icon legible at 16–64 px; crisp at 512–1024 px  
- [x] Filenames match BI-000 programme structure  
