# Learning Evidence Model

**Status:** Canonical domain architecture specification  
**Epic:** Epic 0 – Student Intelligence Platform  
**Capability:** 0.2 – Define the Learning Evidence Model  
**Audience:** Product, engineering, AI agents, future subsystem owners  
**Scope:** Conceptual specification of how Kwalitec learns about students — not a database schema and not an implementation guide  
**Companion docs:** [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md), [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md), [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`knowledge/`](knowledge/)

---

## Document purpose

This specification defines the **Learning Evidence Model** for Kwalitec.

It answers:

- What constitutes learning evidence
- How evidence is generated
- How evidence affects the Student Digital Twin
- Confidence levels of evidence
- Evidence lifecycle
- Evidence quality
- Evidence aggregation
- Which systems produce and consume evidence
- How recommendations remain traceable to evidence

This document is the **canonical reference** for every piece of evidence that can influence the Student Digital Twin. Every recommendation, prediction, and adaptive decision must ultimately be traceable to Learning Evidence.

**Non-goals of this document**

- Table designs, Alembic revisions, or ORM class layouts
- API contracts for HTTP routes
- Concrete scoring formulas, weighting coefficients, or ML model choices
- Replacement of the Curriculum Engine as syllabus source of truth
- Replacement of the Student Digital Twin as learner-state authority

---

# Executive Summary

**Learning Evidence** is Kwalitec’s immutable record of what a student did, achieved, skipped, reported, or experienced in the course of exam preparation. It is the only legitimate input that may change Twin beliefs about knowledge, memory, behaviour, performance, motivation, and goals.

Kwalitec learns from **evidence**, not from isolated events treated as truth in isolation. A single correct answer does not mean mastery. A skipped Friday does not mean burnout. A high mock score does not erase months of weak coverage. Intelligence emerges from **accumulated, quality-weighted, time-aware evidence** interpreted against the official curriculum and the student’s goals.

This distinction is central to the product thesis — **reduce decisions, increase learning** ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)):

| Approach | Failure mode | Kwalitec stance |
|---|---|---|
| React to the latest event | Whiplash recommendations; noisy “study next” | Rejected |
| Trust self-report alone | Optimistic mastery; hidden gaps | Self-report is evidence, tagged and down-weighted |
| Trust completion alone | Missions finished without learning | Completion ≠ mastery unless assessed |
| Black-box inference without trail | Unexplainable advice | Forbidden in core paths |
| **Accumulate attributable evidence → update Twin → derive decisions** | — | **Required** |

The Student Digital Twin ([`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md)) is the authoritative *state*. Learning Evidence is the authoritative *history* that produces that state. Plans, missions, readiness scores, and recommendations are *consequences* of Twin state derived from evidence — never substitutes for evidence.

Without a coherent Evidence Model, Twin domains drift, Analytics forks metrics, AI Coach invents narratives, and students lose trust. With it, every intelligent subsystem shares one auditable spine.

---

# Core Philosophy

These principles are binding for all evidence-related design and implementation.

1. **Every meaningful student interaction generates evidence.**  
   Study, practice, skip, reschedule, rate confidence, open a notification, accept or dismiss a recommendation — if it can change how Kwalitec understands the learner, it must leave an evidence record.

2. **Evidence is immutable.**  
   Once written, an evidence record is never edited in place. Corrections are new compensating evidence (e.g. voided attempt, corrected attribution).

3. **Evidence is never overwritten.**  
   Append-only history is the audit spine of the Twin. Derived views may be recomputed; the log is not rewritten.

4. **Knowledge estimates evolve from accumulated evidence.**  
   Mastery and retention are probabilistic beliefs updated by streams of evidence, not binary badges from single events ([`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) Guiding Principles).

5. **Recommendations are derived from evidence, not assumptions.**  
   Heuristics without attributable evidence do not belong in the core recommendation path. Cold-start defaults must be explicit and low-confidence.

6. **The Digital Twin is evidence-driven.**  
   Twin domain updates are functions of prior Twin state plus new evidence. No subsystem may mutate Knowledge, Memory, or Readiness by side channel.

7. **Evidence is attributable.**  
   Every record cites who (student), what (type), when (timestamp), whence (source subsystem), and — when topic-scoped — which curriculum identity.

8. **Evidence is explainable.**  
   Downstream decisions must be able to cite the evidence (or evidence aggregates) that justified them.

9. **Quality and confidence are first-class.**  
   Not all evidence is equal. Quality dimensions and confidence levels shape how strongly evidence moves Twin beliefs.

10. **Curriculum identity remains canonical.**  
    Topic-scoped evidence references official syllabus entities via canonical IDs and traversal ([ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md)). Evidence never invents parallel topics.

