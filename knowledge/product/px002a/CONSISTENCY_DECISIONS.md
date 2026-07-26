# PX-002A — Consistency Decisions

**Programme:** PX-002A — Trust & Friction Resolution
**Input:** `knowledge/product/px001/CONSISTENCY_AUDIT.md`
**Rule applied (acceptance criterion #10):** when two implementations solve the same problem differently, do not compromise — identify the superior implementation and standardise every equivalent screen to match it.

Each decision below names the two (or more) competing implementations found, which one was declared the standard, and why.

---

## Decision 1 — Destructive-action confirmation: styled modal vs. native `confirm()`

**Competing implementations found:**
1. `partials/welcome_modal.html` — a fully styled Bootstrap modal, on-brand, `role="dialog" aria-modal="true"`, already in production use.
2. Native browser `confirm()` — used for Study Plan archive/delete and Settings → Restore from Backup, the two most destructive actions in the product.

**Decision: the styled modal pattern is the standard.** It is more accessible (consistent focus handling via Bootstrap's modal component, rather than a browser-native dialog whose focus/dismiss behaviour varies by browser), it is on-brand, and it was already proven in production for the welcome modal. Native `confirm()` is retired for these two call sites.

**Implementation:** generalised the pattern into a reusable `partials/confirm_modal.html` + `static/js/confirm-modal.js`, rather than duplicating a second bespoke modal — a new component was needed because `welcome_modal.html` is a single-purpose, non-parameterised dialog, not because the existing pattern was rejected.

## Decision 2 — Student home/history labels: "Dashboard"/"Analytics" (shared, colliding) vs. a name reserved once per concept

**Competing implementations found:**
1. Legacy Learning Workspace tree: "Dashboard" (home), "Analytics" (history-adjacent).
2. Canonical Student Experience tree: also "Dashboard" (home — identical label, structurally different screen), "Analytics" (history — identical label, routes to a *different* template/endpoint than legacy Analytics).

This was not two different solutions to choose between — it was the **same label reused for different screens**, which is a worse failure mode than two different labels for the same screen (`CONSISTENCY_AUDIT.md` §1 calls "Analytics" a case of "consistent labelling masking inconsistent implementation").

**Decision: neither existing label is the standard.** The canonical Student Experience — the surface Stage 1 students actually reach under `SOLE_RUNTIME=1` — gets one reserved name per concept: **Home** (already the internal/doc name per `PRODUCT_LANGUAGE_GUIDE.md` §1, just not what the UI rendered) and **History** (new, since "Analytics" was ambiguous with the Founder-facing, differently-scoped Analytics concept). The legacy tree's "Dashboard" is left as-is (see `FRICTION_RESOLUTION_MATRIX.md` T1-1 for why renaming a screen production never serves was out of scope), but it can no longer collide with the canonical Home label a student might see in the same session.

## Decision 3 — Analytics KPI density: 6-per-row vs. the product's own 4-per-row rule

**Competing implementations found:**
1. `analytics/index.html` — six KPI tiles in one row.
2. UX-001 §22, the product's own written design standard — "max four" KPI cards per row.

**Decision: the product's own standard is the standard**, not the screen that happened to ship differently from it. `analytics/index.html` was regrouped into rows of four or fewer. This was not a judgement call between two equally valid patterns — one of the two was already documented as the rule and the screen simply hadn't followed it.

## Decision 4 — Error-page "Reference ID" colour: off-palette pink vs. `tokens.css`

**Competing implementations found:**
1. A pink/magenta monospace colour on `errors/404.html` / `403.html` (likely a default Bootstrap `text-danger`-adjacent utility applied without checking it against the Kwalitec palette), not present in `tokens.css` or `COLOUR_SPECIFICATION.md`.
2. Every other muted/secondary text element in the product, which consistently uses the `tokens.css` muted-text token.

**Decision: `tokens.css`'s existing muted token is the standard**; the off-palette colour was a template-level deviation from an otherwise-sound system (`CONSISTENCY_AUDIT.md` §2: "the *system* is sound... violations found are all template-level deviations from a good system"), not a case requiring a new decision.

## Decision 5 — Coach panel vs. Mission card explanation: two places narrating the same "why"

**Competing implementations found:**
1. The Mission card's own `Why` / `Why now` / `Next` / `Benefit` explanation (via the explainability partial), visible on Home whenever the student is not in an active guided session or reflection.
2. The Coach panel's independent structured `coach_trust` list, rendering the *same four fields from the same underlying data* directly beside it — six of 20 PR-001 reviewers called this out as paraphrase, not new information.

**Decision: the Mission card is the standard bearer for that explanation; Coach must add something the Mission card does not carry, or step back.** Rather than picking one panel and deleting the other's whole *capability*, Coach's structured list is now conditional on whether it is the *only* place the explanation is visible (guided-session/reflection states) — the moment the Mission card is showing it, Coach shows commitment status or a pointer instead. This keeps Coach useful (it still owns commitment-status framing, which the Mission card doesn't carry) while eliminating the literal duplication PR-001 flagged.

## Decision 6 — Appearance/theme switcher: button-group control vs. `<select>` control (identified, not actioned — see rationale)

**Competing implementation found:** `CONSISTENCY_AUDIT.md` §6 (Low) flags "Preferences screen offers the same 3-way choice via two different controls (button group + `<select>`) on one screen": `settings/index.html`'s Preferences section renders both an `appearance-switcher` button group and a fallback `<select id="appearance-select">` for the identical Light/Dark/System choice. A separate, structurally duplicate Appearance button-group also exists on the Internal Alpha tab of the same Settings page.

**Decision: not actioned under PX-002A.** On inspection, the `<select>` on Preferences is not an accidental duplicate — it is pinned by an existing test (`tests/test_theme_system.py::test_settings_preferences_includes_appearance` asserts `data-appearance-select` must be present) and reads as an intentional progressive-enhancement fallback (a native `<select>` alongside a custom button-group control, for keyboard/assistive-technology robustness) rather than two competing implementations of the same idea. Collapsing the Internal Alpha tab's separate button-group into a single shared partial would touch a second pinned test (`test_internal_alpha_polish.py::test_internal_alpha_page_renders` asserts `data-appearance-option="light"` on that route) and is not itemised in `HIGH_PRIORITY_BACKLOG.md`'s Tier 1/Tier 2 list — only in the broader, Low-severity `CONSISTENCY_AUDIT.md` §6. Per this programme's brief ("resolve confirmed Tier 2 issues where they naturally fall within the implementation" — this one did not), it is logged here rather than silently dropped, and left for a future pass that can extract one shared appearance-switcher partial and update both tests deliberately.

## Decision 7 — Session-duration wording: independently-built strings vs. one shared formatter

**Competing implementations found:** duration strings for Home and Mission-adjacent surfaces were each built inline, per view model, with no shared rounding or phrasing rule — not a case of two deliberately different components, but of the same formatting logic having been written more than once with no guarantee the two copies stay in sync.

**Decision: one shared module (`app/presentation/formatting.py`) is the standard**, and every touched view model now calls into it rather than re-implementing the phrase locally. See `TERMINOLOGY_STANDARD.md` §2 and `FRICTION_RESOLUTION_MATRIX.md` T1-2 for the numeric (data-source) half of this problem, which remains open pending a Runtime A decision outside this programme's scope.

---

## Not decided under this programme

- **Icon sourcing** (`CONSISTENCY_AUDIT.md` §2/§4: inline SVGs hand-duplicated per template rather than centrally sourced). This is a structural drift-*risk*, not a currently-visible inconsistency (today's icons are coincidentally uniform) — see `FRICTION_RESOLUTION_MATRIX.md` T2-10 (Deferred).
- **The two navigation trees themselves** (dark left-rail vs. light top-nav). PX-001 already treats this as an architecture question with its own mitigation (`SOLE_RUNTIME`) and evidence trail (EP-007.2), not a copy/consistency decision this programme is positioned to make — see T1-4.
