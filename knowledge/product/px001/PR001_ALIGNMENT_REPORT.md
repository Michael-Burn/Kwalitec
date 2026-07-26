# PX-001 — PR-001 Alignment Report

**Status:** Analysis only. No code changed.
**Purpose:** Map PR-001's mandatory findings (dual homes, inconsistent session durations, reflection workflow, lowest-rated categories) directly onto verifiable code and screenshot evidence, state what has already changed since PR-001 captured its evidence, and identify what remains open.

---

## 0. PR-001 in one page

| Field | Value |
|---|---|
| Method | 20 simulated blind student reviews (personas SV-001…SV-020) judged against `knowledge/reviews/V1_REVIEW_PACKAGE/` — documents **and** screenshots, not a live interactive session (`PR-001 COMPLETION_REPORT.md`) |
| Status | Simulated only — explicitly **not** Stage 1 pilot evidence, not educational-effectiveness evidence, ΔKSI = 0 |
| Grand mean (per-review) | 5.46 / 10 |
| Highest category | Clarity of Study Plan — 6.30 |
| Lowest categories | Reflection Workflow — 4.55; Navigation — 4.60 |
| Most polarising | Likelihood of Continued Use — mean 5.4, σ 1.5 |
| Top praise (thematic) | Daily mission / "what to study next"; Commitment/defer without shame; Study-plan wizard concreteness |
| Top criticism (thematic) | Dual homes / navigation complexity; inconsistent briefings/durations; shallow reflection |
| Explicit PR-001 instruction | *"What not to prioritise from this corpus alone: Visual polish unrelated to study blockers; new gamification; pass-rate claims"* (`IMPROVEMENT_PRIORITY.md`) |

This alignment report treats PR-001's method honestly: reviewers judged a **documentation-and-screenshot package**, not the live Render deployment, and that package is now demonstrably out of date in at least two specific, checkable ways (§2). This does not invalidate PR-001's findings — the underlying architecture that produced them is still in the codebase — but it changes how confidently each finding should be read today.

---

## 1. Strengths PR-001 said to preserve — verified in code

| PR-001 strength | Where it lives | Verification |
|---|---|---|
| Daily Mission clarity | `mission/index.html`, `student/home.html` hero (simple state) | Confirmed — screenshot `09-mission.png` shows the exact pattern reviewers praised: topic, duration, why, checklist, one CTA. Preserve this layout unchanged; see `SCREEN_BY_SCREEN_REVIEW.md` §3.1. |
| Commitment / Defer workflow | `student/home.html` lines 155–177 (`is_committed`, `is_deferred`, `show_defer_affordance`), `app/application/student_experience/recommendation_commitment.py` (referenced) | Confirmed in template — an honest, no-shame "Not today" disclosure with reason codes rather than a forced binary. This is exactly the "agency without shame" pattern PR-001's thematic analysis calls out. **Do not add friction, confirmation steps, or guilt-toned copy here.** |
| Study Plan clarity | `study_plan/wizard_step_1.html`, `study_plan/view.html` | Confirmed — concrete exam/sitting/date/minutes fields and an honest supported/unsupported matrix (screenshot `28-wizard-step-1.png`). The roadmap view (`30-study-plan-view.png`) is the highest-scoring surface in the product; its only issues are the repeated "Not available yet" boilerplate and numeric over-precision (`SCREEN_BY_SCREEN_REVIEW.md` §6.3), neither of which touches the structure PR-001 praised. |

**Explicit guardrail carried into `HIGH_PRIORITY_BACKLOG.md`:** none of the recommended fixes in this programme's output should touch the layout, copy tone, or interaction model of these three patterns. They are reference patterns other screens should move toward, not candidates for redesign.

---

## 2. Package-freshness discrepancy (read before trusting any "dual home" screenshot)

Two strings that appear in the PR-001 screenshot package were checked against the current `app/templates/` tree with a direct search and **do not exist in code today**:

| String | Appears in | Current code status |
|---|---|---|
| "Open Version 2 Learning Experience" | `42-empty-dashboard.png`, `54-welcome-modal.png`, `51-theme-dark.png` (all legacy Dashboard captures) | **Removed.** `docs/architecture/PHASE_1_CONSOLIDATION_REPORT.md` records: *"Dual-run 'Version 2 Learning Experience' / 'Back to Dashboard' CTAs removed."* Grep of `app/templates/` confirms zero matches. |
| "Back to Dashboard" (footer link on canonical Home/Journey) | `45-empty-journey.png` (and implied on other canonical empty states) | **Removed**, same commit reference as above. Zero matches in current templates. |

