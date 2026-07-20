# Concept Decomposition Model

**Document ID:** V2-SAA-002  
**Classification:** Educational Architecture — Subject Authoring Foundation  
**Status:** Authoritative model of syllabus-to-concept decomposition  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`SUBJECT_AUTHORING_MODEL.md`](SUBJECT_AUTHORING_MODEL.md)  

**Related:** [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md) · [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md) · [`MISCONCEPTION_AUTHORING_MODEL.md`](MISCONCEPTION_AUTHORING_MODEL.md) · [`REPRESENTATION_MODEL.md`](REPRESENTATION_MODEL.md) · [`APPLICATION_AND_TRANSFER_MODEL.md`](APPLICATION_AND_TRANSFER_MODEL.md) · [`AUTHORING_INVARIANTS.md`](AUTHORING_INVARIANTS.md)

---

## 1. Purpose

This document defines how a **syllabus objective** is decomposed into teachable educational knowledge under Subject Authoring.

It answers:

> **What stages transform an examinable aim into concepts a tutor can teach?**

Decomposition is educational analysis performed by subject experts. It is not content writing, not automated extraction alone, and not episode scripting.

---

## 2. Governing Claim

> A syllabus objective states what may be examined.  
> Decomposition states what must be understood, in what order, under which wrong models, through which representations, in which uses, and toward which precise learning aims.

Skipping stages produces brittle teaching: objectives without concepts, practice without prerequisites, assessment without aims.

---

## 3. Decomposition Pipeline

```text
Syllabus Objective
        ↓
    Concepts
        ↓
    Dependencies
        ↓
    Misconceptions
        ↓
    Representations
        ↓
    Applications
        ↓
    Transfer Opportunities
        ↓
    Assessment Opportunities
        ↓
    Learning Objectives
```

### Ordering principle

Stages are **educationally sequential**: each stage presupposes the intellectual products of earlier stages. Authors may iterate (e.g. discovering a missing dependency while designing transfer), but may not declare a later stage “complete” while an earlier stage remains undefined for the same objective cluster.

---

## 4. Stage Definitions

### 4.1 Syllabus Objective

**What it is**  
An official (or officially authorised) statement of examinable expectation — what the awarding body requires candidates to know, explain, or do within a scoped area of the syllabus.

**Authoring role**  
The **authority input**. It bounds scope and legitimacy. It does not itself supply concept anatomy, misconception catalogues, or representation sets.

**Author obligations**

- Preserve traceability from every derived learning objective back to syllabus authority  
- Resist inventing scope outside the syllabus (except clearly marked enrichment, which must not be treated as examinable core without governance)  
- Note when one syllabus objective spans multiple teachable concepts (split) or when several bullets share one concept (cluster)

**Inadequate substitutes**  
Chapter titles; “do Chapter 5”; marketing learning outcomes disconnected from official wording.

**Illustration**  
A syllabus objective requiring candidates to calculate and interpret net premiums under the equivalence principle — authority to teach present values of benefits and premiums, equivalence, and related procedures; not yet a teachable concept list.

---

### 4.2 Concepts

**What it is**  
Named teachable ideas (and, where needed, companion skills, procedures, principles, rules, and formulae) extracted from the syllabus objective’s intellectual demand. See [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) and [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md).

**Authoring role**  
Identify the **objects of understanding**. Decomposition fails if authors stop at topic labels.

**Author obligations**

- Name concepts with stable meaning and boundaries  
- Separate declarative concepts from procedural skills/procedures without collapsing them  
- Attach each concept to syllabus containers (topic/module) without equating concept with container  
- Meet minimal completeness before treating the concept as teachable

**Inadequate substitutes**  
A flat keyword list; one “concept” per syllabus bullet regardless of intellectual structure; formula names without meaning.

**Illustration**  
From the net-premium objective: concepts such as *equivalence principle*, *net premium*, *expected present value of benefits*, *expected present value of premiums* — each with core meaning and boundaries.

---

### 4.3 Dependencies

**What it is**  
Educational dependency relations among concepts (and related entities): what must be adequately in place for a later idea to be intelligible. See [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md).

**Authoring role**  
Establish **readiness structure**. Dependencies are authored before Learning Episodes that assume those foundations.

**Author obligations**

