# Learning Episode Sequence

**Document ID:** V2-LEA-005  
**Classification:** Educational Architecture — Learning Episode Foundation  
**Status:** Authoritative sequencing doctrine  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md)  

**Related:** [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) · [`LEARNING_EPISODE_LIFECYCLE.md`](LEARNING_EPISODE_LIFECYCLE.md) · [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md) · [`../LEARNING_JOURNEY_DOMAIN.md`](../LEARNING_JOURNEY_DOMAIN.md)

---

## 1. Purpose

This document explains how Learning Episodes **combine** into larger educational structures — and why educational sequencing matters.

Atomic episodes are necessary. They are not sufficient. Professional preparation requires ordered composition so that teaching builds, repairs, retains, and transfers without thrash.

---

## 2. Composition Hierarchy

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

| Level | Educational meaning |
|-------|---------------------|
| **Learning Episode** | One deliberate educational improvement |
| **Micro Sequence** | A short ordered chain of episodes serving one arc (for example introduce → example → guided practice) |
| **Learning Session** | One bounded sitting containing one or more episodes / micro-sequences |
| **Learning Journey** | Multi-session path through a curriculum topic toward educational completion |
| **Curriculum Progress** | Syllabus-relative posture of coverage and objective advancement — never mastery by synonym |

---

## 3. Why Educational Sequencing Matters

### 3.1 Cognitive dependency

Concepts and methods have educational prerequisites. Practising transfer before recognition produces noise, not learning. Sequencing respects dependency.

### 3.2 Strategy fading

Worked examples and guided practice exist to fade scaffolds. Skipping to independence too early causes failure cascades; never fading causes dependence.

### 3.3 Misconception hygiene

Repair must interrupt undifferentiated practice. Sequencing that postpones repair while drilling the wrong model is educationally harmful.

### 3.4 Temporal dimensions

Retention and transfer require spacing and variation *across* episodes and sessions. A single session cannot honestly claim retention.

### 3.5 Scarce student time

Professional candidates have limited daily capacity. Good sequencing maximises educational ROI per sitting; poor sequencing burns hours on the wrong grain.

### 3.6 Explainability

A sequence answers *why this next?* Continuity of episodes is the student’s experience of being tutored rather than shuffled.

---

## 4. Micro Sequences

A **Micro Sequence** is an ordered set of Learning Episodes with:

- a shared arc purpose (still composed of atomic episode purposes);  
- explicit succession rules;  
- evaluation checkpoints that can abort or branch the sequence educationally (not UI branching for novelty).

### 4.1 Classic first-pass micro sequence

```text
Concept Introduction
        ↓
   Worked Example
        ↓
  Guided Practice
        ↓
Independent Practice
```

**Arc purpose:** bring one objective from first exposure to independent application floor.

**Atomicity preserved:** each step has one purpose; the arc is composition, not a single mega-episode.

### 4.2 Misconception interrupt

```text
Independent Practice  (patterned failure detected)
        ↓
Misconception Repair
        ↓
 Guided Practice     (re-enter with scaffolds)
        ↓
Independent Practice (re-check)
```

### 4.3 Retention revisit

```text
Retrieval Practice
        ↓
Transfer Practice   (if retrieval succeeds)
   or
Concept Deepening   (if retrieval reveals conceptual fade)
```

### 4.4 Exam sharpening

```text
Revision                 (single aim)
        ↓
Transfer Practice
        ↓
Exam Application
```

### 4.5 Blocked progress

```text
Guided Practice          (collapse attributed to prerequisite)
        ↓
Prerequisite Repair
        ↓
Guided Practice          (resume)
```

---

## 5. Sessions as Containers

A Learning Session packages what a student can sustainably do in one sitting.

**Lawful patterns**

- One micro sequence (common)  
- One standalone episode (for example Recovery, Reflection, short Retrieval)  
- Two short episodes when atomicity and time allow  
- Capstone attempt as the session’s primary work when journey-ready  

**Unlawful patterns**

- Treating the session itself as the atomic teaching unit with no episode identity  
- Packing an entire chapter’s worth of purposes into one sitting without episode boundaries  
- Declaring topic complete because the session finished  

