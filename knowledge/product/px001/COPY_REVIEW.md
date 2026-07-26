# PX-001 — Copy Review

**Status:** Analysis only. No copy changed in the application. Suggested alternatives below are recommendations for a future implementation pass, not applied edits.

**Method:** Every string quoted below was read directly from the live template or Python source cited, not paraphrased from a screenshot alone (screenshots are cited as visual corroboration where available).

---

## 1. Repeated branding

| Location | Evidence | Issue | Suggested direction |
|---|---|---|---|
| Sign in, left panel | `auth/login.html` lines 8–16: logo lockup (icon + wordmark "Kwalitec") immediately followed by `<p class="landing-brand-name">{{ product_name }}</p>` rendering "Kwalitec" again as a headline | The wordmark already says the name; repeating it as a second headline is redundant, not reinforcing | Keep the lockup as the single brand moment; promote the descriptor/value-prop directly to headline weight without a second "Kwalitec" line |
| Sign in, onboarding note | `auth/login.html` lines 108–119: "Kwalitec is invite-only... Sign in with the credentials provided by your **Kwalitec coordinator**... Don't have your details, or need a reset? Contact your **Kwalitec coordinator**." | "Kwalitec coordinator" repeated twice in two consecutive short paragraphs | State it once: "...provided by your coordinator. Missing your details or need a reset? Contact them directly." |
| Sign in, footer | `layouts/auth_base.html` footer includes `app_footer.html`, which (per screenshot `01-login.png`) reads "Kwalitec v2.0.0 · Internal Alpha · Founding Cohort · Build RC2" | Combined with the two "Kwalitec" mentions above, the word "Kwalitec" appears **4 times** on one unauthenticated screen | Not a hard rule violation, but worth counting against §5's "premium quality check" — a calmer screen says the name once with confidence |
| "Education Operating System" descriptor | `app/brand_identity.py` line 26: `PRODUCT_DESCRIPTOR = "Education Operating System"`, pinned by `tests/test_px001_brand_identity.py`. Rendered on Sign in (`01-login.png`), meta description tag (`layouts/base.html`/`auth_base.html` line 6), and Onboarding step 1 (`19-onboarding.png`: *"Kwalitec is an Education Operating System for demanding exams."*) | Deliberately codified brand language (not an accidental leak), but "Operating System" is an engineering/systems metaphor a non-technical exam student has no reason to parse as a benefit. It works against the very next line it always sits beside — "Know exactly what to study next" — which *is* a clear benefit statement | Because this is a single Python constant reused everywhere, it is a **one-line, sitewide fix** if revised. Consider testing outcome-led alternatives (e.g. "Your calm path to exam readiness") against the existing value proposition rather than a systems metaphor. Flagged for product/brand decision, not unilaterally rewritten here. |

---

## 2. Technical wording exposed to students

This is the most severe copy category in the audit — internal/operational language shown directly to students with no filtering for audience.

| Location | Evidence | Why it hurts |
|---|---|---|
| Settings → General | `settings/index.html` lines 56–93: labels "Version," "Build date," "Environment," "Build number," and conditionally `<code>{{ release_info.commit }}</code>` (a raw git commit hash), plus a raw numeric "User ID" (`current_user.id`) | A student has no use for a commit hash or a raw environment string ("development"/"production"). This is release-engineering telemetry, not account information, and it is the *first* section of the *first* Settings page a student opens. |
| Settings → Internal Alpha | `settings/index.html` lines 296–353: "Internal Alpha enablement: Enabled/Disabled," "Current curriculum," "Learning profile status: `{{ alpha_status.twin_status }}`" | "Learning profile status" is a user-facing label wrapped around an internal engine name ("twin") the student has never been introduced to. The value shown is an internal state enum, not a sentence a student would write themselves. |
| Sign-in / Onboarding | See §1 — "Education Operating System" | Systems-metaphor branding language, addressed above. |
| Help & Support | `alpha/help.html` "Release information" table: Application version, Build date, Environment, Build number, Build label, Support contact | Reasonable to keep *some* of this for an Internal Alpha support contact flow, but it currently **is** the entire Help screen — there is no actual help content beside it (see `PREMIUM_UI_AUDIT.md` §6). |

**Suggested direction:** move build/commit/environment metadata behind a single "Diagnostic information" disclosure (collapsed by default, useful only when a student is asked for it by support) rather than presenting it as primary settings content. Rename "Learning profile status" to something a student would recognise, or remove it from the student-facing surface entirely if it has no actionable meaning for them.

---

## 3. Repeated defensive/hedging pattern

Several screens explain, in very similar language, what a number **is not**:

| Location | Quote |
|---|---|
| Dashboard (legacy) | "This is Learning Progress from Study Progress — not Estimated Knowledge." (`03-dashboard-legacy.png`) |
| Dashboard (legacy) | "Estimated knowledge appears here after practice results are recorded — completing a topic alone is not understanding." |
| Practice Outcome Capture | "These results reflect the answers you recorded after today's study session... **This is not Estimated Knowledge.**" (`34-mission-practice-outcome.png`) |
| Analytics | "No topics started yet — coverage and practice history are empty. Estimated readiness uses syllabus coverage, Estimated Knowledge from recorded practice, and recent review habits." |

