# Assembly Explainability

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS002 — Recommendation Assembly Framework  
**Classification:** Explainability contract for assembled educational recommendation sets  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **assembled recommendation sets** to students and developers.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (especially EL-008)
4. [`RECOMMENDATION_ASSEMBLY_FRAMEWORK.md`](RECOMMENDATION_ASSEMBLY_FRAMEWORK.md)
5. [`ASSEMBLY_OBJECTIVES.md`](ASSEMBLY_OBJECTIVES.md) (especially RAO-05)
6. [`ASSEMBLY_COMPONENTS.md`](ASSEMBLY_COMPONENTS.md)
7. [`ASSEMBLY_BOUNDARIES.md`](ASSEMBLY_BOUNDARIES.md)
8. [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md) — per-constituent guidance explainability remains mandatory
9. Programme VI explainability corpora for each owning authority
10. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) — orchestration speech when context is material
11. [`../authority_explainability/`](../authority_explainability/) — permission / refusal / conflict permission speech when ownership narration is material
12. [`../conflict_resolution/RESOLUTION_EXPLAINABILITY.md`](../conflict_resolution/RESOLUTION_EXPLAINABILITY.md) — disposition speech when concurrency arose

> **Explainability improves understanding of recommendation sets already lawfully organised.  
> It never invents educational certainty, ownership, conflict winners, or independent tips.**

---

## 1. Purpose

Students should never have to guess why several recommendations appear together — or how a primary tip relates to one that waits.

Developers should never have to reverse-engineer which constitutional sources and dispositions produced a set.

Assembly explainability exists so every material recommendation set answers — in the right language for the audience — **why recommendations appear together**, **how they relate**, **which constitutional sources contributed**, and **how provenance has been preserved**.

Without assembly explainability:

- tip batches feel arbitrary or manipulative;
- primary and deferred tips appear to argue or vanish without reason;
- ownership and provenance collapse into marketing speech;
- audits cannot prove the set did not invent members or re-resolve conflicts.

With assembly explainability:

- the student trusts coherent tutor packaging;
- developers can verify Workstream 3 / MS002 did not invent meaning or disposition;
- claim types and disposition honesty stay intact;
- empty and single-member sets remain dignified and clear.

---

## 2. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Why these tips belong together; how primary relates to waiting tips; who leads educationally; honest limits | RAO/RAC/RAB IDs, queue names, Twin facets, optimiser jargon, internal document paths |
| **Developer / auditor** | Precise constitutional references | Constituent identities, source classes, ownership refs, workflow context, disposition IDs, provenance preservation checks, boundary test passes | Student-facing motivational fluff as a substitute for audit fields |

Student copy narrates educational organisation. Developer traces cite document IDs, source classes, and set-component completeness.

Per-constituent ERQ-01…ERQ-05 answers remain required under WS3 / MS001. This document adds **set-level** questions; it does not replace tip-level explainability.

---

## 3. Traceability Obligation (Architectural)

Every material constitutional recommendation set must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Why together** | “These belong together because…” | RAC-01 membership warrant + RAC-04 orchestration |
| **How they relate** | “This leads; that waits…” | RAC-05 RO refs / RAC-07 coherence |
| **Contributing sources** | “This comes from your Study Plan and coaching…” | RAC-02 ERS contribution map |
| **Ownership** | “Recovery coaching is leading…” | RAC-03 owner index |
| **Provenance preserved** | Implicit honesty that tips were not invented in packaging | RAC-02 / RAC-06 / constituent ERC refs intact |
| **Set validity** | Implicit honesty that limits are spoken | RAC completeness S1–S7 + RAB-01…RAB-11 pass |

A set with no why-together → relations → sources → provenance chain is invalid — even if the explanation sounds motivating.

---

## 4. Four Assembly Questions (Binding)

Every material recommendation set must answer these four questions.

### RAQ-01 — Why do these recommendations appear together?

