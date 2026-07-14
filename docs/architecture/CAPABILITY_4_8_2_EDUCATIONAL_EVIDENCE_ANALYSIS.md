# Capability 4.8.2 — Educational Evidence Analysis

**Status:** Educational analysis only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.8.2 Educational Evidence Analysis (educational meaning of observations preceding Twin Update Strategies, Evidence contracts, and persistence)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream Evidence architecture:** [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Evidence companion (Epic 0 catalogue):** [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md)  
**Companions:** [`CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md`](CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md), [`CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md)  
**Scope:** Educational meaning of Educational Evidence — **no code, Flask, ORM, contracts, persistence schemas, product flows, UI, Twin Update algorithms, migrations, or tests**

---

## Document purpose

Capability 4.8.1 established Educational Evidence as the sole educational input that may evolve a Digital Twin. It defined purpose, ownership, philosophy, boundaries, and relationships with the Twin and Educational Intelligence.

This milestone analyses the **educational** meaning of that architecture.

It answers:

> What does Educational Evidence mean educationally, and why does Version 1.0 deliberately keep Evidence weaker than educational conclusions?

It protects the binding principle from 4.8.1:

> **Evidence records observations. It never records conclusions. The Twin evolves from Evidence — never from activity.**

**Architectural restatement:**

> **Educational Evidence is intentionally weaker than educational conclusions. Observation precedes interpretation. Educational Intelligence reasons from Twins that Evidence has earned the right to evolve — never from raw student activity.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Student activity** | Transient product events (missions, sessions, clicks, practice attempts, UI actions) |
| **Educational Evidence** | Permanent educational record of an observation derived from (or about) activity — not the activity itself |
| **Observation** | What was recorded as having occurred educationally |
| **Interpretation** | What Strategies and Intelligence conclude from Evidence + Twin |
| **Declared evidence** | Student-reported reflections / statements recorded as self-report observations |
| **Observed evidence** | System-recorded educational facts (completion, duration, practice, assessment result) |
| **Twin Update Strategy** | Lawful interpreter of Evidence that authors a successor Twin |
| **Educational judgement** | Mastery, readiness, pass probability, recommendations — never Evidence |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service designs, or package layouts  
- Flask routes, forms, templates, or product UX flows  
- Database schemas, Alembic migrations, ORM models, or Evidence persistence technology  
- Evidence contracts, APIs, or recorder implementations  
- Twin Update Strategy algorithms or Pipeline redesign  
- Readiness, Decision, Recommendation, Mission, or dashboard logic  
- Assessment interpretation engines or AI observation pipelines  

---

# 1. Educational problem

## 1.1 What Educational Evidence solves

Students perform activities. Activities are not automatically learning.

A student may complete a mission without understanding the topic. They may sit with materials open for forty minutes without durable knowledge change. They may answer practice questions by pattern-matching without conceptual grasp. They may write a confident reflection that misjudges their own understanding.

**Learning cannot be observed directly.** The product can observe behaviour, duration, completion, scores, and self-report. It cannot observe the internal state called “learned.” Treating activity as learning is the foundational educational falsehood of planner-first products.

Educational Intelligence therefore requires **observations** rather than **assumptions**:

| Without Evidence | With Evidence |
|---|---|
| “Mission done ⇒ student knows Topic 4.2” | “Mission completed for Topic 4.2 was recorded” |
| “Studied 40 minutes ⇒ understanding increased” | “Study duration of 40 minutes was observed” |
| “Practised 12 questions ⇒ mastered GLM” | “12 practice questions were attempted” |
| “Said they understood ⇒ readiness rose” | “Student reflection reported understanding (self-report)” |

The educational problem is not missing data. It is **epistemic discipline**: what may the platform honestly remember so that Twin evolution does not invent learning?

## 1.2 Why Version 1.0 captures observations instead of conclusions

Version 1.0 deliberately captures observations because conclusions are **premature at the Evidence layer**.

Conclusions such as mastery, retention, readiness, and pass probability require:

1. interpretation against prior Twin state;  
2. accumulation across multiple observations;  
3. curriculum-scoped warrant;  
4. explicit Strategy authorship of successor beliefs;  
5. later Educational Intelligence judgement from Twin state.

Writing those conclusions into Evidence would:

- collapse observation into judgement;  
- make the audit spine circular (Evidence “proves” what Evidence already concluded);  
- force every sparse Internal Alpha session to pretend denser educational knowledge than exists;  
- teach the product that one activity is enough to know the learner.

Observations are weaker than conclusions **on purpose**. Weakness here is educational honesty, not incompleteness of design.

Governing restatement:

> **Students act. Learning is not the act. Evidence records what was observed. Conclusions wait for interpretation.**

---

# 2. Activity versus Evidence

## 2.1 The distinction

```
Student Activity
        ↓
Educational Evidence
```

| | Student Activity | Educational Evidence |
|---|---|---|
| **Nature** | Transient product event | Permanent educational record |
| **Lifetime** | Session / UI / mission state | Append-only educational memory |
| **Authority over Twin** | None | Sole lawful evolution input (via Strategies) |
| **Educational question** | What did the product do / what did the student click? | What educational observation was recorded? |
| **May equal learning?** | Never automatically | Never — Evidence is still only observation |

**Educational Evidence is not the activity itself.** It is the educational record of that activity — the durable statement that an observation entered educational memory.

## 2.2 Activities that become Evidence only after educational recording

| Activity | Educational Evidence (after recording) | Still not a conclusion |
|---|---|---|
| **Mission completion** | Mission completed (observation) | Not mastery |
| **Study duration** | Duration observed in a session | Not understanding |
| **Practice questions** | Practice completed / attempts recorded | Not conceptual grasp |
| **Reflection** | Student reflection recorded (self-report) | Not validated confidence or truth |

Until educational recording occurs, activity remains **product behaviour**. It may matter for UX, analytics mirrors, or session continuity. It does not lawfully evolve the Twin.

After recording, Evidence exists as educational memory. Twin Update Strategies may interpret it. Educational Intelligence still must not consume the raw activity as Twin substitute.

## 2.3 Why the gap must remain

If activity and Evidence were the same artefact:

- every mission row would become Twin-mutation authority;  
- every click stream would compete with educational state;  
- every abandoned session could silently rewrite learner beliefs;  
- Internal Alpha product events would masquerade as educational truth.

The gap is the firewall:

> **Activity may generate Evidence. Evidence may justify Twin succession. Activity never shortcuts either step.**

Governing restatement:

> **Mission completion is an event. Educational Evidence is an educational observation. The record is not the act.**

---

# 3. Observation versus Interpretation

## 3.1 The separation

```
Observation
     ↓
Evidence
     ↓
Twin Update
     ↓
Educational Interpretation
```

| Layer | Educational verb | Owns |
|---|---|---|
| **Observation** | Notice what occurred | Facts eligible for recording |
| **Evidence** | Remember the observation permanently | Immutable educational memory |
| **Twin Update** | Interpret Evidence into successor Twin | Twin Update Strategies / Pipeline |
| **Educational Interpretation** | Judge from Twin (readiness, next action, mission) | Educational Intelligence |

Crossing these layers recreates study-planner pathology: completion mistaken for mastery, activity mistaken for readiness, sparse reflection mistaken for belief density.

## 3.2 Observed versus concluded — binding examples

| Observed (lawful Evidence) | Not observed (forbidden as Evidence) |
|---|---|
| Student completed Topic 4.2 (mission / topic-studied observation) | Student **mastered** Topic 4.2 |
| Student attempted 12 questions | Student **understands** Generalised Linear Models |
| Student studied for 35 minutes on Topic 3.1 | Student **retained** Topic 3.1 |
| Student abandoned a mission | Student **lacks motivation** |
| Student reflected “I understood this” | Student **is Mid on confidence / readiness** |
| Assessment result recorded for scoped items | Student **will pass** the sitting |

Observation answers: *What happened?*  
Interpretation answers: *What does that mean for learner beliefs and next action?*

Evidence owns the first. Twin Update Strategies and Educational Intelligence own the second — in that order.

## 3.3 Why Educational Intelligence reasons from Evidence-mediated Twins

Educational Intelligence must not reason from student activity because activity is:

- ephemeral;  
- product-shaped (UI affordances, not educational ontology);  
- unbound to Twin warrant;  
- easily mistaken for learning.

Intelligence consumes **Twins**. Twins evolve only when Strategies interpret **Evidence**. That mediation is how observation becomes educationally usable without becoming false certainty.

Governing restatement:

> **Observe → remember → interpret → judge. Never observe → judge.**

---

# 4. Educational honesty

## 4.1 Why Version 1.0 preserves uncertainty

Version 1.0 intentionally preserves uncertainty because early study behaviour does not license educational certainty.

Evidence should **never claim**:

| Forbidden Evidence claim | Why forbidden |
|---|---|
| **Mastery** | Knowledge belief — Strategy-owned interpretation |
| **Retention** | Memory belief — not a single-session observation |
| **Confidence** (as validated judgement) | Confidence domain / measured-vs-felt calibration — reflection may be Evidence; the score-as-truth is not |
| **Readiness** | Preparedness aggregation from Twin |
| **Preparedness** | Product restatement of readiness — not observation |
| **Motivation** (as diagnosis) | Behaviour / Motivation belief — not raw Evidence payload |
| **Pass probability** | Forecast — Predictions / later calibrated forecasting |

Preserving uncertainty means Evidence may accumulate while Twin beliefs remain thin, sparse, or empty where warrant does not yet exist. Sparse Evidence remains sparse. Weak observations remain weak.

## 4.2 Why uncertainty is educationally preferable to false certainty

False certainty fails students educationally:

1. **Misdirected study** — “mastered” topics stop receiving needed revisiting.  
2. **Trust collapse** — when mocks contradict product confidence, students learn the product lies.  
3. **Adaptive theatre** — recommendations change before warrant densifies, creating whiplash without learning gain.  
4. **Audit fiction** — explainability cites mastery that was never observed, only inferred too early.  
5. **Calibration corruption** — birth priors get “upgraded” by one session into Evidence-backed beliefs without Strategy honesty.

Uncertainty is not product weakness. It is **refusal to invent learning**.

Internal Alpha especially requires this humility: early cohorts will produce sparse, uneven observations. Treating sparse Evidence as dense educational knowledge would poison Twin evolution before Strategies are even designed carefully.

Governing restatement:

> **Honest unknown beats false known. Evidence that claims mastery has already stopped being Evidence.**

---

# 5. Declared versus Observed

## 5.1 Two valuable evidence postures

Educational Evidence in Version 1.0 includes both **student declarations recorded as observations** (notably reflection) and **system observations** (mission completion, duration, practice, assessment results).

| | Student declarations (as Evidence) | System observations |
|---|---|---|
| **Example** | “I understood the topic” (reflection) | Mission completed; duration; practice completed |
| **Source** | Student narrative / self-report | Platform-recorded educational fact |
| **Epistemic status** | Claim about experience | Observation of behaviour / outcome (within measurement limits) |
| **Value** | Surfaces felt understanding, friction, intent | Anchors what actually occurred in product study |
| **Risk if over-trusted** | Optimism, miscalibration, strategic framing | Completion theatre, time-on-task fallacy |
| **Tagging requirement** | Explicit self-report provenance | Explicit system / assessed provenance |

These differ from **Calibration declarations** at Twin birth (Capability 3.6): birth declarations are **priors**, not Educational Evidence. Post-birth reflections may become Evidence as self-report observations — still not mastery.

## 5.2 Why both are valuable

| Value of declarations (reflection) | Value of system observations |
|---|---|
| Reveal how the student *experiences* study | Reveal what the student *did* |
| Capture confidence, confusion, and friction the system cannot see | Provide attributable behavioural timeline |
| Support later measured-vs-felt calibration analyses | Support Strategy interpretation of engagement and practice |
| Keep the student voice inside educational memory | Keep autobiography from being the only spine |

A truthful system needs both. Self-report alone recreates optimistic planner pathology. System observation alone treats humans as clickstreams and ignores metacognition that later Strategies may interpret carefully.

## 5.3 Why they remain different educational evidence types

They answer different educational questions and carry different warrant:

- Declaration answers: *What does the student say about this study moment?*  
- Observation answers: *What did the system record as having occurred?*

Collapsing them would:

- treat “I understood” as equivalent to assessed performance;  
- treat mission completion as equivalent to felt mastery;  
- erase provenance needed for explainability;  
- force Strategies to apply one interpretation rule to epistemically unlike inputs.

Version 1.0 must keep provenance explicit. Value is shared; type identity is not.

Governing restatement (aligned with Capability 3.6.2):

> **Self-report is evidence when recorded as such — tagged and never promoted to assessed truth. System observation is evidence — never promoted to mastery by mere occurrence.**

Extended for Twin birth vs post-birth:

> **Calibration declarations birth priors. Post-birth reflections may enter Evidence as self-report. Neither is mastery.**

---

# 6. Educational unknowns

## 6.1 What remains intentionally unknown after one study session

After a single study session — even one that generated lawful Evidence — Version 1.0 intentionally leaves unknown:

| Unknown | Why unknown after one session |
|---|---|
| **Did learning occur?** | Activity and even scored practice do not equal durable knowledge change |
| **Will knowledge persist?** | Retention requires time-aware Memory interpretation across Evidence |
| **Will the student pass?** | Pass probability is a forecast, not an observation |
| **Should recommendations immediately change?** | Decision / Recommendation consume Twin state; one Evidence item may not warrant succession, or succession may not yet change Decision |
| **Has understanding increased?** | Understanding is interpretive belief, not a session flag |
| **Is the student more ready?** | Readiness aggregates Twin domains — not Evidence payloads |
| **Was the reflection accurate?** | Self-report warrant remains thin until contradicted or corroborated |
| **Which Twin domains should move?** | Strategy ownership — Evidence does not assign domain deltas |

## 6.2 Why these belong to later Educational Intelligence reasoning

These unknowns are not Evidence defects. They are **downstream educational questions**.

| Question family | Lawful owner |
|---|---|
| Belief evolution (knowledge, memory, behaviour, performance, confidence) | Twin Update Strategies interpreting Evidence |
| Preparedness for sitting | Readiness Aggregation from Twin |
| What to do next | Decision Engine from Twin (+ Curriculum / Goals / Constraints) |
| How to present that next action | Recommendation Engine |
| How to operationalise today | Mission Intelligence |
| Forecasts | Predictions / later calibrated forecasting |

Evidence’s job ends at honest memory of observation. Forcing Evidence to answer these unknowns would recreate conclusions-in-Evidence and premature adaptive behaviour.

Governing restatement:

> **One session creates observations. It does not close educational questions. Closing questions is interpretation over time.**

---

# 7. Relationship with Twin Update Strategies

## 7.1 Why Twin Update Strategies exist

Evidence answers only: *What was observed?*

Someone must answer: *Given prior Twin + this Evidence, what successor Twin is educationally warranted?*

That someone is **Twin Update Strategies** (via the Twin Update Pipeline). Strategies exist because:

1. **Evidence cannot reason** — observational records have no belief algebra.  
2. **Twins cannot self-mutate from activity** — immutability and succession law require an author.  
3. **Interpretation is contested educational policy** — how much a mission completion moves Knowledge (if at all) is Strategy responsibility, not Evidence payload.  
4. **Warrant must remain explicit** — Strategies decide whether Evidence densifies beliefs or leaves them thin.  
5. **Educational Intelligence must stay read-path pure** — Intelligence judges from Twins; it must not also be the silent writer of Twin beliefs from raw Evidence.

```
Evidence
    ↓
Interpretation (Twin Update Strategies)
    ↓
Successor Twin
```

## 7.2 Evidence never reasons

| Evidence may | Evidence must not |
|---|---|
| Record mission completed | Decide Knowledge is now Mid |
| Record duration | Decide Memory retention improved |
| Record practice completed | Decide Performance is exam-ready |
| Record reflection | Decide Confidence domain truth |
| Carry provenance and syllabus scope | Author successor Twin snapshots |

**Evidence itself never reasons.** Twin Update Strategies own educational interpretation that may evolve the Twin. Educational Intelligence then reasons from the Twin — not from Evidence as a substitute Twin, and not from activity.

Governing restatement (from 4.8.1, educationally reinforced):

> **Evidence never edits a Twin. Twin Update Strategies interpret Evidence. Twin snapshots remain immutable.**

---

# 8. Relationship with Internal Alpha

## 8.1 Why Internal Alpha collects Educational Evidence

Internal Alpha is active. Collecting Educational Evidence during Alpha is **not** a mandate to ship adaptive algorithms immediately.

Purpose of Evidence collection in Internal Alpha:

| Purpose | Meaning |
|---|---|
| **Validate what should count as educational evidence** | Which observations are educationally meaningful vs product noise |
| **Learn what students naturally provide** | Reflections, completions, practice patterns, abandonment, duration realities |
| **Judge observational usefulness** | Which observations later Strategies could honestly interpret |
| **Preserve honesty while Alpha runs** | Activity without Evidence remains Twin-inert; Birth Twin honesty survives |
| **Build educational memory before belief machines** | Append-only history before aggressive Twin evolution |

## 8.2 What Internal Alpha is not for (at Evidence layer)

Internal Alpha Evidence collection is **not** primarily for:

- immediate mastery maps;  
- instant recommendation whiplash from every session;  
- proving adaptive personalisation theatre;  
- seeding fake Evidence density from Calibration;  
- treating Alpha cohorts as already fully modelled learners.

Alpha validates the **observation layer**. Twin Update Strategies and denser Educational Intelligence evolution come after the educational meaning of Evidence is stable — this analysis and 4.8.1 are that foundation.

Governing restatement:

> **Internal Alpha remembers honestly before it adapts aggressively. Evidence first validates observation — not algorithms.**

---

# 9. Educational risks

| Risk | Failure mode | Educational harm | Mitigation principle |
|---|---|---|---|
| **Activity equals learning** | Mission/session treated as knowledge gain | False Twin evolution; skipped revision of weak topics | Activity → Evidence → Strategies only; Evidence stays observational |
| **Completion equals mastery** | “Mission completed” stored or read as mastered | Foundations abandoned without warrant | Never write mastery into Evidence; Strategies refuse single-completion Mid theatre |
| **Time equals understanding** | Duration Observation promoted to Knowledge | Long weak sessions rewarded as learning | Duration is observation only; interpretation elsewhere and cautious |
| **Reflection equals truth** | “I understood” becomes Confidence/Knowledge truth | Optimistic Twin; hidden gaps | Self-report tagged; thin warrant; never auto-mastery |
| **Low evidence equals failure** | Sparse Alpha Evidence treated as student deficiency | Shame, panic recommendations, false Behaviour diagnosis | Sparse remains sparse; absence of Evidence ≠ failure narrative |
| **Over-interpreting sparse evidence** | One session rewrites many Twin domains | Whiplash beliefs; audit fiction | Strategies require warrant density; Intelligence fails closed on thin Twin |
| **Premature adaptive behaviour** | Recommendations jump before Twin succession is warranted | Adaptive theatre without educational gain | Intelligence reads Twin only; no activity shortcut; Alpha collects before aggressive adapt |
| **Declared ≡ observed collapse** | Reflection and completion share one interpretation rule | Provenance erased; wrong Strategy maths | Keep evidence types distinct |
| **Conclusions smuggled into Evidence** | Readiness/pass % stored as Evidence | Circular proof; poisoned audit spine | Closed observational payload (4.8.1) |
| **Calibration seeded as Evidence** | Birth declarations rewritten as Evidence density | Fake warrant; Evidence sovereignty broken | Calibration remains priors-only |

### Risk restatement

The primary educational danger is not missing Evidence types. It is **Evidence that starts concluding**, or **activity that evolves the Twin without Evidence**, or **sparse Alpha observations over-interpreted into adaptive theatre**.

---

# 10. Version 1.0 recommendations

## 10.1 Remain intentionally conservative

Version 1.0 should remain intentionally conservative. Educational Evidence should remain:

| Property | Version 1.0 meaning |
|---|---|
| **Small** | Closed observation surfaces only (mission, session duration/topic, practice, reflection, assessment result as observation) |
| **Immutable** | Append-only; corrections are new records |
| **Observational** | No mastery, retention, confidence-as-truth, readiness, preparedness, motivation diagnosis, or pass probability |
| **Explainable** | Provenance and syllabus scope answer who / what / when / whence |
| **Traceable** | Twin succession may cite Evidence lineage; Intelligence cites Twin — not raw activity |

## 10.2 Enrich Twin reasoning, not Evidence itself

Future capabilities should enrich **Twin Update Strategies** and **Educational Intelligence** rather than thickening Evidence into a judgement engine.

| Evolve later | Do not evolve Evidence into |
|---|---|
| Strategy interpretation rules | Mastery fields inside Evidence |
| Warrant densification policy | Readiness computation |
| Additional observation classes (tutor, AI, richer behaviour) — still observational | Recommendation selection |
| Explainability lineage through Twin | Activity-fed Intelligence shortcuts |

## 10.3 Binding Version 1.0 recommendations

1. Keep Evidence weaker than conclusions — by design.  
2. Keep activity and Evidence as distinct artefacts.  
3. Keep observation and interpretation as distinct layers.  
4. Preserve uncertainty after single sessions.  
5. Treat declared reflections and system observations as different evidence types.  
6. Use Internal Alpha to validate observation quality, not to rush adaptive belief machines.  
7. Let Twin Update Strategies own interpretation; let Intelligence consume Twins only.  
8. Prefer honest unknowns over false certainty in every Alpha explanation surface.

Governing restatement:

> **Version 1.0 Evidence stays small, immutable, observational, explainable, and traceable. Future richness belongs to Twin reasoning — not to Evidence that starts concluding.**

---

# 11. Architecture Compliance Summary

| Invariant | Status under this analysis |
|---|---|
| Evidence weaker than conclusions | Required — educational honesty |
| Activity ≠ Evidence | Required |
| Observation ≠ Interpretation | Required |
| Evidence never claims mastery / readiness / pass probability | Required |
| Declared vs observed remain distinct types | Required |
| Single-session unknowns preserved | Required |
| Evidence never reasons; Strategies interpret | Required |
| Educational Intelligence consumes Twins, not activity | Preserved |
| Calibration ≠ Evidence | Preserved |
| Internal Alpha collects Evidence to validate observation, not rush algorithms | Required |
| No implementation / contracts / persistence / product flow in this milestone | Honoured — analysis only |

Consistency with:

| Companion | Alignment |
|---|---|
| Capability 3.6.2 Student Calibration Analysis | Self-report vs observed; priors ≠ truth; thin warrant |
| Capability 3.7.2 Twin Persistence Analysis | Immutable snapshots; Evidence separate from Twin state |
| Capability 2.10 Mission Intelligence Analysis | Mission completion as evidence signal, not mastery |
| Capability 4.8.1 Educational Evidence Architecture | Ownership, philosophy, and Twin/Intelligence firewall reinforced educationally |

---

# 12. STOP

This document defines **Educational Evidence educational analysis only**.

It does **not** authorise:

- Implementation  
- Flask routes or services  
- ORM models, schemas, or migrations  
- Evidence contracts or recorder APIs  
- Twin Update Strategy algorithms  
- Persistence of Evidence  
- Product flows, dashboards, or UI  
- Educational Intelligence redesign  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md) | Upstream Evidence architecture — purpose, ownership, boundaries |
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; Educational Evidence Principle |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Evidence → Twin → Intelligence |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law; immutable snapshots |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Epic 0 Evidence catalogue companion |
| [`CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md) | Declared vs observed; priors ≠ mastery |
| [`CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md`](CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md) | Twin snapshot educational state vs derived artefacts |
| [`CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md) | Mission completion as Behaviour/planning evidence, not mastery |
| [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md) | Shared educational vocabulary |
