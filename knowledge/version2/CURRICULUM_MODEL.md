# Version 2 Curriculum Model

**Document ID:** V2-001-CURRICULUM  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Authoritative educational structure model  
**Nature:** Structural / educational — does not reproduce copyrighted syllabus content  

**Parent:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)  
**Engine coexistence:** [ADR-003](../architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)

This document models how Version 2 thinks about educational structure. It does **not** copy official syllabus text, questions, or proprietary materials. Concrete papers remain loaded from authorised curriculum JSON via the Curriculum Engine.

---

## 1. Structural Hierarchy

```
Curriculum
    ↓
Subject
    ↓
Chapter
    ↓
Topic
    ↓
Learning Journey
    ↓
Learning Sessions
```

Each level has a distinct educational job. Lower levels inherit identity from higher levels; they do not invent parallel trees.

---

## 2. Curriculum

### Purpose

Name a versioned official syllabus offering a student can prepare for (body + paper + edition/year).

### Responsibilities

- Scope all Subjects (or the single subject paper)
- Carry edition metadata needed for continuity remapping
- Remain the import root for the Curriculum Engine

### Relationship to engine today

Maps to engine/ORM `Curriculum` / `CurriculumDefinition` identity. Flat (V1) and hierarchical (engine V2) formats both remain loadable.

---

## 3. Subject

### Purpose

Represent a coherent examinable domain within a curriculum (often the whole paper for single-paper offerings; multiple subjects when a curriculum is partitioned).

### Responsibilities

- Group Chapters
- Provide subject-level navigation and analytics rollups (future)
- Hold subject-level weighting only when the official syllabus does

### Mapping note

Version 2 educational language introduces **Subject** even when a given JSON file effectively has one subject. Implementation must not require multi-subject data where none exists.

---

## 4. Chapter

### Purpose

Represent a major syllabus partition that groups related Topics — typically corresponding to an official section / part.

### Responsibilities

- Order Topics for recommended traversal
- Carry chapter/section exam weight when provided by the official syllabus
- Support chapter-level progress rollups without claiming mastery

### Mapping note

Aligns with engine **Section** in hierarchical curricula ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md)). For flat V1 curricula without sections, Chapter may be a synthetic single partition or absent in presentation — traversal must still work (ADR-004).

**Naming:** Educational docs prefer Subject / Chapter / Topic. Engineering may continue to say Section until a rename milestone. Meaning must not fork.

---

## 5. Topic

### Purpose

Represent the atomic syllabus unit students journey through — the anchor of a Learning Journey.

### Responsibilities

- Bind Learning Objectives
- Anchor Study Progress / Topic Complete
- Participate in prerequisites and recommended ordering
- Carry topic-level weight only when the syllabus assigns it (flat curricula)

### Invariants

- Stable official identity codes where provided
- Never invented by missions, recommendations, or Twin
- One primary Learning Journey per learner per topic per curriculum edition (reopen policy deferred)

---

## 6. Learning Journey (structural role)

At the curriculum-model layer, a Learning Journey is the **student-specific instantiation** of learning a Topic.

Structure docs care about:

- which Topic it binds
- which objectives it must address
- what completion criteria apply
- how sessions are expected to unfold (effort estimate)

Domain behaviour: [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md).

---

## 7. Learning Sessions (structural role)

Sessions are ordered or unordered **work units** within a journey. The curriculum model may recommend a default session pattern (e.g. expose → practice → revise) without mandating identical lengths for every topic.

---

## 8. Learning Objectives

### Purpose

State what the learner should be able to do or understand for a Topic, using official outcome/objective wording references (ids + titles), not republished copyrighted prose beyond fair operational need.

### Responsibilities

- Guide session focus and explainability
- Inform completion criteria (which objectives need exposure / practice evidence)
- Remain curriculum-owned

### Mapping note

Corresponds to Learning Outcome (flat) / Learning Objective (hierarchical) definitions in the engine.

---

## 9. Prerequisites

### Purpose

Express that Topic B assumes competence or coverage of Topic A (or Chapter-level preparation).

### Rules

1. Prerequisites are curriculum facts or curated educational edges — not Twin guesses.
2. Recommendations may warn or suggest prerequisite journeys; Learning Mode sequencing still prefers official order unless a disclosed mode interrupts.
3. Missing prerequisite evidence increases uncertainty; it does not invent false completion of the dependent topic.

