# Conflict Resolution Framework

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS002 — Conflict Resolution Framework  
**Classification:** Highest educational authority for *conflict resolution* meaning within Programme VII Workstream 2  
**Status:** APPROVED — governing for educational conflict resolution contract  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Conflict Resolution Framework** for Kwalitec.

It is subordinate to the Educational Constitution, specialised Programme VI educational models, and the Educational Authority Model (WS2 / MS001). It governs **how simultaneously valid educational recommendations yield one lawful acted-upon outcome**. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning, transfer ownership, or amend Authority Model boundaries.

Authority order for educational conflict resolution:

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Evidence Model defines what may warrant educational claims.  
> Continuity Standard preserves rightful educational history.  
> State Authority Matrix defines who may mutate educational states.  
> Programme VI (Master Planner and coaches) defines educational reasoning and may emit authorised recommendations.  
> Programme VII Workstream 1 defines how that reasoning is orchestrated across components.  
> Educational Authority Model (WS2 / MS001) defines who owns each educational decision.  
> **This Conflict Resolution Framework (Programme VII / Workstream 2 / MS002) defines how conflicts among constitutionally valid recommendations yield a lawful educational outcome.**  
> Downstream Runtime A, product surfaces, and narration must consume this resolution law — never invent ownership, rewrite meaning, or arbitrate by discretionary score.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabi such as CM1/CS1 and peers).

An expert IFoA tutor does not invent a new tutor when several good pieces of advice arrive at once. After Programme VI has defined *what each educational question means*, after Workstream 1 has defined *how reasoning flows*, and after the Authority Model has defined *who owns each decision*, the tutor still needs an answer to one coordination question:

> **“When multiple constitutionally valid recommendations coexist, how does Kwalitec determine the lawful educational outcome?”**

That answer must select which valid recommendation is acted upon, preserve each owner’s constitutional rights, leave educational meaning unchanged, apply published rules rather than runtime discretion, and remain explainable — without becoming a second Authority Model, a meta-coach, or a ranking engine.

This document records that tutor posture so every future Educational Authority Engine subsystem has a single educational reference for *how conflicts are resolved while authority is preserved*.

> **The Conflict Resolution Framework describes coordination among valid educational decisions.  
> It does not transfer ownership, redefine educational meaning, or implement Runtime A.**

---

## 2. What Conflict Resolution Is

**Educational conflict resolution** is the constitutional act by which Kwalitec determines the **lawful educational outcome** when two or more **constitutionally valid** recommendations, priorities, or orchestration claims **compete for action** at the same coordination moment — without transferring decision ownership or changing educational meaning.

| Concept | Definition | Primary question |
|---------|------------|------------------|
| **Conflict** | Simultaneous coexistence of multiple constitutionally valid artefacts that cannot all be acted upon as primary at once (`CONFLICT_TYPES.md`) | What competes for action? |
| **Valid recommendation** | An educational artefact already authorised by its Programme VI owner within its Authority Model domain | Is each claim already lawful on its own? |
| **Resolution principle** | Binding constitutional rule that selects among valid artefacts without rewriting them (`RESOLUTION_PRINCIPLES.md`) | Which rule applies? |
| **Resolution outcome** | Lawful disposition of each competing artefact (`RESOLUTION_OUTCOMES.md`) | What happens to each recommendation? |
| **Acted-upon outcome** | The recommendation (or permitted merge) that becomes the student’s primary educational action now | What may the student treat as primary? |
| **Ownership preservation record** | Explicit confirmation that owners, meanings, and Authority Model boundaries survived resolution | Did authority stay intact? |

Conflict resolution is:

- **coordinating** — it settles action among already-valid artefacts;
- **ownership-preserving** — owners remain owners after the outcome;
- **meaning-preserving** — Programme VI educational meanings are unchanged by the resolution itself;
- **rule-bound** — published principles decide; runtime discretion does not;
- **non-alienating** — resolution never transfers constitutional ownership;
- **non-inventing** — resolution does not mint a new educational tip without a Programme VI warrant;
- **explainable** — students and developers can see why the conflict existed and why the outcome was lawful;
- **orthogonal to mutation** — selecting an acted-upon outcome does not grant EIP-001 write rights.

Conflict resolution is **not**:

- arbitration of *who owns* a decision class (that is MS001 / Authority Model);
- reinterpretation of Educational Evidence under a conflict label;
- modification of Programme VI recommendations’ educational meaning;
- a rewrite of the Canonical Study Plan;
- a meta-coach that absorbs Daily, Recovery, Revision, Exam, Learning, or Master Planner domains;
- a scoring, ranking, or optimiser algorithm;
- a scheduler, job queue, saga, or runtime state machine;
- a claim that resolving a conflict guarantees learning or a pass.

