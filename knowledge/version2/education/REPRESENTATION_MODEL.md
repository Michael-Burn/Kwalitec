# Representation Model

**Document ID:** V2-SAA-004  
**Classification:** Educational Architecture — Subject Authoring Foundation  
**Status:** Authoritative model of educational representations  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`SUBJECT_AUTHORING_MODEL.md`](SUBJECT_AUTHORING_MODEL.md)  

**Related:** [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md) · [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`APPLICATION_AND_TRANSFER_MODEL.md`](APPLICATION_AND_TRANSFER_MODEL.md) · [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md) · [`AUTHORING_INVARIANTS.md`](AUTHORING_INVARIANTS.md)

---

## 1. Purpose

This document defines **educational representations**: the legitimate modes through which subject structure is made intelligible for teaching, learning, diagnosis, and transfer.

It answers:

> **How may a concept be shown — and when must it be shown in more than one way?**

Representations are educational knowledge artefacts. They are not UI widgets, diagram libraries, or media formats — though software may later render them.

---

## 2. Definition

**Representation:** a mode of presenting subject structure that makes relationships, quantities, conditions, or procedures inspectable — symbolic, verbal, visual, or otherwise — without being identical to the concept itself.

### Governing sentence

> Representations support concepts.  
> They do not replace concepts.  
> Ability to translate among representations is itself evidence of understanding.

---

## 3. Why Representations Matter

Professional examinations and professional practice routinely demand movement across forms: formula ↔ narrative ↔ table ↔ diagram. A student who can only recognise one preferred picture has fragile grasp.

For the tutor:

- Choice of representation is an instructional decision  
- Failure to translate across representations is a diagnostic signal  
- Misconceptions often live inside a single representation and collapse under contrast  

---

## 4. Representation Categories

The following categories are architectural kinds. A given concept may use a subset. Authors name which kinds apply and which are primary.

### 4.1 Symbolic

**What it is**  
Notation, formulae, algebraic identities, formal operators.

**When useful**  
Precision, derivation, compact expression of relationships; standard professional communication.

**Risks**  
Ritual symbol manipulation without meaning; notation treated as the concept.

**Authoring note**  
Always pair primary symbolic forms with conditions of validity and interpretation obligations (aligns with subject invariants on formulae).

---

### 4.2 Verbal

**What it is**  
Natural-language statements of meaning, definitions, principles, and conditions — precise subject language and learner-accessible paraphrase that does not falsify meaning.

**When useful**  
Establishing core meaning; explanation objectives; diagnosing whether the student can say *what* and *why* without hiding behind symbols.

**Risks**  
Vague paraphrases that alter meaning; purely verbal teaching that never connects to operational forms required by exams.

---

### 4.3 Visual

**What it is**  
Spatial depictions that emphasise structure — shapes, icons of process, simple schematics — where the visual encodes relationships (not mere decoration).

**When useful**  
Making part–whole or process structure perceptible; reducing load when introducing new structure.

**Risks**  
Decorative imagery with no structural content; visuals that smuggle unstated assumptions.

**Boundary**  
“Visual” is the broad category; *graphical* and *tabular* are specialised visual-structural forms below.

---

### 4.4 Graphical

**What it is**  
Plots, curves, axes-based relationships, geometric representations of functions or distributions.

**When useful**  
Continuity, rates, comparative magnitudes, sensitivity; concepts whose meaning is relational across a domain (e.g. survival curves, present-value as function of interest).

**Risks**  
Reading graph cosmetics instead of structure; graphs that require untaught scale literacy.

---

### 4.5 Tabular

**What it is**  
Tables of values, schedules, select/ultimate excerpts, commutation layouts, probability arrays.

**When useful**  
Discrete structure, lookup reasoning, comparison across categories, professional table literacy.

**Risks**  
Memorising cells without meaning; tables used where a principle should be derived.

---

### 4.6 Worked Example

**What it is**  
A fully (or partially) unfolded solution path that exhibits procedure and concept use under stated assumptions — including faded or incomplete variants used instructionally.

**When useful**  
Initial procedure acquisition; modelling expert reasoning; reducing search for novices when cognitive load is high.

**Risks**  
Template lock; students copying steps without principle; worked examples that secretly depend on unstated prerequisites.

**Authoring note**  
Worked examples are representations of *use*, not substitutes for application contexts or assessment opportunities.

---

### 4.7 Analogy

**What it is**  
A mapping from a more familiar domain to the target structure that preserves selected relations.