**Implication:** the PR-001 screenshot package was captured from a build that pre-dates at least one round of dual-run cleanup. Reviewers who cited these two literal links as evidence of "two homes" were, to that specific extent, describing a state that has already been partially remediated. This should be read as **encouraging, verifiable progress**, not as grounds to discount the underlying finding — because the two navigation *trees* themselves (not just these two links) still exist in `app/templates/partials/sidebar.html`, gated by `SOLE_RUNTIME` (§3). The link removal fixed a symptom; it did not, and was not intended to, remove the second stack.

**Recommendation for any future review package:** re-capture screenshots against the current build before running another blind-review programme, and note in the package which `KWALITEC_V2_SOLE_RUNTIME` value was active during capture, since that flag determines which of the two stacks a reviewer actually sees.

---

## 3. Friction #1 — Dual homes / multiple entry points / navigation forks

**PR-001 evidence:** Navigation is the second-lowest category (mean 4.60/10, narrow spread σ 0.58 — i.e. *consistently* rated low, not a few outliers pulling the average down). Thematic analysis: *"Dual homes (Learning Workspace Dashboard vs Student Home)... is the dominant friction cluster."* Improvement priority #1: *"Unify dual home / single start path."*

**Code verification:**

- `app/templates/partials/sidebar.html` contains two complete, hand-maintained navigation trees in one file, branching on `v2_flags.SOLE_RUNTIME` (lines 3–7, 18–60 vs. 61–106). Legacy tree: Dashboard · Study Plan · Session · Analytics · Settings · Share Feedback · Help. Canonical tree: Dashboard · Journey · Revision · Analytics · Settings · Study Plan · Help.
- `knowledge/architecture/NAVIGATION_AUDIT.md` (MS-001, dated 2026-07-25) independently documents the same two-stack architecture and states the root `/` route redirects to `student.home` under sole runtime, else `dashboard.index`.
- **Production mitigation, verified:** `render.yaml` sets `KWALITEC_V2_SOLE_RUNTIME=1` for the deployed environment (lines 34–47). Under this setting, `app/presentation/consolidation.py`'s `redirect_if_sole_runtime()` sends every legacy entry point (`/dashboard/`, `/missions/`, `/analytics/` in its legacy form) to the canonical Home. **This means a real Stage 1 pilot student on Render should only ever see one navigation tree in a single session — not two.**
- **What is not fully cleared:** `knowledge/product/ep007_2_canonical_journey_perception_validation/COMPLETION_REPORT.md` and `JOURNEY_PERCEPTION_REPORT.md` independently score this exact question and record dual-home as **"cleared" only within the W-PROD claim window (`SOLE_RUNTIME=ON`) at Tier B / Medium confidence**, with the residual explicitly still open for any dual-run environment (`SOLE_RUNTIME=OFF`, e.g. internal Alpha/QA) and for external N=0 (`K1_REVALIDATION.md`: *"External Stage 1 N=0 keeps K1 confidence at Medium"*). PR-001's screenshot package itself documents **both** stacks side by side without labelling one "production-only," so a reviewer following the package as instructed would reasonably perceive two live homes even though only one ships to Render.

