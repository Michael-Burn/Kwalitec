# Component Catalogue

**Programme:** DX-006A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Documentation standard:** Every entry satisfies `COMPONENT_STANDARDS.md`  

---

## How to read this catalogue

- **Status:** `Canonical` (in foundation) · `Justified optional` · `Rejected`  
- **Level:** L1 Primitive · L2 Layout · L3 Operational  
- Components **compose tokens only** — no hard-coded colour/space/type.

---

# Level 1 — Primitive Components

## Button

| Field | Spec |
|---|---|
| **Purpose** | Trigger the user’s next action or a secondary alternative |
| **When to use** | Any explicit action; Primary for the single next-best action |
| **When NOT to use** | Navigation that is merely a link (use Link); decorative chrome |
| **Inputs** | `label`, `variant` (primary \| secondary \| ghost \| text \| danger), `disabled`, `loading`, `type` (button \| submit), `aria-describedby` |
| **Outputs** | Click / submit event |
| **States** | Default, hover, focus, active, disabled, loading |
| **Accessibility** | Native `<button>`; accessible name = label; loading announced via `aria-busy` |
| **Keyboard** | Enter / Space activate; focus visible |
| **Responsive** | Full-width optional on mobile for Primary only when layout requires |
| **Examples** | Resume Work · Start Mission · Publish · Cancel (text) |
| **Anti-patterns** | Two Primaries on one page; Primary blue for delete; icon-only without name |

**Rule:** Exactly **one** Primary-variant Button per page.

---

## Input

| Field | Spec |
|---|---|
| **Purpose** | Single-line text entry |
| **When to use** | Names, emails, search queries, short fields |
| **When NOT to use** | Multi-line (Textarea); binary (Checkbox/Toggle); enumerated (Select/Radio) |
| **Inputs** | `label`, `name`, `value`, `placeholder` (avoid as sole label), `required`, `error`, `disabled`, `autocomplete` |
| **Outputs** | Current string value |
| **States** | Default, focus, disabled, error, readonly |
| **Accessibility** | `<label for>`; error linked via `aria-describedby`; `aria-invalid` when error |
| **Keyboard** | Tab focus; standard text editing |
| **Responsive** | Width 100% of container; touch target ≥ `shell.touch-target-min` |
| **Examples** | Subject name · Email |
| **Anti-patterns** | Placeholder-only labels; colour-only error |

---

## Textarea

| Field | Spec |
|---|---|
| **Purpose** | Multi-line text entry |
| **When to use** | Notes, reflection after practice, longer descriptions |
| **When NOT to use** | Single-line fields; chat walls on Session by default |
| **Inputs** | Same as Input + `rows` |
| **Outputs** | String |
| **States** | Default, focus, disabled, error |
| **Accessibility** | Labelled; error described |
| **Keyboard** | Tab; Enter inserts newline (unless form submit shortcut documented) |
| **Responsive** | Fluid width; min-height from tokens |
| **Examples** | Post-session reflection |
| **Anti-patterns** | Pre-practice journal modals on Session (DX-005C) |

---

## Checkbox

| Field | Spec |
|---|---|
| **Purpose** | Toggle independent boolean options |
| **When to use** | Multi-select filters; accept terms; optional flags |
| **When NOT to use** | Exclusive choice (Radio); immediate settings switch (Toggle) |
| **Inputs** | `label`, `checked`, `disabled`, `indeterminate` (lists) |
| **Outputs** | Boolean / set of values |
| **States** | Unchecked, checked, indeterminate, disabled, focus |
| **Accessibility** | Native input or `role="checkbox"` with `aria-checked` |
| **Keyboard** | Space toggles |
| **Responsive** | Hit area ≥ touch minimum |
| **Examples** | Filter “Ready only” |
| **Anti-patterns** | Using checkbox for single Primary confirmation path |

---

## Radio

