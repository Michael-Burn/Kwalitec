# Explanation Principles

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS003 — Authority Decision Explainability  
**Classification:** Binding constitutional principles for authority decision explanations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional principles** governing how Kwalitec explains authority decisions, delegations, and conflict resolutions.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`AUTHORITY_DECISION_EXPLAINABILITY.md`](AUTHORITY_DECISION_EXPLAINABILITY.md)
4. [`../authority/AUTHORITY_PRINCIPLES.md`](../authority/AUTHORITY_PRINCIPLES.md) — ownership principles explanations must faithfully reflect
5. [`../conflict_resolution/RESOLUTION_PRINCIPLES.md`](../conflict_resolution/RESOLUTION_PRINCIPLES.md) — resolution principles conflict explanations must faithfully reflect
6. Programme VI meaning corpora — meanings that explanation must not rewrite
7. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md) — orchestration must not be narrated as educational ownership

> **Authority explanations must make ownership and permission transparent.  
> They must never invent constitutional law.**

---

## 1. Purpose

Principles prevent authority narration from becoming a second empire: motivational copy that invents owners, “helpful” merges that hide conflict, or developer traces that cite UX preference instead of published domains.

These principles bind every authority explanation path — documentation, design, and future Runtime A behaviour. They deliberately **do not** specify rendering, templates, or generation algorithms.

---

## 2. Principle Catalogue

| ID | Principle | One-line rule |
|----|-----------|---------------|
| **AEP-01** | Ownership transparency | Every material explanation names the decision owner |
| **AEP-02** | Authority traceability | Permission and refusal are traceable to published constitutional artefacts |
| **AEP-03** | Constitutional justification | Only published Constitution / EIP / MS001 / MS002 rules may justify permission |
| **AEP-04** | Conflict transparency | When concurrency arose, conflict kind, rules, and dispositions are speakable |
| **AEP-05** | Delegation transparency | Temporary exercise names owner, delegate, scope, and restore condition |
| **AEP-06** | Refusal dignity | Non-permission is explained as constitutional refusal, not product failure theatre |
| **AEP-07** | Meaning non-invention | Explanation never redefines Programme VI educational meaning |
| **AEP-08** | Ownership non-transfer | Explanation never implies transferred or absorbed ownership |
| **AEP-09** | Layer honesty | Meaning, ownership, orchestration, and conflict disposition remain distinct in speech |
| **AEP-10** | Audience fidelity | Student and developer speech share one truth; vocabulary differs by audience |

---

## 3. AEP-01 — Ownership Transparency

**Rule:** Every material authority explanation must identify the constitutional decision owner for the decision class at stake.

| Lawful | Unlawful |
|--------|----------|
| “Your day coach owns today’s priority…” / `owner=AD-02` | “The app decided…” with no owner |
| “Recovery is leading action now; Daily still owns day-priority decisions…” | “Recovery owns your daily plan for now…” |
| Name AD-0x in developer traces | Substitute UI surface names for constitutional owners |

**Relationship to MS001:** AEP-01 is the explanation-face of AP-01 / AP-02. Transparency describes ownership; it does not create it.

---

## 4. AEP-02 — Authority Traceability

**Rule:** Permission (“why this component”) and non-permission (“why not another”) must be reconstructible from published domains, principles, boundaries, and (when applicable) conflict artefacts.

| Lawful | Unlawful |
|--------|----------|
| Trace owner → decision class → AP/AD/AB (and CT/RP/RO if conflict) | “It felt right in the product path” |
| Cite consumed owners of inputs (AP-05) | Hide that a sibling artefact was consumed |
| Record refused_or_non_primary with reason codes | Silent omission of material alternatives that would confuse an audit |

**Traceability tests:**

1. Can a developer reconstruct AEQ1–AEQ4 without reading implementation code?
2. Can a student hear *which educational voice* was entitled without needing architecture jargon?
3. If the answer depends on unpublished tribal knowledge, the explanation is not yet constitutional — amend owning corpora or refuse.

---

## 5. AEP-03 — Constitutional Justification

**Rule:** The only lawful justifications for permission are published constitutional rules — Constitution, EIP obligations, MS001 AP/AD/AB, and MS002 CT/RP/RO when concurrency applies.

| Lawful | Unlawful |
|--------|----------|
| “AD-04 owns recovery after disruption (AP-01 / AP-03)” | “Recovery scored higher than Daily” |
| “RP-03 higher obligation: restore continuity before ordinary day priority” | “Ops preferred recovery this sprint” |
| “AB-02 forbids plan rewrite by coaches; escalate to Master Planner pathways” | Invented “emergency ownership” under time pressure |

**No unpublished precedence:** Explanation may not introduce ranking tables, soft hierarchies, or “usually X wins” customs that are not already written in MS001/MS002 or higher law.

---

## 6. AEP-04 — Conflict Transparency

**Rule:** When a material conflict existed under MS002, explanation must make the conflict kind, applied rules, and outcome dispositions speakable — without implying ownership transfer.

