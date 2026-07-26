# Authority Explainability

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS001 — Educational Authority Model  
**Classification:** Explainability contract for educational decision ownership  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **educational authority** — why a component made a decision, why another could not, how authority was preserved, and how conflicts are prevented by design.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`EDUCATIONAL_AUTHORITY_MODEL.md`](EDUCATIONAL_AUTHORITY_MODEL.md)
4. [`AUTHORITY_PRINCIPLES.md`](AUTHORITY_PRINCIPLES.md)
5. [`AUTHORITY_DOMAINS.md`](AUTHORITY_DOMAINS.md)
6. [`AUTHORITY_BOUNDARIES.md`](AUTHORITY_BOUNDARIES.md)
7. Programme VI explainability corpora for the deciding owner
8. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) — orchestration-layer narration (complementary)

> **Explainability improves understanding of ownership already authorised.  
> It never invents educational certainty or a second owner.**

---

## 1. Purpose

Students should never have to guess why “today’s advice” came from day coaching rather than recovery, or why the plan was not rewritten on the spot.

Developers should never have to reverse-engineer which constitutional component owned a decision.

Authority explainability exists so every material educational outcome answers — in the right language for the audience:

1. **Why this component made the decision**
2. **Why another component could not**
3. **How authority was preserved** (and restored if temporarily handed off)
4. **How conflicts are prevented by design** (single owner / boundaries — not ad-hoc arbitration theatre)

Without authority explainability:

- coaches appear to argue or swap roles arbitrarily;
- refusals feel like product failure;
- plan non-mutation looks like stubbornness rather than constitutional care;
- audits cannot prove ownership discipline.

With authority explainability:

- the student trusts which tutor voice is speaking;
- developers can verify ownership against `AUTHORITY_DOMAINS.md`;
- preservation and restoration are speakable;
- design-time conflict prevention is visible (AP-01), not hidden in clever code.

---

## 2. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Which kind of guidance this is (today / recovery / revision / exam / plan change); why that voice is right *now*; honest limits | AD/AP/AB IDs, engine names, Twin facets, optimiser jargon |
| **Developer / auditor** | Precise constitutional references | Owner domain ID, decision class, consumed owners, prohibited alternatives refused, boundary IDs, preservation/restoration record | Student motivational fluff as a substitute for audit fields |

Student copy narrates educational roles. Developer traces cite document IDs and domain outcomes.

---

## 3. Traceability Obligation

Every material educational decision must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Decision class** | “We’re choosing what to do today / how to recover / what to revise…” | Named class from `AUTHORITY_DOMAINS.md` |
| **Authority owner** | “Your day coach / recovery coach / …” in plain speech | AD-0x owner |
| **Why this owner** | “Because the question right now is…” | AP-01 + primary question match |
| **Why not another** | “We’re not rewriting your plan / not treating this as recovery / …” when material | Prohibited-list refusal or non-primary sibling |
| **Consumed inputs** | “Given your Study Plan and recent study…” | Source owners of consumed artefacts |
| **Delegation (if any)** | “Within today’s goal, your session may adjust how you work…” | AP-04 owner → delegate → scope |
| **Preservation** | Implicit: plan/coach roles stay coherent | Explicit AP-06 checks / AB pass |
| **Restoration (if any)** | “Now that recovery is done, we return to ordinary daily guidance…” | AP-07 restoration record |
| **Conflict prevention** | “We focus on one main question at a time…” | Single primary owner; no silent merge |
| **Programme VI reasoning** | That owner’s explainability contract | Link to coach / planner explainability artefact |
| **Orchestration (if any)** | Optional: “We switched focus because…” | Workflow explainability + this ownership layer |

Authority explainability does **not** replace Programme VI educational explainability. It **frames** who was entitled to speak.

---

## 4. Mandatory Explanation Themes

### 4.1 Why a component made a decision

Student pattern:

> “We’re focusing on **[domain in plain speech]** because **[primary question in plain speech]**.”

Developer pattern:

> `owner=AD-0x; decision_class=…; primary_question_match=true; principles=[AP-01, AP-03]`

### 4.2 Why another component could not

Student pattern (when the alternative would be confusing if unnamed):

> “We’re **not** changing your long-term Study Plan today — that needs a proper planning review.”  
> “This isn’t recovery coaching — you need consolidating revision of what you’ve already learned.”  
> “The system isn’t inventing a tip on its own — your day coach owns today’s priority.”

