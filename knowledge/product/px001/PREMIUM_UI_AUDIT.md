# PX-001 — Premium Experience Audit

**Program:** PX-001 — Premium Experience Audit
**Status:** Analysis only. No code changed. No screens redesigned. No commit made.
**Date:** 2026-07-26
**Scope:** Full application — every student-facing screen, state, and interaction currently reachable in Version 1, evaluated before Render deployment and before Stage 1 external pilot. The separate Kwalitec Console operator/founder admin surface (`app/founder/dashboard/templates/`, 26 templates, e.g. Console overview, Curriculum Studio, evidence gates, participant management) is **out of scope** — it is not student-facing and was not reviewed screen-by-screen; it is referenced only where it shares a layout shell with in-scope surfaces.

---

## 1. Method and sources

This audit is **read-only analysis**. No application code, template, or stylesheet was modified while producing it.

Evidence used:

| Source | What it provided |
|---|---|
| `app/templates/**/*.html` (81 templates), `app/static/css/*.css`, `app/*/routes.py`, `app/presentation/**` | Live markup, design tokens, and route/navigation truth |
| `knowledge/reviews/V1_REVIEW_PACKAGE/` (docs + 70 screenshots) | The exact package PR-001 reviewers judged, including desktop screenshots at 1440×900 in light and dark theme |
| `knowledge/product/pr001_internal_blind_review/` (20 reviews, thematic analysis, score summary, improvement priority) | Simulated student verdicts and quantified friction |
| `knowledge/design/BRAND_GUIDELINES.md`, `knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md` (UX-001) | Kwalitec's own premium bar — used as the primary rubric, since it already names Apple/Linear/Notion as benchmarks |
| `knowledge/architecture/NAVIGATION_AUDIT.md`, `app/application/config/v2_flags.py`, `render.yaml`, `docs/architecture/*.md` | Ground truth on which navigation stack is actually live for Render production |
| `knowledge/GOVERNANCE.md`, `knowledge/product/vision/PRODUCT_VISION_2030.md` | Explainability/recommendation-quality guardrails and north-star language |

Where a finding could be verified directly against current code (not just a screenshot), that is stated. Two items visible in the PR-001 screenshot package (an "Open Version 2 Learning Experience" link and a "Back to Dashboard" footer link on the canonical Home) were checked against the live templates and **no longer exist in code** — see `PR001_ALIGNMENT_REPORT.md` §2 for the discrepancy and its implications for how PR-001 findings should be read.

---

## 2. Premium benchmark comparison

Kwalitec's own standard (`UI_UX_IMPLEMENTATION_STANDARD.md`, "UX-001") already sets Apple, Linear, and Notion as the reference bar and states the golden rule: *"Kwalitec is not trying to look modern. It is trying to look timeless."* This audit extends that same rubric to the benchmark set specified for PX-001 (Linear, Stripe Dashboard, Raycast, Apple HIG, Notion Calendar), judging **principles, not appearance**.

| Dimension | Benchmark expectation | Kwalitec today | Rating |
|---|---|---|---|
| **Clarity** | One primary object per screen; no ambiguity about what matters | Home/Mission ("Today's Mission") is clear in isolation; Analytics and Study Plan roadmap sometimes present many equally-weighted numbers with no ranking | Partial |
| **Consistency** | One design language, one nav model, one vocabulary | Two co-existing navigation shells (legacy sidebar vs. canonical top nav) share the same page name ("Dashboard") for structurally different screens; icon set is hand-inlined per template rather than a single shared source | Fails in places (see `CONSISTENCY_AUDIT.md`) |
| **Hierarchy** | Eye moves top → down without competing signals | Card-grid dashboards (`dashboard/index.html`, `student/home.html`) generally follow a clear top-to-bottom flow; Analytics shows 6 KPI tiles in one row against the product's own 4-per-row rule | Partial |
| **Calmness** | Absence of urgency/anxiety cues where none is warranted | Empty/zero states in Analytics use warning-triangle icons for "Only studied 0 days" on a brand-new account — reads as reproach rather than encouragement | Fails in places |
| **Focus** | Single obvious next action | Daily Mission / Start Session pattern is genuinely strong — this is the one place Kwalitec already matches the benchmark | Pass |
| **Craftsmanship** | Deliberate spacing, no accidental duplication, no leftover scaffolding | Tokens file (`tokens.css`) is disciplined and well-authored; but student-facing screens leak internal build metadata (commit hash, environment, "Learning profile status") that a premium product would never surface | Partial |

