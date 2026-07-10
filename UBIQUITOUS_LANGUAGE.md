# Ubiquitous Language

**Status:** Canonical domain language specification  
**Epic:** Epic 0 – Student Intelligence Platform  
**Capability:** 0.3 – Define the Ubiquitous Language  
**Audience:** Product, engineering, design, AI agents, documentation authors  
**Scope:** Shared meaning of core business concepts — not a database schema and not an implementation guide  
**Companion docs:** [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](LEARNING_EVIDENCE_MODEL.md), [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md), [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`knowledge/development/glossary.md`](knowledge/development/glossary.md)

---

# Introduction

Kwalitec is a commercial adaptive learning product. Its intelligence — planning, missions, readiness, recommendations, predictions — only works if every participant means the same thing by the same words.

A **ubiquitous language** is the shared vocabulary of the domain. It binds product intent to engineering reality. Without it, “mastery” becomes a progress bar in one place and a spaced-repetition score in another; “mission” means a daily plan to product and a database row to engineering; “student model” and “digital twin” compete as if they were different systems.

This document is the **canonical domain language for Kwalitec**. Every specification, service, API, UI label, AI agent prompt, ADR, milestone brief, and completion report should use these definitions consistently. When code or docs invent a synonym, the canonical term in this document wins.

**Rules of use**

