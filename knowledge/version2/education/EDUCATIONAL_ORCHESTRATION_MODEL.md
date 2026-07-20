# Educational Orchestration Model

**Document ID:** V2-EOA-001  
**Classification:** Educational Architecture — Orchestration  
**Status:** Authoritative model of educational orchestration  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`TUTOR_MODEL.md`](TUTOR_MODEL.md)  
**Companions:** [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md) · [`EDUCATIONAL_DECISION_POINTS.md`](EDUCATIONAL_DECISION_POINTS.md) · [`EDUCATIONAL_STATE_TRANSITIONS.md`](EDUCATIONAL_STATE_TRANSITIONS.md) · [`SESSION_ASSEMBLY_MODEL.md`](SESSION_ASSEMBLY_MODEL.md) · [`ORCHESTRATION_INVARIANTS.md`](ORCHESTRATION_INVARIANTS.md)

---

## 1. Purpose

This document defines **Educational Orchestration** for Kwalitec Version 2: how the Educational Operating Model’s existing concepts collaborate to produce a tutoring experience.

Orchestration answers:

> *In what order do educational acts collaborate so that tutoring remains continuous, justified, and honest?*

It does **not** introduce new educational concepts. It describes interaction among concepts already defined in the Domain, Reasoning, Strategy, Episode, and Subject Knowledge foundations.

This is educational architecture. It is not implementation, API design, workflow software, scoring, or UI flow specification.

---

## 2. Definition

**Educational Orchestration:** the architecture by which the tutor coordinates Review of the Student Digital Twin, interpretation of evidence, diagnosis, hypothesis, priority, intention, strategy, Learning Episode selection and delivery, evidence collection, reflection, Twin update, and the next recommendation — as one continuous educational responsibility rather than as isolated product features.

Orchestration specialises the Tutor Model obligation (Diagnose → Teach → Observe → Interpret → Adapt) and the Educational Reasoning Loop into the **complete tutoring flow** a student experiences across episodes and sessions.

| Adjacent architecture | Grain | Relationship |
|-----------------------|-------|--------------|
| **Tutor Model** | Product obligation | Why tutoring must exist |
| **Educational Reasoning Loop** | Pre- and post-teaching reasoning | Cognitive spine inside orchestration |
| **Learning Episode Lifecycle** | Single episode execution | How one orchestrated turn is enacted |
| **Learning Episode Sequence** | Composition hierarchy | How episodes become sessions and journeys |
| **Educational Orchestration** (this document) | Full tutoring collaboration | How all stages collaborate end-to-end |

---

## 3. Complete Tutoring Flow

```text
Student arrives
       ↓
Review Digital Twin
       ↓
Interpret Evidence
       ↓
Educational Diagnosis
       ↓
Educational Hypothesis
       ↓
Educational Priority
       ↓
Teaching Intention
       ↓
Teaching Strategy
       ↓
Learning Episode Selection
       ↓
Episode Delivery
       ↓
Evidence Collection
       ↓
Reflection
       ↓
Twin Update
       ↓
Next Recommendation
       ↓
(return — continue tutoring)
```

The flow is continuous. Closing one recommendation reopens arrival into the next turn with a revised Twin and educational history. Sessions bound *sitting capacity*; they do not terminate the tutor obligation.

---

## 4. Stage Responsibilities

Each stage has one educational responsibility. Stages may be brief under thin evidence (cold start); they may not be silently absent when tutoring is claimed.

---

### 4.1 Student Arrives

**Responsibility**  
Recognise that a learner is present for tutoring — whether at session start, mid-journey return, revision re-entry, or after interruption — and establish the educational frame: who the student is, which curriculum aims are in view, and that tutoring (not mere content browsing) is the obligation.

**Inputs**  
Student identity; curriculum / journey context; session constraints (time, exam proximity); optional student-stated focus.

**Outputs**  
A lawful tutoring encounter ready for Twin review — not yet a teaching assignment.

**Must not**  
Treat arrival as licence to push the next chapter; equate login or navigation with educational need.

---

### 4.2 Review Digital Twin

**Responsibility**  
Consult the Student Digital Twin as standing educational belief about the learner: provisional estimates of knowledge, understanding-related posture, confidence calibration, retention, readiness, and uncertainty — always as *context for interpretation*, never as invented new evidence.

**Inputs**  
Current Twin estimates and uncertainty; educational history summaries the Twin lawfully holds; open educational problems previously warranted.

**Outputs**  
A Twin-informed starting picture: what the tutor already believes, what remains uncertain, and which aims appear open — still short of a fresh diagnosis commitment for this turn.

