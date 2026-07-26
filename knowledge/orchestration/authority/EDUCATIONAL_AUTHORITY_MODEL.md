# Educational Authority Model

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS001 — Educational Authority Model  
**Classification:** Highest educational authority for *decision ownership* meaning within Programme VII Workstream 2  
**Status:** APPROVED — governing for educational authority educational contract  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Educational Authority Model** for Kwalitec.

It is subordinate to the Educational Constitution and specialised Programme VI educational models. It governs **which constitutional component owns which educational decisions**. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning absent from Programme VI.

Authority order for educational decision ownership:

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Evidence Model defines what may warrant educational claims.  
> Continuity Standard preserves rightful educational history.  
> State Authority Matrix defines who may mutate educational states.  
> Programme VI (Master Planner and coaches) defines educational reasoning for planning, today, learning, recovery, revision, and examination.  
> Programme VII Workstream 1 defines how that reasoning is orchestrated across components.  
> **This Educational Authority Model (Programme VII / Workstream 2 / MS001) defines who owns each educational decision.**  
> Downstream Runtime A, product surfaces, and narration must consume this ownership law — never invent ownership by proximity, convenience, or silent absorption.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabi such as CM1/CS1 and peers).

An expert IFoA tutor does not let every subsystem invent its own right to decide. After Programme VI has defined *what each educational question means*, and after Programme VII Workstream 1 has defined *how reasoning flows*, the tutor still needs an answer to one constitutional ownership question:

> **“Which constitutional component has authority to make which educational decisions?”**

That answer must distribute ownership explicitly, allow bounded delegation, preserve authority under product pressure, restore authority after temporary handoff, and prevent competing claims — without redefining educational meaning or becoming a second Workflow Engine.

This document records that tutor posture so every future Educational Authority Engine subsystem has a single educational reference for *how authority is distributed and exercised*.

> **The Educational Authority Model describes ownership of educational decisions.  
> It does not redefine educational meaning, orchestrate workflows, or implement Runtime A.**

---

## 2. What Educational Authority Is

**Educational authority** is the constitutional right of a named component to **make**, **delegate within bounds**, or **refuse** a defined class of educational decisions — and to be the accountable owner when that class is at stake.

| Concept | Definition | Primary question |
|---------|------------|------------------|
| **Authority owner** | Constitutional component accountable for a decision class | Who owns this decision? |
| **Educational decision** | Judgement that changes what the student or system may lawfully treat as educational guidance | What is being decided? |
| **Authority domain** | Bundle of owned, consumed, and prohibited decisions for one owner | What may this owner decide? |
| **Delegated authority** | Temporary, bounded exercise of a decision under the owner’s warrant | Who is acting for whom? |
| **Authority boundary** | Hard limit the owner and all delegates must not cross | What is forbidden regardless of convenience? |
| **Authority preservation** | Continued recognition of the owner while others consume or coordinate | Did ownership survive the handoff? |
| **Authority restoration** | Return of a temporarily delegated or suspended decision right to its owner | Has ownership returned cleanly? |

Educational authority is:

- **explicit** — ownership is named in this Model, not inferred from code location or UI;
- **singular per decision** — each educational decision class has exactly one owner;
- **domain-bounded** — owners decide only within their published domain;
- **delegable but not alienable** — delegation does not transfer ownership;
- **consumable** — other components may read authorised outputs without absorbing the decision;
- **preservable** — orchestration and siblings must not silently replace the owner;
- **restorable** — after temporary handoff or suspension, ownership returns to the constitutional owner;
- **explainable** — students and developers can see why one component decided and another could not.

Educational authority is **not**:

- a licence to redefine another component’s educational meaning;
- mutation rights over Study Progress, Evidence, or Mastery (EIP-001 owns that map);
- workflow stage sequencing (Programme VII Workstream 1);
- an independent recommendation engine that invents tips without a Programme VI warrant;
- product ownership of screens, analytics, or infrastructure adapters;
- a claim that owning a decision guarantees student success.

---

## 3. Educational Purpose

The Educational Authority Model exists so that:

1. **Ownership is never ambiguous** — “who decided this?” has one constitutional answer.
2. **Coaches and the Master Planner do not absorb each other’s jobs** — day priority, progression, recovery, revision, examination, and long-term planning remain distinct.
3. **Orchestration cannot become a second tutor** — the Workflow Engine coordinates owners; it does not own their decisions.
4. **Delegation remains honest** — a session may adapt locally under Daily Coach warrant without becoming a new Master Planner.
5. **Conflicts are prevented by design** — competing claims fail the single-owner principle before algorithms are invented.
6. **Authority survives product complexity** — Version 2 engines, experience surfaces, and adapters consume this map; they do not invent parallel educational ownership.

---

## 4. Core Responsibilities

The Educational Authority Model is educationally responsible for:

| Responsibility | Meaning |
|----------------|---------|
| **Name authority owners** | Publish the constitutional components that own educational decisions (`AUTHORITY_DOMAINS.md`) |
| **Bind principles** | Enforce single owner, delegation, bounds, preservation, restoration, and explicitness (`AUTHORITY_PRINCIPLES.md`) |
| **Separate ownership from consumption** | Distinguish deciding from reading authorised outputs |
| **Separate ownership from mutation** | Decision ownership ≠ EIP-001 write rights |
| **Separate ownership from orchestration** | Decision ownership ≠ Workflow Engine stage order |
| **Draw hard boundaries** | Forbid reinterpretation, plan rewrite outside authority, evidence redefinition, and domain overclaim (`AUTHORITY_BOUNDARIES.md`) |
| **Require explainability** | Make owner, refusal, preservation, and conflict-prevention speakable (`AUTHORITY_EXPLAINABILITY.md`) |

