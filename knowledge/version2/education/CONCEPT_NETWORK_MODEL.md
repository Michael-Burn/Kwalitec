# Concept Network Model

**Document ID:** V2-SKA-004  
**Classification:** Educational Architecture — Subject Knowledge Foundation  
**Status:** Authoritative model of conceptual relationships  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  

**Related:** [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md) · [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md) · [`TUTOR_MODEL.md`](TUTOR_MODEL.md) · [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md)

---

## 1. Purpose

This document defines how **concepts connect** in a subject: the Concept Network.

It answers:

> **What relationship types structure teachable knowledge, and how does a tutor navigate them?**

A subject is not a pile of definitions. It is a network of meanings. Tutoring is navigation and intervention on that network — guided by diagnosis, intention, and dependency — not random hops between flashcards.

---

## 2. Definition

**Concept Network:** the structured set of concepts in a discipline together with typed relationships among them (and, where relevant, to closely allied skills, procedures, and principles treated as neighbouring nodes).

The network is educational architecture. It is not a UI graph widget, not a database schema, and not an automatic embedding space.

### Governing sentence

> Concepts gain power through relationships.  
> A tutor teaches nodes *and* edges.  
> Isolated nodes produce brittle examination performance.

---

## 3. Relationship Types

Each type below is a directed or symmetric educational relation. Direction, where present, matters for teaching order and explanation.

---

### 3.1 Depends on

**Meaning**  
Target requires source for intelligibility or honest primary-aim teaching (educational dependency; see [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md)).

**Direction**  
Target → Source (“B depends on A”).

**Tutor use**  
Before teaching B, verify A; if A is weak, remediate A or change aim.

**Example**  
Gross premium reserves *depend on* understanding of expenses loading and net premium ideas.

---

### 3.2 Explains

**Meaning**  
Source provides the explanatory account that makes the target intelligible (principle or deeper concept explaining a method, formula, or narrower idea).

**Direction**  
Source → Target (“A explains B”).

**Tutor use**  
When students can compute B but not justify it, teach along the *explains* edge toward A.

**Example**  
Equivalence principle *explains* net premium formulae.

---

### 3.3 Generalises

**Meaning**  
Source is a broader idea that subsumes the target as a special case or instance class.

**Direction**  
Source → Target (“A generalises B” / A is more general than B).

**Tutor use**  
Move to the general when transfer across instances is required; return to the special for concreteness.

**Example**  
Present value of contingent payments *generalises* particular assurance and annuity valuations.

---

### 3.4 Specialises

**Meaning**  
Source is a narrower, constrained, or particular form of the target (inverse companion of generalises).

**Direction**  
Source → Target (“A specialises B”).

**Tutor use**  
Introduce via a clean special case, then climb to the general; or descend from general to special for application.

**Example**  
Constant-force mortality *specialises* general force-of-mortality models.

---

### 3.5 Contrasts with

**Meaning**  
Two concepts are educationally adjacent through difference: distinguishing them is necessary to avoid confusion.

**Direction**  
Symmetric for teaching purposes (contrast pair).

**Tutor use**  
Use contrastive teaching, dual examples, and forced classification when diagnosis shows mix-ups.

**Example**  
Annuity-due *contrasts with* annuity-immediate; select *contrasts with* ultimate mortality.

---

### 3.6 Supports

**Meaning**  
Source strengthens, scaffolds, or makes more robust the grasp or use of the target without being a full required prerequisite in every pathway.

**Direction**  
Source → Target (“A supports B”).

**Tutor use**  
Optional strengthening when time and priority allow; helpful for retention and connection.

**Example**  
Cash-flow diagram literacy *supports* verbal contract interpretation for contingencies.

---

### 3.7 Applies to

**Meaning**  
Source (concept, principle, or procedure) is used in the domain of the target situation class or topic region.

**Direction**  
Source → Target (“A applies to B”).

**Tutor use**  
Build application episodes that make the edge explicit: “we are using A in situation B.”

**Example**  
Maximum likelihood *applies to* parameter estimation for specified GLM families.

---

### 3.8 Derived from

**Meaning**  
Target is obtained from source by legitimate derivation, transformation, or definitional construction.

**Direction**  
Target → Source (“B is derived from A”).

**Tutor use**  
When students memorise B, reconstruct the derivation from A to restore meaning.

**Example**  
A particular annuity identity *derived from* the present-value definition and payment timing assumptions.

---

### 3.9 Equivalent to

**Meaning**  
Two expressions, formulations, or concept presentations denote the same underlying idea under stated conditions (notational or representational equivalence).

**Direction**  
Symmetric under stated conditions.

**Tutor use**  
Teach translation between equivalents; test whether students recognise sameness beneath surface form.

**Example**  
A continuous whole-life assurance integral form *equivalent to* a recognised actuarial notation under the same assumptions.

---

### 3.10 Part of

**Meaning**  
Source is a constituent of a composite target concept or structured whole.

**Direction**  
Source → Target (“A is part of B”).

**Tutor use**  
Teach parts before demanding fluent command of the whole; diagnose which part failed when the composite fails.

**Example**  
Interest discounting and survival probability are each *part of* a contingent present-value construction.

---

## 4. Relationship Summary Table

