# Subject Knowledge Model

**Document ID:** V2-SKA-001  
**Classification:** Educational Architecture — Subject Knowledge Foundation  
**Status:** Authoritative model of teachable knowledge structure  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Audience:** Product, educational governance, architecture, curriculum designers, future implementers  

**Authority relationships**

| Document | Relationship |
|----------|--------------|
| [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md) | Parent vocabulary; this model specialises *what is taught* |
| [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) | Deepens the teachable structure of a *Concept* |
| [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md) | Educational dependency among knowledge entities |
| [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md) | How concepts relate as a navigable network |
| [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md) | Binding rules for subject knowledge representation |
| [`SUBJECT_AUTHORING_MODEL.md`](SUBJECT_AUTHORING_MODEL.md) | How experts populate this model from a syllabus (authoring architecture) |
| [`CURRICULUM_MODEL.md`](../CURRICULUM_MODEL.md) | Syllabus packaging hierarchy (Subject → Chapter → Topic); distinct from knowledge kinds |
| [`LEARNING_MODEL.md`](LEARNING_MODEL.md) · [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md) | What learning and understanding *mean*; this model names *what is known* |

---

## 1. Purpose

This document defines the **Subject Knowledge Model (SKM)** for Kwalitec Version 2: the conceptual architecture for representing teachable knowledge in *any* discipline.

It answers:

> **What is the structure of teachable knowledge?**

The SKM is intentionally independent of any specific examination subject (including any particular IFoA paper). Actuarial illustrations appear only as examples. The same entities apply to statistics, finance, mathematics, or any other structured professional domain Kwalitec may later serve.

This is **not** implementation, database design, curriculum authoring, content production, or AI prompting. It is educational architecture.

---

## 2. Governing Distinctions

Three distinctions must remain sharp:

| Distinction | Meaning |
|-------------|---------|
| **Knowledge kind vs syllabus container** | A *Concept* or *Skill* is a kind of knowledge. A *Topic*, *Module*, or *Syllabus* is a packaging / authority container. Containers organise; they do not replace kinds. |
| **Declarative vs procedural** | Knowing *what* and *why* differs from knowing *how*. Both are teachable; neither substitutes for the other. |
| **Official syllabus order vs educational dependency** | Syllabus chapters may list material in a convenient order. Educational dependency states what a learner must grasp for a later idea to be intelligible. They often coincide; they are not identical. |

### Governing sentence

> Subject knowledge is a structured network of teachable entities — concepts, skills, procedures, principles, and supporting artefacts — organised under syllabus authority and linked by educational dependency.  
> A syllabus lists what must be examined.  
> Subject knowledge describes what must be understood.

---

## 3. Entity Catalogue

Each entity below is defined with:

- **Definition** — precise meaning inside Kwalitec  
- **Educational purpose** — why the entity exists in teaching  
- **Relationships** — how it connects to other SKM entities  
- **Examples** — discipline-portable illustrations (often actuarial for concreteness)  
- **Non-examples** — what must not be confused with the entity  

---

### 3.1 Concept

**Definition**  
A Concept is a named, teachable idea with stable meaning, boundaries, and relations to other ideas. It answers *what this is* and *how it fits* in the subject’s conceptual structure.

**Educational purpose**  
To give teaching a primary object of understanding — something that can be explained, contrasted, applied, and transferred — rather than only steps or labels.

**Relationships**  
Concepts have *Prerequisites* and participate in *Dependencies*. They are clarified by *Definitions*, *Examples*, *Counterexamples*, *Analogies*, and *Representations*. They may be governed by *Principles* and *Rules*, expressed by *Formulae*, and targeted by *Learning Objectives*. *Misconceptions* attach to concepts. Concepts live inside *Topics* / *Modules* under a *Syllabus* but are not identical to those containers. See [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md).

**Examples**  
Force of mortality; present value; equivalence principle; exponential family; Bayesian prior.

**Non-examples**  
A chapter title; a memorised formula without meaning; a single exam question; a UI screen labelled “concept.”

---

### 3.2 Skill

**Definition**  
A Skill is a durable capacity to perform a class of legitimate subject tasks with appropriate accuracy, judgement, and (where relevant) efficiency. Skills integrate conceptual grasp with action.

**Educational purpose**  
To name what the student can *do* with knowledge under realistic demand — not only what they can recite.

**Relationships**  
Skills typically rest on one or more *Concepts* and often employ *Procedures*. They are assessed relative to *Learning Objectives* and practised in *Application Contexts*. Fluency without concept yields brittle skill; concept without skill yields incomplete examination readiness.