| Field | Spec |
|---|---|
| **Purpose** | Choose exactly one option from a small set |
| **When to use** | 2–5 mutually exclusive options visible at once |
| **When NOT to use** | Many options (Select); binary on/off (Toggle) |
| **Inputs** | `name`, `options[]`, `value`, `disabled` |
| **Outputs** | Selected value |
| **States** | Unselected, selected, disabled, focus |
| **Accessibility** | `radiogroup` + labelled radios |
| **Keyboard** | Arrow keys move selection within group |
| **Responsive** | Stack vertically on mobile |
| **Examples** | Difficulty preference (when justified) |
| **Anti-patterns** | Radio for unrelated multi-select |

---

## Select

| Field | Spec |
|---|---|
| **Purpose** | Choose one (or documented multi) from a longer list |
| **When to use** | ≥6 options; space-constrained forms |
| **When NOT to use** | Primary navigation; stage switching (use Stage Indicator) |
| **Inputs** | `label`, `options`, `value`, `disabled`, `searchable` (optional) |
| **Outputs** | Selected value(s) |
| **States** | Closed, open, focus, disabled, error |
| **Accessibility** | Native `<select>` preferred; custom listbox must implement ARIA listbox pattern |
| **Keyboard** | Native behaviour or ARIA listbox keys |
| **Responsive** | Full width of form column |
| **Examples** | Exam board filter |
| **Anti-patterns** | Custom select without keyboard support |

---

## Toggle

| Field | Spec |
|---|---|
| **Purpose** | Immediate on/off setting |
| **When to use** | Settings that take effect immediately |
| **When NOT to use** | Form submit binary (Checkbox); destructive without confirm |
| **Inputs** | `label`, `on`, `disabled` |
| **Outputs** | Boolean |
| **States** | Off, on, disabled, focus |
| **Accessibility** | `role="switch"` + `aria-checked`; label required |
| **Keyboard** | Space toggles |
| **Responsive** | Adequate hit target |
| **Examples** | Show archived subjects |
| **Anti-patterns** | Unlabelled switch; gold-coloured “premium” toggles |

---

## Link

| Field | Spec |
|---|---|
| **Purpose** | Navigate to another location or open related resource |
| **When to use** | Cross-page or in-content navigation without asserting Primary action |
| **When NOT to use** | The page’s sole next-best action (prefer Primary Button) |
| **Inputs** | `href`, `label`, `external` |
| **Outputs** | Navigation |
| **States** | Default, hover, focus, visited (neutral — no carnival visited colours) |
| **Accessibility** | `<a href>`; meaningful text (no “click here”) |
| **Keyboard** | Enter activates |
| **Responsive** | Wrap naturally |
| **Examples** | View all · Return Home (quiet) |
| **Anti-patterns** | Styling Link as Primary Button duplicate |

---

## Divider

| Field | Spec |
|---|---|
| **Purpose** | Separate unrelated content regions |
| **When to use** | Between L1 and L2 sections when spacing alone is insufficient |
| **When NOT to use** | Between every list row; decorative rules under titles |
| **Inputs** | `orientation` (horizontal \| vertical), `label` (optional) |
| **Outputs** | None |
| **States** | Static |
| **Accessibility** | `role="separator"` or plain `<hr>` |
| **Keyboard** | N/A |
| **Responsive** | Fluid width |
| **Examples** | Between Mission and Learning Queue |
| **Anti-patterns** | Hairline grids that create dashboard noise |

---

## Badge

| Field | Spec |
|---|---|
| **Purpose** | Compact status or count that affects decisions |
| **When to use** | Publication status, blocking count, Ready / Coming soon |
| **When NOT to use** | Decoration; gamification; streaks |
| **Inputs** | `label`, `tone` (neutral \| success \| warning \| danger \| info) |
| **Outputs** | None (display) |
| **States** | Static; optional dismiss never for status badges |
| **Accessibility** | Text conveys meaning (not colour alone) |
| **Keyboard** | N/A unless interactive (then use Chip carefully) |
| **Responsive** | Truncate with title attribute if needed |
| **Examples** | Blocking · Ready · Draft |
| **Anti-patterns** | Achievement badges; XP badges |

