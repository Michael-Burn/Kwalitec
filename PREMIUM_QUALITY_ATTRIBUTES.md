# Premium Quality Attributes

**Programme:** PX-001 — Premium Experience  
**Preparation:** PX-000 — Premium Experience Preparation  
**Status:** Binding quality bar for post-gate PX waves — **not a current product claim**  
**Effective:** 2026-08-02  
**Authority:** `PX001_PROGRAMME_CHARTER.md` · `PREMIUM_EXPERIENCE_ROADMAP.md`  
**Baselines to consume (not overwrite):** `knowledge/release/RP-001/PREMIUM_QUALITY_SCORECARD.md` · historical `knowledge/product/px001/` · `knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md`  

---

## 1. Purpose

Define what “premium” means for Kwalitec after Version 1 educational completion — as auditable attributes across the ten focus areas — so implementation and certification share one bar.

These attributes govern **experience craft**. They do not redefine educational excellence, coverage, or recommendation quality.

---

## 2. Scoring method

| Score | Meaning |
|-------|---------|
| **Exemplary (5)** | Distinctive restraint; would serve as house reference for other surfaces |
| **Target (4)** | Strong premium — minor residuals only; wave exit default |
| **Adequate (3)** | Usable; disclosed debt allowed only with Founder waiver |
| **Weak (2)** | Noticeably dilutes premium perception or trust |
| **Failing (1)** | Would reject a premium claim on that attribute |

**Wave exits** require **Target (4)+** on in-scope attributes unless a written waiver names the residual and owner.

Scores are audit judgements from live sole-runtime student surfaces plus Founder dogfood — not marketing aspiration.

---

## 3. Cross-cutting invariants

Every focus area is judged against these invariants:

| ID | Invariant |
|----|-----------|
| **I-1 Honesty** | Copy and chrome never invent readiness, coverage, or pass likelihood |
| **I-2 Calm** | Urgency is educationally warranted, never manufactured |
| **I-3 Agency** | Students can defer or stop without shame |
| **I-4 One next action** | Primary path is obvious; secondary content does not compete |
| **I-5 Consistency** | Same concept → same name, duration, and verb across surfaces |
| **I-6 Accessibility** | Keyboard, assistive tech, and touch are first-class |
| **I-7 Performance** | Interaction feels immediate on ordinary student paths |
| **I-8 Sole runtime** | Premium claims apply only to the student experience students actually get |

---

## 4. Focus-area attributes

### 4.1 Student emotional journey

| Attribute | Target behaviour |
|-----------|------------------|
| **EJ-1 First-touch composure** | Sign-in / onboarding feel inviting and serious — not internal tooling |
| **EJ-2 Daily steadiness** | Ordinary study days feel clear; setbacks do not feel punitive |
| **EJ-3 Session containment** | During study, chrome recedes; cognitive load stays on the material |
| **EJ-4 Reflection dignity** | Reflection is optional, valued, and explained at the moment of use |
| **EJ-5 Return without guilt** | Coming back after a gap is welcomed; catch-up is honest, not shaming |
| **EJ-6 Exam-horizon tone** | Near-exam framing is focused and calm — not panic theatre |

**Fail examples:** Alpha/internal jargon on first touch; warning icons on day-zero empty history; missed-day language that implies moral failure.

---

### 4.2 Visual polish

| Attribute | Target behaviour |
|-----------|------------------|
| **VP-1 Token discipline** | Spacing, type, colour follow house tokens; no one-off palette drift |
| **VP-2 Hierarchy** | Brand and primary action dominate; secondary chrome is quiet |
| **VP-3 Density control** | Information density matches decision need; max KPI discipline respected |
| **VP-4 Iconography** | Consistent stroke weight and meaning; icons do not replace clarity |
| **VP-5 State craft** | Empty / loading / success / error states are designed, not browser-default |
| **VP-6 Mobile composition** | Narrow viewports recompose intentionally — not accidental wrap chaos |

