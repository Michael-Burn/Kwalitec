# Educational State Model

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS001 — Educational State Model  
**Classification:** Highest educational authority for *constitutional educational context* meaning within Programme VII Workstream 4  
**Status:** APPROVED — governing for educational state educational contract  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Educational State Model** for Kwalitec.

It is subordinate to the Educational Constitution and specialised Programme VI educational models. It governs **what constitutional educational state may exist** and **what each recognised state represents** as educational *context*. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning, alter ownership, execute workflows, or mint recommendations.

Authority order for educational state (constitutional context):

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Evidence Model defines what may warrant educational claims.  
> Continuity Standard preserves rightful educational history.  
> State Authority Matrix defines who may mutate Article IV educational states.  
> Programme VI (Master Planner and coaches) defines educational meaning for planning, today, learning, recovery, revision, and examination.  
> Programme VII Workstream 1 defines how that reasoning is orchestrated across components.  
> Programme VII Workstream 2 defines who owns decisions, how valid recommendations compete, and how permission is explained.  
> Programme VII Workstream 3 defines what recommendations and recommendation sets are.  
> **This Educational State Model (Programme VII / Workstream 4 / MS001) defines what constitutional educational context may exist and what each state represents.**  
> Downstream Runtime A, product surfaces, and narration must consume this context law — never treat context labels as success, mastery, or workflow completion.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabi such as CM1/CS1 and peers).

An expert IFoA tutor does not confuse *where the student is in constitutional educational context* with *whether they have mastered a topic* or *whether a workflow finished*. After Programme VI has defined *what each educational question means*, after Workstreams 1–3 have defined *flow, ownership, and recommendations*, the tutor still needs one context answer:

> **“What constitutional educational state may exist, and what does each state represent?”**

That answer must represent constitutional educational context, support lawful orchestration, support recommendation assembly, preserve educational continuity, and enable constitutional explainability — without creating educational meaning, altering authority, executing workflows, or claiming success or mastery.

This document records that tutor posture so every future Educational State Engine subsystem has a single educational reference for *what educational state is and is not*.

> **The Educational State Model describes constitutional educational context.  
> It does not create educational meaning, alter authority, or implement Runtime A.**

---

## 2. What Educational State Is

**Educational state** (in this Programme VII Workstream 4 sense) is the constitutional **representation of educational context** — a named, speakable posture describing which class of constitutional educational situation is currently live for a learner under an Active-class Canonical Study Plan (or its lawful absence) — without asserting educational success, learner mastery, workflow completion, or Article IV meaning-bearing facts.

| Concept | Definition | Primary question |
|---------|------------|------------------|
| **Constitutional educational context** | The live class of educational situation (e.g. day priority, recovery, revision, exam, structural planning) | Where are we educationally *as context*? |
| **Recognised state type** | A published EST-xx posture with meaning, entry, exit, observers, and prohibited interpretations | Which named context applies? |
| **Context warrant** | Constitutional conditions that make a state type lawfully enterable | Why may this context exist now? |
| **Observing component** | Workflow, authority, recommendation, or Programme VI consumer that may *read* the context | Who may observe it? |
| **Context continuity** | Preservation of honest context history when focus changes (EIP-005 specialised to context narration) | Did we erase where we were? |
| **Prohibited interpretation** | Readings that turn context into success, mastery, completion, tips, or ownership transfer | What must this state *never* mean? |

Educational state is:

- **representational** — it names context; it does not invent educational truth;
- **constitutional** — only published EST types exist; ad-hoc product labels are unlawful;
- **non-evaluative of success** — context ≠ pass, mastery, or “good student”;
- **non-executing** — state labels do not run workflows, write Article IV states, or pack calendars;
- **orchestration-supporting** — WS1 may observe context when coordinating;
- **assembly-supporting** — WS3 may reference context when packaging lawful guidance;
- **authority-preserving** — observing context never transfers WS2 ownership;
- **meaning-preserving** — Programme VI questions remain owned by their corpora;
- **explainable** — students and developers can see current context, why it exists, what supports it, and who references it;
- **continuity-aware** — context changes do not erase learner-owned educational history.

Educational state is **not**:

- Constitution Article IV meaning-bearing states (Study Progress, Educational Evidence, Estimated Knowledge / Mastery, Mission, …);
- a licence to create recommendations or redefine coach meaning;
- transfer or absorption of constitutional ownership;
- workflow stages, transitions, or completion criteria;
- a UI mode, feature flag, analytics segment, or database enum contract;
- a claim that being “in Recovery Context” means recovery succeeded;
- a claim that being “in Day Priority Context” means today’s mission is complete;
- a state machine implementation or Runtime A service.

### 2.1 Binding distinction from Article IV

| Horizon | Object | Owns |
|---------|--------|------|
| **Constitution Article IV / EIP** | Meaning-bearing educational states | Educational definitions and (via EIP-001) mutation rights |
| **This Model (VII / WS4 / MS001)** | Constitutional educational *context* states | Representation of live educational situation class |

Naming collision is intentional historically (“Educational State”) and **must be disambiguated in speech**:

- Student / tutor speech: prefer “educational focus / context” language.
- Developer / auditor speech: cite **EST-xx** for this Model; cite **Article IV / EIP-001 rows** for meaning-bearing states.

---

## 3. Educational Purpose

The Educational State Model exists so that:

