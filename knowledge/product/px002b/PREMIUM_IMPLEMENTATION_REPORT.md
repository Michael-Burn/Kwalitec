# PX-002B — Premium Implementation Report

**Programme:** PX-002B (Premium Experience Implementation)
**Precedes:** PX-001 (Audit), PX-002A (Trust & Friction Resolution)
**Scope:** Refinement of the existing Kwalitec UI — not a redesign.

## 1. Starting position

PX-001 audited every student-facing screen and produced a prioritised backlog.
PX-002A closed the Tier 1/2 trust and friction items (dual "Dashboard" labels,
conflicting durations, un-framed Reflection screen, terminology drift). Its
completion report explicitly named four items as carried debt into this
programme:

1. Icon markup duplicated across `sidebar.html` / `topnav.html` (13+ inline
   SVGs, no single source of truth).
2. The appearance (Light/Dark/System) switcher implemented twice — icon+label
   buttons in the top nav, text-only buttons in Settings — one visual
   language violated twice.
3. Numeric false precision (`|round(1)` on a decimal-hour computation) in the
   Study Plan roadmap.
4. Several screen-level polish items flagged in `PREMIUM_UI_AUDIT.md` under
   "cards", "buttons", and "empty states" that PX-002A intentionally left for
   this programme.

This report documents what PX-002B did about each of those, plus the
additional refinement passes required by the brief (empty states, buttons,
responsiveness, accessibility, microcopy, branding).

## 2. What changed, and why

### 2.1 Design standardisation — one icon system, one appearance control

**Before:** `sidebar.html` and `topnav.html` each hard-coded the same 15+
SVG icons inline. Any visual change (stroke width, sizing) required editing
every occurrence by hand, and small copy/paste drift had already crept in
(e.g. non-identical `stroke-width` on a couple of nav icons).

**After:** `app/templates/partials/icons.html` defines a single `icon(name,
size, stroke_width, class)` macro covering every icon used across
navigation, settings, appearance, and data actions. `sidebar.html`,
`topnav.html`, and `settings/index.html` now all call the same macro.

Per the brief's "whenever two implementations exist, choose the better one,
standardise the rest" rule: the icon markup, stroke widths (1.75 for nav,
2.0 default elsewhere), and sizing already in use were kept as-is — this is
a **de-duplication**, not a re-skin. No icon looks different than before;
there is simply one definition of each icon instead of several.

**Before (appearance switcher):** the top nav rendered an icon+label button
group with `aria-labelledby` pointing at a shared "Appearance" caption; the
Settings pages rendered a *different*, text-only button group for the exact
same three-state control, and only the Preferences instance additionally
offered a `<select>` fallback.

**After:** `app/templates/partials/appearance_switcher.html` is the one
implementation, parameterised for the three contexts that need it (`topnav`,
`settings/preferences` with the select fallback, `settings/internal-alpha`
without it). The richer treatment (icon + label) was chosen as "the better
one" and is now what Settings renders too — Settings previously showed only
bare text buttons, which was the weaker of the two implementations.

While consolidating the switcher, each button was given an explicit
`aria-label` (see §5, Accessibility) — a small but real accessibility gap
in both prior implementations, fixed once, centrally, instead of twice.

All `data-appearance-option`, `data-appearance-select`, and `aria-pressed`
attributes that `theme.js` and the existing test suite depend on were
preserved exactly; this is a template-authoring change only, with no
behavioural change to how appearance preference is read, stored, or applied.

### 2.2 Empty states — teach, encourage, guide the next step

`PREMIUM_UI_AUDIT.md` and the brief both call out the "No data." anti-pattern.
Three screens still had the plain, unhelpful form of this: Journey, Revision,
and History rendered a bare heading and one flat sentence
("Your learning path will appear here.") with **no call to action** when the
underlying snapshot was unavailable (new student with no study plan yet, or
a transient service degradation). Home already modelled the correct pattern
(`.student-empty` / `.student-empty-title` / `.student-empty-description`)
for its own empty case — that pattern is now reused, consistently, on the
three secondary surfaces:

- **Journey:** *"Your journey will take shape after your first session"* +
  a "Go to Home" primary action.
- **Revision:** *"Revision opens up after your first session"* + a "Go to
  Home" primary action.
- **History:** *"Your history starts with your first session"* + a "Go to
  Home" primary action. The narrower "No completed sessions yet." sub-empty
  (a populated History page with zero session rows) was upgraded from a
  single muted sentence to the same teach/encourage pattern.

