# Educational Decision Points

**Document ID:** V2-EOA-002  
**Classification:** Educational Architecture — Orchestration  
**Status:** Authoritative catalogue of educational decisions  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_ORCHESTRATION_MODEL.md`](EDUCATIONAL_ORCHESTRATION_MODEL.md)  
**Companions:** [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md) · [`STRATEGY_SELECTION_MODEL.md`](STRATEGY_SELECTION_MODEL.md) · [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md) · [`ORCHESTRATION_INVARIANTS.md`](ORCHESTRATION_INVARIANTS.md)

---

## 1. Purpose

This document identifies every **major educational decision** the tutor must make while orchestrating tutoring.

A decision point is a reasoned fork in educational responsibility — not a UI button, not a workflow node, and not an algorithm branch. Each decision has purpose, inputs, possible outcomes, and educational rationale grounded in existing Educational Operating Model concepts.

---

## 2. How to Read a Decision Point

Each decision defines:

| Element | Meaning |
|---------|---------|
| **Purpose** | Why the decision exists educationally |
| **Inputs** | Lawful educational inputs (not software payloads) |
| **Possible outcomes** | Educationally distinct results |
| **Educational rationale** | Why these outcomes protect learning |

Decisions are ordered roughly along the orchestration flow. Several may recur mid-session when evidence interrupts a planned arc.

---

## 3. Pre-Teaching Decisions

---

### D1 — Should we teach now?

**Purpose**  
Decide whether the present encounter should become targeted teaching, or whether observation, calibration, recovery, or honest deferral is the lawful first move.

**Inputs**  
Twin review; interpreted evidence thickness; student capacity and affective state; session constraints; whether a diagnosable need (including cold-start introduction) is present.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Teach** | Proceed through diagnosis → intention → strategy → episode |
| **Observe / diagnose first** | Elicit discriminating evidence before committing to instruction |
| **Recover** | Address capacity/affect (low confidence overload, exhaustion) before content push |
| **Defer** | Stop or reschedule the sitting without inventing a teaching claim |

**Educational rationale**  
Teaching without need or capacity is broadcasting or harm. Cold start may still lawfully teach introduction under curriculum sequencing, but that is still a *named* introduction need — not silence pretending to be tutoring.

---

### D2 — What educational problem governs?

**Purpose**  
Commit to the Educational Diagnosis (or competing set) that will frame this turn.

**Inputs**  
Interpreted evidence; Twin context; learning objectives; deficiency catalogue; prior diagnoses.

**Possible outcomes**  
Any lawful deficiency category (or competing provisional set): Conceptual Misunderstanding, Procedural Weakness, Weak Retention, Knowledge Fragmentation, Prerequisite Gap, Misconception, Low Confidence, False Confidence, Exam Technique Weakness, Application Weakness, Transfer Weakness, Incomplete Understanding — plus lawful cold-start introduction need.

**Educational rationale**  
Without a named problem, intention and strategy become opportunistic. Diagnosis decides *what is wrong*; it does not decide *how*.

---

### D3 — Which problem comes first? (Priority)

**Purpose**  
Order competing diagnoses so one primary problem governs the next episode.

**Inputs**  
Competing diagnoses; Priority principles; exam proximity; session time; educational memory of deferred needs.

**Possible outcomes**

| Outcome | Typical trigger |
|---------|-----------------|
| **Prioritise prerequisite gap** | Upstream absence blocks honest progress |
| **Prioritise misconception** | Stable wrong model before practice volume |
| **Prioritise dangerous false confidence** | Overclaim near examinations |
| **Prioritise incomplete / conceptual misunderstanding** | Thin grasp before fluency theatre |
| **Prioritise weak retention** | Fade after delay; exam window with prior acquisition |
| **Prioritise transfer / application** | Local grasp adequate; exam credibility needs variation or use |
| **Prioritise exam technique** | Capacity present; deployment under constraint fails |
| **Prioritise recovery / confidence calibration** | Affect blocks learning or misallocates effort |
| **Hold discriminating fork** | Competitors underdetermine; prefer a test before long commitment |

**Educational rationale**  
See [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md). Priority protects prerequisites, misconception hygiene, honesty about confidence, and durable learning over progress theatre.

---

### D4 — Why does this problem likely exist? (Hypothesis posture)

**Purpose**  
Decide whether a working Educational Hypothesis is clear enough to teach under, or whether discrimination among competitors is required first.

**Inputs**  
Diagnosis; evidence patterns; prior hypotheses; reflection.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Commit to working hypothesis** | Teach as if this explanation is roughly right |
| **Hold competitors** | Design the next intention to discriminate |
| **Revise / replace hypothesis** | Prior explanation no longer warranted |
| **Admit thin explanation** | Proceed with modest hypothesis and high uncertainty |

**Educational rationale**  
Dogmatic hypotheses produce wrong long teaching commitments. Discrimination is teaching with epistemic honesty, not delay theatre.

---

### D5 — What change should we seek? (Intention)

**Purpose**  
Select the Teaching Intention for the next episode.

**Inputs**  
Primary diagnosis; hypothesis posture; atomicity; priority outcome.

**Possible outcomes** (illustrative classes already in the Intention Model)

- Repair misconception  
- Build intuition / introduce concept  
- Strengthen prerequisite  
- Consolidate / deepen understanding  
- Improve application or procedural fluency  
- Improve transfer  
- Recover confidence / calibrate confidence  
- Strengthen retention (retrieval)  
- Prepare for examination (technique under constraint)  

**Educational rationale**  
Intention answers *what improvement*; without it, episodes are activity. One primary intention per episode preserves Educational Atomicity.

---

## 4. Method and Episode Decisions

---

### D6 — Should we retrieve?

**Purpose**  
Decide whether the governing move is retrieval (Retention dimension) rather than first teaching, deepening, or new practice volume.

**Inputs**  
Diagnosis of Weak Retention or retention risk; Twin retention estimates; interval since last success; exam proximity; whether acquisition once appeared present.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Retrieve** | Select Retrieval / Revision-class episode |
| **Re-teach** | Evidence suggests never-acquired or collapsed to absence — introduction/deepening, not pure retrieval |
| **Retrieve then deepen** | Retrieval reveals conceptual fade → Concept Deepening follows |
| **Defer retrieval** | Higher-priority misconception or prerequisite blocks honest retrieval on this objective |

**Educational rationale**  
Retention repair differs from first teaching. Massed re-reading is not retrieval. Spacing across sessions is required for durable retention claims.

---

### D7 — Should we repair?

**Purpose**  
Decide whether misconception (or critical incomplete understanding requiring contrastive repair) must interrupt the current arc.

**Inputs**  
Patterned errors; confident wrong explanations; discrimination failures; Priority P2 (repair misconceptions before practice).

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Repair now** | Misconception Repair (or equivalent deepening with contrast) becomes primary |
| **Continue practice with caution** | Errors look like slips/noise, not stable wrong model |
| **Repair then re-enter practice** | Classic interrupt micro-sequence |
| **Relocate to prerequisite** | “Misconception” dissolves into upstream gap |

**Educational rationale**  
Practice on a wrong model strengthens the wrong model. Repair must be explicit; burying error in more drills is unlawful.

---

### D8 — Should we revisit prerequisites?

**Purpose**  
Decide whether struggle on the current objective is truly about that objective, or about an upstream dependency.

**Inputs**  
Failure patterns; scaffolded success when prerequisite is supplied; Knowledge Dependency / Concept Network structure; Priority P1.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Prerequisite Repair** | Move teaching focus upstream |
| **Stay on current objective** | Prerequisite posture adequate |
| **Minimal concurrent scaffold** | Brief prerequisite support without abandoning the aim — still atomic per episode |
| **Journey resequencing signal** | Persistent upstream absence warrants journey-level adjustment |

**Educational rationale**  
Advanced struggle that is really upstream absence produces theatre and false diagnosis of the advanced topic.

---

### D9 — Should we increase challenge?

**Purpose**  
Decide whether to advance demand: fade scaffolds, move to independence, introduce variation/transfer, or add exam constraint.

**Inputs**  
Episode evaluation; understanding level posture; application success; false vs calibrated confidence; strategy fade principles.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Fade scaffolds** | Worked Example → Guided → Independent |
| **Introduce near transfer** | Surface variation within syllabus |
| **Introduce far transfer / synthesis** | When objective and local competence warrant |
| **Add exam constraint** | Timing, paper discipline — only if technique is the deficit class or readiness path |
| **Hold challenge** | Evidence does not yet support increase |
| **Reduce challenge** | Collapse indicates premature demand |

**Educational rationale**  
Challenge without foundation is demoralisation; endless scaffold is dependence. Transfer and exam constraint are lawful only when dependency and diagnosis allow.

---

### D10 — Which Teaching Strategy?

**Purpose**  
Select the instructional approach that pursues the intention.

**Inputs**  
Intention; diagnosis class; hypothesis; student constraints; Strategy Catalogue and Selection Model; Instructional Principles.

**Possible outcomes**  
Named strategies from the Teaching Strategy Catalogue (for example conceptual contrast, worked-example fading, interleaved practice, retrieval practice, explanatory teaching) — always as *how*, never as a substitute diagnosis.

**Educational rationale**  
Method must fit deficit class. Default undifferentiated questioning for every need is broadcasting.

---

### D11 — Should we change strategy?

**Purpose**  
Decide whether to continue, fade, or revise the Teaching Strategy mid-arc or after evaluation.

**Inputs**  
Evidence against expected evidence profile; reflection; hypothesis revision; Strategy Composition rules.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Continue strategy** | Evidence aligns with expected progress |
| **Fade within strategy family** | Reduce support deliberately |
| **Revise strategy** | Same intention; different method |
| **Change intention** | Evidence shows the problem was mis-named — return to diagnosis |
| **Abort arc for repair interrupt** | Misconception/prerequisite discovered mid-sequence |

**Educational rationale**  
Adaptation without interpretation is thrash. Persisting with a failing strategy because it was planned is also thrash.

---

### D12 — Which Learning Episode type?

**Purpose**  
Select the episode type that realises intention and strategy under atomicity.

**Inputs**  
Intention; strategy; type catalogue; prerequisites; session assembly constraints.

**Possible outcomes**  
Any lawful type from [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) (Concept Introduction, Concept Deepening, Misconception Repair, Prerequisite Repair, Worked Example, Guided Practice, Independent Practice, Retrieval Practice, Transfer Practice, Exam Application, Recovery, Reflection, Revision, Capstone inputs, etc.).

**Educational rationale**  
Type encodes educational intent. Materials and screens do not invent types.

---

## 5. Session and Continuity Decisions

---

### D13 — Should this episode continue the micro-sequence?

**Purpose**  
Decide succession inside a planned micro-sequence versus educational interrupt or early stop.

**Inputs**  
Micro-sequence arc purpose; episode evaluation; dependency/fade rules; remaining session capacity.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Advance to next planned episode** | Evaluation supports succession |
| **Repeat / remediate current grain** | Insufficient evidence of readiness for next step |
| **Interrupt for repair** | Misconception or prerequisite intervenes |
| **End sequence early** | Capacity, collapse, or intention change |

**Educational rationale**  
Sequences compose atoms; they are not scripts immune to evidence.

---

### D14 — Should we finish today’s session?

**Purpose**  
Decide whether the sitting should close now.

**Inputs**  
Session capacity and fatigue; episode completion; whether an atomic purpose can still be finished honestly; Priority of remaining needs; danger of starting an episode that cannot be evidenced.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Continue** | Another coherent episode fits capacity |
| **Finish after reflection** | Close sitting with consequence-bearing reflection |
| **Hard stop** | Capacity exhausted; preserve educational honesty over volume |
| **Stop mid-arc with memory** | Defer remaining micro-sequence with educational continuity preserved |

**Educational rationale**  
Scarce professional time must not become exhausted theatre. Session completion is sitting closure, not mastery. Prefer not to start an episode that cannot collect evidence and reflection.

---

### D15 — What is the next recommendation?

**Purpose**  
State the Adaptation outcome in explainable form after Twin Update.

**Inputs**  
Updated Twin; current diagnosis/intention posture; session assembly state; journey aims.

**Possible outcomes**

| Outcome | Meaning |
|---------|---------|
| **Next episode now** | Continue sitting under current or revised intention |
| **Next episode later** | Spaced return (especially retention) |
| **Change focus** | Different objective/problem per priority |
| **Strategy change** | Same aim; different how |
| **Journey-level signal** | Resequencing or dimensional rebalancing across sessions |
| **Honest pause** | No productive teaching move under current capacity |

**Educational rationale**  
Every material recommendation answers what, why, and what follows. Recommendations without diagnosis + intention justification are unlawful as tutoring claims.

---

## 6. Decision Map Along the Flow

```text
Arrive / Twin review
    → D1 Should we teach?
