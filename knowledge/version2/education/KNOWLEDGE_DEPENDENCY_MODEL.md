# Knowledge Dependency Model

**Document ID:** V2-SKA-003  
**Classification:** Educational Architecture — Subject Knowledge Foundation  
**Status:** Authoritative model of educational dependency  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  

**Related:** [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md) · [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md) · [`../CURRICULUM_GRAPH.md`](../CURRICULUM_GRAPH.md) · [`../CURRICULUM_MODEL.md`](../CURRICULUM_MODEL.md)

---

## 1. Purpose

This document defines **educational dependency** for Kwalitec Version 2.

It answers:

> **What must already be graspable for new knowledge to be honestly teachable?**

Dependencies govern learnability. They are not identical to syllabus chapter order, study-plan calendars, or product navigation sequences — though good curriculum design often aligns those with dependency.

---

## 2. Definition

**Educational dependency:** a directed educational relationship from a *source* knowledge entity to a *target* knowledge entity stating that competent engagement with the target is constrained by the state of the source.

In plain language: the target leans on the source.

Dependencies may hold between concepts, skills, procedures, principles, learning objectives, or coherent sets thereof. The Knowledge Dependency Model classifies *kinds* of dependency; the Concept Network Model describes a broader set of conceptual relations (of which dependency is one family).

### Governing sentence

> Dependencies are educational, not merely syllabus order.  
> Syllabus order is a publishing and examination convenience.  
> Dependency is a claim about intelligibility and honest assessment.

---

## 3. Why Dependency Matters

1. **Intelligibility** — Without required foundations, explanations become empty words and formulae become rituals.  
2. **Honest diagnosis** — Failure on an advanced aim may be missing prerequisite, not weakness on the named target.  
3. **Teaching economy** — Repairing foundations once prevents repeated shallow remediations downstream.  
4. **Transfer** — Combination questions assume multiple nodes are jointly available; hidden dependency gaps collapse transfer.  
5. **False confidence** — Coverage of later chapters without dependency readiness produces candidates who “have seen everything” and understand little.  
6. **Tutor legitimacy** — A tutor that advances past absences behaves as a content broadcaster, not as a tutor.

---

## 4. Dependency Types

### 4.1 Required Prerequisite

**Definition**  
The source must be adequately established before the target can be taught or assessed as the primary aim. Without the source, the target is not intelligibly learnable at the intended grain.

**Educational force**  
Strongest. Violating it is educationally unlawful for primary-aim teaching.

**Example**  
Present-value reasoning is a required prerequisite for net premium via equivalence.

**Non-example**  
Preferring one textbook’s chapter order when an alternative order preserves foundations.

---

### 4.2 Helpful Prerequisite

**Definition**  
The source substantially eases learning of the target and improves quality of grasp, but a carefully designed path can introduce the target with extra scaffolding if the source is weak — at cost and risk.

**Educational force**  
Advisory but serious. Ignoring helpful prerequisites increases load and misconception risk.

**Example**  
Comfort with discrete probability mass functions is highly helpful before introducing probability generating functions; emergency scaffolding is possible but slower.

**Non-example**  
Optional enrichment reading with no effect on core intelligibility.

---

### 4.3 Parallel Knowledge

**Definition**  
Two (or more) entities do not depend on each other for basic intelligibility; they may be learned in either order or interleaved, though later combination objectives will require both.

**Educational force**  
Permissive on order; still demanding on eventual joint command.

**Example**  
Elementary force of interest and elementary life-table look-ups may be parallel early on; contingent present values later require both.

**Non-example**  
Labelling as “parallel” two ideas where one silently assumes the other.

---

### 4.4 Extension Knowledge

**Definition**  
The source is the core; the target deepens, generalises, or elaborates it. The extension should not be taught as if it were the core, and the core should not be assessed only through the extension.

**Educational force**  
Order: core before extension. Assessment: distinguish core competence from extension competence.

**Example**  
Net premium as core; gross premium with expenses as extension. Constant force models before select-period refinements in some pathways.

**Non-example**  
Treating an advanced special case as the only way the core is ever taught.

---

### 4.5 Remediation Dependency

**Definition**  
When evidence shows a stable deficit or misconception on a source entity, lawful progress on a dependent target requires remediation of the source (or an explicit, temporary narrowing of the target aim).

**Educational force**  
Conditional and evidence-triggered. It is not a permanent edge in a static syllabus graph alone; it is activated by learner state.

**Example**  
Persistent confusion of annuity-due vs immediate creates a remediation dependency before further contingent annuity pricing aims.

**Non-example**  
Repeating an entire module because of one slip; blocking all progress for unrelated weak topics.

---

### 4.6 Bridge Concept

**Definition**  
A concept (or small set) whose educational role is to connect two regions of the network that students otherwise experience as disconnected — enabling a later target that depends on the joining.

**Educational force**  
Strategic. Omitting the bridge forces students to jump a structural gap.

**Example**  
Equation of value as a bridge between interest-theory cash flows and contingent payment pricing; likelihood as a bridge between probability models and estimation.