**Fail examples:** Six KPI tiles in one row against house rules; native `confirm()` for destructive actions when styled modal exists.

---

### 4.3 Premium interaction design

| Attribute | Target behaviour |
|-----------|------------------|
| **IX-1 Predictability** | Primary CTAs behave the same way across Home → Mission → Session |
| **IX-2 Feedback clarity** | Every significant action yields immediate, calm feedback |
| **IX-3 Progressive disclosure** | Advanced detail available without forcing it on day one |
| **IX-4 Dead-end absence** | No inert buttons; unfinished capabilities are Hidden / Coming Soon, not clickable lies |
| **IX-5 Motion restraint** | Motion clarifies hierarchy (2–3 intentional patterns), never distracts from study |
| **IX-6 Confirmation discipline** | Destructive or irreversible actions use the shared modal pattern |

**Fail examples:** Different “start study” verbs on every screen; finish-session with no confirm where accidental tap ends work.

---

### 4.4 Motivation systems

| Attribute | Target behaviour |
|-----------|------------------|
| **MO-1 Diligence support** | Motivation reinforces showing up and finishing real missions |
| **MO-2 Non-coercion** | No streaks-as-punishment, dark patterns, or forced social proof |
| **MO-3 Honest signals** | Progress cues map to real study evidence, not vanity metrics |
| **MO-4 Professional tone** | Motivation language fits professional exam preparation |
| **MO-5 Recoverability** | Motivation systems survive imperfect weeks without narrative collapse |

**Fail examples:** Leaderboards; fake XP; “you’re falling behind” without educational warrant; pass-rate promises.

---

### 4.5 Accessibility

| Attribute | Target behaviour |
|-----------|------------------|
| **A11Y-1 Keyboard completeness** | All primary student paths operable without a pointer |
| **A11Y-2 Focus visibility** | `:focus-visible` rings are clear; mouse click does not fake keyboard focus styling |
| **A11Y-3 Names and roles** | Interactive controls expose accessible names; dialogs declare dialog semantics even if JS fails soft |
| **A11Y-4 Live updates** | Time-sensitive updates (e.g. session timer) use appropriate live regions when useful |
| **A11Y-5 Touch targets** | Interactive controls meet house minimum (token-backed) |
| **A11Y-6 Contrast & motion** | Text contrast holds; `prefers-reduced-motion` respected |

**Claim rule:** Do not assert WCAG conformance level without a recorded audit. Target is **presentation quality** ready for that audit.

---

### 4.6 Performance

| Attribute | Target behaviour |
|-----------|------------------|
| **PF-1 Perceived immediacy** | Primary navigations and mission open feel instant on broadband |
| **PF-2 Loading honesty** | Slow paths show crafted loading/skeleton — not blank or layout jump |
| **PF-3 Interaction readiness** | Controls do not appear clickable before they work |
| **PF-4 Asset hygiene** | CSS/JS weight on student paths stays disciplined; no decorative bloat |
| **PF-5 Resilience** | Soft JS failure fails visibly and safely (especially modals / confirms) |

**Fail examples:** Silent modal failure when Bootstrap missing; multi-second blank paints on Home.

---

### 4.7 Microcopy

| Attribute | Target behaviour |
|-----------|------------------|
| **MC-1 One vocabulary** | Home / Mission / Session / Revision share one verb set for the same acts |
| **MC-2 Value at point of use** | Explanations appear where the student needs them (e.g. Reflection), not only in onboarding |
| **MC-3 Student-grade language** | No commit hashes, env strings, engine status, or research-instrument framing on default paths |
| **MC-4 Explainability house style** | Prefer “what we observed / what we can conclude / what happens next” craft where guidance is shown |
| **MC-5 Helpfulness** | Help answers real “how do I…” questions; not release tables alone |
| **MC-6 Error dignity** | Errors name the problem and the next safe step |

**Fail examples:** “Education Operating System” as first-touch hero jargon without product decision; “Practice Outcome Capture” as student eyebrow.

---