**Overall reading:** Kwalitec's *foundations* (design tokens, one font, 8-point spacing, a genuine internal standard that already quotes the right benchmarks) are more mature than the *execution* across every screen. The gap is not a missing design system — it is inconsistent application of the one that already exists, plus unresolved product-architecture residue (two navigation stacks) leaking into copy and structure.

---

## 3. Findings by checklist category

### 3.1 Typography

- `tokens.css` correctly implements the UX-001 hierarchy (40/28/20/16/14 via `--font-4xl…--font-xs`) on Inter only — no competing font families found in templates. **Compliant.**
- Page-title conventions are inconsistent in practice: the legacy Dashboard uses an eyebrow ("LEARNING WORKSPACE") + H1 ("Student Dashboard") + description pattern; the canonical Home uses eyebrow ("YOUR LEARNING") + H1 ("Dashboard") + description. Same visual grammar, different label for the same concept — a typography-hierarchy pattern applied consistently, undermined by a copy inconsistency (see `CONSISTENCY_AUDIT.md` §1).
- Numeric typography is inconsistent in precision: exam countdown ("200 Days Remaining"), readiness ("199.98" remaining study hours), and roadmap topic estimates ("11.4h", "7.3h", "30.0h") mix whole numbers with two-decimal precision that reads as false precision rather than calm confidence (`study_plan/view.html` roadmap cards; screenshot `30-study-plan-view.png`).

### 3.2 Spacing, alignment, margins, padding

- The 8-point scale in `tokens.css` (`--space-xs` … `--space-4xl`) is well-formed and used consistently inside components that were built against it (cards, skeletons).
- Canonical shell pages that are still light on content (`student/journey.html`, `student/revision.html`) leave 60–70% of the viewport below the fold as flat, uninterrupted background (screenshots `05-journey.png`, `06-revision.png`). UX-001 asks for "whitespace as a feature," but this reads as an unfinished page rather than an intentionally calm one — there is no illustration, secondary content, or affordance filling that space, which is the difference between "spacious" and "empty."
- Legacy Analytics stacks 6 KPI tiles across one row on a 1440px viewport (screenshot `10-analytics-legacy.png`), directly against the product's own dashboard rule ("Maximum four KPI cards per row," UX-001 §22).

### 3.3 Navigation

This is the single most substantiated finding in the whole audit and is treated in full in `PR001_ALIGNMENT_REPORT.md` and `CONSISTENCY_AUDIT.md`. Summary:

