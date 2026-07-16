# PTP-005 — Version 1 Cohesion

**Capability ID:** PTP-005  
**Programme:** Product Trust Programme  
**Programme ID:** PTP-000  
**Title:** Version 1 Cohesion  
**Priority:** P0  
**Status:** APPROVED — design only; awaiting Architecture Review  
**Version:** 1.0  
**Date:** 2026-07-16  
**Nature:** Product trust — Version 1 cohesion audit and fix specification. **Documentation only; no application code.**  
**Classification:** Product capability — subordinate to Educational Constitution, Educational Logic Registry, Evidence Authority, EIP, LXP, and PTP-000 through PTP-004.

---

## Scope reconciliation (read first)

`PTP-000` originally scoped **PTP-005** as *"Release Polish"* — version consistency,
terminology, and microcopy. Following **Blind Internal Alpha Review v3** (overall
**64 / 100**, recommendation **CONDITIONAL YES**), PTP-005 is **broadened and renamed
"Version 1 Cohesion."**

The reason is the v3 conclusion itself: the remaining issues are no longer
educational or architectural — they are **product cohesion** issues. Polish is a
subset of cohesion, so PTP-005 now covers the whole cohesion surface (version,
terminology, onboarding repetition, disclaimer fatigue, microcopy, visual
consistency, button wording, navigation friction, empty states, unexpected
behaviour). This supersedes the narrower "Release Polish" line item in
`PRODUCT_TRUST_PROGRAMME.md` §5 Capability 5.

**This capability adds no new functionality.** Its entire purpose is to make the
Version 1 that already exists *feel* like one product.

---

## Executive Summary

Version 1 is educationally lawful (EIP), has a complete honest daily loop (LXP),
gates unsupported subjects (PTP-001), has one daily workflow (PTP-002), speaks
honestly about evidence limits (PTP-003), and has a decluttered Dashboard
(PTP-004). What remains is that a student moving across surfaces still meets small
seams that make them pause and ask **"why is this different?"** — and for a product
whose entire brand is *trust*, every such pause is a withdrawal from the trust
account.

A full cohesion audit of the fourteen major Version 1 student surfaces found the
product does its **jobs** consistently but does not yet **name, label, or present**
them consistently. The three findings that genuinely damage trust are:

1. **The product contradicts itself about its own version** — Settings shows
   `1.0.0`, page footers show `v1.1`, the Internal Alpha panel shows `4.3`, and the
   authenticated app shows no version at all. A tool asking students to trust its
   numbers cannot disagree with itself about its own number.
2. **The central daily object has five names** — "Today's Mission," "Daily Mission,"
   "Study Session," "Today's Session," and eyebrow "Study Coach" all refer to the
   same thing, sometimes on the same screen. A student cannot tell whether Mission
   and Study Session are one feature or two.
3. **Onboarding asks the same question twice** — the Study Plan Wizard asks *"what
   have you already completed studying"* and the Educational History step asks it
   again, back to back. Being asked the same thing twice is the fastest way to make
   a student distrust that the product is listening.

Below these, a layer of High/Medium/Low issues (landing-page overpromise, disclaimer
fatigue, button-wording drift, nav-label vs heading mismatches, empty-state phrasing,
error-page divergence) each cost a small amount of coherence.

None of these require new features, algorithms, or educational redesign. Every fix is
a **wording, labelling, presentation, or de-duplication** change to surfaces that
already work. Delivered together, they convert a product that *works* honestly into
one that *feels* intentional.

---

## Version 1 Cohesion Principles

The Cohesion Principle from the brief — *every student-facing surface should feel like
it belongs to the same product; nothing should make the student pause and wonder "why
is this different?"* — decomposes into seven operating rules for Version 1.

### C-1 — One name per concept
Each product concept has exactly one student-facing name, used everywhere. The daily
study object, the readiness estimate, the coverage metric, and the practice-capture
step each get a single canonical noun. Internal/engineering names may differ; the
student never sees two.

### C-2 — One version, one voice
The product presents a single version identity, in one place, sourced from one value.
Version strings never disagree across Settings, footers, and status panels.

### C-3 — Ask once
No onboarding question is asked twice. If two steps need the same information, they
share it; they do not re-request it with different wording.

