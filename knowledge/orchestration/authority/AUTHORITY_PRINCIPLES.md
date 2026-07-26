# Authority Principles

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS001 — Educational Authority Model  
**Classification:** Binding constitutional principles for educational decision ownership  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional principles** governing educational authority in Kwalitec.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`EDUCATIONAL_AUTHORITY_MODEL.md`](EDUCATIONAL_AUTHORITY_MODEL.md)
3. Programme VI meaning corpora for each named owner
4. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md) — orchestration must respect these principles
5. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) — mutation principles remain separate

> **Authority must be explicit rather than inferred.**

---

## 1. Purpose

Principles prevent ownership from dissolving into convenience. Without them, Daily Coach absorbs Master Planner, Workflow Engine invents tips, and Revision Coach quietly becomes Recovery.

These principles bind every educational decision path — documentation, design, and future Runtime A behaviour.

---

## 2. Principle Catalogue

| ID | Principle | One-line rule |
|----|-----------|---------------|
| **AP-01** | Single owner | Each educational decision class has exactly one constitutional owner |
| **AP-02** | Explicit authority | Ownership is published; silence is not ownership |
| **AP-03** | Domain boundedness | Owners decide only within their published domain |
| **AP-04** | Delegated authority | Temporary exercise is allowed; ownership does not transfer |
| **AP-05** | Consumed authority | Reading authorised outputs never creates a parallel owner |
| **AP-06** | Authority preservation | Coordination and consumption must not erase the owner |
| **AP-07** | Authority restoration | Temporary handoff / suspension returns rights to the owner |
| **AP-08** | Refusal duty | Components must refuse out-of-domain decisions and name the owner |
| **AP-09** | Non-reinterpretation | No owner may redefine another owner’s educational meaning |
| **AP-10** | Separation of layers | Decision ownership ≠ orchestration ≠ state mutation ≠ presentation |

---

## 3. AP-01 — Single Owner for Each Educational Decision

**Rule:** Every educational decision class has exactly one Owner.

| Lawful | Unlawful |
|--------|----------|
| Daily Coach owns today’s primary educational priority | Daily Coach and Revision Coach both “own” today’s tip with equal final say |
| Master Planner owns Canonical Study Plan publication | Workflow Engine co-publishes the plan “for orchestration” |
| Learning Coach owns progression / obstacle / intervention meaning | Session adaptation invents a new long-term progression owner |

**Conflict prevention:** Competing claims are resolved by consulting the domain map (`AUTHORITY_DOMAINS.md`), not by merging meanings or inventing a third “meta-coach.”

**Note:** Multiple components may *contribute inputs*. Only one owns the *decision*.

---

## 4. AP-02 — Explicit Authority

**Rule:** Authority that is not named in this corpus (or in a Programme VI model that this corpus catalogues) does not exist for educational decision-making.

| Lawful | Unlawful |
|--------|----------|
| Amend `AUTHORITY_DOMAINS.md` before claiming a new decision class | Infer ownership because a service sits next to the mission UI |
| Cite the owner in explainability traces | Assume “the adaptive engine” owns Programme VI coaching questions by Version 2 proximity |
| Document temporary delegation explicitly | Rely on tribal knowledge that “recovery usually wins” |

**Explicitness tests:**

1. Can a developer name the owner from this corpus without reading implementation code?
2. Can a student-facing explanation name *why this component* decided without inventing a new owner?
3. If the answer is “probably X,” ownership is not yet constitutional — amend or refuse.

---

## 5. AP-03 — Bounded Authority

**Rule:** Every owner’s authority is limited to its domain’s owned decisions. Bounds are constitutional, not discretionary.

| Lawful | Unlawful |
|--------|----------|
| Recovery Coach decides restorative posture after disruption | Recovery Coach rewrites Educational Strategy as if it were Master Planner |
| Exam Coach decides examination-preparation warrant and priorities | Exam Coach redefines Estimated Mastery from mock proximity alone |
| Workflow Engine sequences owners | Workflow Engine answers “what should I revise?” |

Bounded authority implies:

- **hard prohibited lists** per domain (`AUTHORITY_DOMAINS.md`);
- **no emergency override** that invents ownership under time pressure;
- **escalation** to the rightful owner when the living question leaves the current domain.

---

## 6. AP-04 — Delegated Authority

**Rule:** An owner may authorise another component to exercise a *narrow* decision under the owner’s warrant. Delegation is temporary, scoped, and revocable. Ownership remains with the delegator.

| Example | Owner | Delegate | Bound |
|---------|-------|----------|-------|
| Local session phase adaptation within today’s objective | Daily Coach | Learning Session Model | May not invent a new Daily Coach job |
| Day emphasis informed by revision warrant | Daily Coach (day priority) | Revision Coach (revision meaning) | Revision informs; does not commandeer day authority |
| Workflow invitation of primary authority | Workflow Engine (orchestration) | Invoked Programme VI owner (decision) | Engine invites; owner decides |

**Delegation invariants:**

1. Delegator remains accountable for the decision class.
2. Delegate may not expand scope beyond the warrant.
3. Delegate may not redelegate educational ownership to a third component without the owner’s published pathway.
4. Explainability must name owner and delegate when both are material.

**Delegation is not:** silent absorption, permanent transfer, or a licence to redefine the owner’s meaning.