Session reflection may summarise a micro-sequence only if each episode retains evidence identity (see lifecycle compression rules).

---

## 6. Journeys as Multi-Session Stories

A Learning Journey sequences sessions — and therefore episode sequences — across days.

**Typical journey narrative (illustrative)**

```text
Week span for Topic T
  Session 1: Introduction micro sequence on Objective A
  Session 2: Deepening + connection for Objective A; introduce Objective B
  Session 3: Practice / repair as diagnosed
  Session 4: Retrieval on A; practice on B
  Session 5: Transfer + exam application on declared aims
  Session 6: Capstone inputs toward journey completion criteria
```

Journeys attend over time to all five learning dimensions. No single session must advance all five. Sequencing distributes dimensional attention honestly.

Revision sessions re-enter the same journey (or lawful return) rather than inventing a disconnected educational island.

---

## 7. Curriculum Progress

Curriculum Progress answers syllabus questions: what has been studied, which objectives have been addressed, what remains.

It **aggregates** journey and episode history. It must not:

- collapse episode evaluation into mastery;  
- treat coverage checkboxes as understanding;  
- reorder tutoring against official curriculum primacy without educational justification.

Episode sequencing remains accountable to curriculum structure while still allowing diagnosis-driven interrupts (prerequisite repair, misconception repair).

---

## 8. Sequencing Principles

1. **Dependency before demand** — do not demand transfer before introduction.  
2. **Repair before volume** — misconception and prerequisite interrupts outrank more clones.  
3. **Fade scaffolds deliberately** — Worked Example → Guided → Independent.  
4. **Space for retention** — retrieval/revision episodes across sessions.  
5. **Vary for transfer** — after independence, introduce legitimate novelty.  
6. **One purpose per step** — sequences compose atoms; they do not fuse them.  
7. **Evaluate to adapt** — sequence succession follows episode evaluation, not a fixed script immune to evidence.  
8. **Explain the path** — students should understand the arc, not only the next button.

---

## 9. Worked Examples (Actuarial)

### 9.1 Select vs ultimate mortality

```text
Concept Introduction   — select period meaning
        ↓
Concept Deepening      — why select differs from ultimate
        ↓
Worked Example         — reading a select table
        ↓
Guided Practice        — compute a probability with hints
        ↓
Independent Practice   — similar lookups alone
```

If patterned “always use ultimate from age 0” errors appear:

```text
Misconception Repair   — contrastive timelines
        ↓
Guided Practice        — re-check
```

### 9.2 Net premium calculation

```text
Concept Introduction   — equivalence principle
        ↓
Worked Example         — standard whole life net premium
        ↓
Guided Practice
        ↓
Independent Practice
        ↓
Transfer Practice      — deferred / temporary variants
        ↓
Exam Application       — word-problem stem under time
```

### 9.3 Pre-exam revision of one objective

```text
Retrieval Practice
        ↓
Confidence Calibration
        ↓
Exam Application
```

Not: “Revise all of Subject CM1 today” as one episode.

---

## 10. Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Fixed chapter playlist immune to diagnosis | Ignores misconceptions and prerequisites |
| Only independent practice forever | Starves concept and repair |
| Only explanations forever | Starves application, retention, transfer |
| Session = one undifferentiated blob | Loses atomic evaluation |
| Journey thrash across topics | Breaks continuity and retention |
| Capstone on day one | Violates dependency and atomic readiness |

---

## 11. Relationship to Product Surfaces

Product surfaces (Home, Session Experience, Journey views) may *present* sequences. They do not own sequencing law. Educational sequencing is determined by diagnosis, curriculum norms, episode types, and journey principles — then projected into UI.

One screen may show multiple episodes; one episode may span screens. Sequence identity remains educational.

---

## 12. Summary Propositions

1. Episodes compose into micro-sequences, sessions, journeys, and curriculum progress.  
2. Sequencing exists to respect dependency, fading, repair, spacing, and scarce time.  
3. Micro-sequences preserve atomicity while enabling arcs.  
4. Evidence can interrupt and redirect sequences.  
5. Curriculum progress aggregates; it does not redefine tutoring ontology.