---

## Chip

| Field | Spec |
|---|---|
| **Purpose** | Removable or selectable filter token — **only when justified** |
| **When to use** | Active filter summary on Subjects / Choose Exam |
| **When NOT to use** | Tags for decoration; keyword clouds; emotion labels |
| **Inputs** | `label`, `selected`, `dismissible`, `onDismiss` |
| **Outputs** | Selection / dismiss events |
| **States** | Default, selected, focus, disabled |
| **Accessibility** | Button semantics if dismissible; group labelled |
| **Keyboard** | Enter/Space select; Delete/Backspace dismiss when focused |
| **Responsive** | Wrap; no horizontal scroll traps |
| **Examples** | Filter: “Ready” |
| **Anti-patterns** | Chip walls; skill-tag decoration |
| **Status** | **Justified optional** — default omit |

---

## Spinner

| Field | Spec |
|---|---|
| **Purpose** | Indicate indeterminate short wait |
| **When to use** | Inline on Button loading; brief fetches |
| **When NOT to use** | Full-page skeleton replacement for known layout (use Skeleton) |
| **Inputs** | `size`, `label` (sr-only required) |
| **Outputs** | None |
| **States** | Animating (respect reduced motion → static) |
| **Accessibility** | `role="status"` + polite live text |
| **Keyboard** | N/A |
| **Responsive** | Scales with token sizes |
| **Examples** | Publishing… |
| **Anti-patterns** | Multiple competing spinners; decorative loaders |

---

## Skeleton

| Field | Spec |
|---|---|
| **Purpose** | Preserve layout while content loads |
| **When to use** | Known structure loading (lists, mission block) |
| **When NOT to use** | Errors; empty collections |
| **Inputs** | `variant` (text \| title \| row \| button) |
| **Outputs** | None |
| **States** | Pulse (reduced motion → static opacity) |
| **Accessibility** | `aria-busy` on container; sr “Loading” |
| **Keyboard** | N/A |
| **Responsive** | Match final layout widths |
| **Examples** | Mission Card placeholder |
| **Anti-patterns** | Skeleton that doesn’t match final DOM |

---

## Tooltip

| Field | Spec |
|---|---|
| **Purpose** | Brief clarification on hover/focus |
| **When to use** | Icon-only controls with short explanation |
| **When NOT to use** | Essential instructions (put in UI); long essays |
| **Inputs** | `content`, `target` |
| **Outputs** | None |
| **States** | Hidden, visible |
| **Accessibility** | Does not replace accessible name; `aria-describedby` when supplemental |
| **Keyboard** | Show on focus; Escape hides |
| **Responsive** | Prefer visible label on mobile over tooltip-only |
| **Examples** | “Blocking findings” on icon |
| **Anti-patterns** | Tooltips for Primary CTA meaning |

---

## Popover

| Field | Spec |
|---|---|
| **Purpose** | Small non-modal anchored content |
| **When to use** | Overflow actions; compact filters |
| **When NOT to use** | Critical confirmations (Dialog); full forms |
| **Inputs** | `trigger`, `content`, `placement` |
| **Outputs** | Open/close; action events |
| **States** | Closed, open |
| **Accessibility** | Focus trap light or restore; Escape closes |
| **Keyboard** | Escape; Tab within |
| **Responsive** | Flip placement; full-width sheet on narrow if needed |
| **Examples** | Row overflow menu |
| **Anti-patterns** | Nested popovers |

---

## Disclosure

