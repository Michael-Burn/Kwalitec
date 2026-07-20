# Learning Episode Architecture

**Document ID:** V2-LEA-001  
**Classification:** Educational Architecture — Learning Episode Foundation  
**Status:** Authoritative architectural definition  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural (educational composition unit)  
**Audience:** Product, educational governance, architecture, future implementers  

**Authority relationships**

| Document | Relationship |
|----------|--------------|
| [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md) | Parent vocabulary; this document specialises *Learning Episode* |
| [`LEARNING_EPISODE_LIFECYCLE.md`](LEARNING_EPISODE_LIFECYCLE.md) | Stage-by-stage episode lifecycle |
| [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) | Catalogue of educational episode categories |
| [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) | Binding episode rules |
| [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md) | How episodes compose into larger educational structures |
| [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md) | Foundational principle of one capability per episode |
| [`TUTOR_MODEL.md`](TUTOR_MODEL.md) | Tutor loop that selects and evaluates episodes |
| [`LEARNING_MODEL.md`](LEARNING_MODEL.md) | Five learning dimensions episodes may advance |
| [`../EDUCATIONAL_PRINCIPLES.md`](../EDUCATIONAL_PRINCIPLES.md) | Journey / session principles episodes must respect |
| [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) | Highest educational law |

---

## 1. Purpose

This document defines exactly what a **Learning Episode** is in Kwalitec Version 2.

A Learning Episode is the **fundamental educational unit** from which every tutoring interaction is composed. Everything Kwalitec teaches should ultimately be expressible as one or more Learning Episodes.

This architecture is intentionally **technology-independent**. It describes education, not software. It remains valid across UI frameworks, storage models, and engine implementations.

---

## 2. Definition

**Learning Episode:** a bounded educational engagement with **exactly one deliberate educational purpose** — to produce **one** intentional improvement in the student’s educational capability relative to a curriculum-grounded learning objective — during which teaching (or an equivalent instructional opportunity), student interaction, evidence collection, and reflection occur under a chosen teaching strategy.

### Governing sentence

> A Learning Episode exists to produce one deliberate educational improvement.  
> Not multiple.  
> One.

That single improvement is the episode’s **educational purpose**. Secondary effects may occur (for example, incidental practice while repairing a misconception). They do not expand the episode’s declared purpose. If two distinct improvements are both required, they require two episodes — or a deliberate micro-sequence of episodes (see [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md)).

### What a Learning Episode is not

A Learning Episode is **educational**. It is not:

| Not this | Why |
|----------|-----|
| A UI component | Presentation is not educational purpose |
| A page or screen | One episode may span several screens; one screen may host several episodes |
| An “activity” in the product-mechanical sense | Activities may *realise* episodes; they are not identical to them |
| A database row | Persistence is implementation, not educational meaning |
| A prompt or message | Language may deliver teaching; a prompt is not the episode |
| A calendar block or timer | Duration may constrain an episode; time alone is not purpose |
| A mission, session, or journey | Those are larger (or differently scoped) educational containers |
| A mastery certificate | Episodes never declare mastery |

---

## 3. Educational Purpose

The educational purpose of Learning Episodes is to make tutoring **composable, diagnosable, and honest**.

Without episodes as the atomic teaching unit:

- progress is narrated as time spent or tasks closed;
- teaching strategies become vague “do more”;
- evidence cannot be attributed to a clear instructional intent;
- sessions and journeys accumulate activity without a teachable story.

With episodes:

- every tutoring move answers *what single educational change was intended?*;
- diagnosis selects an episode type matched to need;
- evidence evaluates whether that one purpose advanced;
- twin updates remain interpretable because each update can cite episode outcomes.

Episodes are how Kwalitec discharges the Tutor obligation at the smallest coherent grain of teaching.

---

## 4. Responsibilities

A Learning Episode is responsible for:

