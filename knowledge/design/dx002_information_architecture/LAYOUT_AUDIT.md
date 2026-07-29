# Layout Audit

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Focus:** Visual grouping, whitespace, alignment, reading flow, scanning, eye movement — architecture of attention, not CSS tokens.

---

## Ideal scanning model (DX-001)

```
Title
Primary action / decision object
Critical blockers
Supporting list/table
Secondary links (quiet)
```

Eye path: **F-pattern or single column** — not a KPI dashboard mosaic.

---

## Surface-by-surface

### Console Overview

| Aspect | Current | Target |
|---|---|---|
| Grouping | Header → 4-card grid → 4-card grid → Quick Actions → detail cards | Header → one next action → list |
| Whitespace | Filled with grids | Section gaps between action and list |
| Alignment | Card mosaic equal weight | Primary column left-weighted |
| Reading flow | Metrics before meaning | Action before analytics |
| Scan | Cannot answer “do X” in 3s when healthy | Single CTA obvious in 3s |

**Eye movement today:** Zigzag across 8 metric tiles before finding work. **Fail.**

### Curriculum Studio hubs

| Aspect | Current | Target |
|---|---|---|
| Grouping | Breadcrumb → header → next hint → workflow card → forms → table | Header → create/open → table |
| Flow | Tutorial before inventory | Inventory first for returning users |
| Scan | Repeated structure across 5 hubs trains blindness | One catalogue layout |

### Curriculum Workspace

| Aspect | Current | Target |
|---|---|---|
| Grouping | Vertical stack of many equal sections | Stage L0 block; details collapsed |
| Alignment | Full-width cards; 3-col KPI; 9-tab row | Primary action sticky/nearby; tabs ≤3 |
| Reading flow | Must scroll past upload/processing to Actions | Actions adjacent to Next step |
| Scan | Tab bar requires horizontal hunt | Stage-driven panels |

**Eye movement today:** Top-to-bottom through ~7 major bands before committing. **Fail.**

### Student Home

| Aspect | Current | Target |
|---|---|---|
| Grouping | Hero stack then secondary panels | Hero = title + why + CTA only |
| Whitespace | Interrupted by status/duration/purpose layers | One cluster, then optional disclosure |
| Flow | Correct intent (hero first) | Preserve; cut layers |
| Scan | Title competes with greeting/narrator/eyebrow | One title signal |

### History

| Aspect | Current | Target |
|---|---|---|
| Flow | Essay → CTAs → narrative → KPI grid → sessions | Sessions first |
| Scan | Teaching before archive | Archive first |

### Login

| Aspect | Current | Target |
|---|---|---|
| Grouping | Split: brand panel + form | Keep split; brand quieter |
| Flow | Feature list delays eye to form on large screens | Form primary; brand one sentence |
| Decorative shapes | Pull attention | Remove |

### Session activity

| Aspect | Current | Target |
|---|---|---|
| Flow | Question → controls → advance | Preserve |
| Scan | Generally supports focus | P3 polish only |

### Help

| Aspect | Current | Target |
|---|---|---|
| Flow | Search → long orientation → actions | Search → quick actions → short topics |
| Scan | Essay wall | Fail for “get unblocked” |

---

## Cross-cutting layout defects

1. **Equal-weight sections** — every `command-card` / `student-card` shouts equally.  
2. **Primary below the fold** — Workspace Actions after intelligence panel.  
3. **Horizontal overload** — 9 CIP tabs exceed comfortable scan.  
4. **Duplicate vertical rhythms** — Hub template clones inflate learning cost.  
5. **Legacy dual chrome** — Appearance + alpha badge + email in topnav compete with task.

---

## Layout principles for redesign

1. One primary column for decision surfaces.  
2. Place stage Primary within one viewport of Next step.  
3. Tables/lists for inventories; never metric mosaics on Homes.  
4. Progressive disclosure for L2; never parallel L0 panels.  
5. Breadcrumbs and badges stay visually quieter than Page Heading.