11. **Determinism over theatre.**  
    Same evidence stream + same Twin snapshot → same core Twin updates and same core consumer outputs ([`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)).

12. **Privacy and ownership.**  
    Evidence belongs to the student. It is auditable and inspectable. Learning signals are separated from unnecessary PII where practical.

---

# Evidence Categories

Evidence types are grouped into high-level categories. Categories organise the catalogue; they do not replace type-level semantics.

## Learning Activity

Evidence that the student engaged with syllabus content in a learning mode — reading, working through topics, completing planned study blocks — without necessarily producing a scored assessment outcome.

**Role:** Updates Behaviour (adherence, effort), may lightly reinforce Memory when topic-tagged, and signals Planning progress. Alone, it is weak evidence of Knowledge.

## Assessment

Evidence from scored or judged practice — questions, quizzes, mocks, past papers, diagnostics — that measures performance against curriculum entities.

**Role:** Primary driver of Performance and Knowledge belief updates; strong input to Readiness and Predictions when exam-condition or syllabus-mapped.

## Behaviour

Evidence of how the student actually studies: starts, completions, skips, abandons, preference decisions (accept/dismiss), adherence patterns.

**Role:** Feeds Behaviour and Motivation domains; improves Planning realism and Notification timing; does not directly grant mastery.

## Time

Evidence about duration, timing, and temporal structure of study — time on task, breaks, session length, quiet hours engagement.

**Role:** Validates capacity assumptions, informs Burnout Monitor, and contextualises other evidence. Time alone does not prove Knowledge.

## Confidence

Evidence from explicit self-report of certainty, readiness feelings, or perceived mastery.

**Role:** Tagged `self_report`; updates Knowledge/Motivation channels at lower weight than assessed evidence; enables calibration against Performance.

## Revision

Evidence from deliberate review and spaced reinforcement — revision sessions, flashcard reviews, overdue clearances.

**Role:** Primary driver of Memory updates; counters decay; feeds Revision Engine scheduling and retention forecasts.

## Planning

Evidence about plan and goal structure changes — reschedules, skipped planned sessions, manual goal changes, exam date changes, readiness reviews that alter strategy.

**Role:** Updates Goals and Planning domains; triggers rebalance; does not rewrite historical Performance.

## Engagement

Evidence of product engagement that is not itself a learning outcome — daily check-ins, notification responses, coach dialogue turns confirmed by the student.

**Role:** Behaviour and Motivation signals; optional reflection evidence; never a substitute for Assessment.

## System Events

Evidence generated by the platform itself when it records a material state transition — mission generated and expired uncompleted, plan regenerated after slip, diagnostic completed, Twin cold-start marked.

**Role:** Completes the audit trail; attributes provenance as `system` vs `user`; supports explainability of automatic rebalances.

## Future Sensors

Reserved category for evidence sources not yet productised — wearables, eye-tracking, voice tutoring telemetry, institution feedback, calendar sync, peer collaboration signals.

**Role:** Extensibility without breaking immutability or Twin authority. Future sensors must still obey attribution, quality, and privacy rules before influencing Knowledge.

---

# Evidence Catalogue

Each type below is a conceptual evidence kind. Names may map to multiple implementation events later; semantics must not fork.

For every type: **Purpose**, **When generated**, **Source**, **Reliability**, **Confidence Weight**, **Example**, **Potential future use**.

---

## Study Session

| | |
|---|---|
| **Purpose** | Record that a student engaged in a bounded study block, optionally topic-scoped. |
| **When generated** | Session start and/or successful completion of a study block. |
| **Source** | Study session / mission task flows; Learning Activity producers. |
| **Reliability** | Medium for Behaviour; low for Knowledge unless paired with Assessment. |
| **Confidence Weight** | Low–medium toward Knowledge; medium toward Behaviour adherence. |
| **Example** | Student completes a 45-minute CS1 topic block on “Hypothesis testing.” |
| **Potential future use** | Capacity realism; habit coaching; deep-work vs shallow-work tagging. |

---

## Topic Started

| | |
|---|---|
| **Purpose** | Mark first meaningful exposure to a curriculum topic in the active goal. |
| **When generated** | Student begins planned or recommended work on a topic not previously started. |
| **Source** | Missions, study plan progression, Learning Activity. |
| **Reliability** | High for coverage *exposure*; low for mastery. |
| **Confidence Weight** | High for coverage flags; negligible for Knowledge belief strength. |
| **Example** | First mission task opens Topic “Linear regression” under CS1 2026. |
| **Potential future use** | Cold-start diagnostics; time-to-first-exposure analytics. |

---

## Topic Completed

| | |
|---|---|
| **Purpose** | Record planned learning coverage of a topic as complete (plan sense), distinct from assessed mastery. |
| **When generated** | Student or system marks topic learning tasks complete per plan rules. |
| **Source** | Planning / Mission completion paths. |
| **Reliability** | Medium for Planning progress; must not be confused with Assessment. |
| **Confidence Weight** | Medium for Planning/coverage; low for Knowledge unless Assessment co-occurs. |
| **Example** | All “learn” tasks for a topic cleared in the week plan. |
| **Potential future use** | Coverage denominators; catch-up pressure without false mastery. |

---

## Question Attempt

| | |
|---|---|
| **Purpose** | Record that a student attempted a practice item mapped to curriculum identity. |
| **When generated** | Answer submitted (correctness may be separate or combined events). |
| **Source** | Questions / Active Learning / Learning services. |
| **Reliability** | Medium–high depending on item quality and independence from hints. |
| **Confidence Weight** | Medium base; adjusted by difficulty, hint use, and independence. |
| **Example** | Student submits an answer to a syllabus-tagged practice question. |
| **Potential future use** | Adaptive item selection; mistake taxonomy; item-level Memory. |

---

## Question Correct

| | |
|---|---|
| **Purpose** | Positive Assessment signal for the mapped topic/objective. |
| **When generated** | Graded correct outcome on an attempt. |
| **Source** | Assessment producers. |
| **Reliability** | Medium–high; single items remain noisy. |
| **Confidence Weight** | Medium; rises with item quality and repetition under varied conditions. |
| **Example** | Correct untimed practice on “Bayes’ theorem” application. |
| **Potential future use** | Slow Memory decay; calibrate self-confidence vs accuracy. |

---

## Question Incorrect

| | |
|---|---|
| **Purpose** | Negative Assessment signal; drives review urgency and weak-area detection. |
| **When generated** | Graded incorrect (or materially incomplete) outcome. |
| **Source** | Assessment producers; mistake capture. |
| **Reliability** | Medium–high for identifying gaps; context (slip vs misconception) may be incomplete. |
| **Confidence Weight** | Medium–high toward Knowledge downward revision and Memory due acceleration. |
| **Example** | Incorrect answer tagged to objective “Interpret p-values.” |
| **Potential future use** | Mistake taxonomy; targeted Revision; AI Coach debriefs grounded in Twin. |

---

## Question Difficulty

| | |
|---|---|
| **Purpose** | Contextualise attempt evidence by intended or observed difficulty. |
| **When generated** | With or after an attempt when difficulty metadata is available. |
| **Source** | Question bank metadata; optional adaptive estimate (future). |
| **Reliability** | Medium — depends on bank curation quality. |
| **Confidence Weight** | Modifier on attempt evidence (hard correct > easy correct for belief strength). |
| **Example** | Attempt recorded with difficulty band “exam-standard.” |
| **Potential future use** | Pass-probability calibration; exam-condition rehearsal design. |

---

## Quiz Completed

| | |
|---|---|
| **Purpose** | Aggregate Assessment across a scoped set of items. |
| **When generated** | Student finishes a quiz mapped to topics/sections. |
| **Source** | Quizzes. |
| **Reliability** | Higher than single items when syllabus-mapped and sufficient length. |
| **Confidence Weight** | Medium–high for Knowledge across quiz scope. |
| **Example** | End-of-section quiz on CS1 Section B completed at 70%. |
| **Potential future use** | Diagnostic refresh; Readiness calibration between mocks. |

---

## Mock Exam

| | |
|---|---|
| **Purpose** | Exam-condition Performance and Readiness stress-test. |
| **When generated** | Timed mock completed (full or product-defined partial mock). |
| **Source** | Mocks. |
| **Reliability** | High for exam-condition belief; may diverge from untimed mastery. |
| **Confidence Weight** | High for Performance and Predictions; still subject to pre-sitting decay. |
| **Example** | Three-hour CS1 mock under timed conditions with section breakdown. |
| **Potential future use** | Sit/defer advice; pass-probability calibration; cohort-relative bands (privacy-preserving). |

---

## Past Paper Attempt

| | |
|---|---|
| **Purpose** | Assessment against authentic or near-authentic exam material. |
| **When generated** | Student completes a past-paper session or marked paper review. |
| **Source** | Past papers / Assessment. |
| **Reliability** | High when marking is reliable and syllabus year aligned. |
| **Confidence Weight** | High for Performance; curriculum-year mismatch reduces weight. |
| **Example** | Attempt of prior sitting paper with topic-mapped mark scheme. |
| **Potential future use** | Year-over-year difficulty norms; objective coverage heatmaps. |

---

## Mission Completed

| | |
|---|---|
| **Purpose** | Behaviour and Planning signal that the day’s (or session’s) mission was finished. |
| **When generated** | All required mission tasks completed, or mission marked complete per product rules. |
| **Source** | Mission Engine. |
| **Reliability** | Medium for adherence; completion ≠ mastery unless tasks included Assessment. |
| **Confidence Weight** | Medium for Behaviour/Planning; Assessment sub-tasks carry their own weights. |
| **Example** | Daily mission with learn + review tasks marked complete. |
| **Potential future use** | Mission Optimizer tuning; consistency metrics; burnout vs reliability. |

---

## Mission Missed

| | |
|---|---|
| **Purpose** | Record that a mission expired or was abandoned without completion. |
| **When generated** | End of mission window without completion, or explicit miss. |
| **Source** | Mission Engine / System Events. |
| **Reliability** | High for Behaviour slip; interpretation (overload vs avoidance) needs pattern context. |
| **Confidence Weight** | Medium toward Behaviour and deadline risk; does not reduce Knowledge directly. |
| **Example** | Tuesday mission expires with two review tasks incomplete. |
| **Potential future use** | Catch-up modes; Notification timing; completion forecast. |

---

## Revision Session

| | |
|---|---|
| **Purpose** | Deliberate review block aimed at retention and weak/high-weight reinforcement. |
| **When generated** | Revision session started/completed, preferably topic-scoped. |
| **Source** | Revision Engine / Learning Activity. |
| **Reliability** | Medium–high for Memory when content is syllabus-mapped. |
| **Confidence Weight** | Medium–high for Memory; medium for Knowledge refresh. |
| **Example** | Weight-aware revision block on high-risk Section A topics. |
| **Potential future use** | Retention forecasts; pre-exam revision intensity caps. |

---

## Flashcard Review

| | |
|---|---|
| **Purpose** | Fine-grained spaced-repetition evidence for cards/objectives. |
| **When generated** | Card reviewed with outcome (remembered / forgotten / partial). |
| **Source** | Flashcards / Adaptive Learning. |
| **Reliability** | Medium — strong for recall scheduling; weaker for deep application mastery. |
| **Confidence Weight** | Medium for Memory; low–medium for Knowledge application beliefs. |
| **Example** | Card for “properties of estimators” marked forgotten. |
| **Potential future use** | Item-level Memory; personalised decay rates. |

---

## Confidence Rating

| | |
|---|---|
| **Purpose** | Explicit self-report of certainty on a topic, objective, or session. |
| **When generated** | Student submits a confidence rating (pre/post task or periodic). |
| **Source** | Confidence / Manual Updates. |
| **Reliability** | Low–medium; valuable for calibration, dangerous if treated as mastery. |
| **Confidence Weight** | Low–medium; tagged `self_report`; must not override dense contrary Assessment. |
| **Example** | Student rates “Survival models” confidence as 2/5 after a review. |
| **Potential future use** | Honesty calibration; diagnostic bootstrap; Motivation energy proxies. |

---

## Hint Requested

| | |
|---|---|
| **Purpose** | Qualify Assessment independence — help was used before or during an attempt. |
| **When generated** | Student requests a hint on a practice item. |
| **Source** | Questions / AI Tutor (when hinting). |
| **Reliability** | High as a contextual flag; interpretation of “needed help” is medium. |
| **Confidence Weight** | Reduces weight of subsequent correct outcomes on that attempt. |
| **Example** | Hint opened before submitting a correct answer. |
| **Potential future use** | Scaffolding analytics; true-unaided mastery estimates. |

---

## Time On Task

| | |
|---|---|
| **Purpose** | Measure effort duration associated with a session or task. |
| **When generated** | Session timer completes, pauses, or is reconciled. |
| **Source** | Time producers / study sessions. |
| **Reliability** | Medium for effort; low for Knowledge (time ≠ learning). |
| **Confidence Weight** | Weak for Knowledge; medium for Behaviour capacity and Motivation load. |
| **Example** | 52 minutes active on a mission task. |
| **Potential future use** | Burnout Monitor; realistic hour budgets; deep-work detection. |

---

## Session Abandoned

| | |
|---|---|
| **Purpose** | Record premature end of a study/practice session. |
| **When generated** | Session closed before planned completion without success criteria met. |
| **Source** | Behaviour / System Events. |
| **Reliability** | Medium — may be interruption or avoidance. |
| **Confidence Weight** | Medium for Behaviour; pattern strength matters more than single events. |
| **Example** | Quiz started and closed after two questions. |
| **Potential future use** | Friction analysis; Notification quiet-hours; coach prompts. |

---

## Study Break

| | |
|---|---|
| **Purpose** | Record intentional recovery within or between sessions. |
| **When generated** | Student starts a break or system detects planned rest. |
| **Source** | Time / Motivation-related flows. |
| **Reliability** | Medium when explicit; low when inferred. |
| **Confidence Weight** | Low for Knowledge; positive for sustainable Motivation when appropriate. |
| **Example** | Five-minute break between timed mock sections. |
| **Potential future use** | Intensity budgets; recovery-week recommendations. |

---

## Daily Check-in

| | |
|---|---|
| **Purpose** | Lightweight Engagement signal that the student connected with the product intent for the day. |
| **When generated** | Check-in completed (energy, intent, or simple presence). |
| **Source** | Engagement / Notifications. |
| **Reliability** | Low–medium for Motivation; not Assessment. |
| **Confidence Weight** | Low; useful in aggregate for consistency. |
| **Example** | Morning check-in: “available 90 minutes today.” |
| **Potential future use** | Dynamic capacity; burnout early warning. |

---

## Plan Rescheduled

| | |
|---|---|
| **Purpose** | Record that planned work moved in time without necessarily changing goals. |
| **When generated** | Student or system rebalances week/day distribution. |
| **Source** | Planning Engine / System Events. |
| **Reliability** | High as a Planning fact; reason codes improve interpretation. |
| **Confidence Weight** | High for Planning domain; Behaviour if user-initiated slip. |
| **Example** | Thursday topics moved to Saturday after a missed evening. |
| **Potential future use** | Explainable rebalance narratives; adherence vs flexibility metrics. |

---

## Skipped Session

| | |
|---|---|
| **Purpose** | Explicit or inferred skip of a planned study session. |
| **When generated** | Student skips, or session window passes unused. |
| **Source** | Behaviour / Planning. |
| **Reliability** | High for slip; Motivation interpretation needs patterns. |
| **Confidence Weight** | Medium toward Behaviour and deadline risk; no direct Knowledge reduction. |
| **Example** | Planned Friday review skipped. |
| **Potential future use** | Completion forecast; Notification strategy; catch-up missions. |

---

## Manual Goal Change

| | |
|---|---|
| **Purpose** | Student-directed change to exam target, intensity, or availability commitments. |
| **When generated** | Settings/wizard update to Goals attributes. |
| **Source** | Manual Updates / Study Plan Wizard. |
| **Reliability** | High for Goals facts. |
| **Confidence Weight** | High for Goals/Planning regeneration; does not erase Performance history. |
| **Example** | Availability reduced from 2h/day to 1h/day. |
| **Potential future use** | Multi-paper capacity budgets; intensity caps. |

---

## Exam Date Change

| | |
|---|---|
| **Purpose** | Change the sitting date or defer/advance the target exam. |
| **When generated** | Student updates sitting; catalogue timeline change applied to goal. |
| **Source** | Manual Updates / Examination catalogue binding. |
| **Reliability** | High for Goals time remaining. |
| **Confidence Weight** | High — major rebalance trigger for Planning, Readiness, Predictions. |
| **Example** | Sitting moved from April to September. |
| **Potential future use** | Re-sit workflows; institutional cohort date overlays. |

---

## Readiness Review

| | |
|---|---|
| **Purpose** | Capture that the student (or coach flow) explicitly reviewed readiness narrative and optionally recorded a decision intent. |
| **When generated** | Readiness surface reviewed; optional sit/defer intent logged. |
| **Source** | Readiness Engine / Engagement. |
| **Reliability** | High for “reviewed”; intent is self-report. |
| **Confidence Weight** | Medium for Decision Journal / Goals intent; Readiness scores remain engine-owned. |
| **Example** | Student reviews pass-risk factors and notes “continue toward April.” |
| **Potential future use** | Sit/defer product surface; coach workflows (Phase 7). |

---

## AI Tutor Interaction

| | |
|---|---|
| **Purpose** | Record assistive dialogue or tutoring turns that may include explanations, practice proposals, or reflections. |
| **When generated** | Tutor session events; **assessed outcomes** still emit separate Assessment evidence. |
| **Source** | AI Tutor / AI Coach. |
| **Reliability** | Medium for Engagement; Knowledge only via confirmed Assessment or explicit student-confirmed reflection. |
| **Confidence Weight** | Low for Knowledge unless paired with graded work; must not silently rewrite Twin Knowledge ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)). |
| **Example** | Coach explains why a topic was recommended; student confirms understanding reflection. |
| **Potential future use** | Grounded tutoring; reflection journals; never black-box path ownership. |

---

## Reflection Journal

| | |
|---|---|
| **Purpose** | Student-authored reflection on what worked, what failed, and strategy changes. |
| **When generated** | Journal entry submitted (post-session, post-mock, post-exam). |
| **Source** | Engagement / Manual Updates / AI Coach (user-confirmed). |
| **Reliability** | Medium as qualitative Behaviour/Motivation; low as Assessment. |
| **Confidence Weight** | Low–medium; explicit and attributable. |
| **Example** | Post-mock reflection: “ran out of time on Section C.” |
| **Potential future use** | Post-exam outcome loops; Decision Journal enrichment. |

---

## Recommendation Decision (Accept / Dismiss)

| | |
|---|---|
| **Purpose** | Record student response to a recommendation for preference learning and audit. |
| **When generated** | Accept, dismiss, or snooze of a Recommendation Contract item. |
| **Source** | Recommendation Engine / Decision Journal. |
| **Reliability** | High as preference evidence; not mastery evidence. |
| **Confidence Weight** | Indirect — shapes future ranking, not Knowledge beliefs. |
| **Example** | Student dismisses “review Topic X” with reason “already revised today.” |
| **Potential future use** | Alternative recommendation quality; explainability audits. |

---

## Diagnostic Assessment

| | |
|---|---|
| **Purpose** | Establish initial Knowledge map and cold-start position. |
| **When generated** | Diagnostic completed at Twin birth, re-sit repositioning, or major reset. |
| **Source** | Assessment / onboarding. |
| **Reliability** | High at baseline relative to empty Twin; subsequent evidence dominates over time. |
| **Confidence Weight** | High initially for Knowledge; freshness decays as new Assessment arrives. |
| **Example** | Onboarding diagnostic covering weighted CS1 sections. |
| **Potential future use** | Re-sit repositioning; institution placement tests. |

---

## Notification Engagement

| | |
|---|---|
| **Purpose** | Record open, dismiss, or ignore of study prompts. |
| **When generated** | Notification interaction or expiry. |
| **Source** | Notifications. |
| **Reliability** | Medium for Engagement timing preferences. |
| **Confidence Weight** | Low–medium for Behaviour; none for Knowledge. |
| **Example** | Evening review reminder dismissed. |
| **Potential future use** | Quiet hours; anti-nag burnout protection. |

---

## Post-Exam Outcome (Future)

| | |
|---|---|
| **Purpose** | Capture sitting result for Predictions calibration and Goals completion. |
| **When generated** | Student or institution records pass/fail/score after sitting. |
| **Source** | Future Integrations / Manual Updates. |
| **Reliability** | Outcome-level — high for calibration, not for topic micro-beliefs alone. |
| **Confidence Weight** | High for Predictions model improvement; does not rewrite historical attempts. |
| **Example** | April CS1 result recorded as pass. |
| **Potential future use** | Pass-rate KPI; model calibration; next-sitting planning. |

---

# Evidence Quality

Evidence quality describes how fit a record (or aggregate) is to influence Twin intelligence. Quality is multi-dimensional; a record can be fresh but incomplete, or accurate but stale.

## Quality dimensions

| Dimension | Meaning |
|---|---|
| **Accuracy** | The record correctly represents what occurred (grading correctness, timestamps, curriculum mapping). |
| **Completeness** | Required context is present (topic identity, source, outcome, duration when claimed). |
| **Freshness** | How recently the underlying event occurred relative to the decision being made. |
| **Consistency** | Agreement with related evidence (e.g. high confidence vs repeated incorrect attempts). |
| **Reliability** | Trustworthiness of the producer and conditions (exam-condition mock vs distracted micro-quiz). |
| **Recency** | Temporal proximity used in aggregation — recent streams outweigh ancient ones *all else equal*. |

Freshness emphasises “is this still informative?”; Recency emphasises “how should aggregators order time?” They often move together but are not identical (a yesterday’s mock is fresh; a yesterday’s accidental tap may be fresh but low-reliability).

## How quality influences intelligence

1. **Low-quality evidence still exists** — immutability forbids deletion for convenience — but Twin updates apply **reduced influence**.
2. **Incomplete topic mapping** limits Knowledge updates; Behaviour may still update.
3. **Inconsistent clusters** increase Twin uncertainty (wider confidence intervals) rather than silently averaging into false certainty.
4. **Stale high-reliability evidence** (old mock) remains historically true but contributes less to *current* Readiness than a recent quiz of equal reliability — per weighting principles, not a fixed formula.
5. **Analytics and AI Coach** must surface quality caveats when narrating (“based on a short quiz, not a mock”).
6. **Deterministic cores** consume quality/confidence metadata as inputs so reproducibility is preserved.

---

# Evidence Confidence

Confidence expresses how strongly Kwalitec should believe that a piece of evidence (or an aggregate) warrants moving Twin state.

## Confidence levels

| Level | Meaning | Typical origins |
|---|---|---|
| **High** | Strong warrant to update beliefs | Syllabus-mapped mocks; substantial quizzes; repeated independent correct/incorrect patterns; explicit Goals changes |
| **Medium** | Useful but noisy or partial | Single well-mapped questions; mission completion; revision sessions; timed practice without full exam conditions |
| **Low** | Weak warrant; contextual only | Time on task alone; check-ins; notification dismissals; single self-reports; abandoned micro-sessions |
| **Unknown** | Insufficient basis to classify | Future sensors not yet validated; poorly mapped content; corrupted or partial imports pending validation |

## How confidence is determined

Confidence is a **judgement from provenance and context**, not a vibe:

1. **Producer class** — Assessment under exam conditions > short practice > self-report > passive engagement.
2. **Curriculum attribution** — Canonical topic/objective mapping raises confidence; free-text-only context lowers it to Unknown/Low for Knowledge.
3. **Independence** — Unaided attempts outrank hinted or tutor-scaffolded successes.
4. **Repetition and diversity** — Repeated similar outcomes across items/conditions raise confidence in the *aggregate belief*, even if each event is Medium.
5. **Contradiction** — Conflicting evidence lowers confidence in the *conclusion*, even if each record is individually High.
6. **Provenance** — `user` actions and graded `system` assessments outrank inferred sensors until those sensors are validated.
7. **Cold start** — Absence of evidence yields Unknown/Low Knowledge confidence, never fabricated High mastery ([`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) Twin Lifecycle).