### Storage

Formal graph edges are a V2-002 Curriculum Graph concern. V2-001 requires the concept only.

---

## 10. Dependencies

Dependencies generalise prerequisites to include:

- soft dependencies (helpful but not blocking)
- assessment dependencies (practice sets that assume prior topics)
- revision dependencies (return edges after later chapters)

Dependencies must be typed so engines do not treat all edges as hard blockers.

---

## 11. Recommended Ordering

### Purpose

Provide the default sequence for Learning Mode journey activation.

### Rules

1. Official syllabus order is canonical when published.
2. Hierarchical curricula: Chapter order, then Topic order within Chapter (ADR-004).
3. Flat curricula: established topic ordering helpers remain authoritative.
4. Adaptive reordering is advice or authorised mode behaviour — never silent corruption of official order records.
5. Journey continuation on an active topic outranks starting the next topic in order (Principles P3).

---

## 12. Effort Estimation

### Purpose

Estimate how much learning work a Topic journey likely needs — in sessions and/or time — so planning and recommendations stay realistic.

### Characteristics

| Property | Rule |
|----------|------|
| Nature | Estimate, always labelled as such |
| Inputs | Syllabus weight, objective count, historical cohort medians (future), Twin capacity |
| Output | Suggested session count / duration band for the journey |
| Non-output | Mastery guarantee; pass probability |

### Rules

1. Effort estimates inform planning; they do not auto-complete anything.
2. Undershoot / overshoot vs estimate is behavioural evidence for capacity realism.
3. Estimates must be revisable as evidence accumulates (without rewriting history).

Concrete formulae are deferred to V2-003 / V2-008.

---

## 13. Completion Criteria

### Purpose

Define when a Learning Journey may enter `READY_FOR_COMPLETION` and when Topic Complete may be confirmed.

### Conceptual criteria families

| Family | Question | Notes |
|--------|----------|-------|
| **Exposure / coverage** | Has the student completed the defined study obligations for this topic? | Maps to Study Progress honesty |
| **Session sufficiency** | Has the journey produced the minimum learning sessions (or equivalent effort)? | Default: more than one session allowed/required per topic policy |
| **Reflection closure** | Are owed reflections captured? | Principle P5 |
| **Objective attention** | Have listed objectives been addressed by sessions/evidence? | Not the same as mastered |
| **Evidence floor** (optional by topic type) | Is there minimum authorised practice evidence when the topic requires it? | Never sole mastery proof |

### Hard rules

1. Completion criteria **must not** be “Estimated Mastery ≥ threshold.”
2. Completion criteria **must not** be “one mission completed.”
3. Confirming Topic Complete may update coverage (Study Progress) when constitutionally lawful.
4. Twin estimates may **inform** advice to continue practice after Topic Complete; they do not block coverage honesty indefinitely without disclosure (product policy for V2-003).
5. Student confirmation remains part of lawful coverage completion unless a future constitutional pathway defines otherwise.

### Topic Complete meaning

Topic Complete = journey `COMPLETED` under these criteria.

It means: **completed studying this topic’s journey obligations.**

It does **not** mean: Exam Ready, Mastered, or certified professional competence.

---

## 14. Progress Rollups

| Level | Progress meaning |
|-------|------------------|
| Session | Finished / abandoned / in progress |
| Journey / Topic | JourneyProgress + Topic Complete posture |
| Chapter | Aggregate of topic journey postures (coverage-oriented) |
| Subject / Curriculum | Aggregate coverage vs syllabus scope |

Understanding estimates may be rolled up separately by the Twin / analytics — never mixed unlabeled into coverage percentages (EPA-002 dual-readiness class failure).

---

## 15. What This Document Does Not Contain

- Official syllabus paragraphs, formulae sheets, or past-paper content
- Database schemas for Section/Topic tables
- Numeric weighting algorithms
- Copyrighted learning objective full text beyond id/title operational references

---

## 16. Closing

Version 2 curriculum structure exists so Learning Journeys attach to real syllabus anatomy. Implementation builds the Curriculum Graph (V2-002) from this model without renaming educational meaning ad hoc.
