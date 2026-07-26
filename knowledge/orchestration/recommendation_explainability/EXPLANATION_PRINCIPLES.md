# Explanation Principles

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS003 — Recommendation Set Explainability  
**Classification:** Binding constitutional principles for recommendation set explanations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional principles** governing how Kwalitec explains assembled educational recommendation sets.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`RECOMMENDATION_SET_EXPLAINABILITY.md`](RECOMMENDATION_SET_EXPLAINABILITY.md)
4. [`../recommendation_assembly/ASSEMBLY_OBJECTIVES.md`](../recommendation_assembly/ASSEMBLY_OBJECTIVES.md) — especially RAO-05
5. [`../recommendation_assembly/ASSEMBLY_EXPLAINABILITY.md`](../recommendation_assembly/ASSEMBLY_EXPLAINABILITY.md) — RAQ speech themes explanations must remain consistent with
6. [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md) — per-constituent speech remains mandatory
7. Programme VI meaning corpora — meanings that explanation must not rewrite
8. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md) — orchestration must not be narrated as tip ownership

> **Recommendation set explanations must make provenance, assembly, ownership, and workflow context transparent.  
> They must never invent constitutional law or educational tips.**

---

## 1. Purpose

Principles prevent set narration from becoming a second empire: motivational copy that invents tips, “helpful” merges that hide disposition, ownership absorption into “the app,” or developer traces that cite UX preference instead of published assembly law.

These principles bind every recommendation-set explanation path — documentation, design, and future Runtime A behaviour. They deliberately **do not** specify rendering, templates, or generation algorithms.

---

## 2. Principle Catalogue

| ID | Principle | One-line rule |
|----|-----------|---------------|
| **RSEP-01** | Provenance transparency | Every material explanation makes contributing sources and tip provenance reconstructable |
| **RSEP-02** | Assembly transparency | Every material explanation describes organisation of lawful artefacts — never tip creation |
| **RSEP-03** | Ownership visibility | Every material explanation names each constituent’s constitutional owner |
| **RSEP-04** | Workflow context visibility | When orchestration situates the set, that context is speakable without claiming tip ownership |
| **RSEP-05** | Constitutional traceability | Set existence, assembly, and interpretation are traceable to published constitutional artefacts |
| **RSEP-06** | Interpretation honesty | Primary vs waiting, empty / single-member sets, and limits are spoken without shame or fiction |
| **RSEP-07** | Disposition fidelity | When concurrency applied, conflict dispositions are referenced — never re-resolved in speech |
| **RSEP-08** | Meaning non-invention | Explanation never redefines Programme VI educational meaning or invents tips |
| **RSEP-09** | Layer honesty | Meaning, ownership, disposition, orchestration, tip artefact, and set packaging remain distinct in speech |
| **RSEP-10** | Audience fidelity | Student and developer speech share one truth; vocabulary differs by audience |

---

## 3. RSEP-01 — Provenance Transparency

**Rule:** Every material recommendation set explanation must make contributing constitutional sources and each constituent’s provenance reconstructable for the audience.

| Lawful | Unlawful |
|--------|----------|
| “This comes from your Study Plan and today’s coaching…” | “The system put some tips together” with no sources |
| Developer: RAC-02 / ERS contribution map + constituent ERC refs | Hide that a sibling coach contributed |
| Preserve deferred tip’s provenance when it waits | Rewrite waiting tip provenance to fit packaging |

**Relationship to MS002:** RSEP-01 is the explanation-face of RAC-02 / RAC-06 provenance preservation and RAQ-03 / RAQ-04.

---

## 4. RSEP-02 — Assembly Transparency

**Rule:** Explanation must describe how lawful recommendations were *organised* into the set — membership warrant, relation posture, coherence — and must never narrate assembly as creating educational guidance.

| Lawful | Unlawful |
|--------|----------|
| “These tips already apply; we show them together so the priority is clear.” | “We created a combined tip for you.” |
| “There isn’t a recommendation set yet — we won’t invent filler.” | Silent empty set replaced by motivational slogans |
| Developer: RAC-01 membership + RAC-07 coherence | “Assembly scored and minted members” |

**Relationship to MS002:** RSEP-02 is the explanation-face of RAO-01 (organise lawful recommendations) and RAB non-invention.

---

## 5. RSEP-03 — Ownership Visibility

**Rule:** Every material set explanation must identify the constitutional owner of each constituent recommendation, plus a set-level ownership index that never invents a set owner that absorbs members.

| Lawful | Unlawful |
|--------|----------|
| “Recovery coaching is leading; your day coach still owns ordinary daily priorities.” | “The recommendation set owns today’s advice.” |
| “Revision informed today; it did not replace your day coach.” | “We merged coaches into one owner.” |
| Developer: RAC-03 owner index matching Authority Model | Substitute UI surface names for constitutional owners |

**Relationship to MS001 / MS002:** RSEP-03 is the explanation-face of RAO-02 and RAC-03. Visibility describes ownership; it does not create it.

---

## 6. RSEP-04 — Workflow Context Visibility

**Rule:** When a workflow, stage handoff, or completion event situates *why this set is live now*, that orchestration context must be speakable — without attributing tip content or educational meaning to the Workflow Engine.

| Lawful | Unlawful |
|--------|----------|
| “You’ve returned to study, so today’s coaching and your Study Plan sit together as the live advice.” | “The workflow recommends Topic X.” |
| Developer: RAC-04 workflow_explainability_ref + primary owners | `owner=workflow` for educational tip content |
| Escalate speech: “Your Study Plan needs attention before a recommendation set.” | Invent tips to skip planning pathways |

**Relationship to WS1:** RSEP-04 aligns with workflow explainability participation speech. Orchestration *invites*; Programme VI owners *decide*; MS003 explains *set packaging*.