**Examples**  
Computing an expected present value under stated assumptions; classifying a GLM response distribution from problem features; constructing a cash-flow timeline from a worded assurance.

**Non-examples**  
A single lucky correct answer; clicking through a worked video; “being good at maths” as an undifferentiated trait.

---

### 3.3 Procedure

**Definition**  
A Procedure is an ordered method for accomplishing a legitimate task: a sequence of steps with conditions of applicability and stopping criteria.

**Educational purpose**  
To make executable methods teachable, scaffoldable, and diagnosable — while requiring conceptual grounding so steps are not empty ritual.

**Relationships**  
Procedures implement *Skills* and rest on *Concepts*, *Principles*, and often *Formulae*. They require *Rules* (when to apply / when not). *Examples* demonstrate procedures; *Counterexamples* show misuse. Procedures without conceptual grounding violate subject invariants.

**Examples**  
Prospective reserve calculation sequence; Newton–Raphson root finding for an equation of value; constructing a select life table excerpt for a probability query.

**Non-examples**  
An unexplained answer key; a formula written without steps; “just follow the template” with no conditions of use.

---

### 3.4 Principle

**Definition**  
A Principle is a governing idea that justifies methods and constrains legitimate reasoning across many situations (the deep *why* behind families of techniques).

**Educational purpose**  
To provide explanatory power that survives surface variation — the intellectual spine of transfer.

**Relationships**  
Principles ground *Procedures* and *Rules*. They connect multiple *Concepts*. *Learning Objectives* often require students to invoke principles, not only execute steps. Misapplications of principles generate characteristic *Misconceptions*.

**Examples**  
Equivalence of present values of premiums and benefits; law of large numbers as justification for risk pooling intuition; likelihood as the bridge from model to data in estimation.

**Non-examples**  
A local mnemonic; a syllabus bullet; a numerical constant; a house style for writing answers.

---

### 3.5 Rule

**Definition**  
A Rule is a conditional prescription: under stated conditions, a particular action, classification, or inference is required, permitted, or forbidden.

**Educational purpose**  
To make conditions of validity explicit — especially where novices apply methods indiscriminately.

**Relationships**  
Rules specialise *Principles* into actionable constraints. They govern *Procedures* and interpretation of *Formulae*. Rules appear in *Definitions* of scope and in *Application Contexts*. Violating a rule while “getting the number” is not competence.

**Examples**  
“If payments are continuous and force of interest is constant, use the continuous annuity formulae”; “do not interchange select and ultimate probabilities without adjusting the age/duration basis.”

**Non-examples**  
Vague advice (“be careful with timing”); a preference for one textbook’s notation; an exam rubric mark scheme item alone.

---

### 3.6 Formula

**Definition**  
A Formula is a symbolic expression that compactly represents a relationship among quantities under stated assumptions.

**Educational purpose**  
To support precise calculation and communication — always subordinate to interpretation: what the symbols mean, when the expression is valid, and what quantity it returns.

**Relationships**  
Formulae *represent* *Concepts* and *Principles*. They appear inside *Procedures*. They require *Definitions* of symbols and *Rules* of applicability. A formula without interpretation is incomplete knowledge.

**Examples**  
\(\bar{A}_x = \int_0^\infty e^{-\delta t}\,{_t}p_x\,\mu_{x+t}\,dt\); logit link \(g(\mu)=\log(\mu/(1-\mu))\).

**Non-examples**  
A formula memorised with no symbol meanings; a spreadsheet cell reference; an unexplained numeric result.

---

### 3.7 Definition

**Definition**  
A Definition is an authoritative statement that fixes the meaning of a term or symbol within the subject’s language.

**Educational purpose**  
To stabilise vocabulary so teaching, diagnosis, and assessment refer to the same objects. Definitions enable precision; they do not by themselves constitute understanding.

**Relationships**  
Definitions introduce or clarify *Concepts*. They constrain *Formulae* (symbol meanings) and *Rules* (scope language). Definitions are necessary inputs to teaching; mastery requires more than restating them.

**Examples**  
“The force of mortality \(\mu_x\) is the instantaneous rate of mortality at age \(x\)”; “a prior distribution represents beliefs about parameters before observing data.”

**Non-examples**  
A lengthy textbook chapter; a student’s paraphrase that alters meaning; equating “I can recite the definition” with understanding.

---

### 3.8 Example

**Definition**  
An Example is a concrete instance that illustrates a concept, principle, rule, procedure, or formula in a clear case where the idea applies.

**Educational purpose**  
To make abstract structure perceptible and to provide initial models for imitation that teaching can later fade.