Confidence attaches both to **individual evidence** and to **Twin beliefs derived from aggregates**. Belief confidence is what Recommendations and Predictions expose in their contracts.

---

# Evidence Weighting

Principles only — **no mathematical formulas** in this specification.

1. **Mock exams generally outweigh quizzes.**  
   Exam-condition, syllabus-breadth signals dominate short formative quizzes for Readiness and pass-risk narratives.

2. **Quizzes generally outweigh single questions.**  
   Aggregates reduce item noise when scope is curriculum-mapped.

3. **Assessed outcomes outweigh completion events.**  
   Mission or topic completion without Assessment does not grant mastery.

4. **Recent evidence generally outweighs old evidence.**  
   All else equal, newer signals better represent current Knowledge and Memory — while history remains immutable for audit.

5. **Repeated behaviour strengthens confidence.**  
   Patterns of skips, adherence, or accuracy matter more than one-off events.

6. **Contradictory evidence reduces certainty.**  
   Do not “pick a winner” silently; widen uncertainty and prefer explainable caution in recommendations.

7. **Self-report never overrides dense contrary Assessment.**  
   Confidence ratings inform calibration; they do not erase attempt history.

8. **Hinted success weighs less than unaided success.**  
   Independence is part of evidential strength.

9. **High-weight syllabus areas amplify decision urgency, not evidence truth.**  
   Curriculum weight affects *priority of action*, not whether an event happened. Evidence remains factual; planning consumes weights separately ([ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md)).

