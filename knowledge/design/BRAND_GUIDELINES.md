# Kwalitec Brand Guidelines

**Programme:** BI-000 — Official Vector Brand Pack  
**Status:** Permanent master brand assets  
**Source:** Approved Kwalitec logo (visual reference only — rebuilt as hand-authored SVG geometry, not traced)

---

## Mission of the brand

Kwalitec helps learners build mastery through structured curriculum, clear progress, and quality-first study. The brand should feel **simple, modern, premium, minimal, and timeless** — at home beside Stripe, Linear, Notion, GitHub, Vercel, and Figma.

---

## Logo philosophy

The mark unites three ideas in one symbol:

| Component | Meaning |
|---|---|
| **Book** (white page + blue left lobe) | Curriculum, knowledge, structured learning |
| **Stylised K** (blue stem + arms) | Kwalitec identity; open pages / letterform |
| **Gold ascending stroke + gold dot** | Growth, reach, quality — a learner rising |

The gold ascending stroke is the primary motion cue. It should always read as upward and forward.

**Construction rule:** All masters are **vector-first**. Paths are geometric Bézier constructions. No bitmap tracing. No embedded raster inside SVG.

---

## Colour palette

Canonical tokens live in `app/static/assets/branding/COLOUR_SPECIFICATION.md`.

| Token | HEX | CSS variable | Role |
|---|---|---|---|
| Primary Blue | `#3B4FB8` | `--brand-primary-blue` | Symbol K / book accents |
| Primary Dark | `#0D1B2A` | `--brand-primary-dark` | Light-surface lockups, mono black |
| Deep Navy | `#0A1628` | `--brand-deep-navy` | Elevated dark chrome |
| Midnight | `#020D24` | `--brand-midnight` | Dark canvases, OG, app icons |
| Gold | `#E8B02B` | `--brand-gold` | Ascending stroke, dots, accent |
| Gold Hover | `#F0C040` | `--brand-gold-hover` | Interactive gold states |
| White | `#FFFFFF` | `--brand-white` | Book page, dark-surface wordmark |
| Text Secondary | `#8B93A7` | `--brand-text-secondary` | Supporting copy on dark |
| Divider | `#1E2A3D` | `--brand-divider` | Rules / separators on dark |

Flat fills only in master artwork. Gradients and bevels in the approved PNG are **presentation effects**, not part of the permanent vector system.

---

## Typography

### Production recommendation

| Priority | Family | Why |
|---|---|---|
| **1 — Primary** | **Inter** (SemiBold / 600) | Closest match to the approved wordmark: geometric sans, double-story **a**, clean **t**, excellent UI coverage |
| 2 — Alternate | **Manrope** (SemiBold) | Slightly softer geometric tone; good marketing alternative |
| 3 — Alternate | **Sora** (SemiBold) | More distinctive display character for campaigns |
| 4 — Alternate | **Space Grotesk** | Tech-forward; use sparingly for headlines |

**Do not outline the wordmark** in product UI. Keep live text so the app can use the production font stack.

**Special rule:** The tittle (dot) on **i** in the wordmark is brand gold (`#E8B02B`), matching the symbol’s gold dot. SVG masters place a gold circle over the i; UI implementations should style the i-dot equivalently when customising.

Suggested tracking for lockups: approximately `-0.015em` to `-0.02em` at display sizes.

---

## Spacing (brand safe area)

### Unit

**1U = diameter of the gold dot** in the symbol masters (≈ 14.4 units in the symbol’s normalised space; scale with the rendered mark).

### Minimum clear space

Surround the full lockup or icon with **≥ 1U** of empty space on all sides. Prefer **1.5U** in marketing layouts.

```
        ← 1U →
    ╔═══════════════╗
    ║               ║
 1U ║   [LOGO]      ║ 1U
    ║               ║
    ╚═══════════════╝
        ← 1U →
```

### Symbol ↔ wordmark gap

In the primary lockup, leave approximately **1U–1.5U** between the symbol’s rightmost extent (excluding extreme gold tip optical overhang) and the wordmark’s first glyph.

### Minimum sizes

| Asset | Minimum |
|---|---|
| Icon only | **16 px** tall (favicon); prefer **24 px+** in UI |
| Primary lockup | **24 px** tall; prefer **32 px+** |
| Print embroidery | Icon ≥ **12 mm** tall |
| Print full lockup | ≥ **25 mm** tall |

---

## Icon usage

| File | Use when |
|---|---|
| `svg/logo-icon.svg` / `logo-icon-dark.svg` | Dark or coloured surfaces (white book) |
| `svg/logo-icon-light.svg` | Light surfaces (dark book) |
| `svg/logo-icon-mono-*.svg` | Single-colour stamps, embroidery, watermarks |
| `icons/favicon.*` | Browser tab |
| `icons/apple-touch-icon.png` | iOS home screen |
| `icons/android-*.png` / `maskable-icon.png` | PWA / Android |
| `icons/mstile-150.png` | Windows tile |

At **16 px**, favour the icon (not the full lockup). Preserve gaps between book, K, and gold so the mark does not muddy.

---

## Background rules

| Background | Recommended mark |
|---|---|
| Midnight / Deep Navy / Primary Dark | `logo-*-dark` (white book + white wordmark) |
| White / light grey | `logo-*-light` (dark book + dark wordmark) |
| Photography / busy imagery | Place on a solid midnight panel, or use monochrome white/black |
| Single-colour print | Monochrome black or white only |

**Never** place the dark lockup on black without checking contrast of blue/gold (usually fine). **Never** place the light lockup on midnight.

---

## Incorrect usage

Do **not**:

1. Stretch, skew, or rotate the mark non-uniformly  
2. Recolour gold or blue to off-palette hues  
3. Add drop shadows, glows, outlines, or gradients to masters  
4. Place the mark inside a competing shape that crops the gold tip  
5. Separate the gold dot from the ascending stroke as a “new” logo  
6. Replace Inter/Manrope with decorative or script fonts in the lockup  
7. Trace or embed the approved PNG inside SVG/PDF masters  
8. Use the old IAHF-era neural-book mark as the product logo  
9. Set clear space below **1U**  
10. Use the full lockup below **24 px** height  

---

## Accessibility

- Prefer **logo-icon-light** / **logo-primary-light** on light UI chrome so the book remains visible.  
- Gold on white alone is insufficient for small text; gold is an **accent**, not body text colour.  
- Maintain contrast: white or primary-dark wordmarks on their intended surfaces.  
- Provide accessible names (`aria-label="Kwalitec"`) on inline SVG.  
- Favicons use the light variant so the glyph reads on typical light tab chrome.

---

## File organisation

```
app/static/assets/branding/
  svg/          Master vectors
  png/          Raster exports (64–1024)
  icons/        Favicon, touch, PWA, tile
  social/       OG, Twitter/X, LinkedIn, GitHub
  print/        Large transparent PNG + CMYK-annotated SVG
  COLOUR_SPECIFICATION.md
  ASSET_INVENTORY.md
  EXPORT_INVENTORY.md
  README.md
```

Guidelines (this document): `knowledge/design/BRAND_GUIDELINES.md`

---

## Font recommendation (summary)

**Use Inter SemiBold (600) as the production wordmark font.**  
Fallbacks: Manrope, Sora, system UI sans. Keep text live; gold i-dot is a brand exception drawn as geometry.

---

## Confirmation

All BI-000 masters are **vector-first**, free of embedded raster artwork, and suitable for long-term product branding, print conversion, and multi-density export.