**Non-example**  
A mnemonic; a motivational pep talk; a purely historical anecdote with no structural joining role.

---

## 5. Dependency vs Syllabus Order

| | Syllabus order | Educational dependency |
|--|----------------|------------------------|
| **Authority** | Examination body / curriculum publication | Learnability and honest teaching |
| **Question answered** | In what sequence is material listed / examined as parts? | What must be graspable for the next idea to make sense? |
| **May they differ?** | Yes | — |
| **When aligned** | Good instructional design often follows dependency | Ideal when official structure permits |
| **When they diverge** | Teaching may lawfully reorder within syllabus scope to respect dependency | Dependency still binds teaching honesty |
| **Completion language** | “Finished Chapter 3” | “Required prerequisites for Concept B are evidenced” |

### Worked contrast

A syllabus may place a computational technique early because it is examinable and self-contained as a drill, while a deep principle that *explains* the technique appears later. Educationally, early drills without the principle produce procedural fluency at risk of brittleness; the dependency model still requires eventual conceptual grounding and may require conceptual insertion before advanced transfer aims — even if the PDF listed drills first.

---

## 6. Educational Consequences of Violating Dependencies

### 6.1 Violating required prerequisites

| Consequence | Manifestation |
|-------------|---------------|
| Ritual procedure | Students execute steps they cannot justify |
| Illusion of progress | Correct clone answers with zero transfer |
| Misdiagnosis | System or tutor treats foundation gaps as target-concept failure |
| Misconception entrenchment | Wrong models fill explanatory voids |
| Motivation damage | Students conclude they are “bad at the subject” when the path was unintelligible |
| Wasted later study | Advanced practice rehearses emptiness |

### 6.2 Ignoring helpful prerequisites

Higher cognitive load, slower acquisition, thinner connections, greater need for scaffolding, elevated misconception risk — still possibly recoverable with excellent teaching, but inefficient and fragile.

### 6.3 Treating parallel knowledge as strictly ordered

Artificial bottlenecks, delayed exposure to motivating applications, and false inferences that early struggles imply permanent incapacity in a later “dependent” topic that was never truly dependent.

### 6.4 Teaching extensions as cores

Students master ornaments and fail basics; assessment becomes unfair; remediation becomes confused about what to repair.

### 6.5 Ignoring remediation dependencies

Practice on dependent targets *strengthens* the wrong or missing foundation; volume becomes harmful.

### 6.6 Omitting bridge concepts

Fragmented knowledge: students can perform in islands but fail combination and “explain why” demands — exactly what professional examinations punish.

---

## 7. Dependency Strength and Adequacy

Dependency claims should state:

1. **Type** — required, helpful, parallel, extension, remediation, bridge  
2. **Source and target** — named knowledge entities  
3. **Adequacy level** — what “enough” means for the source (recognition vs explanation vs application), because full mastery of all prerequisites is not always required for an introductory pass at the target  
4. **Evidence trigger** (for remediation) — what pattern activates the dependency  

**Adequacy principle:** Required prerequisites demand *sufficient* prior grasp for the target’s grain — not necessarily lifelong mastery of the entire prior module.

---

## 8. Tutor Reasoning with Dependencies

When selecting a next educational aim, the tutor asks:

1. What are the **required** prerequisites of this aim?  
2. Is there **evidence** they are adequately in place?  
3. If not, is the lawful move **remediation / foundation teaching**, not advanced assessment?  
4. Are there **helpful** prerequisites worth strengthening first given time scarcity?  
5. Is a **bridge concept** missing between regions the student must combine?  
6. Am I about to teach an **extension** as if it were the core?

These questions precede strategy selection. Strategy cannot repair an unlawful aim.

---

## 9. Relationship to Curriculum Graph

The Version 2 Curriculum Graph may encode sequencing and structural edges for computation. Educationally:

- Graph edges that merely reflect PDF order are **not** automatically educational dependencies.  
- Educational dependencies may be represented as typed edges (or equivalent metadata) when implementation exists.  
- Until then, this document remains the normative meaning of dependency — technology-independent.

Implementation must not collapse all edge types into a single “comes before” relation.

---

## 10. Architectural Ambiguities (Recorded)

1. **Partial ordering** — Real subjects are rarely a single total order; multiple lawful topological sorts may exist.  
2. **Mutual reinforcement** — Some pairs strengthen each other without a strict required direction; classify carefully (often parallel + later joint objective).  
3. **Population dependence** — Helpful vs required can shift with prior education of the candidate population.  
4. **Objective grain** — An advanced objective may require a prerequisite that an introductory objective on the “same topic” does not. Dependencies attach to aims and entities, not only to topic titles.  
5. **Remediation scope** — How much of a foundation to reopen is a priority/ROI judgement (Priority Model / Adaptive Decision elsewhere), constrained by this model’s types.

---

## 11. Related Documents

- [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  
- [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md)  
- [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md)  
- [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md)  
- [`../CURRICULUM_GRAPH.md`](../CURRICULUM_GRAPH.md)  
- [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md)  