**Must not**  
Treat Twin estimates as fresh observations; overwrite Twin authority by episode completion; teach from Twin labels alone without interpreting evidence.

**Authority note**  
The Twin is consulted before teaching. Episodes supply evidence to the Twin; they do not own Twin belief. See Digital Twin doctrine and Learning Episode invariant spirit on Twin authority.

---

### 4.3 Interpret Evidence

**Responsibility**  
Separate signal from noise; distinguish observation from inference; weigh soft versus stronger evidence; name conflicts (for example confidence versus performance); admit thinness honestly.

**Inputs**  
Observations from prior and current activity; evidence history; reflection artefacts; Twin uncertainty as interpretive caution; curriculum context.

**Outputs**  
An interpreted evidence picture: patterns, strengths, contradictions, and honesty about thinness — still short of a full deficiency-category commitment when underdetermined.

**Must not**  
Jump from a single uninterpreted event to a teaching assignment; invent evidence from scores alone; treat engagement metrics as educational proof.

**Cold start**  
“Almost no evidence yet” is a lawful interpretative result. Curriculum sequencing may temporarily guide introduction need without fabricating mastery history.

---

### 4.4 Educational Diagnosis

**Responsibility**  
Name the current educational problem: deficiency category, learning objective, learning dimension(s) implicated, warrant, and uncertainty. Answer *what educational problem currently exists?*

**Inputs**  
Interpreted evidence; learning objectives; curriculum / prerequisite structure; Twin context; prior diagnoses (revisable).

**Outputs**  
Provisional Educational Diagnosis (or a set of competing provisional diagnoses). See [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md).

**Must not**  
Encode a teaching method inside the diagnosis; diagnose from confidence or completion alone; invent need from calendar position.

---

### 4.5 Educational Hypothesis

**Responsibility**  
Propose *why* the diagnosed problem likely exists; hold confidence modestly; allow competitors when underdetermined.

**Inputs**  
Diagnosis; supporting and contradicting evidence; prior hypotheses; reflection.

**Outputs**  
Working Educational Hypothesis (or explicit competitors) with confidence posture. See [`EDUCATIONAL_HYPOTHESIS_MODEL.md`](EDUCATIONAL_HYPOTHESIS_MODEL.md).

**Must not**  
Treat hypothesis as proven fact; teach long sequences as if an untested competitor were settled.

---

### 4.6 Educational Priority

**Responsibility**  
When multiple material diagnoses exist, select which problem — and therefore which intention path — governs the next Learning Episode. Priority orders needs; it does not invent them.

**Inputs**  
Competing diagnoses; Priority principles (prerequisites before extension, misconceptions before practice, dangerous false confidence, foundational understanding over speed, durable learning over progress theatre, exam readiness without erasing conceptual work, discriminating teaching when hypotheses compete); session and exam constraints as *ordering pressure*, not as fake need.

**Outputs**  
Primary educational problem for this turn; deferred problems retained in educational memory. See [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md).

**Must not**  
Let streaks, coverage dashboards, or engagement outrank educational truth; skip priority when multiple material needs compete.

**Single-need case**  
When only one material diagnosis is present, priority is trivial confirmation — still an explicit act, not an absent stage.

---

### 4.7 Teaching Intention

**Responsibility**  
Commit to the educational change sought in the next Learning Episode (or governing intention for a micro-sequence decomposed atomically). Answer *what educational improvement should the next episode achieve?*

**Inputs**  
Primary diagnosis; working hypothesis (or discriminating plan); priority outcome; Educational Atomicity constraint.

**Outputs**  
Primary Teaching Intention; atomic Teaching Goal candidate linked to a learning objective. See [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md).

**Must not**  
Bundle unrelated improvements; use mastery declarations or calendar blocks as intentions; adopt intention without diagnosis.

---

### 4.8 Teaching Strategy

**Responsibility**  
Choose *how* instruction will pursue the intention: the named instructional approach that fits the deficit class, hypothesis, student understanding posture, and objective.

**Inputs**  
Teaching Intention / Teaching Goal; diagnosis category; hypothesis; student constraints; legitimate pedagogical moves from the Strategy Architecture and Catalogue.

**Outputs**  
Named Teaching Strategy with educational rationale. See [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md).

**Must not**  
Default “more questions” for every diagnosis; choose strategy for novelty or engagement over educational fit; let strategy replace diagnosis.

---

### 4.9 Learning Episode Selection

**Responsibility**  
Select the Learning Episode type (and concept / objective focus) that lawfully realises the intention and strategy — preserving atomicity, prerequisites, and concept continuity.