10. **System-inferred sensors start underweight.**  
    Future Sensors must earn weight through validation before influencing Knowledge.

11. **Corrections are additive.**  
    Voiding or amending is new evidence that supersedes influence without erasing the original record’s existence.

12. **Deterministic application.**  
    Whatever weighting policy an implementation adopts, the same evidence multiset + Twin snapshot must yield the same Twin update in core paths.

---

# Evidence Lifecycle

```
Student Action
      ↓
Evidence Created
      ↓
Validated
      ↓
Stored
      ↓
Digital Twin Updated
      ↓
Predictions Updated
      ↓
Recommendations Updated
      ↓
Evidence Archived
```

## Student Action

The learner (or an authorised system acting on a defined trigger) performs something meaningful: studies, answers, skips, reschedules, rates confidence, interacts with coach or notifications.

## Evidence Created

A typed evidence record is composed with timestamp, student identity, source subsystem, provenance, optional curriculum references, and payload sufficient for later explanation. Creation is conceptual append — not Twin mutation yet.

## Validated

Checks for structural integrity and policy: required fields present, curriculum IDs resolvable when topic-scoped, provenance allowed for the producer, no silent PII leakage into learning payload beyond need. Invalid candidates are rejected or accepted as Low/Unknown quality with explicit flags — never silently “fixed” by overwriting.