### C-4 — Honest, not repetitive
Educational honesty (Constitution / PTP-003) is preserved, but each caveat is stated
**where the decision is made**, not repeated on every surface. Truth once, clearly,
beats truth five times, wearily.

### C-5 — The same action uses the same words
A button that begins today's study says the same thing on every surface. "Start," "Back
to," "Create," and "Record" verb families are used consistently.

### C-6 — The label matches the destination
A navigation item, browser title, and the page heading it leads to agree. A student
who clicks "Analytics" should not arrive at a page titled "Insights."

### C-7 — Every surface wears the same skin
Authenticated, unauthenticated, and error surfaces share layout, theme (including dark
mode), footer, typography, and title format. No surface should feel like a different
application.

These principles are subordinate to higher educational authority: where truth and
brevity conflict, **truth wins** and the caveat stays (C-4 trims repetition, never
honesty).

---

## Version 1 Cohesion Audit — Findings

All findings are evidenced with `file:line`. Surfaces audited: Landing/Authentication
(`auth/login.html`, `layouts/auth_base.html`), Onboarding
(`calibration/alpha.html`, `partials/welcome_modal.html`), Study Plan Wizard
(`study_plan/wizard_*`), Study Plan (`study_plan/list|view|edit.html`), Dashboard
(`dashboard/index.html`), Today's Mission (`mission/index.html`), Study Session
(`mission/session.html`), Practice Outcome Capture
(`mission/session_practice_outcome.html`), Study Session Feedback
(`mission/session_recorded.html`), the retired review
(`mission/review.html`, `mission/session_review.html`), Analytics
(`analytics/index.html`), Recommendations (Dashboard cards), Settings
(`settings/index.html`), Error pages (`errors/403|404|500.html`), Navigation
(`partials/sidebar.html`, `topnav.html`).

---

### F-1 — Version identity contradicts itself (Critical)

The product displays **three different version numbers and one absence**:

| Surface | Value | Evidence |
|---------|-------|----------|
| Settings → General → "Version" | `1.0.0` (hardcoded) | `settings/index.html:55` |
| Settings → Internal Alpha → "Application version" | `1.0.0` (dynamic) | `settings/index.html:244`, `internal_alpha_status_service.py:21` |
| Settings → Internal Alpha → "Internal Alpha version" | `4.3` | `settings/index.html:236`, `internal_alpha_status_service.py:22` |
| Auth + error page footers | `Kwalitec v1.1` | `auth_base.html:34`, `errors/403.html:26`, `404.html:26`, `500.html:26` |
| Authenticated app shell (base/sidebar/topnav) | *(no version shown)* | `layouts/base.html` (no footer), `partials/sidebar.html`, `topnav.html` |
| `pyproject.toml` | `1.0.0` | `pyproject.toml:3` |

The same conceptual field ("Version") is hardcoded in one place (`settings/index.html:55`)
and data-bound in another (`:244`). Both blind reviews flagged this explicitly as a
trust signal: *"for a product whose entire brand is 'trust my numbers,' I still noticed"*
(Review v2). This is the clearest possible self-contradiction and is classified Critical
despite being trivially cheap to fix.

---

### F-2 — The daily study object has five names (Critical)

The single most-used object in the product is named inconsistently, sometimes on one
screen:

| Name | Evidence |
|------|----------|
| "Today's Mission" | `dashboard/index.html:81` ("Open Today's Mission") |
| "Daily Mission" (page H1 + title) | `mission/index.html:6`, `mission/routes.py:190` |
| "Today's Study Session" (card title) | `dashboard/index.html:41` |
| "Today's Session" (CTAs) | `dashboard/index.html:71,73` ("Review/Start Today's Session") |
| "Study Session" (eyebrow + title) | `mission/session.html:5`, `mission/routes.py:271` |
| "Study Coach" (mission eyebrow) | `mission/index.html:5` |

On the Dashboard alone, one card is titled **"Today's Study Session"** but its buttons
say **"Resume Mission"** (`:69`), **"Start Today's Session"** (`:73`), and **"Open
Today's Mission"** (`:81`). The sidebar calls it **"Mission"** (`sidebar.html:19`); the
page it opens is headed **"Daily Mission"** under an eyebrow **"Study Coach."** A student
cannot tell whether "Mission" and "Study Session" are the same feature or two. This is a
core-navigation trust break and is classified Critical.