### 4.1 Binding non-responsibility

The Educational Authority Model must **not**:

- redefine Programme VI educational meaning or coach questions;
- invent workflow stages, transition conditions, or completion criteria;
- grant or invent EIP-001 mutation rights;
- implement conflict-resolution algorithms, ranking, or Runtime A services;
- select Educational Strategy, pack calendars, or mint mastery from ownership labels;
- absorb ownership of Educational Evidence, Estimated Knowledge, or Estimated Mastery under an “authority engine” label;
- treat Version 2 Adaptive / Twin / Mission authorities as replacements for Programme VI educational decision ownership.

---

## 5. Constitutional Components (Authority Domains)

The following components hold educational decision domains under this Model. Detailed owned / consumed / prohibited tables live in `AUTHORITY_DOMAINS.md`.

| Domain owner | Primary educational question |
|--------------|------------------------------|
| **Master Planner** | How should this student’s long-term preparation be designed and published as the Canonical Study Plan? |
| **Daily Coach** | What is most educationally valuable for this student to do *today* under that contract? |
| **Learning Coach** | Is the student genuinely learning over time — and if not, why, and what learning response is warranted? |
| **Recovery Coach** | How should the student recover educationally after meaningful disruption? |
| **Revision Coach** | What previously learned material should be revised now, and why? |
| **Exam Coach** | How should the learner prepare for and approach the examination? |
| **Workflow Engine** | How should constitutional reasonings be sequenced, handed off, and concluded without inventing meaning? |

Supporting authorities that **constrain** decision owners but are not listed as coach domains above:

| Supporting authority | Role relative to decision ownership |
|----------------------|-------------------------------------|
| **Educational Constitution / EIP corpora** | Bound what any owner may claim educationally |
| **Educational Evidence Pipeline** | Owns observational evidence meaning; owners consume, never redefine |
| **Digital Twin (estimate paths)** | Owns Evidence-driven estimates under EIP; owners consume, never author via coaching fiat |
| **Curriculum Engine** | Owns syllabus structure truth; owners traverse, never rewrite syllabus law |
| **State Authority Matrix (EIP-001)** | Owns mutation rights; orthogonal to decision ownership |

---

## 6. Authority vs Related Concepts

| Concept | Owns | Example |
|---------|------|---------|
| **Educational meaning** (Programme VI) | What a coach’s question *means* and how it is reasoned | “Revision ≠ first learning” |
| **Educational decision ownership** (this Model) | Who may *decide* within that meaning | Revision Coach owns revision warrants |
| **Orchestration** (Programme VII WS1) | How owners are *invited and sequenced* | Workflow stage S3 invokes primary authority |
| **State mutation** (EIP-001) | Who may *write* persistent educational states | Mission completion may write Study Progress coverage |
| **Product presentation** (Student Experience) | How outcomes are *shown* | UI shows today’s guidance; does not own it |

Confusing these layers is an architectural defect. Convenience does not merge them.

---

## 7. Integrity Rules

1. **Single owner.** Every educational decision class has exactly one constitutional owner.
2. **Explicit map.** Ownership not listed here is not owned — propose an amendment or refuse.
3. **Consume ≠ own.** Reading an authorised output never transfers the decision.
4. **Delegate ≠ transfer.** Temporary exercise remains under the owner’s warrant and boundaries.
5. **Orchestrate ≠ decide.** The Workflow Engine may select *which owner’s question is live*; it may not answer that question.
6. **Mutate ≠ decide.** Writing Study Progress or Evidence does not grant coaching ownership.
7. **Preserve under pressure.** Performance, UI, or “single tip” product pressure must not collapse domains.
8. **Restore after handoff.** When a temporary primary question ends, decision rights return to the standing owners for their domains.
9. **Refuse overreach.** Components must refuse decisions outside their domain and name the rightful owner.
10. **Explain ownership.** Material outcomes must cite why the deciding component could act and why siblings could not.

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
        │
        ▼
Programme VII / WS2 — Educational Authority Model (this document)
        │  decision ownership map
        │
        ├── Programme VII / WS1 — Workflow Engine …… flow among owners
        │
        ▼
Runtime A / Version 2 adapters / product surfaces
        │  consume ownership; never invent it
```

---

## 9. Relationship to Programme VII Workstream 1

| Concern | Workstream 1 (Workflows) | Workstream 2 (Authority — this Model) |
|---------|--------------------------|----------------------------------------|
| Primary question | How do decisions *flow*? | Who *owns* decisions? |
| Artefacts | Events, stages, objectives, completion | Principles, domains, boundaries, explainability |
| May select primary authority | Yes (orchestration invitation) | Yes (ownership catalogue the invitation must respect) |
| May answer the educational question | No | No — owners answer via Programme VI meaning |
| May redefine coach meaning | No | No |

Workstream 1 without Workstream 2 risks *routing without ownership clarity*.  
Workstream 2 without Workstream 1 risks *ownership without lawful coordination*.  
Both are required; neither replaces Programme VI meaning.

---

## 10. Out of Scope

This Model does **not** include:

- Runtime A, feature flags, or services
- Conflict-resolution algorithms or scoring
- Database models or persistence schemas
- Scheduling / calendar engines
- UI, analytics, or notifications
- Amendments to Programme VI educational meaning corpora
- Changes to EIP-001 permitted writers

Those remain with their respective owners.

---

## 11. Closing

Educational authority is the map that keeps Kwalitec’s tutors from talking over each other.

When a component would decide outside its domain, **refuse and name the owner**.  
When ownership is unclear, **amend this Model** — do not invent authority in code.  
When orchestration needs an owner, **consult this Model**; when it needs a stage path, **consult the Workflow Model**.

> **Authority must be explicit rather than inferred.**
