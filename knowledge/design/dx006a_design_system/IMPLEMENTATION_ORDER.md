# Implementation Order

**Programme:** DX-006A  
**Status:** Binding sequence for foundation build & DX-006B readiness  
**Release Candidate:** `RC-2026.07.29-01`  

---

## Law

```
Phase 1 Design Tokens
    ↓
Phase 2 Primitive Components
    ↓
Phase 3 Layout Components
    ↓
Phase 4 Operational Components
    ↓
Phase 5 Guardian Enforcement
```

Do not skip upward. Do not redesign pages until Phases 1–5 are done (page work = **DX-006B**).

DX-006A **delivers the specifications and Guardian law** for all phases. Code execution of Phases 1–5 may continue immediately after this programme using these docs as the acceptance criteria.

---

## Phase 1 — Design Tokens

**Goal:** Single canonical token source aligned to DX-001.

| Task | Target |
|---|---|
| Remap CSS type scale | `app/static/css/tokens.css` → 32/24/18/16/14/12 |
| Remap spacing law | Document aliases; gate new work to 4/8/16/24/32/48/64 |
| Align Python tokens | `src/presentation/design_system/{typography,spacing,colours,…}.py` |
| Z-index + opacity + motion | Ensure CSS + Python expose full `DESIGN_TOKEN_SPEC.md` |
| Tests | Extend `test_design_token_integrity.py` for DX-001 scale |

**Exit:** Every visual token has a canonical source; no new UI uses retired 12/40/28 scales.

---

## Phase 2 — Primitive Components

**Goal:** L1 catalogue implemented (or adapted) against tokens.

| Task | Notes |
|---|---|
| Button variants + one-Primary helper | Deprecate competing primary helpers |
| Form controls | Input, Textarea, Checkbox, Radio, Select, Toggle |
| Feedback primitives | Spinner, Skeleton, Toast, Empty, Loading, Error |
| Overlay primitives | Tooltip, Popover, Disclosure, Dialog |
| Markers | Badge; Chip only if justified call sites exist |
| Remove/deprecate Rejected | StatisticTile, ProgressRing chrome, etc. |

**Exit:** Each L1 has catalogue fields satisfied; token-only styles; a11y keyboard paths.

---

## Phase 3 — Layout Components

**Goal:** L2 composition primitives.

| Task | Notes |
|---|---|
| Page, Section, Container, Stack, Inline, Grid | |
| Sidebar, Header, Footer, Toolbar, Search Bar | Shell only |
| Table, List | Prefer over cards for collections |
| Card | Justified optional; document allowed variants only |

**Exit:** Pages can compose structure without local layout CSS invention.

---

## Phase 4 — Operational Components

**Goal:** L3 from DX-004 / DX-005.

| Component | Authority |
|---|---|
| Persistent Context Header / Session Context | DX-004C, DX-005C |
| Primary Action Strip | All OS surfaces |
| Stage Indicator | DX-004C |
| Current Work + Publication Queue | DX-004A |
| Mission Card + Learning Queue + Recent Progress | DX-005A |
| Search Results + Publication Status | DX-004B, DX-005B |
| Blocking Findings | DX-004C, DX-005C |
| Feedback Block | DX-005C |

**Exit:** No page-specific duplicates of these jobs remain in the foundation; pages only compose.

---

## Phase 5 — Guardian Enforcement

**Goal:** Process + automated checks where feasible.

| Task | Notes |
|---|---|
| `UI_GUARDIAN.md` includes G-1–G-12 | Done in DX-006A docs |
| Cursor rule `09-ui-templates.mdc` / `30-DESIGN.md` point to DX-006A | Follow-up in same wave |
| Optional lint | Flag hex in `app/templates` / component CSS outside tokens |
| PR checklist | Require Guardian G-1–G-12 |

**Exit:** Guardian rules enforce the design system for all subsequent UI.

---

## Explicitly deferred to DX-006B

- Founder Home / Subjects / Workspace template migration  
- Student Home / Choose Exam / Study Session template migration  
- Removal of legacy page chrome after composition  
- Visual QA scorecards per migrated surface  

---

## Coordination with surface UI execution

If Study Session or Home UI is implemented before full DX-006B, it **must** still consume Phases 1–4 contracts and pass Phase 5 Guardian — do not invent parallel primitives.

---

*Release Candidate: RC-2026.07.29-01*
