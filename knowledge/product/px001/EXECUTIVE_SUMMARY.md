# PX-001 — Premium Experience Audit: Executive Summary

**Status:** Analysis only. No code changed. No screens redesigned. No commit made.
**Date:** 2026-07-26
**Audience:** Product/founder decision-makers preparing for Render deployment and the Stage 1 external pilot.

---

## Verdict

Kwalitec's design **foundations are genuinely strong** — a disciplined token system, a written internal standard (`UI_UX_IMPLEMENTATION_STANDARD.md`) that already benchmarks Apple/Linear/Notion correctly, on-brand colour and typography discipline, and at least three screens (Daily Mission, Commitment/Defer, Study Plan) that would not look out of place next to the premium products this programme was asked to benchmark against.

What is not yet premium is **consistency of execution** across the two navigation stacks the product currently maintains, and **completeness of a small number of screens** (Reflection, Help & Support, Analytics) that do not yet carry the same care as the product's best work. Nothing found in this audit requires a ground-up redesign. Everything found is either a naming/copy decision, a component-reuse gap, or a content addition to an existing, working template.

This assessment is deliberately consistent with, not independent of, PR-001's simulated findings — this audit exists specifically to verify PR-001's claims against real code and screenshots, and in every case (dual homes, duration conflict, reflection) it found direct, reproducible evidence supporting PR-001's conclusions, plus two pieces of good news PR-001 could not have known: two of the specific screen elements it likely reacted to have already been removed from the codebase (§3).

---

## The three things that matter most

1. **The same word, "Dashboard," names two different home screens.** Kwalitec runs two coexisting navigation stacks (a legacy dark-sidebar "Learning Workspace" and a canonical light-topnav "Student Experience"), gated by one feature flag. Render production is configured to show only one (`KWALITEC_V2_SOLE_RUNTIME=1` in `render.yaml`), which meaningfully reduces the literal dual-home problem for real pilot students. But both stacks' home screens are independently labelled "Dashboard," so the confusion PR-001's twenty simulated reviewers converged on (Navigation: lowest-but-one category, mean 4.60/10, tightly agreed at σ 0.58) persists as a naming problem even where the architecture is mitigated.

2. **The exact same study topic shows two different durations — 30 minutes on one screen, 90 minutes on another — for the same student, the same day.** This is not an inference from user complaints; it is directly visible in two screenshots in the review package used for PR-001 (`04-dashboard-student.png` vs. `09-mission.png`). PR-001's own words describe this class of issue precisely: *"Cohesion bugs (two homes, mismatched durations) read as trust failures, not minor UI nits."*

3. **Reflection is the lowest-scoring category PR-001 measured (4.55/10 of ten categories), and the product already has the words to fix it — they are just in the wrong place.** Onboarding already tells students reflection "helps Kwalitec understand how the session felt and keeps tomorrow's guidance honest." That sentence never reappears when a student actually reaches the Reflection screen itself.

All three are addressed with specific, scoped recommendations in `HIGH_PRIORITY_BACKLOG.md` Tier 1, and none require touching the three patterns PR-001 explicitly praised (Daily Mission, Commitment/Defer, Study Plan clarity) — those should be left alone and used as the reference standard for fixing everything else.

---

## What is already good — protect it

- **Daily Mission / Today's Study Session** (`mission/index.html`): topic, duration, reason, checklist, one button. This is the strongest single interaction pattern in the product and the thing PR-001's reviewers praised most consistently.
- **Commitment / Defer workflow**: an honest "Not today" option with reason codes instead of a forced binary — exactly the "agency without shame" pattern PR-001 called unexpectedly central to trust.
- **Study Plan clarity** (wizard + roadmap view): concrete exam/date/minutes inputs and an honest supported/unsupported matrix — PR-001's highest-scoring category (6.3/10).
- **Study Session Feedback** screen's explainability copy ("What did Kwalitec observe? / What can Kwalitec honestly conclude? / What happens next?") is genuinely excellent and should be the house style extended to Reflection and elsewhere, not replaced.
- **Design tokens** (`tokens.css`): correctly implements the 8-point spacing grid, Inter-only typography hierarchy, and documented brand colours almost everywhere it was checked.

---

## What needs attention before a public pilot

