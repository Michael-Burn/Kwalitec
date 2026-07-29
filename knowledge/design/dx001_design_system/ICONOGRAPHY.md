# Iconography

**Programme:** DX-001  
**Status:** Binding  

---

## Family

Use **one icon family only: Lucide Icons**.

Never mix icon libraries (Font Awesome, Heroicons, Bootstrap Icons, ad-hoc SVGs with different stroke systems) in product UI.

Brand mark / logo SVGs are brand assets, not Lucide — they remain under Brand Guidelines.

---

## Role of icons

Icons **support recognition**. They never replace labels.

| Allowed | Not allowed |
|---|---|
| Icon + text in nav | Icon-only primary nav for core destinations |
| Icon beside status for faster scan | Mystery icons without accessible names |
| Icon on Primary button when it clarifies action | Icon salad on KPI cards |

Every interactive icon requires an accessible name (`aria-label` or visible text).

---

## Size scale

| Size | Use |
|---:|---|
| **16px** | Inline with Supporting/Caption text; dense tables |
| **20px** | Default UI (buttons, list rows, form affordances) |
| **24px** | Navigation, section markers |
| **32px** | Rare empty-state or feature markers — not decoration on every card |

Maintain consistent stroke weight as provided by Lucide. Do not mix filled and outline styles arbitrarily within one toolbar.

---

## Colour

Icons inherit **Neutral** text colour by default.

Semantic colour only when the icon denotes Success / Warning / Danger / Primary interactive state.

Do not use Gold for general UI icons.

---

## Anti-patterns

- Different libraries on Founder vs Student shells  
- Oversized illustrative icons competing with Page Heading  
- Icons as the only carrier of meaning for irreversible actions  
- Animated decorative icons  