- Two structurally distinct navigation trees exist in one file, `app/templates/partials/sidebar.html`, branching on `v2_flags.SOLE_RUNTIME`: a dark left-rail "Learning Workspace" tree (Dashboard · Study Plan · Session · Analytics · Settings · Share Feedback · Help) and a light top-nav "Student Experience" tree (Dashboard · Journey · Revision · Analytics · Settings · Study Plan · Help).
- `render.yaml` sets `KWALITEC_V2_SOLE_RUNTIME=1` for the deployed environment, so only the canonical tree should render in production. This materially reduces — but does not eliminate — the dual-home risk for the actual Render deployment (see `PR001_ALIGNMENT_REPORT.md` §2 for the full nuance, including why PR-001's simulated reviewers still rated Navigation lowest of all ten categories).
- Both trees label their home entry **"Dashboard."** Even with only one tree live at a time, this label is reused for two conceptually different products in the codebase and in internal documentation, which is a durable source of confusion for anyone cross-referencing screenshots, support tickets, or prior review packages against the live app.
- Two now-removed dual-run CTAs ("Open Version 2 Learning Experience," "Back to Dashboard") are visible in the PR-001 screenshot package but absent from current templates — confirmed by direct grep. This is genuine, already-completed progress that predates this audit.

### 3.4 Buttons

- Primary/secondary/ghost button styling is applied consistently through Bootstrap utility classes plus `tokens.css` overrides (`btn-primary`, `btn-outline`), matching UX-001 §9 in spirit.
- Two archive/delete actions in Study Plan use the **native browser `confirm()` dialog** rather than a styled confirmation (`settings/index.html` restore action: `onclick="return confirm('This will replace all existing data with the backup. Continue?')"`; Study Plan archive/delete per `KNOWN_LIMITATIONS.md` #19). This is the single clearest "component system" violation — an unstyled OS dialog breaking into an otherwise on-brand product for the two highest-stakes destructive actions in the app (deleting a study plan, overwriting all learning data).
- Primary CTA copy is inconsistent across equivalent actions: "Start Session" (Home), "Start Study Session" (Mission), "Resume Study Session" (Dashboard/Mission when in progress) — three different verbs for the same action depending on which shell renders it.

### 3.5 Cards

- Card geometry (16px radius, soft shadow, no gradient) is consistently implemented and matches UX-001 §10 well — this is one of the stronger, more consistent primitives in the product.
- Card *density* is inconsistent across the two shells: legacy Dashboard cards carry 3–5 lines of explanatory microcopy per card; canonical Home/Journey/Revision cards are often a title plus one line, leaving noticeably more unused card real estate.

### 3.6 Colour usage

- Palette adherence to `BRAND_GUIDELINES.md` is generally good (Primary Blue for primary actions, Gold reserved for the alpha badge/accent use, not used for primary buttons or navigation — correctly following UX-001 §3).
- One clear off-system colour: the "Reference ID" shown on 403/404/500 error pages renders in a bright pink/magenta monospace token that does not appear anywhere in `COLOUR_SPECIFICATION.md` or `tokens.css`'s named palette (screenshots `error-404.png`, `error-403-or-denied.png`). It reads as a debug artifact left in a customer-facing error screen.
- Dark theme (`[data-theme="dark"]` in `tokens.css`) is implemented as a complete second palette, not an inverted filter, and renders correctly across the one dark screenshot available (`51-theme-dark.png`) — a genuine strength.

### 3.7 Copy

Covered in full in `COPY_REVIEW.md`. Headline findings: repeated internal/technical vocabulary shown directly to students ("Education Operating System," build/commit/environment metadata in Settings, "Learning profile status"), duplicated boilerplate ("Learning Outcomes Not available yet" repeated on all 14 topic cards of a single Study Plan roadmap), and a very long conditional copy stack possible on the canonical Home hero (`student/home.html`, lines 23–314) that can render up to ten stacked explanatory lines depending on feature-flag state.

### 3.8 Iconography

- Icons are hand-authored inline SVG per template rather than sourced from one shared partial/icon set. Visual style (24px, 1.75 stroke width, rounded caps) is consistent enough to look like a single system, but UX-001 §7 mandates "Lucide Icons exclusively… never mix icon libraries" as a controlled dependency — the current approach cannot be verified as a single controlled source and is at risk of silently drifting (e.g., two different clock icons, or inconsistent stroke widths, entering the codebase from different contributors/times without anyone noticing at review time).

### 3.9 Interaction hierarchy

- The Daily Mission / Start Session interaction is the clearest, most confidently hierarchical pattern in the product: one heading, one duration, one reason, one button. This is the pattern PR-001 praised most and should be treated as the reference implementation for every other primary screen.
- The canonical Home hero (`student/home.html`) does not consistently reach that bar: depending on flag/state combination, the hero can stack greeting → eyebrow → title → status → duration → purpose → "why now" → expected benefit → readiness bridge → suggested next action → plan coherence → commitment state → confidence → expected outcome → progress summary, before the primary button even appears. Even though most of these are mutually exclusive in a given state, the template shows this is a screen that *can* become a wall of stacked assertions rather than the one-line clarity of the Mission pattern it is meant to be a superset of.

### 3.10 Accessibility

- `skip-link`, `aria-label`, `aria-live`/`role="status"`, and `role="alert"` patterns appear correctly in the base layouts and forms (`layouts/base.html` line 22; `auth/login.html` lines 90, 97).
- Appearance switcher buttons correctly use `aria-pressed` and `role="group"`.
- Native `confirm()` dialogs (§3.4) are a genuine accessibility regression relative to the rest of the product — they bypass the app's own focus/contrast/motion system entirely and behave unpredictably with screen readers depending on browser.
- The off-palette pink "Reference ID" text has not been checked for WCAG AA contrast against the light background; given it does not appear in the documented palette at all, contrast compliance cannot be assumed and should be verified before Stage 1.
- No systemic alt-text or heading-order violations were found in the templates sampled.
- The canonical Home's inline reflection options are rendered as `<span>` elements with `data-presentation-only="true"` and `role="status"` — visually styled to look like selectable choices but not focusable or operable as form controls (`student/home.html` reflection block). This is a genuine accessibility gap: a screen reader or keyboard-only user encounters a status announcement, not an interactive choice, at the exact moment sighted mouse users are invited to click.
- **Evidence caveat:** none of PR-001's 20 written reviews comment on accessibility (screen readers, contrast, keyboard navigation) or mobile/responsive layout at all — the persona pool exclusively walked through desktop-style sessions. Every accessibility and responsiveness finding in this section is based on direct code inspection, not corroborated or contradicted by simulated student evidence.
- **No product brand/logo asset system exists in the repository.** `git ls-files` returns zero tracked PNG/SVG/ICO/WebP/JPG image assets; there is no favicon, no Apple touch icon, no PWA manifest, and no Open Graph/Twitter card image, despite `partials/brand_meta.html` emitting `og:title`/`site_name` tags that reference a visual identity with no corresponding image. Branding currently depends entirely on typography (`.landing-brand-name`) and one inline SVG icon, and that treatment is itself inconsistent between the public/auth shell (icon + wordmark) and the authenticated shell (text-only `.sidebar-brand`). This is a concrete, verifiable gap against the brand mission's own bar — *"simple, modern, premium, minimal, and timeless — at home beside Stripe, Linear, Notion, GitHub, Vercel, and Figma"* (`BRAND_GUIDELINES.md`) — since none of those reference products ship without a favicon or share-preview image.

### 3.11 Responsiveness

- All available screenshots are desktop-only (1440×900 per `V1_REVIEW_PACKAGE/README.md`); no mobile or tablet capture exists in the evidence base used by PR-001 or this audit. This is a genuine gap: UX-001 §19 mandates "recompose, don't shrink" navigation and hierarchy at tablet/mobile widths, and neither PR-001 nor this audit can currently confirm that behaviour empirically. **This should be treated as an explicit unknown, not a pass**, ahead of a public pilot where a meaningful share of study-break usage is plausible on mobile.
- The sidebar/topnav both implement a documented collapse affordance (`data-sidebar-toggle`, backdrop dismiss in `sidebar.html` lines 3–5, 110), which is the right mechanism, but its actual behaviour was not visually verified in this evidence base.

### 3.12 Component consistency

Covered in full in `CONSISTENCY_AUDIT.md`. Headline: the product runs two parallel design executions (legacy Bootstrap-heavy dark-sidebar shell vs. canonical lighter top-nav shell) sharing one token file but not one component vocabulary, which is the structural reason many of the smaller inconsistencies above exist.

---

## 4. Product philosophy check

UX-001 asks every page to answer three questions ("What is important? What should I do next? What has changed?") and this programme's brief adds six explicit tests. Applied to the primary screens:

| Screen | Reduce decision fatigue | Increase trust | Improve clarity | Calm the student | Guide next action | Remove unnecessary thinking |
|---|---|---|---|---|---|---|
| Sign in | Pass | Partial (jargon undercuts calm trust — see §5) | Pass | Pass | Pass (one button) | Pass |
| Dashboard (legacy) | Pass | Pass | Pass | Pass | Pass | Pass |
| Home (canonical) | Partial (many optional panels compete for attention) | Partial (hero can stack many claims) | Partial | Partial | Pass (one CTA) | Partial |
| Today's Study Session / Mission | Pass | Pass | Pass | Pass | Pass | Pass |
| Session Reflection | Fail (no explanation of why reflection matters or what happens to the note) | Partial | Partial | Pass | Partial | Fail |
| Journey / Revision (canonical) | Pass (little to decide) | Partial (very little content to build trust from) | Partial | Fail (reads empty/unfinished, not calm) | Partial | Pass |
| Analytics (legacy) | Fail (6 KPI tiles + 6 charts + weekly report + lifetime stats, all at once) | Partial (all-zero charts before any use) | Fail | Fail (warning icons on a brand-new zero-history account) | Fail | Fail |
| Settings → General / Internal Alpha | Pass | Fail (exposes commit hash, environment, raw user ID) | Partial | Partial | N/A | Pass |
| Help & Support | Pass | Partial | Fail (no search, no topics, no actual help content) | Pass | Fail (four buttons, no guidance on which to use when) | Fail |
| Errors (403/404) | Pass | Partial (unexplained pink reference ID) | Pass | Pass | Pass | Pass |

**Pattern:** every screen built around a single recommended action (Mission, Sign in, error pages) passes almost every test. Every screen built as an open-ended dashboard of panels (Analytics, canonical Home in its richest state, Help) fails multiple tests. This is a structural, fixable pattern, not twelve unrelated defects.

---

## 5. Sign-in audit (explicit checks requested)

Evidence: `app/templates/auth/login.html`, `app/templates/layouts/auth_base.html`, screenshot `01-login.png`.

| Check | Finding |
|---|---|
| **Duplicate "Kwalitec"** | The logo lockup (icon + wordmark "Kwalitec") sits directly above a second, separate `<p class="landing-brand-name">Kwalitec</p>` heading (`login.html` lines 8–16). This is a real duplication: the wordmark already says "Kwalitec"; repeating it as a headline directly beneath adds no information and reads as unconfident branding rather than deliberate reinforcement. The onboarding note below it says "Kwalitec coordinator" twice more in two short paragraphs (lines 111–118). Four "Kwalitec" mentions in one screen. |
| **Visual hierarchy** | Left/right split (brand story vs. form) is a sound, premium pattern and matches the benchmark set well structurally. Within the left panel, hierarchy is muddied by three competing headline-weight elements in sequence: wordmark, "Kwalitec" name, "Education Operating System" descriptor — three things asking to be read as *the* headline. |
| **Brand presentation** | Strong use of the dark Deep Navy panel with the light wordmark, correctly following `BRAND_GUIDELINES.md`'s background rules. The gold accent dot and ascending stroke are preserved correctly at this size. |
| **Whitespace** | Right-hand sign-in card is well-proportioned and calm. Left panel is comparatively dense (badge, name, descriptor, value prop, 5 feature bullets, decorative shapes) for what should be the "breathing room" side of the layout. |
| **Primary action** | Single "Sign in" button, full width, correctly weighted as the only strong call to action on the form side. This part is done well. |
| **Trust signals** | "Internal Alpha · Founding Cohort" badge is honest and appropriately prominent. However, "Education Operating System" is a deliberately codified brand descriptor (`app/brand_identity.py:26`, `PRODUCT_DESCRIPTOR`, pinned by `tests/test_px001_brand_identity.py`) — not an accidental leak — that nonetheless reads as an internal systems/engineering term when it is the first thing a prospective student sees. It is reused verbatim across sign-in, onboarding step 1, and the meta description tag, so it is a single-source, low-effort fix if revised (see `COPY_REVIEW.md` §1). |

**Recommended direction (documented for the backlog, not implemented here):** collapse the lockup + name duplication into a single brand moment (icon+wordmark only, no repeated text headline), replace "Education Operating System" with outcome-oriented language consistent with the value proposition already present one line below it ("Know exactly what to study next"), and reduce the onboarding note's second "Kwalitec coordinator" mention now that it is already established in the first sentence.

---

## 6. Help Centre audit (explicit focus requested)

Evidence: `app/templates/alpha/help.html`, screenshot `18-help.png`.

The current Help & Support screen is not a help centre. It contains exactly two content blocks: a "Release information" table (application version, build date, environment, build number, build label, support contact) and a "Quick feedback" row of four buttons (Report a problem, Suggest an improvement, Full Product Check-in, Revisit onboarding). There is no FAQ, no article content, no search, and no contextual guidance of any kind.

| Requested capability | Present today |
|---|---|
| Search | Absent |
| Popular topics | Absent |
| Expandable help (accordions/disclosures) | Absent |
| Contextual guidance (in-context tips tied to the screen a student is on) | Absent — `partials/contextual_help.html` exists as a "learn more" disclosure component used on Home (readiness "Why this estimate?"), but it is not surfaced from, or linked to, the Help screen itself |

No long paragraphs were found on this specific screen (its problem is emptiness, not verbosity) — but the release-information table is release-engineering content, not student help, and occupies the majority of the screen. See `COPY_REVIEW.md` §2 for the technical-language findings on this screen, and `HIGH_PRIORITY_BACKLOG.md` for the prioritized recommendation.

**Evidence caveat:** none of PR-001's 20 written reviews mention the Help screen at all — not as helpful, missing, or a source of friction. This finding is based entirely on direct inspection of `alpha/help.html`; it is not corroborated (or contradicted) by simulated student evidence. It should be weighted accordingly relative to the three PR-001-mandated friction points, even though the programme brief specifically requested this screen receive attention.

---

## 7. Severity distribution (this document's findings only)

| Severity | Count | Examples |
|---|---:|---|
| Critical | 2 | Two co-existing navigation trees sharing the "Dashboard" label; native unstyled `confirm()` for destructive data actions |
| High | 5 | Technical/internal jargon exposed to students (Settings, sign-in "Education Operating System"); Help Centre has no actual help content; Analytics exceeds the product's own 4-KPI-per-row rule and reads as alarming rather than calm on a zero-history account; Reflection screen provides no value framing; unverified mobile/tablet responsiveness |
| Medium | 7 | Off-palette error "Reference ID" colour; duplicate/verbose boilerplate copy ("Not available yet" ×14); inconsistent CTA verbs for the same action; icon system not centrally sourced; empty canonical shell pages read as unfinished rather than calm; numeric false-precision in estimates; reflection choice controls not keyboard/screen-reader operable |
| Low | 4 | Duplicate "Kwalitec" wordmark/name on sign-in; card content density asymmetry between shells; persistent Internal Alpha badge chrome (expected for this programme phase); no favicon/PWA manifest/share-preview image anywhere in the repo |

Full severity/effort/owner detail with recommended fixes lives in `HIGH_PRIORITY_BACKLOG.md`.
