# Design Token Spec

**Programme:** DX-006A  
**Status:** Binding — single source of truth for visual values  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001 Colour / Typography / Spacing / Interaction · Brand Guidelines  

---

## 1. Law

Nothing hard-coded in components or pages.

| Rule | Enforcement |
|---|---|
| No component defines colours directly | Use semantic colour tokens |
| No component defines spacing directly | Use spacing tokens |
| No component invents type sizes | Use type roles |
| No component invents radii, shadows, motion | Use elevation / radius / motion tokens |

**Canonical product sources (after Phase 1 remap):**

1. Spec: this document (law)  
2. CSS: `app/static/css/tokens.css`  
3. Python: `src/presentation/design_system/` (`colours`, `spacing`, `typography`, `radius`, `elevation`, `motion`, `layout`)  

Brand HEX ownership remains `knowledge/design/BRAND_GUIDELINES.md`.

---

## 2. Colour

### 2.1 Semantic roles

| Token | Role | Light binding (Brand) | Product use |
|---|---|---|---|
| `colour.primary` | Brand action / focus | `#3B4FB8` | Primary button, key links, focus ring, selected nav |
| `colour.primary-hover` | Primary hover | `#2F3F96` | Hover/active Primary |
| `colour.secondary` | Quiet emphasis | `#475569` | Secondary chrome text/border |
| `colour.success` | Positive completion | `#0f766e` | Passed validation, safe confirm |
| `colour.success-bg` | Success surface | `#e6f7f5` | Soft success field |
| `colour.warning` | Caution | `#A16207` | Soft blockers, stale |
| `colour.warning-bg` | Warning surface | `rgba(161,98,7,0.12)` | Soft warning field |
| `colour.danger` | Error / destructive | `#c81e1e` | Blocking errors, delete confirm |
| `colour.danger-bg` | Danger surface | `#fef1f1` | Soft danger field |
| `colour.info` | Informational (alias Primary) | `#3B4FB8` | Optional fourth status — not a decorative hue |
| `colour.background` | Page canvas | `#F4F6F9` | Page background |
| `colour.surface` | Content surface | `#FFFFFF` | Panels, tables |
| `colour.border` | Default border | `#d5dae3` | Dividers, inputs |
| `colour.border-subtle` | Quiet border | `#e6e9ef` | Soft separators |
| `colour.text` | Primary text | `#1E2430` | Body / headings |
| `colour.text-secondary` | Secondary text | `#4A5568` | Supporting |
| `colour.text-muted` | Muted text | `#5C6570` | Metadata |
| `colour.text-inverse` | On dark / on primary | `#f8fafc` | Chrome / on Primary |
| `colour.on-primary` | Text on Primary fill | `#f8fafc` | Primary button label |
| `colour.chrome` | Dark shell | `#0D1B2A` | Nav chrome |
| `colour.focus-ring` | Focus indicator | `0 0 0 3px rgba(59,79,184,0.28)` | Visible focus |

**Gold `#E8B02B` is not a product semantic UI colour.** Logo, achievement, certificates only — never CTAs, links, focus, or nav.

Dark theme remaps the same **roles**; does not invent new hues. See `tokens.css` `[data-theme="dark"]`.

### 2.2 Anti-patterns

- Hard-coded hex in templates or component CSS  
- Purple-indigo decorative themes  
- Rainbow KPI tiles  
- Status colour as whole-card decoration  

---

## 3. Typography

**Family:** Inter only (UI). Mono for codes/IDs only.

| Role | Token | Size | Weight | Line height | Tracking | Use |
|---|---|---:|---:|---:|---|---|
| Display | `type.display` | **32px** | 600 | 1.2 | −0.02em | Rare product moments — at most one per major surface |
| Page Heading | `type.page` | **24px** | 600 | 1.25 | −0.015em | Screen title — **one H1** |
| Section Heading | `type.section` | **18px** | 600 | 1.3 | −0.01em | Group label |
| Body | `type.body` | **16px** | 400 | 1.5 | 0 | Default reading / UI |
| Supporting | `type.support` | **14px** | 400 | 1.45 | 0 | Secondary labels, helpers |
| Caption | `type.caption` | **12px** | 500 | 1.4 | +0.01em | Timestamps, footnotes |
| Mono | `type.mono` | 14–16px | 400 | 1.45 | 0 | IDs, hashes, codes |

### 3.1 Breaking vs UX-001 / current Python TYPE_STYLES

| Legacy UX-001 / V3 | DX-006A (DX-001) |
|---|---|
| Display / page 40px | Page **24px**; Display **32px** exceptional |
| Section 28px | Section **18px** |
| Card title 20px | Section or Body semibold — no fourth “card title” tier |
| Caption 14px as micro | Supporting **14**; Caption **12** |

Phase 1 implementation **must remap** `TYPE_STYLES` and CSS `--font-*` aliases to this table.

---

## 4. Spacing

**8-point system.** Product UI allows **only**:

| Token | px | rem | Typical use |
|---|---:|---|---|
| `space.1` | 4 | 0.25 | Inline icon↔label |
| `space.2` | 8 | 0.5 | Control clusters, compact lists |
| `space.3` | 16 | 1 | Default component padding, form stack |
| `space.4` | 24 | 1.5 | Section / justified card padding |
| `space.5` | 32 | 2 | Between major blocks |
| `space.6` | 48 | 3 | Between page sections |
| `space.7` | 64 | 4 | Page breathing room |

### 4.1 Retired for product redesigns

| Value | Status |
|---|---|
| **12** | Retired — use 8 or 16 |
| **96** | Not product UI scale |
| **128** | Not product UI scale |

CSS may keep transitional `--space-md: 0.75rem` aliases until unmigrated pages move; **new components must not use 12/96/128**.

Python `SpacingToken.MD` (12), `XXXXXL` (96), `XXXXXXL` (128) are **non-canonical for DX redesigns** — remap or gate in Phase 1.

---

## 5. Elevation

DX-001 prefers **border + spacing** over shadow stacks.

| Token | Treatment |
|---|---|
| `elevation.none` | Flat surface |
| `elevation.border` | `1px` `colour.border` / `border-subtle` |
| `elevation.sm` | Minimal shadow only if border insufficient (`--shadow-sm`) |
| `elevation.md` | Rare — overlays |
| `elevation.lg` / `xl` | Avoid in product OS; marketing only if ever |

Default content surface: **border**, not lift.

---

## 6. Radius

| Token | rem | Use |
|---|---|---|
| `radius.sm` | 0.5 | Small controls, skeleton chips |
| `radius.md` | 0.75 | Inputs, buttons |
| `radius.lg` | 1 | Justified cards, panels |
| `radius.full` | 9999px | Avatars / true pills only when functional |

Do not invent per-component radii.

---

## 7. Motion & transitions

| Token | Duration | Easing | Use |
|---|---|---|---|
| `motion.press` | 100ms | ease-out | Button press |
| `motion.fast` | 150ms | ease-out | Hover, tooltip |
| `motion.base` | 200ms | ease-out | Colour / background |
| `motion.panel` | ≤250ms | ease-out | Expand / collapse |
| `motion.page` | ≤250ms | ease-out | Route enter opacity |

Respect `prefers-reduced-motion: reduce` — disable non-essential animation.

No bounce, elastic, confetti, or cinematic fades in product OS.

---

## 8. Opacity

| Token | Value | Use |
|---|---|---|
| `opacity.disabled` | 0.5 | Disabled controls |
| `opacity.muted` | 0.7 | De-emphasised chrome |
| `opacity.skeleton-min` | 0.55 | Skeleton pulse floor |
| `opacity.skeleton-max` | 1 | Skeleton pulse peak |

---

## 9. Breakpoints

| Token | Range | Columns (default grid) |
|---|---|---|
| `breakpoint.mobile` | &lt; 768px | 4 |
| `breakpoint.tablet` | 768–1023px | 8 |
| `breakpoint.desktop` | ≥ 1024px | 12 |

Containers:

| Token | Max width |
|---|---|
| `container.narrow` | 44rem (reading) |
| `container.content` | 60rem (default page) |
| `container.wide` | 72rem (shell) |
| `container.full` | none |

---

## 10. Z-index

| Token | Value | Layer |
|---|---:|---|
| `z.base` | 0 | Content |
| `z.sticky` | 100 | Persistent context / sticky header |
| `z.dropdown` | 200 | Select, popover |
| `z.overlay` | 300 | Dimmer |
| `z.dialog` | 400 | Modal dialog |
| `z.toast` | 500 | Toast |
| `z.tooltip` | 600 | Tooltip |

Do not invent ad-hoc z-index values in pages.

---

## 11. Shell metrics

| Token | Value | Use |
|---|---|---|
| `shell.sidebar-width` | 260px | Founder / student shell |
| `shell.topnav-height` | 56px | Top chrome |
| `shell.touch-target-min` | 2.75rem | Minimum interactive size |

---

## 12. Token coverage checklist

| Category | Covered |
|---|---|
| Colours (semantic + chrome) | ✓ |
| Typography roles | ✓ |
| Spacing scale | ✓ |
| Elevation | ✓ |
| Radius | ✓ |
| Motion / transitions | ✓ |
| Opacity | ✓ |
| Breakpoints / containers / grids | ✓ |
| Z-index | ✓ |
| Shell metrics | ✓ |

Every visual value in L1–L3 must map to a row above.

---

## 13. Implementation remap notes (Phase 1)

1. Align CSS `--font-*` to DX-001 sizes (24 / 18 / 16 / 14 / 12).  
2. Document `--space-*` aliases: map product work to `space.1`–`space.7`; deprecate 12/96/128 for new UI.  
3. Update Python `TYPE_STYLES` and `SPACING` allowed sets to match this spec.  
4. Keep Brand HEX imports intact.  
5. Do not migrate pages in Phase 1 — tokens only.

---

*Release Candidate: RC-2026.07.29-01*