**Assessment:** the underlying intent — being honest that "topic marked done" ≠ "concept mastered" — is exactly right and matches the product's Runtime A explainability philosophy (`RUNTIME_API_MODEL.md`) and governance expectations around not overclaiming educational confidence. The *execution* repeats a near-identical caveat sentence on multiple independent screens, which reads as anxious over-explaining rather than calm confidence when encountered three or four times in one session. **Suggested direction:** define this distinction once, prominently, in one place a student can always find (e.g., a single "How we measure progress" explainer linked consistently), and let individual cards use a short label ("Estimated," "Recorded") rather than re-deriving the full caveat sentence each time.

---

## 4. Duplicate / repeated instructions at scale

| Location | Evidence | Issue |
|---|---|---|
| Study Plan roadmap | `study_plan/view.html` rendering, screenshot `30-study-plan-view.png`: "Learning Outcomes Not available yet" appears identically on **all 14** topic cards in the visible roadmap | At small scale this is a fine per-item note; at 14 repeats in one screen it reads as broken/incomplete content rather than one honest disclaimer. |
| Appearance switcher | Present, in near-identical triplicated button form (Light/Dark/System), independently on: public auth layout footer (`auth_base.html` lines 26–37), authenticated top nav (`topnav.html` lines 18–53), Settings → Preferences (`settings/index.html` lines 193–209, plus a *second*, redundant `<select>` dropdown for the same three values immediately below it), and Settings → Internal Alpha (lines 302–312) | This is a legitimate global control repeated in its natural places (nav + settings), which is reasonable — but Settings → Preferences renders **the same three-way choice twice in two different control types** (button group, then a `<select>`) on one screen, which is a direct, single-screen duplication with no clear reason for a student to prefer one over the other. |

**Suggested direction:** for the roadmap, replace the 14 repeated captions with a single top-of-roadmap note ("Learning outcomes will appear here as they become available") and drop the per-card repetition. For Preferences, remove the redundant `<select>` and keep only the button group (or vice versa), not both.

---

## 5. The Reflection screen — no value framing (PR-001's #3 friction, verbatim gap)

Current copy, `session/components/reflection_card.html`:

> **Reflection**
> [Key insight] / [Concept confidence] / [Suggested improvement] — if present
> **Reflection prompt** — {{ reflection.reflection_prompt }}
> [Optional note field] → **Continue**

Nowhere on this screen does the product say why this step exists. Compare with copy that already exists elsewhere in the product for adjacent moments:

- `alpha/onboarding.html`, Step 4: *"After a session, a short reflection closes the loop. It helps Kwalitec understand how the session felt and keeps tomorrow's guidance honest."*
- `mission/session_recorded.html` (Study Session Feedback): *"What did Kwalitec observe? / What can Kwalitec honestly conclude? / What happens next?"* — shown even for an incomplete session, with total honesty ("Nothing from today changes your practice-based guidance").
- `student/home.html` line 240, in the canonical reflection-active state: *"Reflection is optional and stays with you — nothing is saved yet."* — this line already exists in the canonical Home's reflection block but has no equivalent in the Session Experience's `reflection_card.html`.

**Suggested direction (documented only, not implemented under this analysis-only programme):** add one short line to `reflection_card.html`, reusing language and tone already proven elsewhere in the product (the onboarding promise or the Study Session Feedback pattern), stating what the reflection is for and what happens to it — e.g., something in the register of "This note helps tune tomorrow's mission — it's short, and it's just for the record." Do not invent new claims about personalization that the current engine does not make (see `knowledge/GOVERNANCE.md` explainability constraints) — reuse exactly the honesty level already present in the Study Session Feedback screen.

---

## 6. Numeric false precision

| Location | Evidence |
|---|---|
| Dashboard "Time Status" | "Remaining Study Hours: **199.98**" (`03-dashboard-legacy.png`) |
| Study Plan roadmap | Per-topic estimates: "11.4h," "8.8h," "7.3h," "3.6h," "20.0h," "40.0h," "30.0h" (`30-study-plan-view.png`) |

Two-decimal precision on a modelled estimate ("199.98 hours") implies a level of certainty the underlying calculation does not actually have, and reads as a raw floating-point value rather than a considered display choice. **Suggested direction:** round remaining-hours and per-topic estimates to sensible increments (whole hours, or "~12 hrs") consistent with how the "200 Days Remaining" exam countdown is already displayed as a clean integer on the same card.

---

## 7. What is already working well (do not rewrite)

To keep this review balanced and actionable, three copy patterns are strong and should be treated as house style to extend, not replace:

1. **Study Session Feedback** (`mission/session_recorded.html`) — "What happened today? / What did Kwalitec observe? / What can Kwalitec honestly conclude? / What happens next?" is calm, structured, and honest even in a failure/incomplete state.
2. **Onboarding** (`alpha/onboarding.html`) — four short, jargon-light steps (aside from the one "Education Operating System" repetition noted in §1) that explain explainability and reflection in plain language.
3. **Today's Study Session briefing** (`mission/index.html`) — "Why you are studying this" / "What success looks like today" / "Recommended activities" is a genuinely good instructional pattern: concrete, scoped, and non-repetitive.

Any future copy pass should extend the voice of these three screens outward to Reflection, Settings, and Help, rather than introducing a new voice.