**Relationships**  
Examples instantiate *Concepts*, *Procedures*, and *Rules*. They live inside *Application Contexts*. Over-reliance on a narrow example set produces illusion of mastery. Examples pair with *Counterexamples* for boundary teaching.

**Examples**  
A fully worked whole-life assurance EPV at constant force; a simple Poisson GLM with canonical link; a cash-flow diagram for an annuity-due.

**Non-examples**  
An exam question used only as a score event with no instructional role; a counterexample mislabelled as a supporting example; an analogy presented as a literal case.

---

### 3.9 Counterexample

**Definition**  
A Counterexample is a concrete instance that shows where a concept, rule, or method does *not* apply, or that falsifies a tempting but false generalisation.

**Educational purpose**  
To teach boundaries and defeat overgeneralisation — a primary tool against misconceptions.

**Relationships**  
Counterexamples sharpen *Concept* boundaries and *Rules*. They are central to repairing *Misconceptions*. They contrast with *Examples* and support *Transfer* preparation.

**Examples**  
Showing that a discrete annuity formula fails under continuous payment without adjustment; a dataset where a linear probability model produces impossible fitted probabilities.

**Non-examples**  
A random hard question; an error caused only by arithmetic slip; “any wrong answer.”

---

### 3.10 Analogy

**Definition**  
An Analogy is a structured comparison that maps relations from a familiar domain onto a target concept to support initial understanding — while remaining explicitly non-identical to the target.

**Educational purpose**  
To bootstrap intuition when formal structure is dense, then to be retired or qualified so students do not treat the analogy as the theory.

**Relationships**  
Analogies support early grasp of *Concepts* and *Principles*. They must be bounded by *Definitions* and *Counterexamples* lest they become misconceptions. Analogies are teaching aids, not syllabus objects of equal standing with concepts.

**Examples**  
Force of interest as a continuous compounding “speed”; likelihood as a measure of how well a parameter “explains” the observed sample (carefully qualified).

**Non-examples**  
A joke; a metaphor that contradicts the formal definition; replacing the formal model permanently with the analogy.

---

### 3.11 Representation

**Definition**  
A Representation is a mode of presenting subject structure — symbolic, graphical, tabular, verbal, or diagrammatic — that makes relationships inspectable.

**Educational purpose**  
To allow students to see structure that prose alone may hide, and to require translation across representations as evidence of understanding.

**Relationships**  
Representations express *Concepts*, *Procedures*, and *Formulae*. Multiple representations of the same concept strengthen *Connection*. Inability to move between representations is a diagnostic signal of shallow grasp.

**Examples**  
Cash-flow timeline; life table; survival curve plot; directed graph of model dependencies; verbal protocol of a derivation.

**Non-examples**  
Decorative imagery with no information content; a single representation treated as the only legitimate form of knowledge.

---

### 3.12 Learning Objective

**Definition**  
A Learning Objective is a precise statement of what the student should be able to know, explain, or do with respect to one or more knowledge entities. It is an educational aim, not a container and not an exam item.

**Educational purpose**  
To give teaching, diagnosis, and evidence a clear target at teachable grain.

**Relationships**  
Objectives target *Concepts*, *Skills*, *Procedures*, and often *Principles*. They sit under *Topics* / *Modules* within a *Syllabus*. Episodes and strategies aim at objectives (see Educational Domain Model). Objectives imply *Prerequisites* via the entities they involve.

**Examples**  
“Explain select versus ultimate mortality and compute a survival probability from a select table”; “state the equivalence principle and use it to derive a net premium under given assumptions.”

**Non-examples**  
“Chapter 4”; “do past papers”; “get better at CT5”; a single MCQ stem used as if it were the objective itself.

---

### 3.13 Topic

**Definition**  
A Topic is a syllabus-facing unit that groups related knowledge entities for organisation, navigation, and examination mapping. It is a **container**, not a knowledge kind.

**Educational purpose**  
To align teaching with how official syllabuses and study materials partition content, without mistaking the partition for understanding.

**Relationships**  
Topics contain or reference *Concepts*, *Skills*, *Procedures*, *Learning Objectives*, and supporting artefacts. Topics belong to *Modules* (or chapters) under a *Syllabus*. Educational *Dependencies* may cross topic boundaries. Completing a topic is coverage, not mastery.

**Examples**  
“Life contingencies — annuities”; “GLM — estimation and inference”; “interest theory — force of interest.”

**Non-examples**  
A concept itself; a single formula; “I finished the topic” as proof of competence.

---

### 3.14 Module