---

## 7. RSEP-05 — Constitutional Traceability

**Rule:** Why the set exists, how it was assembled, and how it should be interpreted must be reconstructible from published Constitution / EIP / MS001 / MS002 / WS1 / WS2 artefacts — not from product preference or unpublished customs.

| Lawful | Unlawful |
|--------|----------|
| Trace set → RAC components → constituent ERCs → owners / dispositions / sources | “It felt right in the product path” |
| Cite MS002 RAQ answers and MS003 RSEQ answers | Cite only engagement metrics as set warrant |
| Record boundary passes (RAB / RSEB) | Tribal “we usually batch these coaches” without published law |

**Traceability tests:**

1. Can a developer reconstruct RSEQ1–RSEQ4 without reading implementation code?
2. Can a student hear *why this package* and *how to read it* without architecture jargon?
3. If the answer depends on unpublished tribal knowledge, the explanation is not yet constitutional — amend owning corpora or refuse.

---

## 8. RSEP-06 — Interpretation Honesty

**Rule:** How the set should be read — primary vs waiting, empty / single-member honesty, thin evidence, refuse / defer / escalate — must be spoken without shame language, dual-primary theatre, or invented certainty.

| Lawful | Unlawful |
|--------|----------|
| “Focus on restoring continuity first; today’s ordinary priority waits.” | Hide a waiting tip so packaging looks simpler |
| “This is the live guidance right now.” (single-member) | Fabricate sibling tips for “completeness” |
| “We don’t have enough evidence to claim more than this.” | Completeness theatre that overclaims |

**Relationship to MS002:** RSEP-06 is the explanation-face of RAQ-02 and empty/single-member explainability duties.

---

## 9. RSEP-07 — Disposition Fidelity

**Rule:** When MS002 concurrency applied and Conflict Resolution dispositioned action, set explanation must reference published RO outcomes (and CT/RP when material) — and must never invent a packaging-time winner.

| Lawful | Unlawful |
|--------|----------|
| Name deferred / superseded / acted-upon posture honestly | “The set picked the better tip” |
| Align with Resolution Explainability RQ1–RQ4 | Soft-rank siblings with scores as disposition |
| Preserve deferred meaning (RP-02) | “The waiting tip was wrong because we packaged recovery first” |

**Relationship to WS2:** RSEP-07 is the explanation-face of RAO-04 / RAC-05. Assembly and set speech *reference* disposition; they do not *perform* it.

---

## 10. RSEP-08 — Meaning Non-Invention

**Rule:** Set explanation frames *packaging and interpretation*. It does not invent recommendations, reinterpret Evidence, or silently edit Programme VI educational meanings.

| Lawful | Unlawful |
|--------|----------|
| Point to each owner’s Programme VI / MS001 explainability for educational warrant | Invent a compromise tip in set speech |
| Consume Evidence / Twin estimates as published inputs on constituents | Reinterpret Evidence inside set packaging speech |
| Keep coverage ≠ understanding ≠ mastery in any adjacent claims (EIP-006) | Imply mastery from clear set narration alone |

---

## 11. RSEP-09 — Layer Honesty

**Rule:** Speech must keep layers distinct: Programme VI meaning, MS001 tip artefact, MS002 assembly, WS2 ownership / disposition, WS1 orchestration, and this set-explanation contract.

| Layer | Explanation may | Explanation must not |
|-------|-----------------|----------------------|
| Meaning | Reference owners’ Programme VI explainability | Substitute set speech for educational warrant |
| Tip artefact | Require ERQ-01…ERQ-05 per member | Treat incomplete slogans as set members |
| Assembly | Describe RAC organisation | Claim assembly created tips |
| Ownership | Name RAC-03 owners | Invent domains or absorb owners into “the set” |
| Conflict | Reference RAC-05 / RO outcomes | Invent CT/RP/RO |
| Orchestration | Reference RAC-04 participation | Claim orchestration owns tip content |

---

## 12. RSEP-10 — Audience Fidelity

**Rule:** Student-facing and developer/auditor-facing explanations describe the **same constitutional facts**. Vocabulary differs; truth does not.

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Why this package; how tips relate; who leads; honest limits | RSEP/RSEC/RAC IDs, queue names, Twin facets, optimiser jargon |
| **Developer / auditor** | Precise constitutional references | Constituents, sources, owners, workflow context, dispositions, evidence refs, RSEQ answers, boundary passes | Motivational fluff as a substitute for audit fields |

Student copy that invents a tip or a second owner is unlawful even if warm. Developer traces that only say “UX batched the cards” are unlawful even if precise about screens.

---

## 13. Application Order (Conceptual)

When composing a material recommendation set explanation:

1. Identify lawful constituents (or explicit empty set) and existence warrant (RSEQ1 / RSEP-02 / RSEP-05).
2. Describe assembly organisation and contributing sources (RSEQ2 / RSEP-01 / RSEP-02).
3. Make ownership visible for each member (RSEP-03).
4. If workflow situates the set, narrate orchestration context without tip ownership (RSEP-04).
5. State interpretation: relations, dispositions, limits (RSEQ3 / RSEP-06 / RSEP-07).
6. Confirm provenance / ownership / integrity preservation (RSEQ4 / RSEP-01 / RSEP-08).
7. Preserve layer honesty and emit audience-appropriate speech (RSEP-09 / RSEP-10).

This order is constitutional guidance for explanation composition. It is **not** a runtime algorithm.

---

## 14. Closing

Principles keep recommendation-set speech honest: **provenance visible, assembly transparent, ownership named, workflow context clear, constitutional facts traceable — without inventing tips, meaning, or winners.**

> **Transparent provenance. Transparent assembly. Visible ownership. Traceable constitutional speech.**