## Stored

The record enters the immutable Evidence Log (conceptual). Storage is append-only. This log is the audit spine referenced by [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md).

## Digital Twin Updated

Deterministic Twin update functions apply evidence to relevant domains (Knowledge, Memory, Behaviour, Performance, Goals, Motivation, Planning/Readiness derived views). No consumer bypasses this step to invent private mastery.

## Predictions Updated

Material evidence triggers recalculation of Predictions from Twin state only — never from side channels ([`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) Prediction Contract).

## Recommendations Updated

Recommendation Engine regenerates explainable next actions from Twin + Predictions + Curriculum. Accept/dismiss will create *new* Behaviour evidence later — closing the loop.

## Evidence Archived

Operational archival (cold storage, retention tiers) may move records between storage classes for cost or compliance. **Archival is not deletion of meaning**: archived evidence remains part of the student’s history for audit and, where product policy allows, for Twin recomputation. Legal erasure requests are a privacy process, not a convenience rewrite of learning history without accountability.

---

# Evidence Flow

Closed learning loop — Curriculum remains upstream syllabus truth; Evidence feeds the Twin; plans are downstream.

```
Student
   ↓
Interaction
   ↓
Evidence
   ↓
Digital Twin
   ↓
Prediction Engine
   ↓
Recommendation Engine
   ↓
Student
```

### Expanded flow

```
┌──────────────┐
│   Student    │
└──────┬───────┘
       │ interaction (study, practice, skip, decide, …)
       ▼
┌──────────────┐
│  Producers   │  Questions, Quizzes, Mocks, Sessions, …
└──────┬───────┘
       │ create + validate
       ▼
┌──────────────┐
│   Evidence   │  Immutable, attributable records
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Digital Twin │  Knowledge · Memory · Behaviour · Performance · …
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Predictions  │  Pass risk, retention, completion, burnout, …
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Recommend. Eng│  Explainable next actions (Recommendation Contract)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Plan/Mission │  Derived schedule + daily work
│ Notifications│
│   AI Coach   │
└──────┬───────┘
       │
       └──────────► Student (loop) ──► new Evidence
```

### Layering alignment

Per [`ARCHITECTURE.md`](ARCHITECTURE.md) and [ADR-001](knowledge/architecture/ADR-001-service-layer.md) / [ADR-002](knowledge/architecture/ADR-002-blueprint-architecture.md):

- Blueprints collect interactions and present outcomes
- Services create evidence, update Twin projections, and derive plans/recommendations
- Curriculum Engine remains syllabus truth
- Models persist evidence and Twin projections without becoming a second curriculum

---

# Evidence Consumers

Consumers **read** evidence and/or Twin state derived from evidence. They must not invent evidence or maintain competing mastery stores.

## Planning Engine

**Benefit:** Rebuilds schedules from Goals + Knowledge/Memory gaps + Behaviour adherence revealed by skips, completions, and reschedules. Evidence of slip and capacity makes rebalance explainable rather than arbitrary.

See [study-planning.md](knowledge/subsystems/study-planning.md).

## Mission Engine

**Benefit:** Prioritises daily tasks using urgency from Assessment weakness, Revision due pressure, and Behaviour reliability. Mission Completed/Missed evidence tunes future load without treating missions as a second syllabus.

See [missions.md](knowledge/subsystems/missions.md).

## Readiness Engine

**Benefit:** Coverage, pace, and pass-risk narratives grounded in Assessment aggregates, Memory durability, and Goals time remaining. Mocks and quizzes inform risk concentration; skips inform pace risk — with shared metric definitions Analytics must not fork.

See [readiness.md](knowledge/subsystems/readiness.md).

## Analytics

**Benefit:** Longitudinal views, heatmaps, and consistency/accuracy trends over the Evidence Log and Twin projections. **Read-only** regarding authoritative beliefs; may emit Engagement telemetry only if productised as evidence.

See [analytics.md](knowledge/subsystems/analytics.md).

## AI Tutor / AI Coach

**Benefit:** Explanations, debriefs, and strategy dialogue grounded in Twin factors and cited evidence summaries. May propose practice; graded results enter as Assessment. Must not silently rewrite Knowledge or hide scoring ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)).

## Revision Engine

**Benefit:** Schedules review from Memory due sets and weak/high-weight gaps evidenced by incorrect attempts and fading reinforcement. Revision Session / Flashcard Review evidence closes the retention loop.

## Notifications

**Benefit:** Timely prompts from due reviews, expiring recommendations, and deadline pressure — tempered by Notification Engagement and Motivation/burnout evidence so nagging does not become product failure.

## Recommendation Engine

**Benefit:** Ranks next actions from full Twin state with Recommendation and Explainability contracts. Decision Journal evidence personalises alternatives without creating a parallel learner model.

## Predictions (Prediction Engine)

**Benefit:** Forecasts pass probability, retention, completion, burnout, and deadline risk strictly from Twin domains that evidence has shaped — with confidence intervals reflecting evidence density.

## Burnout Monitor

**Benefit:** Intensity flags from Time On Task, Mission load, Session Abandoned patterns, and check-ins — constraining Missions and Planning toward sustainable intensity.

---

# Evidence Producers

Producers **emit** evidence. Every producer must set source, provenance, and curriculum references when applicable.

| Producer | Typical evidence emitted |
|---|---|
| **Questions** | Question Attempt/Correct/Incorrect, Question Difficulty, Hint Requested |
| **Quizzes** | Quiz Completed, constituent attempt evidence |
| **Mocks** | Mock Exam, section/topic performance slices |
| **Past Papers** | Past Paper Attempt |
| **Study Sessions** | Study Session, Topic Started/Completed, Time On Task, Session Abandoned, Study Break |
| **Flashcards** | Flashcard Review |
| **AI Tutor / AI Coach** | AI Tutor Interaction; optional Reflection Journal (user-confirmed); never silent Knowledge writes |
| **Revision** | Revision Session, Flashcard Review, related Time On Task |
| **Missions** | Mission Completed, Mission Missed, task-level Learning Activity |
| **Planning / Wizard** | Plan Rescheduled, Manual Goal Change, Exam Date Change, Topic Started/Completed |
| **Manual Updates** | Confidence Rating, Manual Goal Change, Exam Date Change, Reflection Journal, Post-Exam Outcome |
| **Notifications** | Daily Check-in prompts, Notification Engagement |
| **Readiness surfaces** | Readiness Review |
| **Recommendation / Decision Journal** | Recommendation Decision (accept/dismiss) |
| **Diagnostics** | Diagnostic Assessment |
| **System / platform** | Mission expiry, automatic rebalance records, cold-start markers (System Events) |
| **Future Integrations** | Institution feedback, calendar sync, wearables, peer collaboration, voice tutoring, eye-tracking (Future Sensors) |

**Producer rules**

1. Producers create evidence; they do not directly patch Twin Knowledge fields.
2. Assistive AI proposes; Assessment producers confirm learning outcomes.
3. Future Integrations remain Low/Unknown confidence until validated.
4. Cross-student evidence is forbidden in a student’s Knowledge path (security tenancy).

---

# Explainability

Every recommendation should be traceable back to evidence. Explainability is an acceptance criterion for core paths, not polish ([`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md); [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) Explainability Contract).

