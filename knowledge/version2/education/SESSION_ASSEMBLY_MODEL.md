# Session Assembly Model

**Document ID:** V2-EOA-004  
**Classification:** Educational Architecture — Orchestration  
**Status:** Authoritative model of session assembly  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_ORCHESTRATION_MODEL.md`](EDUCATIONAL_ORCHESTRATION_MODEL.md)  
**Companions:** [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md) · [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md) · [`STRATEGY_COMPOSITION_MODEL.md`](STRATEGY_COMPOSITION_MODEL.md) · [`LEARNING_EPISODE_LIFECYCLE.md`](LEARNING_EPISODE_LIFECYCLE.md) · [`EDUCATIONAL_DECISION_POINTS.md`](EDUCATIONAL_DECISION_POINTS.md)

---

## 1. Purpose

This document defines how **Learning Episodes become Learning Sessions**.

A session is one bounded sitting: a container for coherent educational work a student can sustainably complete. Session assembly answers:

> *How should episodes be ordered, bounded, and closed so that atomicity, strategy continuity, concept continuity, reflection, and honest stopping are preserved?*

This is educational architecture. It is not a calendar product, UI wizard, timer specification, or API for session resources.

---

## 2. Definition

**Session Assembly:** the educational composition of one or more Learning Episodes (and optional micro-sequences) into a single Learning Session, governed by diagnosis-driven orchestration, Educational Atomicity, and sustainable sitting capacity.

```text
Learning Episode
       ↓
  Micro Sequence   (optional arc)
       ↓
 Learning Session  ← this document
       ↓
 Learning Journey
