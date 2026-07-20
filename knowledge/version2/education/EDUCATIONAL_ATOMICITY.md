# Educational Atomicity

**Document ID:** V2-LEA-006  
**Classification:** Educational Architecture — Learning Episode Foundation  
**Status:** Foundational educational principle  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Foundational (episode scope) / Architectural (application)  
**Parent:** [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md)  

**Related:** [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) · [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) · [`LEARNING_MODEL.md`](LEARNING_MODEL.md) · [`TUTOR_MODEL.md`](TUTOR_MODEL.md)

---

## 1. Purpose

This document defines **Educational Atomicity**: a foundational principle governing the scope of every Learning Episode.

Educational Atomicity is why Learning Episodes can be diagnosed, taught, evidenced, and sequenced without collapsing into chapter-sized theatre.

---

## 2. Definition

**Educational Atomicity:** the requirement that every Learning Episode be scoped to improve **one** educational capability — one deliberate, nameable improvement in what the student can understand, do, connect, retain, transfer, or correct — relative to a curriculum-grounded learning objective.

### Governing statement

> Every Learning Episode should improve one educational capability.

Not a chapter.  
Not a subject.  
Not “everything weak.”  
One capability.

---

## 3. What Counts as One Educational Capability

An educational capability is a **single teachable advance**, for example:

- grasp exponential-family intuition for a modelled response;  
- correctly distinguish select vs ultimate mortality;  
- execute one net-premium method family independently;  
- repair the misconception that continuous and discrete payment models are interchangeable without adjustment;  
- retrieve after delay the conditions of validity for a reserve method;  
- transfer an annuity valuation to a reworded stem.

A capability is **not**:

- an entire GLM catalogue;  
- a full syllabus chapter;  
- “be ready for the exam”;  
- “finish today’s mission” as educational meaning;  
- a bundle of unrelated improvements packed for calendar convenience.

---

## 4. Good vs Poor Scope

### 4.1 Good (atomic)

| Episode purpose | Why it is atomic |
|-----------------|------------------|
| Teach exponential-family intuition | One conceptual capability |
| Repair one misconception (select vs ultimate) | One wrong model |
| Guided practice on term-assurance EPV under constant force | One method family under scaffolds |
| Retrieval of commutation-function selection rules | One retrieval aim |
| Transfer practice on deferred annuities from whole-life drills | One variation class |

### 4.2 Poor (non-atomic)

| Episode purpose | Why it fails |
|-----------------|--------------|
| Teach all GLMs | Many capabilities collapsed |
| Revise an entire chapter | Coverage region, not one capability |
| Learn mortality | Vague; unbounded |
| Do Chapter 4 | Administrative container as purpose |
| Practice everything I got wrong this month | Multiple unrelated repairs without episode boundaries |
| Capstone the whole subject in one sitting | Violates dependency and atomicity |

Poor scopes may still be **journey or plan goals**. They must be decomposed into atomic episodes (and sequences of episodes) before tutoring executes them.

---

## 5. Why Atomicity Improves Tutoring

### 5.1 Diagnosability

When an episode fails, the tutor knows *which* capability did not advance. Non-atomic episodes produce ambiguous failure: the student “didn’t get Chapter 4,” which cannot select a strategy.

### 5.2 Strategy fit

Different deficits need different strategies. Atomic purposes allow Misconception Repair vs Retrieval vs Guided Practice to be chosen precisely. Mega-purposes force a generic firehose.

### 5.3 Evidence quality

Evidence must be relevant to purpose. One purpose yields interpretable evidence. Many purposes yield a slurry of scores that support false confidence.

### 5.4 Honest evaluation

Episode evaluation can say yes / partial / no / inconclusive about one goal. Multi-goal episodes invite grade averaging that hides unrepaired misconceptions.

### 5.5 Sequencing power

Atomic episodes compose into micro-sequences. Composition is how Kwalitec builds arcs without lying about what each step was for.

### 5.6 Twin interpretability

Learner-state updates are cleaner when evidence is attributed to one objective and one purpose. Non-atomic episodes blur which belief should move.

### 5.7 Student trust

Students experience tutoring as purposeful: “we are fixing this one confusion,” not “we are drowning in content.” Scarce professional study time rewards precision.

### 5.8 Implementation independence

Atomic educational units survive UI redesigns. Screens may group or split presentation; the educational atom remains stable.

---

## 6. Relationship to Learning Dimensions

Educational Atomicity requires **one capability**, typically aligned with **one primary learning dimension**.

This is compatible with the Learning Model rule that an episode advance **at least one** dimension:

- Atomicity forbids advancing many unrelated aims at once.  
- The Learning Model forbids dimension-free busywork.  
- Together: one purpose, one primary dimension, relevant evidence.

Secondary dimensional effects may occur. They do not expand the declared purpose.

---

## 7. Relationship to Episode Types

Episode types encode *kinds* of atomic purposes. Atomicity constrains even broad-sounding types:

| Type | Atomic reading | Non-atomic abuse |
|------|----------------|------------------|
| Revision | Revisit one aim | “Revise all of Subject X” |
| Capstone | One integrated capstone aim | “Do the whole topic unsorted” |
| Synthesis | Integrate a declared set of facets into one whole | Merge unrelated topics |
| Prerequisite Repair | Repair one blocking prerequisite | Re-teach prior chapter wholesale |
| Exam Application | Exam-format probe of one aim | Full mock as one undivided educational purpose without internal episode structure |

Full mocks and long sittings may **contain** many atomic episodes. The sitting is not itself the atom.

---

## 8. Decomposition Rule

When a desired outcome is non-atomic, educational design must **decompose**:

```text
Non-atomic aim
     ↓
Identify constituent capabilities
     ↓
Map each to a Learning Episode (type + objective + strategy)
     ↓
Order as Micro Sequence / Session / Journey plan
     ↓
Execute and evaluate atomically
```

Decomposition is not bureaucracy. It is how tutoring remains possible.

---

## 9. Tension with Student Desire for “Coverage”

Students often want chapter completion. Kwalitec may acknowledge coverage as Study Progress while still tutoring atomically.

**Lawful product stance**

- Show coverage progress honestly as coverage.  
- Deliver teaching as atomic episodes.  
- Never equate chapter coverage with atomic learning success.

---

## 10. Failure Modes if Atomicity Is Abandoned

1. **False mastery** — finishing large blobs feels like competence.  
2. **Unrepairable misconceptions** — buried inside volume.  
3. **Unexplainable recommendations** — “do more of Chapter 4” without educational need.  
4. **Twin noise** — evidence cannot update specific beliefs.  
5. **Session bloat** — sittings expand until learning collapses under fatigue.  
6. **UI ontology capture** — pages become the unit of education.

---

## 11. Governance

1. Episode design reviews must ask: *What single capability improves?*  
2. If the answer lists multiple unrelated capabilities, split episodes.  
3. Journey and mission packaging may batch episodes for the day; batching is not fusion.  
4. Amendments that weaken atomicity require explicit educational governance rationale.

---

## 12. Summary Propositions

1. Educational Atomicity means one Learning Episode improves one educational capability.  
2. Good tutoring scopes are precise; poor scopes are chapter-sized or catalogue-sized.  
3. Atomicity enables diagnosis, strategy fit, evidence, sequencing, and twin honesty.  
4. Non-atomic aims must be decomposed before teaching.  
5. Atomicity is foundational to Version 2 Learning Episode Architecture.
