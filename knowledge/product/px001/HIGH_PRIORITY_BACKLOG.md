# PX-001 — High Priority Backlog

**Status:** Analysis only. This is a prioritized, documented backlog for a future implementation programme. **Nothing in this document has been implemented.** No code changed, no screens redesigned, no commit made under PX-001.

**Structure:** Two tiers, per PR-001's own explicit instruction (`IMPROVEMENT_PRIORITY.md`: *"What not to prioritise from this corpus alone: Visual polish unrelated to study blockers"*):

- **Tier 1 — Cohesion & trust.** Directly traceable to PR-001's top three friction findings (dual homes, duration/terminology conflict, reflection value). These should be sequenced before Tier 2 in any future implementation programme.
- **Tier 2 — Premium polish.** Real, evidence-backed findings from this audit that improve craftsmanship and benchmark parity (Linear/Stripe/Raycast/Apple HIG/Notion Calendar) but were not what PR-001's simulated students flagged as blocking.

Effort is a rough sizing signal only (S = small/contained, M = medium/cross-cutting, L = large/architectural), not an estimate for engineering to commit to.

---

## Tier 1 — Cohesion & trust

### T1-1. Resolve the shared "Dashboard" label across both navigation stacks

| Field | Detail |
|---|---|
| Severity | Critical |
| Screen(s) | `dashboard/index.html` (legacy), `student/home.html` (canonical), both nav trees in `sidebar.html` |
| Description | Legacy Learning Workspace home and canonical Student Experience home both render the H1/nav label "Dashboard," despite being structurally different screens on different data sources (see `PR001_ALIGNMENT_REPORT.md` §3, `CONSISTENCY_AUDIT.md` §1) |
| Why it hurts | Directly implicated in PR-001's lowest-variance low score (Navigation, mean 4.60, σ 0.58) — a broadly and consistently shared complaint, not an outlier. Anyone cross-referencing a screenshot, support ticket, or prior review against the live app cannot use "Dashboard" as a disambiguator. |
| Recommended solution | Adopt one canonical name for the "what to do next" home screen (e.g., "Home") and apply it consistently to whichever stack is live, independent of which flag state is active; retire "Dashboard" as the label for this screen in favour of a name reserved (if needed) for an actual multi-metric overview screen |
| Expected benefit | Directly targets PR-001's #1 and #2 improvement priorities; removes a screen-visible collision independent of any deeper architecture work |
| Estimated effort | S — copy/label change in a small number of templates; no data-model change |

### T1-2. Establish one authoritative session-duration label

| Field | Detail |
|---|---|
| Severity | Critical |
| Screen(s) | `student/home.html` ("30 minutes"), `mission/index.html` ("90 min") — same topic, same account, confirmed via screenshots `04-dashboard-student.png` and `09-mission.png` |
| Description | The identical topic shows two different duration estimates depending on which surface renders it |
| Why it hurts | The single most citable, reproducible defect in the entire review — a 3× numeric contradiction for the same fact, on the same day, for the same student. PR-001 explicitly names this as friction #2 and its `COMPLETION_REPORT.md` calls "cohesion bugs (two homes, mismatched durations)" **trust failures, not minor UI nits.** |
| Recommended solution | Pick one authoritative duration source and one label (e.g., always show the plan-derived minutes, or always show the mission-engine estimate) and apply it identically everywhere a duration appears for a given day's topic. This is a content/consistency decision to make first; the deeper two-computation architecture (`SOURCE_OF_TRUTH_ANALYSIS.md`) is a separate, larger effort outside this programme's scope. |
| Expected benefit | Removes the single clearest "trust failure" cited in PR-001; likely to move Recommendation Trust (mean 5.4) and Navigation (mean 4.60) together, since both categories cite this same contradiction |
| Estimated effort | M — requires a product decision on which source is authoritative before any template change; template change itself is small once decided |

### T1-3. Add value framing to the Reflection screen