**Definition**  
A Module is a larger organisational grouping of related *Topics* (often corresponding to a syllabus chapter, part, or major section).

**Educational purpose**  
To support coherent progression and roll-up of study structure at a scale larger than a single topic.

**Relationships**  
Modules nest *Topics* under a *Syllabus*. Cross-module *Dependencies* are common and educationally important. Modules inherit syllabus authority; they do not invent educational kinds.

**Examples**  
A syllabus Part on survival models; a course unit on statistical modelling; a chapter cluster on reserves.

**Non-examples**  
A Learning Episode; a Study Plan calendar block; a product feature named “module” without syllabus grounding.

---

### 3.15 Syllabus

**Definition**  
A Syllabus is the authoritative statement of what a qualification body (or equivalent curriculum authority) requires candidates to know and be able to do for a named offering and edition.

**Educational purpose**  
To ground all subject knowledge work in external legitimacy: Kwalitec teaches toward official aims, not toward a private parallel curriculum.

**Relationships**  
The syllabus authorises *Modules*, *Topics*, and implied *Learning Objectives*. Subject knowledge entities must be mappable to syllabus scope. Syllabus *order* is not identical to educational *Dependency* order.

**Examples**  
An IFoA subject syllabus for a given year; a university course specification; a professional body’s learning outcomes document.

**Non-examples**  
A textbook table of contents alone (unless adopted as authority); a tutor’s preferred teaching sequence; a product roadmap.

---

### 3.16 Dependency

**Definition**  
A Dependency is an educational relationship stating that competent engagement with one knowledge entity requires, is helped by, or is shaped by another. Dependencies are about learnability and intelligibility, not merely about document order.

**Educational purpose**  
To prevent teaching that asks students to build on absences — the structural cause of shallow mimicry and false confidence.

**Relationships**  
Dependencies link *Concepts*, *Skills*, *Procedures*, and *Learning Objectives*. They specialise into types (required, helpful, parallel, extension, remediation, bridge) in [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md). *Prerequisite* is the everyday name for a required (or strongly expected) dependency source.

**Examples**  
Understanding present value before pricing assurances; knowing discrete distributions before GLMs for count data.

**Non-examples**  
“Chapter 3 comes before Chapter 4 in the PDF”; a marketing content calendar; arbitrary UI navigation order.

---

### 3.17 Prerequisite

**Definition**  
A Prerequisite is a knowledge entity (or coherent set) that must be adequately in place — at a stated level — before another entity can be taught or assessed honestly as the primary aim.

**Educational purpose**  
To make readiness conditions explicit for teaching moves and for diagnosing “failure” that is actually missing foundation.

**Relationships**  
Prerequisite is the learner-facing / teaching-facing face of a *required* (or sometimes *helpful*) *Dependency*. Prerequisites attach to *Concepts*, *Skills*, *Procedures*, and *Learning Objectives*. Missing prerequisites change lawful teaching intention (foundation repair before advanced aims).

**Examples**  
Basic probability before Bayes’ theorem applications; equation of value before internal rate of return interpretations.

**Non-examples**  
Having purchased a study guide; having marked a prior topic complete; chronological age or “years of experience” alone.

---

### 3.18 Misconception

**Definition**  
A Misconception is a stable, incorrect mental model that systematically produces wrong reasoning or wrong answers. It is not a slip, a gap of pure ignorance, or a one-off arithmetic error.

**Educational purpose**  
To name patterned wrong structure so teaching can confront it explicitly rather than burying it under more undifferentiated practice.

**Relationships**  
Every misconception belongs to one or more *Concepts* (and often to misapplied *Principles*, *Rules*, or *Formulae*). Misconceptions are diagnosed from *Evidence* and repaired with contrast (*Examples* / *Counterexamples*). Unresolved misconceptions block mastery and transfer.

**Examples**  
Treating select and ultimate mortality as interchangeable; believing continuous and discrete payment models differ only by a cosmetic notation change; interpreting \(p\)-values as the probability that the null is true.

**Non-examples**  
A single calculation slip; never having seen a topic; low confidence without a wrong model.

---

### 3.19 Application Context

**Definition**  
An Application Context is a situation type in which knowledge is legitimately used — characterised by task demands, assumptions, constraints, and typical surface forms.

**Educational purpose**  
To situate practice and assessment so students learn *when* and *how* knowledge is used, not only abstract statements.

**Relationships**  
Application contexts host *Examples*, *Procedures*, and *Skills*. They map to *Learning Objectives*. Narrow contexts produce clone competence; varied contexts prepare transfer. Contexts remain within syllabus-legitimate demand.