This closes the gap between "the page technically explains itself" (already
true after PX-002A's terminology work) and "the page tells the student what
to do next," which is the specific bar the brief sets for empty states.

### 2.3 Numeric precision — Study Plan roadmap hour estimates

**Before:** `{{ ((topic.recommended_minutes or 0) / 60)|round(1) }}h` — a
computed decimal-hour value (e.g. "0.8h", "1.3h") that implies a level of
precision the underlying estimate does not actually carry, and that reads as
a spreadsheet artefact rather than a considered product decision.

**After:** the roadmap now reuses `format_minutes()` — the same duration
phrase already used everywhere else a study duration is shown (Home, Mission,
Session Overview, per PX-002A T1-2) — via a new `format_minutes` Jinja
filter registered once in `_register_template_context`. The roadmap now
reads "1 hour 30 min" instead of "1.5h", consistent with how every other
screen phrases the same kind of number. Metric label was renamed from the
abbreviated "Est. Hours" to "Estimated time" to match the phrase it now
displays. **Formatting only** — the underlying `recommended_minutes` value
and the planning logic that produces it were not touched.

### 2.4 Button hierarchy — Study Session Feedback screen

**Before:** `mission/session_recorded.html` stacked three full-width buttons
of near-identical visual weight ("Continue", "Return Home", and "Back to
Today's Study Session" — the last one additionally had anomalous `mx-4 mb-4`
spacing that didn't match its siblings). Three competing full-width CTAs
violates the brief's "one dominant action, secondary actions visually
secondary, no competing CTAs" rule.

**After:** "Continue" remains the one primary action (`btn-mark-complete`).
"Return Home" remains a secondary action. "Back to Today's Study Session" —
the least likely path off this screen — was demoted from a full-width
outline button to a plain centred text link, removing both the visual
competition and the spacing anomaly in one change.

`session_practice_outcome.html` was audited against the same rule and found
already compliant (one primary action, two legitimately equal-weight
secondary paths) — no change was needed there.

### 2.5 Responsiveness — mission hero metrics on narrow screens

**Before:** `.mission-hero-metrics` was a plain `display:flex` row with two
`flex:1` metric cards (icon + label + value) side by side, with no
breakpoint override. On a narrow phone viewport this squeezes two
44px-icon-plus-text cards into half the width each — exactly the "shrunk
desktop" the brief warns against, rather than a recomposed mobile layout.

**After:** added one rule inside the existing `max-width:575.98px` media
query to stack `.mission-hero-metrics` vertically below that breakpoint, so
each metric card gets the full card width instead of being squeezed.

This CSS addition was kept intentionally minimal (see
`RESPONSIVE_REPORT.md` for the byte-budget story) — the fix is scoped to
the one layout rule that mattered, not a broader rewrite of the hero card's
spacing scale.

### 2.6 Accessibility — Help search empty state

**Before:** the "No topics match that search" message in Help toggled its
`hidden` attribute via `help-search.js` but had no `role`/`aria-live`, so a
screen reader user typing a query that matched nothing received no
notification that the result set had changed.

**After:** `role="status" aria-live="polite"` added to that element. No JS
change was required — `help-search.js` already just flips `hidden`.

### 2.7 What was reviewed and intentionally left unchanged

- **"Practice Outcome Capture" eyebrow** (`session_practice_outcome.html`) —
  this reads as internal jargon, but it is the formal name of a shipped
  capability (LXP-003) asserted directly in three test suites
  (`test_ptp002_single_source_of_truth.py`,
  `test_lxp002_study_session_experience.py`,
  `test_lxp003_practice_outcome_capture.py`). Changing student-facing copy
  that is simultaneously a test-pinned capability identifier is out of scope
  for a copy pass; flagged here rather than silently ignored.
- **Appearance switcher's group-level duplicate accessible name** — the
  three buttons in the topnav variant still sit inside one `role="group"
  aria-label="Appearance"` region; giving each button its own `aria-label`
  (done in this pass) already resolves the practical screen-reader
  experience. A deeper redesign of the group semantics was judged
  disproportionate to the remaining benefit.
- **Full re-audit of every screen against the "Premium Test"** — see
  `FINAL_PRE_RENDER_REVIEW.md` for the screen-by-screen walk that was
  performed; it confirms most screens already meet the bar after PX-002A,
  and this programme targeted the concrete gaps that remained rather than
  re-touching screens that already passed.

## 3. Constraints honoured

- No Runtime A, educational logic, recommendation logic, or governance
  changes. All edits are templates, one CSS breakpoint rule, one Jinja
  filter registration (formatting only), and two new partial files.
- No new dependencies, no new animation, no gamification, no decoration
  without a stated purpose.
- No feature creep — every change above traces to a named gap in
  `PREMIUM_UI_AUDIT.md`, `HIGH_PRIORITY_BACKLOG.md`, or the PX-002B brief
  itself.

## 4. Verification

Full test suite run before and after (see `COMPLETION_REPORT.md` for exact
counts). No new failures were introduced; the CSS byte-budget test
(`test_first_party_css_js_under_budget`) briefly regressed during
development and was fixed by trimming the responsive rule to its minimal
form before this work was considered complete.

## 5. Related documents

- `SCREEN_STANDARDIZATION_REPORT.md` — before/after per screen.
- `MICROCOPY_REVIEW.md` — copy changes in full.
- `VISUAL_CONSISTENCY_REPORT.md` — icon/appearance-switcher consolidation detail.
- `ACCESSIBILITY_REPORT.md` — accessibility changes and spot-check findings.
- `RESPONSIVE_REPORT.md` — responsive review and the mission-hero fix.
- `BRANDING_IMPLEMENTATION_REPORT.md` — branding asset verification.
- `FINAL_PRE_RENDER_REVIEW.md` — screen-by-screen Premium Test walk.
- `COMPLETION_REPORT.md` — governance-format completion record.
