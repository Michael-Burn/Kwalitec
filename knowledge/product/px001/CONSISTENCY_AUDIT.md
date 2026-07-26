# PX-001 — Consistency Audit

**Status:** Analysis only. No code changed.
**Purpose:** Catalogue where Kwalitec's own design system (`BRAND_GUIDELINES.md`, `UI_UX_IMPLEMENTATION_STANDARD.md`/UX-001, `tokens.css`) is and is not applied consistently across the two coexisting presentation stacks.

---

## 1. Terminology matrix — the same concept, different names

The clearest, most measurable inconsistency in the product. Compiled directly from template/route inspection.

| Concept | Legacy label(s) | Canonical label(s) | Where seen |
|---|---|---|---|
| The "what to do today" home screen | "Student Dashboard" (H1), "Dashboard" (nav) | "Dashboard" (H1 **and** nav pill, per screenshot `04`), though internal docs call it "Home" | `dashboard/index.html`; `student/home.html`; `SCREEN_INVENTORY.md` calls the canonical route "Home" while the rendered UI says "Dashboard" |
| The daily study activity | "Session" (nav item), "Study Session" (page titles), "Today's Study Session" (H1) | "Today's Mission" (hero eyebrow/title) | `sidebar.html` legacy tree line 74 ("Session"); `mission/index.html`; `student/home.html` line 30 |
| The record-what-happened step | "Practice Outcome Capture" (H1), reached via "Finish Study Session" | "Reflection" (canonical Session Experience), also folded into Home's `reflection_active` state ("Guided Reflection") | `mission/session_practice_outcome.html`; `session/reflection.html`; `student/home.html` lines 25–57 |
| Profile / account | "Settings → Profile" section | Screenshot evidence (`08-settings-profile-student.png`) shows `/student/profile` rendering H1 "Settings" with the "Settings" nav pill active, not a distinct "Profile" pill, despite `SCREEN_INVENTORY.md` documenting it as a "Profile" destination | `settings/index.html` section=profile; `student/profile` route — **recommend verifying current routing/naming intent before Stage 1**, since two independent documents (screen inventory vs. rendered UI) disagree |
| "Analytics" | Present in both trees, same label | Present in both trees, same label | **Superficial consistency only.** Both trees render the identical label and identical inline icon, but they route to two different endpoints and templates: legacy `analytics.index` → `/analytics/` → `analytics/index.html` (6-KPI dashboard, Chart.js), vs. canonical `student.history` → `/student/history` → `student/history.html` (session/history list). A student who learns "Analytics" in one stack and later encounters it in the other is looking at a structurally different screen behind the same word — this reads as consistent in a side-by-side nav audit but is not consistent in the underlying product. |

**Takeaway:** four of five core concepts have at least two different names depending on which stack renders them, and one (home) reuses the *same* name for two different screens. This is the mechanism behind PR-001's Navigation score (mean 4.60) independent of the dual-stack architecture question addressed in `PR001_ALIGNMENT_REPORT.md` §3 — even a student who only ever sees one stack in production still encounters "Mission" vs. "Session" vs. "Study Session" vs. "Today's Mission" for what is, to them, one thing.

---

## 2. Design-token compliance

`app/static/css/tokens.css` is a well-authored, disciplined implementation of `UI_UX_IMPLEMENTATION_STANDARD.md` (UX-001):

| UX-001 rule | Token implementation | Compliant? |
|---|---|---|
| §5 8-point spacing grid | `--space-xs` (4) through `--space-4xl` (64), lines 79–86 | Yes |
| §6 Typography — Inter only, 40/28/20/16/14 hierarchy | `--font-family: "Inter"...`, `--font-4xl` (40) … `--font-xs`/`--font-sm` (14), lines 88–98 | Yes |
| §3 Brand colours — Blue #3B4FB8, Dark #0D1B2A, Navy #0A1628, Midnight #020D24, Gold #E8B02B | `--primary`, `--brand`, `--brand-gold` all map to the documented hex values, lines 17–51 | Yes |
| §3 "Gold is not a UI colour... never for primary buttons, navigation, links, focus, charts" | `--focus-ring` uses blue-based rgba, not gold (line 52); primary buttons map to `--primary` (blue) | Yes, as far as tokens go — not independently re-verified against every template's inline usage in this pass |
| §10 Cards — 16px radius, soft shadow, no gradients | `--radius-lg: 1rem` (16px), `--shadow`/`--shadow-lg` soft box-shadows, no gradient tokens defined at all | Yes |
| §11 Inputs — 12px radius, blue focus ring | `--radius-md: 0.75rem` (12px), `--focus-ring` blue-based | Yes |
| §14 Motion — hover 150ms, page 250ms, modal 200ms, sidebar 220ms, tooltip 120ms | `--transition-fast` (150ms), `--transition-page` (250ms), `--transition-sidebar` (220ms), `--transition-tooltip` (120ms) all present and correctly valued, lines 116–123 | Yes |
| §15 Loading — skeletons, never blank | `.skeleton`, `.skeleton--text/title/card/button/bar/avatar` fully implemented, lines 184–249, with `prefers-reduced-motion` handling | Yes |
| §22 Dashboards — max 4 KPI cards per row | Not a token (a layout rule) — **violated** in `analytics/index.html` (6 tiles in one row, screenshot `10-analytics-legacy.png`) | **No** |
| §7 Iconography — Lucide Icons exclusively, single source | No shared icon partial or icon-sprite file found; every SVG is hand-inlined per template (`sidebar.html`, `topnav.html`, `login.html`, etc., each define their own `<svg>` markup) | **Not verifiable as a single controlled source** — visually consistent today (24px, 1.75 stroke, rounded caps) but structurally unenforced |
| Named colour palette (`COLOUR_SPECIFICATION.md`) | Error-page "Reference ID" renders in a pink/magenta tone not present in `tokens.css` or the brand colour spec (screenshots `error-404.png`, `error-403-or-denied.png`) | **No** — likely a default Bootstrap utility class (`text-danger`-adjacent) applied without checking it against the Kwalitec palette |

