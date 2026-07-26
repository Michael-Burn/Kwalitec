# Event Boundaries

**Programme:** VIII — Workstream 1 — Constitutional Runtime Contracts  
**Milestone:** MS002 — Constitutional Event Processing Model  
**Classification:** Authority limits — what runtime may and must never do when processing constitutional events  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **Constitutional Event Processing authority limits**: what runtime implementations may lawfully do when receiving, evaluating, and executing events, and what must remain with the Constitution, EIP, Programme VI, Programme VII, and Programme VIII MS001 contracts.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md)
3. [`CONSTITUTIONAL_EVENT_PROCESSING_MODEL.md`](CONSTITUTIONAL_EVENT_PROCESSING_MODEL.md)
4. [`EVENT_OBJECTIVES.md`](EVENT_OBJECTIVES.md)
5. [`EVENT_TYPES.md`](EVENT_TYPES.md)
6. [`../contracts/CONTRACT_BOUNDARIES.md`](../contracts/CONTRACT_BOUNDARIES.md)
7. Programme VI boundary corpora (Master Planner and coaches)
8. Programme VII boundary corpora (workflow, authority, recommendation, state)
9. EIP Evidence, Continuity, Explainability, and Knowledge & Mastery standards

> **Runtime may receive published constitutional events,  
> validate published contracts,  
> invoke published execution paths,  
> and produce published execution records.  
> Runtime must never invent new constitutional event types,  
> reinterpret educational meaning,  
> transfer authority,  
> bypass constitutional workflows,  
> or generate unpublished recommendations.**

---

## 1. Purpose

Runtime that silently becomes a second constitution — inventing event types in handlers, reinterpreting educational meaning because a payload looked suggestive, transferring ownership by queue name, bypassing workflows for “already handled” flags, or minting tips from unpublished notifications — destroys student trust and educational integrity.

This document draws a bright line between **lawful event processing** (Programme VIII / MS002) and **constitutional authorship** (Constitution / EIP / Programmes VI–VII).

---

## 2. Boundary Principles

1. **Execute, do not author.** Event processing applies published behaviour; it does not create it.
2. **Published events only.** Unpublished customs and infrastructure signals without CE mapping are hard stops.
3. **Published contracts only.** Processing without RC binding is unlawful execution.
4. **Published paths only.** Handler shortcuts are not educational optimisation.
5. **Published records only.** Execution records are constitutional artefacts, not free-form logs as law.
6. **Meaning non-reinterpretation.** Programme VI questions survive handlers intact.
7. **Authority non-transfer.** Ownership stays with the Authority Model.
8. **Workflow non-bypass.** Stage skipping via events is still stage skipping.
9. **Recommendation non-invention.** Tips stay with WS3 + Programme VI owners.
10. **Evidence non-reinterpretation.** Classifications stay with the Evidence Model.
11. **State non-invention.** Context postures stay with WS4 EST/CST law.
12. **Order preservation.** Published succession is not optional under load.
13. **Determinism.** Race-dependent educational disposition is a defect.
14. **Explain the stop.** Students and developers should hear when processing must refuse.
15. **No emergency exemption.** Load, deadlines, and demos never mint constitutional event power.

---

## 3. What Runtime May Do (Lawful)

| Lawful action | Constitutional meaning |
|---------------|------------------------|
| **Receive published constitutional events** | Accept only CE-01…CE-07 instances with identifiable published producers |
| **Validate published contracts** | Bind and check RC-01…RC-07 (and upstream conditions) before execution |
| **Invoke published execution paths** | Perform only actions already authorised by Constitution / EIP / Programmes VI–VII under MS001 |
| **Produce published execution records** | Emit RC-07 / CE-06 reconstructable trails and published output classes |
| **Refuse unlawfully requested processing** | Prefer honest stop / defer / escalate over improvisation |
| **Preserve execution order** | Honour published succession, conflict disposition, and continuity |
| **Remain deterministic** | Same published inputs → same disposition |
| **Remain replaceable** | Honour event law in any compliant implementation |
| **Explain processing** | Answer event / contract / artefacts / outputs / boundaries without rewriting meaning |

These actions **process**. They do **not** publish a new Constitution, invent coach questions, mint tips, author ownership maps, or invent CE types.

---

## 4. What Runtime Must NEVER Do