**Student examples:**

- “You’ve returned to study, so today’s coaching and your Study Plan sit together as the live advice.”
- “Recovery is leading right now; ordinary daily priorities are still recorded, but they wait.”
- “We’re not inventing extra tips — only the guidance that already applies is shown.”
- “There isn’t a recommendation set yet — we need your Study Plan pathway first.”

**Developer requirements:**

- Record RAC-01 membership rationale (which complete artefacts qualify for this moment).
- Record RAC-04 workflow / event warrant when orchestrated.
- Record why members were *not* invented when absent (empty / single set honesty).

---

### RAQ-02 — How do the recommendations relate?

**Student examples:**

- “Focus on restoring continuity first; today’s ordinary priority waits until then.”
- “These tips support the same Study Plan — they aren’t competing guesses.”
- “One tip leads for a clear educational reason; the other remains valid but not primary.”

**Developer requirements:**

- Record primary-action posture and sibling dispositions (RAC-05 / RO-xx when concurrency applied).
- Record RAC-07 coherence checks (no dual primary; no orphaned material siblings).
- Never claim assembly “chose a winner” — Conflict Resolution did, when concurrency existed.
- For single-member sets, record that relation is trivial identity (not invented ranking).

---

### RAQ-03 — Which constitutional sources contributed?

**Student examples:**

- “This comes from your Study Plan and today’s coaching.”
- “Recovery coaching and today’s coaching both contributed; recovery is leading.”
- “Revision emphasis informed the set; it didn’t rewrite your plan.”

**Developer requirements:**

- List contributing ERS classes and underlying artefacts (RAC-02).
- Distinguish meaning contributors (ERS-01) from context (ERS-02), ownership (ERS-03), disposition (ERS-04), and evidence (ERS-05).
- Never list Recommendation Assembly / Recommendation Engine as a meaning contributor.

---

### RAQ-04 — How has provenance been preserved?

**Student examples:**

- “We’re not inventing a new tip by combining coaches — each piece keeps its own reason.”
- “The waiting tip is still valid; it hasn’t been rewritten to fit.”
- “We don’t have enough evidence to claim more than what’s already said.”

**Developer requirements:**

- Confirm each constituent’s ERC-02 / ERC-03 / ERC-05 / ERS provenance remains reconstructable after packaging.
- Confirm no undocumented source substituted for ERS catalogue entries.
- Confirm ownership references (RAC-03) match Authority Model and were not absorbed.
- When concurrency applied, confirm RO disposition referenced equals Conflict Resolution outcome (no assembly mutation of disposition).
- Record applicable boundary test passes (RAB-01…RAB-11).

---

## 5. Relationship to Sibling Explainability Corpora

| Corpus | Answers | Relationship to this document |
|--------|---------|-------------------------------|
| **EIP-003 Educational Explainability Standard** | General student-facing educational speech contract | This corpus specialises *set organisation* speech under EL-008 |
| **Recommendation Explainability (WS3 / MS001)** | Why *each tip* exists and is valid | Mandatory per constituent; this corpus adds set-level questions |
| **Programme VI coach explainability** | Why *that coach’s* reasoning warrants guidance | Consumed inside constituents; not replaced by set speech |
| **Workflow Explainability** | Why a workflow started / who participated / authority preserved | Feeds RAQ-01 when orchestration context is material |
| **Authority Decision Explainability** | Why a component was *permitted* to decide | Complements ownership narration; does not replace set-why speech |
| **Resolution Explainability** | Why a conflict disposition was lawful | Complements RAQ-02 / RAQ-04 when RAC-05 applies |
| **This Assembly Explainability** | Why recommendations *appear together* and how provenance survived packaging | Organises set-level explainability themes (RAQ-01…RAQ-04) |
| **Recommendation Set Explainability (WS3 / MS003)** | Full set-explanation contract: principles, components, boundaries, patterns (RSEQ1…RSEQ4) | Specialises and binds set speech; does not amend this Framework’s assembly law |