**Conclusion:** the *system* (tokens.css) is sound and closely matches the internal standard. Violations found are all **template-level deviations from a good system**, not gaps in the system itself — which is a favourable finding for remediation effort (fix the instances, not the foundation).

---

## 3. Component consistency — dialogs and confirmations

| Pattern | Implementation | Consistent? |
|---|---|---|
| Informational modal | `partials/welcome_modal.html` — fully styled, on-brand, `role="dialog" aria-modal="true"`, primary + dismiss actions | Reference-quality |
| Destructive confirmation (Study Plan archive/delete) | Native browser `confirm()` via inline `onclick`, per `KNOWN_LIMITATIONS.md` #19 | **Inconsistent** — bypasses the entire design system for the highest-stakes actions in Study Plan |
| Destructive confirmation (Settings → Restore from Backup) | `settings/index.html` line 285: `onclick="return confirm('This will replace all existing data with the backup. Continue?')"` | **Inconsistent** — same issue, for an action explicitly warned as replacing "all existing data" |

Kwalitec already has a working styled-dialog component (`welcome_modal.html`'s pattern). The inconsistency is a reuse gap, not a missing capability.

---

## 4. Component consistency — CSS/JS architecture

- Stack: Bootstrap 5.3.3 (via CDN, `layouts/base.html`/`auth_base.html` line 14) + a custom token/utility layer (`brand.css`, `tokens.css`, `app.css`) + area-specific stylesheets (`student/student.css`, `session/session.css`, `wizard/wizard.css`).
- This is a coherent, intentional layering (Bootstrap for structural utilities, custom CSS for brand/tokens), not a random mix — no evidence of a second competing UI framework was found.
- Icon SVGs are duplicated verbatim across files (e.g., the same "circle with 3-dot gear" settings icon markup appears independently in `sidebar.html` line 46 and `settings/index.html` line 18) rather than being defined once and referenced. This is a maintainability/consistency risk (a future icon tweak requires finding every duplicate instance) rather than a currently-visible defect.
- Dark theme (`[data-theme="dark"]` block, `tokens.css` lines 130–175) is a complete, deliberately re-authored palette rather than a filter/invert — this is the correct approach and renders cleanly in the one available dark screenshot (`51-theme-dark.png`).

---

## 5. Navigation structure — full comparison

| | Legacy tree (`sidebar.html` lines 61–106) | Canonical tree (`sidebar.html` lines 18–60, `topnav.html`) |
|---|---|---|
| Chrome | Dark left rail, always visible ≥ lg breakpoint | Light top bar, full width |
| Home label | "Dashboard" | "Dashboard" (canonical Home) |
| Items | Dashboard · Study Plan · Session · Analytics · Settings · Share Feedback · Help · Sign out | Dashboard · Journey · Revision · Analytics · Settings · Study Plan · Help · Sign out |
| Shared infrastructure | `study_plan`, `calibration`, `alpha`, `settings`, `auth`, `research` are not gated by the flag and render inside whichever chrome is active (`NAVIGATION_AUDIT.md` §1) | Same |
| Governing flag | `KWALITEC_V2_SOLE_RUNTIME=0` (default/unset) | `KWALITEC_V2_SOLE_RUNTIME=1` (Render production per `render.yaml`) |

Both trees are well-built individually (clear active-state styling via `request.endpoint` checks, consistent icon sizing, accessible `aria-label="Primary"`). The inconsistency is entirely at the level of *which one a given student sees and when*, and the shared "Dashboard" label across both (§1), not in the quality of either tree's construction.

---

## 6. Summary of consistency violations by severity

| Severity | Finding |
|---|---|
| Critical | Two navigation trees share the label "Dashboard" for structurally different home screens |
| High | Native `confirm()` dialogs used for the two highest-stakes destructive actions, alongside an existing, unused, better-styled dialog pattern |
| High | Terminology fragmentation across 4 of 5 core concepts (Mission/Session/Study Session/Today's Mission; Profile vs. Settings) |
| Medium | Analytics KPI row exceeds the product's own 4-per-row dashboard rule |
| Medium | Off-palette pink "Reference ID" colour on error pages |
| Medium | "Analytics" nav label is identical in both stacks but routes to two structurally different screens/templates (see §1) — consistent labelling masking inconsistent implementation |
| Low | Icon markup duplicated per-template rather than centrally sourced (maintainability risk, not a current visible defect) |
| Low | Preferences screen offers the same 3-way choice via two different controls (button group + `<select>`) on one screen |