## How Kwalitec explains decisions

1. **Factor citation** — Recommendations expose reason codes (weight, overdue, gap, deadline, workload) grounded in Twin domains.
2. **Evidence lineage** — Those Twin domains must be reconstructible from Evidence Log aggregates (e.g. “overdue” ← Memory ← failed Flashcard Reviews / elapsed time since Question Correct).
3. **Decision Journal** — Accept/dismiss stores preference evidence and preserves why an alternative was offered.
4. **Quality honesty** — Narratives disclose weak evidence (“based on two practice questions, not a mock”).
5. **AI phrasing ≠ AI ranking** — Coach may word explanations but must cite the same factors the deterministic engines used.
6. **No orphan recommendations** — If an engine cannot answer “why this topic / why today / why not another?” the recommendation is not shippable in the core path.
7. **Auditability** — Support and the student can inspect the evidence trail that justified a readiness warning or mission priority.

### Traceability chain

```
Recommendation / Prediction / Readiness claim
        ↓
Twin domain factors (Knowledge, Memory, Behaviour, …)
        ↓
Evidence aggregates (by type, topic, time window, confidence)
        ↓
Individual immutable evidence records
```

---

# Privacy

Principles only — not a legal policy text.

1. **Evidence belongs to the student.**  
   Learning history is part of the student’s educational record within Kwalitec, not a free-floating training corpus for unrelated purposes.