**When useful**  
Early intelligibility; bridging to abstraction; repairing intimidation barriers — when the analogy’s limits are taught.

**Risks**  
Overextension; analogies that teach the wrong structure; cute stories that cannot be retired when precision is required.

**Authoring note**  
Every analogy used as a primary teaching representation should have stated **limits** (where the mapping fails).

---

### 4.8 Simulation

**What it is**  
An interactive or stepped dynamic model that lets the learner vary assumptions and observe consequences (conceptual simulation — not necessarily software).

**When useful**  
Building intuition for dependence on parameters; exploring “what if” under controlled legitimacy; connecting procedure to principle.

**Risks**  
Play without reflection; simulations that train buttons instead of concepts; scope creep beyond syllabus.

---

### 4.9 Counterexample

**What it is**  
An instance that marks where a tempting rule, overgeneralisation, or concept application fails — a boundary representation.

**When useful**  
Misconception repair; teaching boundaries; preventing overgeneralisation after narrow example sets.

**Risks**  
Gotchas outside syllabus legitimacy; “harder questions” that still obey the same rule and thus fail as counterexamples.

**Authoring note**  
Counterexamples are first-class representations of *boundary*, complementary to positive examples.

---

## 5. Additional Common Forms (Non-Exhaustive)

Authors may also use:

| Form | Typical role |
|------|----------------|
| **Timeline / cash-flow diagram** | Contingent payments, deferment, payment timing |
| **Tree / state diagram** | Multi-state models, decision structure |
| **Classification matrix** | Boundary teaching across variants |
| **Proof / derivation sketch** | Principle-level justification |

These specialise visual/graphical/symbolic kinds; they do not escape representation obligations.

---

## 6. When Multiple Representations Are Required

Multiple representations are **required** (not merely nice) when any of the following hold:

1. **Disciplinary standard** — professionals routinely move between the forms (e.g. formula ↔ table ↔ narrative).  
2. **Objective demands translation** — the learning objective includes explaining, interpreting, or switching forms.  
3. **Known misconception is representation-bound** — the wrong model thrives in one form and breaks in another.  
4. **Assessment legitimacy** — examinations tax more than one representational mode for the concept family.  
5. **Transfer design** — surface variation includes representational change as a controlled transfer dimension.

### Minimal rule

> Every concept has at least one representation.  
> Concepts central to examination pathways should have an authored plan for representation diversity — which forms, which are primary, and what translation is expected.

---

## 7. Representation Diversity

**Representation diversity** is the deliberate availability of more than one legitimate mode for the same conceptual structure, plus planned translation among them.

| Diversity level | Meaning |
|-----------------|---------|
| **Single** | One primary mode — acceptable only for narrow or early draft concepts; debt if exam demands more |
| **Paired** | Two modes with explicit translation (e.g. symbolic ↔ verbal) |
| **Rich** | Three or more modes including at least one structural visual/tabular/graphical form where discipline-appropriate |

Diversity is for understanding and transfer — not for decorative variety. Adding a third representation that encodes no new structural access is noise.

### Translation as evidence

Asking a student to move from representation A to B (without coaching the mapping) is a strong probe of understanding when A and B encode the same structure.

---

## 8. Authoring Obligations

For each concept (or tightly bound concept cluster), authors should specify:

| Field | Content |
|-------|---------|
| **Primary representation(s)** | Default mode(s) for first teaching |
| **Supporting representations** | Modes used for contrast, depth, or exam alignment |
| **Required translations** | Which moves students must eventually perform |
| **Misconception links** | Which wrong models attach to which modes |
| **Limits** | Especially for analogies and simulations |

Representations must **support** the concept’s core meaning and boundaries (Authoring Invariants).

---

## 9. Relationship to Teaching and Episodes

Teaching Strategies may choose a representation shift as the instructional move (e.g. from symbolic drill to timeline contrast). Learning Episodes realise that choice. Authoring supplies the lawful representation inventory; runtime selects among it.

---

## 10. Non-Goals

This model does not:

- Prescribe graphic design systems  
- Enumerate every diagram type for every subject  
- Equate “has an image” with “has a representation”  
- Define media production pipelines  

---

## 11. Summary

Educational representations are the modes through which concepts become inspectable. Authors must provide at least one per concept, plan diversity where professional and examination demand require it, and treat translation across representations as both a teaching resource and a source of evidence — without ever letting a representation replace the concept itself.
