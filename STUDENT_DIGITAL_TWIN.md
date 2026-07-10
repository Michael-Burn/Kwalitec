# Student Digital Twin

**Status:** Canonical domain architecture specification  
**Epic:** Epic 0 – Student Intelligence Platform  
**Capability:** 0.1 – Design the Student Digital Twin  
**Audience:** Product, engineering, AI agents, future subsystem owners  
**Scope:** Conceptual domain model — not a database schema and not an implementation plan  
**Companion docs:** [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md), [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`knowledge/`](knowledge/)

---

## Document purpose

This specification defines the **Student Digital Twin** as the central domain model of Kwalitec.

It answers:

- What the Student Digital Twin is
- Why it exists
- What information it owns
- How it evolves over a student’s exam journey
- Which subsystems update it
- Which subsystems consume it
- Which architectural rules govern it

This document is the **canonical reference** for future intelligent features — Planning, Missions, Readiness, Analytics, AI Coach, Revision, Notifications, and Predictions. Implementation milestones must conform to this model; they must not invent competing learner-state stores.

**Non-goals of this document**

- Table designs, Alembic revisions, or ORM class layouts
- API contracts for HTTP routes
- Concrete scoring formulas or ML model choices
- Replacement of the Curriculum Engine as syllabus source of truth

---

# Executive Summary

The **Student Digital Twin** is Kwalitec’s single authoritative representation of a learner’s exam-preparation state. It is a living, evidence-backed model of *who the student is relative to a syllabus and a sitting* — not a static profile, not a study plan, and not a dashboard cache.

Kwalitec’s product thesis is to **reduce decisions and increase learning** ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)). The hardest problem in professional exam preparation is not finding content; it is deciding what to study next under a fixed exam date, uneven syllabus weights, incomplete coverage, fading memory, and limited hours. That decision quality depends on an accurate model of the learner.

Therefore Kwalitec models **learners**, not merely study plans:

| Artefact | Role |
|---|---|
| **Curriculum** | Official syllabus truth (sections, topics, objectives, exam weights) — shared across students |
| **Student Digital Twin** | Per-student learning state — knowledge, memory, behaviour, readiness, goals, predictions |
| **Study Plan / Mission** | *Derived* schedules and daily work — regenerated from Twin + Curriculum + constraints |

A study plan is a consequence of intelligence. If the Twin is wrong, every plan, mission, readiness score, and recommendation is wrong — even if the curriculum is perfect. If the Twin is right, plans can be rebuilt safely whenever life, mastery, or calendar change.

The Twin is **probabilistic where knowledge is uncertain**, **immutable in its evidence trail**, and **deterministic in how core engines read it**. Generative AI may explain or coach *around* Twin-derived outputs; it must never silently own or bypass Twin state ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) Core Product Principles; [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)).

---

# Vision

Long-term, every serious candidate’s relationship with Kwalitec is mediated by a continuously evolving Digital Twin that:

1. **Knows the student’s position** on the official syllabus (V1 flat or V2 hierarchical) without inventing a parallel topic tree.
2. **Tracks evidence of learning** — attempts, missions, revisions, mocks, skips, and confidence signals — without discarding history.
3. **Estimates knowledge and retention** as probabilistic beliefs that decay and recover with evidence.
4. **Drives personalised recommendations** that remain explainable: same Twin inputs → same core outputs.
5. **Powers adaptive planning** so schedules rebalance from current state rather than from stale week grids.
6. **Surfaces readiness and pass risk** as evidence-based narratives tied to curriculum weight and time remaining.
7. **Improves predictions over time** as outcomes (sittings, mocks, longitudinal accuracy) calibrate forecasts.
8. **Supports an AI Learning Coach** that grounds dialogue in Twin state — never invents syllabus order or hides scoring logic.

The Twin is the operating-system state of exam preparation: the place every intelligent subsystem reads from and writes evidence into, until the student walks into the exam room ready.

---

# Guiding Principles

These principles are binding for all Twin-related design and implementation.

1. **The Digital Twin is the single source of truth for learner state.**  
   Subsystems may cache projections for performance, but must not maintain competing mastery, readiness, or “study next” stores that diverge from the Twin.

2. **Curriculum remains the source of truth for syllabus structure.**  
   The Twin references curriculum entities (curriculum, section, topic, learning objective) via canonical identity and traversal ([ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md)). It never invents topics.

3. **Knowledge is probabilistic.**  
   Mastery and retention are beliefs updated by evidence, not binary badges. Uncertainty must be representable (confidence, intervals, evidence density).

4. **Recommendations must be explainable.**  
   Every recommendation cites Twin factors (coverage gap, weight, overdue review, deadline pressure, workload) — not an opaque composite ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)).

