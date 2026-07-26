# Recommendation Explainability

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS001 — Educational Recommendation Model  
**Classification:** Explainability contract for constitutional educational recommendations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **educational recommendations** to students and developers.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (especially EL-008)
4. [`EDUCATIONAL_RECOMMENDATION_MODEL.md`](EDUCATIONAL_RECOMMENDATION_MODEL.md)
5. [`RECOMMENDATION_OBJECTIVES.md`](RECOMMENDATION_OBJECTIVES.md) (especially ERO-05)
6. [`RECOMMENDATION_SOURCES.md`](RECOMMENDATION_SOURCES.md)
7. [`RECOMMENDATION_STRUCTURE.md`](RECOMMENDATION_STRUCTURE.md)
8. [`RECOMMENDATION_BOUNDARIES.md`](RECOMMENDATION_BOUNDARIES.md)
9. Programme VI explainability corpora for the owning authority
10. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) — orchestration speech when context is material
11. [`../authority_explainability/`](../authority_explainability/) — permission / refusal / conflict permission speech when ownership narration is material
12. [`../conflict_resolution/RESOLUTION_EXPLAINABILITY.md`](../conflict_resolution/RESOLUTION_EXPLAINABILITY.md) — disposition speech when concurrency arose

> **Explainability improves understanding of recommendations already authorised.  
> It never invents educational certainty, ownership, or independent tips.**

---

## 1. Purpose

Students should never have to guess why Kwalitec recommended a particular next step — or why it refused one.

Developers should never have to reverse-engineer which constitutional components produced a tip.

Recommendation explainability exists so every material recommendation answers — in the right language for the audience — **why the recommendation exists**, **which constitutional components contributed**, **who owns it**, **what evidence supports it**, and **why it is constitutionally valid**.

Without recommendation explainability:

- tips feel arbitrary or manipulative;
- coaches appear to argue or vanish without reason;
- ownership and evidence honesty collapse into marketing speech;
- audits cannot prove constitutional validity.

With recommendation explainability:

- the student trusts the tutor posture;
- developers can verify Workstream 3 did not invent meaning;
- claim types stay honest;
- refusals and deferrals remain dignified and clear.

---

## 2. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Why this guidance; who is leading educationally; what supports it; honest limits; what to do next | ERO/ERS/ERC IDs, queue names, Twin facets, optimiser jargon, internal document paths |
| **Developer / auditor** | Precise constitutional references | Source classes, owner domain, evidence references, orchestration context, disposition IDs, constitutional refs, boundary test passes | Student-facing motivational fluff as a substitute for audit fields |

Student copy narrates educational reasons. Developer traces cite document IDs, source classes, and component completeness.

---

## 3. Traceability Obligation (Architectural)

Every material constitutional recommendation must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Why it exists** | “Because today / recovery / revision / exam focus is the live educational question…” | ERS-01 artefact + ERS-02 event/warrant |
| **Contributing components** | “This comes from your Study Plan and today’s coaching…” | ERS-01…ERS-07 contribution set |
| **Constitutional owner** | “Recovery coaching is leading right now…” | ERC-02 / Authority domain |
| **Supporting evidence** | “Given what your recent study showed…” | ERC-03 evidence references + claim types |
| **Orchestration / disposition** | “We’re focusing on this first, so the other tip waits…” | ERC-04 + ERC-06 (RO-xx when applicable) |
| **Constitutional validity** | Implicit honesty that limits are spoken | ERC-05 refs + RB-01…RB-10 pass |

A tip with no why → contributors → owner → evidence honesty → validity chain is invalid — even if the explanation sounds motivating.

---

## 4. Five Recommendation Questions (Binding)

Every material recommendation must answer these five questions.

### ERQ-01 — Why does this recommendation exist?

**Student examples:**

- “You’ve come back to study, so the most useful next step under your Study Plan is…”
- “There’s been a break in your study rhythm, so the priority is restoring continuity sustainably.”
- “Your recent sittings suggest a learning obstacle, so the response is… — not just ‘do more.’”
- “We’re not inventing a tip yet — we need to adjust your Study Plan first.”

**Developer requirements:**

- Record ERS-01 artefact identity (or refuse/escalate class).
- Record ERS-02 warrant / event when orchestrated.
- Record why a tip was *not* invented when absent.

---

### ERQ-02 — Which constitutional components contributed?

**Student examples:**

- “This comes from your Study Plan and today’s coaching.”
- “Recovery coaching is leading; ordinary daily priorities take a back seat until continuity is restored.”
- “Revision emphasis informed today’s choice; it didn’t replace your plan.”

**Developer requirements:**

- List contributing ERS classes and underlying artefacts.
- Distinguish meaning contributors (ERS-01) from context (ERS-02), ownership (ERS-03), disposition (ERS-04), and evidence (ERS-05).
- Never list Recommendation Engine as a meaning contributor.

---

### ERQ-03 — Who owns it?

**Student examples:**

- “This is today’s coaching under your Study Plan.”
- “Recovery coaching owns this priority right now.”
- “This needs your long-term plan pathway — not a quick daily tip.”