1. **Context remains speakable** — “where we are educationally” has a constitutional answer independent of tip text and stage IDs.
2. **Orchestration stays honest** — workflows observe published context rather than inventing parallel posture labels.
3. **Recommendations stay situated** — assembled guidance can reference context without inventing it.
4. **Continuity survives product pressure** — context changes do not erase history or silently relabel mastery.
5. **Explainability is end-to-end** — current state, warrant, supporting evidence of context, and consumers are always answerable (EIP-003).
6. **Forbidden readings are blocked by design** — success, mastery, and workflow completion are never inferred from EST labels.

---

## 4. Core Responsibilities

The Educational State Model is educationally responsible for:

| Responsibility | Meaning |
|----------------|---------|
| **Define context representation** | Publish what counts as constitutional educational state (`STATE_TYPES.md`) |
| **Bind objectives** | Enforce context representation, orchestration support, assembly support, continuity, and explainability (`STATE_OBJECTIVES.md`) |
| **Draw hard boundaries** | Forbid tip creation, evidence redefinition, authority transfer, workflow replacement, and action execution (`STATE_BOUNDARIES.md`) |
| **Require explainability** | Make current state, warrant, supporting context evidence, and consumers speakable (`STATE_EXPLAINABILITY.md`) |
| **Preserve layering** | Keep context subordinate to Programme VI meaning and orthogonal to Article IV mutation |

### 4.1 Binding non-responsibility

The Educational State Model must **not**:

- redefine Programme VI educational meaning or coach questions;
- redefine Constitution Article IV educational states or EIP-001 mutation rows;
- invent workflow stages, transition conditions, or completion criteria;
- amend Authority Model domains or Conflict Resolution catalogues by context fiat;
- create, rank, or assemble educational recommendations;
- grant or invent EIP-001 mutation rights;
- implement Runtime A services, state machines, schedulers, databases, UI, or analytics;
- select Educational Strategy, pack calendars, or mint mastery from context labels;
- treat Version 2 operational state machines as replacements for this constitutional context law.

---

## 5. Educational Guarantees

A lawful Educational State posture **guarantees** the following educational properties — not exam outcomes.

| Guarantee | Meaning |
|-----------|---------|
| **Context fidelity** | Only published EST types may be treated as constitutional educational state |
| **Meaning fidelity** | Context representation never redefines Programme VI or Article IV meanings |
| **Non-success reading** | EST labels never mean educational success |
| **Non-mastery reading** | EST labels never mean learner mastery or Estimated Mastery |
| **Non-completion reading** | EST labels never mean workflow completion |
| **Authority preservation** | Observing or naming context never transfers WS2 ownership |
| **Boundary honesty** | Forbidden actions in `STATE_BOUNDARIES.md` are hard stops |
| **Explainability** | Every material context can answer the state explainability questions |
| **Continuity** | Context changes do not erase learner-owned educational history (EIP-005) |
| **Honest absence** | When no warrant exists, prefer Continuity Holding / Absent Plan over invented focus |

---

## 6. Relationship to Related Concepts

| Concept | Owns | Example |
|---------|------|---------|
| **Educational meaning** (Programme VI) | What guidance *means* | “Revision ≠ first learning” |
| **Article IV educational states** | Meaning-bearing educational objects | Study Progress, Educational Evidence |
| **Orchestration** (WS1) | How owners are invited and sequenced | Stage S3 invokes Daily Coach |
| **Authority / Conflict** (WS2) | Who owns decisions; which tip is acted upon | AD-02 owns “what today” |
| **Recommendations / Assembly** (WS3) | What tips and sets are | Structured recommendation artefact |
| **Educational state / context** (this Model) | Which constitutional context posture is live | EST-07 Recovery Context |

---

## 7. Integrity Rules

1. **Published types only.** Undocumented “modes” are not constitutional educational state.
2. **One primary context.** At most one primary EST type is constitutive for student-facing educational focus at a time, unless a documented parallel-read pattern applies (sibling contexts as read-only inputs).
3. **Entry before speech.** Context may not be narrated as live without satisfying entry conditions in `STATE_TYPES.md`.
4. **Exit before succession.** Successor context requires lawful exit of the prior primary where the catalogue requires it.
5. **Observers consume; they do not own.** Workflow, authority, and recommendation engines observe context; they do not become Master Planner or coaches by reading EST labels.
6. **Evidence of context ≠ Educational Evidence of understanding.** Warrants for context entry may cite plan class, disruption signals, or orchestration facts — they do not redefine EIP-002 observations.
7. **No silent Article IV writes.** Context change never mutates Study Progress, Evidence, or estimates.
8. **Amend before inventing.** New context types require amending this corpus first.

---

## 8. Stack Position Summary

```
Constitution / EIP (truth, Article IV states, mutation, continuity, explainability)
        │
        ▼
Programme VI — educational meaning
        │
        ▼
Programme VII WS4 — Educational State Model (this corpus)
        │  constitutional context representation (EST-xx)
        │
        ├──► WS1 Workflow …… observes context when coordinating
        ├──► WS2 Authority / Conflict …… consumes context; ownership intact
        └──► WS3 Recommendations / Assembly …… references context; does not invent it
```

---

## 9. Out of Scope

This milestone does **not** deliver Runtime A, state machines, algorithms, scheduling, database models, services, UI, or analytics. Those remain future or orthogonal workstreams and must consume — never redefine — this Model.
