# API Boundaries

**Programme:** VIII — Workstream 5 — Constitutional Runtime APIs  
**Milestone:** MS001 — Runtime API Model  
**Classification:** Authority limits — what runtime APIs may and must never do  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **Runtime API authority limits**: what runtime APIs may lawfully expose and exchange, and what must remain with the Constitution, EIP, Programme VI, Programme VII, and Programme VIII WS1–WS4.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md)
3. [`RUNTIME_API_MODEL.md`](RUNTIME_API_MODEL.md)
4. [`API_OBJECTIVES.md`](API_OBJECTIVES.md)
5. [`API_TYPES.md`](API_TYPES.md)
6. Programme VI boundary corpora (Master Planner and coaches)
7. Programme VII boundary corpora (workflow, authority, recommendation, state)
8. Programme VIII WS1–WS4 boundary corpora (contracts, evidence, services, interfaces)
9. EIP Evidence, Continuity, Explainability, and Knowledge & Mastery standards

> **Runtime APIs may expose published runtime interfaces,  
> accept authorised constitutional requests,  
> return authorised constitutional responses,  
> and preserve explainability.  
> Runtime APIs must never redefine interface contracts,  
> expose implementation internals,  
> bypass runtime contracts,  
> or modify constitutional specifications.**

---

## 1. Purpose

APIs that silently become a second constitution — rewriting interface meanings in handlers, inventing tips in clients, or skipping contracts because a route was convenient — destroy student trust and educational integrity.

This document draws a bright line between **lawful exposure** (Programme VIII / WS5) and **constitutional authorship** (Constitution / EIP / Programmes VI–VII, with WS1–WS4 binding execution / evidence / service / interface law).

---

## 2. Boundary Principles

1. **Expose, do not author.** APIs surface published interfaces; they do not write law.
2. **Published interfaces only.** Unpublished “helpful” endpoints are hard stops.
3. **Authorised requests only.** Request shapes that invent meaning, tips, evidence classes, or interface semantics are refused.
4. **Authorised responses only.** Response shapes that invent dispositions or artefacts are defective.
5. **No interface redefinition.** RI-01…RI-07 meanings remain with the Runtime Interface Model.
6. **No service redefinition.** RS-01…RS-07 responsibilities remain with the Runtime Service Model.
7. **No internals as law.** Stack traces, private schemas, adapter paths, and wire formats are never constitutional producers.
8. **No contract bypass.** RC-01…RC-07 remain binding regardless of transport convenience.
9. **No evidence alteration.** Classifications stay with the Evidence Model / WS2 law.
10. **No specification mutation.** Code and protocols never amend constitutional corpora by side effect.
11. **No authority or policy invention.** APIs never define educational meaning, constitutional authority, runtime policy, or transport protocols.
12. **Explain the stop.** Students and developers should hear when an exposure must refuse.
13. **Technology neutrality.** Protocol choice never expands constitutional power.
14. **No emergency exemption.** Load, deadlines, and demos never mint constitutional exposure rights.

---

## 3. What Runtime APIs May Do (Lawful)

| Lawful action | Constitutional meaning |
|---------------|------------------------|
| **Expose published runtime interfaces** | Surface RA-mapped RI-01…RI-07 contracts already published under WS4 |
| **Accept authorised constitutional requests** | Consume request shapes that cite published interfaces, contracts, evidence, events, or service responsibilities |
| **Return authorised constitutional responses** | Emit only published dispositions, artefacts, audit trails, or diagnostic records |
| **Preserve explainability** | Answer API / interface / request / response / boundaries without rewriting meaning |
| **Refuse unlawfully requested acts** | Prefer honest stop / defer / escalate over improvisation |
| **Compose recognised APIs** | Bind multiple RA types when law requires cross-cutting exposure |
| **Remain technology neutral** | Honour RA meanings over any compliant transport (RAO-06) |
| **Preserve audit records** | Retain reconstructable RA-06 trails for material interactions |

These actions **expose and exchange**. They do **not** publish a new Constitution, invent coach questions, mint tips, author ownership maps, redefine interfaces, or define runtime policy.

---

## 4. What Runtime APIs Must NEVER Do