**Inputs**  
Teaching Intention and Goal; Teaching Strategy; episode type catalogue; Knowledge Dependency and Concept Network constraints; session assembly constraints (time, prior episodes in the sitting).

**Outputs**  
Selected episode type and educational focus ready for delivery. See [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) · [`SESSION_ASSEMBLY_MODEL.md`](SESSION_ASSEMBLY_MODEL.md).

**Must not**  
Select by content inventory or UI template availability alone; fuse multiple purposes into one episode; demand transfer before introduction when dependency forbids it.

---

### 4.10 Episode Delivery

**Responsibility**  
Enact the selected Learning Episode: instruction and interaction under one purpose, realising intention and strategy as a bounded educational engagement.

**Inputs**  
Selected episode; Teaching Goal; Teaching Strategy; lawful materials and representations; prerequisite posture.

**Outputs**  
Lived instructional experience; student interaction; continuous production of observational material toward evidence.

**Must not**  
Present screens, timers, or content clicks as episodes without educational purpose; change the episode’s primary purpose mid-flight without a reasoned mid-episode educational decision (see Decision Points).

**Lifecycle detail**  
Inside delivery, the Learning Episode Lifecycle governs Instruction → Interaction → Evidence Collection stages. Orchestration owns *why this episode now*; the lifecycle owns *how one episode runs*.

---

### 4.11 Evidence Collection

**Responsibility**  
Capture observed educational happenings attributable to the episode’s purpose — the factual spine for later claims. Evidence is distinct from inferences and from Twin estimates.

**Inputs**  
Student performances, explanations, classifications, timings, discrimination results, and other lawful observations during and at close of the episode.

**Outputs**  
Evidence items ready for interpretation on the next turn and for Twin update on this turn.

**Must not**  
Invent evidence from scores alone; treat Twin estimates as if they were new observations; skip evidence because the episode “felt complete.”

---

### 4.12 Reflection

**Responsibility**  
Elicit the student’s structured consideration of difficulty, understanding, uncertainty, and felt readiness; produce soft metacognitive evidence that can change subsequent diagnosis, hypothesis, intention, and Twin interpretation.

**Inputs**  
Episode experience; prompts appropriate to episode type and intention.

**Outputs**  
Reflection artefact with consequence — or lawful deferred reflection with preserved consequence.

**Must not**  
Collect decorative reflection that cannot change the next move; fabricate student reflection; treat reflection as optional ornament when tutoring is claimed.

---

### 4.13 Twin Update

**Responsibility**  
Supply lawful inputs so the Student Digital Twin can revise standing educational belief — with uncertainty preserved — after evidence and reflection from this turn.

**Inputs**  
Evidence; reflection; episode evaluation outcomes; prior Twin state; diagnosis / hypothesis revisions as interpretive context.

**Outputs**  
Updated Twin estimates and uncertainty; explainable change in learner-state belief.

**Must not**  
Let episode completion overwrite Twin mastery authority; silently erase educational history; treat Twin update as optional decoration.

---

### 4.14 Next Recommendation

**Responsibility**  
State the next educational move in explainable educational language: what should happen next, why (diagnosis + intention at minimum), and what follows. The recommendation is the student’s visible face of Adaptation after Twin Update.

**Inputs**  
Updated Twin; revised or confirmed diagnosis/hypothesis/intention; session assembly state (continue sitting vs stop); journey and curriculum constraints.

**Outputs**  
An explainable recommendation: continue with next episode in session, change strategy or focus, open a repair interrupt, space for retention, or finish today’s sitting with a justified stop — always educationally warranted.

**Must not**  
Recommend from engagement optimisation alone; omit educational justification; present “next chapter” as if it were diagnosis-driven tutoring.

**Return**  
The recommendation closes one orchestration turn and opens the next: the student arrives again (immediately or later) into Review Digital Twin with revised belief.

---

## 5. Compressed Spines

### 5.1 Belief and need (pre-teaching)

```text
Arrive → Review Twin → Interpret Evidence → Diagnosis → Hypothesis → Priority → Intention → Strategy → Episode Selection
```

### 5.2 Enactment and belief revision (teaching and after)

```text
Episode Delivery → Evidence Collection → Reflection → Twin Update → Next Recommendation
```

### 5.3 Mapping to Tutor Model

