# Colour System

**Programme:** DX-001  
**Status:** Binding  
**Brand HEX ownership:** `knowledge/design/BRAND_GUIDELINES.md`  

---

## Philosophy

Create **semantic colour tokens only**.

Colour communicates **meaning**, not personality.

Avoid decorative colours. Do not invent seasonal or “fun” accents for product UI.

---

## Semantic roles

| Role | Purpose | Product use |
|---|---|---|
| **Primary** | Brand action and focus | Primary button, key links, focus ring, selected nav |
| **Secondary** | Quieter emphasis | Secondary button border/text, neutral emphasis |
| **Success** | Positive completion / healthy state | Validation passed, publish success, safe confirmation |
| **Warning** | Caution; proceed carefully | Soft blockers, stale data, capacity risk |
| **Danger** | Error / destructive / hard stop | Validation failures, delete, blocking errors |
| **Neutral** | Surfaces, text, borders | Backgrounds, body text, dividers, tables |

Optional semantic **Info** may alias Primary when a fourth status is required; do not introduce a decorative fifth hue.

---

## Brand mapping (canonical HEX)

These values are owned by Brand Guidelines; DX-001 assigns **roles**.

| Semantic role | Light UI binding | Notes |
|---|---|---|
| Primary | `#3B4FB8` (Primary Blue) | Primary actions always |
| Secondary | Neutral slate for chrome (`#475569` class) | Not a second brand colour |
| Success | Teal/green status (e.g. `#0f766e`) | Meaning only |
| Warning | Amber/brown status (e.g. `#A16207`) | Meaning only |
| Danger | Red status (e.g. `#c81e1e`) | Meaning only |
| Neutral surfaces | White / light grey canvas (`#FFFFFF`, `#F4F6F9`) | Calm professional field |
| Neutral text | `#1E2430` / `#4A5568` / `#5C6570` | Primary / secondary / muted |
| Chrome (dark shells) | Primary Dark `#0D1B2A`, Deep Navy `#0A1628`, Midnight `#020D24` | Navigation chrome, not body canvas by default |

**Gold `#E8B02B` is not a UI semantic colour.** Reserved for logo, achievement, certificates, premium indicators — never primary buttons, nav, links, or focus.

---

## Usage rules

1. **One Primary action colour per screen** for the main CTA.  
2. **Status colour only on status.** Do not colour whole cards “success green” for decoration.  
3. **Text remains Neutral** unless stating status or link.  
4. **Borders stay Neutral.** Do not rainbow-border panels.  
5. **Charts (when justified):** limited palette from semantic tokens; no decorative rainbow by default.  
6. **Dark theme** (if present): remap semantic roles for contrast; do not invent new hues.

---

## Backgrounds and elevation

| Layer | Treatment |
|---|---|
| Page background | Neutral canvas |
| Content surface | Neutral surface (usually white in light mode) |
| Elevation | Prefer **border + spacing**, not heavy shadow stacks |
| Shadow | Minimal or none in redesigns; hierarchy via type/space |

DX-001 prefers flat professional surfaces over soft “card lift” as the default importance signal.

---

## Anti-patterns

- Purple-to-indigo decorative gradients as product theme  
- Multi-colour KPI tiles  
- Gold as CTA  
- Success/Warning/Danger used as section decoration  
- Low-contrast muted text for primary instructions  