5. **Evidence is never discarded.**  
   Raw learning events are append-only. Derived Twin views may be recomputed; the evidence log is the audit spine.

6. **Predictions improve over time.**  
   Forecasts are first-class Twin outputs that recalibrate as new evidence and outcomes arrive. Predictions never bypass Twin inputs.

7. **Learning is dynamic.**  
   Memory decays; behaviour shifts; availability changes. The Twin must support decay, rebalance, and recovery — not only monotonic “completion.”

8. **Planning is a consequence of intelligence.**  
   Study plans and missions are regenerated from current Twin state + curriculum + constraints. They are not the authoritative learner model.

9. **Determinism over theatre.**  
   Core Twin updates and core consumers (planning, readiness, recommendations) must be reproducible from the same inputs ([`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)).

10. **Protect sustainable intensity.**  
    Motivation and burnout signals are Twin domains. Unsustainable streaks are product failures, not engagement wins.

11. **AI assists; it does not own the path.**  
    Assistive coaching consumes Twin state and explainable recommendations. It must not write hidden Twin mutations or invent syllabus order.

12. **One Twin per student (per product identity).**  
    Multi-exam and multi-paper context lives *inside* the Twin as scoped goals and knowledge slices — not as duplicate Twins that fight each other.

---

# Domain Model

The Student Digital Twin is composed of ten major domains. Together they form one conceptual aggregate. Persistence layout is deferred; domain boundaries are not.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Student Digital Twin                              │
│                                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Identity │ │  Goals   │ │Knowledge │ │  Memory  │ │Behaviour │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │Performan.│ │ Planning │ │Readiness │ │Motivation│ │Predicts. │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                                          │
│              Evidence Log (immutable)  ·  Decision Journal               │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Identity

### Purpose

Anchor the Twin to a real Kwalitec user and their account-level attributes without conflating authentication with learning state.

### Responsibilities

- Bind Twin to authenticated user identity (Flask-Login user; see [authentication.md](knowledge/subsystems/authentication.md))
- Hold stable learner identifiers used by all subsystems
- Record account-level preferences that affect intelligence (timezone, notification defaults) without owning auth secrets

### Inputs

- Registration / admin-provisioned account creation
- Settings updates (preferences)
- Exam catalogue selections that attach goals (not identity itself)

### Outputs

- Stable `student_id` / user reference for all Twin reads and writes
- Preference context for notifications and scheduling windows

### Relationships

- **Owns:** link to User; preference slice
- **Does not own:** passwords, sessions, CSRF (security layer)
- **Feeds:** all domains (every Twin operation is scoped to Identity)

### Future extensions

- Multi-device presence; institution-linked identity overlays (Phase 7); privacy export / deletion packages that traverse Twin evidence

---

## 2. Goals

### Purpose

Represent what the student is trying to achieve: which paper, which sitting, what target outcome, and under what time constraints.

### Responsibilities

- Active and historical exam targets (body, paper, year/curriculum version, sitting date)
- Target intensity and pass ambition (e.g. first-time pass vs re-sit focus)
- Availability commitments that constrain planning (hours/day, study days)
- Goal status: active, deferred, completed, abandoned

### Inputs

- Study plan wizard selections ([study-planning.md](knowledge/subsystems/study-planning.md))
- Examination catalogue / exam timeline metadata
- Manual goal changes (defer sitting, switch paper)

### Outputs

- Active goal context for Planning, Readiness, Predictions
- Deadline and capacity constraints for recommendation priority

### Relationships

- **References:** Curriculum (official syllabus for the goal)
- **Drives:** Planning domain, Readiness time-remaining, Prediction target-date risk
- **Distinct from:** Planning artefacts (WeekPlan rows are derived, not goals)

### Future extensions

- Multi-paper concurrent goals with shared capacity budgets
- Career-path goals beyond a single sitting
- Institution-assigned cohort goals

---

## 3. Knowledge

### Purpose

Represent the student’s estimated mastery of curriculum entities — the core “what do they know?” model.

### Responsibilities

- Per-topic (and eventually per-objective) mastery belief
- Coverage state relative to canonical traversal order
- Strength of evidence supporting each belief
- Gap identification against exam weights (V1 topic weights / V2 section weights)

### Inputs

- Learning evidence (attempts, quizzes, mocks, mission completions)
- Diagnostic assessment results
- Manual confidence adjustments (explicitly tagged as self-report)

### Outputs

- Mastery map consumable by Planning, Missions, Readiness, Recommendations
- Weighted coverage summaries aligned with curriculum weights

### Relationships

- **Bound to:** Curriculum entities via canonical IDs; ordering via `CurriculumService` helpers only
- **Updated by:** Evidence Model; Adaptive Learning / mastery services conceptually
- **Consumed by:** nearly all intelligence subsystems
- **Must remain V1/V2 compatible** ([ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md))

### Future extensions

- Objective-level mastery; prerequisite-aware knowledge graphs; transfer across related papers

---

## 4. Memory

### Purpose

Model retention and forgetting — knowledge that was demonstrated may fade without review.

### Responsibilities

- Spaced-repetition / review-due state per topic (or card/objective unit)
- Retention estimates and last-reinforced timestamps
- Decay parameters informed by evidence density and time since success

### Inputs

- Successful and failed reviews
- Time elapsed without reinforcement
- Adaptive learning scheduling outcomes

### Outputs

- Overdue / due-soon review sets for Missions and Recommendations
- Retention forecasts for Predictions

### Relationships

- **Complements Knowledge:** Knowledge is “can they do it now?”; Memory is “will they still be able to?”
- **Feeds:** Revision Engine, Mission Optimizer review pressure, Readiness durability narrative

### Future extensions

- Item-level memory for question banks; exam-condition interference models; personalised decay rates

---

## 5. Behaviour

### Purpose

Capture how the student actually studies — patterns that affect plan realism and burnout risk.

### Responsibilities

- Session cadence, start times, completion rates
- Skip / postpone patterns
- Preference signals revealed by Decision Journal (accept / dismiss reasons)
- Adherence to planned vs actual study

### Inputs

- Study sessions started/completed
- Skipped sessions and dismissed recommendations
- Mission completion ratios
- Time-spent telemetry (when collected)

### Outputs

- Reliability / adherence scores for Planning rebalance
- Behavioural features for Predictions (completion forecast, burnout risk)
- Coaching hooks for AI Coach (“you tend to skip Friday reviews”)

### Relationships

- **Feeds:** Motivation, Planning capacity realism, Notifications timing
- **Audited by:** Decision Journal (recommendation responses)

### Future extensions

- Context tags (commute study vs deep work); device patterns; collaboration attendance

---

## 6. Performance

### Purpose

Represent measured outcomes from practice — accuracy, mistake patterns, and exam-condition rehearsal results.

### Responsibilities

- Attempt and accuracy trends by topic / objective
- Mistake taxonomy aggregates (conceptual; concrete taxonomies may evolve)
- Mock exam and quiz score histories
- Calibration between self-confidence and observed accuracy

### Inputs

- Questions answered, quizzes, mock exams
- Mistake records ([LearningService](PROJECT_CONTEXT.md) conceptual ownership)
- Timed rehearsal metadata

### Outputs

- Performance slices for Analytics and Readiness
- Weak-area signals for Revision and Missions
- Calibration inputs for Predictions

### Relationships

- **Updates Knowledge and Memory** via Evidence Model
- **Must share metric definitions with Analytics** so dashboards never fork readiness formulas ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) Analytics pillar)

### Future extensions

- Exam-style item types; partial-credit models; cross-sitting performance baselines

---

## 7. Planning

### Purpose

Hold the *current derived plan state* and planning constraints — always regenerable from Twin + Curriculum.

### Responsibilities

- Active plan reference and generation metadata (inputs hash / version for determinism)
- Distribution of topics across available time (conceptual WeekPlan / schedule view)
- Rebalance triggers and last-rebalance reasons
- Catch-up / intensity mode flags

### Inputs

- Goals (deadline, availability)
- Knowledge + Memory gaps
- Behaviour adherence
- Curriculum canonical topic order

### Outputs

- Schedule consumed by Mission Engine
- Pace baseline for Readiness
- Explainable “why this week’s topics” factors

### Relationships

- **Derived, not authoritative:** if Twin Knowledge changes, Planning regenerates
- **Owned conceptually by:** Planning Engine / StudyPlan + Planning services ([study-planning.md](knowledge/subsystems/study-planning.md))
- **Must use** canonical traversal ([ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md))

### Future extensions

- Multi-paper calendars; automatic illness catch-up modes; preference-aware intensity caps

---

## 8. Readiness

### Purpose

Estimate exam preparedness and pass-risk concentration in language the student can act on.

### Responsibilities

- Coverage vs weighted syllabus
- Pace vs days remaining
- Risk concentration on high-weight weak areas
- Sit / defer narrative inputs (future product surface)

### Inputs

- Knowledge, Memory, Performance, Goals (time remaining), Planning pace
- Curriculum weights (V1/V2 aware)

### Outputs

- Readiness summary for dashboard / analytics
- Risk factors for Recommendations and AI Coach
- Inputs to Predictions (expected readiness, pass probability)

### Relationships

- **Owner of readiness definitions** — Analytics consumes, does not redefine ([readiness.md](knowledge/subsystems/readiness.md))
- **Explainability required:** factors must be inspectable

### Future extensions

- Mock-informed calibration; “if you study X hours/week” projections; explicit sit/defer bands

---

## 9. Motivation

### Purpose

Protect sustainable intensity and model engagement health — the long-game domain.

### Responsibilities

- Workload intensity and burnout risk signals ([BurnoutMonitor](knowledge/development/glossary.md))
- Consistency vs overwork
- Recovery recommendations
- Guardrails on mission load

### Inputs

- Behaviour (session volume, streaks)
- Mission completion under high load
- Self-reported energy (future)
- Goals’ intensity targets

### Outputs

- Burnout flags for Mission Optimizer and Notifications
- Rest / recovery suggestions for Recommendations
- Motivation context for AI Coach

### Relationships

- **Constrains Planning and Missions** — product principle: protect sustainable intensity
- **Feeds Predictions:** risk of burnout, risk of missing target date via collapse

### Future extensions

- Intensity budgets; recovery weeks; celebration of durable habits over vanity streaks

---

## 10. Predictions

### Purpose

Host forward-looking estimates derived from Twin state — never from side-channel data that Twin domains do not contain.

### Responsibilities

- Maintain current prediction set with confidence intervals
- Recalculate when material Twin evidence arrives
- Expose prediction metadata (model/version, as-of timestamp, input factors)

### Inputs

- All Twin domains relevant to the forecast
- Historical calibration data (as product matures)
- Outcome capture post-exam (future)

### Outputs

- Pass probability, mastery/retention/completion forecasts, burnout and deadline risk, expected readiness  
  (see [Prediction Contract](#prediction-contract))

### Relationships

- **Strictly downstream of Twin state** — predictions never bypass Twin
- **Consumed by:** Recommendations, AI Coach, Analytics, Notifications
- **Must remain explainable at factor level** even when probabilistic

### Future extensions

- Sitting-level calibration; cohort-relative benchmarks (privacy-preserving); multi-exam portfolio forecasts

---

# Learning Evidence Model

Evidence is the only legitimate way to mutate Twin beliefs. Evidence records are **immutable** once written. Corrections are new evidence (e.g. “void attempt”), never silent edits.

```
Student action / system event
        ↓
Evidence record (append-only)
        ↓
Twin domain updates (Knowledge, Memory, Behaviour, Performance, …)
        ↓
Predictions recalculated
        ↓
Recommendations / Plans / Missions regenerated as needed
```

| Evidence type | What changes | Confidence impact | Decay behaviour | Future use |
|---|---|---|---|---|
| **Study session** | Behaviour (time, adherence); may lightly reinforce Memory if tagged to topics | Low–medium for Knowledge unless paired with assessment | Session alone does not prevent mastery decay | Capacity realism; coaching on habits |
| **Question answered** | Performance accuracy; Knowledge belief for mapped topic/objective; Memory last-reinforced | Medium–high depending on item quality and independence | Correct answers slow decay; errors may accelerate review due | Mistake taxonomy; adaptive item selection |
| **Quiz** | Performance aggregate; Knowledge across quiz scope | Higher than single item if quiz is syllabus-mapped | Topic-level retention clock updates for covered items | Diagnostic refresh; readiness calibration |
| **Mock exam** | Performance under exam conditions; Readiness calibration inputs; Knowledge stress-test | High for exam-condition belief; may differ from untimed mastery | Strong signal but still subject to time decay before sitting | Pass-probability calibration; sit/defer advice |
| **Mission completion** | Behaviour adherence; Planning progress; topic exposure flags | Medium — completion ≠ mastery unless tasks include assessed work | Incomplete missions increase catch-up pressure | Mission Optimizer tuning; consistency metrics |
| **Revision** | Memory reinforcement; Knowledge refresh on weak/high-weight topics | Medium–high for retention beliefs | Explicitly counters decay; overdue revision raises risk | Revision Engine scheduling; weight-aware focus |
| **Skipped session** | Behaviour (skip pattern); Motivation / burnout interpretation; Planning slip | Does not reduce Knowledge directly; increases deadline risk | Increases urgency and rebalance need | Notifications; completion forecast |
| **Manual confidence adjustment** | Knowledge self-report channel (tagged `self_report`) | Low–medium; must not override dense contrary evidence | Self-report decays faster than assessed evidence | Diagnostic bootstrap; honesty calibration vs Performance |
| **Time spent** | Behaviour effort; Planning capacity validation | Weak for Knowledge alone | No mastery permanence from time alone | Burnout Monitor; realistic hour budgets |
| **Diagnostic assessment** | Initial Knowledge map; Goals starting position | High at Twin birth / reset | Establishes baseline; subsequent evidence dominates | Cold-start quality; re-sit repositioning |
| **Recommendation decision** (accept/dismiss) | Behaviour preference; Decision Journal | Indirect — shapes future ranking, not mastery | N/A | Explainability audit; personalisation of alternatives |
| **Post-exam outcome** (future) | Predictions calibration; Goals completion | Outcome-level — calibrates models, not topic micro-beliefs | N/A | Pass-rate KPI; model improvement |

### Evidence rules

1. Every evidence record cites **curriculum identity** when topic-scoped (never free-text-only topics).
2. Evidence carries **timestamp**, **source subsystem**, and **provenance** (user action vs system-inferred).
3. Twin domain updates are **functions of evidence + prior Twin state** — deterministic for core paths.
4. Analytics and AI Coach may *read* evidence; they must not invent evidence.

---

# Twin Lifecycle

```
Student account provisioned / registers (controlled access)
        ↓
Student Digital Twin created (empty domains + Identity)
        ↓
Exam / curriculum goal selected
        ↓
Diagnostic assessment (optional but recommended)
        ↓
Initial Knowledge + Goals state established
        ↓
Planning begins (plan derived from Twin + Curriculum + availability)
        ↓
Daily loop:
    Learning evidence received
        ↓
    Twin domains updated
        ↓
    Predictions recalculated
        ↓
    Recommendations regenerated
        ↓
    Missions / plan rebalance as triggered
        ↓
    Student acts again
        ↓
(repeat until sitting)
        ↓
Exam day (minimal decision surface)
        ↓
Post-exam reflection / outcome capture → Twin archival slice + calibration
```

### Lifecycle notes

- **Twin creation** is idempotent with respect to user identity: exactly one Twin per student.
- **Cold start** without diagnostic is allowed but must mark Knowledge confidence as low.
- **Re-sits** extend Goals and may reset Planning while preserving historical Evidence and Performance.
- **Curriculum version changes** (new syllabus year) attach new Knowledge slices; they do not delete prior evidence.

---

# Intelligence Flow

Information moves in a closed learning loop. Curriculum is upstream of the Twin; plans are downstream.

```
┌─────────────────────┐
│  Curriculum Engine   │  Official syllabus (V1/V2 JSON → DB)
│  + Catalogue/Timeline│
└──────────┬──────────┘
           │ structure, weights, order
           ▼
┌─────────────────────┐
│  Student actions     │  Study, practice, skip, decide
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Evidence            │  Immutable learning events
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Student Digital Twin│  Authoritative learner state
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Prediction Engine   │  Forecasts from Twin only
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Recommendation Eng. │  Explainable next actions
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Study Plan / Mission│  Derived schedule + daily work
└──────────┬──────────┘
           │
           └──────────► Student actions (loop)
```

### Layering alignment

This flow respects Kwalitec’s service-layer architecture ([ADR-001](knowledge/architecture/ADR-001-service-layer.md), [`ARCHITECTURE.md`](ARCHITECTURE.md)):

- HTTP blueprints collect actions and display outputs
- Services apply Twin updates and derive plans/recommendations
- Curriculum Engine remains syllabus truth
- Models persist Twin projections and evidence — without becoming a second curriculum

---

# Recommendation Contract

Every recommendation emitted from Twin-consuming engines **must** include the following fields. Field names may vary in code; semantics must not.

| Field | Meaning |
|---|---|
| **Recommendation ID** | Stable identifier for Decision Journal accept/dismiss |
| **Topic** | Canonical curriculum topic (and section when V2); never an ad-hoc label |
| **Duration** | Suggested study duration for this action |
| **Priority** | Rank or priority band for the session/day |
| **Reasoning** | Human-readable and machine-readable reason codes (weight, overdue, gap, deadline, workload) |
| **Expected Benefit** | What Twin metric should improve (mastery, retention, coverage, readiness) |
| **Confidence** | Confidence in the recommendation given evidence density |
| **Dependencies** | Prerequisites or blocking reviews that should precede this action |
| **Alternative Recommendation** | Next-best option if dismissed (supports explainability “why not another?”) |
| **Expiry** | When this recommendation must be regenerated (time or Twin-version based) |

Recommendations are **derived from the Twin**. They are not stored as competing learner state. Accept/dismiss writes Behaviour evidence + Decision Journal entries only.

---

# Explainability Contract

Every user-facing recommendation must be able to answer all of the following. If an engine cannot answer one, the recommendation is not shippable in the core path.

| Question | Grounded in Twin / Curriculum |
|---|---|
| **Why this topic?** | Knowledge gap, Memory due, Performance weakness, and/or exam weight |
| **Why today?** | Deadline pressure, review schedule, plan slot, adherence catch-up, or mission capacity |
| **Why this duration?** | TimeEngine / availability, topic size, burnout guardrails, remaining daily capacity |
| **Why this priority?** | Relative urgency vs other candidates (weight × risk × due pressure × plan position) |
| **Why not another topic?** | Explicit comparison to Alternative Recommendation factors |
| **What is the expected benefit?** | Named Twin outcome (e.g. reduce pass-risk on Section X; clear overdue review) |

AI Coach narratives may *phrase* these answers but must cite the same underlying factors — not invent new ranking logic ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) AI Learning Coach pillar).

---

# Prediction Contract

Predictions are Twin outputs. The following capabilities are in-scope for the Twin architecture (delivery may be phased).

| Prediction | Description | Primary Twin inputs |
|---|---|---|
| **Pass probability** | Likelihood of passing the active sitting | Readiness, Knowledge (weighted), Performance (mocks), Goals time, Motivation |
| **Topic mastery forecast** | Expected mastery at a future date under current pace | Knowledge, Memory, Behaviour adherence, Planning |
| **Retention forecast** | Probability material remains recallable at sitting | Memory, Revision adherence, time-to-exam |
| **Completion forecast** | Likelihood of covering weighted syllabus in time | Planning, Knowledge coverage, Behaviour, Goals capacity |
| **Risk of burnout** | Probability of unsustainable intensity / dropout | Motivation, Behaviour volume, Mission load |
| **Risk of missing target date** | Probability goals’ sitting becomes unrealistic | Completion forecast, skip patterns, pace vs plan |
| **Expected readiness** | Forecast readiness score/band at sitting | Readiness trajectory, Predictions above |
| **Confidence interval** | Uncertainty band on any forecast | Evidence density, model calibration state |

### Prediction rules

1. Predictions **read Twin state**; they do not maintain a private learner model.
2. Each prediction exposes **as-of time**, **confidence interval**, and **top factors**.
3. Recalculation is triggered by material evidence or goal changes — not by UI page views alone.
4. Until calibrated on outcomes, products must present predictions as **estimates with uncertainty**, not guarantees.

---

# Subsystem Responsibilities

Subsystem names map to Kwalitec’s existing and planned engines/services. “Produces” means outputs for users or peers; “Updates” means Twin mutations via Evidence or derived Twin domains.

## Planning Engine

| | |
|---|---|
| **Consumes** | Goals, Knowledge, Memory, Behaviour adherence, Curriculum order/weights, Motivation guardrails |
| **Produces** | Derived study plan / week distribution; rebalance explanations |
| **Updates** | Planning domain (derived); may emit plan-slip evidence when rebalance follows skips |

See [study-planning.md](knowledge/subsystems/study-planning.md).

## Mission Engine

| | |
|---|---|
| **Consumes** | Planning, Knowledge, Memory (due reviews), Readiness urgency, Motivation / burnout, Goals capacity |
| **Produces** | Daily mission + prioritised tasks; task-level reasoning |
| **Updates** | Evidence on mission completion/skip; Behaviour; Planning progress flags |

See [missions.md](knowledge/subsystems/missions.md). Missions are optimizer outputs, not a second syllabus.

## Readiness Engine

| | |
|---|---|
| **Consumes** | Knowledge, Memory, Performance, Goals (time remaining), Planning pace, Curriculum weights |
| **Produces** | Readiness summary, risk concentration, sit/defer inputs |
| **Updates** | Readiness domain (derived view); feeds Predictions — does not invent coverage order |

See [readiness.md](knowledge/subsystems/readiness.md).

## Analytics

| | |
|---|---|
| **Consumes** | Twin domains + Evidence (same metric spine as Readiness) |
| **Produces** | Longitudinal views, heatmaps, consistency/accuracy trends |
| **Updates** | None to authoritative Twin beliefs — **read-only consumer** (may record view telemetry as Behaviour only if productised) |

See [analytics.md](knowledge/subsystems/analytics.md). Analytics must not fork readiness definitions.

## AI Coach

| | |
|---|---|
| **Consumes** | Twin state, Recommendations, Predictions, Decision Journal, Evidence summaries |
| **Produces** | Explanations, reflection prompts, debriefs, strategy dialogue |
| **Updates** | Optional reflection evidence (explicit user-confirmed); **must not** silently rewrite Knowledge or bypass Recommendation Contract |

Aligns with Phase 6 in [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md).

## Revision Engine

| | |
|---|---|
| **Consumes** | Memory due sets, Knowledge weak/high-weight gaps, Readiness risk, Goals time |
| **Produces** | Revision schedules and revision-focused recommendations |
| **Updates** | Revision evidence → Memory + Knowledge; Behaviour for revision adherence |

## Notifications

| | |
|---|---|
| **Consumes** | Recommendations (expiry), Memory due, Motivation burnout, Goals deadlines, Behaviour quiet hours |
| **Produces** | Timely prompts that reduce missed sessions without nagging into burnout |
| **Updates** | Notification engagement evidence (open/dismiss) → Behaviour |

## Recommendation Engine

| | |
|---|---|
| **Consumes** | Full Twin + Predictions + Curriculum |
| **Produces** | Recommendations satisfying Recommendation + Explainability contracts |
| **Updates** | Decision Journal + Behaviour on accept/dismiss; never stores a parallel mastery map |

## Adaptive Learning / Learning services (supporting)

| | |
|---|---|
| **Consumes** | Evidence stream, prior Knowledge/Memory |
| **Produces** | Mastery and review schedule updates |
| **Updates** | Knowledge, Memory, Performance via Evidence Model |

## Burnout Monitor

| | |
|---|---|
| **Consumes** | Behaviour, Motivation inputs, Mission load |
| **Produces** | Intensity flags for Missions, Planning, Notifications |
| **Updates** | Motivation domain |

---

# Architectural Rules

These rules are **non-negotiable** for Twin-related work.

1. **Exactly one Student Digital Twin per student.**  
   Multi-exam context is modelled inside Goals and scoped Knowledge — not duplicate Twins.

2. **No subsystem stores competing learning state.**  
   Caches must be invalidatable projections of the Twin. Forbidden: private mastery tables owned by Missions that diverge from Twin Knowledge.

3. **Recommendations are derived from the Twin.**  
   They obey the Recommendation and Explainability contracts.

4. **Predictions never bypass the Twin.**  
   No side-channel features that Twin domains do not contain.

5. **Evidence is immutable.**  
   Corrections are compensating events.

6. **Planning is always regenerable from current Twin state.**  
   Stale plans are refreshed; plans are not the source of truth for mastery.

7. **Curriculum identity is canonical.**  
   Topic ordering and coverage denominators use `CurriculumService` traversal helpers ([ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md)). V1 and V2 both remain valid ([ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md)).

8. **Deterministic cores stay deterministic.**  
   Planning, readiness, and recommendation math: same Twin snapshot + curriculum → same outputs ([`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)).