| Field | Detail |
|---|---|
| Severity | High |
| Screen(s) | `session/reflection.html`, `session/components/reflection_card.html` |
| Description | The Reflection screen never explains why it exists or what happens to the note (see `PR001_ALIGNMENT_REPORT.md` §5, `COPY_REVIEW.md` §5) |
| Why it hurts | Reflection Workflow is PR-001's single lowest-scoring category of ten (mean 4.55). Thematic analysis: *"Reflection is appreciated in principle, skipped in practice."* |
| Recommended solution | Reuse the explanatory sentence already written for Onboarding step 4 ("It helps Kwalitec understand how the session felt and keeps tomorrow's guidance honest") or the tone of the Study Session Feedback screen, and surface it directly on the Reflection screen at the moment it matters — not only once, days earlier, in onboarding |
| Expected benefit | Directly targets PR-001's #3 friction and improvement priority #3 ("Deeper reflection / mistake insight"); low-risk since the copy tone already exists and is proven elsewhere in the product |
| Estimated effort | S — copy addition to an existing template; no new logic required |

### T1-4. Confirm no non-production dual-home exposure ahead of Stage 1

| Field | Detail |
|---|---|
| Severity | High |
| Screen(s) | Both navigation trees; `render.yaml`; deployment/QA environment configuration |
| Description | `SOLE_RUNTIME=1` is confirmed for the Render production config, but the dual-run default (`SOLE_RUNTIME=0`) still renders both stacks' full experience in any environment that has not explicitly set the flag, and EP-007.2's dual-home "cleared" claim is scoped to W-PROD at Tier B/Medium confidence with N=0 external validation |
| Why it hurts | If any Stage 1 pilot participant, support demo, or QA session runs against an environment without the flag set, the exact dual-home experience PR-001 criticized will reappear in full, undoing the mitigation this report otherwise credits |
| Recommended solution | Not a code change — an operational verification: confirm the flag is set identically in every environment a real or prospective Stage 1 student could reach, and treat any deviation as a release blocker |
| Expected benefit | Protects the one piece of good news this audit found (production-side mitigation) from being silently undone by an environment misconfiguration |
| Estimated effort | S — configuration verification, not a code change |

---

## Tier 2 — Premium polish

### T2-1. Remove technical/build metadata from student-facing Settings

| Field | Detail |
|---|---|
| Severity | High |
| Screen(s) | `settings/index.html` (General, Internal Alpha sections), `alpha/help.html` |
| Description | Commit hash, environment string, raw user ID, and "Learning profile status: {twin_status}" shown directly to students |
| Why it hurts | No student decision depends on this information; it reads as an internal admin panel and undermines the "premium, timeless" brand positioning `BRAND_GUIDELINES.md` asks for |
| Recommended solution | Move to a collapsed "Diagnostic information" disclosure used only when a student is asked for it by support; rename or remove internal engine-state labels not meaningful to a student |
| Expected benefit | Removes the clearest "premium violation" found outside the PR-001-mandated areas; low technical risk since it is a display change only |
| Estimated effort | S |

### T2-2. Rebuild Help & Support as an actual help centre

| Field | Detail |
|---|---|
| Severity | High |
| Screen(s) | `alpha/help.html` |
| Description | Current screen is a release-info table plus four feedback buttons; no search, topics, FAQ, or contextual guidance exist (see `PREMIUM_UI_AUDIT.md` §6) |
| Why it hurts | Explicitly called out for particular attention in this programme's brief; a public pilot audience will have real "how do I..." questions this screen cannot currently answer |
| Recommended solution | Add search, a small set of popular-topic entries (e.g., "How is my study plan built," "What does readiness mean," "How do I change my exam"), and expandable (accordion) detail; link the existing `partials/contextual_help.html` "learn more" pattern from here so contextual and centralized help reinforce each other |
| Expected benefit | Meaningful reduction in support load during a public pilot; directly matches the requested Help Centre audit focus |
| Estimated effort | M — new content authoring plus a modest new component (search/accordion); no backend change required |