| Tutor Model stage | Orchestration coverage |
|-------------------|------------------------|
| Diagnose | Review Twin → Interpret Evidence → Diagnosis → Hypothesis → Priority |
| Teach | Intention → Strategy → Episode Selection → Episode Delivery |
| Observe | Evidence Collection (+ interaction within delivery) |
| Interpret | Reflection interpretation + evidence interpretation toward Twin and next diagnosis |
| Adapt | Twin Update → Next Recommendation → return |

### 5.4 Mapping to Educational Reasoning Loop

Orchestration **includes** the Reasoning Loop and adds the explicit tutoring frame around it: Student Arrives, Review Digital Twin (as a named stage before interpretation), Educational Priority (as a first-class stage), Learning Episode Selection distinct from Strategy, Episode Delivery distinct from the abstract “Learning Episode” reasoning commitment, and Next Recommendation as the explainable Adaptation surface.

The Reasoning Loop remains the tutor’s standing cognitive architecture. Orchestration is how that architecture collaborates as a complete tutoring experience.

---

## 6. Continuity Across Grain

| Grain | What persists | What may change each turn |
|-------|---------------|---------------------------|
| **Within episode** | Intention, strategy, type, objective | Interaction responses; mid-episode educational decisions when evidence demands |
| **Within session** | Session assembly commitments; micro-sequence arc when active | Episode succession; repair interrupts; stop decisions |
| **Across sessions** | Twin belief; unresolved misconceptions; priority memory; journey aims | Which diagnosis governs; strategy continuity or revision |
| **Across journey** | Curriculum aims; educational history | Dimensional attention; spacing and transfer timing |

Educational memory of need, hypothesis, and intention persists beyond a single sitting. Orchestration never “finishes” the learner by closing one episode or one session.

---

## 7. Integrity Rules for Orchestration

1. **No stage may silently skip when tutoring is claimed.** Brief is allowed; absent is not.  
2. **The Digital Twin is consulted before teaching.**  
3. **Diagnosis precedes Intention; Intention precedes Strategy; Strategy precedes Episode Selection; Selection precedes Delivery.**  
4. **Priority orders competing diagnoses before Intention locks.**  
5. **Evidence outweighs assumptions** at every interpretative step.  
6. **Hypothesis remains revisable** after Evidence and Reflection.  
7. **Reflection must be able to change** Diagnosis, Hypothesis, Intention, or Strategy on a subsequent turn.  
8. **Recommendations require educational justification** (diagnosis + intention at minimum).  
9. **Cold start** enters with thin evidence and may use curriculum sequencing as lawful temporary guide — not as fake mastery history.  
10. **Session completion is administrative sitting closure**, never mastery by synonym.

---

## 8. Actuarial Walkthrough (Illustrative)

1. **Student arrives** — candidate returns for a CM1 reserves sitting.  
2. **Review Digital Twin** — Twin shows provisional application strength on net premium; elevated uncertainty on with-profits; prior false-confidence flag near exam window.  
3. **Interpret Evidence** — last session: clone success; first surplus-distribution stem failed; reflection claimed “ready.”  
4. **Educational Diagnosis** — Misconception (or Incomplete Understanding) on bonus structures relative to valuation objective; competing False Confidence.  
5. **Educational Hypothesis** — student treats with-profits as ordinary net premium with a cosmetic label.  
6. **Educational Priority** — Misconception before further practice; False Confidence remains secondary but material.  
7. **Teaching Intention** — Repair misconception.  
8. **Teaching Strategy** — Conceptual contrast (with vs without surplus) + forced explanation.  
9. **Learning Episode Selection** — Misconception Repair episode on the valuation objective.  
10. **Episode Delivery** — contrastive instruction and discrimination interaction.  
11. **Evidence Collection** — discrimination probes; corrected explanation on two of three contrasts.  
12. **Reflection** — “I mixed bonus with interest-rate adjustments.”  
13. **Twin Update** — reduce confidence in prior ‘valuation OK’ estimate; record misconception-repair evidence; raise uncertainty appropriately.  
14. **Next Recommendation** — guided practice re-check on surplus steps in this sitting if time remains; otherwise stop with a justified continue-tomorrow for application/fluency — never “chapter complete = mastered.”

---

## 9. Summary Propositions

1. Educational Orchestration is how existing Educational Operating Model concepts collaborate to produce tutoring.  
2. The complete flow runs from Student Arrives through Next Recommendation and returns.  
3. Twin review precedes teaching; diagnosis and priority precede intention; strategy precedes episode selection; evidence and reflection precede Twin update.  
4. Orchestration specialises — and does not replace — the Tutor Model, Reasoning Loop, and Episode Lifecycle.  
5. No new educational concepts are introduced; interaction among existing concepts is the subject.