| Lawful | Unlawful |
|--------|----------|
| Name CT-xx, peers, RP list, RO set (developer); plain concurrency story (student) | Hide concurrency as a single anonymous tip |
| Preserve deferred / superseded meanings (RP-02 / RP-07) | “The earlier tip was wrong because we switched” |
| Align with MS002 RQ1–RQ4 | Replace RQ chain with a discretionary winner story |

**Relationship to MS001 prevention speech:** MS001 emphasises conflict *prevention by design* (AP-01). When valid artefacts still compete for *action*, AEP-04 requires MS002 disposition transparency. Both may appear in one journey; they must not contradict.

---

## 7. AEP-05 — Delegation Transparency

**Rule:** When authority is exercised under AP-04, explanation must name the standing owner, the delegate, the bounded scope, and the condition of restoration — and must not narrate alienation.

| Lawful | Unlawful |
|--------|----------|
| “Within today’s goal, your session may adjust *how* you work…” | “The session is now your day coach / planner” |
| `delegation={owner:AD-02, delegate:session, scope:…, restore_when:…}` | Permanent transfer fiction |
| Speak restoration when handoff ends (AP-07) | Leave temporary focus sounding like a new standing owner |

---

## 8. AEP-06 — Refusal Dignity

**Rule:** When a component was not permitted to decide, explanation treats that as constitutional refusal (AP-08 / domain prohibited / boundary / RP-08 / RO-05) — not as unexplained error, shame, or “the system broke.”

| Lawful | Unlawful |
|--------|----------|
| “We’re not rewriting your Study Plan today — that needs a planning review.” | Hard failure with no named rightful owner |
| “This isn’t recovery coaching — consolidating revision is the question now.” | Blaming the student for asking the “wrong” coach |
| Developer: `refused_owners=[…]; reason=…` | Empty refusal with only HTTP/status theatre |

---

## 9. AEP-07 — Meaning Non-Invention

**Rule:** Authority explanation frames *who was permitted*. It does not invent, reinterpret, or silently edit Programme VI educational meanings or Evidence classifications.

| Lawful | Unlawful |
|--------|----------|
| Point to the owner’s Programme VI explainability for educational warrant | Rewrite a deferred tip’s warrant so conflict “disappears” |
| Consume Evidence / Twin estimates as published inputs | Reinterpret Evidence inside ownership speech |
| Keep coverage ≠ understanding ≠ mastery in any adjacent educational claims (EIP-006) | Imply mastery from permission clarity alone |

---

## 10. AEP-08 — Ownership Non-Transfer

**Rule:** Explanation must never imply that resolution, orchestration, UI proximity, or temporary focus transferred decision ownership.

| Lawful | Unlawful |
|--------|----------|
| “Recovery leads *action* now; Daily remains owner of day-priority decisions.” | “Recovery temporarily owns Daily’s domain.” |
| “Workflow handed off to Recovery as primary authority for this stage.” | “The workflow decided what you should study.” |
| RO-02 supersedes *acted-upon status* only | RO-02 narrated as ownership replacement |

**Relationship to MS002:** AEP-08 is the explanation-face of RP-01 / AP-06.

---

## 11. AEP-09 — Layer Honesty

**Rule:** Speech must keep layers distinct: Programme VI meaning, MS001 ownership, MS002 conflict disposition, and WS1 orchestration participation.

| Layer | Explanation may | Explanation must not |
|-------|-----------------|----------------------|
| Meaning | Reference owner’s Programme VI explainability | Substitute ownership speech for educational warrant |
| Ownership | Answer AEQ1–AEQ2 | Invent domains |
| Conflict | Answer AEP-04 / MS002 RQ chain | Invent CT/RP/RO |
| Orchestration | Reference participation / handoff context | Claim orchestration owns educational decisions |

---

## 12. AEP-10 — Audience Fidelity

**Rule:** Student-facing and developer/auditor-facing explanations describe the **same constitutional facts**. Vocabulary differs; truth does not.

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Which voice was entitled; why alternatives wait or were refused; honest limits | AD/AP/AB/CT/RP/RO IDs, engine names, Twin facets, optimiser jargon |
| **Developer / auditor** | Precise constitutional references | Owner domain, principles, boundaries, consumed/refused peers, conflict artefacts if any, preservation | Motivational fluff as a substitute for audit fields |

Student copy that invents a second owner is unlawful even if warm. Developer traces that only say “UX chose recovery” are unlawful even if precise about screens.

---

## 13. Application Order (Conceptual)

When composing a material authority explanation:

1. Identify decision class and MS001 owner (AEP-01).
2. State permission warrant (AEQ1) from published AP/AD/AB (AEP-02 / AEP-03).
3. State material non-permissions (AEQ2) with dignity (AEP-06).
4. If AP-04 applied, narrate delegation transparently (AEP-05).
5. If MS002 concurrency applied, narrate conflict transparently (AEP-04) without transfer (AEP-08).
6. Preserve meaning and layer honesty (AEP-07 / AEP-09).
7. Emit audience-appropriate speech with shared truth (AEP-10).

This order is constitutional guidance for explanation composition. It is **not** a runtime algorithm.

---

## 14. Closing

Principles keep authority speech honest: **ownership visible, permission traceable, justification published, conflict and delegation transparent — without inventing meaning or transferring owners.**

> **Transparent ownership. Traceable permission. Published justification only.**
