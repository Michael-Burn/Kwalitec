# BI-001D — Brand Pack Validation Report

## Regenerated assets

### `app/static/branding/logo-primary.png`
- **Source master:** `app/static/assets/branding/svg/logo-primary-light.svg` (byte-identical to runtime sibling SVG)
- **Before SHA-256:** `fb7af49633f3ab7d8068da407a21e2b2b2f428762fcddec302d62777cb086aef`
- **After SHA-256:** `4a157df5f1b1455877a8f3c4998d40cd75205127530e6ff3062249ea7bb9e848`
- **Reason:** Was dark-surface/white-text twin of logo-white (plus opaque white letterboxing). Regenerated as light-surface lockup matching logo-primary.svg.

### `app/static/branding/logo-white.png`
- **Source master:** `app/static/assets/branding/svg/logo-primary-dark.svg` (byte-identical to runtime sibling SVG)
- **Before SHA-256:** `6939e66df24f0751ce0f6bed7526efa261f45fb8bf4bdce9d87a3d7ad2883f0f`
- **After SHA-256:** `aeffc3d5c0c70b4d207e24df608f4815937ecb001ea77a098fca43e567a7dec3`
- **Reason:** Correct dark-surface colourway but had opaque white letterboxing (~82% edge white). Regenerated with true transparency from master SVG.

## Assets validated — no regeneration needed

All runtime SVGs already matched BI-000 pack masters. Icon/favicon/social PNGs matched pack exports and contain official `#3B4FB8` / `#E8B02B` mark geometry corresponding to the approved logo.

| Runtime | BI-000 master |
|---|---|
| logo-icon.svg | svg/logo-icon-dark.svg |
| favicon.svg | svg/logo-icon-light.svg |
| logo-primary.svg | svg/logo-primary-light.svg |
| logo-white.svg | svg/logo-primary-dark.svg |
| logo-monochrome.svg | svg/logo-monochrome-black.svg |
| favicon-*.png, apple-touch, android-chrome, maskable, social-preview, logo-icon.png | icons/* / social/og-logo.png / png/logo-icon.png |