| Forbidden action | Why | Lawful alternative |
|------------------|-----|--------------------|
| **Invent new constitutional event types** | CE catalogue is closed; invention is law invention | Refuse unpublished signals; propose Programme VIII amendment |
| **Reinterpret educational meaning** | Programme VI owns coach / planner questions and envelopes | Consume published meaning; escalate for corpus amendment |
| **Transfer authority** | Programme VII WS2 owns ownership, permission, and conflict disposition | Apply Authority / Conflict corpora; refuse domain absorption |
| **Bypass constitutional workflows** | Programme VII WS1 owns orchestration | Require published events, stages, transitions, and completion |
| **Generate unpublished recommendations** | Programme VII WS3 + Programme VI owners own tip warrant | Surface lawful artefacts or no-recommendation |
| **Invent educational state** | Programme VII WS4 owns EST/CST context law | Apply published postures / transitions only |
| **Reinterpret constitutional evidence** | EIP-002 / EIP-006 / EIP-001 writers own observational truth and claim honesty | Consume classifications; leave writers to permitted paths |
| **Modify constitutional specifications** | Constitution / EIP / Programmes VI–VIII are amended only under their governance | Change code to obey law, or propose a corpus amendment — never patch law in a handler |
| **Reorder educational succession for convenience** | EPO-02 / EIP-005 | Preserve published order; disposition concurrency under WS2 |
| **Treat Twin / Adaptive / UI / broker noise as CE publishers** | They are consumers / delivery surfaces | Require published CE mapping or refuse |
| **Present scores / acks / latency as constitutional warrant** | Operational proxies are not event law | Cite published corpora, CE, and RC |
| **Become irreplaceable by event topology** | RCO-06 / CE-07 replaceability | Keep event law implementation-independent |

---

## 5. Authority Map

| Concern | Owner | Runtime event-processing role |
|---------|-------|-------------------------------|
| Educational truth / integrity | Constitution + EIP | Consume / obey |
| Educational meaning | Programme VI | Consume / never reinterpret via handlers |
| Workflow orchestration & WE-xx stimuli | Programme VII WS1 | Process under CE-02 / RC-03 |
| Decision ownership / conflict | Programme VII WS2 | Process under CE-03 / RC-04 |
| Recommendations | Programme VII WS3 + VI owners | Process under CE-04 / RC-05 |
| Educational context (EST/CST) | Programme VII WS4 | Process under CE-05 / RC-06 |
| Evidence classification & writers | EIP-002 / EIP-001 | Process under CE-01 / RC-02 |
| Runtime execution contracts | Programme VIII / MS001 | Validate / bind RC-01…RC-07 |
| Constitutional event processing rules | Programme VIII / this corpus | Bind / enforce CE-01…CE-07 |
| Product UX / Adaptive / Twin / brokers | Architecture / Version 2 / infra | Downstream delivery only — never CE authors |

---

## 6. Boundary Checks (Pre-Processing)

Before a material constitutional event is executed, processing requires affirmative answers:

| Check | Question |
|-------|----------|
| **EB-01 Event class** | Is this a published CE-01…CE-07 category (not an unpublished custom)? |
| **EB-02 Producer** | Which published corpus authored the event meaning / stimulus? |
| **EB-03 Contract** | Which RC-01…RC-07 contract(s) authorise processing? |
| **EB-04 Meaning** | Does processing avoid reinterpreting Programme VI educational meaning? |
| **EB-05 Authority** | Does processing avoid transferring ownership / inventing permission? |
| **EB-06 Workflow** | If orchestration is involved, is WS1 law followed without bypass? |
| **EB-07 Tip honesty** | If guidance would be surfaced, is it a lawful recommendation (not unpublished)? |
| **EB-08 State honesty** | If context is represented, is it a published EST/CST posture? |
| **EB-09 Evidence honesty** | Does processing avoid reinterpreting Evidence classifications? |
| **EB-10 Order / determinism** | Is published succession preserved; is disposition reproducible from published inputs? |
| **EB-11 Spec immutability** | Does processing avoid modifying constitutional specifications? |
| **EB-12 Audit** | Will published execution records preserve event, contract, artefacts, outputs, and boundaries? |

Any failed check → refuse / defer / escalate. Do not “best-effort” invent event law.

---

## 7. Relationship to Sibling Boundaries

| Sibling corpus | Relationship |
|----------------|--------------|
| [`../contracts/CONTRACT_BOUNDARIES.md`](../contracts/CONTRACT_BOUNDARIES.md) | MS002 specialises those limits for the event-processing horizon |
| Programme VI `*_BOUNDARIES.md` | Handlers must not cross coach / planner boundaries while processing |
| Programme VII `WORKFLOW_BOUNDARIES.md` | CE-02 specialises processing under those limits |
| Programme VII `AUTHORITY_BOUNDARIES.md` | CE-03 specialises processing under those limits |
| Programme VII `RECOMMENDATION_BOUNDARIES.md` | CE-04 specialises processing under those limits |
| Programme VII state / transition boundaries | CE-05 specialises processing under those limits |
| EIP-001 State Authority Matrix | Mutation rights remain orthogonal; events never grant them by arrival |

This document does not replace sibling boundaries. It binds **event processing** so those boundaries survive queues, handlers, and replacements.

---

## 8. Closing Statement

> **Runtime event processing is powerful only as a faithful executor of published events.  
> The moment it invents event types, reinterprets meaning, transfers authority, bypasses workflows, or mints unpublished tips, it has left constitutional education and entered product fiction.**
