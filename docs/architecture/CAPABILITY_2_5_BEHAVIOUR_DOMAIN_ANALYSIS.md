# Capability 2.5 — Behaviour Domain Analysis

**Status:** Educational / architecture analysis — analysis only  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.5 Behaviour Update Strategy (analysis milestone preceding implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Domain definition, boundaries, evidence ownership, and relationships — **no implementation, code, tests, schema, or services**

---

## Document purpose

This milestone answers what **Behaviour** is inside the Student Digital Twin, what it may and must not own, how evidence updates it, and how it relates to Knowledge, Memory, Performance, and Readiness.

It prepares Capability 2.5 implementation (`BehaviourUpdateStrategy`) the same way Knowledge (2.3) and Memory (2.4) were prepared: **architecture and educational clarity first**, structural write path later, scoring algorithms deferred.

**Non-goals of this document**

- Code, pseudocode algorithms, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete adherence / consistency / burnout formulas  
- UI redesign, gamification, streaks-as-product, notifications, or social features  
- Replacement of Curriculum Engine, Evidence Model, or Twin aggregate contracts  

---

# 1. Definition of Behaviour

## 1.1 Canonical question

> **How does the student actually study?**

Not: what they know (Knowledge).  
Not: whether they will still know it (Memory).  
Not: how they score under assessment (Performance).  
Not: whether they feel ready (Confidence).  
Not: whether they are on track to pass (Readiness).  
Not: what they should do next (Decision Engine).

## 1.2 Educational meaning

**Behaviour** is the Twin domain that represents the student’s **study practice patterns**: cadence, completion and skip habits, time-on-task structure, adherence of planned vs actual study, and preference signals revealed by recommendation accept/dismiss.

In Epic 2 language:

| Concept | Relation to Behaviour |
|---|---|
| **Study** | Time and activity with content — Behaviour’s primary raw material |
| **Activity** | Engagement events — Behaviour’s typical evidence shape |
| **Motivation** | Willingness / sustainability — related signal that Behaviour may *surface* as pattern risk; Motivation is not collapsed into Behaviour ownership |
| **Learning** | Durable Knowledge/Memory change — Behaviour enables learning conditions; it does **not** certify learning |

Governing principle (Educational Intelligence Architecture §13):

> **Behaviour is not learning; Activity is not readiness.**

## 1.3 Product purpose

Behaviour exists so Kwalitec can:

1. Keep plans and missions **realistic** against observed capacity and adherence.  
2. Supply **feasibility** constraints to the Decision Engine (sustainable intensity, skip risk).  
3. Contribute a **pace / consistency factor** to Readiness Aggregation — without equating mission completion with exam readiness.  
4. Close the recommendation loop: accept/dismiss becomes attributable Behaviour (and Decision State) evidence.  
5. Support later Predictions (completion forecast, burnout risk) from structural behavioural facts — without inventing those forecasts inside Behaviour itself.

## 1.4 Ubiquitous language anchors

| Term | Meaning |
|---|---|
| **Behaviour** | Twin domain of how the student actually studies |
| **Consistency** | Sustainable, regular engagement over time — adherence without destructive overwork; distinct from streak theatre |
| **Learning Velocity** | Pace of coverage/mastery gain relative to time invested (Performance/Behaviour-derived later; not owned as mastery by Behaviour) |
| **Mission Completion / Miss** | Behavioural adherence facts; not mastery grants or penalties |

---

# 2. Responsibilities

Behaviour **owns** the educational concern of **study practice structure and adherence facts** inside the Twin.

## 2.1 Owns

| Responsibility | Notes |
|---|---|
| **Consistency structure** | Structural place for consistency / adherence metrics (values may be supplied later; computation deferred) |
| **Session lineage** | References to study session history / session-shaped evidence |
| **Pattern lineage** | References to study-pattern records or pattern-tagged evidence aggregates |
| **Adherence-related structural facts** | Completions, misses, skips, abandons, planned-vs-actual signals as *referenced* evidence — not as a private mission store |
| **Preference / response signals (structural)** | Recommendation accept/dismiss as secondary Behaviour evidence (Decision State remains primary for decision audit) |
| **Temporal study structure (structural)** | Time-on-task, breaks, quiet-hour engagement references when collected |
| **Update ownership** | Future `BehaviourUpdateStrategy` evolves `BehaviourState` from Learning Evidence via the Twin Update Pipeline |

## 2.2 Typical primary evidence (from ownership matrix)

- Mission completed / missed  
- Skipped / abandoned session  
- Time on task / study break  
- (Secondary) Recommendation accept/dismiss  
- (Secondary) Plan reschedule when user-initiated slip is behavioural  
- (Secondary) Assessment or revision events as *session activity* signals only — never as mastery ownership

## 2.3 Downstream consumers (read-only of Behaviour)

| Consumer | Uses Behaviour for |
|---|---|
| **Goals / Planning consequences** | Capacity realism; rebalance when adherence slips |
| **Decision Engine** | Feasibility, intensity demotion, burnout/skip flags |
| **Readiness Aggregation** | Pace / consistency factor |
| **Mission Generation Intelligence** | Load tuning; avoid over-ambition given observed reliability |
| **Predictions (later)** | Completion forecast; burnout risk features |
| **Insight / Coach (later)** | Narrate habits (“you tend to skip Friday reviews”) without rewriting mastery |

## 2.4 Write-path responsibility

Behaviour beliefs and structural slots change **only** through:

```
Learning Evidence → Twin Update Pipeline → BehaviourUpdateStrategy → new BehaviourState in new Twin snapshot
```

No mission service, dashboard, or recommendation packager may write Behaviour “truth” outside that path.

---

# 3. Non-responsibilities

Behaviour must **not** own or silently become:

| Non-responsibility | Why |
|---|---|
| **Mastery / Knowledge beliefs** | Completing a mission ≠ knowing a topic |
| **Retention / Memory beliefs or clocks** | Revision discipline *affects* Memory via Memory’s own strategy; Behaviour does not store `retention_belief` |
| **Performance scoring** | Assessment outcomes belong to Performance (+ Knowledge) |
| **Exam pass probability or readiness composite** | Readiness is derived; Behaviour is one input factor only |
| **Next-action selection** | Decision Engine owns selection; Behaviour supplies feasibility |
| **Curriculum structure or weights** | Curriculum Engine remains syllabus truth |
| **Mission / plan persistence as learner model** | Missions are projections; Behaviour references evidence about them |
| **Streak gamification as educational authority** | Consistency ≠ longest badge; unsustainable streaks are failures, not wins |
| **Personality / learning-style taxonomy** | Behaviour is evidence of practice, not a quiz identity |
| **Motivation domain wholesale** | Burnout/energy may be *inferred from* Behaviour patterns later; Motivation remains separable where productised |
| **Confidence calibration math** | Confidence is separable; self-report is Confidence-primary |
| **Persistence, HTTP, Flask, ORM** | Domain strategies stay framework-free |
| **Inventing syllabus topics** | Behaviour may be topic-tagged when evidence is; it does not create curriculum identity |

**Hard educational rule:** Behaviour never grants or revokes mastery by itself.

---

# 4. Behaviour state

## 4.1 Position in the Twin

`BehaviourState` is a first-class domain inside the Student Digital Twin aggregate, alongside Knowledge, Memory, Performance, Confidence (separable), Goals, Identity, and Prediction snapshots.

It is:

- **evidence-backed** — evolved from Learning Evidence;  
- **immutable per snapshot** — updates produce new Twin snapshots;  
- **structural-first** — slots and references before scoring algorithms;  
- **curriculum-optional** — many Behaviour facts are session/mission scoped rather than topic-slot scoped (unlike Knowledge/Memory topic records).

## 4.2 Structural shape (conceptual — already present as Twin vocabulary)

The Twin already exposes a structural `BehaviourState` contract conceptually aligned with:

| Structural field | Educational role |
|---|---|
| **consistency_metrics** | Named bag for later adherence/consistency values — **not computed by domain analysis**; storage-ready structure only |
| **session_history_ids** | Lineage to session / activity evidence or history records |
| **study_pattern_ids** | Lineage to pattern aggregates (cadence, skip clusters, timing preferences) |
| **last_updated** | Materialisation timestamp for the Behaviour snapshot |

This analysis does **not** redesign that contract. Implementation of Capability 2.5 should prefer **additive** structural evolution if new references are required (e.g. explicit evidence id lists), consistent with Knowledge/Memory additive practice.

## 4.3 What Behaviour state is *not*

- Not a dashboard cache of “hours this week” UI widgets  
- Not a competing store of mission rows  
- Not a parallel readiness score  
- Not a mutable streak counter that bypasses evidence  

## 4.4 Topic scoping note

Knowledge and Memory are primarily **per-topic** structural slots.

Behaviour is primarily **practice-pattern** state:

- Often student/sitting scoped (cadence, adherence).  
- May carry topic or mission references when evidence is tagged.  
- Must not invent per-topic mastery under Behaviour labels.

---

# 5. Behaviour evidence

## 5.1 Ownership relative to Learning Evidence

Learning Evidence is the immutable history. BehaviourState is derived Twin state.

From the Educational Intelligence **Evidence Ownership Matrix**:

| Evidence type (illustrative) | Behaviour role |
|---|---|
| Mission completed / missed | **Primary** |
| Skipped / abandoned session | **Primary** |
| Time on task / study break | **Primary** |
| Recommendation decision (accept/dismiss) | **Secondary** (Decision State primary) |
| Plan reschedule / goal change | **Secondary** when slip/capacity-related; Goals primary for goal facts |
| Question attempt / quiz / mock | **Secondary** (activity presence only); Knowledge/Performance primary |
| Revision / flashcard | **Secondary** (revision adherence); Memory primary |
| Confidence rating / readiness self-review | **Secondary**; Confidence primary |
| Post-exam outcome | **—** (not Behaviour-owned) |

## 5.2 Evidence quality principles for Behaviour

1. **Pattern over anecdote** — one skipped Friday is a slip; a month of Friday skips is a pattern. Structural updates may append references early; derived consistency later must require pattern context.  
2. **Completion ≠ learning** — mission completed is strong for adherence, weak for Knowledge unless nested Assessment evidence also arrives.  
3. **Time ≠ mastery** — time-on-task validates capacity and load; it does not prove Knowledge.  
4. **Attribution matters** — user skip vs system expiry vs interrupt; reason codes improve interpretation without changing ownership.  
5. **Secondary never steals primary** — a quiz may add a Behaviour session reference; it must not become Behaviour’s excuse to own Performance.  
6. **Append-only evidence ids** — domains reference evidence; they never rewrite the log.

## 5.3 Categories feeding Behaviour

From the Evidence Model categories most relevant to Behaviour:

| Category | Behaviour relevance |
|---|---|
| **Behaviour** | Core: starts, completions, skips, abandons, accept/dismiss |
| **Time** | Capacity validation, load, break structure |
| **Learning Activity** | Engagement/adherence; weak for Knowledge alone |
| **Engagement** | Check-ins, notification responses — aggregate consistency only |
| **Planning** | Reschedules / skipped planned sessions — secondary Behaviour when user slip |
| **System Events** | Mission expired uncompleted — Behaviour slip with `system` provenance |
| **Assessment / Revision** | Secondary session signals only |

## 5.4 Cold start

With little Behaviour evidence, Twin BehaviourState remains sparsely populated. Decision Engine and Planning must treat missing Behaviour as **explicit low confidence / default feasibility**, not as “perfect adherence” or “hopeless inconsistency.”

---

# 6. Behaviour events

“Events” here means **educationally meaningful occurrences** that become Learning Evidence and may move Behaviour — not implementation event buses.

## 6.1 Primary Behaviour events

| Event | Educational meaning | Twin effect (architectural) |
|---|---|---|
| **Mission completed** | Planned study unit finished per product rules | Strengthens adherence lineage; may update session/pattern references |
| **Mission missed / expired** | Window closed without completion | Records slip; pattern context decides overload vs avoidance later |
| **Skipped session** | Explicit or inferred skip of planned study | Adherence slip; deadline/pace risk input |
| **Session abandoned** | Started then closed without success criteria | Friction or avoidance signal; pattern-sensitive |
| **Study session started/completed** | Learning activity block engaged | Session lineage; effort presence |
| **Time on task recorded** | Duration associated with session/task | Capacity and load structure |
| **Study break** | Intentional recovery | Sustainability signal; not a Knowledge event |

## 6.2 Secondary Behaviour events

| Event | Primary owner | Behaviour role |
|---|---|---|
| **Recommendation accept / dismiss** | Decision State | Preference / compliance signal |
| **Plan rescheduled** | Goals / Planning | Slip or flexibility signal when user-initiated |
| **Daily check-in / notification response** | Engagement | Weak consistency aggregate |
| **Assessment or revision session** | Performance / Knowledge / Memory | Secondary activity presence |

## 6.3 Non-events for Behaviour ownership

These may occur in product flows but must **not** be treated as Behaviour granting educational learning state:

- Viewing a dashboard  
- Opening a recommendation without accept/dismiss evidence  
- Cosmetic streak increments without underlying evidence  
- Coach narration without confirmed student action  

## 6.4 Event → evidence → strategy chain (architectural)

```
Student / system occurrence
      → Learning Evidence (append-only, typed, attributable)
            → TwinUpdatePipeline
                  → BehaviourUpdateStrategy (when supports)
                        → new BehaviourState inside new DigitalTwin snapshot
```

Outcomes of Decision Engine (accept/dismiss) re-enter this chain as evidence — they do not mutate Behaviour inside the Decision Engine itself.

---

# 7. Structural vs derived behaviour

Epic 2 repeats a proven Knowledge/Memory pattern: **structure first, beliefs later**.

## 7.1 Structural behaviour (Capability 2.5 target)

Structural Behaviour is what the Twin should be able to hold and evolve **without** committing to scoring:

- Evidence / session / pattern **references**  
- Materialisation **timestamps**  
- Optional **metric bag slots** that store values when a later engine supplies them — without computing them in the structural strategy  
- Immutable snapshot semantics  

Structural updates answer: *What behavioural evidence has been observed and linked?*

They intentionally do **not** answer: *Is this student “consistent enough”?* with a productised score.

## 7.2 Derived behaviour (deferred)

Derived Behaviour is computed later by dedicated consumers or enriched strategies:

| Derived concept | Likely future owner | Notes |
|---|---|---|
| **Consistency score / quality** | Behaviour enrichment or Prediction features | Sustainable regularity ≠ streak length |
| **Adherence ratio** | Planning / Behaviour metrics | Planned vs completed over a window |
| **Skip/abandon pattern clusters** | Pattern inference | Needs multi-event context |
| **Learning velocity (effort-adjusted)** | Cross-domain derivation | Must not redefine mastery |
| **Burnout risk** | Motivation / Predictions consuming Behaviour | Behaviour supplies volume/load facts |
| **Preferred study windows** | Notifications / Decision feasibility | Timing personalisation |

## 7.3 Boundary rules

1. Structural strategy must **preserve unknown metric fields** when not computing them (same discipline as `mastery_belief` / `retention_belief`).  
2. Derived metrics must remain **factorable and explainable** when shown to students or used in decisions.  
3. Derived Behaviour must **not** become a second readiness composite.  
4. Gamified “streak” UI, if ever added outside Epic 2, must remain a **projection** of evidence — never Twin authority.

## 7.4 Implementation implication (analysis only)

Capability 2.5 implementation should ship a **structural `BehaviourUpdateStrategy`**, analogous to Knowledge/Memory:

- `supports` on Behaviour-primary evidence types  
- append/update structural references and `last_updated`  
- no adherence formula, burnout model, or velocity math  

Numeric consistency engines remain deliberately unlocked (Educational Intelligence Architecture §11.3).

---

# 8. Relationship with Knowledge

## 8.1 Complementary questions

| Domain | Question |
|---|---|
| **Knowledge** | What does the student know *now*? |
| **Behaviour** | How does the student actually study? |

## 8.2 Allowed interactions

- Behaviour can explain **why Knowledge coverage is slow** (chronic skips) without changing mastery beliefs.  
- Assessment-shaped sessions may update Knowledge **and** leave a secondary Behaviour activity reference.  
- Decision Engine may choose Knowledge-building actions only if Behaviour feasibility allows.

## 8.3 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| Mission completed → raise mastery | Completion ≠ assessed knowing |
| Time on task → mastery belief | Time ≠ learning |
| Behaviour streak → Knowledge “coverage complete” | Activity ≠ syllabus mastery |
| Knowledge strategy owns mission miss types | Steals Behaviour primary ownership |

## 8.4 Educational takeaway

Strong Behaviour with weak Knowledge means the student shows up but has not demonstrated learning.  
Strong Knowledge with weak Behaviour means assessed competence may be at risk from unsustainable or irregular practice — a Readiness/Decision concern, not a Knowledge rewrite.

---

# 9. Relationship with Memory

## 9.1 Complementary questions

| Domain | Question |
|---|---|
| **Memory** | Will the student still know it when it matters? |
| **Behaviour** | How does the student actually study (including revision discipline as practice)? |

## 9.2 Allowed interactions

- Architecture notes **Memory ↔ Behaviour**: revision discipline affects retention clocks — via **MemoryUpdateStrategy** when revision evidence arrives, not by Behaviour storing retention.  
- Chronic skip of revision missions is a Behaviour adherence fact that Decision Engine may use to prioritise feasible revision actions.  
- Revision sessions: Memory primary; Behaviour secondary (session adherence).

## 9.3 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| Behaviour stores `retention_belief` / `last_reinforced` | Domain collapse |
| Skipping revision directly decays Memory without Memory strategy | Bypasses ownership; skips are Behaviour, decay is Memory math |
| Treating flashcard reviews as Behaviour-only | Memory must remain primary owner |

## 9.4 Educational takeaway

Behaviour describes whether revision *happens*; Memory describes what revision *does* to retention structure. Keep those questions separate so explanations stay honest (“you skipped reviews” vs “retention risk is high”).

---

# 10. Relationship with Performance

## 10.1 Distinct questions

| Domain | Question |
|---|---|
| **Performance** | How does the student perform when assessed? |
| **Behaviour** | How does the student actually study day to day? |

## 10.2 Allowed interactions

- Quizzes/mocks: Performance (+ Knowledge) primary; Behaviour may record secondary session engagement.  
- Abandoned assessments: Behaviour (abandon) + incomplete Performance signal — dual update is valid; ownership remains split.  
- Decision Engine uses Performance weakness for *what* to practise and Behaviour for *how hard / how soon* is feasible.

## 10.3 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| High mission adherence → “strong Performance” | Adherence ≠ assessed accuracy |
| Collapsing Performance into Behaviour “study quality” | Hides assessment trends |
| Behaviour owns mock score summaries | Performance domain exists precisely to prevent that collapse |

## 10.4 Educational takeaway

A student can complete every mission and still fail mocks (activity without learning).  
A student can score well on sparse assessments and still show fragile Behaviour (unsustainable or irregular practice). Both must remain visible as separate Twin factors.

---

# 11. Relationship with Readiness

## 11.1 Readiness is derived

Readiness answers: *Are we on track to pass?*  
Behaviour answers: *How does the student actually study?*

Readiness Aggregation (Capability 2.7) consumes Behaviour as **one factor class** among:

```
Curriculum weights + Knowledge + Memory + Performance
+ Behaviour consistency / pace
+ Confidence calibration (optional)
+ Goals (exam date, capacity)
```

## 11.2 Behaviour’s contribution to Readiness

Architectural factor roles (names illustrative):

| Factor family | Behaviour contribution |
|---|---|
| **Pace / adherence** | Observed completion vs planned capacity |
| **Time pressure interaction** | Skips increase catch-up pressure against Goals deadline |
| **Sustainability** | Overwork + collapse patterns demote “on track” confidence even if short-term hours look high |

## 11.3 What Behaviour must not do to Readiness

- Emit the overall readiness composite inside BehaviourUpdateStrategy  
- Treat mission completion as equivalent to exam readiness (explicit Readiness non-goal)  
- Bypass factorability with a single opaque “behaviour score” that cannot be explained  

## 11.4 Decision Engine vs Readiness

| Concern | Owner | Behaviour’s role |
|---|---|---|
| On track for sitting? | Readiness Aggregation | Pace/consistency factor |
| What to do in the next session? | Decision Engine | Feasibility / intensity constraint |

Same BehaviourState; different read-side questions. Do not conflate them.

---

# 12. Example scenarios

## 12.1 Steady adherent, thin assessment

**Situation:** Student completes missions five days/week for three weeks; almost no quizzes.

**Twin reading:** Behaviour structural adherence lineage is rich; Knowledge/Performance remain sparse.

**Correct intelligence:** Do not declare readiness from Behaviour. Decision Engine should favour assessment-shaped actions that create Knowledge/Performance evidence, within Behaviour feasibility.

## 12.2 Chronic Friday skips

**Situation:** Revision missions scheduled Friday repeatedly missed; weekday learn tasks completed.

**Twin reading:** Behaviour shows a skip pattern; Memory may show stale `last_reinforced` on topics that only appear in Friday revisions.

**Correct intelligence:** Explain separately — Behaviour (“Friday revision often skipped”) and Memory (“Topic T last reinforced 28 days ago”). Decision may move revision to a historically completed window rather than inventing mastery loss from the skip alone.

## 12.3 Mission complete with embedded quiz

**Situation:** Daily mission includes a scored quiz on Topic T; student completes the mission.

**Twin reading:** Mixed batch — Behaviour primary for mission completed; Knowledge + Performance primary for quiz outcomes.

**Correct intelligence:** Dual strategy application is valid. Mission completion must not overwrite or replace quiz-driven Knowledge updates.

## 12.4 High hours, abandon spikes

**Situation:** Long time-on-task weekends; frequent mid-session abandons mid-week.

**Twin reading:** Behaviour shows volume without sustainable consistency.

**Correct intelligence:** Consistency ≠ maximum hours. Readiness/Decision should demote intensity and prefer shorter feasible actions; do not reward abandon-prone overload as “commitment.”

## 12.5 Recommendation dismiss loop

**Situation:** Student repeatedly dismisses “revise Topic T” recommendations.

**Twin reading:** Decision State records candidates/outcomes; Behaviour receives secondary preference/compliance signals.

**Correct intelligence:** Future Decision Engine may change framing, timing, or alternatives — not silently raise or lower mastery. Accept/dismiss never grants Knowledge.

## 12.6 Cold-start student

**Situation:** New Twin; Goals set; no sessions yet.

**Twin reading:** Empty Behaviour references; unknown consistency.

**Correct intelligence:** Explicit defaults and low confidence for Behaviour factors; avoid both optimistic “perfect adherence” and punitive “unreliable” labels.

## 12.7 Strong mocks, irregular practice

**Situation:** Strong Performance on mocks; irregular mission adherence.

**Twin reading:** Performance/Knowledge optimistic relative to Behaviour pace risk vs remaining calendar.

**Correct intelligence:** Readiness may still flag time/pace risk. Decision Engine balances retention/coverage needs against feasibility — Behaviour constrains ambition without erasing Performance evidence.

---

# 13. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| **Equating Behaviour with learning** | False mastery; broken trust | Hard rule: Behaviour never grants mastery; ownership matrix |
| **Equating Behaviour with readiness** | Mission theatre replaces exam preparedness | Readiness derived multi-factor; explicit non-equivalence |
| **Domain collapse into Motivation** | Unexplainable “engagement score” | Keep Motivation separable; Behaviour holds practice facts |
| **Streak / gamification capture** | Unsustainable intensity rewarded | Consistency ≠ streak; educational fidelity over engagement theatre |
| **Mission rows as Behaviour authority** | Stale private state | Missions are projections; evidence → strategy → Twin |
| **Single-skip overreaction** | Noisy coaching and plan thrash | Pattern-over-anecdote for derived metrics |
| **Secondary evidence theft** | Behaviour absorbs quizzes/revisions | Primary columns remain Knowledge/Memory/Performance |
| **Strategy order hazards** | Non-reproducible updates when mixed batches arrive | Document registration order in Capability 2.5 implementation notes |
| **Premature scoring complexity** | Unmaintainable adherence math before structure settles | Structural strategy first; derived metrics later |
| **Confidence/Behaviour conflation** | Self-report treated as habit truth or vice versa | Confidence separable; ratings Confidence-primary |
| **Parallel learner-state in analytics** | Divergent “engagement readiness” | Analytics read Twin; do not fork Behaviour formulas |
| **LLM habit invention** | Fabricated skip reasons / patterns | Coach narrates Twin+evidence only |
| **V1/V2 irrelevance mistaken for exemption** | Inventing topic trees for Behaviour | Behaviour remains curriculum-referenced when topic-tagged; never invents syllabus |

---

# 14. Future extensibility

## 14.1 Safe extension points

| Extension | How to extend safely |
|---|---|
| **`BehaviourUpdateStrategy`** | Register with Twin Update Pipeline; framework-free; immutable snapshots |
| **Richer consistency metrics** | Fill `consistency_metrics` via later engines; keep structural slots stable |
| **New Behaviour evidence types** | Add to Evidence catalogue; assign primary/secondary in ownership matrix |
| **Pattern inference** | Derive pattern ids from evidence aggregates; store references, not opaque blobs without lineage |
| **Context tags** | Commute vs deep work; device patterns — additive metadata on evidence |
| **Collaboration attendance** | Optional Behaviour evidence; Knowledge remains individual |
| **Notification engagement** | Behaviour secondary; never Knowledge |
| **Burnout / Motivation models** | Consume Behaviour volume/load; do not overwrite Knowledge/Memory |
| **Prediction features** | Completion forecast / burnout risk read Behaviour; write via Prediction snapshot path only |

## 14.2 Compatibility guarantees to preserve

1. Curriculum V1 and V2 remain loadable; Behaviour must not require Sections globally.  
2. Structural Twin fields prefer additive optional fields over breaking renames.  
3. Evidence append-only semantics remain permanent.  
4. Deterministic cores remain free of required network LLM calls.  
5. Knowledge and Memory remain complementary mastery/retention stores — Behaviour must not become a third.

## 14.3 Deliberately unlocked

Not locked by this analysis beyond ownership:

- Exact adherence ratios and windows  
- Burnout probability models  
- Learning velocity formulas  
- Preferred-hour personalisation algorithms  
- Any gamification surface  

---

# 15. Recommendations

## 15.1 For Capability 2.5 next milestones

1. **Treat this analysis as the domain charter** for Behaviour before writing `BehaviourUpdateStrategy`.  
2. **Implement structural-only strategy first** — mirror Knowledge/Memory discipline: references, timestamps, preserve unknown metric fields, no scoring.  
3. **Fix evidence `supports` types explicitly** — primary: mission completed/missed, skip, abandon, time-on-task, study break; secondary types only with documented weak updates.  
4. **Document pipeline registration order** relative to Knowledge/Memory/Performance once Performance analysis exists (mixed batches must stay reproducible).  
5. **Do not expand Confidence into Behaviour** — keep Confidence separable even if some ratings appear as secondary Behaviour signals.  
6. **Keep missions as projections** — Mission Generation Intelligence consumes Behaviour; it does not own Behaviour truth.

## 15.2 Educational design recommendations

1. Prefer **explainable patterns** over punitive single-event messaging.  
2. Always separate “you showed up” from “you demonstrated learning.”  
3. Use Behaviour to **constrain ambition**, not to inflate readiness.  
4. When Friday skips and stale Memory co-occur, explain **both factors** in the chain — do not merge them into one opaque score.

## 15.3 Architecture compliance checklist

| Invariant | Status for Behaviour |
|---|---|
| Twin is sole educational state authority | BehaviourState lives only in Twin |
| Evidence is only legitimate belief input | Required |
| Strategies own domain evolution | `BehaviourUpdateStrategy` planned |
| Behaviour ≠ learning; activity ≠ readiness | Binding |
| V1/V2 curriculum compatibility | Behaviour must not invent syllabus or require V2-only structure |
| No implementation in this milestone | Satisfied by analysis-only deliverable |

## 15.4 Explicit stop line

This milestone delivers **analysis only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, or UI.

Next engineering step (separate milestone): Capability 2.5 architecture notes for `BehaviourUpdateStrategy` → structural implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Behaviour in the capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | BehaviourState already part of Twin vocabulary; pipeline will register Behaviour strategy later |
| 2.3–2.4 | Knowledge / Memory strategies | Structural precedents Behaviour must follow |
| **2.5** | **Behaviour Update Strategy** | **This analysis precedes implementation** |
| 2.6 | Performance | Distinct assessment domain; secondary Behaviour only |
| 2.7 | Readiness | Consumes Behaviour as pace/consistency factor |
| 2.8–2.10 | Decision / Recommendation / Missions | Read Behaviour for feasibility; write back via evidence |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.5 — Behaviour Domain Analysis |
| Nature | Architecture / educational analysis only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; Behaviour analysis introduces no traversal changes |
| Application code intentionally untouched | Yes |
| Next | Behaviour Update Strategy architecture → structural implementation (separate milestone) |

---

*End of Capability 2.5 Behaviour Domain Analysis.*