| Forbidden action | Why | Lawful alternative |
|------------------|-----|--------------------|
| **Redefine interface contracts** | Programme VIII WS4 owns RI-01…RI-07 interaction meanings | Expose published RI contracts as-is; escalate for corpus amendment |
| **Redefine runtime services** | Programme VIII WS3 owns RS-01…RS-07 responsibilities | Expose published capabilities through bound interfaces only |
| **Expose implementation internals as constitutional law** | Internals are delivery details, not educational truth | Keep ops breadcrumbs optional and subordinate to constitutional citations |
| **Bypass runtime contracts** | Programme VIII WS1 owns RC-01…RC-07 authorisation | Require named contract bindings via RA-01 / RI-01 before material execution exposure |
| **Alter constitutional evidence** | EIP-002 / WS2 / EIP-001 writers own observational truth | Expose evidence as published via RA-02 / RI-02; leave writers to permitted paths |
| **Modify constitutional specifications** | Constitution / EIP / Programmes VI–VIII are amended only under their governance | Change transport bindings to obey law, or propose a corpus amendment — never patch law in an API |
| **Create educational meaning** | Programme VI owns coach / planner questions and envelopes | Expose only published meaning artefacts; escalate for corpus amendment |
| **Establish constitutional authority** | Ownership and governance live upstream of WS5 | Remain an exposure contract; refuse authority invention |
| **Define runtime policy** | Execution / collaboration / composition policy lives in WS1–WS4 | Expose published dispositions; never invent when law may be skipped |
| **Invent recommendations / state / event classes** | Programme VII + WS1 event law own those artefacts | Surface only already-authorised artefacts or none |
| **Elevate REST / GraphQL / gRPC / HTTP / OpenAPI into architecture law** | Technology neutrality (RAO-06) | Treat them as replaceable delivery mechanisms |
| **Mint mastery / readiness from API convenience** | Knowledge & Mastery and Evidence authorities own estimates | Preserve claim ladder; refuse overclaim |
| **Erase educational history** | EIP-005 Continuity | Preserve lawful history across retries and replacements |
| **Treat Twin / Adaptive / UI as constitutional authors** | They are consumers / delivery surfaces | Keep them subordinate to Runtime API + upstream corpora |
| **Present scores as constitutional warrant** | Scores are operational proxies | Cite published corpora, interfaces, and evidence classes |

---

## 5. Authority Map

| Concern | Owner | API role |
|---------|-------|----------|
| Educational truth / integrity | Constitution + EIP | Expose / obey — never author |
| Educational meaning | Programme VI | Expose published artefacts only |
| Workflow orchestration | Programme VII WS1 | Expose via RA-05 / RI-05 under published flows |
| Decision ownership / conflict | Programme VII WS2 | Preserve ownership; never absorb |
| Recommendations | Programme VII WS3 + VI owners | Expose lawful artefacts only (RA-05 / RI-05) |
| Educational context (EST/CST) | Programme VII WS4 | Expose published postures only (RA-05 / RI-05) |
| Evidence classification & writers | EIP-002 / EIP-001 / WS2 | Expose / consume as published (RA-02 / RI-02) |
| Runtime contracts / events / completion | Programme VIII WS1 | Gate exposure (RA-01 / RA-03 / RA-05) |
| Runtime services / collaboration | Programme VIII WS3 | Expose catalogue capabilities via RA-04 / RI-04 |
| Runtime interaction contracts | Programme VIII WS4 | Expose published RI contracts — never redefine |
| Runtime exposure contracts | Programme VIII / this corpus | Bind / enforce (RA-01…RA-07) |
| Product UX / Adaptive / Twin delivery | Architecture / Version 2 surfaces | Downstream consumers only |
| Transports / OpenAPI / auth stacks | Engineering delivery | Never constitutional producers |

---

## 6. Boundary Checks (Pre-Exposure)

Before a material constitutional API interaction, lawful exposure requires affirmative answers:

| Check | Question |
|-------|----------|
| **ABC-01 API** | Which RA-01…RA-07 API(s) bind this interaction? |
| **ABC-02 Interface** | Which published RI-01…RI-07 interface(s) are being exposed (without redefinition)? |
| **ABC-03 Request** | Is the request an authorised constitutional request shape (not an invention)? |
| **ABC-04 Response** | Will the response be an authorised constitutional artefact only? |
| **ABC-05 Contracts** | If execution is involved, are RC bindings preserved (no bypass)? |
| **ABC-06 Evidence** | If evidence is involved, are classifications preserved (no alteration)? |
| **ABC-07 Internals** | Does this interaction avoid elevating implementation internals into law? |
| **ABC-08 Spec immutability** | Does this interaction avoid modifying constitutional specifications? |
| **ABC-09 Authority / policy non-invention** | Does this interaction avoid establishing constitutional authority or defining runtime policy? |
| **ABC-10 Audit / explainability** | Will RA-06 / explainability records preserve API, interface, request, response, and boundaries? |

Any failed check → refuse / defer / escalate. Do not “best-effort” invent law at the exposure boundary.

---

## 7. Relationship to Sibling Boundaries

| Sibling corpus | Relationship |
|----------------|--------------|
| Programme VI `*_BOUNDARIES.md` | APIs must not cross coach / planner boundaries while exposing |
| Programme VII workflow / authority / recommendation / state boundaries | RA-05 / RI-05 specialises exposure of those limits |
| Programme VIII `CONTRACT_BOUNDARIES.md` | RA-01 / RI-01 specialises exposure without bypass |
| Programme VIII evidence boundaries | RA-02 / RI-02 specialises exposure without alteration |
| Programme VIII `SERVICE_BOUNDARIES.md` | RA-04 / RA-05 expose RS capabilities without redistributing them |
| Programme VIII `INTERFACE_BOUNDARIES.md` | RA catalogue must honour RI boundaries; never redefine them |
| EIP-001 State Authority Matrix | Mutation rights remain orthogonal; APIs never gain them by endpoint shape |

This document does not replace sibling boundaries. It binds **constitutional API exposure** so those boundaries survive any transport or OpenAPI document.

---

## 8. Closing Statement

> **Runtime APIs are powerful only as faithful exposure contracts.  
> The moment they redefine interfaces, bypass contracts, expose internals as law, establish constitutional authority, or modify specifications, they have left constitutional education and entered product fiction.**