Developer pattern:

> `refused_owners=[…]; reason=prohibited_for_caller|not_primary_question|boundary=AB-xx`

### 4.3 How authority was preserved

Student pattern:

> Speak in ways that keep roles coherent — do not imply the day coach rewrote the plan, or that orchestration “decided the syllabus.”

Developer pattern:

> `preservation=pass; plan_mutation=false; evidence_redefinition=false; independent_recommendation=false; domain_overclaim=false`

### 4.4 How conflicts are prevented by design

Student pattern:

> “We keep one main educational question at a time so advice doesn’t pull you in two directions.”

Developer pattern:

> `conflict_prevention=AP-01_single_owner; primary_question=…; no_silent_merge=true`

Do **not** narrate fictional runtime “arbitration scores.” Prevention is constitutional (single owner + boundaries), not a hidden algorithm invented by this Model.

---

## 5. Explanation Patterns by Situation

| Situation | Student emphasis | Developer emphasis |
|-----------|------------------|--------------------|
| **Ordinary day coaching** | Today’s goal under the plan | AD-02 owned; plan consumed |
| **Recovery primary** | Restoring progress after disruption; ordinary study waits | AD-04 primary; AD-02 not answering recovery |
| **Revision informs day** | Revisiting what you already learned; day coach still sets today | AD-05 meaning + AD-02 day ownership preserved |
| **Exam preparation primary** | Assessment-facing preparation; not a substitute for first learning | AD-06 warrant; AB / prohibited checks |
| **Structural escalation** | Plan may need adjustment through planning pathways | AD-01 pathway; coaches refused plan rewrite |
| **Workflow handoff** | Focus changed because the educational question changed | WS1 flow + AD owner invitation |
| **Refusal** | Honest “we won’t do X; Y is needed instead” | AP-08 + prohibited row |
| **Delegation (session)** | Adjusting *how* you work within today’s goal | AP-04 Daily → Session; no new day job |
| **Restoration after recovery** | Returning to ordinary daily guidance | AP-07 restoration |

---

## 6. Relationship to Sibling Explainability

| Layer | Document | Adds |
|-------|----------|------|
| Educational claims | EIP-003 | Honesty of what may be claimed |
| Coach / planner reasoning | Programme VI `*_EXPLAINABILITY.md` | Why *this* educational answer emerged |
| Orchestration flow | `WORKFLOW_EXPLAINABILITY.md` | Why the *flow* started and who participated |
| **Decision ownership** | **This document** | Why *this owner* could decide and others could not |

A complete material outcome ideally carries all layers that applied. Ownership explainability without Programme VI reasoning is hollow. Programme VI reasoning without ownership clarity invites role confusion.

---

## 7. Forbidden Explanation Behaviours

| Forbidden | Why |
|-----------|-----|
| Inventing a second owner in copy (“the app decided”) | Violates AP-01 / explicit authority |
| Claiming plan changes when only day priority changed | Misrepresents AD-01 vs AD-02 |
| Implying workflow “recommended” educational content | AB-05 / Workflow boundaries |
| Presenting refusal as unexplained error | AP-08 requires named owner |
| Using scores, ranks, or black-box confidence as ownership proof | Authority is constitutional, not scored |
| Student copy that names Twin facets / AD IDs | Wrong audience |
| Developer traces that only say “UX chose recovery” | Missing domain / principle citations |
| Narrating conflict “resolved by merging coaches” | Conflicts prevented by design — not merged meanings |

---

## 8. Minimal Audit Record (Conceptual)

Documentation and future implementations should be able to reconstruct at least:

```
decision_class:
owner: AD-0x
principles_applied: [AP-01, …]
consumed_owners: [AD-…, …]
refused_or_non_primary: [AD-… → reason]
boundaries_checked: [AB-…]
delegation: null | { owner, delegate, scope, restore_when }
preservation: pass | fail+detail
restoration: n/a | completed
programme_vi_explainability_ref: …
workflow_explainability_ref: null | …
```

This is a **constitutional audit shape**, not a database schema. Persistence design is out of scope for MS001.

---

## 9. Closing

Authority explainability makes ownership visible without turning the product into a lecture on architecture.

Students hear **which educational voice is speaking and why**.  
Developers see **which domain owned the decision and which boundaries held**.

> **Why this component. Why not another. How ownership survived. How conflict was designed out.**