| Field | Spec |
|---|---|
| **Purpose** | Progressive disclosure of L2/L3 content |
| **When to use** | Hints, explainability, technical metadata, “why” stacks |
| **When NOT to use** | Primary content that answers the page question |
| **Inputs** | `summary`, `open` (default false), `children` |
| **Outputs** | Toggle open |
| **States** | Collapsed, expanded |
| **Accessibility** | Native `<details>`/`<summary>` or `aria-expanded` button |
| **Keyboard** | Enter/Space on summary |
| **Responsive** | Full width |
| **Examples** | Session hint; L3 technical IDs |
| **Anti-patterns** | Default-open Coach walls (DX-005C) |

---

## Dialog

| Field | Spec |
|---|---|
| **Purpose** | Modal focus for confirmations or short required tasks |
| **When to use** | Destructive confirm; blocking choice that must complete |
| **When NOT to use** | Routine success; tutorials; marketing |
| **Inputs** | `title`, `body`, `primaryAction`, `secondaryAction`, `open` |
| **Outputs** | Confirm / cancel |
| **States** | Closed, open |
| **Accessibility** | `role="dialog"` · `aria-modal` · labelled by title · focus trap · restore focus |
| **Keyboard** | Escape cancels; Tab cycles; Enter on Primary when safe |
| **Responsive** | Near full-width on mobile with margin `space.3` |
| **Examples** | Confirm publish · Confirm delete |
| **Anti-patterns** | Success celebration modals; stacked dialogs |

---

## Toast

| Field | Spec |
|---|---|
| **Purpose** | Transient feedback after an action |
| **When to use** | Non-blocking success/info after save/publish |
| **When NOT to use** | Blocking errors (inline / Feedback Block); permanent status |
| **Inputs** | `message`, `tone`, `duration` |
| **Outputs** | Dismiss |
| **States** | Entering, visible, leaving |
| **Accessibility** | `role="status"` polite; errors may be assertive if non-blocking |
| **Keyboard** | Focus not stolen; optional dismiss control |
| **Responsive** | Bottom or top safe area; not covering Primary |
| **Examples** | “Published” |
| **Anti-patterns** | Toast storms; emotional cheer |

---

## Empty State

| Field | Spec |
|---|---|
| **Purpose** | Explain absence and provide the next action |
| **When to use** | No mission, no subjects, empty queue, empty search |
| **When NOT to use** | Loading; errors |
| **Inputs** | `reason`, `nextAction` (Primary or Link), optional `support` |
| **Outputs** | Action event |
| **States** | Static |
| **Accessibility** | Region with heading; action focusable |
| **Keyboard** | Action reachable |
| **Responsive** | Single column |
| **Examples** | “No exam chosen yet” + Choose Exam |
| **Anti-patterns** | Illustration-heavy empty theatre; reason without action (DX-003) |

---

## Loading State

| Field | Spec |
|---|---|
| **Purpose** | Page or region busy with known intent |
| **When to use** | Initial page fetch; stage transition |
| **When NOT to use** | Empty; error |
| **Inputs** | `label`, optional Skeleton composition |
| **Outputs** | None |
| **States** | Busy |
| **Accessibility** | `aria-busy`; live region |
| **Keyboard** | N/A |
| **Responsive** | Match layout |
| **Examples** | Opening workspace… |
| **Anti-patterns** | Full-page spinner when Skeleton fits |

---

## Error State

| Field | Spec |
|---|---|
| **Purpose** | Present failure and recovery path |
| **When to use** | Region or page failure |
| **When NOT to use** | Field validation (inline on Input); soft warnings |
| **Inputs** | `title`, `message`, `recoveryAction` |
| **Outputs** | Retry / navigate |
| **States** | Static |
| **Accessibility** | `role="alert"` when immediate |
| **Keyboard** | Recovery focusable |
| **Responsive** | Single column |
| **Examples** | “Couldn’t load queue” + Retry |
| **Anti-patterns** | Stack traces; blame; sarcasm (DX-003) |

---

# Level 2 — Layout Components

## Page

