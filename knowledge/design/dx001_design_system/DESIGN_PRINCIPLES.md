# Design Principles

**Programme:** DX-001  
**Status:** Binding  
**Companion:** `PRODUCT_DESIGN_MANIFESTO.md`

---

## 1. Minimal by Default

Everything must earn its place.

If removing an element improves the page, remove it.

Tests:

- Does this element change a decision or enable an action?  
- If the user already knows the product, is this still needed?  
- Would a professional peer mock this as “dashboard filler”?  

If any answer is no, cut it.

---

## 2. Professional First

Interfaces respect the user’s intelligence.

- Prefer **labels** over paragraphs.  
- Prefer **structure** over instruction.  
- Prefer **naming** over onboarding copy.  

Never write copy that teaches how to click a button. Redesign the control instead.

---

## 3. Action Over Analytics

Dashboards exist to help users decide what to do next — not to display database statistics.

Allowed metrics are those that **change the next action** (e.g. blocking validation errors, awaiting approval, today’s study mission).

Forbidden by default: subjects created, topics imported, total publications, historical totals, vanity counts.

See `DASHBOARD_PHILOSOPHY.md` and KPI policy in `COMPONENT_GUIDELINES.md`.

---

## 4. One Screen, One Purpose

Every screen answers exactly one question.

| Surface | Question |
|---|---|
| Founder Console | What should I work on next? |
| Student Home | What should I study next? |
| Subject Workspace | What is the next publication task? |
| Session | What is the work of this sitting? |
| Settings | What do I configure here? |

Secondary content belongs behind progressive disclosure, secondary routes, or detail panels — not in the primary viewport as equal peers.

---

## 5. Whitespace Is a Feature

Empty space is intentional.

Do not fill unused areas because they exist. Compression to “fit more” is a failure mode, not a virtue.

Spacing communicates hierarchy. See `SPACING_SYSTEM.md`.

---

## 6. Hierarchy Before Decoration

Use typography and spacing.

Not colour as personality.  
Not shadows as importance.  
Not oversized cards as structure.

Colour communicates **meaning** (success, warning, danger, primary action). Decoration do not create hierarchy.

---

## 7. Progressive Disclosure

Hide complexity until requested.

Never expose every detail, every metric, every document field, and every history row simultaneously.

Patterns:

- Summary → expand / detail  
- Primary action → secondary actions in menus or quieter variants  
- Status chip → full validation list on demand  
- Table row → detail drawer or page  

---

## 8. Consistency Beats Creativity

Reuse patterns. Never invent a new component unless no existing pattern fits.

One button hierarchy.  
One table rhythm.  
One empty-state shape.  
One navigation model per shell.

Creativity belongs in educational product value — not in chrome novelty.

---

## Decision order when uncertain

1. Remove  
2. Simplify  
3. Reuse an existing pattern  
4. Only then design something new — and document why  

---

## Failure modes (reject in review)

| Failure | Why it fails |
|---|---|
| KPI grid of database counts | Action diluted by analytics theatre |
| Multiple primary buttons | No clear next step |
| Paragraphs explaining the UI | Interface is unclear |
| Competing nav systems | Cognitive tax |
| Decorative cards / heavy shadows | Hierarchy via decoration |
| Oversized display headings on every page | Noise; body should dominate |