- Type dependencies (required, helpful, parallel, bridge, remediation, extension) where relevant  
- Distinguish syllabus order from educational dependency when they diverge  
- Identify entry primitives vs concepts that always need prerequisites  
- Record cross-topic dependencies explicitly

**Inadequate substitutes**  
“Do earlier chapters first” without naming prerequisite concepts; circular dependencies without resolution strategy.

**Illustration**  
*Net premium via equivalence* requires grasp of EPVs of benefits and premiums; helpful dependency may include facility with a particular commutation notation if the pathway uses it.

---

### 4.4 Misconceptions

**What it is**  
Stable incorrect mental models that systematically distort reasoning about the decomposed concepts. See [`MISCONCEPTION_AUTHORING_MODEL.md`](MISCONCEPTION_AUTHORING_MODEL.md).

**Authoring role**  
Anticipate **patterned error** so diagnosis and repair can be intentional.

**Author obligations**

- Attach every misconception to one or more concepts (and related principles/rules/formulae as needed)  
- Capture observable evidence, likely causes, and typical incorrect reasoning  
- Recommend teaching intentions and strategies for repair  
- Define what counts as evidence of repair  

**Inadequate substitutes**  
“Students find this hard”; catalogues of slips and arithmetic mistakes; free-floating confusion labels.

**Illustration**  
Misconception: equivalence means equating *undiscounted* total premiums to total benefits — ignoring present value.

---

### 4.5 Representations

**What it is**  
Legitimate modes of presenting concept structure (symbolic, verbal, visual, graphical, tabular, worked example, analogy, simulation, counterexample, etc.). See [`REPRESENTATION_MODEL.md`](REPRESENTATION_MODEL.md).

**Authoring role**  
Make concepts **intelligible and translational**. Representation choice shapes what students can see.

**Author obligations**

- Specify at least one primary representation per concept  
- Plan representation diversity where the discipline or examination demands translation across forms  
- Ensure representations support the concept — they do not replace it  
- Note when a representation is canonical vs optional enrichment  

**Inadequate substitutes**  
Decorative imagery; a single notation treated as the whole concept; representations that smuggle unstated advanced prerequisites.

**Illustration**  
Equivalence principle as verbal statement, as equation of EPVs, and as a cash-flow timeline balancing premiums and benefits.

---

### 4.6 Applications

**What it is**  
Legitimate *Application Contexts* — situation types in which concepts are used to classify, derive, compute, decide, or explain. See [`APPLICATION_AND_TRANSFER_MODEL.md`](APPLICATION_AND_TRANSFER_MODEL.md).

**Authoring role**  
Encode **authentic use** under syllabus-legitimate demand. Application follows understanding in educational sequence; authoring still designs applications once concepts exist.

**Author obligations**

- Describe context features: task demand, assumptions, constraints, typical surface forms  
- Prefer contexts that reflect professional and examination legitimacy  
- Avoid defining application only as clone drills of one template  
- Link applications to the concepts and skills they exercise  

**Inadequate substitutes**  
Random hard questions; contexts outside syllabus authority presented as core; application without conceptual anchors.

**Illustration**  
Computing a net premium for a whole-life assurance under stated mortality and interest — an application of equivalence and EPV concepts.

---

### 4.7 Transfer Opportunities

**What it is**  
Planned *Transfer Contexts*: controlled surface variation that preserves underlying conceptual demand. Includes near and far transfer within legitimate scope. See [`APPLICATION_AND_TRANSFER_MODEL.md`](APPLICATION_AND_TRANSFER_MODEL.md).

**Authoring role**  
Prepare **flexible understanding** and exam-credible command under rewording and recombination.

**Author obligations**

- Define what varies (wording, numbers, contract features, representation) and what stays constant (target structure)  
- Distinguish near transfer from far transfer and from a *new* learning objective  
- Keep transfer within syllabus-legitimate demand  
- Require multiple contexts before claiming transfer readiness as an authored aim  

**Inadequate substitutes**  
Novelty for its own sake; stacking so many new elements that the objective becomes unclear; treating every harder question as “transfer.”

**Illustration**  
Same equivalence reasoning under a deferred assurance with expenses entering a gross-premium discussion — transfer or new objective depending on whether gross premium is in scope for the current aim.

---