### T2-3. Bring Analytics within the product's own dashboard rules

| Field | Detail |
|---|---|
| Severity | Medium |
| Screen(s) | `analytics/index.html` |
| Description | Six KPI tiles in one row (product rule: max four); warning-triangle icons applied to zero-history "Areas for improvement" tips on what may be a brand-new account |
| Why it hurts | Directly contradicts the product's own written design standard (UX-001 §22) and the "calm the student" philosophy pillar — a new user's first Analytics visit can look like a list of failures rather than a fresh start |
| Recommended solution | Regroup KPIs into rows of four or fewer; suppress or soften "needs improvement" framing until there is enough history for it to be meaningful, replacing warning icons with neutral/encouraging ones for day-one accounts |
| Expected benefit | Improves first-week retention perception; low risk, presentation-only change |
| Estimated effort | S–M |

### T2-4. Replace native `confirm()` dialogs with the existing styled modal pattern

| Field | Detail |
|---|---|
| Severity | Medium |
| Screen(s) | Study Plan archive/delete, Settings → Restore from Backup |
| Description | Native browser dialogs used for the two most destructive actions in the product, while a working styled modal (`partials/welcome_modal.html`) already exists |
| Why it hurts | Breaks visual and accessibility consistency at the highest-stakes moments; native dialogs are unstyled, easy to dismiss accidentally, and behave inconsistently with the rest of the app's focus/motion system |
| Recommended solution | Extend the existing modal component to a generic confirmation variant and reuse it for both actions |
| Expected benefit | Removes the clearest component-system violation found in the audit; reduces risk of accidental data loss from an easy-to-miss browser dialog |
| Estimated effort | S–M — one reusable component, two call sites |

### T2-5. Fix the sign-in screen's brand redundancy

| Field | Detail |
|---|---|
| Severity | Low |
| Screen(s) | `auth/login.html` |
| Description | Logo lockup + separate "Kwalitec" headline + two "Kwalitec coordinator" mentions on one screen (see `PREMIUM_UI_AUDIT.md` §5, `COPY_REVIEW.md` §1) |
| Why it hurts | First impression screen; redundant branding reads as unconfident rather than reinforcing, undermining the "simple, modern, premium, minimal, timeless" bar `BRAND_GUIDELINES.md` sets for itself |
| Recommended solution | Remove the duplicate "Kwalitec" headline beneath the lockup; state "Kwalitec coordinator" once in the onboarding note instead of twice |
| Expected benefit | Small, low-risk craftsmanship improvement to the single highest-traffic screen in the product (every session starts here) |
| Estimated effort | S |

### T2-6. Reduce repeated boilerplate and numeric false precision

| Field | Detail |
|---|---|
| Severity | Medium |
| Screen(s) | `study_plan/view.html` (roadmap), Dashboard "Time Status" card |
| Description | "Learning Outcomes Not available yet" repeated on all 14 topic cards; "199.98" remaining hours and per-topic hour estimates carry two-decimal precision |
| Why it hurts | Repetition at scale reads as broken content rather than an honest disclaimer; false precision undercuts the calm, confident tone the rest of the roadmap otherwise achieves |
| Recommended solution | One top-level roadmap note instead of 14 repeats; round hour estimates to sensible increments |
| Expected benefit | Cleaner, more premium-feeling Study Plan detail screen — currently the highest-scoring surface in PR-001 (Clarity of Study Plan, mean 6.3) and worth protecting from small erosion |
| Estimated effort | S |

### T2-7. Correct the off-palette error-page "Reference ID" colour