All are required where their facts apply; none invents unpublished meaning.

**Consistency with MS003:** When composing material set narration, also satisfy [`../recommendation_explainability/`](../recommendation_explainability/). MS002 `ASSEMBLY_EXPLAINABILITY.md` owns RAQ themes for assembly speech; MS003 owns the closed principles / components / boundaries / pattern catalogue.

---

## 6. Narrative Rules

1. **Faithfulness over persuasion.** Explanation may not strengthen claims beyond constituents and evidence.
2. **Owner before brand.** Name educational owners; do not attribute the set to “Kwalitec AI” as a meaning authority.
3. **Relation before ranking.** Speak primary vs waiting in educational terms; never as optimiser scores.
4. **Limits are first-class.** Empty sets, single-member sets, thin evidence, refuse, defer, and escalate must be speakable without shame language.
5. **No optimiser speech.** Engagement, ranking scores, and A/B winners are not educational explanations of assembly.
6. **No silent dual primary.** If a sibling tip waits, say so when material to trust (align with RO dispositions).
7. **No invented merge speech.** Do not narrate a compromise tip unless RO-03 authorised a constitutional merge.
8. **Plan honesty.** Never imply the set rewrote the Canonical Study Plan.
9. **Audience separation.** Student copy and developer traces must not contradict each other.
10. **Explainability ≠ execution.** Explaining a set does not perform recommended actions or mutate state.

---

## 7. Empty and Single-Member Set Explainability

When the set has **zero** or **one** lawful constituent, explanation remains mandatory for material student-facing moments that might otherwise invent filler:

| Situation | Student posture | Developer record |
|-----------|-----------------|------------------|
| Empty set — no Programme VI warrant | “We shouldn’t invent tips to fill a list.” | RAC-01 empty; refuse invention |
| Single-member set | “This is the live guidance right now.” | RAC-01 n=1; no fabricated siblings |
| Authority refusal blocks members | “This decision belongs to…; we won’t override it with a batch.” | RAC-03 / ERS-03 refusal |
| Workflow escalate | “Your Study Plan needs attention before a recommendation set.” | RAC-04 escalate |
| Unlawful candidates rejected | Not shown as set members | RO-05 + reason; RAB-01 pass |
| Thin evidence across members | “We don’t have enough to claim more than this.” | RAC-07 / ERC-07 thin-evidence |

Absence of set members must not become silence that students fill with distrust — nor become invented batch certainty.

---

## 8. Explainability Tests (Pass / Fail)

| ID | Test | Pass | Fail |
|----|------|------|------|
| **RAX-01** | Four questions | RAQ-01…RAQ-04 answerable | Any question unanswered for a material set |
| **RAX-02** | Constituent coverage | Each material member also satisfies ERQ-01…ERQ-05 | Set speech without tip-level provenance |
| **RAX-03** | Audience honesty | Student and developer traces consistent | Student overclaim vs developer thin evidence / empty set |
| **RAX-04** | Non-invention | Explanation cites only documented sources and complete constituents | Motivational invention of members, meaning, or evidence |
| **RAX-05** | Relation fidelity | Disposition / relation explained when concurrency applied | Hidden dual primary or silent average |
| **RAX-06** | Provenance fidelity | Ownership and sources preserved after packaging | “The system assembled a new tip” as provenance |
| **RAX-07** | Limit speech | Empty / single / thin-evidence spoken when true | Completeness theatre |

---

## 9. Closing

Assembly explainability is how coherent recommendation packaging earns student trust.

When a set cannot answer the four questions, **it is not ready to be a constitutional recommendation set**.  
When explanation would require inventing members, inventing certainty, or inventing a conflict winner, **weaken the packaging or refuse** — do not narrate fiction.

> **Why together · how related · sources · provenance preserved — or no constitutional set.**