**Examples**  
Pricing a term assurance from a worded contract; fitting a GLM to count claims data; solving an equation of value for an unknown interest rate under exam time pressure.

**Non-examples**  
A context outside syllabus scope presented as core; a decorative story with no structural demand; pure recall of a definition with no use situation.

---

### 3.20 Transfer Context

**Definition**  
A Transfer Context is an application situation that differs in surface features from those practised, while remaining within legitimate subject demand — requiring the student to recognise underlying structure.

**Educational purpose**  
To probe and develop flexible competence; to expose misconceptions and clone-bound procedures.

**Relationships**  
Transfer contexts relate to *Application Contexts* by controlled variation. They evidence the Transfer dimension of learning. They often recombine *Concepts* across *Topics*. Success in transfer contexts is strong evidence toward mastery; failure after clone success is a diagnostic signal.

**Examples**  
An annuity problem reworded with altered payment timing; a reserve question that mixes prospective reasoning with an expense twist not present in drill sets; a modelling task with a non-canonical but valid link function choice.

**Non-examples**  
Tricks outside the syllabus; unfair ambiguity; variation so extreme it assesses a different objective unnoticed.

---

## 4. Entity Map (Conceptual)

```text
Syllabus
  └── Module
        └── Topic
              ├── Learning Objective(s)
              │     └── target → Concept / Skill / Procedure / Principle
              ├── Concept
              │     ├── Definition, Representation, Analogy
              │     ├── Example / Counterexample
              │     ├── Formula, Rule, Principle (related)
              │     ├── Misconception(s)
              │     └── Dependency / Prerequisite → other entities
              ├── Skill
              │     └── uses Procedure + Concept
              └── Procedure
                    └── grounded by Concept / Principle / Rule / Formula

Application Context  →  practice & assessment situations
Transfer Context      →  varied legitimate situations
```

Containers (*Syllabus*, *Module*, *Topic*) organise.  
Knowledge kinds (*Concept*, *Skill*, *Procedure*, *Principle*, …) constitute what is taught.  
Artefacts (*Definition*, *Example*, *Formula*, …) support teaching and evidence.  
Relations (*Dependency*, *Prerequisite*) govern learnable order.

---

## 5. What This Model Deliberately Excludes

| Excluded | Why |
|----------|-----|
| Database schemas / ORM entities | Implementation concern |
| JSON curriculum file formats | Engine/runtime concern |
| Lesson plans and UI flows | Presentation concern |
| Prompt templates for generative AI | Not educational architecture |
| Copyrighted syllabus prose reproduction | Legal / content concern |
| Scoring algorithms and mastery formulae | Twin / assessment engineering |

---

## 6. Relationship to Other Architectures

| Architecture | Question it answers | Relation to SKM |
|--------------|---------------------|-----------------|
| Educational Domain Model | What are learning, teaching, tutor, evidence? | SKM supplies *objects* those processes act upon |
| Learning Episode Architecture | What is one teaching unit? | Episodes target SKM entities via objectives |
| Curriculum Model / Graph | How is official structure packaged and sequenced? | Packaging ≠ knowledge kinds; graph may encode dependencies |
| Teaching Strategy Architecture | *How* to teach a diagnosed need? | Strategies operate on SKM entities |
| Student Digital Twin | What is believed about the learner? | Twin estimates state *with respect to* SKM entities |

---

## 7. Architectural Ambiguities (Recorded)

The following ambiguities are acknowledged for governance; they are not resolved by implementation speculation:

1. **Grain of Concept vs Topic** — Official syllabuses sometimes name “topics” that are themselves concept-sized, and sometimes concept clusters. Mapping must be explicit per curriculum edition.
2. **Skill vs Procedure** — Some professional tasks blur capacity and method. Prefer: *Skill* = durable capacity class; *Procedure* = particular method family.
3. **Principle vs Rule** — Principles justify; rules prescribe under conditions. Borderline maxims should be classified by whether they generalise across methods or constrain a method.
4. **Analogy status** — Analogies are first-class teaching artefacts but second-class syllabus objects; they must not displace formal definitions in authority.
5. **Transfer Context threshold** — How much surface variation counts as “transfer” vs “new objective” is a design judgement guided by the Learning Objective, not by a universal metric in this document.

---

## 8. Related Documents

- [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md)  
- [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md)  
- [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md)  
- [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md)  
- [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  
- [`EDUCATIONAL_GLOSSARY.md`](EDUCATIONAL_GLOSSARY.md)  
- [`../CURRICULUM_MODEL.md`](../CURRICULUM_MODEL.md)  
