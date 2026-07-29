# Interaction Principles

**Programme:** DX-001  
**Status:** Binding  

---

## Philosophy

Motion is **subtle, fast, purposeful**. Never decorative.

Interactions should feel like professional tools (Linear, Stripe, Raycast): immediate feedback, minimal ceremony, clear consequences.

---

## Timing

| Token | Duration | Use |
|---|---|---|
| Press | ~100ms | Button press / scale |
| Fast | ~150ms | Hover, tooltip appear |
| Base | ~200ms | Colour/background transitions |
| Panel | ≤250ms | Drawers, expand/collapse |
| Page | ≤250ms | Route transition opacity if any |

Prefer **ease-out**. Avoid bounce, elastic, and long cinematic fades.

If motion does not clarify state change, remove it.

---

## Feedback

| Event | Response |
|---|---|
| Click Primary | Immediate pressed state; then navigate or show progress |
| Submit | Disable duplicate submit; show calm progress — not confetti |
| Success | Brief Success treatment; return focus to next useful control |
| Error | Danger message at point of failure; keep user input |
| Destructive | Confirm once; clear consequence language |

Never celebrate routine saves with modal theatre.

---

## Focus & keyboard

- Visible focus ring (Primary semantic) on all interactive elements  
- Logical tab order matching visual order  
- Escape closes overlays  
- Do not trap focus accidentally outside dialogs  

---

## Progressive disclosure in interaction

- Default view: next action + essential status  
- Details: expand, “View”, or secondary route  
- Power actions: menus, overflow, or settings — not equal Primary buttons  

---

## Loading

- Prefer skeletons that preserve layout over blank flashes  
- Prefer inline progress for known short waits  
- Never block the whole app for a partial panel refresh when avoidable  

---

## Anti-patterns

- Hover-only critical information  
- Animations longer than 300ms for routine UI  
- Parallel competing spinners  
- Native `alert` / `confirm` for product flows  
- Hover lift + shadow as the main affordance for clickability  