1. **Declaring one educational purpose** — a single intended capability improvement, named relative to a learning objective and (typically) one primary learning dimension.  
2. **Anchoring to curriculum** — remaining accountable to official syllabus identity and a precise learning objective.  
3. **Embodying a teaching strategy** — applying one primary instructional approach matched to educational diagnosis.  
4. **Providing instructional opportunity** — teaching (or lawful equivalent) before post-instruction judgement of the taught aim.  
5. **Eliciting student interaction** — requiring observable student work, not passive exposure alone.  
6. **Producing evidence** — recording educational happenings attributable to this episode’s purpose.  
7. **Closing with reflection** — capturing structured student reflection that can influence the next educational decision.  
8. **Supporting episode evaluation** — enabling a modest judgement of whether the deliberate improvement occurred, partially occurred, or did not.  
9. **Feeding lawful twin update inputs** — contributing evidence and evaluation outcomes without writing mastery theatre.  
10. **Remaining atomic** — refusing to smuggle a second educational purpose into the same episode (see [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md)).

---

## 5. Educational Boundaries

### 5.1 In scope

- One purpose, one primary objective, one primary strategy  
- Instruction, interaction, evidence, reflection, and evaluation for that purpose  
- Attribution of outcomes to the student, journey, and session contexts that contain the episode  

### 5.2 Out of scope

| Concern | Owner elsewhere |
|---------|-----------------|
| Multi-topic journey planning | Learning Journey |
| Daily commitment / mission packaging | Mission / recommendation layers |
| Learner-state belief / mastery estimates | Student Digital Twin |
| Syllabus structure and official ordering | Curriculum |
| Pedagogy catalogue design | Instructional Blueprint (strategy inventory) |
| UI navigation and screens | Presentation / Session Experience |
| Persistence schemas | Infrastructure |

### 5.3 Boundary with Teaching Strategy

A **Teaching Strategy** is the instructional *approach* (for example worked-example fading, conceptual contrast, spaced retrieval).  
A **Learning Episode** is the *bounded engagement* that applies a strategy to one purpose.

Strategy without episode is an unbound method. Episode without strategy is undirected activity.

### 5.4 Boundary with Session and Journey

| Concept | Educational grain |
|---------|-------------------|
| Learning Episode | One deliberate improvement |
| Micro Sequence | Ordered set of episodes serving a short arc |
| Learning Session | Bounded sitting that may contain one or more episodes |
| Learning Journey | Multi-session path through a topic toward educational completion |
| Curriculum Progress | Coverage / objective posture relative to syllabus |

Sessions and journeys **contain** episodes. They do not replace them.

---

## 6. Inputs

A Learning Episode requires, at minimum:

| Input | Meaning |
|-------|---------|
| **Student identity** | Whose educational state is being addressed |
| **Educational diagnosis** | Why this episode is needed now |
| **Learning objective** | Curriculum-grounded aim the purpose serves |
| **Teaching goal** | The single deliberate improvement sought |
| **Teaching strategy** | Instructional approach matched to diagnosis and goal |
| **Episode type** | Educational category (see [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md)) |
| **Context** | Journey / session / prior evidence relevant to selection |
| **Constraints** | Time, exam proximity, fatigue, lawful mode (learn / revise) when applicable |

Optional but common inputs: known misconception identity, prerequisite status, twin estimates (as *context*, never as invented evidence), prior episode evaluation outcomes.

---

## 7. Outputs

A completed (or lawfully aborted) Learning Episode produces:

| Output | Meaning |
|--------|---------|
| **Evidence** | Observed educational happenings during the episode |
| **Reflection** | Structured student metacognitive signal for this episode |
| **Episode evaluation** | Modest judgement relative to the single teaching goal |
| **Understanding / capability delta signal** | What appears to have changed — provisional, evidential |
| **Misconception disposition** | Resolved, reduced, unchanged, or newly recorded |
| **Next educational decision inputs** | Facts the tutor loop needs to Adapt |
| **Twin update inputs** | Lawful evidence package for learner-state interpretation |

Outputs never include: a mastery declaration; a claim that the topic is complete; a substitution of confidence for evidence.

---

## 8. Relationships

### 8.1 Student

