# PX-002B — Visual Consistency Report

Scope: component and design-token consistency work performed in this
programme. Design tokens themselves (`tokens.css`, `brand.css`) were not
modified — this programme consolidated *usage* of the existing system.

## 1. Icon system — one source of truth

**Problem:** icon SVGs were hand-copied into `sidebar.html`, `topnav.html`,
and `settings/index.html` — the same "home", "settings-gear", "help", etc.
markup repeated 3+ times each, with no guarantee of staying in sync.

**Resolution:** `app/templates/partials/icons.html` — a single Jinja macro,
`icon(name, size=20, stroke_width=2, class='')`, covering every icon in use:
`home`, `journey`, `revision`, `history`, `study-plan`, `session`,
`settings-gear`, `help`, `sign-out`, `feedback`, `profile`, `preferences`,
`data`, `internal-alpha`, `download`, `upload`, `menu`, `sun`, `moon`,
`monitor`.

All three templates now call this macro exclusively for these icons. Visual
output is unchanged (same paths, same default stroke widths per call site —
1.75 for primary nav links, 2.0 elsewhere, matching what was already in use)
— this is deduplication of markup, not a visual change.

## 2. Appearance switcher — one implementation, three contexts

**Problem:** two different visual treatments existed for the identical
Light/Dark/System control — icon+label in the top nav, text-only in
Settings — a direct violation of "everything should belong to one design
language."

**Resolution:** `app/templates/partials/appearance_switcher.html` exports
`appearance_switcher(group_aria_label, show_switcher_label, show_select)`.
Per the "choose the better one, standardise the rest" rule, the icon+label
treatment (the richer, clearer implementation) was kept and is now what
every context renders:

- Top nav: `appearance_switcher(group_aria_label='Appearance',
  show_switcher_label=true)` — unchanged visual output, now macro-driven.
- Settings → Preferences: `appearance_switcher(show_select=true)` — now
  renders icon+label buttons (previously text-only) plus the existing
  `<select>` fallback.
- Settings → Internal Alpha: `appearance_switcher()` — now renders
  icon+label buttons (previously text-only).

All `data-appearance-option`, `data-appearance-select`, and `aria-pressed`
attributes `theme.js` depends on are unchanged; only the markup source
changed from three copies to one.

## 3. Numeric formatting — one duration phrase, everywhere

**Problem:** the Study Plan roadmap independently computed and rounded a
decimal-hour value (`(minutes/60)|round(1)` → "0.8h"), while every other
study-duration display on the product (Home, Mission, Session Overview) used
the shared `format_minutes()` helper (→ "45 minutes", "1 hour 30 min") from
`app/presentation/formatting.py` (introduced in PX-002A T1-2).

**Resolution:** `format_minutes` is now registered as a Jinja filter
(`app.jinja_env.filters["format_minutes"]`) so templates can call
`{{ minutes | format_minutes }}` directly. The Study Plan roadmap is the
first template to use this filter form; the underlying Python helper and its
existing call sites in `view_models.py` are unchanged.

## 4. Empty-state pattern — one visual treatment

**Problem:** Home used the `.student-empty` / `.student-empty-title` /
`.student-empty-description` pattern for its true-empty state; Journey,
Revision, and History used a plain `.student-card` with a bare `<h2>` and
one paragraph for the equivalent state — two different visual treatments for
the same underlying situation (no data yet).

**Resolution:** Journey, Revision, and History's true-empty states — and
History's "no sessions" sub-empty — now use the same `.student-empty`
pattern as Home, with a `.student-primary-action` CTA where the brief calls
for guiding the next step. No new CSS was introduced; the existing
`.student-empty*` classes in `student.css` were already defined but only
used on one screen.

## 5. Button hierarchy — Study Session Feedback

**Problem:** three full-width, visually equal buttons on
`session_recorded.html`, one with an inconsistent margin utility (`mx-4
mb-4`) not used anywhere else on the page.

**Resolution:** kept the existing one-primary / one-secondary full-width
pair; demoted the third, least-used action to a plain centred text link
(`text-center small mt-1`), removing the spacing inconsistency and the
three-way visual competition in one change.

## 6. Responsive layout — mission hero metrics

**Problem:** `.mission-hero-metrics` had no breakpoint override; on narrow
viewports two `flex:1` metric cards were squeezed side by side instead of
being recomposed for the smaller width.

**Resolution:** one rule added inside the existing `max-width:575.98px`
media query (`.mission-hero-metrics{flex-direction:column;}`), stacking the
cards vertically below that width. See `RESPONSIVE_REPORT.md` for the full
before/after and the CSS byte-budget constraint that shaped how minimal this
fix needed to be.

## 7. What was not touched

- Corner radius, shadow, and motion tokens in `tokens.css` — already
  consistent per PX-001's consistency audit; no drift found in this pass.
- Table, list, alert, chip, and divider components — reviewed, no
  duplicate implementations found requiring consolidation.
- Card component structure (`.student-card`, `.mission-card`,
  `.roadmap-card`) — each already has one implementation per surface family;
  no cross-surface duplication found beyond the icon/appearance/empty-state
  items resolved above.
