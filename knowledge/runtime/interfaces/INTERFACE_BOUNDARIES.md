# Interface Boundaries

**Programme:** VIII — Workstream 4 — Constitutional Runtime Interfaces  
**Milestone:** MS001 — Runtime Interface Model  
**Classification:** Authority limits — what runtime interfaces may and must never do  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **Runtime Interface authority limits**: what runtime interfaces may lawfully expose and exchange, and what must remain with the Constitution, EIP, Programme VI, Programme VII, and Programme VIII WS1–WS3.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md)
3. [`RUNTIME_INTERFACE_MODEL.md`](RUNTIME_INTERFACE_MODEL.md)
4. [`INTERFACE_OBJECTIVES.md`](INTERFACE_OBJECTIVES.md)
5. [`INTERFACE_TYPES.md`](INTERFACE_TYPES.md)
6. Programme VI boundary corpora (Master Planner and coaches)
7. Programme VII boundary corpora (workflow, authority, recommendation, state)
8. Programme VIII WS1–WS3 boundary corpora (contracts, evidence, services)
9. EIP Evidence, Continuity, Explainability, and Knowledge & Mastery standards

> **Runtime interfaces may expose published constitutional capabilities,  
> accept authorised constitutional inputs,  
> return authorised constitutional outputs,  
> and preserve explainability.  
> Runtime interfaces must never expose implementation internals,  
> redefine constitutional meaning,  
> bypass runtime contracts,  
> alter constitutional evidence,  
> or modify constitutional specifications.**

---

## 1. Purpose

Interfaces that silently become a second constitution — rewriting meaning in request handlers, inventing tips in SDK clients, or skipping contracts because a route was convenient — destroy student trust and educational integrity.

This document draws a bright line between **lawful interaction** (Programme VIII / WS4) and **constitutional authorship** (Constitution / EIP / Programmes VI–VII, with WS1–WS3 binding execution / evidence / service law).

---

## 2. Boundary Principles

1. **Expose, do not author.** Interfaces surface published capabilities; they do not write law.
2. **Published capabilities only.** Unpublished “helpful” endpoints are hard stops.
3. **Authorised inputs only.** Request shapes that invent meaning, tips, or evidence classes are refused.
4. **Authorised outputs only.** Response shapes that invent dispositions or artefacts are defective.
5. **No internals as law.** Stack traces, private schemas, adapter paths, and wire formats are never constitutional producers.
6. **No contract bypass.** RC-01…RC-07 remain binding regardless of transport convenience.
7. **No evidence alteration.** Classifications stay with the Evidence Model / WS2 law.
8. **No specification mutation.** Code and protocols never amend constitutional corpora by side effect.
9. **No policy invention.** Interfaces never define educational meaning, authority, governance, or execution policy.
10. **Explain the stop.** Students and developers should hear when an interaction must refuse.
11. **Technology neutrality.** Protocol choice never expands constitutional power.
12. **No emergency exemption.** Load, deadlines, and demos never mint constitutional exposure rights.

---

## 3. What Runtime Interfaces May Do (Lawful)

| Lawful action | Constitutional meaning |
|---------------|------------------------|
| **Expose published constitutional capabilities** | Surface RI-mapped RS / WS1 / WS2 capabilities already published |
| **Accept authorised constitutional inputs** | Consume request shapes that cite published contracts, evidence, events, or service responsibilities |
| **Return authorised constitutional outputs** | Emit only published dispositions, artefacts, audit trails, or diagnostic records |
| **Preserve explainability** | Answer interface / capability / inputs / outputs / boundaries without rewriting meaning |
| **Refuse unlawfully requested acts** | Prefer honest stop / defer / escalate over improvisation |
| **Compose recognised interfaces** | Bind multiple RI types when law requires cross-cutting exposure |
| **Remain technology neutral** | Honour RI meanings over any compliant transport (RIO-06) |
| **Preserve audit records** | Retain reconstructable RI-06 trails for material interactions |

These actions **expose and exchange**. They do **not** publish a new Constitution, invent coach questions, mint tips, author ownership maps, or define execution policy.

---

## 4. What Runtime Interfaces Must NEVER Do