| Theme | Headline finding | Full detail |
|---|---|---|
| Navigation & naming | Two stacks share the label "Dashboard"; four of five core concepts have inconsistent names across screens | `PR001_ALIGNMENT_REPORT.md` §3, `CONSISTENCY_AUDIT.md` §1 |
| Trust / duration | Same topic, two different time estimates, no explanation of the discrepancy | `PR001_ALIGNMENT_REPORT.md` §4 |
| Reflection | Lowest-scoring category; missing value framing that already exists elsewhere in the product | `PR001_ALIGNMENT_REPORT.md` §5, `COPY_REVIEW.md` §5 |
| Technical language leaking to students | Commit hashes, environment strings, raw user IDs, and "Learning profile status" shown in Settings; "Education Operating System" branding reads as a systems metaphor at first touch | `COPY_REVIEW.md` §2, §1 |
| Help Centre | No search, topics, FAQ, or contextual guidance — currently a release-info table and four feedback buttons | `PREMIUM_UI_AUDIT.md` §6 |
| Component discipline | Native browser confirmation dialogs used for the two most destructive actions, despite a working styled-modal pattern already existing | `CONSISTENCY_AUDIT.md` §3 |
| Analytics calmness | Six KPI tiles in one row (the product's own rule is four); warning icons on a brand-new zero-history account | `SCREEN_BY_SCREEN_REVIEW.md` §5.4 |

---

## Good news the review package could not show

Two specific dual-run artifacts visible in the PR-001 screenshot set — an "Open Version 2 Learning Experience" link and a "Back to Dashboard" footer link — were checked against the live codebase and **no longer exist**, per `docs/architecture/PHASE_1_CONSOLIDATION_REPORT.md`'s recorded removal and confirmed by direct search of `app/templates/`. The screenshot package PR-001 reviewed predates this cleanup. This does not resolve the underlying two-stack architecture (still present and still the root cause of finding #1 above), but it is verifiable, already-completed progress worth crediting. See `PR001_ALIGNMENT_REPORT.md` §2 for the full discrepancy note and a recommendation to re-capture the review package before any future blind-review programme.

---

## What this audit deliberately does not recommend

Per PR-001's own explicit instruction (*"What not to prioritise from this corpus alone: Visual polish unrelated to study blockers; new gamification; pass-rate claims"*), this audit does not recommend treating premium-polish findings (icon sourcing, off-palette error colour, numeric precision) as equal in priority to the cohesion/trust findings above. `HIGH_PRIORITY_BACKLOG.md` is explicitly tiered to reflect this. Likelihood of Continued Use — PR-001's most polarising category — is assessed as primarily a subject-coverage/product-scope question (only 3 of 8+ listed exam bodies are fully supported in Version 1), not a UI/UX defect, and is out of scope for a design-quality recommendation.

---

## Readiness framing for Stage 1

This is a UX/design-quality analysis, not a release-gate assessment. It makes no claim about Version 1 production-readiness (see `VERSION_1_RELEASE_FRAMEWORK.md` G1–G12, which this programme does not touch) and no KSI claim (ΔKSI = 0 for this analysis-only programme, per `COMPLETION_REPORT.md`). What it does establish: the specific, PR-001-mandated friction points are real, reproducible, and — based on the evidence gathered — addressable without architectural rewrites, using patterns the product has already proven work well elsewhere in its own codebase.

---

## Deliverables in this programme

| Document | Contents |
|---|---|
| `PREMIUM_UI_AUDIT.md` | Full checklist audit (typography, spacing, navigation, buttons, cards, colour, copy, iconography, interaction hierarchy, accessibility, responsiveness, component consistency), premium benchmark comparison, product philosophy check, sign-in and Help Centre deep dives |
| `SCREEN_BY_SCREEN_REVIEW.md` | Every reachable screen/state, grouped by feature area, with severity-tagged findings |
| `PR001_ALIGNMENT_REPORT.md` | Direct mapping of PR-001's mandatory findings to code/screenshot evidence, including the package-freshness discrepancy |
| `COPY_REVIEW.md` | Branding duplication, technical jargon, repeated boilerplate, and specific rewrite directions |
| `CONSISTENCY_AUDIT.md` | Terminology matrix, design-token compliance table, component/dialog consistency |
| `HIGH_PRIORITY_BACKLOG.md` | Tiered, severity/effort-scored backlog ready for a future implementation programme's planning — not authorization to implement |
| `COMPLETION_REPORT.md` | Formal programme completion record |
