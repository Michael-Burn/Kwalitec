# Accessibility Standard

**Programme:** DX-006A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Target:** WCAG **2.2 Level AA** minimum  

---

## 1. Principles

1. **Keyboard first** — every action available without a pointer.  
2. **Visible focus** — `colour.focus-ring` token; never `outline: none` without replacement.  
3. **Semantic HTML first** — ARIA only when native semantics are insufficient.  
4. **Name, role, value** — every control exposes an accessible name.  
5. **Colour is not the only signal** — status uses text + tone.  
6. **Contrast** — text and UI components meet AA against adjacent backgrounds.

---

## 2. Contrast

| Content | Minimum ratio |
|---|---|
| Normal text (&lt;18px / &lt;14px bold) | 4.5:1 |
| Large text | 3:1 |
| UI components & graphical objects | 3:1 |

Validate with `presentation.design_system.contrast` helpers and/or equivalent audits. Dark theme must pass independently.

Gold on white/dark for **UI chrome** is out of scope — gold is not a UI semantic colour.

---

## 3. Keyboard behaviour (global)

| Key | Behaviour |
|---|---|
| Tab / Shift+Tab | Move focus in visual order |
| Enter / Space | Activate buttons; Space toggles checkboxes/switches |
| Escape | Close Dialog, Popover, Tooltip |
| Arrows | Radios, listboxes, Stage Indicator where documented |

Focus must not trap outside Dialogs. Dialogs trap and restore focus on close.

Skip link to `<main>` on shells.

---

## 4. Screen reader

- Page: one `h1`; logical `h2`/`h3`.  
- Landmarks: `header`, `nav`, `main`, `footer` as applicable.  
- Live regions: Toasts and Loading use polite `status` unless error requires assertive.  
- Images/icons: decorative → `aria-hidden`; functional → text alternative.  
- Forms: labels; errors via `aria-describedby` + `aria-invalid`.

---

## 5. Component-level requirements

| Component | Extra rule |
|---|---|
| Button loading | `aria-busy`; do not remove accessible name |
| Dialog | `aria-modal="true"`; labelled by title |
| Toggle | `role="switch"` + `aria-checked` |
| Disclosure | `aria-expanded` |
| Empty / Error | Clear heading + actionable control |
| Badge status | Text conveys state |

---

## 6. Motion

Respect `prefers-reduced-motion`. Skeleton pulse and page enter animations disable or become static opacity.

---

## 7. Touch

Minimum target: `shell.touch-target-min` (2.75rem) for primary interactive controls on touch breakpoints.

---

## 8. Forbidden

- Focus removed without visible replacement  
- Icon-only Primary without accessible name  
- Error indicated by colour alone  
- Auto-playing motion that cannot be stopped  
- Captchas / puzzles as default product flow  

---

## 9. Verification (implementation)

Before shipping a migrated surface (DX-006B):

- [ ] Keyboard-only walkthrough of Primary path  
- [ ] Screen reader spot-check of L0 + forms  
- [ ] Contrast check light + dark  
- [ ] Reduced-motion check  

---

*Release Candidate: RC-2026.07.29-01*