| Forbidden action | Why | Lawful alternative |
|------------------|-----|--------------------|
| **Expose implementation internals as constitutional law** | Internals are delivery details, not educational truth | Keep ops breadcrumbs optional and subordinate to constitutional citations |
| **Redefine constitutional meaning** | Programme VI owns coach / planner questions and envelopes | Expose only published meaning artefacts; escalate for corpus amendment |
| **Bypass runtime contracts** | Programme VIII WS1 owns RC-01…RC-07 authorisation | Require named contract bindings via RI-01 before material execution exposure |
| **Alter constitutional evidence** | EIP-002 / WS2 / EIP-001 writers own observational truth | Expose evidence as published via RI-02; leave writers to permitted paths |
| **Modify constitutional specifications** | Constitution / EIP / Programmes VI–VIII are amended only under their governance | Change transport bindings to obey law, or propose a corpus amendment — never patch law in an interface |
| **Invent recommendations / state / event classes** | Programme VII + WS1 event law own those artefacts | Surface only already-authorised artefacts or none |
| **Define educational meaning, authority, governance, or execution policy** | Those belong upstream of WS4 | Remain an interaction contract; refuse policy invention |
| **Elevate REST / GraphQL / gRPC / HTTP / WebSockets / SDKs into architecture law** | Technology neutrality (RIO-06) | Treat them as replaceable delivery mechanisms |
| **Mint mastery / readiness from interface convenience** | Knowledge & Mastery and Evidence authorities own estimates | Preserve claim ladder; refuse overclaim |
| **Erase educational history** | EIP-005 Continuity | Preserve lawful history across retries and replacements |
| **Treat Twin / Adaptive / UI as constitutional authors** | They are consumers / delivery surfaces | Keep them subordinate to Runtime Interface + upstream corpora |
| **Present scores as constitutional warrant** | Scores are operational proxies | Cite published corpora and evidence classes |

---

## 5. Authority Map

| Concern | Owner | Interface role |
|---------|-------|----------------|
| Educational truth / integrity | Constitution + EIP | Expose / obey — never author |
| Educational meaning | Programme VI | Expose published artefacts only |
| Workflow orchestration | Programme VII WS1 | Expose via RI-05 under published flows |
| Decision ownership / conflict | Programme VII WS2 | Preserve ownership; never absorb |
| Recommendations | Programme VII WS3 + VI owners | Expose lawful artefacts only (RI-05) |
| Educational context (EST/CST) | Programme VII WS4 | Expose published postures only (RI-05) |
| Evidence classification & writers | EIP-002 / EIP-001 / WS2 | Expose / consume as published (RI-02) |
| Runtime contracts / events / completion | Programme VIII WS1 | Gate exposure (RI-01 / RI-03 / RI-05) |
| Runtime services / collaboration | Programme VIII WS3 | Expose catalogue capabilities (RI-04) |
| Runtime interaction contracts | Programme VIII / this corpus | Bind / enforce (RI-01…RI-07) |
| Product UX / Adaptive / Twin delivery | Architecture / Version 2 surfaces | Downstream consumers only |
| Transports / SDKs / auth stacks | Engineering delivery | Never constitutional producers |

---

## 6. Boundary Checks (Pre-Interaction)

Before a material constitutional interface interaction, lawful exposure requires affirmative answers:

| Check | Question |
|-------|----------|
| **IBC-01 Interface** | Which RI-01…RI-07 interface(s) bind this interaction? |
| **IBC-02 Capability** | Which published constitutional capability is being exposed? |
| **IBC-03 Inputs** | Are inputs authorised constitutional request shapes (not inventions)? |
| **IBC-04 Outputs** | Will outputs be authorised constitutional artefacts only? |
| **IBC-05 Contracts** | If execution is involved, are RC bindings preserved (no bypass)? |
| **IBC-06 Evidence** | If evidence is involved, are classifications preserved (no alteration)? |
| **IBC-07 Internals** | Does this interaction avoid elevating implementation internals into law? |
| **IBC-08 Spec immutability** | Does this interaction avoid modifying constitutional specifications? |
| **IBC-09 Policy non-invention** | Does this interaction avoid defining meaning, authority, governance, or execution policy? |
| **IBC-10 Audit / explainability** | Will RI-06 / explainability records preserve interface, capability, inputs, outputs, and boundaries? |

Any failed check → refuse / defer / escalate. Do not “best-effort” invent law at the boundary.

---

## 7. Relationship to Sibling Boundaries

| Sibling corpus | Relationship |
|----------------|--------------|
| Programme VI `*_BOUNDARIES.md` | Interfaces must not cross coach / planner boundaries while exposing |
| Programme VII workflow / authority / recommendation / state boundaries | RI-05 specialises exposure of those limits |
| Programme VIII `CONTRACT_BOUNDARIES.md` | RI-01 specialises exposure without bypass |
| Programme VIII evidence boundaries | RI-02 specialises exposure without alteration |
| Programme VIII `SERVICE_BOUNDARIES.md` | RI-04 / RI-05 expose RS capabilities without redistributing them |
| EIP-001 State Authority Matrix | Mutation rights remain orthogonal; interfaces never gain them by endpoint shape |

This document does not replace sibling boundaries. It binds **constitutional interaction** so those boundaries survive any transport or SDK.

---

## 8. Closing Statement

> **Runtime interfaces are powerful only as faithful interaction contracts.  
> The moment they author meaning, bypass contracts, alter evidence, expose internals as law, or modify specifications, they have left constitutional education and entered product fiction.**