2. **Evidence is auditable.**  
   Students (and authorised support under policy) can reconstruct what the system believed and why.

3. **Students can inspect evidence.**  
   Product surfaces should allow inspection of material evidence contributing to Twin beliefs and recommendations, with quality/confidence context.

4. **PII is separated from learning evidence where practical.**  
   Auth secrets, payment data, and unnecessary identity attributes do not belong in Evidence payloads. Twin Identity binds the log; evidence bodies carry learning semantics.

5. **Tenancy is strict.**  
   Evidence reads/writes are scoped to the authenticated student; no cross-student leakage ([`.cursor/rules/10-security.mdc`](.cursor/rules/10-security.mdc)).

6. **Institution overlays (future) do not seize ownership.**  
   Cohort insights are projections; the student Twin and Evidence Log remain student-owned ([`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) Future Evolution).

7. **Erasure and export are governed processes.**  
   Legal deletion requests are explicit workflows — not ad-hoc overwrites that destroy auditability without accountability.

8. **Future Sensors are privacy-sensitive by default.**  
   Eye-tracking, voice, wearables require heightened consent and minimisation before influencing Knowledge.

---

# Future Evolution

Possible future evidence sources — admitted only through the same immutability, attribution, quality, and Twin-update rules:

| Future source | Category | Notes |
|---|---|---|
| **Eye-tracking** | Future Sensors | Attention proxies; High privacy sensitivity; start Unknown/Low |
| **Voice tutoring** | Future Sensors / AI Tutor | Dialogue + optional graded follow-ups as Assessment |
| **Wearables** | Future Sensors | Fatigue/stress proxies for Motivation — not mastery |
| **Institution feedback** | Future Integrations | Coach observations; must not silently override Assessment |
| **Peer collaboration** | Future Sensors / Engagement | Attendance/behaviour; Knowledge remains individual |
| **Calendar integration** | Planning / Time | Availability truth; Plan Rescheduled automation |
| **Learning groups** | Engagement | Cohort activity; privacy-preserving aggregates only |
| **Richer item banks** | Assessment | Objective- and item-level Performance/Memory |
| **Outcome calibration** | Assessment / System | Post-Exam Outcome improves Predictions |

Non-goals remain those in [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md): no black-box path ownership, no parallel syllabus invention, no vanity-metric-driven Twin mutations disguised as evidence.

---

# Architectural Rules

These rules are **non-negotiable** for evidence-related work.

1. **Evidence is immutable.**  
   No in-place edits of meaning. Corrections are compensating events.

2. **Evidence is append-only.**  
   The Evidence Log grows; it is not rewritten for convenience.

3. **Evidence is timestamped.**  
   Every record has a reliable event time for lifecycle, freshness, and determinism.

4. **Evidence updates the Twin.**  
   Material evidence flows through Twin domain updates before Predictions and Recommendations change.

5. **Evidence never bypasses the Twin.**  
   Forbidden: Missions, Analytics, or AI Coach maintaining private mastery that diverges from Twin Knowledge.

6. **Evidence is explainable.**  
   Downstream decisions must be able to cite evidence lineage.

7. **Evidence must be attributable.**  
   Student, source subsystem, provenance, and curriculum identity (when scoped) are mandatory concepts.

8. **Curriculum identity is canonical.**  
   Topic-scoped evidence uses official entities and canonical traversal ([ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md)); V1 and V2 both remain valid ([ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md)).

9. **Deterministic cores stay deterministic.**  
   Same evidence + Twin snapshot → same core updates and consumer outputs ([`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)).

10. **Service layer owns evidence application.**  
    Blueprints do not compute Twin updates from raw events ([ADR-001](knowledge/architecture/ADR-001-service-layer.md), [ADR-002](knowledge/architecture/ADR-002-blueprint-architecture.md)).

