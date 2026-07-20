# Concept Architecture

**Document ID:** V2-SKA-002  
**Classification:** Educational Architecture — Subject Knowledge Foundation  
**Status:** Authoritative architecture of the teachable concept  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  

**Related:** [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md) · [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md) · [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md) · [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md)

---

## 1. Purpose

This document defines what makes a **Concept** teachable in Kwalitec Version 2.

A named idea is not automatically a teachable concept. Teachability requires a structured educational anatomy: meaning, boundaries, prerequisites, connections, misconceptions, representations, examples, applications, transfer opportunities, and mastery indicators.

This architecture answers:

> **What must be true of a concept for a tutor to teach it, diagnose it, and recognise progress on it?**

It does not author content for any subject. It specifies the *structure* any discipline’s concepts must be able to fill.

---

## 2. Governing Claim

> A concept is teachable when a tutor can make its core meaning intelligible, mark its boundaries, locate it among prerequisites and neighbours, confront typical misconceptions, and recognise evidence of grasp under application and transfer.

A label in a syllabus index, without this anatomy, is a filing tag — not a teachable concept.

---

## 3. Anatomy of a Teachable Concept

Every teachable concept has the following architectural facets. Facets may be thin for elementary ideas and rich for advanced ones; none may be permanently undefined without educational cost.

```text
Teachable Concept
├── Core meaning
├── Boundaries
├── Prerequisites
├── Connections
├── Typical misconceptions
├── Representations
├── Examples
├── Counterexamples
├── Applications
├── Transfer opportunities
└── Mastery indicators
```

---

## 4. Facet Definitions

### 4.1 Core Meaning

**What it is**  
The essential content of the concept: what it denotes, what role it plays in the subject, and why it exists as a distinct idea.

**Educational role**  
Without core meaning, teaching degenerates into symbol manipulation or keyword recognition.

**Tutor obligation**  
Be able to state the core meaning in precise subject language and in a learner-accessible paraphrase that does not falsify the precise meaning.

**Inadequate substitutes**  
A formula alone; a one-word label; “it’s in Chapter 6.”

**Illustration**  
Core meaning of *force of mortality*: the instantaneous rate of mortality at a given age — the continuous analogue of a mortality rate — used to construct survival models and present values of contingent benefits.

---

### 4.2 Boundaries

**What it is**  
Where the concept begins and ends: what falls inside, what falls outside, and which neighbouring ideas are easily confused with it.

**Educational role**  
Boundaries prevent overgeneralisation and support accurate classification under exam rewording.

**Tutor obligation**  
Know contrast pairs and scope limits (assumptions, domains of definition, mutually exclusive variants).

**Inadequate substitutes**  
Open-ended “etc.”; treating near-synonyms as identical without analysis.

**Illustration**  
Boundaries for *annuity-due* vs *annuity-immediate*: payment timing at the start vs end of periods — same broad family, different cash-flow structure, different formulae.

---

### 4.3 Prerequisites

**What it is**  
The knowledge entities that must be adequately in place before the concept can be introduced as a primary teaching aim (see [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md)).

**Educational role**  
Prerequisites protect intelligibility. Teaching past absences produces mimicry.

**Tutor obligation**  
Distinguish *required* from *helpful* prerequisites; diagnose missing foundations before attributing failure to the target concept.

**Inadequate substitutes**  
Assuming “they must have done earlier chapters”; equating topic completion with prerequisite mastery.

**Illustration**  
Before *net premium via equivalence principle*, required prerequisites typically include present value of benefits and premiums, and the meaning of equivalence of EPVs.

---

### 4.4 Connections

**What it is**  
The concept’s place in the subject’s relational structure: what it explains, what it specialises or generalises, what it supports, and what derives from it (see [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md)).

**Educational role**  
Connection is a learning dimension. Isolated concepts fail combination questions and transfer.

**Tutor obligation**  
Teach the concept as a node in a network, not as a flashcard island.