The episode exists for one student. Educational ownership of outcomes belongs to the learner. The episode does not exist as an abstract content unit detached from a learner’s diagnosed need — though episode *types* and instructional materials may be reusable templates.

### 8.2 Journey

Episodes advance a Learning Journey when their learning objective belongs to the journey’s topic. A journey accumulates many episodes over many sessions. Journey completion criteria are never satisfied by a single episode alone.

### 8.3 Session

A Learning Session is a bounded sitting. It may contain one episode or a micro-sequence of episodes. Session completion is administrative/educational closure of the sitting; it is not episode mastery and not topic complete.

### 8.4 Teaching Strategy

The strategy is selected *before* or *as part of* episode selection, from diagnosis. The episode realises that strategy for one purpose. Changing strategy mid-episode because the purpose changed means the episode should end and a new episode begin.

### 8.5 Evidence

Every episode must produce evidence. Evidence is attributed to the episode’s purpose and objective. Thin evidence yields honest uncertainty in evaluation — not invented success.

### 8.6 Reflection

Reflection belongs to the episode (or to the session’s episode set when a session closes multiple episodes). Reflection is soft evidence and must be capable of influencing the next educational decision. Fabricated reflection is educationally void.

### 8.7 Digital Twin

The Twin interprets accumulated evidence. Episodes supply evidence and evaluation outcomes; they do not mutate Twin belief directly as an educational authority. Episodes never write “mastered” into the Twin.

### 8.8 Learning Objectives

An episode **cannot exist without a learning objective**. The objective is the curriculum-grounded aim; the teaching goal is the single deliberate improvement toward that aim (for example “repair select-vs-ultimate confusion” toward the objective “interpret select mortality tables”).

---

## 9. Educational Atomicity (Summary)

Educational Atomicity requires that every Learning Episode improve **one** educational capability.

| Good | Poor |
|------|------|
| Teach exponential-family intuition | Teach all generalised linear models |
| Repair one misconception | Revise an entire chapter |
| Practise retrieval of one method family | “Do Chapter 4” |

Full doctrine: [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md).

Atomicity is compatible with the Learning Model requirement that an episode advance **at least one** learning dimension: the episode’s single purpose typically names one primary dimension (Understanding, Application, Connection, Retention, or Transfer). It does not advance “everything at once.”

---

## 10. Composition Hierarchy

```text
Learning Episode
       ↓
 Micro Sequence
       ↓
 Learning Session
       ↓
 Learning Journey
       ↓
Curriculum Progress
```

Everything Kwalitec teaches should reduce to episodes (and lawful sequences of episodes). Larger structures organise, constrain, and accumulate — they do not invent a second educational ontology that bypasses episodes.

---

## 11. Independence from Implementation

This architecture must remain valid if:

- the product UI is redesigned;
- sessions render as one screen or many;
- engines are rewritten;
- storage schemas change;
- content formats change.

Implementation may *project* episodes onto screens, activities, and rows. Implementation must never redefine what an episode *is*.

**Cardinality reminders for implementers (non-normative of UI):**

- One Learning Episode may span several screens.  
- One screen may contain multiple Learning Episodes.  
- Mapping is a presentation concern; educational identity remains the episode.

---

## 12. Governance

1. New tutoring features must be expressible as Learning Episode(s) or explain why they are non-teaching utilities.  
2. Episode types may expand only by deliberate amendment of [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md).  
3. Conflict with the Educational Constitution is resolved in favour of the Constitution until formal amendment.  
4. Product language may simplify wording for students but must not collapse episode completion with mastery.  
5. This document is intended as a **permanent** Version 2 architectural reference.

---

## 13. Summary Propositions

1. A Learning Episode is the fundamental educational unit of tutoring in Kwalitec.  
2. Each episode has exactly one deliberate educational purpose — one intentional improvement.  
3. Episodes are educational concepts, not UI, storage, or prompt artefacts.  
4. Episodes produce evidence, invite reflection, and never declare mastery.  
5. Sessions, journeys, and curriculum progress compose episodes; they do not replace them.  
6. Educational Atomicity governs episode scope.