11. **AI cannot invent evidence or syllabus order.**  
    Assistive only; assessed results enter through Assessment producers.

12. **One Evidence Log per student Twin.**  
    Multi-exam context is scoped inside the Twin/Goals — not duplicate conflicting logs that fight.

13. **Analytics is not an evidence authority.**  
    It consumes; it does not redefine readiness or mastery.

14. **Security and tenancy.**  
    Evidence is student-scoped; secrets never appear in evidence payloads.

---

# Diagrams

## 1. Evidence lifecycle

```
Student Action
      ↓
Evidence Created ──► (reject / flag if invalid)
      ↓
Validated
      ↓
Stored (append-only Evidence Log)
      ↓
Digital Twin Updated (domain beliefs)
      ↓
Predictions Updated
      ↓
Recommendations Updated → Plan / Mission / Notify / Coach
      ↓
Evidence Archived (retention tier; meaning preserved)
```

## 2. Evidence flow

```
                ┌────────────┐
                │  Student   │
                └─────┬──────┘
                      │
                      ▼
                ┌────────────┐
                │Interaction │
                └─────┬──────┘
                      │
                      ▼
                ┌────────────┐
                │  Evidence  │
                └─────┬──────┘
                      │
                      ▼
                ┌────────────┐
                │Digital Twin│
                └─────┬──────┘
                      │
                      ▼
                ┌────────────┐
                │ Predictions│
                └─────┬──────┘
                      │
                      ▼
                ┌────────────┐
                │Recommend.  │
                └─────┬──────┘
                      │
                      └───────► Student
```

## 3. Evidence classification

```
                    Learning Evidence
                           │
       ┌───────────┬───────┼───────┬───────────┐
       ▼           ▼       ▼       ▼           ▼
   Learning    Assessment  Time  Confidence  Revision
   Activity
       │           │       │       │           │
       ▼           ▼       ▼       ▼           ▼
   Behaviour   Planning  Engagement  System   Future
                           Events            Sensors
```

## 4. Evidence ownership

```
┌─────────────────────────────────────────────────────────┐
│                     Student (owner)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Student Digital Twin                  │  │
│  │                   ▲                                │  │
│  │                   │ updates                        │  │
│  │         ┌─────────┴─────────┐                      │  │
│  │         │   Evidence Log    │  ← student-scoped    │  │
│  │         └─────────▲─────────┘                      │  │
│  └───────────────────┼────────────────────────────────┘  │
└──────────────────────┼──────────────────────────────────┘
                       │ emit (attributable)
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Producers      Validators     Consumers
   (write)         (gate)         (read via Twin)
```

Institution/coach views (future) are **projections**, not owners of the Evidence Log.

## 5. Evidence → Twin relationship

```
 Evidence types (examples)
 Session / Answer / Quiz / Mock / Mission / Revision /
 Skip / Confidence / Time / Goal change / Decision
                         │
                         ▼
              ┌────────────────────┐
              │  Append Evidence    │
              └─────────┬──────────┘
                        │
    ┌──────────┬────────┼────────┬──────────┬─────────┐
    ▼          ▼        ▼        ▼          ▼         ▼
Knowledge   Memory  Behaviour Performance Motivation Goals
    │          │        │        │          │         │
    └──────────┴────────┴────┬───┴──────────┴─────────┘
                             ▼
                  Readiness / Planning (derived)
                             ▼
                        Predictions
                             ▼
                      Recommendations
```

---

# Quality Expectations

This specification is an enterprise architecture artefact for Kwalitec’s Student Intelligence Platform.

**Authors and implementers must:**

- Prefer Kwalitec terminology from the [glossary](knowledge/development/glossary.md)
- Treat [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) as the learner-state authority and this document as the evidence authority that feeds it
- Cross-check product intent against [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md)
- Cross-check layering against [`ARCHITECTURE.md`](ARCHITECTURE.md) and ADRs under [`knowledge/architecture/`](knowledge/architecture/)
- Keep V1/V2 curriculum compatibility explicit for topic-scoped evidence
- Treat explainability, immutability, and determinism as acceptance criteria

**Authors and implementers must not:**

- Treat this document as permission to redesign the database in the same milestone
- Introduce LLM calls into core evidence application or recommendation paths
- Equate “mission completion” or “time on task” with mastery
- Allow Analytics or AI Coach to define private mastery stores
- Invent weighting formulas here and call them product law without a later, reviewed decision

---

# Related documents

| Document | Relationship |
|---|---|
| [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) | Learner-state authority; Evidence Log; Recommendation/Prediction/Explainability contracts |
| [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) | Product vision, principles, AI Coach non-goals |
| [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) | Engineering orientation, deterministic thesis, service map |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layering, curriculum engine, service dependency flow |
| [`knowledge/README.md`](knowledge/README.md) | Knowledge base index |
| [ADR-001](knowledge/architecture/ADR-001-service-layer.md) | Business logic in services |
| [ADR-002](knowledge/architecture/ADR-002-blueprint-architecture.md) | Thin HTTP blueprints |
| [ADR-003](knowledge/architecture/ADR-003-curriculum-v1-v2.md) | Dual curriculum formats |
| [ADR-004](knowledge/architecture/ADR-004-canonical-topic-traversal.md) | Single topic ordering path |
| [ADR-005](knowledge/architecture/ADR-005-testing-strategy.md) | Test expectations for future evidence/Twin implementation |
| Subsystem docs | [study-planning](knowledge/subsystems/study-planning.md), [missions](knowledge/subsystems/missions.md), [readiness](knowledge/subsystems/readiness.md), [analytics](knowledge/subsystems/analytics.md) |

---

# Document governance

- **Canonical for:** Learning Evidence conceptual model — categories, catalogue semantics, quality, confidence, weighting principles, lifecycle, producers/consumers, and architectural rules  
- **Not canonical for:** ORM schema, HTTP APIs, or numeric weighting coefficients  
- Conflicts with Core Product Principles in [`PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md) are resolved in favour of the blueprint unless this document is explicitly revised  
- Conflicts with Twin authority in [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) are resolved in favour of the Twin for learner *state*; this document remains authoritative for evidence *semantics* that feed the Twin  
- Future Epic 0 capabilities and implementation milestones must cite this document and preserve its architectural rules  

---

*End of Learning Evidence Model specification — Epic 0 / Capability 0.2*