9. **Service layer owns Twin logic.**  
   Blueprints do not compute Twin updates ([ADR-001](knowledge/architecture/ADR-001-service-layer.md), [ADR-002](knowledge/architecture/ADR-002-blueprint-architecture.md)).

10. **AI cannot invent syllabus order or hide scoring.**  
    Assistive only ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)).

11. **Readiness definitions have a single owner.**  
    Analytics and dashboards consume Readiness Engine outputs.

12. **Security and tenancy.**  
    Twin reads/writes are scoped to the authenticated user; no cross-student Twin leakage ([`.cursor/rules/10-security.mdc`](.cursor/rules/10-security.mdc)).

---

# Future Evolution

The Twin is designed to grow without breaking its role as single learner-state authority.

| Evolution | Twin impact |
|---|---|
| **Learning styles / preferences** | Behaviour + Goals preference slices; never replace evidence-based Knowledge |
| **Institution insights** | Read-only cohort projections for coaches; student Twin remains student-owned (Phase 7) |
| **Collaboration** | Optional Behaviour evidence from study groups; Knowledge remains individual |
| **AI tutor** | Consumes Twin; may propose practice; assessed results enter Evidence Model |
| **Career planning** | Extended Goals beyond single sittings; multi-paper Knowledge portfolio |
| **Benchmarking** | Privacy-preserving aggregates; Predictions may include relative bands without exposing peers |
| **Multi-exam support** | Multiple Goals + capacity budget inside one Twin |
| **Richer question banks** | Performance/Memory at objective and item grain |
| **Outcome calibration** | Post-exam evidence improves Prediction Contract quality |