| Type | Primary educational job | Typical tutoring move |
|------|-------------------------|------------------------|
| Depends on | Enforce readiness | Foundation check / remediate |
| Explains | Restore justification | Teach principle behind method |
| Generalises | Expand scope | Lift from instance to pattern |
| Specialises | Concrete entry / precise case | Descend to clean case |
| Contrasts with | Disambiguate | Side-by-side contrast |
| Supports | Strengthen | Scaffold or optional prep |
| Applies to | Situate use | Application episode |
| Derived from | Rebuild meaning | Re-derive, don’t only recall |
| Equivalent to | Translate forms | Notation / representation switch |
| Part of | Manage composition | Teach constituents, then compose |

---

## 5. Network Properties (Educational)

### 5.1 Local neighbourhood

For any concept, the tutor should know its **local neighbourhood**: required dependencies, key contrasts, the principle that explains it, and one or two important applications. Global completeness is ideal; local navigability is mandatory for teaching.

### 5.2 Hubs and bridges

Some concepts are **hubs** (many edges) or **bridges** (join regions). These deserve early clarity because failure there cascades. Hub status is educational, not popularity of exam keywords alone — though correlation is common.

### 5.3 Clusters

Syllabus modules often correspond to **clusters** in the network. Cross-cluster edges are where combination questions and transfer live; they must not be treated as rare decoration.

### 5.4 Multiple paths

More than one explanatory path may exist to a concept. Tutors may choose a path that fits diagnosis and prerequisites; they must not invent paths that violate required dependencies.

---

## 6. How a Tutor Navigates the Concept Network

Navigation is purposeful movement along typed edges under the tutor reasoning loop (diagnosis → hypothesis → intention → strategy → episode → evidence).

### 6.1 Entry

The tutor enters at a node justified by:

- syllabus-grounded learning objective;  
- diagnosed need (gap, misconception, fluency deficit, retention fade, transfer failure);  
- dependency readiness.

Random entry for novelty is not tutoring.

### 6.2 Orientation

At the current node, the tutor orients using Concept Architecture facets: meaning, boundaries, misconceptions, representations.

### 6.3 Edge selection

Given intention, the tutor selects edges:

| If the problem is… | Prefer edges… |
|--------------------|---------------|
| Missing foundation | *Depends on* (walk toward sources) |
| Can compute, can’t justify | *Explains*, *Derived from* |
| Confuses two ideas | *Contrasts with* |
| Clone-bound | *Applies to*, then transfer variants |
| Lost in abstraction | *Specialises* toward a clean case |
| Can’t see the pattern | *Generalises* from known instances |
| Notation confusion | *Equivalent to* across representations |
| Composite failure | *Part of* (isolate failed constituent) |

### 6.4 Traversal discipline

- **Atomicity** — one educational capability per episode; do not tour the whole neighbourhood in one episode.  
- **Return** — after a foundation excursion, return to the original aim or explicitly revise the aim.  
- **Evidence gates** — do not claim the target node is mastered because a neighbouring node was taught.  
- **Explainability** — the next hop should be narratable: “We need X because Y depends on it.”

### 6.5 Exit and transfer

Exit toward application and transfer contexts that exercise the same node under variation, and toward connected nodes only when connection itself is the intentional aim.

### 6.6 Navigation sketch

```text
Diagnosed need at Concept B
        │
        ├─ missing prerequisite? ──► walk Depends-on to A ──► remediate A
        │                              │
        │                              └─ return / re-aim
        │
        ├─ misconception vs contrast pair C? ──► Contrasts-with edge ──► repair
        │
        ├─ ritual procedure? ──► Explains / Derived-from to principle P
        │
        └─ clone success only? ──► Applies-to + Transfer contexts
```

---

## 7. What Navigation Is Not

| Not navigation | Why |
|----------------|-----|
| Chapter thrash | Order without typed purpose |
| Exhaustive graph tours | Violates atomicity; overwhelms |
| Keyword linking without relationship type | Fake connection |
| UI “related topics” clickstreams alone | Presentation ≠ educational reasoning |
| Embedding similarity as dependency | Statistical nearness ≠ learnability |

---

## 8. Network and Other Models

| Model | Role relative to the network |
|-------|------------------------------|
| Subject Knowledge Model | Defines node kinds and artefacts |
| Concept Architecture | Defines the internal anatomy of a node |
| Knowledge Dependency Model | Specialises *Depends on* and related readiness types |
| Teaching Strategy Architecture | Chooses *how* to teach along a chosen edge/aim |
| Learning Episode Architecture | Enacts one hop’s worth of capability improvement |
| Student Digital Twin | Stores evidential state *on* nodes (and possibly edges) |

---

## 9. Architectural Ambiguities (Recorded)

1. **Edge multiplicity** — Two concepts may share several relationship types at once (e.g. *depends on* and *part of*). Teaching must pick the edge that matches the intention.  
2. **Skill/procedure nodes** — Whether skills and procedures sit inside the concept network as first-class nodes or as attached artefacts is a modelling choice; relationships still apply. Prefer explicitness per curriculum design.  
3. **Symmetric vs directed contrasts** — Contrast is symmetric pedagogically; asymmetry may appear if one member is prerequisite to understanding the other.  
4. **Equivalence conditions** — “Equivalent to” is always conditional on assumptions; teaching must surface those conditions.  
5. **Dynamic edges** — Remediation dependencies activate with learner state; the static network is not the whole story.

---

## 10. Related Documents

- [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  
- [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md)  
- [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md)  
- [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md)  
- [`TUTOR_MODEL.md`](TUTOR_MODEL.md)  
- [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md)  