**Inadequate substitutes**  
A flat list of “related topics” without relationship type; encyclopaedic digression that loses the teaching aim.

**Illustration**  
*Equivalence principle* connects to net premium, gross premium (when expenses enter), reserve identities, and equation-of-value reasoning across interest theory and contingencies.

---

### 4.5 Typical Misconceptions

**What it is**  
Stable wrong models students commonly form about this concept — patterned, not random.

**Educational role**  
Anticipating misconceptions allows explicit contrast and diagnosis rather than hopeful volume of practice.

**Tutor obligation**  
Know at least the high-frequency misconceptions for concepts central to the syllabus; treat evidence of patterned error as misconception until proven otherwise.

**Inadequate substitutes**  
“Students find this hard”; listing every possible mistake including slips.

**Illustration**  
Typical misconception: continuous and discrete life-contingent models differ only notationally, so formulae may be swapped freely.

---

### 4.6 Representations

**What it is**  
The legitimate modes through which the concept can be shown: verbal, symbolic, graphical, tabular, diagrammatic, and so on.

**Educational role**  
Multiple representations deepen understanding; translation across representations is itself evidence.

**Tutor obligation**  
Be able to move among the representations the discipline treats as standard for this concept.

**Inadequate substitutes**  
A single preferred picture treated as the whole concept; decorative visuals without structural content.

**Illustration**  
Present value represented as formula, as discounted cash-flow timeline, and as verbal “value today of future payments under interest.”

---

### 4.7 Examples

**What it is**  
Clear positive instances that exhibit the concept under conditions where it applies cleanly.

**Educational role**  
Examples make structure perceptible and seed initial procedures.

**Tutor obligation**  
Maintain a small set of canonical examples, then vary them; avoid teaching only one clone.

**Inadequate substitutes**  
An example that secretly relies on unstated advanced prerequisites; an example so ornate it obscures the concept.

**Illustration**  
A constant-force whole-life assurance EPV as a clean first example of integrating discounted contingent payments.

---

### 4.8 Counterexamples

**What it is**  
Instances that mark where the concept or a tempting rule about it fails.

**Educational role**  
Counterexamples teach boundaries and dismantle misconceptions.

**Tutor obligation**  
Pair important examples with at least one boundary-marking counterexample for concepts students overgeneralise.

**Inadequate substitutes**  
Harder questions that still fit the same rule; gotchas outside syllabus legitimacy.

**Illustration**  
Applying a continuous annuity formula to clearly discrete payments without adjustment — a counterexample to “any bar notation is interchangeable.”

---

### 4.9 Applications

**What it is**  
Legitimate use situations (*Application Contexts*) in which the concept is put to work to classify, derive, compute, decide, or explain.

**Educational role**  
Application converts meaning into competence; professional exams heavily tax application.

**Tutor obligation**  
Connect the concept to tasks the syllabus may demand — not only to definitions.

**Inadequate substitutes**  
Application as pure drill with no conceptual check; application only on identical clones.

**Illustration**  
Using select mortality to compute a probability for a life newly underwritten — an application of the select vs ultimate distinction.

---

### 4.10 Transfer Opportunities

**What it is**  
Planned variations (*Transfer Contexts*) that change surface form while preserving the underlying conceptual demand.

**Educational role**  
Transfer opportunities test whether the concept is understood as structure rather than as a template.

**Tutor obligation**  
Design or select variations that remain syllabus-legitimate and objective-aligned.

**Inadequate substitutes**  
Novelty for its own sake; combining so many new elements that the objective becomes unclear.

**Illustration**  
After drills at a fixed interest rate, requiring the same contingent present-value reasoning under a reworded contract and a different rate basis.

---

### 4.11 Mastery Indicators

**What it is**  
Observable patterns of performance and explanation that support — never by themselves prove in a single event — durable command of the concept.

**Educational role**  
Indicators guide evidence interpretation. They keep “mastery” from collapsing into completion or one correct answer.