---

### F-3 — Onboarding asks the same thing twice (High)

Two consecutive onboarding steps request the student's prior study coverage with
different titles and framing:

| Step | Heading | Ask | Evidence |
|------|---------|-----|----------|
| Study Plan Wizard step 4 | "Where are you currently?" | "Tell us what you have already completed studying" (tick topics done) | `wizard_step_4.html:3-4` |
| Educational History | "Where are you starting from?" | "Tell us your educational history … declarations, not measured mastery" (tick sections covered) | `calibration/alpha.html:6-7` |

Both reviews called this out as the fastest way to erode trust that the tool is
listening (Review v1: *"Being asked the same thing twice, back to back, is the fastest
way to make me distrust that the tool is actually listening."*). Two parallel
questionnaires also have different submit CTAs ("Next" vs "Create my study profile").
Classified High (borderline Critical; contained only because the loop still functions).

---

### F-4 — Landing page overpromises versus delivered product (High)

The landing/auth surface advertises capabilities the authenticated product either
disclaims or does not name the same way:

| Landing claim | Reality on delivered surface | Evidence |
|---------------|------------------------------|----------|
| "Burnout Monitoring" | Dashboard: "not a prediction of burnout or exam outcome" | `login.html:55` vs `dashboard/index.html:220` |
| "Adaptive Learning" / "Intelligent Study Planning" | Learning Mode is explicitly sequential; wizard limits to supported papers only | `login.html:31,37` vs `mission/index.html:111`, `wizard_step_1.html:4` |
| "Estimated readiness insights" / "exam readiness analytics" | Analytics page H1 is "Insights" | `login.html:49`, `auth_base.html:6` vs `analytics/index.html:6` |
| Product identity: "Intelligent Exam Preparation" | Elsewhere: "disciplined learning system" / "Disciplined exam preparation." | `login.html:17` vs `base.html:6`, `sidebar.html:4` |

Review v1: *"the first impression slightly oversells what's behind the door."* The
product's own positioning (`PRODUCT_TRUST_PROGRAMME.md` §8.3) is "adaptive study planner
and honest practice tracker — not readiness oracle," which the landing page contradicts.
Classified High.

---

### F-5 — Two competing product identities / taglines (High)

The product describes itself two incompatible ways depending on surface:

- **"Intelligent" family:** "Intelligent Exam Preparation" (`login.html:17`),
  "intelligent exam preparation" (`auth_base.html:6`), "Intelligent Study Planning"
  (`login.html:37`).
- **"Disciplined" family:** "disciplined learning system" (`base.html:6`,
  `settings/index.html:70`), "Disciplined exam preparation." (`sidebar.html:4`),
  "Discipline over motivation." (`settings/index.html:71`).

These are two different brand promises (cleverness vs discipline) shown to the same
student minutes apart. Classified High (brand cohesion).

---

### F-6 — Disclaimer / hedging fatigue (High)

Educational honesty caveats are correct but repeated to the point of fatigue, in
near-duplicate wording, across nearly every surface. Representative clusters:

- *"…not Estimated Knowledge"* — `wizard_step_4.html:4`, `dashboard/index.html:144`
- *"completing … alone is not understanding"* — `dashboard/index.html:198`
  ("completing studying alone"), `analytics/index.html:177` ("completing a topic alone")
  — **same idea, two wordings**
- *"not independently verified exam performance"* / *"not a verified exam score"* —
  `dashboard/index.html:180`, `analytics/index.html:74`, `analytics/index.html:100`
- *"Based on your recorded practice outcomes."* — repeated at
  `dashboard/index.html:180`, `analytics/index.html:85`, `study_plan/view.html:146,207`,
  plus six `title=` badge tooltips across Dashboard and Analytics
- *"not … mastery"* — `session_review.html:8`, `session_practice_outcome.html:10`,
  `calibration/alpha.html:7,43`

Both reviews flagged this ("*I'm being read a disclaimer on every screen … exhausting*").
The fix is C-4 (state each caveat where the decision is made; unify wording; remove
duplicates) — **not** removing honesty. Classified High.

---

### F-7 — Navigation label ≠ destination heading/title (Medium)

| Sidebar / nav label | Destination heading / browser title | Evidence |
|---------------------|--------------------------------------|----------|
| "Analytics" | H1 "Insights"; title "Analytics · Kwalitec" | `sidebar.html:26` vs `analytics/index.html:6`, `analytics/routes.py:66` |
| "Mission" | H1 "Daily Mission"; eyebrow "Study Coach" | `sidebar.html:19` vs `mission/index.html:5-6` |
| "Study Plan" | H1 "Study Plans" (list) or exam name (view) | `sidebar.html:15` vs `study_plan/list.html:8`, `study_plan/view.html:9` |
| "Internal Alpha" (settings sub-nav) | H1 remains "Settings" | `settings/index.html:39` vs `:8` |

A label that does not match where it lands creates low-grade "am I in the right place?"
friction on every navigation. Classified Medium.

---

### F-8 — Button / CTA wording drift (Medium)

The same action is worded differently by surface:

| Action | Variants | Evidence |
|--------|----------|----------|
| Begin today's study | "Start Today's Session" / "Start Study Session" / "Start Studying" | `dashboard/index.html:73`, `mission/index.html:160`, `welcome_modal.html:15` |
| Resume in-progress study | "Resume Mission" / "Resume Study Session" | `dashboard/index.html:69`, `mission/index.html:151` |
| Return to mission page | "Back to Today's Mission" / "Back to Daily Mission" | `mission/session.html:100`, `session_recorded.html:62` |
| Return home | "Return to Dashboard" / "Back to Dashboard" | `session_recorded.html:59`, `study_plan/view.html:258` |
| Create a plan | "Create Study Plan" / "+ Create New Plan" | (many) vs `study_plan/list.html:11` |
| Submit capture | "Record Study Session" / "Record Practice Results" | `session_review.html:56`, `session_practice_outcome.html:83` |

Classified Medium.

---

### F-9 — Readiness terminology split: "Estimated Knowledge" vs "Estimated readiness" (Medium)

Two closely related student-facing terms coexist without a stated relationship, plus
casing inconsistency:

- "Estimated Knowledge" — `dashboard/index.html:166`, `analytics/index.html:84`,
  `study_plan/view.html:144`
- "Estimated readiness" — `login.html:49`, `analytics/index.html:22,73`
- Case drift: "Estimated Knowledge" vs "Estimated knowledge" —
  `dashboard/index.html:166` vs `analytics/index.html:177`

A student sees two terms and cannot tell if they are the same thing. Whether they
*should* be merged is partly an educational-model question (see V2-1); the **casing and
label consistency** within Version 1 is in scope. Classified Medium.

---

### F-10 — Empty-state phrasing is inconsistent (Medium)

Empty states are honest but phrased many ways for the same situation:

- "…will appear here once available" (`dashboard/index.html:80`) vs "…appears here after
  practice results are recorded" (`analytics/index.html:177`) vs "No Missions Yet"
  (`mission/index.html:213`) vs "Not available yet" (`study_plan/view.html:153,214`) vs
  bare "—" (`analytics/index.html:18`, `mission/index.html:65,83`).
- "Create your first study plan to …" has four different tails
  (`dashboard/index.html:149,390`, `study_plan/list.html:94`, `mission/index.html:222`).

Classified Medium.

---

### F-11 — Retired reflection flow still present (Medium)

`mission/review.html` ("Reflect on Your Learning," confidence-before/after, mistakes)
is marked retired at `review.html:1-2` and routes redirect (`mission/routes.py:506-520`),
but the template and its distinct vocabulary still exist in the tree. PTP-002 consolidated
the live path; PTP-005 should confirm the dead surface is fully removed or clearly
quarantined so it can never re-enter the student journey or confuse future edits.
Classified Medium.

---

### F-12 — Error pages feel like a different application (Low)

`errors/403|404|500.html` are standalone documents that do **not** extend either base
layout. Consequences (`errors/403.html:7-8`, `404.html`, `500.html`):

- No `theme.js` → **no dark mode**; a dark-mode user hits a white error page.
- No appearance switcher, no `app.js`, no CSRF meta.
- Title separator is em dash — "Page Not Found — Kwalitec" (`404.html:6`) — vs the
  middle-dot "· Kwalitec" used everywhere else.
- Footer shows `v1.1` (feeds F-1).

Classified Low.

---

### F-13 — Browser title format and coverage inconsistency (Low)

- Study Plan pages pass no `title`, so the browser tab reads bare "Kwalitec"
  (`study_plan/routes.py:993,1001,1065`), while every other surface reads "{Page} ·
  Kwalitec".
- Error pages use "—" instead of "·".
- Meta descriptions differ between layouts: "Kwalitec disciplined learning system."
  (`base.html:6`) vs "intelligent exam preparation…" (`auth_base.html:6`) — feeds F-5.

Classified Low.

---

### F-14 — Unexpected behaviour: "Study Plan" nav does not open a "Study Plan" (Low)

Clicking sidebar "Study Plan" (`sidebar.html:15`) redirects to either the active plan
view (titled by exam name) or the wizard (`study_plan/routes.py:164-169`) — never a page
called "Study Plan." Not broken, but mildly surprising. Classified Low.

---

## Cohesion Matrix

| ID | Finding | Surfaces | Cohesion principle | Classification | Trust impact |
|----|---------|----------|--------------------|----------------|--------------|
| F-1 | Version identity contradicts itself (`1.0.0` / `v1.1` / `4.3` / none) | Settings, footers, error pages, app shell | C-2 | **Critical** | Product disagrees with itself about its own number — direct hit on a trust brand |
| F-2 | Daily object has five names (Mission/Session/Study Coach) | Dashboard, Mission, Study Session, sidebar | C-1 | **Critical** | Student cannot tell one feature from two |
| F-3 | Onboarding asks prior coverage twice | Wizard step 4, Educational History | C-3 | **High** | "Is it even listening?" |
| F-4 | Landing overpromises vs delivered product | Landing, Dashboard, Analytics | C-1 | **High** | First-impression overselling |
| F-5 | Two product identities ("intelligent" vs "disciplined") | Landing, sidebar, Settings, meta | C-1 | **High** | Confused brand promise |
| F-6 | Disclaimer / hedging fatigue | All educational surfaces | C-4 | **High** | Honest but exhausting; patronising tone |
| F-7 | Nav label ≠ destination heading/title | Sidebar, Analytics, Mission, Study Plan, Settings | C-6 | **Medium** | "Am I in the right place?" |
| F-8 | Button / CTA wording drift | Dashboard, Mission, Study Plan, session flow | C-5 | **Medium** | Low-grade inconsistency |
| F-9 | "Estimated Knowledge" vs "Estimated readiness" + casing | Landing, Dashboard, Analytics, Study Plan | C-1 | **Medium** | Two terms, one concept |
| F-10 | Empty-state phrasing inconsistent | Dashboard, Mission, Analytics, Study Plan | C-1 | **Medium** | Uneven polish |
| F-11 | Retired "Reflect on Your Learning" surface still present | mission/review.html | C-1 | **Medium** | Latent re-confusion risk |
| F-12 | Error pages diverge (no dark mode, own layout) | 403/404/500 | C-7 | **Low** | Feels like another app |
| F-13 | Browser title format / coverage inconsistency | Study Plan pages, error pages, meta | C-6 | **Low** | Minor |
| F-14 | "Study Plan" nav opens a non-"Study Plan" page | Sidebar → Study Plan routing | C-6 | **Low** | Mild surprise |

**Critical count: 2** (F-1, F-2) — each a genuine self-contradiction a serious student
will notice and cannot un-see.

---

## Recommended Fixes

All fixes are wording/labelling/presentation/de-duplication only. **No algorithms,
educational states, evidence rules, curriculum, readiness maths, or new features are
touched.** Educational caveats are preserved (C-4 trims repetition, never truth).

| ID | Recommended fix | Type |
|----|-----------------|------|
| F-1 | Define **one** version source of truth (`APP_VERSION`) and render it everywhere version is shown. Remove the hardcoded `1.0.0` in `settings/index.html:55`; make footers and Settings read the same value; decide whether the authenticated shell should show a version footer at all (recommended: yes, one small footer via `base.html`). Keep "Internal Alpha version" as a **distinct, clearly-labelled** internal build track, not a competing product version. | Wording / template binding |
| F-2 | Choose **one** canonical student noun for the daily object. Recommended: **"Study Session"** for the activity (matches LXP + PTP-004 Dashboard card) with **"Today's Study Session"** as the daily instance; retire "Mission"/"Daily Mission"/"Today's Mission"/"Study Coach" from student-facing copy, or keep "Mission" **only** as the sidebar section name if it maps 1:1 and consistently. Align Dashboard card title, all CTAs, sidebar, page H1, eyebrow, and browser title to the single name. | Terminology |
| F-3 | Merge or link the two coverage questions so the student declares prior coverage **once**. If both steps must remain, the second reads back the first ("You told us you've completed X — confirm or adjust") rather than re-asking. Unify the two submit CTAs. | Flow de-duplication |
| F-4 | Align the landing feature list with what Version 1 actually delivers and how the product positions itself (PTP-000 §8.3): present "adaptive study planner and honest practice tracker," soften/relabel "Burnout Monitoring," and match "Analytics/Insights" naming to the destination. | Copy |
| F-5 | Pick one product identity line and use it in landing H1, meta descriptions (both layouts), sidebar tagline, and Settings "About." Recommended: settle the "intelligent vs disciplined" tension into one sentence. | Brand copy |
| F-6 | Deduplicate caveats: one canonical phrasing per idea ("not verified exam performance," "practice you record," "not mastery"), shown at the decision point, not repeated on every card/tooltip. Remove near-duplicate variants (e.g. unify "completing studying alone" / "completing a topic alone"). Keep the four-part Feedback honesty intact. | Microcopy |
| F-7 | Make each nav label equal its destination heading and browser title (e.g. Analytics H1 → "Analytics," or rename nav to "Insights" — choose one; align "Mission"/"Study Session" per F-2). | Labelling |
| F-8 | Standardise verb families: one "Start …", one "Resume …", one "Back to …", one "Create Study Plan," one capture-submit label per PTP-002 path. | Button copy |
| F-9 | Standardise casing to "Estimated Knowledge"; within Version 1 keep "Estimated readiness" only where it is a genuinely distinct concept, and state the relationship once. (Full merge is V2-1.) | Terminology / casing |
| F-10 | Adopt one empty-state pattern: `{Heading} · {one-line reason} · {single primary CTA}`; unify the "Create your first study plan …" tails; replace bare "—" with a short consistent placeholder where a label is expected. | Microcopy |
| F-11 | Fully remove (or hard-quarantine) `mission/review.html` and its vocabulary now that PTP-002 owns the single path; confirm no route can reach it. | Cleanup |
| F-12 | Make error pages extend the shared base (theme.js/dark mode, appearance switcher, "·" title separator, one footer version). | Template |
| F-13 | Pass a `title` on Study Plan routes; standardise the "· Kwalitec" separator everywhere; align meta descriptions with F-5. | Template / route |
| F-14 | Either title the Study Plan landing page "Study Plan," or rename the nav item to match where it lands. | Labelling |

---

## Implementation Order

Ordered so that decisions (canonical names) are made before they are applied, and so
that trust-damaging items land first. All steps remain design→implementation subject to
Architecture Review; PTP-005 itself ships **no code**.

```
Phase 0 — Decide the vocabulary (design)
  0a. Ratify one canonical name for the daily object (F-2)
  0b. Ratify one version source of truth (F-1)
  0c. Ratify one product identity line (F-4, F-5)
  0d. Ratify canonical caveat phrasings (F-6) — with educational sign-off

Phase 1 — Critical (self-contradiction; land first)
  1. F-1  One version everywhere
  2. F-2  One daily-object name everywhere

Phase 2 — High (trust-eroding friction)
  3. F-3  Ask prior coverage once
  4. F-4  Honest landing feature list
  5. F-5  One product identity
  6. F-6  Deduplicate disclaimers (truth preserved)

Phase 3 — Medium (coherence polish)
  7. F-7  Nav label = destination
  8. F-8  Consistent button verbs
  9. F-9  Readiness term + casing
 10. F-10 Consistent empty states
 11. F-11 Remove retired review surface

Phase 4 — Low (finishing pass)
 12. F-12 Error pages share the skin
 13. F-13 Title format + Study Plan titles
 14. F-14 Study Plan nav/label agreement
```

Rationale: Phase 0 prevents locking wording twice. Phase 1 removes the two genuine
self-contradictions a student cannot un-see. Phases 2–4 descend by trust impact.

---

## Success Criteria

Version 1 Cohesion succeeds when a blind reviewer moving across all fourteen surfaces
never pauses to ask "why is this different?" Concretely:

| Signal | Threshold |
|--------|-----------|
| Version identity | Exactly one product version value is shown to students, from one source; no surface disagrees (F-1 closed) |
| Daily-object name | The daily study object has one student-facing name across Dashboard, Mission, Study Session, sidebar, titles (F-2 closed) |
| Onboarding | No question is asked twice; prior coverage is declared once (F-3 closed) |
| Positioning | Landing claims match delivered Version 1 and the approved "planner + honest tracker" positioning (F-4, F-5 closed) |
| Disclaimer load | Each educational caveat appears in one canonical wording at its decision point; no near-duplicate repetition — **honesty unchanged** (F-6 closed) |
| Navigation | Every nav label equals its destination heading and browser title (F-7, F-13, F-14 closed) |
| Buttons | One verb per action across surfaces (F-8 closed) |
| Terminology & empty states | One term per concept, consistent casing, one empty-state pattern (F-9, F-10 closed) |
| Skin | Authenticated, unauthenticated, and error surfaces share layout, dark mode, footer, and title format (F-11, F-12 closed) |
| Educational non-regression | EIP state ownership, Evidence Authority, LXP feedback honesty, PTP-001–004 outcomes all preserved |
| Blind Review v3 → v-next | Cohesion is no longer cited as a residual reason to withhold dependence |

Success is explicitly **not** new features, content, question banks, or any change to
educational meaning — only that the existing Version 1 reads as **one coherent,
intentional, trustworthy product**.

---

## Out of Scope (preserved, not redesigned)

Educational Constitution · Educational Logic Registry · Evidence Authority · Digital
Twin · Educational Intelligence · Readiness algorithms · Recommendation algorithms ·
Question banks / in-app content · Adaptive Learning surfaces · Revision Mode · the
Learning Experience daily loop · PTP-001 subject gating · PTP-002 single workflow ·
PTP-003 evidence speech · PTP-004 Dashboard information architecture.

PTP-005 changes how these are **named and presented**, never what they **mean or
compute**.

---

## Version 2 (deferred, not Version 1 cohesion)

| ID | Item | Why deferred |
|----|------|--------------|
| V2-1 | Decide whether "Estimated Knowledge" and "Estimated readiness" should merge into one readiness vocabulary | Touches the educational model / Evidence Authority — needs a constitutional decision, not a wording pass |
| V2-2 | Full onboarding redesign (single unified profile flow replacing Wizard + Educational History) | Larger UX/architecture change beyond cohesion de-duplication |
| V2-3 | In-app study/practice content so evidence is not purely self-reported | Explicitly out of the Product Trust Programme (PTP-000 §7.2) |
| V2-4 | Verified performance capture | Out of programme; readiness-model scope |

---

## Cross References

| Document | Relationship |
|----------|--------------|
| `knowledge/product/PRODUCT_TRUST_PROGRAMME.md` | Parent programme; PTP-005 broadens its "Release Polish" line into "Version 1 Cohesion" |
| `knowledge/product/PTP-001_SUPPORTED_SUBJECT_INTEGRITY.md` | Subject gating preserved; cohesion aligns supported-subject wording |
| `knowledge/product/PTP-002_SINGLE_SOURCE_OF_TRUTH.md` | Single daily workflow; F-8/F-11 respect its one path |
| `knowledge/product/PRODUCT_COMMUNICATION_STANDARD.md` (PTP-003) | Canonical caveat wording for F-6 must obey this standard |
| `knowledge/product/PTP-004_INFORMATION_ARCHITECTURE.md` | Dashboard IA preserved; PTP-004 §4 "PTP-005 may trim disclaimer fatigue" is realised here (F-6) |
| `BLIND_INTERNAL_ALPHA_REVIEW.md`, `BLIND_INTERNAL_ALPHA_REVIEW_V2.md` | Product evidence for version, disclaimer, onboarding, terminology findings |
| Blind Internal Alpha Review v3 (64/100, CONDITIONAL YES) | Triggering evidence: remaining issues are cohesion, not educational/architectural |
| `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Higher authority; honesty preserved under C-4 |

---

**End of PTP-005 Version 1 Cohesion.**  
**Design only — no application code changed.**  
**Stop. Return for Architecture Review.**