```

The session does **not** become the atomic teaching unit. Episodes remain the atoms. The session packages what one sitting can honestly hold.

---

## 3. Assembly Principles

### 3.1 Coherence over volume

A session should read as one educational story — or a small number of tightly related stories — not as a shuffled playlist of unrelated objectives.

### 3.2 Capacity honesty

Professional candidates have limited daily capacity. Assembly maximises educational ROI per sitting; it refuses exhausted theatre.

### 3.3 Evidence interruptibility

Planned assembly yields to repair and prerequisite interrupts when Priority principles require.

### 3.4 Explainability

The student (and a reviewing educator) should understand why these episodes share a sitting.

---

## 4. Episode Ordering

### 4.1 Lawful ordering sources

Episode order inside a session derives from:

1. **Educational Priority** — which problem governs now;  
2. **Knowledge Dependencies** — prerequisites before dependent demand;  
3. **Micro-sequence arcs** — introduce → example → guided → independent; repair interrupts; retrieval → deepen-or-transfer;  
4. **Strategy Composition** — fade scaffolds deliberately; do not reverse-fade without reason;  
5. **Dimensional honesty** — retention and transfer often need spacing *across* sessions; do not fake them by stuffing.

### 4.2 Typical session shapes

| Shape | Composition | When lawful |
|-------|-------------|-------------|
| **Single episode** | One standalone episode | Recovery, short Retrieval, focused Repair, Reflection-heavy close |
| **One micro-sequence** | Ordered arc of atomic episodes | Most first-pass and repair arcs |
| **Two short episodes** | Related aims or repair + re-check | When atomicity and time allow |
| **Capstone-primary** | Capstone attempt as main work | Journey-ready only |

### 4.3 Ordering rules

1. **Dependency before demand** — do not demand transfer before introduction.  
2. **Repair before volume** — misconception/prerequisite interrupts outrank more clones.  
3. **Fade scaffolds deliberately** — Worked Example → Guided → Independent.  
4. **Discriminate before long commitment** when hypotheses compete.  
5. **Do not thrash topics** inside one sitting without educational justification.  
6. **Evaluate to adapt** — succession follows episode evaluation, not a fixed script immune to evidence.

### 4.4 Unlawful ordering

- Chapter playlist immune to diagnosis  
- Independent practice forever  
- Explanations forever without application  
- Advanced synthesis as session opener for a cold objective  
- Interleaving unrelated deficiency classes for novelty

---

## 5. Atomicity Preservation

Educational Atomicity requires **one primary purpose per episode**. Session assembly composes atoms; it must not fuse them.

**Preserved when:**

- each episode retains its Teaching Goal and type identity;  
- micro-sequence arc purpose is composition, not a mega-episode;  
- evidence identity remains attributable per episode;  
- mid-session interrupts become new episodes (or explicitly replace the planned next episode), not silent purpose mutation.

**Violated when:**

- the session is treated as one undifferentiated teaching blob;  
- multiple co-equal aims share a single episode;  
- “finish the chapter today” collapses many purposes into one sitting without episode boundaries;  
- UI screens redefine educational purpose.

Compression of reflection or summary at session end is lawful only if each episode retains evidence identity (see Episode Lifecycle compression rules).

---

## 6. Strategy Continuity

### 6.1 Continuity within a sitting

When a Teaching Strategy governs a micro-sequence, successive episodes should normally continue, fade, or compose that strategy deliberately — not abandon it for unrelated method fashion.

**Lawful continuity**

- Same strategy family with planned fade (example → guided → independent)  
- Strategy revision after evaluation with explicit rationale (Decision D11)  
- Interrupt that *suspends* the strategy for repair, then re-enters with scaffolds

**Unlawful discontinuity**

- Novelty-driven method switching every episode  
- Persisting with a failing strategy solely because it was assembled at session start  
- Changing strategy without interpreting evidence

### 6.2 Continuity across sittings

Strategy memory may persist across sessions when the same intention and diagnosis remain active. A new sitting may resume a paused micro-sequence. Twin Update and deferred educational memory make that resumption intelligible.

---

## 7. Concept Continuity

### 7.1 Meaning

**Concept continuity** means the session’s episodes share a coherent conceptual focus — one concept facet, one objective, or a justified dependency move (prerequisite → dependent) — so the student experiences tutoring rather than topic thrash.

### 7.2 Lawful focus patterns

| Pattern | Description |
|---------|-------------|
| **Single objective arc** | All episodes serve one learning objective |
| **Prerequisite bridge** | Brief upstream repair, then resume dependent objective |
| **Contrastive pair** | Near concepts contrasted for misconception repair (still one governing intention) |
| **Retrieval of prior objective** | Spaced return that may sit beside light work on a current aim — only if capacity and coherence allow |

### 7.3 Concept Network guidance

Navigation through the Concept Network and Knowledge Dependencies constrains what may share a sitting. Remediation edges may activate from learner state; assembly must honour those edges rather than force syllabus page-order when diagnosis says otherwise.

### 7.4 Forbidden concept thrash

- Jumping across unrelated topics for engagement  
- Declaring multi-topic coverage success because the clock filled  
- Transfer across concepts that were never introduced

---

## 8. Reflection Placement

### 8.1 Per-episode reflection

Every Learning Episode that claims to teach should produce reflection with consequence — or lawfully defer reflection while preserving that consequence for the next interpretative turn.

### 8.2 Session-level reflection

A session may add a short closing reflection that summarises the sitting’s arc (difficulty, uncertainty, felt readiness across the micro-sequence). Session reflection **supplements**; it does not erase per-episode reflection obligations.

**Lawful**

- Brief per-episode reflection after each atom  
- Compressed reflection when lifecycle compression rules allow, with evidence identity preserved  
- Session-end metacognitive summary after the last episode

**Unlawful**

- One decorative end-of-session survey substituting for all episode reflection  
- Reflection that cannot change future teaching  
- Fabricated or skipped reflection while claiming tutoring completeness

### 8.3 Placement relative to Twin Update

Reflection feeds Twin Update. Assembly should not close a session in a way that systematically strands episodes without reflection input to the Twin.

---

## 9. Stopping Conditions

Stopping is an educational decision (Decision D14), not merely a timer event.

### 9.1 Prefer stop when

- sustainable capacity is exhausted;  
- starting another episode would prevent honest evidence and reflection;  
- the atomic purpose of the current episode is complete and no coherent next episode fits;  
- affective collapse requires Recovery rather than more content;  
- Priority deferred work belongs in a later sitting (spacing for retention).

### 9.2 Prefer continue when

- a micro-sequence step is ready and capacity remains;  
- a repair interrupt can complete within remaining capacity;  
- discrimination evidence is one short probe away and the student can sustain it.

### 9.3 Hard educational stops

Stop rather than:

- begin transfer or exam-application episodes without time to evidence them;  
- push volume after an unresolved misconception interrupt was identified but not addressed;  
- convert fatigue into false “completion of topic.”

---

## 10. Session Completion

### 10.1 What completion means

**Session completion** means the sitting has closed: episodes enacted (or lawfully stopped), evidence and reflection captured as required, Twin Update supplied for the work done, and a Next Recommendation issued for later return.

Session completion is **administrative and experiential closure of a sitting**.

### 10.2 What completion does not mean

Session completion does **not** mean:

- mastery of the objective or topic;  
- journey completion;  
- curriculum progress as understanding;  
- licence to erase unresolved diagnoses;  
- that deferred micro-sequence steps are abandoned (they remain in educational memory).

### 10.3 Completion outputs (educational)

| Output | Role |
|--------|------|
| Episode evaluations | Per-atom educational results |
| Evidence set | Factual spine for the sitting |
| Reflection artefacts | Soft evidence with consequence |
| Twin Update inputs | Lawful belief revision |
| Next Recommendation | Explainable Adaptation |
| Deferred arc memory | What remains of an unfinished micro-sequence |

### 10.4 Incomplete sittings

A sitting may end incomplete relative to a planned arc. That is lawful when stopping conditions fire. Orchestration must preserve continuity so the next arrival can resume without pretending the arc finished.

---

## 11. Relationship to Product Surfaces

Product surfaces (Session Experience, Home, Journey) may *present* assembled sessions. They do not own assembly law. Educational assembly is determined by orchestration, diagnosis, episode types, strategy composition, and sequence doctrine — then projected into UI.

One screen may show multiple episodes; one episode may span screens. Session identity remains educational: a bounded sitting of coherent episodes.

---

## 12. Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Session = one mega-lesson with no episode identity | Loses atomic evaluation |
| Maximise minutes regardless of coherence | Burns scarce time |
| Ignore repair interrupts to “finish the plan” | Strengthens wrong models |
| Skip reflection to save time | Breaks consequence and Twin honesty |
| Declare topic complete at session end | Completion ≠ mastery |
| Resume tomorrow with no memory of deferred arc | Breaks continuity |

---

## 13. Summary Propositions

1. Sessions assemble Learning Episodes; they do not replace them as atoms.  
2. Ordering follows priority, dependency, micro-sequences, and strategy composition.  
3. Atomicity, strategy continuity, and concept continuity make a sitting feel like tutoring.  
4. Reflection belongs per episode and may be summarised at session end without erasure.  
5. Stopping and completion protect honesty: sittings close; mastery is never conferred by the clock.
