# PX-002B — Responsive Report

Scope: responsive review across desktop, tablet, and mobile breakpoints, and
the one recomposition fix made in this programme.

## Breakpoints in use (unchanged)

The existing system uses four breakpoints in `app.css`, matching Bootstrap's
grid: `≤1199.98px` (sidebar width reduction), `≤991.98px` (sidebar becomes an
overlay drawer), `≤767.98px` (top nav height, section titles, chart height),
`≤575.98px` (main padding, stat cards, ready-score circle, command hero
value). This programme did not introduce a new breakpoint — the fix below
was added to the existing `≤575.98px` rule.

## Finding: mission hero metrics squeeze on narrow screens

**Where:** `mission/index.html` (Today's Session) and `mission/session.html`
(active session) both render a `.mission-hero-metrics` row. On the mission
index specifically, this row holds *two* metric cards side by side
("Estimated Time" and "Syllabus coverage"), each a `flex:1` box containing a
44×44px icon, a label, and a value.

**Problem:** `.mission-hero-metrics{display:flex;gap:var(--space-xl);...}`
had no responsive override. Below ~400px of available width, two such cards
side by side is a textbook "shrunk desktop" layout — the icon, label, and
value text get compressed rather than recomposed, which is exactly the
anti-pattern the brief calls out ("No screen should feel like a shrunk
desktop. Recompose layouts where appropriate.").

**Fix:** added `.mission-hero-metrics{flex-direction:column;}` inside the
existing `@media (max-width:575.98px)` block. Below 576px, the metric cards
now stack full-width instead of splitting the row, so each retains its full
icon/label/value layout instead of being compressed.

### Why the fix is this small

`app/static/css/app.css` is served pre-minified (one selector per line, no
extra whitespace), and the repository has a hard CSS budget test
(`tests/test_v1sp003_performance.py::test_first_party_css_js_under_budget`,
`assert css_bytes < 70_000`). The baseline was already at ~69,892 bytes
before this programme touched anything — 99.8% of budget already consumed
by pre-existing CSS, unrelated to this work.

A first version of this fix also reduced horizontal padding on
`.mission-hero-topic`, `.mission-hero-tasks`, `.mission-hero-why`, and
`.btn-mark-complete` at the same breakpoint (a further "recompose, don't
shrink" improvement). That version pushed the budget to 70,308 bytes and
failed the test. Rather than raise the budget (which the brief's "no
unnecessary [...] decoration" and the project's own performance contract
argue against doing casually), the fix was trimmed to the one rule that
actually mattered — the flex-direction change — which fits comfortably
under budget. The padding refinement is recorded here as a follow-up
opportunity rather than shipped as a byte-budget risk.

## Screens reviewed, no change needed

- **Journey / Revision / History:** single-column `student-*` layouts
  already recompose correctly at all three breakpoints — verified by
  inspection of `student.css`'s existing mobile rules and the templates'
  lack of any fixed-width elements.
- **Settings:** the two-column sidebar/content layout already collapses to
  a single stacked column at `≤991.98px` (existing rule, unchanged).
- **Study Plan roadmap:** `.roadmap-grid` uses
  `grid-template-columns:repeat(auto-fill, minmax(300px, 1fr))`, which
  already recomposes to a single column on narrow viewports without any
  breakpoint override needed.
- **Top nav / appearance switcher:** already had a `≤575.98px` rule hiding
  the text labels and reducing button padding for an icon-only mobile
  layout — reviewed as part of the appearance-switcher consolidation
  (`VISUAL_CONSISTENCY_REPORT.md`) and left as-is; it already recomposes
  correctly and is not a "shrunk desktop" pattern.

## Verification

Manual review only (template/CSS inspection against each breakpoint's
computed layout) — no visual regression tooling was run as part of this
programme. `tests/presentation/student/test_responsive.py` (pre-existing)
continues to pass.