**Developer requirements:**

- Record ERC-02 owner matching Authority Model.
- If delegated, record owner + delegation bounds (owner remains accountable).
- Align with WS2 / MS003 permission speech when narrating *why permitted* — without replacing this question.

---

### ERQ-04 — What evidence supports it?

**Student examples:**

- “Given your recent practice on this topic…”
- “We don’t yet have enough clear evidence to claim mastery — so the tip is about continuing carefully, not finishing.”
- “Your Study Plan still marks this as first learning, so exam-style focus isn’t warranted yet.”

**Developer requirements:**

- Record ERC-03 evidence identifiers / classifications or explicit thin-evidence flag (ERC-07).
- Preserve claim ladder: coverage ≠ understanding ≠ mastery.
- Forbid explanations that invent observations.

---

### ERQ-05 — Why is it constitutionally valid?

**Student examples:**

- “We’re working inside your Study Plan — not rewriting it.”
- “This tip doesn’t claim you’ve mastered the topic.”
- “Another useful tip waits; this one leads for a clear educational reason.”

**Developer requirements:**

- Cite ERC-05 constitutional references.
- Record applicable boundary test passes (RB-01…RB-10).
- When concurrency applied, cite RO disposition and consistency with Resolution Explainability.
- Confirm structure completeness (C1–C7).

---

## 5. Relationship to Sibling Explainability Corpora

| Corpus | Answers | Relationship to this document |
|--------|---------|-------------------------------|
| **EIP-003 Educational Explainability Standard** | General student-facing educational speech contract | This corpus specialises recommendation artefacts under EL-008 |
| **Programme VI coach explainability** | Why *that coach’s* reasoning warrants guidance | Consumed inside ERQ-01 / ERQ-04; not replaced |
| **Workflow Explainability** | Why a workflow started / who participated / authority preserved | Feeds ERQ-01 / ERQ-02 when orchestration context is material |
| **Authority Decision Explainability** | Why a component was *permitted* to decide | Complements ERQ-03; does not replace guidance-why speech |
| **Resolution Explainability** | Why a conflict disposition was lawful | Complements ERQ-02 / ERQ-05 when ERC-06 applies |
| **This Recommendation Explainability** | Why *this recommendation artefact* exists and is valid end-to-end | Unifies guidance communication explainability |

All are required where their facts apply; none invents unpublished meaning.

---

## 6. Narrative Rules

1. **Faithfulness over persuasion.** Explanation may not strengthen claims beyond the underlying artefact and evidence.
2. **Owner before brand.** Name the educational owner; do not attribute tips to “Kwalitec AI” as a meaning authority.
3. **Limits are first-class.** Thin evidence, refuse, defer, and escalate must be speakable without shame language.
4. **No optimiser speech.** Engagement, ranking scores, and A/B winners are not educational explanations.
5. **No silent dual primary.** If a sibling tip waits, say so when material to trust (align with RO dispositions).
6. **Plan honesty.** Never imply the tip rewrote the Canonical Study Plan.
7. **Audience separation.** Student copy and developer traces must not contradict each other.
8. **Explainability ≠ execution.** Explaining a recommendation does not perform the recommended action or mutate state.

---

## 7. Refusal and Absence Explainability

When there is **no** constitutional recommendation, explanation remains mandatory for material student-facing moments that might otherwise invent a tip:

| Situation | Student posture | Developer record |
|-----------|-----------------|------------------|
| No Programme VI warrant | “We shouldn’t invent a tip yet.” | ERS-01 absent; refuse class |
| Authority refusal | “This decision belongs to…; today’s coaching won’t override it.” | ERS-03 refusal |
| Workflow escalate | “Your Study Plan needs attention before a daily tip.” | ERS-02 escalate |
| Unlawful candidate rejected | Not shown as peer tip | RO-05 + reason |
| Thin evidence | “We don’t have enough to claim that yet.” | ERC-07 thin-evidence |

Absence of a tip must not become silence that students fill with distrust — nor become invented certainty.

---

## 8. Explainability Tests (Pass / Fail)

| ID | Test | Pass | Fail |
|----|------|------|------|
| **REX-01** | Five questions | ERQ-01…ERQ-05 answerable | Any question unanswered for a material tip |
| **REX-02** | Audience honesty | Student and developer traces consistent | Student overclaim vs developer thin evidence |
| **REX-03** | Non-invention | Explanation cites only documented sources | Motivational invention of meaning or evidence |
| **REX-04** | Owner clarity | Owner named and matches Authority Model | “The system recommends” as ownership |
| **REX-05** | Conflict fidelity | Disposition explained when concurrency applied | Hidden dual primary or silent average |
| **REX-06** | Limit speech | Thin evidence / refuse spoken when true | Certainty theatre |

---

## 9. Closing

Recommendation explainability is how lawful guidance earns student trust.

When a tip cannot answer the five questions, **it is not ready to be a constitutional recommendation**.  
When explanation would require inventing certainty, **weaken the claim or refuse** — do not narrate fiction.

> **Why · contributors · owner · evidence · validity — or no recommendation.**