| Field | Spec |
|---|---|
| **Purpose** | Document shell for one screen — title region + main |
| **When to use** | Every Founder/Student surface |
| **When NOT to use** | Embedded partials |
| **Inputs** | `title` (H1), `description?`, `children` |
| **Outputs** | None |
| **States** | Default + composed Loading/Error |
| **Accessibility** | One `h1`; `<main>` landmark |
| **Keyboard** | Skip link target |
| **Responsive** | Container tokens |
| **Examples** | Student Home page frame |
| **Anti-patterns** | Multiple H1; shell title + hero title duplicate |

---

## Section

| Field | Spec |
|---|---|
| **Purpose** | Group related content under one section heading |
| **When to use** | L0 / L1 / L2 page layers |
| **When NOT to use** | Wrapping single buttons for “card feel” |
| **Inputs** | `heading`, `level` (h2–h3), `children`, `description?` |
| **Outputs** | None |
| **States** | Static |
| **Accessibility** | Heading hierarchy intact |
| **Keyboard** | N/A |
| **Responsive** | Stack |
| **Examples** | Learning Queue section |
| **Anti-patterns** | Section per KPI |

---

## Container

| Field | Spec |
|---|---|
| **Purpose** | Constrain content width |
| **When to use** | Page content bands |
| **When NOT to use** | Nested max-width traps |
| **Inputs** | `width` (narrow \| content \| wide \| full) |
| **Outputs** | None |
| **Anti-patterns** | Arbitrary max-widths |

---

## Grid

| Field | Spec |
|---|---|
| **Purpose** | Responsive column layout |
| **When to use** | Multi-column forms or justified side-by-side when both columns earn space |
| **When NOT to use** | KPI tile mosaics |
| **Inputs** | `columns` behaviour from breakpoints |
| **Anti-patterns** | Dashboard card grids |

---

## Stack

| Field | Spec |
|---|---|
| **Purpose** | Vertical rhythm with token gaps |
| **When to use** | Default content flow |
| **When NOT to use** | Horizontal toolbars (Inline) |
| **Inputs** | `gap` (`space.2`–`space.6`) |
| **Anti-patterns** | Arbitrary gap pixels |

---

## Inline

| Field | Spec |
|---|---|
| **Purpose** | Horizontal cluster of related controls |
| **When to use** | Button + quiet link; filter row |
| **When NOT to use** | Primary + competing Primary |
| **Inputs** | `gap`, `align`, `wrap` |
| **Anti-patterns** | CTA button bars with equal weight |

---

## Sidebar

| Field | Spec |
|---|---|
| **Purpose** | Shell navigation region |
| **When to use** | Founder Console / Student shell only |
| **When NOT to use** | In-page duplicate nav (DX-004/005 boundaries) |
| **Inputs** | `items`, `activeId` |
| **Accessibility** | `nav` landmark; current page `aria-current` |
| **Anti-patterns** | Quick Actions grids; duplicate trees on page |

---

## Header

| Field | Spec |
|---|---|
| **Purpose** | Shell top chrome |
| **When to use** | Product shells |
| **When NOT to use** | Page-level marketing heroes |
| **Anti-patterns** | Welcome banners; promo strips |

---

## Footer

| Field | Spec |
|---|---|
| **Purpose** | Quiet legal / account links when required |
| **When to use** | Shell footer only |
| **When NOT to use** | Primary action placement |
| **Anti-patterns** | Footer CTA competing with page Primary |

---

## Toolbar

| Field | Spec |
|---|---|
| **Purpose** | Contextual actions for a list/table region |
| **When to use** | Search + filters above Subjects / Choose Exam |
| **When NOT to use** | Replacing Primary Action Strip |
| **Anti-patterns** | Dense icon toolbars without labels |

---

## Search Bar

| Field | Spec |
|---|---|
| **Purpose** | Filter catalogue / discovery lists |
| **When to use** | Subjects, Choose Exam (DX-004B / DX-005B) |
| **When NOT to use** | Global god-search inventing new IA |
| **Inputs** | `query`, `placeholder`, `onSubmit` |
| **Accessibility** | Labelled search landmark |
| **Anti-patterns** | Search as decoration |

