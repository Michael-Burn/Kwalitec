# Educational Reasoning Loop

**Document ID:** V2-ERM-004  
**Classification:** Educational Architecture — Reasoning Foundation  
**Status:** Authoritative tutor reasoning loop  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`TUTOR_MODEL.md`](TUTOR_MODEL.md)  
**Companions:** [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) · [`EDUCATIONAL_HYPOTHESIS_MODEL.md`](EDUCATIONAL_HYPOTHESIS_MODEL.md) · [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md) · [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md) · [`LEARNING_EPISODE_LIFECYCLE.md`](LEARNING_EPISODE_LIFECYCLE.md) · [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md)

---

## 1. Purpose

This document defines the **complete Educational Reasoning Loop**: how an expert tutor thinks before, during, and after selecting a Learning Episode.

It specialises the Tutor Model’s Diagnose → Teach → Observe → Interpret → Adapt cycle into the permanent Version 2 reasoning architecture.

The loop is educational law for design and governance. It is not a software state machine.

---

## 2. Loop Overview

```text
Observe
   ↓
Interpret Evidence
   ↓
Educational Diagnosis
   ↓
Educational Hypothesis
   ↓
Teaching Intention
   ↓
Teaching Strategy
   ↓
Learning Episode
   ↓
Evidence
   ↓
Reflection
   ↓
Twin Update
   ↓
Repeat
```

The loop is continuous across episodes and sessions. Educational memory of need, hypothesis, and intention persists beyond a single sitting.

---

## 3. Relationship to Adjacent Loops

| Loop | Grain | Role |
|------|-------|------|
| **Tutor Model loop** | Product obligation | Diagnose → Teach → Observe → Interpret → Adapt |
| **Educational Reasoning Loop** (this document) | Pre-teaching and post-teaching reasoning | Full chain from observation through twin update |
| **Learning Episode Lifecycle** | Single episode execution | Diagnosis → Teaching Goal → Strategy → … → Next Decision |

The Reasoning Loop is the tutor’s standing cognitive architecture. The Episode Lifecycle is how one turn of that architecture is realised as a bounded educational unit. Teaching Goal is the atomic episode expression of Teaching Intention.

---

## 4. Stage Transitions

Each subsection defines: purpose · inputs · outputs · transition rule · forbidden substitute.

---

### 4.1 Observe

**Purpose**  
Notice educationally relevant happenings: what the student attempted, produced, skipped, timed, explained, or disclosed.

**Inputs**  
Ongoing student activity; prior episode residues; curriculum context; lawful Twin context (as background, not as observation).

**Outputs**  
Raw observational material — not yet a diagnosis.

**Transition to Interpret Evidence**  
When observations are available to read — including the limiting case of “almost no evidence yet” (cold start), which must itself be observed as thin history.

**Forbidden substitute**  
Treating content delivery or schedule position as if observation of learning had occurred.

---

### 4.2 Interpret Evidence

**Purpose**  
Separate signal from noise; distinguish observation from inference; weigh soft vs stronger evidence; name conflicts (for example confidence vs performance).

**Inputs**  
Observations from Observe; prior evidence history; reflection artefacts when present; Twin uncertainty as interpretive caution.

**Outputs**  
An interpreted evidence picture: patterns, strengths, contradictions, and honesty about thinness — still short of a full deficiency category commitment when underdetermined.

**Transition to Educational Diagnosis**  
When the tutor can lawfully ask: *what educational problem does this picture suggest?*

**Forbidden substitute**  
Jumping from a single uninterpreted event to a teaching assignment (Invariant spirit of I15 / reasoning invariants).

**Notes**  
Interpretation may conclude “insufficient to diagnose beyond cold-start sequencing.” That is a lawful interpretative result, not a failure.

---

### 4.3 Educational Diagnosis

**Purpose**  
Name the current educational problem (deficiency category, objective, dimension, warrant, uncertainty).

**Inputs**  
Interpreted evidence; learning objectives; curriculum/prerequisite structure; priority context when multiple problems compete.

**Outputs**  
Provisional Educational Diagnosis (see [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md)).

**Transition to Educational Hypothesis**  
When a problem is named — including “introduction needed” as a lawful cold-start diagnosis under curriculum sequencing.