### 4.8 Assessment Opportunities

**What it is**  
Structured designs for eliciting evidence of capacity relative to forthcoming learning objectives — diagnostic probes, explanation prompts, classification tasks, calculation under constraint, transfer probes, etc.

**Authoring role**  
Ensure teaching aims are **evidence-amenable**. Assessment opportunities derive from learning objectives (authored in tandem at the end of decomposition); they are not a disconnected item bank.

**Author obligations**

- State what educational claim the opportunity can support (and what it cannot)  
- Prefer opportunities that distinguish understanding from recognition where the objective requires it  
- Align difficulty and form with objective grain  
- Separate diagnostic assessment opportunities from post-teaching evaluation opportunities conceptually  

**Inadequate substitutes**  
Proprietary past papers copied wholesale as “the architecture”; MCQs that only test keyword recognition for an explanation objective; assessment without a named objective.

**Illustration**  
Ask the student to explain why premiums and benefits are equated in present value, then classify three worded contracts as net-premium or not — evidence toward conceptual and classificatory aims.

---

### 4.9 Learning Objectives

**What it is**  
Precise statements of what the student should be able to know, explain, or do with respect to the decomposed knowledge entities. Educational aims — not containers, not exam items, not topic completion criteria.

**Authoring role**  
Synthesise the decomposition into **teachable, diagnosable, evaluable aims**. Learning Objectives appear last because they must be informed by concepts, dependencies, misconceptions, representations, applications, transfer, and assessment design — otherwise they become vague slogans.

**Author obligations**

- Ground every objective in syllabus authority and named concepts  
- Make objectives precise enough to guide Teaching Intention and episode purpose  
- Ensure assessment opportunities can speak to the objective  
- Avoid objectives that smuggle multiple unrelated purposes (episode atomicity will forbid bundling later)  

**Inadequate substitutes**  
“Understand Chapter 4”; “Be ready for the exam”; objectives that name only a formula without conceptual conditions.

**Illustration**  
“Explain the equivalence principle in present-value terms and compute a net premium for a standard whole-life assurance under stated assumptions” — may be split into separate objectives if episode atomicity requires one purpose per episode.

---

## 5. Stage Dependencies (Summary Table)

| Stage | Requires earlier | Enables later |
|-------|------------------|---------------|
| Syllabus Objective | Authorised curriculum | All stages |
| Concepts | Syllabus Objective | Dependencies, misconceptions, representations, … |
| Dependencies | Concepts | Lawful episode sequencing, readiness claims |
| Misconceptions | Concepts (+ often dependencies) | Repair intentions, diagnostic assessment |
| Representations | Concepts | Teaching intelligibility, multi-rep transfer |
| Applications | Concepts (+ typically dependencies) | Competence aims, near practice |
| Transfer Opportunities | Applications + concepts | Flexible understanding / mastery evidence design |
| Assessment Opportunities | Draft aims + concepts | Evidence collection design |
| Learning Objectives | Full prior decomposition (at least minimal) | Strategies, episodes, Twin targets |

---

## 6. Iteration and Feedback

Decomposition is allowed to iterate:

- Episode design may reveal missing dependencies or misconceptions  
- Assessment trials may show that an objective is too coarse  
- Transfer design may force boundary clarification between concepts  

Iteration updates authored knowledge. It does not excuse teaching against undefined concepts or objectives.

---

## 7. Relationship to Concept Architecture Facets

Concept Architecture defines the **anatomy of one concept**. Concept Decomposition defines the **pipeline from syllabus objective to a set of concepts and supporting artefacts**.

| Concern | Document |
|---------|----------|
| One concept’s facets (meaning, boundaries, …) | Concept Architecture |
| From syllabus objective through the authoring stages | This document |
| Binding authoring rules | Authoring Invariants |

---

## 8. Non-Goals

This model does not:

- Provide a checklist for a specific paper  
- Automate decomposition  
- Define storage or Studio workflow screens  
- Replace Knowledge Dependency Model typing detail  

---

## 9. Summary

Concept Decomposition is the ordered educational analysis that turns syllabus objectives into teachable concepts with dependencies, misconceptions, representations, applications, transfer opportunities, assessment opportunities, and precise learning objectives — so the Educational Operating Model has something lawful to teach.