---

## Table

| Field | Spec |
|---|---|
| **Purpose** | Scan comparable records |
| **When to use** | Subjects rows, publication lists, findings |
| **When NOT to use** | Mission presentation (use Mission Card) |
| **Accessibility** | `<table>` with headers; sortable buttons named |
| **Anti-patterns** | Card grids mimicking tables |

---

## List

| Field | Spec |
|---|---|
| **Purpose** | Sequential items (queues, progress) |
| **When to use** | Learning Queue, Publication Queue, Recent Progress |
| **When NOT to use** | When comparison across columns matters (Table) |
| **Anti-patterns** | Nested card lists |

---

## Card

| Field | Spec |
|---|---|
| **Purpose** | Group related content that must be perceived as **one unit** |
| **When to use** | Mission + why + Primary; bounded validation summary; settings group |
| **When NOT to use** | KPI tiles; wrapping every block; nested cards |
| **Status** | **Justified optional** per DX-001 |
| **Anti-patterns** | Soft multi-shadow lift; decorative card walls |

---

# Level 3 — Operational Components

Origin: DX-004 · DX-005. Compose L1/L2 only.

## Persistent Context Header

| Field | Spec |
|---|---|
| **Purpose** | Keep subject / stage / activity orientation visible while working |
| **When to use** | Workspace (DX-004C), Study Session (DX-005C) |
| **When NOT to use** | Home (context is the Mission / Current Work itself) |
| **Inputs** | Subject, stage or chapter/objective/activity, progress quiet |
| **Anti-patterns** | Second nav tree; KPI strip |

---

## Primary Action Strip

| Field | Spec |
|---|---|
| **Purpose** | Host the single Primary and quiet escapes |
| **When to use** | Adjacent to L0 Current Work / Mission / Stage task |
| **When NOT to use** | Multiple Primaries; Quick Action grids |
| **Inputs** | One Primary Button; optional Text/Ghost secondary |
| **Anti-patterns** | CTA clusters |

---

## Stage Indicator

| Field | Spec |
|---|---|
| **Purpose** | Show Founder workspace stage position (Upload → … → Publish) |
| **When to use** | Curriculum Workspace only |
| **When NOT to use** | Student Session; decorative steppers on Home |
| **Inputs** | Current stage, completed stages (DX-004C model) |
| **Anti-patterns** | Clickable future stages that skip gates unlawfully |

---

## Mission Card

| Field | Spec |
|---|---|
| **Purpose** | Present the student’s current mission and one Primary |
| **When to use** | Student Home L0 (DX-005A) |
| **When NOT to use** | Founder Home (use Current Work pattern via Card/Section); queues |
| **Inputs** | Subject, objective, why-now (collapsed if long), Primary label/action |
| **Anti-patterns** | Progress rings; cheer; multi-why walls default open |

---

## Feedback Block

| Field | Spec |
|---|---|
| **Purpose** | Immediate educational outcome after practice attempt |
| **When to use** | Study Session after answer/exercise (DX-005C) |
| **When NOT to use** | Emotional encouragement; Home celebrations |
| **Inputs** | Correctness/outcome, explanation, next step hint |
| **Tone** | Educational, calm — DX-003 / DX-005C |
| **Anti-patterns** | Confetti; “Great job!!!” |

---

## Search Results

| Field | Spec |
|---|---|
| **Purpose** | Render catalogue/discovery hits |
| **When to use** | Subjects, Choose Exam |
| **When NOT to use** | Mission replacement |
| **Composes** | List or Table + Empty State |
| **Anti-patterns** | Result cards with vanity metrics |

---

## Publication Status

