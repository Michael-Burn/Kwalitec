# Teaching Strategy Architecture

**Document ID:** V2-TSA-001  
**Classification:** Educational Architecture — Teaching Strategy Foundation  
**Status:** Authoritative architectural definition  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Audience:** Product, educational governance, architecture, future implementers  

**Authority relationships**

| Document | Relationship |
|----------|--------------|
| [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md) | Parent vocabulary; this document specialises *Teaching Strategy* |
| [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md) | Locates strategy in the permanent tutor reasoning chain |
| [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md) | Intention answers *what change*; strategy answers *how* |
| [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) | Diagnosis constrains lawful strategy classes |
| [`EDUCATIONAL_HYPOTHESIS_MODEL.md`](EDUCATIONAL_HYPOTHESIS_MODEL.md) | Hypothesis informs which instructional approach will test or repair |
| [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md) | Episodes realise strategy under intention |
| [`TEACHING_STRATEGY_CATALOGUE.md`](TEACHING_STRATEGY_CATALOGUE.md) | Named instructional strategies |
| [`INSTRUCTIONAL_PRINCIPLES.md`](INSTRUCTIONAL_PRINCIPLES.md) | Principles governing selection |
| [`STRATEGY_SELECTION_MODEL.md`](STRATEGY_SELECTION_MODEL.md) | Qualitative selection rules |
| [`STRATEGY_COMPOSITION_MODEL.md`](STRATEGY_COMPOSITION_MODEL.md) | How strategies combine across episodes |
| [`STRATEGY_INVARIANTS.md`](STRATEGY_INVARIANTS.md) | Binding strategy rules |

---

## 1. Purpose

This document defines **Teaching Strategy** for Kwalitec Version 2.

Teaching Strategy is the educational reasoning artefact that transforms a Teaching Intention into one or more Learning Episodes. It sits after Educational Diagnosis, Educational Hypothesis, and Teaching Intention, and before episode enactment.

This architecture answers:

> *HOW does the tutor intend to produce the desired educational change?*

It does **not** answer *what is wrong* (diagnosis), *why it is likely so* (hypothesis), or *what improvement to seek* (intention). Those precede strategy.

This is educational architecture only. It is not implementation, AI prompting, UI design, lesson planning, or content authoring.

---

## 2. Definition

**Teaching Strategy:** a named instructional approach — an educational reasoning commitment — that specifies *how* the tutor will pursue a Teaching Intention through one or more Learning Episodes, chosen because it fits the diagnosed educational problem, the working hypothesis, the student’s current understanding, and the learning objective.

A Teaching Strategy governs **instructional decisions**. It does not prescribe screens, prompts, message templates, database rows, or delivery media.

### Governing sentence

> A Teaching Strategy specifies HOW a tutor intends to produce the desired educational change.  
> It does not specify implementation.  
> It does not prescribe screens or prompts.  
> It governs instructional decisions.

### What a Teaching Strategy is not

| Not this | Why |
|----------|-----|
| An AI prompt or LLM template | Language may deliver teaching; a prompt is not instructional reasoning |
| A UI workflow or screen flow | Presentation realises strategy; it is not strategy |
| A lesson plan or timetable block | Plans may schedule episodes; strategy is the pedagogical approach |
| A question set or item bank slice | Materials realise strategy; they are not the strategy |
| A database entity or API contract | Persistence and interfaces are implementation |
| A Teaching Intention | Intention is *what change*; strategy is *how* |
| An Educational Diagnosis | Diagnosis names the problem; strategy does not rename it |
| Mastery theatre | Strategy never declares mastery as its outcome |

---

## 3. Educational Purpose

The educational purpose of Teaching Strategies is to make tutoring **methodologically accountable**.

Without named strategies:

- “teach more” remains vague and unfalsifiable;
- every deficit collapses into undifferentiated practice;
- evidence cannot be attributed to a deliberate instructional approach;
- adaptation becomes thrash rather than reasoned revision.

With named strategies:

- every instructional move answers *which approach was chosen, and why?*;
- different deficit classes invite different approaches (misconception vs forgetting vs fluency);
- composition across episodes can be justified educationally;
- mid-session revision remains intelligible because the prior commitment is explicit.

Teaching Strategies are how Kwalitec discharges the Tutor obligation at the grain of *instructional method*, after intention has named the educational change sought.

---

## 4. Responsibilities

A Teaching Strategy is responsible for:

1. **Serving one Teaching Intention** — existing only as a means to a named educational change.  
2. **Fitting the diagnosis class** — remaining coherent with the deficiency category and learning objective.  
3. **Respecting the working hypothesis** — choosing an approach that would succeed if the hypothesis is roughly right, or that would discriminate among competitors when discrimination is needed.  
4. **Constraining episode selection** — implying one or more lawful Learning Episode types.  
5. **Defining expected evidence profiles** — making success, partial success, and productive failure imaginable in principle.  
6. **Governing instructional decisions within episodes** — what kind of explanation, contrast, modelling, practice, retrieval, or reflection is primary.  
7. **Remaining revisable** — yielding to new evidence mid-session or mid-sequence without pretending the first choice was sacred.  
8. **Preserving Educational Atomicity** — not smuggling multiple co-equal educational aims under one method label.  
9. **Remaining subordinate to learning objectives** — methods serve syllabus-grounded aims, not the reverse.  
10. **Refusing implementation identity** — never collapsing into prompts, screens, or content files.

---

## 5. Inputs

A Teaching Strategy may be selected only when the following educational inputs are available (including lawful thin inputs under cold start):

| Input | Role |
|-------|------|
| **Educational Diagnosis** | Names the problem class, objective, dimension, warrant, and uncertainty |
| **Educational Hypothesis** | Explains the likely cause; constrains which approaches can test or repair |
| **Teaching Intention** | Names the educational change sought |
| **Teaching Goal** | Atomic, objective-linked statement realising the intention for the next episode |
| **Current understanding** | What the student already grasps, partially grasps, or misunderstands |
| **Prerequisites** | Upstream capabilities that must hold or be repaired first |
| **Evidence history** | Patterns of success, failure, retention, transfer, and reflection |
| **Confidence calibration** | Whether self-appraisal supports or impairs the intended approach |
| **Exam horizon** | Whether examination constraints lawfully shape method (never erase conceptual honesty) |
| **Cognitive load context** | Whether the student can absorb the chosen instructional demand |
| **Learning objective** | Curriculum-grounded aim that instruction must remain accountable to |
| **Instructional principles** | Standing educational constraints on selection and composition |

Cold start does not waive strategy. It licenses strategies appropriate to introduction under curriculum sequencing, with honest thin evidence.

---

## 6. Outputs

Selecting a Teaching Strategy produces:

1. **Named strategy** — from the catalogue (or a lawful specialised variant with explicit justification).  
2. **Educational rationale** — why this approach fits diagnosis, hypothesis, and intention.  
3. **Episode implications** — one or more typical Learning Episode types that may realise it.  
4. **Expected evidence profile** — what would count as progress, stall, or productive contradiction.  
5. **Composition stance** — whether this strategy stands alone for the next episode, or opens a planned micro-sequence (see Composition Model).  
6. **Revision conditions** — what evidence would warrant changing strategy before the intention is abandoned.

Outputs are educational commitments, not software artefacts.

---

## 7. Relationships

### 7.1 Educational Diagnosis

Diagnosis answers: *what educational problem currently exists?*

Strategy answers: *how should instruction pursue the change that problem requires?*

Diagnosis **constrains** strategy by naming the deficit class. Diagnosis does **not** select strategy. Encoding a method inside a diagnosis statement (“needs spaced retrieval”) collapses the reasoning loop.

### 7.2 Educational Hypothesis

Hypothesis answers: *why is this problem likely present?*

Strategy should be coherent with the working hypothesis: the instructional approach should either repair the hypothesized cause or produce discriminating evidence among competitors. A strategy chosen against the hypothesis without justification is theatrical method-shopping.

### 7.3 Teaching Intention

