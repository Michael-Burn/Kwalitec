# ILE-001A — Accessibility Checklist

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001A  
**Status:** Active (infrastructure / standards)  
**Effective:** 2026-07-28  
**Implementation:** `app/application/adaptive_assessment/accessibility.py`

---

## Purpose

Ensure Adaptive Assessment components expose accessible labels, keyboard support, semantic structure, screen-reader descriptions, and reduced-motion compatibility — without a UI redesign in this milestone.

---

## Checklist (required for every AA surface)

| Requirement | Standard |
|---|---|
| Accessible label | Region / control has a clear accessible name (e.g. “Learning check: Quick Check”) |
| Keyboard navigation | All actions operable by keyboard; focus order matches reading order |
| Semantic structure | Prefer landmarks / regions (`role="region"` or equivalent) |
| Screen-reader description | Purpose + effort estimate available to AT |
| Explain control | Accessible name for “Why am I seeing this?” |
| Defer / pause | Accessible names; not mouse-only |
| Reduced motion | Honour `prefers-reduced-motion`; no essential info in motion alone |
| Colour | Correct/incorrect / state never colour-only |
| Focus visible | Visible focus indicator on interactive controls |

---

## Infrastructure API

```python
from app.application.adaptive_assessment import accessibility_for_session

meta = accessibility_for_session("quick_check")
# meta.accessible_label, meta.screen_reader_description,
# meta.keyboard_navigable, meta.reduced_motion_compatible, ...
```

`reduced_motion_safe(prefers_reduced_motion=...)` returns whether non-essential motion may run.

---

## Non-goals (ILE-001A)

- Visual redesign  
- Full WCAG audit of live pages (no AA UI yet)  
- Custom component library  

Implementers of ILE-001B+ must satisfy this checklist when building UI.

---

**End of ACCESSIBILITY_CHECKLIST**