| Field | Spec |
|---|---|
| **Purpose** | Communicate curriculum release state that changes operator decisions |
| **When to use** | Subjects rows, Workspace context, Home queue |
| **When NOT to use** | Student Ready decoration without meaning |
| **Composes** | Badge + optional short Supporting text |
| **Anti-patterns** | Health-score dashboards |

---

## Learning Queue

| Field | Spec |
|---|---|
| **Purpose** | Attention-only upcoming learning items (Student Home L1) |
| **When to use** | Student Home |
| **When NOT to use** | Session chrome |
| **Composes** | List + quiet row actions (never second Primary) |
| **Anti-patterns** | Queue louder than Mission |

---

## Recent Progress

| Field | Spec |
|---|---|
| **Purpose** | Quiet orientation — last ≤5 completed items (Student Home L2) |
| **When to use** | Student Home |
| **When NOT to use** | Gamified history; streaks |
| **Anti-patterns** | Charts; XP |

---

## Blocking Findings

| Field | Spec |
|---|---|
| **Purpose** | Surface hard blockers that prevent lawful Primary success |
| **When to use** | Workspace Validate/Review; Session when validation blocks |
| **When NOT to use** | Soft tips as “blockers” |
| **Composes** | List + Badge danger + Disclosure for details |
| **Anti-patterns** | Burying blockers below vanity content |

---

## Session Context

| Field | Spec |
|---|---|
| **Purpose** | Session-specific persistent orientation (alias specialisation of Persistent Context Header) |
| **When to use** | Study Session |
| **Inputs** | Subject, chapter, objective, activity, session progress |
| **Anti-patterns** | Progress dashboard; mastery rings |

---

## Current Work (Founder)

| Field | Spec |
|---|---|
| **Purpose** | Founder Home L0 — subject, stage, one Primary (Resume) |
| **When to use** | Founder Home (DX-004A) |
| **When NOT to use** | Student Home |
| **Composes** | Section/Card + Primary Action Strip |
| **Anti-patterns** | Platform summary KPIs |

---

## Publication Queue (Founder)

| Field | Spec |
|---|---|
| **Purpose** | Attention-only rows needing operator action (Founder Home L1) |
| **When to use** | Founder Home |
| **Anti-patterns** | Full catalogue duplicate of Subjects |

---

# Rejected components

| Component | Reason |
|---|---|
| **StatisticTile** | Decorative KPI pattern — forbidden by DX-001 |
| **ProgressRing** (product OS chrome) | Vanity mastery theatre on Home/Console |
| **ProgressCard** | KPI/progress decoration without decision value |
| **RecommendationCard** as Mission peer | Competes with single Primary / Mission ownership |
| **Tag** (duplicate of Badge/Chip) | Consolidate into Badge or justified Chip |
| **Timeline** (Home/Console) | Narrative theatre unless a justified audit view |
| **Stepper** outside Workspace stages | Decorative; Stage Indicator owns Founder stages |
| **Accordion** as default Coach wall | Use Disclosure; keep collapsed (DX-005C) |
| **Achievement / Streak / XP widgets** | Gamification banned on OS surfaces |
| **Quick Actions grid** | Duplicate navigation / multi-Primary |
| **Welcome / Hero / Promo panels** | Marketing chrome on product OS |
| **Page-specific foundation widgets** | Belong on pages until promoted with purpose |

Existing Python exports that match Rejected rows must be **deprecated** in Phase 2–4 implementation and **removed from foundation imports** used by DX-006B migrations.

---

## Inventory summary

| Level | Canonical | Justified optional | Rejected (named) |
|---|---:|---:|---:|
| L0 Tokens | All categories in token spec | — | Hard-coded values |
| L1 | 19 | Chip | — |
| L2 | 13 | Card | KPI grids |
| L3 | 12 | — | See Rejected table |
| Legacy V3 reject list | — | — | StatisticTile, ProgressRing, ProgressCard, RecommendationCard peer, Tag dup, etc. |

---

*Release Candidate: RC-2026.07.29-01*