Non-goals remain those in [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md): no black-box path ownership, no parallel syllabus invention, no vanity-metric-driven Twin mutations.

---

# Diagrams

## 1. Digital Twin architecture

```
                    ┌────────────────────────────┐
                    │     Curriculum Engine       │
                    │  (syllabus truth V1 / V2)   │
                    └─────────────┬──────────────┘
                                  │ references
┌─────────────────────────────────▼──────────────────────────────────┐
│                     Student Digital Twin                            │
│  Identity · Goals · Knowledge · Memory · Behaviour · Performance    │
│  Planning(derived) · Readiness(derived) · Motivation · Predictions│
│                         ▲                                           │
│                         │ evidence                                  │
│                  ┌──────┴───────┐                                   │
│                  │ Evidence Log │                                   │
│                  └──────▲───────┘                                   │
└─────────────────────────┼──────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   Planning Eng.    Mission Eng.     Readiness Eng.
        │                 │                 │
        └────────────┬────┴────┬────────────┘
                     ▼         ▼
              Recommend.    Analytics
                     │
                     ▼
                 AI Coach / Notifications / Revision
```

## 2. Learning loop

```
          ┌──────────────┐
          │   Mission /  │
          │  Recommendation
          └──────┬───────┘
                 │ act
                 ▼
          ┌──────────────┐
          │   Evidence   │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │     Twin     │
          └──────┬───────┘
                 │
         ┌───────┴───────┐
         ▼               ▼
   Predictions     Readiness
         │               │
         └───────┬───────┘
                 ▼
          Recommendations
                 │
                 └──────► (loop)
```

