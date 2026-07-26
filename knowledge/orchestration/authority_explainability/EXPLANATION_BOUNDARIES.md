# Explanation Boundaries

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS003 — Authority Decision Explainability  
**Classification:** Hard limits on what authority explanations may and must not do  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **constitutional boundaries** for authority decision explanations.

Subordinate to:

1. [`AUTHORITY_DECISION_EXPLAINABILITY.md`](AUTHORITY_DECISION_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md)
4. [`../authority/AUTHORITY_BOUNDARIES.md`](../authority/AUTHORITY_BOUNDARIES.md)
5. [`../conflict_resolution/RESOLUTION_PRINCIPLES.md`](../conflict_resolution/RESOLUTION_PRINCIPLES.md)
6. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
7. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md)

> **Authority explanations may describe constitutional reasoning.  
> They must never invent ownership, meaning, or unpublished law.**

---

## 1. Purpose

Boundaries prevent explanation from becoming a back door: narration that quietly transfers ownership, rewrites evidence, invents a meta-coach, or exposes runtime guts as if they were educational law.

These boundaries bind every authority explanation path. Crossing them makes the narration **unlawful** even if motivationally effective.

---

## 2. Boundary Catalogue

| ID | Boundary | One-line rule |
|----|----------|---------------|
| **AEB-01** | Constitutional reasoning only | Explanations may describe published ownership and resolution reasoning |
| **AEB-02** | Ownership identification | Explanations may identify decision ownership |
| **AEB-03** | Workflow participation reference | Explanations may reference orchestration participation as context |
| **AEB-04** | No educational meaning rewrite | Explanations must not redefine Programme VI educational meaning |
| **AEB-05** | No evidence reinterpretation | Explanations must not reinterpret Educational Evidence or Twin estimates |
| **AEB-06** | No invented authority | Explanations must not invent owners, domains, or decision classes |
| **AEB-07** | No unpublished precedence | Explanations must not introduce ranking, scores, or undeclared winner rules |
| **AEB-08** | No ownership transfer fiction | Explanations must not imply transferred, absorbed, or dual ownership |
| **AEB-09** | No runtime implementation exposure as law | Explanations must not present implementation details as constitutional justification |
| **AEB-10** | No orchestration-as-tutor | Explanations must not cast the Workflow Engine as educational decision owner |

---

## 3. What Authority Explanations May Do

### AEB-01 — Describe Constitutional Reasoning

**Permitted:** Narrate why a component was permitted and why alternatives were not, citing published AP/AD/AB and (when applicable) CT/RP/RO.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “Recovery leads now because restoring continuity after disruption is the primary question.” | “Recovery scored 0.91 against Daily’s 0.44.” |
| Developer cites `AP-01; AD-04; RP-03` | Developer cites “pager duty preferred recovery” |

### AEB-02 — Identify Decision Ownership

**Permitted:** Name the MS001 owner in audience-appropriate language; record AD-0x in developer traces.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “Your day coach owns today’s priority.” | “Whoever rendered the card owns the decision.” |
| “Master Planner owns Study Plan changes.” | “Support staff can rewrite the plan in copy.” |

### AEB-03 — Reference Workflow Participation

**Permitted:** Mention that a workflow started, handed off, or concluded — as *orchestration context* that invited an owner — without attributing educational content decisions to the Workflow Engine.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “We switched focus because the educational question changed — recovery coaching is leading.” | “The workflow decided you should study Topic X.” |
| Developer: `workflow_explainability_ref=…; primary_owner=AD-04` | Developer: `owner=AD-07` for educational tip content |

---

## 4. What Authority Explanations Must Not Do

### AEB-04 — Must Not Redefine Educational Meaning

**Forbidden:** Using explanation to reinterpret, rewrite, or silently edit Programme VI meanings or the substance of authorised recommendations.

| Forbidden narration | Why |
|---------------------|-----|
| “That earlier topic tip wasn’t really needed…” (to erase a deferral) | Disposition ≠ meaning invalidation (RP-02) |
| Relabel Recovery as Revision in speech to simplify the story | AB-01 / AP-09 |
| Claim mastery / pass certainty from ownership clarity | EIP-006 / AB-06 adjacency |

**Lawful alternative:** Preserve meaning; explain action disposition and permission only; link Programme VI explainability for educational warrant.

### AEB-05 — Must Not Reinterpret Evidence

**Forbidden:** Treating explanation as a licence to reclassify Educational Evidence, invent observations, or mint Estimated Knowledge / Mastery from coaching or UI completion.

| Forbidden narration | Why |
|---------------------|-----|
| “Because you opened the mission, we now know you understand…” | AB-03 / AB-06 |
| Ownership speech that rewrites Evidence Model classifications | Evidence Pipeline / EIP-002 owns meaning |
| Twin facet names in student copy as ownership proof | Wrong audience + wrong authority |

**Lawful alternative:** Consume Evidence / estimates as published inputs; leave reclassification to rightful writers under EIP-001 / Evidence law.

### AEB-06 — Must Not Invent Authority

**Forbidden:** Creating owners, domains, or decision classes in speech that are not published in MS001 (or higher constitutional corpora).