**Tutor obligation**  
Seek converging indicators across explanation, correct use under variation, boundary sensitivity, and retention over time (aligned with the Understanding and Learning Models).

**Characteristic positive indicators**

| Indicator | Suggests |
|-----------|----------|
| Accurate definition *and* paraphrase | Vocabulary stable, not mere keyword |
| Correct classification of novel wordings | Boundary grasp |
| Explanation of *why* a method applies | Principle-level grasp |
| Success after delay | Retention contributing to mastery |
| Success under transfer variation | Flexible understanding |
| Detection and repair of own near-miss | Self-monitoring |

**Characteristic false indicators**

| False indicator | Why it fails |
|-----------------|--------------|
| Topic marked complete | Coverage ≠ grasp |
| One correct MCQ | Recognition / luck / mimicry |
| High confidence alone | Feeling ≠ capacity |
| Fast clone drill success only | May be template lock |
| Formula recited without conditions | Interpretation missing |

---

## 5. Minimal Completeness for Teaching

A concept may be introduced when the tutor (or curriculum design) can specify at least:

1. Core meaning  
2. Primary boundaries (including one key contrast)  
3. Required prerequisites  
4. One canonical example  
5. One high-frequency misconception *or* an explicit note that evidence is still thin  
6. At least one application context  
7. Provisional mastery indicators for the associated learning objective  

Representations, counterexamples, rich connection maps, and transfer batteries deepen teachability; their absence in early drafts is a design debt, not a licence to treat the concept as fully articulated.

---

## 6. Concept vs Related Entities

| Entity | Difference from Concept |
|--------|-------------------------|
| **Definition** | Fixes wording of meaning; does not exhaust the concept |
| **Formula** | Symbolic representation of relations; needs interpretation |
| **Procedure** | How to compute or construct; must be grounded in the concept |
| **Skill** | Capacity class that uses the concept in action |
| **Topic** | Syllabus container that may house many concepts |
| **Learning Objective** | Aim stating what to know/do regarding the concept |
| **Misconception** | Wrong model *about* the concept |

---

## 7. Lifecycle of Conceptual Grasp (Educational, Not Software)

Conceptual grasp typically progresses:

```text
Recognition → Explanation → Conditional use → Connected use → Transfer → Retained command
```

Tutors must not treat earlier stages as later ones. Recognition is not explanation; clone use is not transfer; same-day success is not retained command.

This progression aligns with the Understanding Model’s ladder; the Concept Architecture supplies the *object* that ladder climbs.

---

## 8. Tutor Use of This Architecture

When preparing to teach a concept, the tutor reasons through the facets:

1. **What is the core meaning I must establish?**  
2. **What boundary will students likely violate?**  
3. **What prerequisites must I verify or repair?**  
4. **What connections matter for this objective (not all connections)?**  
5. **Which misconception should I probe or confront?**  
6. **Which representation best reveals structure now?**  
7. **Which example / counterexample pair serves the intention?**  
8. **What application and transfer evidence will I seek next?**  

Episode design and strategy selection (elsewhere) consume these answers; they do not replace them.

---

## 9. Architectural Ambiguities (Recorded)

1. **Composite concepts** — Some syllabus items are bundles (e.g. “gross premium reserves”). Design may treat a bundle as a concept cluster with a parent objective, or as one concept with internal parts — but must declare which.
2. **Notational variants** — Different texts use different symbols for the same concept. The concept is the meaning; notation is a representation family. Equivalence must be taught explicitly.
3. **Threshold of “typical” misconception** — Frequency varies by population. “Typical” means educationally recurrent in the target candidate population, not universal.
4. **Mastery indicator aggregation** — How indicators combine into Twin estimates is an evidence/Twin concern; this document only defines the educational meaning of indicators.

---

## 10. Related Documents

- [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  
- [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md)  
- [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md)  
- [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md)  
- [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md)  
- [`LEARNING_MODEL.md`](LEARNING_MODEL.md)  
