# Spacing System

**Programme:** DX-001  
**Status:** Binding  

---

## Philosophy

Adopt an **8-point spacing system**.

Spacing communicates hierarchy. It is not random padding.

Whitespace is intentional. Unused regions stay empty unless content earns them.

---

## Canonical scale

| Token | Value (px) | Rem (16px root) | Typical use |
|---|---:|---|---|
| `space-1` | **4** | 0.25 | Tight inline gaps (icon ↔ label), hairline insets |
| `space-2` | **8** | 0.5 | Related control clusters, compact list gaps |
| `space-3` | **16** | 1 | Default component padding, form field stack |
| `space-4` | **24** | 1.5 | Section internal padding, card content padding when cards are justified |
| `space-5` | **32** | 2 | Between major blocks within a column |
| `space-6` | **48** | 3 | Between page sections |
| `space-7` | **64** | 4 | Page top/bottom breathing room; major layout breaks |

**Only these values are allowed** in redesign work unless an explicit exception is recorded in the programme report.

---

## Hierarchy through space

| Relationship | Prefer |
|---|---|
| Label → control | 4–8 |
| Stacked form fields | 16 |
| Sibling cards / blocks (when cards exist) | 16–24 |
| Distinct sections | 32–48 |
| Page edge → content | 24–32 (mobile); 32–48 (desktop) |
| Primary action isolated from secondary | Extra 8–16 above secondary cluster |

Larger gap = weaker association. Smaller gap = stronger association.

---

## Layout density

Professionals tolerate **focused density**. Density is not clutter.

| Mode | When |
|---|---|
| Comfortable | Student Home, Founder Console primary viewport — generous section gaps |
| Efficient | Tables, Curriculum Studio lists, validation findings — tighter row rhythm (8–16) |

Never “fill the dashboard” with cards to remove whitespace.

---

## Legacy note (breaking)

UX-001 allowed **12, 96, 128**. DX-001 canonical set is **4, 8, 16, 24, 32, 48, 64**.

- **12** is retired for redesigns (use 8 or 16).  
- **96 / 128** are not part of the product UI scale; reserve for marketing / print if needed outside product shells.

Existing `tokens.css` may retain transitional aliases until a later DX implementation programme remaps them. New redesigns must target this scale.

---

## Anti-patterns

- Arbitrary values (`13px`, `18px`, `22px` padding)  
- Equal padding on every box regardless of content importance  
- Collapsing section gaps to fit more KPI cards  
- Large empty decorative frames that still feel “busy” because of borders and shadows  