## 3. Evidence flow

```
Session / Answer / Quiz / Mock / Mission / Revision / Skip / Confidence / Time
                                      │
                                      ▼
                         ┌────────────────────┐
                         │  Append Evidence    │
                         └─────────┬──────────┘
                                   │
           ┌───────────┬───────────┼───────────┬───────────┐
           ▼           ▼           ▼           ▼           ▼
      Knowledge     Memory    Behaviour  Performance  Motivation
           │           │           │           │           │
           └───────────┴───────────┴─────┬─────┴───────────┘
                                         ▼
                              Readiness / Planning (recompute)
                                         ▼
                                   Predictions
```

## 4. Recommendation flow

```
Twin snapshot + Curriculum weights/order + Predictions
                        │
                        ▼
              Recommendation Engine
                        │
                        ├─► Recommendation Contract fields
                        ├─► Explainability answers
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
     Mission Engine            Notifications
            │                       │
            ▼                       ▼
     Student decision ──► Decision Journal + Behaviour evidence
```

## 5. Subsystem interaction

```
                 ┌────────── Twin ──────────┐
                 │                          │
    Planning ◄───┤                          ├──► Readiness
                 │                          │
    Missions ◄───┤                          ├──► Predictions
                 │                          │
    Revision ◄───┤                          ├──► Analytics (RO)
                 │                          │
 Notifications ◄─┤                          ├──► AI Coach (RO+)
                 │                          │
                 └──────────▲───────────────┘
                            │
                     Evidence writers
            (Learning, Missions, Wizard, Settings)
```