1. Prefer the **canonical term** over colloquial alternatives (see [Canonical Terminology](#canonical-terminology)).
2. Do not invent parallel meanings for Twin, Evidence, Curriculum, or Recommendation concepts.
3. If a new concept is needed, add it here (or in a companion Epic 0 domain spec) before it spreads through code and UI.
4. Implementation names (classes, columns, routes) should map clearly to these concepts — see [Naming Standards](#naming-standards).

**Non-goals of this document**

- Table designs, Alembic revisions, or ORM layouts
- API contracts or HTTP route catalogues
- Scoring formulas, ML model choices, or UI copy style guides beyond term choice
- Replacement of [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) or [`LEARNING_EVIDENCE_MODEL.md`](LEARNING_EVIDENCE_MODEL.md) as deeper domain architecture

---

# Core Domain Concepts

For each concept: **Definition**, **Purpose**, **Examples**, **Related Concepts**, **Common Misunderstandings**.

---

## Student

**Definition**  
A person preparing for a professional examination who has a Kwalitec account and exactly one Student Digital Twin. “Student” is the domain role; authentication identity (User) is the security/account binding.

**Purpose**  
Anchor all personal learning state, evidence, goals, plans, and recommendations to a single learner without conflating login mechanics with exam-preparation intelligence.

**Examples**  
- An IFoA CS1 candidate studying for the April sitting.  
- A re-sitter whose Twin preserves historical Learning Evidence while Goals target a new sitting.

**Related Concepts**  
Digital Twin, Goal, Target Sitting, Learning Evidence, Identity (Twin domain)

**Common Misunderstandings**  
- Student ≠ anonymous browser session.  
- Student ≠ institution cohort member (institutions may observe; the Twin remains student-owned).  
- Creating a second Twin for a second paper is wrong — multi-exam context lives inside one Twin via Goals.

---

## Curriculum

**Definition**  
The official syllabus for an organisation, paper, and syllabus version — the shared source of truth for structure, ordering, and exam weighting. Exists as curriculum JSON / Curriculum Engine definitions and as imported persistence; it is not per-student.

**Purpose**  
Ensure coverage, planning, readiness, and recommendations map to the real exam syllabus (V1 flat or V2 hierarchical), never to an invented parallel topic tree.

**Examples**  
- IFoA CS1 syllabus version 2026 loaded from `app/curriculum/data/`.  
- A V2 curriculum with sections carrying exam weights and nested topics.

**Related Concepts**  
Section, Topic, Learning Objective, Exam Weighting, Prerequisite, Dependency, Canonical Traversal

**Common Misunderstandings**  
- Curriculum is not a Study Plan.  
- Curriculum is not the Digital Twin.  
- Importing curriculum into the database does not make ORM rows a second syllabus authority — the engine + official JSON remain syllabus truth; DB is the operational projection.

---

## Section

**Definition**  
A top-level grouping within a Curriculum V2 hierarchy (e.g. syllabus part). Sections are ordered and typically carry Exam Weighting. Pure V1 curricula may have no sections.

**Purpose**  
Preserve official syllabus structure for weighted coverage, readiness risk concentration, and navigation — especially where exam marks attach at section level.

**Examples**  
- CS1 Section A “Data analysis” with a stated exam weight.  
- A readiness narrative: “Pass risk concentrated in Section C.”

**Related Concepts**  
Curriculum, Topic, Exam Weighting, Readiness

**Common Misunderstandings**  
- Section ≠ Topic. Topics sit under sections in V2.  
- Absence of sections in V1 does not mean the curriculum is invalid — V1 remains loadable and traversable.  
- Do not invent sections in the Twin; reference curriculum identity only.

---

## Topic

**Definition**  
A study unit within a Curriculum — the primary grain for planning, missions, mastery, and recommendations. In V2, a topic belongs to a Section; in V1, topics may form a flatter or parent-linked structure. Ordering must use canonical Curriculum Service traversal.

**Purpose**  
Give planners and recommenders a stable unit of work that maps to official syllabus identity.

**Examples**  
- Topic “Hypothesis testing” scheduled in this week’s Adaptive Plan.  
- A Recommendation naming a canonical topic ID, not a free-text label.

**Related Concepts**  
Section, Learning Objective, Mastery, Prerequisite, Difficulty, Mission, Recommendation

**Common Misunderstandings**  
- Topic completion ≠ Mastery.  
- UI labels must not invent topics outside curriculum identity.  
- Engine `Topic` / `TopicDefinition` and ORM `Topic` are related projections of the same domain concept — do not treat them as unrelated entities.

---

## Learning Objective

**Definition**  
The finest official syllabus leaf describing what the candidate must be able to do. V1 materials often say “learning outcome”; the canonical product term is **Learning Objective** (imported as such). Topics group one or more objectives.

**Purpose**  
Support fine-grained assessment mapping, future objective-level Mastery, and explainable gaps beneath a topic.

**Examples**  
- “Calculate and interpret a confidence interval for a mean.”  
- A quiz item tagged to a specific Learning Objective under a Topic.

**Related Concepts**  
Topic, Section, Curriculum, Diagnostic Assessment, Learning Evidence

**Common Misunderstandings**  
- Learning Objective ≠ Mission task text.  
- “Learning outcome” in legacy V1 JSON is the same concept — prefer Learning Objective in new specs and UI.  
- Objectives are curriculum truth, not Twin-invented skills.

---

## Prerequisite

**Definition**  
A curriculum-declared requirement that one Topic (or Learning Objective) should be understood before another. Prerequisites constrain ordering and Recommendation Dependencies; they are syllabus structure, not Twin state.

**Purpose**  
Prevent plans and recommendations from asking students to study advanced material before foundational material when the official syllabus (or product rules derived from it) requires sequence.

**Examples**  
- “Regression” listed as prerequisite to “Generalised linear models.”  
- A Recommendation Dependency that blocks Topic B until Topic A’s Knowledge State is adequate.

**Related Concepts**  
Dependency, Topic, Adaptive Plan, Recommendation, Knowledge State

**Common Misunderstandings**  
- Prerequisite ≠ soft preference (“students often study X first”).  
- Twin Mastery does not create prerequisites; it only reports readiness against them.  
- Missing prerequisite data must not be invented by AI Coach.

---

## Study Session

**Definition**  
A bounded block of learning activity in which the student engages with syllabus content (often topic-scoped), with start/end (or completion) recorded as Learning Evidence. Distinct from a Revision Session by intent: first-pass or planned learning vs deliberate review.

**Purpose**  
Capture effort, adherence, and exposure for Behaviour and Planning realism; optionally lightly reinforce Memory when topic-tagged. Alone, it is weak evidence of Mastery.

**Examples**  
- A 45-minute block on “Hypothesis testing” from today’s Mission.  
- A Study Session abandoned mid-way (still evidence — Session Abandoned / skip patterns).

**Related Concepts**  
Revision Session, Learning Event, Learning Evidence, Mission, Behaviour, Available Study Time

**Common Misunderstandings**  
- Completing a Study Session ≠ Mastery.  
- Study Session ≠ Mission (a Mission may contain one or more sessions/tasks).  
- Time on task alone does not prove Knowledge.

---

## Revision Session

**Definition**  
A bounded block of deliberate review and spaced reinforcement — clearing overdue material, flashcard review, or weight-aware weak-area revision — recorded as Revision-category Learning Evidence.

**Purpose**  
Counter memory decay, update Retention / Memory Strength, and feed the Revision Engine and retention forecasts.

**Examples**  
- Clearing three overdue topics before the mock.  
- A flashcard review set generated from Memory due dates.

**Related Concepts**  
Study Session, Retention, Memory Strength, Learning Evidence, Recommendation

**Common Misunderstandings**  
- Revision Session ≠ first exposure to a Topic.  
- Revision completion ≠ permanent Mastery; Retention still decays.  
- “Review” in UI should map to Revision Session when the intent is spaced reinforcement.

---

## Learning Event

**Definition**  
A discrete occurrence in the learning journey (student action or material system transition) that is a candidate to become Learning Evidence — e.g. answering a question, completing a mission, skipping a session, changing an exam date.

**Purpose**  
Name the moment something happened, before or as it is validated and stored as immutable Learning Evidence.

**Examples**  
- Student submits a quiz.  
- System marks a Mission as expired uncompleted.  
- Student dismisses a Recommendation.

**Related Concepts**  
Learning Evidence, Evidence Source, Behaviour, Mission Completion, Mission Failure

**Common Misunderstandings**  
- Learning Event ≠ Learning Evidence until it is attributable, validated, and recorded per the Evidence Model.  
- Not every UI click is a Learning Event — only interactions that can change how Kwalitec understands the learner.  
- Events are not Twin state; they feed the evidence log that updates the Twin.

---

## Learning Evidence

**Definition**  
Kwalitec’s immutable, attributable record of what a student did, achieved, skipped, reported, or experienced. It is the only legitimate input that may change Twin beliefs. Full catalogue and rules live in [`LEARNING_EVIDENCE_MODEL.md`](LEARNING_EVIDENCE_MODEL.md).

**Purpose**  
Provide an append-only audit spine so Mastery, Behaviour, Predictions, and Recommendations remain explainable and reproducible.

**Examples**  
- Question Correct mapped to a Learning Objective.  
- Mission Completed with task-level outcomes.  
- Confidence Rating tagged `self_report`.  
- Compensating evidence voiding a mis-attributed attempt.

**Related Concepts**  
Learning Event, Evidence Source, Digital Twin, Mastery, Confidence, Recommendation Reason

**Common Misunderstandings**  
- Learning Evidence ≠ “learning data” dump or analytics warehouse extract.  
- Evidence is never edited in place; corrections are new compensating records.  
- Analytics may read evidence; it must not invent evidence or fork Twin beliefs.

---

## Evidence Source

**Definition**  
The producer or provenance of a Learning Evidence record — which subsystem or channel created it (e.g. Missions, Questions, Revision Engine, Manual Updates, System Events) and whether provenance is user action vs system-inferred.

**Purpose**  
Support attribution, quality weighting, privacy boundaries, and explainability (“this mastery change came from a mock, not a self-rating”).

**Examples**  
- Source: Quiz flow; provenance: user.  
- Source: Mission Engine; provenance: system (mission expired).  
- Source: Manual Updates; type: Confidence Rating.

**Related Concepts**  
Learning Evidence, Learning Event, Confidence, Insight

**Common Misunderstandings**  
- Evidence Source ≠ curriculum identity.  
- AI Coach is not allowed to be a silent Evidence Source for Knowledge mutations.  
- “Source” in logging must not be confused with Evidence Source in the domain model.

---

## Mastery

**Definition**  
A probabilistic belief about how well the student can perform a curriculum entity (typically Topic; eventually Learning Objective) *now*, updated from Learning Evidence. Mastery is a Twin Knowledge-domain estimate, not a binary badge.

**Purpose**  
Drive gap detection, Adaptive Plans, Recommendations, and weighted coverage for Readiness.

**Examples**  
- High Mastery on “Descriptive statistics” after dense correct practice.  
- Low Mastery with low Confidence after cold start without Diagnostic Assessment.

**Related Concepts**  
Confidence, Knowledge State, Retention, Memory Strength, Learning Evidence, Readiness

**Common Misunderstandings**  
- Mastery ≠ Mission Completion.  
- Mastery ≠ time spent.  
- Mastery ≠ Retention (can do it now vs will still recall at sitting).  
- Do not call this “Knowledge Score” or “progress %” in core specs.

---

## Confidence

**Definition**  
A measure of certainty attached to a belief or output. In Twin/Evidence contexts: (1) confidence in a Mastery / Retention / Prediction estimate given evidence density and quality; (2) self-reported Confidence Ratings as Learning Evidence; (3) Recommendation Confidence in a suggested action. Always disambiguate which kind is meant in technical writing.

**Purpose**  
Prevent over-trust in sparse or self-reported signals; surface uncertainty to students and engines.

**Examples**  
- Low Confidence on Mastery after a single Study Session.  
- Recommendation Confidence reduced when Evidence Source is mostly self-report.  
- Student Confidence Rating “3/5” on a topic before a quiz.

**Related Concepts**  
Mastery, Recommendation Confidence, Learning Evidence, Prediction, Insight

**Common Misunderstandings**  
- Confidence ≠ Mastery level (a student can be confidently wrong).  
- Self-report Confidence must not override dense contrary Assessment evidence.  
- UI “confidence” without qualifier is ambiguous — specify Twin confidence vs self-report vs recommendation confidence.

---

## Retention

**Definition**  
An estimate of whether demonstrated knowledge remains recallable over time — the Memory-domain counterpart to Mastery. Retention decays without reinforcement and recovers with Revision Sessions and successful review evidence.

**Purpose**  
Schedule revision, explain overdue pressure, and feed retention forecasts and Readiness durability narratives.

**Examples**  
- Topic mastered last month now due for review.  
- Retention forecast falling as sitting approaches without Revision Sessions.

**Related Concepts**  
Memory Strength, Mastery, Revision Session, Prediction, Readiness

**Common Misunderstandings**  
- Retention ≠ Mastery.  
- High past quiz scores do not freeze Retention forever.  
- Retention is not a content library feature; it is learner-state belief.

---

## Memory Strength

**Definition**  
The Memory-domain estimate of how strongly a curriculum unit is encoded for recall — informed by success/failure of reviews, time since reinforcement, and evidence density. Closely related to Retention; Memory Strength emphasises the scheduling/strength signal used by spaced review.

**Purpose**  
Drive due/overdue sets for Missions and Recommendations and parameterise decay/recovery.

**Examples**  
- Memory Strength drops after weeks without review.  
- Successful Revision Session increases Memory Strength for tagged topics.

**Related Concepts**  
Retention, Revision Session, Mastery, Learning Evidence

**Common Misunderstandings**  
- Memory Strength ≠ Mastery of first-pass learning.  
- Memory Strength ≠ raw streak length.  
- Do not store a competing “review score” outside the Twin Memory domain.

---

## Knowledge State

**Definition**  
The Twin’s current picture of what the student knows across curriculum entities — the Knowledge-domain aggregate including Mastery beliefs, coverage/exposure flags, evidence strength, and gaps vs Exam Weighting.

**Purpose**  
Provide a coherent input to Planning, Missions, Readiness, Recommendations, and Predictions.

**Examples**  
- Knowledge State after Diagnostic Assessment establishes baseline Mastery map.  
- Knowledge State showing high-weight Section weak despite many Study Sessions.

**Related Concepts**  
Mastery, Confidence, Learning State, Digital Twin, Curriculum, Coverage (derived)

**Common Misunderstandings**  
- Knowledge State ≠ Curriculum.  
- Knowledge State ≠ Adaptive Plan.  
- Updating a dashboard cache does not update Knowledge State — only evidence-driven Twin updates do.

---

## Learning Velocity

**Definition**  
A Behaviour / Performance-derived measure of how quickly the student is acquiring coverage and Mastery relative to time invested and plan pace (e.g. topics strengthened per week, weighted coverage gain vs hours).

**Purpose**  
Inform Predictions (completion and pass risk), Planning rebalance, and Insights about whether current intensity is sufficient for the Target Sitting.

**Examples**  
- Velocity too low to finish weighted syllabus before the sitting.  
- Velocity spike followed by Burnout risk — Consistency matters more than short bursts.

**Related Concepts**  
Behaviour, Consistency, Available Study Time, Prediction, Adaptive Plan, Readiness

**Common Misunderstandings**  
- Learning Velocity ≠ hours logged alone.  
- Faster velocity is not always better if Motivation / burnout signals rise.  
- Velocity is derived intelligence, not a second Mastery store.

---

## Recommendation

**Definition**  
A deterministic, explainable suggestion for what the student should do next (typically a Topic, duration, and priority), derived from Digital Twin state + Curriculum + Predictions. Recommendations obey the Recommendation and Explainability contracts in [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md).

**Purpose**  
Reduce daily decision load while keeping “why this?” inspectable.

**Examples**  
- “Study Topic X for 40 minutes — high exam weight, overdue review, coverage gap.”  
- Alternative Recommendation offered when the primary is dismissed.

**Related Concepts**  
Recommendation Reason, Recommendation Confidence, Recommendation Priority, Mission, Digital Twin, Decision Journal

**Common Misunderstandings**  
- Recommendation ≠ Mission (missions package daily work; recommendations are the ranked next-action intelligence).  
- Recommendations are not authoritative learner state; accept/dismiss writes Behaviour evidence only.  
- Generative AI may phrase a Recommendation; it must not invent ranking factors.

---

## Recommendation Reason

**Definition**  
The human-readable and machine-readable justification for a Recommendation — factor codes such as exam weight, overdue review, coverage gap, deadline pressure, workload, prerequisite blocking, or burnout guardrail.

**Purpose**  
Satisfy explainability: every recommendation must answer why this topic, why today, why this duration, why this priority, and why not another.

**Examples**  
- Reason codes: `exam_weight`, `memory_overdue`, `deadline_pressure`.  
- Narrative: “Section B is 20% of the exam and your Retention is decaying.”

**Related Concepts**  
Recommendation, Recommendation Confidence, Insight, Learning Evidence, Exam Weighting

**Common Misunderstandings**  
- A vague slogan (“because it’s important”) is not a Recommendation Reason.  
- AI Coach copy must cite the same factors — not a new private rationale.  
- Reason ≠ Priority (reason explains; priority ranks).

---

## Recommendation Confidence

**Definition**  
Confidence that this Recommendation is appropriate given Twin evidence density, quality, and prediction uncertainty — distinct from the student’s self-reported Confidence and from Mastery level.

**Purpose**  
Allow the product to prefer high-evidence suggestions, surface uncertainty, and avoid brittle cold-start directives.

**Examples**  
- High Recommendation Confidence after dense Assessment evidence on weak high-weight topics.  
- Low Recommendation Confidence when Knowledge State is mostly self-report.

**Related Concepts**  
Recommendation, Confidence, Recommendation Reason, Learning Evidence

**Common Misunderstandings**  
- Recommendation Confidence ≠ “how sure the student feels.”  
- Low confidence should not be hidden behind assertive UI.  
- Confidence is not a substitute for Recommendation Reason.

---

## Recommendation Priority

**Definition**  
The relative rank or priority band of a Recommendation within a session or day — reflecting urgency from weight, risk, due pressure, plan position, and capacity constraints.

**Purpose**  
Order work so the Mission Optimizer and daily UI present the most consequential actions first without overwhelming the student.

**Examples**  
- Priority 1: overdue high-weight revision.  
- Lower priority: low-weight new topic when burnout guardrails are active.

**Related Concepts**  
Recommendation, Mission, Readiness, Available Study Time, Consistency

**Common Misunderstandings**  
- Priority ≠ Difficulty.  
- Priority ≠ Mastery (low mastery may be low priority if weight and deadline say otherwise).  
- Manual reordering in UI does not redefine the engine’s Recommendation Priority unless recorded as preference evidence.

---

## Mission

**Definition**  
A day’s (or session’s) set of prioritised learning tasks for the student — derived from Planning, Twin state, and optimization — not a second syllabus. Produced conceptually by the Mission Engine / Mission Optimizer.

**Purpose**  
Give every study day a clear, finite unit of progress: learn / review / consolidate with purpose.

**Examples**  
- Today’s Mission: two Study Session tasks and one Revision Session task.  
- Mission tasks each cite canonical Topic identity and reasoning.

**Related Concepts**  
Mission Completion, Mission Failure, Recommendation, Adaptive Plan, Study Session, Available Study Time

**Common Misunderstandings**  
- Mission ≠ Curriculum.  
- Mission ≠ Digital Twin.  
- Finishing a Mission ≠ Mastery unless tasks include assessed Learning Evidence.

---

## Mission Completion

**Definition**  
The Learning Event / Evidence that the student finished the Mission’s required tasks for that period. Updates Behaviour adherence and Planning progress; does not by itself rewrite Mastery.

**Purpose**  
Measure plan adherence and Consistency; trigger catch-up logic when missing.

**Examples**  
- All mission tasks marked done before end of day.  
- Partial completion recorded distinctly from full Mission Completion.

**Related Concepts**  
Mission, Mission Failure, Behaviour, Consistency, Learning Evidence

**Common Misunderstandings**  
- Mission Completion ≠ exam readiness.  
- Mission Completion ≠ all topics mastered.  
- System auto-complete without student action is not Mission Completion.

---

## Mission Failure

**Definition**  
The Learning Event / Evidence that a Mission was missed, expired uncompleted, abandoned, or explicitly failed against its success criteria. Includes patterns such as Mission Missed in the Evidence catalogue.

**Purpose**  
Feed Behaviour, Motivation / burnout interpretation, Planning slip, and rebalance — without falsely reducing Mastery.

**Examples**  
- Mission expired at midnight with tasks incomplete.  
- Student abandons mid-mission repeatedly on Fridays.

**Related Concepts**  
Mission, Mission Completion, Behaviour, Recovery Plan, Consistency, Skipped Session

**Common Misunderstandings**  
- Mission Failure ≠ low Mastery.  
- One failure ≠ burnout; patterns matter.  
- Do not delete Twin history because of Mission Failure.

---

## Readiness

**Definition**  
An explainable estimate of exam preparedness for the active Goal / Target Sitting — combining weighted coverage, pace vs time remaining, Memory durability, Performance, and risk concentration. Owned by the Readiness Engine; Analytics consumes and must not redefine it.

**Purpose**  
Answer “Am I on track?” and “Where is pass risk concentrated?” with inspectable factors.

**Examples**  
- Readiness summary: strong coverage but Retention risk on high-weight Section C.  
- Sit/defer narrative inputs derived from Readiness + Predictions.

**Related Concepts**  
Projected Pass Probability, Prediction, Knowledge State, Exam Weighting, Goal, Insight

**Common Misunderstandings**  
- Readiness ≠ vanity progress bar of missions completed.  
- Readiness ≠ Mastery of a single topic.  
- Dashboards must not fork a second readiness formula.

---

## Projected Pass Probability

**Definition**  
A Prediction estimating the likelihood of passing the active Target Sitting, derived only from Twin state (Readiness, weighted Knowledge, Performance including mocks, Goals/time, Motivation). Presented with uncertainty until calibrated on outcomes.

**Purpose**  
Make pass probability the north-star forecast students and product can reason about — never a guarantee.

**Examples**  
- Pass probability band with Confidence interval and top factors.  
- Drop in Projected Pass Probability after sustained Mission Failure and skipped Revision Sessions.

**Related Concepts**  
Prediction, Readiness, Confidence, Target Sitting, Insight

**Common Misunderstandings**  
- Projected Pass Probability ≠ marketing claim.  
- It must not bypass the Twin or use side-channel features Twin domains lack.  
- A single mock score is not the whole probability.

---

## Prediction

**Definition**  
A forward-looking Twin output (pass probability, mastery/retention/completion forecasts, burnout risk, expected readiness, etc.) with as-of time, Confidence interval, and top factors. Predictions are strictly downstream of Twin state.

**Purpose**  
Support planning urgency, coaching, and honest risk communication as evidence accumulates.

**Examples**  
- Retention forecast at sitting date.  
- Risk of missing Target Sitting given Learning Velocity and Available Study Time.

**Related Concepts**  
Projected Pass Probability, Confidence, Digital Twin, Recommendation, Insight

**Common Misunderstandings**  
- Prediction ≠ Recommendation (forecast vs suggested action).  
- Predictions do not maintain a private learner model.  
- UI page views alone should not recalculate Predictions.

---

## Insight

**Definition**  
An explainable, student-facing interpretation derived from Twin state, Learning Evidence, and Predictions — highlighting patterns, risks, or opportunities (e.g. Consistency drop, high-weight weakness, calibration gap between self-report and Performance).

**Purpose**  
Turn raw metrics into actionable understanding without opaque AI theatre; AI Coach may narrate Insights but must cite Twin factors.

**Examples**  
- “You skip Friday revision; Retention on Section B is sliding.”  
- “Self-reported Confidence exceeds assessed Performance on Topic X.”

**Related Concepts**  
Recommendation Reason, Behaviour, Consistency, Readiness, Reflection

**Common Misunderstandings**  
- Insight ≠ raw chart without interpretation contract.  
- Insight ≠ silent Twin mutation.  
- Insights must not invent syllabus structure.

---

## Behaviour

**Definition**  
The Twin domain capturing how the student actually studies — session cadence, completion rates, skips, preference signals (accept/dismiss), planned vs actual adherence.

**Purpose**  
Make plans realistic, detect burnout risk, personalise timing, and improve Predictions of completion.

**Examples**  
- Chronic postponement of Revision Sessions.  
- High accept rate for short morning Missions.

**Related Concepts**  
Consistency, Learning Velocity, Mission Completion, Mission Failure, Motivation, Learning Evidence

**Common Misunderstandings**  
- Behaviour ≠ Mastery.  
- Good Behaviour streaks do not replace Assessment evidence.  
- Behaviour is not a personality quiz result.

---

## Consistency

**Definition**  
A Behaviour-derived quality of sustainable, regular engagement over time — adherence without destructive overwork. Distinct from raw streak length or short Learning Velocity spikes.

**Purpose**  
Protect sustainable intensity; inform Motivation, Recovery Plans, and Predictions about durable progress.

**Examples**  
- Steady five-day study rhythm within Available Study Time.  
- Inconsistency: alternating overwork weekends and abandoned weeks.

**Related Concepts**  
Behaviour, Learning Velocity, Mission Completion, Recovery Plan, Motivation

**Common Misunderstandings**  
- Consistency ≠ longest streak badge.  
- Consistency ≠ maximum hours.  
- Unsustainable streaks are product failures, not wins.

---

## Digital Twin

**Definition**  
Kwalitec’s single authoritative representation of a learner’s exam-preparation state — the Student Digital Twin. A living, evidence-backed model of who the student is relative to a syllabus and a sitting. Full architecture: [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md).

**Purpose**  
Centralise Knowledge, Memory, Behaviour, Performance, Goals, Planning (derived), Readiness (derived), Motivation, and Predictions so every intelligent subsystem shares one learner-state authority.

**Examples**  
- Twin updated after mock exam Learning Evidence.  
- Adaptive Plan regenerated from current Twin + Curriculum + Available Study Time.

**Related Concepts**  
Student, Learning State, Knowledge State, Learning Evidence, Curriculum, Recommendation

**Common Misunderstandings**  
- Digital Twin ≠ Study Plan.  
- Digital Twin ≠ “Student Model” as a competing synonym in specs — use Digital Twin.  
- Exactly one Twin per student; not one Twin per paper.

---

## Learning State

**Definition**  
The holistic, current condition of the learner’s preparation as held by the Digital Twin — encompassing Knowledge State, Memory/Retention, Behaviour, Performance, Motivation, Goals, and derived Readiness/Planning views. Broader than Knowledge State alone.

**Purpose**  
Name “where the student is” as a whole when subsystems consume the Twin snapshot for decisions.

**Examples**  
- Learning State at cold start: Goals set, Knowledge Confidence low.  
- Learning State pre-sitting: high weighted Mastery, mixed Retention, stable Consistency.

**Related Concepts**  
Digital Twin, Knowledge State, Readiness, Goal, Prediction

**Common Misunderstandings**  
- Learning State ≠ a single scalar.  
- Learning State ≠ UI dashboard cache.  
- Do not maintain a second Learning State outside the Twin.

---

## Diagnostic Assessment

**Definition**  
An Assessment-category evaluation used especially at Twin birth, reset, or re-sit repositioning to establish an initial Knowledge State (and related Confidence). Recorded as Learning Evidence.

**Purpose**  
Improve cold-start quality so Adaptive Plans and Recommendations are not pure guesswork.

**Examples**  
- Placement-style diagnostic after exam selection.  
- Re-diagnostic before building a Recovery Plan for a re-sit.

**Related Concepts**  
Learning Evidence, Knowledge State, Mastery, Adaptive Plan, Goal

**Common Misunderstandings**  
- Diagnostic Assessment ≠ mock exam (mocks are exam-condition rehearsal; diagnostics bootstrap position).  
- Skipping diagnostic is allowed but must mark Knowledge Confidence low.  
- Diagnostic results are evidence, not permanent labels.

---

## Adaptive Plan

**Definition**  
A regenerable study schedule derived from Digital Twin + Curriculum + constraints (Available Study Time, Target Sitting, Motivation guardrails). Planning is a consequence of intelligence, not the authoritative learner model. Includes catch-up and intensity modes as Twin/Planning domain flags.

**Purpose**  
Fit the official syllabus into the student’s real life and rebalance when evidence, calendar, or capacity change.

**Examples**  
- Week distribution of topics regenerated after illness skip pattern.  
- Plan hash/version for deterministic regeneration.

**Related Concepts**  
Recovery Plan, Goal, Available Study Time, Mission, Curriculum, Digital Twin

**Common Misunderstandings**  
- Adaptive Plan ≠ Digital Twin.  
- Stale week grids must not override Twin Knowledge.  
- “Study Plan” in product language maps to Adaptive Plan / Planning artefacts — prefer Adaptive Plan when emphasising regenerable intelligence.

---

## Recovery Plan

**Definition**  
A specialised Adaptive Plan mode focused on catch-up after Mission Failure, illness, burnout, or failed sitting — prioritising high-weight gaps, overdue Retention, and sustainable intensity over vanity coverage.

**Purpose**  
Restore realistic path-to-ready without punishing the student with unsustainable load.

**Examples**  
- Post-burnout week with reduced Mission load and Revision-first priorities.  
- Re-sit Recovery Plan preserving historical Learning Evidence while resetting Planning.

**Related Concepts**  
Adaptive Plan, Mission Failure, Consistency, Motivation, Target Sitting, Reflection

**Common Misunderstandings**  
- Recovery Plan ≠ deleting Twin history.  
- Recovery Plan ≠ cramming-only mode without burnout guardrails.  
- Recovery is still curriculum-bound — no invented shortcuts past Prerequisites where required.

---

## Reflection

**Definition**  
Deliberate student (or coach-assisted) review of what worked, what did not, and what to change — including Reflection Journal evidence and post-exam reflection. Optional Learning Evidence when user-confirmed; never a silent Knowledge write by AI.

**Purpose**  
Close the learning loop, calibrate Insights, and improve Goals/strategy for the next period or sitting.

**Examples**  
- Weekly reflection: “Friday skips hurt Retention.”  
- Post-exam Reflection feeding Predictions calibration and next Goal.

**Related Concepts**  
Insight, Learning Evidence, Behaviour, Goal, AI Coach

**Common Misunderstandings**  
- Reflection ≠ automatic Twin Mastery boost.  
- AI-generated text is not Reflection Evidence until the student confirms.  
- Reflection does not replace Assessment evidence.

---

## Goal

**Definition**  
What the student is trying to achieve: which curriculum/paper, which Target Sitting, pass ambition, and related constraints. Twin Goals domain — distinct from derived Planning rows.

**Purpose**  
Scope Twin Knowledge slices, deadlines, Predictions, and plan capacity to a clear exam target.

**Examples**  
- Active Goal: IFoA CS1, April sitting, first-time pass.  
- Deferred Goal: switch sitting date after Manual Goal Change evidence.

**Related Concepts**  
Target Sitting, Available Study Time, Curriculum, Adaptive Plan, Projected Pass Probability

**Common Misunderstandings**  
- Goal ≠ Mission.  
- Goal ≠ Adaptive Plan.  
- Multiple papers are multiple Goals (or goal slices) inside one Twin — not multiple Twins.

---

## Target Sitting

**Definition**  
The specific examination sitting (date/window) the active Goal aims at — the deadline that drives pace, Readiness, and Projected Pass Probability.

**Purpose**  
Ground time-remaining math and urgency in a real exam calendar event.

**Examples**  
- April 2027 CS1 sitting.  
- Exam Date Change evidence moves Target Sitting and triggers plan rebalance.

**Related Concepts**  
Goal, Available Study Time, Readiness, Prediction, Adaptive Plan

**Common Misunderstandings**  
- Target Sitting ≠ curriculum syllabus year (related but distinct).  
- Changing sitting does not erase Learning Evidence.  
- “Someday” without a sitting is an incomplete Goal for core planning.

---

## Available Study Time

**Definition**  
The student’s committed capacity for study — hours per day/week, study days, and related constraints used by Planning and Mission load. Part of Goals / planning constraints; validated over time by Time and Behaviour evidence.

**Purpose**  
Keep Adaptive Plans and Missions feasible; feed Burnout Monitor and completion forecasts.

**Examples**  
- 10 hours/week, weeknights only.  
- Capacity reduced after Time On Task evidence shows chronic overruns.

**Related Concepts**  
Adaptive Plan, Mission, Learning Velocity, Consistency, Goal

**Common Misunderstandings**  
- Available Study Time ≠ time actually spent (actuals are evidence).  
- Inflated availability produces brittle plans.  
- AI must not silently raise Available Study Time to “make the plan fit.”

---

## Exam Weighting

**Definition**  
The relative importance of a curriculum entity for coverage and pass risk — syllabus/exam weight. In V2, typically on Sections (`exam_weight`); in V1, often on Topics. Canonical term in product language: **Exam Weighting** (synonymous with syllabus weight in engineering docs).

**Purpose**  
Ensure readiness and recommendations concentrate effort where the exam concentrates marks.

**Examples**  
- Section with 25% Exam Weighting dominates pass-risk narrative when weak.  
- Low-weight topic deprioritised under time pressure.

**Related Concepts**  
Section, Topic, Readiness, Recommendation Reason, Curriculum

**Common Misunderstandings**  
- Exam Weighting ≠ Difficulty.  
- Exam Weighting ≠ Twin Mastery.  
- Do not invent weights; read them from Curriculum.

---

## Difficulty

**Definition**  
An estimate of how hard a curriculum entity or assessment item is for learners (curriculum metadata and/or empirical item difficulty from Learning Evidence such as Question Difficulty). Distinct from Recommendation Priority and Exam Weighting.

**Purpose**  
Inform duration estimates, sequencing, diagnostic design, and Performance interpretation.

**Examples**  
- Topic metadata: intermediate Difficulty.  
- Item Difficulty inferred from cohort or personal error rates (when productised).

**Related Concepts**  
Topic, Learning Objective, Learning Evidence, Mastery, Adaptive Plan

**Common Misunderstandings**  
- Difficulty ≠ Priority.  
- Difficulty ≠ Exam Weighting.  
- Personal struggle does not rewrite official curriculum Difficulty without evidence rules.

---

## Dependency

**Definition**  
A blocking or ordering relationship that must be respected before an action — including Prerequisites and operational blockers (e.g. overdue reviews that should precede new learning, or Recommendation Dependencies in the Recommendation Contract).

**Purpose**  
Keep Recommendations and Adaptive Plans coherent with syllabus sequence and Twin Memory pressure.

**Examples**  
- Prerequisite Dependency: Topic A before Topic B.  
- Operational Dependency: clear overdue Revision before expanding coverage.

**Related Concepts**  
Prerequisite, Recommendation, Adaptive Plan, Memory Strength, Topic

**Common Misunderstandings**  
- Dependency ≠ soft UI suggestion.  
- Not every related topic is a Dependency.  
- AI Coach must not invent Dependencies absent curriculum or Twin rules.

---

# Relationships

## Concept map — core platform

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Official Curriculum                              │
│         Section → Topic → Learning Objective                             │
│         Exam Weighting · Prerequisite · Difficulty                       │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ references (never invents)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Student  →  Digital Twin                              │
│                                                                         │
│   Goals (Target Sitting, Available Study Time)                          │
│   Knowledge State (Mastery, Confidence)                                 │
│   Memory (Retention, Memory Strength)                                   │
│   Behaviour (Consistency, Learning Velocity)                            │
│   Performance · Motivation · Readiness · Predictions                    │
│   Learning State = Twin snapshot as a whole                             │
│                         ▲                                               │
│                         │ updates                                       │
│              Learning Evidence ◄── Learning Event                       │
│                         ▲                                               │
│                   Evidence Source                                       │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ derives
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 Adaptive Plan /          Recommendation           Mission
 Recovery Plan         (Reason, Confidence,      (Completion /
                        Priority, Dependency)      Failure)
        │                       │                       │
        └───────────────────────┴───────────────────────┘
                                │
                                ▼
                    Insight · Reflection · Prediction
                    (incl. Projected Pass Probability)
```

## Evidence → Twin → decision loop

```
Student / System action
        │
        ▼
  Learning Event ──► Learning Evidence (immutable)
        │
        ▼
  Digital Twin domains updated (deterministic cores)
        │
        ├─► Knowledge State / Mastery / Confidence
        ├─► Retention / Memory Strength
        ├─► Behaviour / Consistency / Learning Velocity
        └─► Readiness / Predictions (Projected Pass Probability)
                │
                ▼
        Recommendation (+ Reason, Confidence, Priority)
                │
                ▼
        Mission / Adaptive Plan / Recovery Plan
                │
                └─► new Learning Events (loop)
```

## Curriculum hierarchy vs learner state

```
Curriculum (shared)              Twin (per Student)
─────────────────                ──────────────────
Section                          Knowledge State @ Section/Topic
  Topic                          Mastery, Confidence
    Learning Objective           (future objective-level Mastery)
Exam Weighting ────────────────► Readiness risk concentration
Prerequisite / Dependency ─────► Recommendation Dependency
Difficulty ────────────────────► duration / sequencing hints

Learning Evidence cites curriculum identity when topic-scoped.
```

## Planning family

```
Goal + Target Sitting + Available Study Time
        │
        ▼
Diagnostic Assessment (optional) ──► initial Knowledge State
        │
        ▼
Adaptive Plan ◄── Digital Twin + Curriculum
        │
        ├─► Mission (daily)
        │       ├─► Mission Completion
        │       └─► Mission Failure ──► Recovery Plan mode
        │
        └─► Study Session / Revision Session ──► Learning Evidence
```

---

# Naming Standards

Use these conventions so specifications, code, and UI stay aligned with this language.

## Specifications and documentation

| Rule | Standard |
|---|---|
| Concept titles | Title Case for defined terms: `Digital Twin`, `Learning Evidence`, `Exam Weighting` |
| First use in a doc | Prefer bold or link to this file / companion Epic 0 specs |
| Synonyms | Forbidden in normative text — use [Canonical Terminology](#canonical-terminology) |
| V1 legacy wording | “Learning outcome” allowed only when describing V1 JSON fields; prose should say Learning Objective |
| British spelling | Prefer product docs’ existing British forms where already used (`Behaviour`, `Personalised`) — stay consistent within a document |

## Database / persistence

| Rule | Standard |
|---|---|
| Tables / models | Singular domain nouns matching concepts where practical (`Mission`, `Topic`, `Section`) |
| Twin projections | Name after Twin domains or evidence — avoid `student_model`, `knowledge_score` |
| Evidence log | Names should read as evidence/events, not mutable “scores” |
| Curriculum FKs | Reference canonical curriculum identities; never free-text topic keys as sole identity |
| Weights | Prefer `exam_weight` / documented synonyms mapped to **Exam Weighting** |

## Services

| Rule | Standard |
|---|---|
| Files / classes | `*_service.py` / `*Service` owning the domain verb (`ReadinessService`, `RecommendationService`) |
| Twin updates | Functions of evidence + prior state — method names should not imply silent score overwrites |
| No god services | One coherent domain per service; do not hide Recommendation math inside route handlers |

## APIs

| Rule | Standard |
|---|---|
| Resource names | Plural nouns aligned to concepts (`/missions`, `/recommendations`) |
| Fields | Prefer canonical terms: `mastery`, `retention`, `recommendation_confidence`, `exam_weighting` / `exam_weight` |
| Errors | Do not leak other students’ Twin identifiers |
| Derived vs authoritative | Response docs should mark plans/recommendations as derived from Twin |

## UI

| Rule | Standard |
|---|---|
| Primary CTAs | “Today’s Mission”, “Study next” (Recommendation), “Readiness” |
| Avoid | “Knowledge Score”, “Student Model”, “Learning Data”, “AI decided” without reasons |
| Uncertainty | Surface Confidence / intervals near Predictions and Projected Pass Probability |
| Explainability | Show Recommendation Reason factors, not only Priority |

## AI agents and prompts

| Rule | Standard |
|---|---|
| Mandatory vocabulary | Digital Twin, Learning Evidence, Mastery, Recommendation Reason |
| Forbidden | Inventing syllabus order; silent Knowledge writes; calling Twin “student model” in normative output |
| Grounding | Insights and coaching cite Twin factors and Evidence Sources |

---

# Canonical Terminology

When multiple words could be used, **use the left-hand term**.

| Canonical term | Do not use (for this meaning) | Notes |
|---|---|---|
| **Digital Twin** | Student Model, Learner Model, Profile Brain | One Twin per student |
| **Learning Evidence** | Learning Data, Telemetry dump, Activity log (alone) | Immutable, attributable records |
| **Learning Event** | Click, Interaction (unqualified) | Only domain-meaningful occurrences |
| **Evidence Source** | Logger, Producer (unqualified) | Provenance of evidence |
| **Mastery** | Knowledge Score, Skill %, Competence badge | Probabilistic belief |
| **Confidence** | Certainty score (unqualified) | Disambiguate Twin vs self-report vs recommendation |
| **Retention** | Memory % (alone), Forget score | Pair with Memory Strength when scheduling |
| **Memory Strength** | SRS score (as product noun) | Memory-domain scheduling strength |
| **Knowledge State** | Topic map (alone), Progress grid | Twin Knowledge aggregate |
| **Learning State** | Overall progress (vague) | Whole Twin snapshot |
| **Learning Velocity** | Speed, Grind rate | Sustainable pace signal |
| **Recommendation** | Suggestion (normative), AI tip | Deterministic explainable next action |
| **Recommendation Reason** | Rationale blurb (without factors) | Factor codes + narrative |
| **Recommendation Confidence** | AI confidence | Evidence-density confidence |
| **Recommendation Priority** | Importance (vague), Difficulty | Rank / band for action order |
| **Mission** | Daily todo list, Homework pack | Optimizer-derived task set |
| **Mission Completion** | Done streak | Evidence of finishing mission |
| **Mission Failure** | Fail (academic), Flunk | Missed/expired/abandoned mission |
| **Readiness** | Progress bar, Preparedness vibes | Explainable exam preparedness |
| **Projected Pass Probability** | Pass guarantee, Chance (casual only in UI microcopy) | Prediction with uncertainty |
| **Prediction** | Forecast model private state | Twin-downstream estimate |
| **Insight** | Fun fact, AI observation (ungrounded) | Twin-grounded interpretation |
| **Behaviour** | Habits module (as Twin replacement) | Twin domain |
| **Consistency** | Streak | Sustainable regularity |
| **Curriculum** | Course content pack, Our syllabus fork | Official syllabus truth |
| **Section** | Chapter (unless official term) | V2 grouping |
| **Topic** | Lesson, Module (as syllabus id) | Canonical study unit |
| **Learning Objective** | Learning Outcome (in new prose), LO blurb | Finest syllabus leaf |
| **Prerequisite** | Suggested prior | Curriculum requirement |
| **Dependency** | Soft link | Blocking/ordering relationship |
| **Study Session** | Study block (OK as synonym in UI), Lesson play | Learning activity block |
| **Revision Session** | Review (when meaning spaced revision) | Deliberate reinforcement |
| **Diagnostic Assessment** | Placement test (OK in UI), Quiz (generic) | Baseline assessment |
| **Adaptive Plan** | Static study plan, Timetable | Regenerable plan |
| **Recovery Plan** | Panic plan, Cram mode | Catch-up Adaptive Plan mode |
| **Reflection** | Journaling (alone) | Confirmed reflective evidence / practice |
| **Goal** | Target (alone), Ambition | Twin Goals domain |
| **Target Sitting** | Exam date (OK in UI), Deadline (alone) | Named sitting window |
| **Available Study Time** | Free time, Capacity (OK if mapped) | Committed study capacity |
| **Exam Weighting** | Importance, Syllabus weight (OK in eng. docs) | Official relative exam importance |
| **Difficulty** | Hardness, Priority | Item/topic hardess — not weight |

---

# Glossary Index

Alphabetical list of core terms defined in this document.

| Term | Section |
|---|---|
| Adaptive Plan | [Adaptive Plan](#adaptive-plan) |
| Available Study Time | [Available Study Time](#available-study-time) |
| Behaviour | [Behaviour](#behaviour) |
| Confidence | [Confidence](#confidence) |
| Consistency | [Consistency](#consistency) |
| Curriculum | [Curriculum](#curriculum) |
| Dependency | [Dependency](#dependency) |
| Diagnostic Assessment | [Diagnostic Assessment](#diagnostic-assessment) |
| Difficulty | [Difficulty](#difficulty) |
| Digital Twin | [Digital Twin](#digital-twin) |
| Evidence Source | [Evidence Source](#evidence-source) |
| Exam Weighting | [Exam Weighting](#exam-weighting) |
| Goal | [Goal](#goal) |
| Insight | [Insight](#insight) |
| Knowledge State | [Knowledge State](#knowledge-state) |
| Learning Evidence | [Learning Evidence](#learning-evidence) |
| Learning Event | [Learning Event](#learning-event) |
| Learning Objective | [Learning Objective](#learning-objective) |
| Learning State | [Learning State](#learning-state) |
| Learning Velocity | [Learning Velocity](#learning-velocity) |
| Mastery | [Mastery](#mastery) |
| Memory Strength | [Memory Strength](#memory-strength) |
| Mission | [Mission](#mission) |
| Mission Completion | [Mission Completion](#mission-completion) |
| Mission Failure | [Mission Failure](#mission-failure) |
| Prediction | [Prediction](#prediction) |
| Prerequisite | [Prerequisite](#prerequisite) |
| Projected Pass Probability | [Projected Pass Probability](#projected-pass-probability) |
| Readiness | [Readiness](#readiness) |
| Recommendation | [Recommendation](#recommendation) |
| Recommendation Confidence | [Recommendation Confidence](#recommendation-confidence) |
| Recommendation Priority | [Recommendation Priority](#recommendation-priority) |
| Recommendation Reason | [Recommendation Reason](#recommendation-reason) |
| Recovery Plan | [Recovery Plan](#recovery-plan) |
| Reflection | [Reflection](#reflection) |
| Retention | [Retention](#retention) |
| Revision Session | [Revision Session](#revision-session) |
| Section | [Section](#section) |
| Student | [Student](#student) |
| Study Session | [Study Session](#study-session) |
| Target Sitting | [Target Sitting](#target-sitting) |
| Topic | [Topic](#topic) |

---

# Related documents

| Document | Role |
|---|---|
| [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) | Twin architecture, recommendation/prediction contracts |
| [`LEARNING_EVIDENCE_MODEL.md`](LEARNING_EVIDENCE_MODEL.md) | Evidence catalogue, quality, lifecycle |
| [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) | Product principles and student journey |
| [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) | Engineering orientation |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System layering |
| [`knowledge/development/glossary.md`](knowledge/development/glossary.md) | Engineering glossary (implementation-oriented) |

---

# Document governance

| | |
|---|---|
| **Owner** | Domain architecture / Epic 0 |
| **Change policy** | Additive clarification preferred; renaming a canonical term requires updating companion Epic 0 specs and the engineering glossary |
| **Normative conflict** | Deeper Twin/Evidence rules in companion specs win on mechanism; **this file wins on term choice** |
| **Implementation** | Out of scope — documentation only for Capability 0.3 |
