# Capability 3.6.3 — Student Calibration Product Flow

**Status:** Product flow only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.6.3 Student Calibration Product Flow (complete student journey from Study Plan creation through Calibration to the first Educational Intelligence recommendation)  
**Governing product law:** [`EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Upstream Calibration architecture:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](../architecture/CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md`](../architecture/CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md)  
**Experience honesty:** [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](../architecture/CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
**Scope:** Product experience design for Initial Student Calibration — **no Flask, routes, database, UI mock-ups, educational algorithms, persistence design, or implementation**

---

## Document purpose

Capabilities 3.6.1 and 3.6.2 established:

- the architecture for Student Calibration (capture → priors → emit; never reason);  
- the educational philosophy of Calibration (self-report establishes priors; Evidence establishes truth).

This milestone defines the **complete product experience**.

It answers:

> What does the student live through from Study Plan creation, through Calibration, to the first Educational Intelligence recommendation?

It does **not** answer how to build that experience in code.

**Governing product feeling (binding):**

> **“I don't have to start from zero.”**

**Governing product constraint (binding):**

> **Calibration records what the student declares. Educational Intelligence decides what to recommend. The questionnaire never becomes the coach.**

**Non-goals of this document**

- Flask routes, forms, templates, or wizard wireframes  
- Database schemas, Alembic migrations, or Twin Persistence implementation  
- Educational algorithms, readiness scores, mastery inference, or Decision redesign  
- UI layouts, visual design, or copy decks beyond product-language principles  
- ADR-002 redesign  

---

# 1. Purpose

## 1.1 Why Calibration exists from the student's perspective

From the student's point of view, Calibration exists so the product does not pretend they are a beginner when they are not.

Many candidates arrive with real educational history outside Kwalitec:

- Core Reading already completed;  
- sections of the syllabus already covered;  
- a previous sitting already attempted;  
- a clear objective that is revision or re-sit, not first exposure.

Without Calibration, the Study Plan can succeed while the learning experience still feels like:

> “Start again from the beginning.”

That feeling is not calm guidance. It is product ignorance wearing the clothes of a fresh start.

Calibration exists so the student can declare that history once, at the right moment, and feel:

> **“I don't have to start from zero.”**

## 1.2 What the student should feel — and what they should not feel

| The student should feel | The student should not feel |
|---|---|
| Their past study matters | They just completed an assessment |
| The product listened before advising | The product now “knows” their mastery |
| Starting here is honest, not blank | They are Mid/High ready because they filled a form |
| They can continue a journey already begun | The questionnaire decided what to study next |
| Early recommendations respect declared posture | Declaring Core Reading means foundations are finished forever |

## 1.3 Purpose restatement

Calibration is the product moment where:

1. the student tells the truth about educational history and objective;  
2. the product records that truth as **declared history**, not measured ability;  
3. Educational Intelligence can begin from a non-beginner-assuming starting point when history was declared;  
4. the student still understands that real readiness and mastery will be discovered through study Evidence later.

Governing restatement:

> **Calibration exists so returning students are recognised — without being over-claimed.**

---

# 2. Entry Point

## 2.1 Exact moment Calibration occurs

Calibration begins **immediately after a Study Plan is successfully created**.

```
Create Study Plan
        ↓
Study Plan successfully created
        ↓
Calibration begins
```

This is the only primary entry point for Initial Student Calibration in Version 1.0 product law.

## 2.2 Why this entry point — not elsewhere

| Not an entry point | Why |
|---|---|
| **First login** | The student may not yet have a syllabus-scoped Study Plan. Calibration without curriculum / exam scope cannot birth a meaningful Twin. Login is identity, not educational history. |
| **Settings** | Settings are maintenance. Calibration is Twin birth for a plan-scoped learning journey — not a preference toggle buried in account configuration. |
| **Dashboard** | The dashboard consumes Educational Intelligence after a Twin exists (or honestly signals absence). Using the dashboard as a Calibration trapdoor invents a read-path birth flow and competes with daily study. |
| **Mid-mission interrupt** | Interrupting study to collect history breaks calm. History belongs at journey birth, not mid-session. |
| **Every new session** | Calibration is not a recurring questionnaire. Birth happens once per Twin scope; later correction is explicit re-calibration, not daily re-asking. |

## 2.3 What “Study Plan successfully created” means for the journey

At this moment the product already knows:

- which student is authorised;  
- which curriculum / exam the plan is scoped to;  
- sitting / capacity facts the plan wizard already collected (where present).

Calibration then collects the **closed educational-history and objective declarations** that the plan alone does not truthfully establish — previous study, Core Reading, attempts, completed sections, study objective — without turning the wizard into a mastery engine.

## 2.4 Entry rules

1. **Calibration follows successful Study Plan creation** — not login, not settings, not dashboard.  
2. **No plan, no Calibration birth** — missing Study Plan means the journey has not started; do not invent a side door.  
3. **Skip is allowed only as explicit beginner / empty-history posture** — never as silent Mid readiness.  
4. **Dashboard may later invite history correction** only as an explicit re-calibration path after Version 1.0 persistence exists — never as the primary birth entry.

Governing restatement:

> **Calibration starts when the study journey starts — at plan birth — not when the student merely arrives.**

---

# 3. Product Journey

Complete student flow. Experience stages only — no screen layouts, routes, or implementation.

```
Welcome
        ↓
Educational History
        ↓
Previous Attempts
        ↓
Current Objective
        ↓
Completed Sections
        ↓
Exam Sitting
        ↓
Review
        ↓
Create Initial Twin
        ↓
First Dashboard
        ↓
Educational Recommendation
```

## 3.1 Stage-by-stage experience

### Welcome

The student is told, calmly, that the next few steps help the product begin from their real educational history — not from an assumed blank start.

They should understand:

- this is history and objective, not a test;  
- answers are declarations, not scores;  
- they may declare they are starting from scratch.

Tone: invitation, not onboarding theatre.

### Educational History

The student declares coarse prior engagement with this paper / syllabus:

- first-time / starting from scratch, or  
- previously studied / returning exposure, and  
- whether Core Reading is declared complete (whole paper and/or section-scoped where syllabus supports it).

Product meaning: exposure / coverage priors only.  
Product must not ask for mastery percentages or “how well do you know it?”

### Previous Attempts

The student declares whether they have sat this paper before — count and/or sitting labels when known; pass/fail only if they state it as history fact.

Product meaning: attempt-history prior.  
Product must not invent marks, predicted grades, or performance summaries from this step.

### Current Objective

The student declares what they are trying to achieve now, for example:

- first learning / first sit;  
- revision after Core Reading;  
- finish remaining sections;  
- re-sit / another attempt.

Product meaning: Goals posture.  
Product must not treat objective as readiness (“I am revising” ≠ High preparedness).

### Completed Sections

Where the student declares prior coverage, they mark completed syllabus sections (or V1-safe topic groupings) using **canonical curriculum structure** — not free-text invention.

Product meaning: declared syllabus-position priors.  
Product must not convert ticks into a mastery map or weighted coverage score presented as truth.

This stage may be light or skipped when the student declared true beginner / empty history.

### Exam Sitting

The student confirms or declares the intended sitting / target date for this journey.

Sitting facts already collected during Study Plan creation may be confirmed rather than re-asked. Capacity hours already collected remain plan/Goals structure — not Behaviour judgement.

Product meaning: Identity / Goals sitting anchor.  
Product must not forecast completion or pass probability here.

### Review

The student sees a plain-language summary of what they declared:

- posture (first-time / returning / revision / re-sit framing as declared);  
- Core Reading / sections / attempts as stated;  
- objective and sitting.

The review must say, truthfully, that this is **self-declared history** the product will use as a starting point — not Estimated Knowledge or readiness.

The student may correct before confirming.

### Create Initial Twin

On confirm, the product creates the initial Digital Twin from those declarations as **priors with thin warrant**.

Student-facing meaning:

- “Your study profile now includes what you told us about your history.”  
- Not: “Assessment complete.”  
- Not: “You are Mid ready.”  
- Not: “Here is your study path from the questionnaire.”

Educational Intelligence has not yet recommended. Calibration has only birthed structure.

### First Dashboard

The student arrives at the first post-Calibration dashboard for this plan.

The dashboard should feel like the start of guided study with history acknowledged — calm next action, not a wall of analytics.

Honesty posture:

- acknowledge declared history where relevant;  
- remain cold-start honest about Evidence still being thin;  
- do not display fake precision readiness theatre from Calibration alone.

### Educational Recommendation

Educational Intelligence produces the **first recommendation** (Decision selects; Recommendation packages).

This is the first educational judgement the student receives after Calibration.

The student should experience:

- one clear next action;  
- a calm reason that can respect declared posture without claiming mastery;  
- invitation to begin studying so Evidence can densify truth.

The recommendation must feel like intelligence beginning from declared history — not like the form echoing itself as a coach.

## 3.2 Journey invariants

1. **Order is birth → Twin → dashboard → recommendation** — never recommendation during Calibration stages.  
2. **Stages may shorten for explicit beginners** — empty-history path remains first-class, not a failed Calibration.  
3. **No stage performs educational judgement** — capture, confirm, birth, then intelligence.  
4. **Journey ends when the first recommendation is available to act on** — Calibration itself does not continue as a parallel daily flow.

Governing restatement:

> **The journey collects history, births priors, then lets Educational Intelligence speak once — calmly.**

---

# 4. Calibration Principles

These principles bind the product experience. They extend Epic 3 product principles and Capabilities 3.6.1 / 3.6.2 into student-facing behaviour.

## 4.1 Calm

Calibration should feel like a short, composed handoff into study — not a high-stakes intake, not urgency theatre, not streak language, not “unlock your readiness” pressure.

Calm means:

- few decisions at a time;  
- plain sequencing;  
- no competing CTAs;  
- no implication that finishing Calibration equals preparedness.

## 4.2 Optional where appropriate

Optional does **not** mean Calibration is unimportant.

It means:

- an explicit beginner / starting-from-scratch declaration is a lawful complete path;  
- detailed completed-sections marking may be skipped or deferred when posture is empty-history;  
- the student must not be trapped in compulsory micro-detail to earn a Twin;  
- skip-as-beginner is honest; skip-as-silence-that-becomes-Mid is forbidden.

Required for a meaningful returning birth: enough closed history to stop beginner falsehood — not a maximal biography.

## 4.3 Never overwhelming

Cognitive load stays low:

- closed field set only (aligned with 3.6.1 / 3.6.2 minimum set);  
- no mastery grids, confidence instruments, predicted-mark questions, or weak-topic essay fields;  
- progressive disclosure — ask deeper section detail only when prior study / coverage was declared;  
- one job per stage.

If a question would require educational judgement to answer well, it does not belong in Calibration.

## 4.4 Educational language

Speak like a serious study companion for professional exams:

- “educational history,” “Core Reading,” “previous attempt,” “sections you've already covered,” “what you're aiming for now”;  
- not gaming language, not clinical psychometrics jargon in the default path, not “we calibrated your mastery model.”

Invisible Intelligence still applies: students need not learn Twin, warrant, or pipeline vocabulary to complete Calibration.

## 4.5 Truthful wording

Product language must preserve the prior / truth distinction:

| Truthful | Forbidden |
|---|---|
| “Based on what you told us…” | “We've measured your mastery…” |
| “Starting from your declared history…” | “You're Mid ready…” |
| “We'll refine this as you study…” | “Assessment complete — profile locked…” |
| “This is not a test…” | “Your pass probability is…” |

After Calibration, the product may say the Twin includes self-declared history. It must not claim measured mastery or Mid/High preparedness from Calibration alone.

## 4.6 No fake precision

Do not display:

- readiness percentages born from the questionnaire;  
- mastery bars filled from declared sections;  
- pass probabilities;  
- false confidence decimals;  
- “coverage complete” presented as Evidence-backed truth.

Declared completed sections may be summarised in plain language as declarations. They must not be rendered as precision analytics.

## 4.7 Principles restatement

| Principle | Product meaning |
|---|---|
| Calm | Short, composed, no pressure theatre |
| Optional where appropriate | Beginner path and light detail are lawful; Mid silence is not |
| Never overwhelming | Closed minimum set; progressive disclosure |
| Educational language | Professional study vocabulary; invisible internals |
| Truthful wording | Declaration ≠ measurement |
| No fake precision | No readiness/mastery/probability theatre from the form |

Governing restatement:

> **Ask little. Speak honestly. Never let Calibration feel like an exam or a readiness score.**

---

# 5. Student Decisions

## 5.1 Decisions that belong to the student

The student owns autobiographical and goal facts only they can declare:

| Student decision | Why it belongs to the student |
|---|---|
| **Revision vs first learning (study objective)** | Only the student knows whether this journey is first exposure, revision, finishing gaps, or re-sit intent. |
| **Completed sections (declared)** | Only the student knows which syllabus parts they believe they already covered outside the product. |
| **Exam sitting / intended target** | The student chooses the sitting they are aiming for (confirming plan facts where already collected). |
| **Study objective framing** | First sit, revise, re-attempt — declared Goals posture. |
| **Previously studied / Core Reading completed** | Off-product history the product did not observe. |
| **Previous attempts** | Sitting history the product did not observe. |
| **Beginner / starting-from-scratch declaration** | Explicit empty-history posture — a student decision, not a system inference. |
| **Whether to skip detailed section marking when beginner** | Optional depth; empty-history completeness does not require section grids. |
| **Confirm or correct the review summary** | Final ownership of what was declared before Twin birth. |

These decisions create **priors**. They do not create recommendations.

## 5.2 Decisions that must remain with Educational Intelligence

Educational Intelligence owns judgement, selection, and packaging. Calibration must never answer these:

| Educational Intelligence decision | Owner |
|---|---|
| **What to study next** | Decision Engine |
| **How the next action is packaged / titled / explained** | Recommendation |
| **What today's mission contains** | Mission Intelligence |
| **How ready / prepared the student is** | Readiness Aggregation |
| **What the student has mastered** | Knowledge beliefs via Evidence → Twin Update Pipeline |
| **What is weak / strong under assessment** | Performance + Evidence-driven judgement |
| **Whether foundations may be skipped** | Decision under thin warrant — never Calibration policy |
| **Predicted marks / pass probability** | Predictions / later forecasting — never Calibration |
| **Whether declaration outweighs later Evidence** | Evidence sovereignty — Evidence dominates conflicting priors for judgement |
| **Session feasibility / burnout pacing as educational judgement** | Constraints + Behaviour / pacing domains — not Calibration autobiography |

## 5.3 Boundary table

| Question | Who answers |
|---|---|
| “Have I studied this before?” | Student |
| “Did I finish Core Reading?” | Student (declaration) |
| “Which sections did I already cover?” | Student (declaration) |
| “Am I revising or learning first?” | Student (objective) |
| “Which sitting am I aiming for?” | Student |
| “What should I do next?” | Educational Intelligence |
| “Am I ready?” | Educational Intelligence |
| “Have I mastered Section X?” | Educational Intelligence (via Evidence) — never Calibration |
| “Should I skip foundations?” | Educational Intelligence — never the form |

## 5.4 Decision ownership invariant

```
Student declares history + objective
        ↓
Calibration births Twin priors
        ↓
Educational Intelligence judges + selects + packages
        ↓
Student acts on recommendation → Evidence begins
```

Governing restatement:

> **Students own their history story. Educational Intelligence owns educational judgement. Neither may seize the other's role.**

---

# 6. Failure Behaviour

Product behaviour only — no implementation mechanics.

## 6.1 Student skips Calibration

**Meaning:** The student declines the history journey or chooses an explicit skip.

**Required product behaviour:**

1. Treat skip as **explicit beginner / empty-history posture** only when the student confirms starting from scratch — or as **no calibrated returning Twin** when they abandon without declaration.  
2. Never invent Mid readiness, mastery, or returning-student theatre to “fill in” a skip.  
3. Study Plan remains successfully created; learning may continue under cold-start honesty / empty Twin posture as architecture allows.  
4. Product language stays honest: we do not yet have declared history — not “you're all set and Mid ready.”  
5. Do not punish skip with nagging loops on every dashboard load; optional later invitation to declare history is Version 1.0+ re-calibration territory, not Alpha harassment.

**Forbidden:** Silent Mid defaults. Fake Evidence. Questionnaire coercion disguised as required settings.

## 6.2 Student abandons halfway

**Meaning:** The student starts Calibration stages then leaves before Review confirm / Twin birth.

**Required product behaviour:**

1. Partial answers are **not** a calibrated Twin.  
2. Do not partially write mastery-like state from incomplete forms.  
3. On return via the plan journey, offer to **resume Calibration** calmly — or confirm beginner / empty-history completion — without shame copy.  
4. Dashboard / recommendation paths must not pretend Calibration finished.  
5. Prefer resume-from-last-stage over forcing a full restart when safe; prefer full restart over corrupted half-priors if continuity would invent structure.

**Forbidden:** Half-written Twin that looks Evidence-dense. Auto-confirming guessed remaining answers.

## 6.3 Missing Study Plan

**Meaning:** Calibration is attempted without a successfully created Study Plan / syllabus-scoped journey.

**Required product behaviour:**

1. Calibration does **not** begin.  
2. Route the student to create a Study Plan first (product direction — not a technical redirect specification).  
3. Do not birth a Twin without curriculum / exam scope.  
4. Do not collect educational history into an orphan profile that later mismatches a different paper.

**Forbidden:** Settings-based Calibration birth. Login-time Calibration without plan scope.

## 6.4 Missing curriculum

**Meaning:** The plan or Calibration cannot resolve a lawful syllabus / curriculum identity (unavailable curriculum, invalid scope, V1/V2 identity unresolved).

**Required product behaviour:**

1. Calibration cannot complete Twin birth.  
2. Fail honestly: the product cannot record section history against an unknown syllabus.  
3. Preserve the Study Plan success state if plan creation already succeeded with a known curriculum; if curriculum is missing entirely, do not fake section pickers.  
4. Student-facing language: we cannot calibrate completed sections without the official syllabus — not an opaque error that implies the student failed a test.

**Forbidden:** Free-text syllabus invention. Accepting invalid section ids as Twin truth.

## 6.5 Conflicting answers

**Meaning:** Declarations disagree with each other — e.g. “starting from scratch” plus many completed sections; “no previous study” plus prior attempts; revision objective with empty coverage and no prior study.

**Required product behaviour:**

1. Prefer **clarify on Review** over silent coercion.  
2. Ask the student to reconcile in plain language before Twin birth.  
3. If the student confirms a coherent posture, record that posture; do not “average” conflicts into Mid beliefs.  
4. If unresolved, degrade to the more conservative honest posture (empty or thinner priors) rather than inventing returning mastery.  
5. Never resolve conflict by inventing readiness, mastery, or recommendations.

**Forbidden:** Algorithmic conflict scoring. Auto-upgrading contradictions into preparedness theatre. Quietly dropping attempt history to make the form look clean.

## 6.6 Failure behaviour summary

| Failure | Product behaviour |
|---|---|
| Skip | Explicit empty-history or no returning Twin — never Mid invention |
| Abandon halfway | No partial Twin theatre; calm resume or beginner confirm |
| Missing Study Plan | No Calibration birth; create plan first |
| Missing curriculum | Honest stop; no free-text syllabus |
| Conflicting answers | Clarify on Review; conservative honesty over invented coherence |

Governing restatement:

> **When Calibration fails or is incomplete, stay honest and empty — never invent a confident student.**

---

# 7. Internal Alpha

Recommend the simplest experience needed for Internal Alpha. Intentionally minimal.

## 7.1 Alpha goal

Prove the product feeling:

> “I don't have to start from zero.”

…without shipping the full Version 1.0 journey, persistence durability, or Evidence-loop densification.

## 7.2 Minimal Alpha flow

```
Study Plan successfully created
        ↓
Short Calibration (minimal closed questions)
        ↓
Confirm declarations
        ↓
Initial Twin priors (session-honest as architecture allows)
        ↓
First dashboard + first Educational Intelligence recommendation
```

## 7.3 What Alpha should include

1. **Entry only after Study Plan success** — no login/settings/dashboard birth.  
2. **Minimal closed questions only:**  
   - previously studied? (yes/no or coarse);  
   - Core Reading completed? (declared);  
   - previous attempts? (none / one / more — coarse);  
   - current objective (first learning / revision / re-sit);  
   - intended sitting confirm if not already known;  
   - optional light completed-sections only if “previously studied” or coverage was declared.  
3. **Explicit beginner path** in one confirmation.  
4. **Review in plain language** with prior ≠ mastery wording.  
5. **One first recommendation** after birth — Decision-owned, thin-warrant honest.  
6. **Calm copy** — no fake readiness numbers from the form.

## 7.4 What Alpha should deliberately omit

| Omit in Alpha | Why |
|---|---|
| Full multi-stage progressive disclosure polish | Minimize steps; prove honesty first |
| Rich section-by-section biography for every student | Overwhelming; optional depth can wait |
| Re-calibration / history editing surfaces | Persistence + lineage not Alpha-critical |
| Diagnostic assessment inside Calibration | Different Evidence path |
| Mastery/readiness/confidence instruments | Violates Calibration law |
| Durable Twin Persistence guarantees | Known debt (E2-PE-01); do not fake durability in copy |
| Dense Evidence-loop storytelling | Evidence loops incomplete — stay cold-start honest |
| Dashboard nag to complete skipped Calibration every visit | Calm over coercion |

## 7.5 Alpha honesty rules

1. Prefer honest emptiness / thin warrant over invented Mid.  
2. If Persistence is not durable yet, do not claim the profile is permanently saved across all sessions.  
3. Do not seed fake Evidence to make the first recommendation look denser.  
4. Skipping remains lawful as beginner posture — not as Mid fill.  
5. Success metric for Alpha: returning testers feel recognised without feeling scored.

### Alpha motto

> **Short questions. Honest priors. One clear next step. No theatre.**

---

# 8. Version 1.0

Recommend how the experience should evolve after Twin Persistence and Evidence Loops exist.

## 8.1 What changes when Twin Persistence exists

| After Persistence | Product evolution |
|---|---|
| Birth Twin survives sessions | Calibration becomes a true once-per-journey birth, not a session ritual |
| Provenance preserved | Review and later explainability can show “declared at plan creation” |
| TwinProvider retrieve path stabilises | First dashboard reliably consumes calibrated priors |
| Re-calibration becomes possible | Explicit history correction — rare, reviewed, provenance retained |

Product implication: the Welcome → … → Create Initial Twin journey becomes durable product law, not an Alpha experiment that evaporates.

## 8.2 What changes when Evidence Loops exist

| After Evidence Loops | Product evolution |
|---|---|
| Study produces Learning Evidence | Product can truthfully say guidance improves from observed study |
| Evidence supersedes conflicting priors for judgement | Student sees recommendations evolve beyond autobiography |
| Thin warrant densifies | Cold-start honesty after Calibration becomes temporary, not permanent emptiness theatre |
| Diagnostics (if added later) | Remain a separate assessed path — never folded into Calibration questionnaire |

Product implication: Calibration's job shrinks emotionally over time — history birth once; truth discovered through study.

## 8.3 Version 1.0 experience recommendations

1. **Keep the same entry point** — Study Plan success → Calibration → Twin → dashboard → first recommendation.  
2. **Keep the closed minimum information set** — expand only by product architecture revision, not ad-hoc form growth.  
3. **Ship the full staged journey** with progressive disclosure (Welcome through Educational Recommendation) while preserving calm and optional depth.  
4. **Distinguish postures in experience without readiness bands** — first-time, returning, revision, repeat as declared framing.  
5. **Make Review the integrity gate** — conflicts clarified; prior ≠ mastery language mandatory.  
6. **First recommendation remains Decision-owned** under thin warrant; prefer evidence-creating early actions when beliefs are empty — including for revision/re-sit postures.  
7. **Add explicit re-calibration** as a rare history-correction journey (not Settings clutter; not daily dashboard interrupt) with retained lineage.  
8. **Surface honesty in the Experience Contract sense** — acknowledge declared history; never claim Mid/High from Calibration alone; show Evidence-backed evolution when it exists.  
9. **Never let Calibration become recommendation repair** — if the student dislikes a recommendation, they study or dismiss with journaled reasons; they do not rewrite history to force a different coach answer.  
10. **Preserve V1/V2 curriculum-safe section picking** — official syllabus only.

## 8.4 Version 1.0 emotional arc

```
Plan created
  → “Tell us where you're starting from.”
  → “We've recorded what you declared — not measured you.”
  → “Here's one clear next step.”
  → (study) “Guidance will deepen from what you actually do.”
```

### Version 1.0 motto

> **Declare history once. Discover truth through Evidence. Keep Educational Intelligence as the only coach.**

---

# 9. Product Flow Compliance Summary

| Invariant | Status under this product flow |
|---|---|
| Entry after Study Plan success only | Affirmed — not login / settings / dashboard |
| Student feeling: “I don't have to start from zero.” | Affirmed as purpose |
| Calibration does not recommend | Affirmed — intelligence after Twin birth |
| Student owns history/objective decisions | Affirmed |
| Educational Intelligence owns judgement | Affirmed |
| Calm, optional-where-appropriate, no fake precision | Affirmed |
| Failure stays honest (no Mid invention) | Affirmed |
| Alpha minimal; Version 1.0 evolves with Persistence + Evidence | Affirmed |
| No Flask / DB / UI mock-ups / algorithms | Honoured — product flow only |
| Aligned with 3.6.1 architecture and 3.6.2 educational analysis | Affirmed |

---

# 10. STOP

This document defines **Student Calibration product flow only**.

It does **not** authorise:

- Implementation  
- Flask routes or forms  
- Database tables or migrations  
- UI mock-ups or visual design  
- Educational algorithms  
- Twin Persistence implementation  
- Evidence seeding  
- Educational Intelligence redesign  

**STOP.**
