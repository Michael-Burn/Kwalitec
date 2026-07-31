# PX-004 — Visual Consistency Report

**Programme:** Product Experience Programme PX-004 — Premium Craft & Release Polish  
**Date:** 2026-07-31

---

### Audit scope

Typography, spacing, padding, margins, cards, grids, buttons, inputs, tables, sections, headings, badges, icons, radius, shadow, borders — Student OS and Founder Console.

### One visual language — corrections

| Inconsistency | Before | After |
|---------------|--------|-------|
| Success flashes on Console | `student-success` class with no Console CSS | Shared `.ds-flash` / `.ds-flash--*` in `design_system.css` |
| Button hover coverage | Only primary had hover | Secondary, ghost, danger hover + active |
| Badge `neutral` | Modifier emitted, no CSS | `.ds-badge--neutral` |
| Origin badges | Hard-coded blue/purple/green hex | Token colours (`--primary`, `--info-bg`, `--success`, …) |
| Disclosure focus | `outline: 2px solid var(--focus-ring)` (invalid — token is box-shadow) | `box-shadow: var(--focus-ring)` |
| Empty reason weight | Title and reason same weight when both present | Reason demotes to body when title exists |
| Feedback / Students CTAs | Bootstrap `btn btn-sm` | `console-btn` primary/secondary |
| Settings Advanced labels | “System Operations”, “Runtime status” | “System health”, “Service status” |

### Spacing & radius

- Founder origin badges aligned to `--space-1` / `--space-2` and `--radius-sm`.
- Flash padding uses DS `--space-3` / `--space-4` / `--space-5`.
- Card radius left on existing `--radius` / `--radius-lg` (no wholesale Founder rem rewrite — avoids churn).

### Heading hierarchy

| Page | Fix |
|------|-----|
| Student Profile | Suppress shell `page_header`; single Settings `h1` |
| Student Journey | Unique `needs-attention-building-title` for building state |
| History empty | Title + one sentence (no duplicate explanation) |

### Remaining visual debt

1. Mixed Console chrome on legacy command-card pages (Vision, Operational Health detail).
2. Founder still uses `--space-md` / `--space-xl` aliases alongside `--space-4` — compatible via tokens, not fully renamed.
3. Student Settings CSS still lives in `student.css` rather than DS primitives.

### No redesign

Layouts and workflows unchanged. Token and class alignment only.