Interpret / Diagnose
    → D2 What problem governs?
    → D3 Which problem first?
Hypothesis
    → D4 Hypothesis posture?
Intention
    → D5 What change?
    → D6 Retrieve?
    → D7 Repair?
    → D8 Prerequisites?
Strategy / Episode
    → D9 Increase challenge?
    → D10 Which strategy?
    → D11 Change strategy?
    → D12 Which episode type?
Delivery / Sequence / Session
    → D13 Continue micro-sequence?
    → D14 Finish today’s session?
After Twin update
    → D15 Next recommendation?
```

---

## 7. Discipline Rules for Decisions

1. **Decisions are educational, not cosmetic** — engagement optimisation is not a lawful primary input.  
2. **Every teaching decision traces to diagnosis and intention.**  
3. **Interrupt decisions (repair, prerequisite) outrank planned volume** when Priority principles say so.  
4. **“Do nothing educational” can be lawful** (recover, defer, observe) — pretending activity is teaching is not.  
5. **Mid-session revision is normal** when evidence warrants; thrash without interpretation is not.  
6. **Explainability** — a competent educator should be able to state why each major fork was taken.

---

## 8. Summary Propositions

1. Major educational decisions are forks in tutor responsibility, not workflow software.  
2. Pre-teaching decisions establish need, priority, hypothesis posture, and intention.  
3. Method decisions select and revise strategy and episode type under diagnosis.  
4. Session decisions protect atomicity, capacity, and honest stopping.  
5. The next recommendation is Adaptation made explainable.