**Forbidden substitute**  
Encoding a teaching method inside the diagnosis; diagnosing from confidence or completion alone.

**Priority branch**  
When multiple material diagnoses exist, apply [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md) before locking the primary problem for this loop turn.

---

### 4.4 Educational Hypothesis

**Purpose**  
Propose why the diagnosed problem exists; hold confidence; allow competitors.

**Inputs**  
Diagnosis; supporting and contradicting evidence; prior hypotheses; reflection.

**Outputs**  
Working Educational Hypothesis (or an explicit set of competitors) with confidence posture.

**Transition to Teaching Intention**  
When the tutor can state what change would follow from the working hypothesis — or what discriminating change would test competitors.

**Forbidden substitute**  
Treating hypothesis as proven fact; teaching without any explanatory commitment when evidence already underdetermines the move.

---

### 4.5 Teaching Intention

**Purpose**  
Commit to the educational change sought in the next Learning Episode.

**Inputs**  
Diagnosis; working hypothesis (or discriminating plan); atomicity constraint; priority outcome.

**Outputs**  
Primary Teaching Intention; atomic Teaching Goal candidate linked to a learning objective.

**Transition to Teaching Strategy**  
When the intended change is named and evaluable in principle.

**Forbidden substitute**  
Bundled intentions (“fix everything”); mastery-as-intention; calendar-as-intention.

---

### 4.6 Teaching Strategy

**Purpose**  
Choose *how* instruction will pursue the intention: the instructional approach that fits the deficit class and hypothesis.

**Inputs**  
Teaching Intention / Teaching Goal; diagnosis category; hypothesis; student constraints; available legitimate pedagogical moves.

**Outputs**  
Named Teaching Strategy with educational rationale.

**Transition to Learning Episode**  
When strategy can be realised by a lawful episode type and materials.

**Forbidden substitute**  
Default “more questions” for every diagnosis; strategy chosen for novelty or engagement over educational fit.

---

### 4.7 Learning Episode

**Purpose**  
Realise intention and strategy as one atomic educational engagement: instruction, interaction, evidence collection, and reflection under one purpose.

**Inputs**  
Teaching Goal; Teaching Strategy; selected episode type; prerequisites check.

**Outputs**  
Lived instructional experience; student interaction; episode-scoped evidence; reflection artefact (or lawful deferred reflection with consequence preserved).

**Transition to Evidence**  
As interaction unfolds and when the episode closes — evidence is produced continuously and consolidated at close.

**Forbidden substitute**  
UI screens, timers, or content clicks presented as episodes without educational purpose; multi-purpose bundles.

**Lifecycle detail**  
See [`LEARNING_EPISODE_LIFECYCLE.md`](LEARNING_EPISODE_LIFECYCLE.md) for Instruction → Interaction → Evidence Collection stages inside the episode.

---

### 4.8 Evidence

**Purpose**  
Capture observed educational happenings attributable to the episode’s purpose — the factual spine for later claims.

**Inputs**  
Student performances, explanations, classifications, timings, discrimination results, and other lawful observations during/after instruction.

**Outputs**  
Evidence items distinct from inferences and from Twin estimates.

**Transition to Reflection**  
When the instructional and interactive core has produced (or clearly failed to produce) material evidence; reflection then adds soft metacognitive evidence.

**Forbidden substitute**  
Inventing evidence from scores alone; treating Twin estimates as if they were new observations.

---

### 4.9 Reflection

**Purpose**  
Elicit the student’s structured consideration of difficulty, understanding, uncertainty, and felt readiness; produce soft evidence with consequence.

**Inputs**  
Episode experience; prompts appropriate to episode type and intention.

**Outputs**  
Reflection artefact capable of influencing subsequent diagnosis, hypothesis, intention, and Twin interpretation.

**Transition to Twin Update**  
When reflection is captured (or lawfully deferred with preserved consequence).

**Forbidden substitute**  
Decorative reflection that cannot change the next move; fabricated student reflection.

---

### 4.10 Twin Update

**Purpose**  
Supply lawful inputs so the Student Digital Twin can revise standing educational belief — knowledge, confidence calibration, retention, readiness, and related estimates — with uncertainty preserved.