### 4.8 Personalisation

| Attribute | Target behaviour |
|-----------|------------------|
| **PE-1 Authorised truth only** | Personalisation changes presentation of guidance already produced by educational cores |
| **PE-2 Contextual density** | New accounts see calmer, shorter chrome; rich history earns richer summary — not denser guilt |
| **PE-3 Exam-horizon framing** | Near-exam students see appropriate emphasis without strategy rewrite |
| **PE-4 Continuity memory** | Returning students see coherent “where you are” without re-onboarding theatre |
| **PE-5 Preference respect** | Appearance / notification / defer preferences stick and are obvious |

**Hard boundary:** Personalisation **must not** re-rank topics, alter mission selection, or invent Twin conclusions. Those remain recommendation / Runtime concerns — out of PX scope.

---

### 4.9 Celebration moments

| Attribute | Target behaviour |
|-----------|------------------|
| **CE-1 Real milestones** | Celebrate completed missions, honest revision returns, Continuity Front advances — not empty clicks |
| **CE-2 Proportion** | Celebration intensity matches educational weight (session complete ≠ exam pass) |
| **CE-3 Non-interruption** | Celebration never blocks the path back to rest or tomorrow’s clarity |
| **CE-4 Crafted completion** | Completion screens that exist in the product are actually reachable on the happy path |
| **CE-5 Shared joy, private dignity** | No forced sharing; optional warmth only |

**Fail examples:** Phantom “Complete” steps never rendered; confetti on thin evidence; research feedback widgets diluting the best completion screen.

---

### 4.10 Long-term engagement

| Attribute | Target behaviour |
|-----------|------------------|
| **LE-1 Multi-week coherence** | Journey / history / plan remain useful as weeks accumulate |
| **LE-2 Return rituals** | After gaps, the product re-orients quickly to one honest next action |
| **LE-3 Fatigue resistance** | Chrome does not grow noisier with use; progressive disclosure holds |
| **LE-4 Trust durability** | Durations, labels, and reasons stay consistent across months |
| **LE-5 Support durability** | Help and settings remain student-grade as the cohort matures past pilot framing |
| **LE-6 Exam approach** | Final weeks emphasise clarity and calm revision posture — not feature novelty |

---

## 5. Surface matrix (certification lens)

At PX-W5, score each Included surface for Visual / Interaction / Emotional (RP-001.4 method), and map residuals to focus-area attributes above.

| Surface | Must reach Target for PX PASS |
|---------|-------------------------------|
| Authentication | Yes |
| Onboarding | Yes |
| Home | Yes |
| Navigation | Yes |
| Mission | Yes |
| Session | Yes |
| Reflection | Yes |
| Study Plan | Yes |
| Journey / History | Yes |
| Help | Yes |
| Settings (student-visible) | Yes |
| Errors / Empty / Success / Loading | Yes |
| Mobile primary path | Yes |
| Analytics (if student-visible) | Yes or Hidden if not ready |
| Admin / diagnostic | Out of premium student claim (Hidden) |

---

## 6. Relationship to prior scorecards

| Prior artefact | Use in PX-001 |
|----------------|---------------|
| RP-001.4 Premium Quality Scorecard | Alpha baseline dimensions — re-score after educational completion; do not inherit PASS as Version 1 educational-completion premium |
| PX-001 / PX-002 / PX-003 findings | Seed backlog; re-verify before implementation |
| UI/UX Implementation Standard | Craft law for tokens and patterns — amend only via design change control, not ad hoc |

---

## 7. Certification rule

A **Premium Experience PASS** may be declared only when:

1. Charter start gates still hold,  
2. Focus-area attributes in §4 are Target+ (or waived),  
3. Surface matrix in §5 is Target+ on required rows,  
4. No §6-forbidden redesign from the charter was used to achieve scores,  
5. Evidence paths (screenshots, dogfood notes, a11y/perf checks) are filed.

Signed notionally: Product Experience · Premium Quality Attributes · PX-000 · 2026-08-02
