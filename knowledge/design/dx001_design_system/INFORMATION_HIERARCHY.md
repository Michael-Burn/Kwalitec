# Information Hierarchy

**Programme:** DX-001  
**Status:** Binding  

---

## Purpose

Every screen must make three things obvious within seconds:

1. **What is important**  
2. **What should I do next**  
3. **What has changed** (only when relevant)

If those answers are unclear, the page fails review.

---

## One screen, one purpose

Define the screen’s single question first (`DESIGN_PRINCIPLES.md`). Everything on the page either:

- Answers that question, or  
- Is deferred via progressive disclosure  

Equal-weight panels answering different questions = hierarchy failure.

---

## Visual stack (top → bottom)

| Priority | Content |
|---:|---|
| 1 | Page Heading (task identity) |
| 2 | Primary next action (or the single decision object) |
| 3 | Decision-critical status (blockers, warnings) |
| 4 | Supporting structure (table, list, grouped fields) |
| 5 | Secondary actions and metadata |
| 6 | Rarely: historical / analytical detail |

Do not place analytics above the next action.

---

## Hierarchy tools (in order of preference)

1. **Position** (top / first)  
2. **Typography** (Page → Section → Body → Supporting → Caption)  
3. **Spacing** (section gaps vs tight clusters)  
4. **Weight** (semibold sparingly)  
5. **Semantic colour** (status and Primary only)  
6. **Border / divider** (quiet separation)  

Avoid relying on: shadows, card chrome, icon size, or decorative colour blocks.

---

## Navigation hierarchy

- One primary nav per shell  
- In-page actions must not duplicate sidebar destinations with equal visual weight  
- Breadcrumbs (when used) are Supporting Text — not a second hero  

---

## Density vs clarity

Professionals can scan dense tables. They cannot scan five competing hero cards.

Prefer:

- One strong primary column  
- Optional secondary column for context — quieter type and no Primary button  

---

## Progressive disclosure map

| Layer | Contains |
|---|---|
| L0 Primary viewport | Next action + critical blockers |
| L1 Expand / panel | Detail needed for the current decision |
| L2 Secondary page | Full history, raw documents, advanced config |
| L3 Admin / debug | Implementation detail — never student-facing |

Leakage of L3 into L0 is a premium failure (IDs, hashes, build stamps as chrome).

---

## Review questions

- Can the user state the next action without scrolling past decoration?  
- Are there multiple elements shouting “start here”?  
- Would removing half the cards improve comprehension?  