**Verdict:** Architecturally substantially mitigated for the intended Render/Stage 1 path, but not fully closed:
1. The single-name collision ("Dashboard" used for both stacks' home screen, screenshots `03` vs `04`) persists regardless of which stack is live, because it is baked into both templates independently, not just into the flag branch.
2. Any environment that runs with `SOLE_RUNTIME=0` (documented as the Alpha/QA default) still exhibits the full dual-home experience PR-001 described.
3. No re-validation evidence exists yet at anything above Medium confidence for the production claim, and none exists at all for real external students (N=0).

**This is Tier 1 in `HIGH_PRIORITY_BACKLOG.md`** — not because the architecture is unaddressed, but because the residual (naming collision + any non-production exposure + unresolved confidence level) is exactly what PR-001 flagged as the most consequential single issue, and premium polish elsewhere will not move this category.

---

## 4. Friction #2 — Inconsistent session durations, conflicting briefings, different terminology

**PR-001 evidence:** Thematic analysis #2: *"thin Session Overview vs fuller Session briefing, and conflicting durations/status fields are the dominant friction cluster [alongside dual homes]."* Improvement priority #2: *"Align duration / briefing consistency (Home vs Learning Workspace Session)."*

**Code/screenshot verification — direct, reproducible:**

| Surface | Screenshot | Same topic | Duration shown |
|---|---|---|---|
| Home (canonical), Today's Mission | `04-dashboard-student.png` | "Review CS1-A: Descriptive statistics foundations" | **30 minutes** |
| Mission (legacy), Today's Study Session | `09-mission.png` | Same title, same date | **90 min** |

This is a 3× discrepancy for the identical topic on the identical account, visible in two screenshots in the same review package — the clearest, most citable single defect in this entire audit. `KNOWN_LIMITATIONS.md` #11 independently documents the same fact in prose.

**Terminology fragmentation (separate from the number itself):** the same underlying concept is labelled "Mission" (legacy nav item, `mission/routes.py`), "Session" (legacy nav item, same blueprint family), "Study Session" (page titles), and "Today's Mission" (canonical hero) depending on which screen renders it. `CONSISTENCY_AUDIT.md` §1 provides the full terminology matrix.

**Root cause (architecture, documented, not to be fixed under PX-001's analysis-only scope):** `knowledge/architecture/SOURCE_OF_TRUTH_ANALYSIS.md` confirms the canonical stack's duration figure and the legacy stack's duration figure come from **two independent computations** — canonical Home reads from demo-seeded opaque Adaptive/Mission projections when `INJECT_PHASE_I_ENGINES=False` (the current default), while legacy Mission reads from real `PlanningService`/SQL `Mission` rows. They are not currently required to agree, and nothing in the UI signals that they might not.

**Verdict:** Confirmed, current, high-severity, and — unlike §3 — **not mitigated by `SOLE_RUNTIME=1` in production**, because the conflict is between the canonical Home (`/student/`) and the canonical Session Experience's own Overview surface reading a *different* duration field (`estimated_duration_label` vs `estimated_study_label` in `student/home.html` lines 59–63) even within the single production stack, not only between legacy and canonical. This should be scoped, at minimum, as a **content/copy consistency pass** (one authoritative duration label, one source of truth for which field renders it) before Stage 1, even though the deeper data-architecture unification is out of this programme's scope.

---

## 5. Friction #3 — Reflection workflow lacks perceived value

**PR-001 evidence:** Reflection Workflow is the single lowest-scoring category (mean 4.55/10) across all ten dimensions. Thematic analysis #5: *"Reflection is appreciated in principle, skipped in practice... fewer find Product Check-in or thin 'what changed' copy worth scarce minutes."* Improvement priority #3: *"Deeper reflection / mistake insight (beyond attempted/correct counts)."*

**Code verification:**

- `session/components/reflection_card.html` (§4.3 of `SCREEN_BY_SCREEN_REVIEW.md`) renders a bare card: title, optional insight/confidence/improvement fields if present, a generic "reflection prompt," an optional note field, "Continue." **No copy anywhere on this screen explains why the reflection exists, what happens to the note, or how it affects tomorrow.**
- This is not a knowledge gap in the product — the *explanation* already exists, just not where the student needs it. `alpha/onboarding.html` step 4 (screenshot `19-onboarding.png`) states plainly: *"After a session, a short reflection closes the loop. It helps Kwalitec understand how the session felt and keeps tomorrow's guidance honest."* That sentence is shown once, days or weeks before the student ever reaches the actual Reflection screen, and never again.
- By contrast, `mission/session_recorded.html` (Study Session Feedback, screenshot `53-mission-session-recorded.png`) is a genuinely strong explainability pattern for a closely related moment ("What did Kwalitec observe? / What can Kwalitec honestly conclude? / What happens next?") — proving the product already knows how to write this kind of copy well. It simply has not been applied to the canonical Reflection screen itself.
- `KNOWN_LIMITATIONS.md` #9 independently confirms: *"No dedicated Reflection nav item... Reflection happens after finishing a session... and via Product Check-in."*

**Verdict:** Confirmed and current. This is a pure copy/content-placement gap, not an architecture problem — the fix is bringing the onboarding's own explanation (or the Study Session Feedback screen's proven tone) forward into the Reflection screen itself, at the moment it matters. See `COPY_REVIEW.md` §5 for a specific rewrite direction (documented only; not implemented under this analysis-only programme).

---

## 6. Lowest-rated categories — deeper read

| Category | Mean | What the code/screenshots show |
|---|---:|---|
| Reflection Workflow | 4.55 | See §5. |
| Navigation | 4.60 (σ 0.58 — tight agreement) | See §3. Low variance across 20 independent personas is notable — this is not a matter of a few reviewers disliking the IA; it is a broadly shared, structural perception. |
| Likelihood of Continued Use | 5.40 (σ 1.5 — most polarising) | Thematic analysis attributes the spread to persona context (exam urgency, existing tool stack, subject support) rather than a single fixable screen. `IMPROVEMENT_PRIORITY.md` explicitly separates this from a UI fix: *"Mature students will not abandon working stacks for an incomplete OS narrative"* (`COMPLETION_REPORT.md`, Lessons learned). This category is **not primarily a UI/UX defect** and this audit does not recommend treating it as one — it is a product-scope/subject-coverage question (only CS1/CM1/CB2 fully supported, per `KNOWN_LIMITATIONS.md` #4) more than a screen-design question. |

---

## 7. A fourth confirmed friction point beyond the mandatory three

PR-001's brief for this audit named three mandatory friction areas. One additional item recurs often enough in the same corpus, and is explicit enough in `IMPROVEMENT_PRIORITY.md`, that it should be recorded alongside them rather than left buried in the raw reviews.

**PR-001 evidence:** *"Richer Coach beyond restatement of the tip already shown"* is ranked **improvement priority #4** — one place above "visible adaptation after poor performance" and two above "exam-transfer linkage." At least six of the twenty reviews independently make the same point: *"Coach often restates the mission"* (REVIEW_05); *"Coach insight loses value after familiarity... repetitive Coach restatements once the tip is already explained"* (REVIEW_07); *"Coach rarely explains improvement mechanisms"* (REVIEW_11); *"Coach may not name the weak topic"* (REVIEW_12); *"Coach can look like a second brain without shared rules"* (REVIEW_14); *"I ignored Coach more than I expected once the tip rationale was visible... redundant Coach paraphrase when Trust L1 already explained the tip"* (REVIEW_15). REVIEW_01 separately notes an expectation mismatch: *"I expected Coach to be a nav destination; it is only a Home panel."*

**Code verification:** the Coach/"Coach insight" panel on `student/home.html` sits directly beside the Today's Mission card, which already carries a "why" explanation via `partials/educational_explainability.html`. No template-level mechanism separates what Coach says from what the Mission card's own explanation already says, which is consistent with reviewers experiencing it as paraphrase rather than new information.

**Verdict:** Confirmed and current, but ranked by PR-001 itself below the three mandatory friction points (#1, #2, #3 in `IMPROVEMENT_PRIORITY.md` are dual homes, duration consistency, and reflection value — Coach restatement is #4). Recorded here for completeness and carried into `HIGH_PRIORITY_BACKLOG.md` as a Tier 2 item; it should not be sequenced ahead of the three mandatory items.

---

## 8. What PR-001 explicitly said not to prioritise

`IMPROVEMENT_PRIORITY.md` states directly: *"What not to prioritise from this corpus alone: Visual polish unrelated to study blockers; new gamification (explicitly disliked / unmissed); claims of pass-rate improvement."*

This audit's own findings (`PREMIUM_UI_AUDIT.md`, `CONSISTENCY_AUDIT.md`) surface a number of genuine polish issues — off-palette error colours, icon-source discipline, numeric precision, card density asymmetry. **These are real and worth fixing, but PR-001's own students would not rank them above cohesion and trust.** `HIGH_PRIORITY_BACKLOG.md` reflects this explicitly with a two-tier structure: Tier 1 (cohesion/trust, directly traceable to PR-001's top three friction points) ranked above Tier 2 (premium polish, valuable but secondary per PR-001's own instruction).

---

## 9. Summary table

| PR-001 finding | Status today | Evidence | Residual for Stage 1 |
|---|---|---|---|
| Dual homes / navigation forks | Substantially mitigated in production config; not fully closed | `render.yaml` SOLE_RUNTIME=1; two dual-run CTAs already removed; EP-007.2 Tier B/Medium confidence, N=0 external | Naming collision ("Dashboard" ×2); confirm no non-production drift before/during pilot; raise confidence with real N>0 evidence |
| Inconsistent session durations/terminology | Open, confirmed with two-screenshot proof | `04-dashboard-student.png` (30 min) vs `09-mission.png` (90 min), same topic | Needs a single authoritative duration label even within the canonical stack alone |
| Reflection lacks perceived value | Open, confirmed, low-effort fix available | `reflection_card.html` bare of value framing; explanation already exists in `alpha/onboarding.html` step 4 and in `session_recorded.html`'s tone | Bring existing explanatory copy/tone forward into the Reflection screen itself |
| Navigation lowest category | Same root cause as dual homes | Mean 4.60, σ 0.58 (broad agreement) | Same as above |
| Likelihood of Continued Use most polarising | Largely a scope/coverage question, not a UI defect | Thematic analysis; subject-support gate | Out of scope for a UI/UX programme; owned by product/curriculum scope decisions |
| Coach restates the tip rather than adding insight (non-mandatory, #4 ranked) | Open, confirmed by 6+ reviews | REVIEW_05/07/11/12/14/15; `IMPROVEMENT_PRIORITY.md` #4 | Lower priority than the three mandatory items; Tier 2 in the backlog |
| Daily Mission / Commitment-Defer / Study Plan clarity | Confirmed strong, verified in code | Screenshots `09`, `28`, `30`; template review | Preserve as-is; use as reference pattern for other screens |