---

## 7. AP-05 — Consumed Authority (Inputs Without Ownership)

**Rule:** Components may consume other owners’ authorised outputs as *inputs*. Consumption never creates co-ownership of the consumed decision.

| Consumer | May consume | Must not treat as own decision |
|----------|-------------|--------------------------------|
| Daily Coach | Canonical Study Plan, Profile, Learning / Recovery / Revision / Exam meanings | Plan redesign; Twin mutation; Evidence redefinition |
| Revision Coach | Learning Coach evidence meaning, Daily Coach day context, Recovery posture | Day-priority ownership; disruption restoration ownership |
| Workflow Engine | All Programme VI artefacts as coordination inputs | Any Programme VI educational answer |
| Product UI | Authorised outcomes for display | Educational decision ownership |

**Consume-and-respect:** If an input contradicts the consumer’s proposed action, the consumer must refuse, escalate, or adapt *within its own domain* — not overwrite the input’s owner.

---

## 8. AP-06 — Authority Preservation

**Rule:** While other components coordinate, consume, present, or temporarily hold primary focus, the standing owner of each decision class remains that owner.

Preservation fails when:

- orchestration emits an independent educational tip;
- a sibling coach rewrites another’s meaning “to keep the story simple”;
- UI or analytics invent a competing “recommended next” without citing the owner;
- plan cells are edited “just for today” without Master Planner / Scheduling pathways;
- Evidence or Mastery is relabelled under a coach brand.

Preservation succeeds when:

- handoffs name the new *primary question* without renaming owners;
- temporary primary focus (e.g. recovery) suspends *competing primary actions*, not ownership of other domains;
- explainability states which owner decided and which boundaries held.

---

## 9. AP-07 — Authority Restoration

**Rule:** After temporary delegation, primary-question suspension, or orchestration handoff, decision rights for each class return to their constitutional owners without residual dual ownership.

| Situation | Restoration |
|-----------|-------------|
| Session local adaptation ends | Decision rights for *today’s objective* remain with Daily Coach; session does not keep a parallel day-priority owner |
| Recovery completion / transition | Restorative primary question ends per Recovery Completion Model; Daily Coach / Learning Coach resume ordinary primary questions under the plan |
| Workflow conclude | Orchestration closes; Programme VI owners remain owners of their domains |
| Escalation to Master Planner completes | Structural decision returns via published plan pathways; coaches resume consuming the updated contract |

**Restoration must not:**

- leave a second “shadow owner” in product state;
- erase educational history (EIP-005 Continuity);
- invent a new owner during the return path.

---

## 10. AP-08 — Refusal Duty

**Rule:** A component asked to decide outside its domain must refuse, name the rightful owner, and — when orchestration is involved — hand off or escalate rather than invent an answer.

Refusal is a first-class educational outcome, not a failure mode.

| Asked of | Outside domain example | Lawful response |
|----------|------------------------|-----------------|
| Daily Coach | Redesign long-term strategy | Refuse; escalate Master Planner pathways |
| Revision Coach | Restore after disruption | Refuse; Recovery Coach |
| Workflow Engine | “What should I study today?” | Invite Daily Coach; do not answer |
| Exam Coach | First-pass learning of unlearned material | Refuse; Learning / Daily first learning |

---

## 11. AP-09 — Non-Reinterpretation

**Rule:** No component may reinterpret another component’s educational meaning to make its own decision easier.

| Forbidden reinterpretation | Why |
|----------------------------|-----|
| Coverage completion as understanding | EIP-006 / Evidence / Learning Coach meaning |
| Session finish as mastery | Evidence / Twin authorities |
| Workflow completion as educational success | Programme VII WS1 Completion Model — orchestration fulfilment ≠ learning |
| Calendar proximity as exam readiness | Exam Coach warrant rules |
| Missed days as automatic recovery theatre | Recovery Coach trigger / boundary rules |

Owners may *consume* sibling meanings as classified. They may not *re-author* those meanings.

---

## 12. AP-10 — Separation of Layers

**Rule:** The following must remain distinct:

```
Meaning (Programme VI)
   ≠  Decision ownership (this Model)
   ≠  Orchestration flow (Programme VII WS1)
   ≠  State mutation (EIP-001)
   ≠  Presentation (Student Experience / UI)
```

A design that collapses two layers for “simplicity” is unconstitutional unless the governing documents are amended first.

---

## 13. Application Checklist

Before any educational decision path ships (documentation or code):

1. **Name the decision class** in plain educational language.
2. **Name the single owner** from `AUTHORITY_DOMAINS.md`.
3. **Confirm the decision is owned, not prohibited**, for that owner.
4. **List consumed inputs** and their owners — no silent redefinition.
5. **State any delegation** with scope and restoration condition.
6. **Confirm orchestration** (if any) invites rather than answers.
7. **Confirm mutation** (if any) is permitted under EIP-001 — separately.
8. **Attach explainability** per `AUTHORITY_EXPLAINABILITY.md`.

If any step fails, **stop**. Amend the corpus or refuse the behaviour.

---

## 14. Closing

These principles are not aspirational. They are the constitutional filters that keep educational authority from becoming folklore.

> **Single owner. Explicit map. Bounded domain. Honest delegation. Preserved and restored ownership.**