Intention answers: *what educational improvement should the next episode achieve?*

Strategy answers: *how will we seek that improvement?*

Intention **precedes** strategy. Strategy may not redefine the aim. If the only available methods cannot serve the intention, revise intention or diagnosis — do not smuggle a new aim under a favourite method.

### 7.4 Learning Episodes

Episodes **realise** strategy under intention.

- One primary strategy governs an episode’s instructional approach.  
- Secondary instructional moves may support the primary strategy; they must not become co-equal competing strategies.  
- A strategy may span a micro-sequence of episodes when composition is deliberate (for example Worked Example → Guided Practice → Independent Practice).

Episode type and Teaching Strategy are related but not identical: type names the *kind of educational improvement container*; strategy names the *instructional approach* inside it. Some pairings are typical; none are automatic without rationale.

### 7.5 Evidence

Strategy commits the tutor to an evidence profile. After enactment:

- confirming evidence supports continuing or fading guidance;  
- contradicting evidence may revise strategy, hypothesis, or diagnosis;  
- thin evidence forbids strong strategy endorsement.

Strategies remain **evidence-driven**. Preference, novelty, or engagement theatre do not override evidence.

### 7.6 Reflection

Student reflection informs whether the strategy felt clarifying, overwhelming, or mismatched — soft evidence that may warrant adaptation. Fabricated or consequence-free reflection does not justify strategy change theatre.

### 7.7 Digital Twin

The Digital Twin holds lawful educational memory of understanding, evidence, uncertainty, and history. Strategy selection may **consult** twin state as background constraint. Strategy selection must **not**:

- treat twin scores as diagnosis;  
- write mastery claims from a single strategy success;  
- ignore twin uncertainty when choosing high-load approaches.

Twin updates after episodes cite evidence and evaluation outcomes; they do not invent strategy efficacy beyond warrant.

---

## 8. Position in the Educational Reasoning Loop

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
Teaching Strategy     ← this architecture
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

**Analytical order is binding:** *what problem* → *why* → *what change* → *how* → *enact*.

**Forbidden collapse:** jumping from a wrong answer to “more questions” without intention and strategy; choosing a fashionable method and reverse-fitting an intention; equating episode type selection with strategy selection without rationale.

---

## 9. Strategy Grain and Scope

| Grain | Meaning |
|-------|---------|
| **Primary strategy (episode)** | The governing instructional approach for one Learning Episode |
| **Strategy sequence (composition)** | An ordered chain of strategies across episodes serving one intention or a lawful intention progression |
| **Standing preference** | Not recognised — Kwalitec does not adopt permanent “house styles” that override diagnosis |

Guidance intensity within a strategy (for example Progressive Scaffolding or Faded Guidance) may change within or across episodes as understanding increases. Changing guidance intensity is not the same as abandoning the intention.

---

## 10. Governance Rules (Summary)

1. Every strategy serves a Teaching Intention.  
2. Strategies never replace diagnosis.  
3. Strategies remain evidence-driven and revisable.  
4. Strategy choice requires educational justification.  
5. Guidance decreases as understanding increases (unless diagnosis warrants temporary re-scaffolding).  
6. Strategies respect Educational Atomicity.  
7. Instruction remains subordinate to learning objectives.  
8. Strategies are educational reasoning artefacts — never prompts, screens, or data entities.

Full binding statements: [`STRATEGY_INVARIANTS.md`](STRATEGY_INVARIANTS.md).

---

## 11. Summary Propositions

1. Teaching Strategy specifies *how* the tutor intends to produce a desired educational change.  
2. Strategy follows diagnosis, hypothesis, and intention; it precedes Learning Episode enactment.  
3. Strategy governs instructional decisions; it does not prescribe implementation, UI, or AI prompts.  
4. Strategy transforms Teaching Intention into one or more Learning Episodes.  
5. Strategy remains subordinate to learning objectives and Educational Atomicity.  
6. Strategy is revisable when evidence warrants — without thrash and without sacred first choices.  
7. The catalogue, principles, selection model, composition model, and invariants specialised this architecture for long-term governance.