| Forbidden narration | Why |
|---------------------|-----|
| “The adaptive engine owns today’s educational question.” | AB-09 / AB-10 / AP-02 |
| “A meta-coach merges all coaches.” | AP-01 / AB-08 |
| Inventing a new decision class mid-product path | Amend `AUTHORITY_DOMAINS.md` first — or refuse |

**Lawful alternative:** Cite existing AD domains; refuse out-of-domain requests (AP-08); amend MS001 before claiming new ownership.

### AEB-07 — Must Not Invent Unpublished Precedence

**Forbidden:** Presenting scores, ranks, optimiser confidence, A/B winners, or tribal “usually X wins” customs as constitutional permission or conflict law.

| Forbidden narration | Why |
|---------------------|-----|
| “The algorithm picked the higher score.” | RP-04 / AEP-03 |
| Soft hierarchy not written in MS001/MS002 | Unpublished precedence |
| “Ops override” as educational ownership | AP-02 / AB-10 |

**Lawful alternative:** Cite only published Constitution / EIP / AP/AD/AB / CT/RP/RO. If a real precedence gap exists, amend owning corpora — do not narrate around it.

### AEB-08 — Must Not Imply Ownership Transfer

**Forbidden:** Speech that makes temporary focus, conflict disposition, delegation, or UI proximity sound like transferred or dual ownership.

| Forbidden narration | Why |
|---------------------|-----|
| “Recovery now owns your daily plan.” | RP-01 / AP-06 / AEP-08 |
| “We merged coaches into one owner.” | AP-01 / AB-08 / RO-03 limits |
| “Delegation made the session the new planner.” | AP-04 non-alienation |

**Lawful alternative:** Distinguish *acted-upon / leading action* from *standing owner*; narrate AP-04 with restore conditions; use RO vocabulary for dispositions.

### AEB-09 — Must Not Expose Runtime Implementation as Law

**Forbidden:** Presenting queues, service names, feature flags, database rows, job IDs, stack traces, or adapter paths as the *constitutional reason* a component was permitted.

| Forbidden as justification | Permitted as non-authoritative ops context (developer-only, clearly labelled) |
|----------------------------|-------------------------------------------------------------------------------|
| “Because `MissionService` ran first…” | Optional ops breadcrumbs *after* constitutional citations, never instead of them |
| “Flag `X` routed to recovery” | Flag may gate delivery; it does not create AD ownership |
| “Row id 12345 won” | Persistence identity ≠ permission warrant |

**Architectural requirement:** Constitutional justification precedes any implementation breadcrumb. Implementation detail never substitutes for AEC-03 / AEC-08.

### AEB-10 — Must Not Cast Orchestration as Tutor

**Forbidden:** Narrating the Workflow Engine (AD-07) as the owner of educational content decisions (what to study, how to recover, what to revise, exam approach, plan publication).

| Forbidden narration | Why |
|---------------------|-----|
| “The workflow recommends Topic X.” | AB-05 / RP-09 / Workflow boundaries |
| “Orchestration chose your strategy.” | Strategy remains Programme VI / Master Planner pathways |
| Completing a workflow narrated as mastery | Completion ≠ educational success (WS1 MS003) |

**Lawful alternative:** Workflow *invites* or *sequences* owners; Programme VI owners *decide*; MS003 explains *permission*.

---

## 5. Boundary Interaction with MS001 / MS002

| MS001 / MS002 law | Explanation boundary effect |
|-------------------|----------------------------|
| AP-01 single owner | AEB-06 / AEB-08 forbid dual-owner speech |
| AP-04 delegation | AEB-08 forbids alienation fiction; AEP-05 requires transparency |
| AP-09 / AB-01 non-reinterpretation | AEB-04 binds explanation |
| AB-03 / AB-06 evidence & mastery | AEB-05 binds explanation |
| RP-01 / RP-02 preservation | AEB-04 / AEB-08 bind conflict speech |
| RP-04 rule-bound resolution | AEB-07 forbids score stories |
| RO-03 exceptional merge | Merge speech only with published pathway; else AEB-06 / AEB-08 |

Explanation boundaries **do not amend** MS001/MS002. They constrain how those corpora are spoken.

---

## 6. Refusal Duty for Unlawful Narration

If a proposed explanation would require crossing AEB-04…AEB-10:

1. **Refuse** the narration path, or
2. **Amend** the owning constitutional corpus first (MS001 domains, MS002 outcomes, Programme VI meaning, EIP), then explain the amended law.

Silent “helpful” copy that crosses a boundary is an architectural defect, not a UX win.

---

## 7. Completeness vs Boundaries

Satisfying `EXPLANATION_COMPONENTS.md` does **not** authorise crossing these boundaries. A complete component set that invents ownership or meaning remains unlawful.

Conversely, a boundary-respecting explanation that omits mandatory components remains incomplete (AEP-02).

Both completeness and boundaries are required.

---

## 8. Closing

Authority explanations are trustworthy only inside these limits:

> **May describe constitutional reasoning, ownership, and workflow participation.  
> Must never redefine meaning, reinterpret evidence, invent authority, publish undeclared precedence, transfer ownership in speech, or treat runtime guts as educational law.**