| Field | Detail |
|---|---|
| Severity | Low |
| Screen(s) | `errors/404.html`, `errors/403.html` (and likely `500.html`) |
| Description | Pink/magenta monospace colour not present in `tokens.css` or `COLOUR_SPECIFICATION.md` |
| Why it hurts | Small but visible off-brand colour on every error a student can hit; unverified WCAG AA contrast |
| Recommended solution | Restyle using an existing muted/neutral token (e.g., `--text-muted`) and add one sentence of guidance on what to do with the reference ID |
| Expected benefit | Removes a small but concrete off-brand detail; near-zero implementation risk |
| Estimated effort | S |

### T2-8. Give Coach a reason to exist beyond restating the Mission card

| Field | Detail |
|---|---|
| Severity | Medium |
| Screen(s) | `student/home.html` (Coach insight panel) |
| Description | The Coach panel sits directly beside the Today's Mission card, which already carries its own "why" explanation via `partials/educational_explainability.html`; nothing currently differentiates what Coach adds from what the Mission card already states |
| Why it hurts | Ranked improvement priority #4 in `IMPROVEMENT_PRIORITY.md` (one place below the three mandatory friction points) and independently cited by 6 of 20 reviews as paraphrase rather than new information — see `PR001_ALIGNMENT_REPORT.md` §7. Not one of PR-001's three mandatory items, so it is sequenced in Tier 2, not Tier 1. |
| Recommended solution | Either give Coach a distinct information contract (e.g., only surface it when it has evidence the Mission card does not already show — a trend, a comparison to a past attempt, an adaptation signal) or remove it as a separate panel until it can meet that bar |
| Expected benefit | Removes a recurring "why does this exist" reaction without touching any of the three PR-001-mandated fixes |
| Estimated effort | M — likely a product-logic decision (what Coach is *for*) before any template change |

### T2-9. Add a minimal brand asset set (favicon, PWA icon, share-preview image)

| Field | Detail |
|---|---|
| Severity | Low |
| Screen(s) | All screens (browser tab, bookmarks, link previews) — `partials/brand_meta.html`, `layouts/base.html`, `layouts/auth_base.html` |
| Description | Zero tracked image assets exist in the repository. There is no favicon, no Apple touch icon, no PWA manifest, and no Open Graph/Twitter preview image, even though `brand_meta.html` already emits `og:title`/`site_name` tags implying one should exist |
| Why it hurts | A public pilot audience will see a blank/generic browser tab and a blank link preview when sharing or bookmarking the product — a small but visible gap against the brand's own "premium, at home beside Stripe, Linear, Notion" positioning (`BRAND_GUIDELINES.md`) |
| Recommended solution | Export the existing approved logo mark (per `BRAND_GUIDELINES.md`'s master artwork) into a standard favicon/touch-icon/OG-image set and wire it into the existing meta partial |
| Expected benefit | Small, low-risk craftsmanship fix; closes a gap that is otherwise invisible until someone actually looks for it (as this audit did) |
| Estimated effort | S — asset export plus a few `<link>`/`<meta>` tags; no template restructuring |

### T2-10. Centralize icon sourcing

| Field | Detail |
|---|---|
| Severity | Low |
| Screen(s) | All templates using inline SVG icons |
| Description | Icons are hand-duplicated inline per template rather than referenced from one shared source, against UX-001 §7's "single icon library" rule |
| Why it hurts | Not currently visible as inconsistency (style is coincidentally uniform today), but is a structural drift risk with no enforcement mechanism |
| Recommended solution | Introduce one shared icon partial/macro set (or a documented Lucide subset) and migrate templates incrementally |
| Expected benefit | Prevents future visual drift as more contributors touch the codebase; not urgent for Stage 1 |
| Estimated effort | M — mechanical but touches many files |

---

## Sequencing note

Per PR-001's own instruction, Tier 1 should be sequenced first in any implementation programme, because it addresses the specific friction points 20 independent simulated reviewers converged on. Tier 2 items are legitimate and evidence-backed but should not compete with Tier 1 for the same implementation window. **This document does not authorize implementation of either tier** — it is the analysis deliverable for a future, separately-scoped implementation programme.
