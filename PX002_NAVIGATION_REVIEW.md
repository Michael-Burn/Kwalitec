# PX-002 — Navigation Review

**Programme:** PX-002 Founder Console Experience Elevation  
**Date:** 2026-07-31

---

## Primary navigation (after)

| Group | Items | Workflow |
|-------|-------|----------|
| Workspace | Home, Subjects, Curriculum Studio | Publish and manage curriculum |
| Community | Students, Feedback | Review people and submissions |
| Administration | Settings | Configure and reach Advanced tools |

Secondary (sidebar foot, muted):

- Search
- Switch Experience
- Enter Student Experience

---

## Changes delivered

1. **Grouped chrome** — `_sidebar.html` renders labelled groups instead of a flat six-item list.
2. **Feedback label aligned** — `FOUNDER_PRIMARY_NAV_LABELS` updated from Support → Feedback (matches live nav and page titles).
3. **Secondary actions demoted** — Search / Switch / Enter Student remain visually quieter in the sidebar foot.
4. **Active section mapping unchanged** — Feedback still maps to `support` section_id (stable routing); Advanced destinations still nest under Settings.

---

## What was not changed

- Endpoint routes and URL prefixes
- Number of primary items (≤6)
- Reachability of Advanced destinations via Settings
- “Curriculum Authority” brand tagline (product identity contract)

---

## Remaining navigation debt

- Nested Advanced *page titles* still use programme-era engineering names (Platform Intelligence, Evidence Gates, Vision Journal). Settings link labels are operational; page H1s were left intact to avoid breaking specialist tests and Founder muscle memory mid-validation.
- Horizontal legacy `founder-cc-nav` CSS retained for rare pages that still reference it.