---

# Quality Expectations

This specification is an enterprise architecture artefact for Kwalitec’s Student Intelligence Platform.

**Authors and implementers must:**

- Prefer Kwalitec terminology from the [glossary](knowledge/development/glossary.md)
- Cross-check product intent against [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)
- Cross-check layering against [`ARCHITECTURE.md`](ARCHITECTURE.md) and ADRs under [`knowledge/architecture/`](knowledge/architecture/)
- Keep V1/V2 curriculum compatibility explicit in Twin Knowledge design
- Treat explainability and determinism as acceptance criteria, not polish

**Authors and implementers must not:**

- Treat this document as permission to redesign the database in the same milestone
- Introduce LLM calls into core Twin update or recommendation paths
- Equate “study plan rows” with the Digital Twin
- Dilute Twin authority by letting Analytics or AI Coach define mastery privately

---

# Related documents

| Document | Relationship |
|---|---|
| [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) | Product vision, principles, pillars, AI Coach non-goals |
| [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) | Engineering orientation, service map, deterministic thesis |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layering, curriculum engine, service dependency flow |
| [`knowledge/README.md`](knowledge/README.md) | Knowledge base index |
| [ADR-001](knowledge/architecture/ADR-001-service-layer.md) | Business logic in services |
| [ADR-002](knowledge/architecture/ADR-002-blueprint-architecture.md) | Thin HTTP blueprints |
| [ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md) | Dual curriculum formats |
| [ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md) | Single topic ordering path |
| [ADR-005](knowledge/architecture/ADR-005-testing-strategy.md) | Test expectations for future Twin implementation |
| Subsystem docs | [study-planning](knowledge/subsystems/study-planning.md), [missions](knowledge/subsystems/missions.md), [readiness](knowledge/subsystems/readiness.md), [analytics](knowledge/subsystems/analytics.md) |

---

# Document governance

- **Canonical for:** Student Digital Twin conceptual model and intelligence contracts  
- **Not canonical for:** ORM schema, HTTP APIs, or scoring formula coefficients  
- Conflicts with Core Product Principles in [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) are resolved in favour of the blueprint unless this document is explicitly revised  
- Future Epic 0 capabilities and implementation milestones must cite this document and preserve its architectural rules  

---

*End of Student Digital Twin specification — Epic 0 / Capability 0.1*