**Inputs**  
Evidence; reflection; episode evaluation outcomes; prior Twin state; diagnosis/hypothesis revisions as interpretive context.

**Outputs**  
Updated Twin estimates and uncertainty; explainable change in learner-state belief.

**Transition to Repeat (Observe)**  
The next loop turn begins from the new observational and belief context — including observing what the Twin now warrants as open educational problems.

**Forbidden substitute**  
Episode completion overwriting Twin mastery authority; silent erasure of educational history; treating Twin update as optional decoration.

**Authority note**  
Episodes and reasoning supply evidence and interpretive inputs. The Twin remains the standing authority for learner-state estimates. See Digital Twin doctrine and Learning Episode Invariant E14 spirit.

---

### 4.11 Repeat

**Purpose**  
Continue tutoring: the educational agent never “finishes” the learner by closing one episode.

**What repeats**  
Observe → … → Twin Update, with revised diagnosis, hypothesis, and intention as warranted.

**What persists**  
Curriculum aims; educational history; unresolved misconceptions; priority commitments; exam constraints.

**What must not thrash**  
Adaptation without interpretation; novelty-driven topic switching; endless identical drill after the hypothesis has changed.

---

## 5. Compressed Views

### 5.1 Reasoning spine (pre-teaching)

```text
Observe → Interpret Evidence → Diagnosis → Hypothesis → Intention → Strategy
```

### 5.2 Enactment spine (teaching)

```text
Learning Episode → Evidence → Reflection → Twin Update
```

### 5.3 Tutor Model mapping

| Tutor Model stage | Reasoning Loop coverage |
|-------------------|-------------------------|
| Diagnose | Observe → Interpret Evidence → Diagnosis → Hypothesis |
| Teach | Intention → Strategy → Learning Episode (instruction/interaction) |
| Observe | Evidence (+ interaction within episode) |
| Interpret | Reflection interpretation + evidence interpretation toward Twin and next diagnosis |
| Adapt | Twin Update → Repeat (new intention/strategy) |

---

## 6. Integrity Rules for the Loop

1. **No stage may silently skip when tutoring is claimed.** Brief is allowed; absent is not.  
2. **Diagnosis precedes Intention; Intention precedes Strategy; Strategy precedes Episode.**  
3. **Evidence outweighs assumptions** at every interpretative step.  
4. **Hypothesis remains revisable** after Evidence and Reflection.  
5. **Reflection must be able to change** Diagnosis, Hypothesis, Intention, or Strategy on the next turn.  
6. **Recommendations that emerge from Repeat** require educational justification (diagnosis + intention at minimum).  
7. **Cold start** enters at Observe/Interpret with thin evidence and may use curriculum sequencing as lawful temporary guide — not as fake mastery history.

---

## 7. Actuarial Walkthrough (Illustrative)

1. **Observe** — student misses three with-profits valuation items; timings normal.  
2. **Interpret Evidence** — errors cluster when surplus distribution appears; pure net-premium items succeed.  
3. **Diagnosis** — misconception (or incomplete understanding) on bonus structures relative to valuation objective.  
4. **Hypothesis** — “Student treats with-profits as ordinary net premium with a cosmetic label.”  
5. **Intention** — Repair misconception.  
6. **Strategy** — Conceptual contrast (with vs without surplus) + forced explanation.  
7. **Learning Episode** — Misconception Repair episode on the objective.  
8. **Evidence** — discrimination probes; corrected explanation on two of three contrasts.  
9. **Reflection** — “I mixed bonus with interest rate adjustments.”  
10. **Twin Update** — reduce confidence in prior ‘valuation OK’ estimate; record misconception-repair evidence; raise uncertainty appropriately.  
11. **Repeat** — new diagnosis may shift toward application/fluency on surplus steps; new hypothesis and intention follow.

---

## 8. Summary Propositions

1. The Educational Reasoning Loop is the permanent Version 2 architecture for how Kwalitec thinks before it teaches.  
2. Every transition has lawful inputs, outputs, and forbidden substitutes.  
3. Diagnosis names problems; hypotheses explain; intentions commit to change; strategies choose method; episodes enact.  
4. Evidence, reflection, and Twin update close the loop and reopen observation.  
5. The loop specialises — and does not replace — the Tutor Model obligation.