---

## 3. Binding Distinction: Conflict Resolution vs Neighbours

| Layer | Educational / coordination job | Unlawful collapse |
|-------|--------------------------------|-------------------|
| **Programme VI meaning** | What a recommendation *means* and why it is warranted | Letting resolution rewrite coach meaning |
| **Authority ownership (MS001)** | Who may *decide* a class | Letting resolution transfer or invent owners |
| **Workflow orchestration (WS1)** | How owners are *invited and sequenced* | Letting resolution invent stages or tips |
| **Conflict resolution (this Framework)** | Which *valid* recommendation is *acted upon* when several coexist | Treating ownership disputes as “conflicts” to merge |
| **State mutation (EIP-001)** | Who may *write* educational states | Treating acted-upon selection as write authority |
| **Product presentation** | How outcomes are *shown* | Letting UI pick winners by convenience |

**Ownership conflicts** (two components claiming the same decision class) are **out of this Framework’s resolution path**. They violate AP-01 and must be **refused** and referred to the Authority Model — not “resolved” by merging meanings.

**Action conflicts** (multiple valid recommendations competing for primary action) are **in scope**. Resolution selects among them while each owner remains owner of its artefact.

MS001 without MS002 risks clear ownership with no lawful story when several owners’ valid outputs arrive together.  
MS002 without MS001 risks selecting winners without a map of who may decide.  
Both are required; neither replaces Programme VI meaning.

---

## 4. Educational Purpose

The Conflict Resolution Framework exists so that:

1. **Concurrent valid advice does not become chaos** — the student receives one lawful primary outcome without coaches appearing to argue randomly.
2. **Ownership survives concurrency** — selecting which recommendation is acted upon never silently absorbs a sibling domain.
3. **Meaning survives concurrency** — deferred, queued, or superseded recommendations keep their educational meaning; they are not rewritten to “fit.”
4. **Higher obligations remain higher** — where the Constitution, Evidence Model, Continuity, or Authority boundaries explicitly constrain action, those obligations take precedence over ordinary coach concurrency.
5. **Rules beat discretion** — the same conflict situation yields the same lawful outcome class under the same published principles.
6. **Explainability remains honest** — students and developers can see why a conflict existed, which rules applied, and that authority was preserved.

---

## 5. Core Responsibilities

The Conflict Resolution Framework is educationally responsible for:

| Responsibility | Meaning |
|----------------|---------|
| **Name conflict kinds** | Publish coordination conflicts that may arise (`CONFLICT_TYPES.md`) |
| **Bind resolution principles** | Enforce ownership preservation, meaning invariance, obligation precedence, and rule-bound selection (`RESOLUTION_PRINCIPLES.md`) |
| **Catalogue lawful outcomes** | Defer, supersede, merge (where permitted), queue, reject as unlawful (`RESOLUTION_OUTCOMES.md`) |
| **Separate action selection from ownership** | Acted-upon ≠ new owner |
| **Separate action selection from meaning** | Outcome disposition ≠ reinterpretation |
| **Refuse ownership disputes** | AP-01 violations are not resolved here |
| **Require explainability** | Make conflict, rules, outcome, and preservation speakable (`RESOLUTION_EXPLAINABILITY.md`) |

### 5.1 Binding non-responsibility

The Conflict Resolution Framework must **not**:

- redefine Programme VI educational meaning or coach questions;
- transfer, invent, or amend Authority Model domains by resolution fiat;
- invent workflow stages, transition conditions, or completion criteria;
- grant or invent EIP-001 mutation rights;
- implement ranking, scoring, priority heaps, or Runtime A services as constitutional law;
- select Educational Strategy, pack calendars, or mint mastery from conflict outcomes;
- absorb ownership of Educational Evidence, Estimated Knowledge, or Estimated Mastery under a “conflict engine” label;
- treat Version 2 Adaptive / Twin / Mission authorities as replacements for Programme VI / VII conflict law;
- silently merge competing coach meanings into a third mega-recommendation without a published constitutional merge pathway.

---

## 6. What May Conflict (Overview)

Detailed kinds live in `CONFLICT_TYPES.md`. At overview level, conflicts concern **coordination only**:

| Conflict family | Coordination question |
|-----------------|----------------------|
| **Concurrent recommendations** | Several owners emitted valid primary-action candidates now |
| **Competing educational priorities** | Distinct educational priorities are each warranted but cannot all lead |
| **Temporary authority contention** | Temporary primary focus and standing day/plan guidance both seek action |
| **Superseding recommendations** | A later valid recommendation claims to replace an earlier one’s *action*, not ownership |
| **Workflow timing conflicts** | Orchestration timing places multiple valid artefacts in the same action window |

Conflicts do **not** include: inventing recommendations, rewriting plans as a conflict side-effect, or arbitrating who owns a decision class.

---

## 7. Integrity Rules

1. **Valid first.** Only constitutionally valid recommendations enter resolution; unlawful claims are rejected, not ranked.
2. **Ownership preserved.** Resolution never transfers decision ownership.
3. **Meaning unchanged.** Resolution disposes action; it does not rewrite educational meaning.
4. **Rules, not discretion.** Published principles decide; optimiser preference does not.
5. **Higher obligations first.** Explicit constitutional obligations (Constitution, Evidence honesty, Continuity, Authority boundaries, plan non-mutation) precede ordinary concurrency among coaches.
6. **Single primary action.** At most one acted-upon primary educational outcome for a given coordination moment (unless a published merge pathway explicitly permits a composite).
7. **Non-acted artefacts remain lawful.** Deferred, queued, or superseded recommendations keep their owner and meaning.
8. **Ownership disputes refuse.** Competing ownership claims → Authority Model; do not “resolve” by merge.
9. **Orchestrate ≠ decide.** Workflow timing may surface a conflict; it may not invent the educational winner’s meaning.
10. **Explain the resolution.** Material outcomes must cite conflict kind, principles, outcome, and ownership preservation.

---

## 8. Position in the Educational Stack

```
Educational Constitution (EGI-001)
        │
        ├── EIP-001 State Authority Matrix ………… mutation rights
        ├── EIP-002 Evidence Model ………………… observational truth
        ├── EIP-006 Knowledge & Mastery …………… claim ladder
        │
        ▼
Programme VI — Educational meaning
        │  Master Planner · Daily · Learning · Recovery · Revision · Exam
        │  emit constitutionally valid recommendations
        │
        ▼
Programme VII / WS2 / MS001 — Educational Authority Model
        │  decision ownership map (unchanged by MS002)
        │
        ├── Programme VII / WS1 — Workflow Engine …… may surface concurrency
        │
        ▼
Programme VII / WS2 / MS002 — Conflict Resolution Framework (this document)
        │  lawful outcome among valid recommendations
        │  preserves ownership · meaning · boundaries
        │
        ▼
Runtime A / Version 2 adapters / product surfaces
        │  consume resolution outcomes; never invent winners
```

---

## 9. Relationship to Programme VII Workstream 1 and MS001

| Concern | WS1 (Workflows) | WS2 / MS001 (Authority) | WS2 / MS002 (this Framework) |
|---------|-----------------|-------------------------|------------------------------|
| Primary question | How do decisions *flow*? | Who *owns* decisions? | Which *valid* recommendation is *acted upon*? |
| Artefacts | Events, stages, transitions, completion | Principles, domains, boundaries | Conflict types, resolution principles, outcomes |
| May select primary action among valid artefacts | Surfaces concurrency; does not invent meaning | Names owners; does not pick winners among valid peers | Yes — by published resolution law |
| May answer the educational question | No | No — owners answer via Programme VI | No — disposition only |
| May redefine coach meaning | No | No | No |
| May transfer ownership | No | No (preservation / restoration only) | No |

Workstream 1 without MS002 risks *concurrency without lawful selection*.  
MS001 without MS002 risks *ownership without lawful concurrency disposition*.  
MS002 without MS001 risks *winners without owners*.  
All three are required; none replaces Programme VI meaning.

---

## 10. Out of Scope

This Framework does **not** include:

- Runtime A, feature flags, or services
- Conflict-resolution algorithms, scores, ranking, or scheduling logic
- Database models or persistence schemas
- UI, analytics, or notifications
- Amendments to Programme VI educational meaning corpora
- Amendments to Authority Model domains by resolution fiat
- Changes to EIP-001 permitted writers

Those remain with their respective owners.

---

## 11. Closing

Conflict resolution is the constitutional posture that keeps several good tutors from talking over each other — without inventing a fourth tutor.

When recommendations compete for action, **apply published principles and name the outcome**.  
When ownership is unclear or contested, **refuse and consult the Authority Model** — do not resolve ownership here.  
When meaning would need rewriting to “make the conflict go away,” **amend Programme VI corpora** — do not resolve by reinterpretation.

> **Conflict resolution preserves authority. It never transfers ownership or changes educational meaning.**
