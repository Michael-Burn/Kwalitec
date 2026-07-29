# Component Guidelines

**Programme:** DX-001  
**Status:** Binding  

---

## Principle

Reuse patterns. Invent a component only when no existing pattern fits — and document the exception.

Every component must support **one screen, one purpose** and **action over analytics**.

---

## Buttons

Exactly **one Primary** action per screen (viewport / primary task context).

| Variant | When |
|---|---|
| **Primary** | The single next best action |
| **Secondary** | Important alternative that is not the default path |
| **Ghost** | Low-emphasis action near content |
| **Text** | Tertiary / cancel / “view all” / quiet navigation |

Rules:

- Never two Primary buttons competing in the same viewport.  
- Destructive actions: Danger styling on confirm; never Primary blue for delete.  
- Disabled: reduced opacity; still explain *why* via adjacent status, not a paragraph tutorial.  
- Motion: fast press feedback only (`INTERACTION_PRINCIPLES.md`).

---

## Cards

Cards exist **only** when they group related content that must be perceived as one unit.

They do **not** exist for decoration, density theatre, or “dashboard look.”

| Allowed | Not allowed |
|---|---|
| Grouping a mission + its why + start action | Wrapping every KPI in a card |
| A bounded validation summary | Card grids that mirror database tables |
| A settings group with related fields | Nested cards inside cards |

Prefer:

- **Tables** for collections of similar records  
- **Sections + headings + spacing** for page structure  
- **Lists** for sequential tasks  

**Breaking change vs UX-001:** Cards are no longer “the primary information container.” Structure is primary; cards are optional grouping.

Avoid soft multi-layer shadows. Prefer border + spacing.

---

## KPI policy

**Default: no KPI cards.**

KPIs are allowed only if they **directly change user decisions**.

| Allowed examples | Forbidden examples |
|---|---|
| Blocking validation errors | Subjects created |
| Awaiting approval | Topics imported |
| Today’s study mission (actionable) | Database counts |
| Hard publish blockers | Total publications |
| | Historical totals |
| | “Engagement” vanity metrics |

If a number does not change what the user does next, remove it from the primary surface.

---

## Tables

Prefer clean tables over decorative cards for professional scanning.

Rules:

- Clear column headers (Supporting or Caption weight)  
- Body-sized cell text  
- Row hover subtle; no carnival striping  
- Row actions: Ghost/Text; one Primary only if the table’s purpose is a single bulk action  
- Empty table → Empty State pattern, not a fake card wall  

---

## Forms & inputs

- Labels above fields; Supporting Text for optional hints that survived content review  
- One column preferred; multi-column only when fields are truly paired  
- Errors: Danger text adjacent to field; do not rely on colour alone  
- Radius and focus: consistent with tokens; focus ring uses Primary  

---

## Badges & status chips

- Short labels (1–3 words)  
- Semantic colour background/text pairs only  
- Never use badges as section decoration  

---

## Navigation

- Calm; one system per shell  
- No duplicated actions between sidebar, top bar, and in-page hero  
- Active state via Neutral/Primary contrast — not loud colour blocks  
- See `INFORMATION_HIERARCHY.md` and `DASHBOARD_PHILOSOPHY.md`  

---

## Empty states

Every empty state includes **only**:

1. Why it is empty  
2. The next action  

Nothing more. No marketing paragraphs. No secondary KPI suggestions.

---

## Dialogs & progressive disclosure

- Dialogs for confirmations and focused tasks — not for dumping full pages  
- Prefer inline expand / detail panel for inspection  
- Native browser `alert` / `confirm` are not part of the design system  

---

## Charts

Charts are rare. Allowed only when they change a decision better than a number or table.

No decorative sparklines on every card.
