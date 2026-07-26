# Explanation Examples

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS003 — Recommendation Set Explainability  
**Classification:** Illustrative constitutional explanation patterns  
**Status:** APPROVED — governing as pattern law; examples are illustrative, not a closed product-copy catalogue  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document provides **illustrative constitutional explanation patterns** for assembled educational recommendation sets.

Subordinate to:

1. [`RECOMMENDATION_SET_EXPLAINABILITY.md`](RECOMMENDATION_SET_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md)
4. [`EXPLANATION_BOUNDARIES.md`](EXPLANATION_BOUNDARIES.md)
5. [`../recommendation_assembly/`](../recommendation_assembly/)
6. [`../recommendations/`](../recommendations/)
7. [`../conflict_resolution/`](../conflict_resolution/)
8. [`../workflows/`](../workflows/)

> **Examples illustrate lawful shape.  
> They are not Runtime A copy, UI templates, or a scoring rubric.**

---

## 1. How to Read These Patterns

Each pattern includes:

| Section | Role |
|---------|------|
| **Situation** | Educational / constitutional setup |
| **Student speech** | Plain-language set narrative (RSEP-10) |
| **Developer trace** | Constitutional audit shape (RSEC-01…RSEC-10) |
| **RSEQ coverage** | How RSEQ1–RSEQ4 are answered |
| **Unlawful contrast** | Narration that would cross RSEB boundaries |

Patterns deliberately avoid binding product microcopy. Wording may vary; constitutional facts must not.

---

## 2. Pattern Catalogue

| ID | Pattern | Situation family |
|----|---------|------------------|
| **RSXP-E01** | Single recommendation set | One lawful member; no fabricated siblings |
| **RSXP-E02** | Multi-coach recommendation set | Multiple owners indexed; coherent packaging without mega-coach fiction |
| **RSXP-E03** | Assembled after conflict disposition | RO outcomes speakable; primary vs waiting; ownership intact |
| **RSXP-E04** | Workflow-driven recommendation set | Orchestration situates *why now*; tip owners remain Programme VI |

---

## 3. RSXP-E01 — Single Recommendation Set

### Situation

Only one constitutionally complete recommendation exists: Daily Coach (AD-02) today-priority under an Active Study Plan. No concurrency. No fabricated siblings. Assembly organises a lawful single-member set.

### Student speech (illustrative)

> “Right now there is **one** clear next step under your Study Plan — from your day coach. We’re not inventing extra tips to fill a list. This is the live guidance for today.”

### Developer trace (illustrative)

```
constituents: [rec_daily_today_priority]
contributing_sources: [ERS-01:daily_coach, ERS-01:canonical_study_plan, ERS-03:AD-02]
owners: [AD-02 → rec_daily_today_priority]
workflow_context: none
conflict_dispositions: none
evidence_references: [evidence_recent_study_thin|…]
assembly_warrant: organise_single_lawful_member; fabricated_siblings=false
interpretation_posture: identity; dual_primary=false; limits=[no_filler]
provenance_preservation:
  sources_intact: true
  owners_intact: true
  evidence_refs_intact: true
  dispositions_unmutated: n/a
  meaning_unrewritten: true
tip_explainability_refs: [rec_daily_today_priority → ERQ-01…ERQ-05]
```

### RSEQ coverage

| RSEQ | Answer |
|------|--------|
| RSEQ1 | Set exists because one lawful today-priority artefact is live |
| RSEQ2 | Assembled as single-member set; no invented siblings |
| RSEQ3 | Interpret as the sole live guidance; not a ranked shortlist |
| RSEQ4 | Owner AD-02, sources, and tip provenance preserved |

### Unlawful contrast

> “Here are three tips so your dashboard looks complete.” / “The set owns today’s advice.” / “Because `rank=0.88`…”

Violates RSEB-04 / RSEB-06 / RSEB-08.

---

## 4. RSXP-E02 — Multi-Coach Recommendation Set

### Situation

Two constitutionally complete recommendations coexist without seeking competing primary action in a conflict sense that requires supersession: Daily Coach today-priority (AD-02) informed by Revision Coach emphasis (AD-05) under a published contribution pathway (Revision *informs* day priority; does not absorb Daily ownership). Assembly indexes both owners. No anonymous mega-coach.

### Student speech (illustrative)

> “Today’s focus comes from your **day coach**, informed by **revision** of material you’ve already learned. Both roles stay distinct — revision is helping shape what is useful today; it is **not** rewriting your Study Plan, and it is **not** replacing your day coach.”

### Developer trace (illustrative)

```
constituents: [rec_daily_today_priority, rec_revision_emphasis]
contributing_sources:
  - ERS-01:daily_coach → rec_daily_today_priority
  - ERS-01:revision_coach → rec_revision_emphasis
  - ERS-01:canonical_study_plan
  - ERS-03:AD-02, AD-05
owners:
  - AD-02 → rec_daily_today_priority
  - AD-05 → rec_revision_emphasis
workflow_context: none
conflict_dispositions: none   # or pathway-only; no RO action race
evidence_references: [evidence_prior_topics…]
assembly_warrant: organise_multi_coach_coherent; published_contribution_pathway=revision_informs_day
interpretation_posture: coherent_siblings; primary_voice=AD-02; contributor=AD-05; mega_coach=false
provenance_preservation:
  sources_intact: true
  owners_intact: true
  evidence_refs_intact: true
  dispositions_unmutated: n/a
  meaning_unrewritten: true
tip_explainability_refs:
  - rec_daily_today_priority → ERQ-01…ERQ-05
  - rec_revision_emphasis → ERQ-01…ERQ-05
```

### RSEQ coverage

| RSEQ | Answer |
|------|--------|
| RSEQ1 | Set exists to present coherent multi-coach guidance already warranted |
| RSEQ2 | Assembled by indexing both lawful artefacts and owners under MS002 |
| RSEQ3 | Day coach leads; revision informs; neither absorbs the other |
| RSEQ4 | Both owners and both tip provenances preserved |

### Unlawful contrast

> “We merged everything into one tip.” / “Revision now owns today.” / Hiding the revision contributor.

Violates RSEB-04 / RSEB-06 / RSEP-03.

**Hard rule:** If no published contribution or merge pathway exists and both seek primary action, do **not** narrate a friendly multi-coach blend — disposition via WS2 first, then explain (see RSXP-E03).

---

## 5. RSXP-E03 — Assembled After Conflict Disposition

### Situation

CT-01 / CT-03: Daily Coach emitted a valid today-priority recommendation; Recovery Coach emitted a valid restorative recommendation after disruption. Conflict Resolution dispositions: Recovery acted upon (RO-06); Daily deferred (RO-01). Owners unchanged. Assembly organises both members with disposition references; set speech explains primary vs waiting.

### Student speech (illustrative)

> “You had more than one good kind of guidance at once: today’s planned focus, and restoring your study rhythm after a disruption. For now, **recovery leads**. Your day coach’s guidance **waits** — we are not throwing it away or rewriting what it means. These tips appear together so you can see what leads and what is still valid.”

### Developer trace (illustrative)

```
constituents: [rec_recovery_restore, rec_daily_today_priority]
contributing_sources:
  - ERS-01:recovery_coach → rec_recovery_restore
  - ERS-01:daily_coach → rec_daily_today_priority
  - ERS-04:conflict_disposition
  - ERS-03:AD-04, AD-02
owners:
  - AD-04 → rec_recovery_restore
  - AD-02 → rec_daily_today_priority
workflow_context: none | {handoff_to_recovery_focus}
conflict_dispositions:
  - rec_recovery_restore → RO-06
  - rec_daily_today_priority → RO-01
  conflict_types: [CT-01, CT-03]
evidence_references: [evidence_disruption…, evidence_plan…]
assembly_warrant: organise_dispositioned_peers; no_re_resolution=true
interpretation_posture:
  primary: rec_recovery_restore
  waiting: [rec_daily_today_priority]
  dual_primary: false
  meaning_of_waiting_preserved: true
provenance_preservation:
  sources_intact: true
  owners_intact: true
  evidence_refs_intact: true
  dispositions_unmutated: true
  meaning_unrewritten: true
  owners_unchanged: [AD-02, AD-04]
tip_explainability_refs:
  - rec_recovery_restore → ERQ-01…ERQ-05
  - rec_daily_today_priority → ERQ-01…ERQ-05
resolution_explainability_ref: RESOLUTION_EXPLAINABILITY.md#RQ1-RQ4
```

### RSEQ coverage

| RSEQ | Answer |
|------|--------|
| RSEQ1 | Set exists to present dispositioned peers honestly in one package |
| RSEQ2 | Assembled by organising both complete artefacts with RO references — not by picking a packaging winner |
| RSEQ3 | Recovery leads action; Daily waits; waiting tip remains valid |
| RSEQ4 | Owners, meanings, and dispositions preserved; no transfer fiction |

### Unlawful contrast

> “Recovery now owns your daily plan.” / “The set picked recovery.” / “Yesterday’s tip was wrong.”

Violates RSEB-06 / RSEB-09 / RSEB-05.

---

## 6. RSXP-E04 — Workflow-Driven Recommendation Set

### Situation

A return-to-study workflow event situates *why now*: orchestration invites Active Study Plan participation and Daily Coach today-priority. The Workflow Engine does not invent tip content. Assembly packages the lawful Daily Coach recommendation (and any plan-context artefacts already authorised) with explicit workflow context.

### Student speech (illustrative)

> “You’ve returned to study, so today’s coaching and your Study Plan sit together as the live advice. The focus comes from your **day coach** under your Study Plan — not from a workflow inventing a tip. If your plan needed a deeper change first, we would say so instead of inventing filler.”

### Developer trace (illustrative)

```
constituents: [rec_daily_today_priority]
contributing_sources:
  - ERS-01:daily_coach → rec_daily_today_priority
  - ERS-01:canonical_study_plan
  - ERS-02:return_to_study_workflow_event
  - ERS-03:AD-02
owners:
  - AD-02 → rec_daily_today_priority
workflow_context:
  event: return_to_study
  participation: [AD-02, plan_context]
  workflow_explainability_ref: WORKFLOW_EXPLAINABILITY.md
conflict_dispositions: none
evidence_references: [evidence_plan_active…]
assembly_warrant: organise_workflow_situated_lawful_members; tip_created_by_workflow=false
interpretation_posture:
  situating: workflow_invites_owners
  tip_owner: AD-02
  orchestration_not_tutor: true
provenance_preservation:
  sources_intact: true
  owners_intact: true
  evidence_refs_intact: true
  dispositions_unmutated: n/a
  meaning_unrewritten: true
tip_explainability_refs: [rec_daily_today_priority → ERQ-01…ERQ-05]
```

### Variant — escalate before set (illustrative student speech)

> “Your Study Plan needs attention before we can show a recommendation set. We won’t invent tips to skip that step.”

Developer: `constituents=[]; assembly_warrant=escalate_before_set; workflow_context=escalate_to_planning; tip_explainability_refs=none`.

### RSEQ coverage

| RSEQ | Answer |
|------|--------|
| RSEQ1 | Set exists because workflow situating + lawful tip(s) warrant a live package (or escalate refuses invention) |
| RSEQ2 | Assembled under MS002 with RAC-04 workflow context; tips remain Programme VI artefacts |
| RSEQ3 | Read orchestration as *why now*, not as *who invented the tip* |
| RSEQ4 | Tip owner and provenance preserved; workflow is coordination context only |

### Unlawful contrast

> “The workflow recommends Topic X.” / “Orchestration chose your strategy.” / Inventing tips to avoid escalate.

Violates RSEB-03 lookalike / RSEB-04 / RSEP-04.

---

## 7. Cross-Cutting Unlawful Anti-Patterns

| Anti-pattern | Typical RSEB / RSEP breach |
|--------------|----------------------------|
| “The app assembled some tips” (no sources/owners) | RSEP-01 / RSEP-03 / RSEB-02 |
| Filler tips for dashboard completeness | RSEB-04 |
| “The recommendation set owns today’s advice” | RSEB-06 |
| Score / rank / confidence as assembly warrant | RSEB-08 |
| “The set picked the winner” | RSEB-09 |
| “Workflow recommends Topic X” | RSEB-03 / RSEP-04 |
| Evidence reinterpreted in set speech | RSEB-07 |
| Mastery claimed from clear packaging narration | RSEB-05 / EIP-006 adjacency |
| Implementation service name as constitutional warrant | RSEB-10 |
| Friendly merge hiding ownership dispute or missing pathway | RSEB-04 / RSEB-06 / RSEB-09 |

---

## 8. Consistency with Sibling Examples

| When the journey also needs… | Also satisfy… |
|------------------------------|---------------|
| Per-tip educational warrant | [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md) ERQ-01…ERQ-05 |
| Set-organisation themes only | [`../recommendation_assembly/ASSEMBLY_EXPLAINABILITY.md`](../recommendation_assembly/ASSEMBLY_EXPLAINABILITY.md) RAQ-01…RAQ-04 |
| Permission / refusal speech | [`../authority_explainability/`](../authority_explainability/) |
| Conflict RQ1–RQ4 | [`../conflict_resolution/RESOLUTION_EXPLAINABILITY.md`](../conflict_resolution/RESOLUTION_EXPLAINABILITY.md) |
| Orchestration start / handoff / close | WS1 workflow / transition / completion explainability |
| Programme VI educational warrant | Owner’s `*_EXPLAINABILITY.md` |

MS003 patterns **frame set packaging speech**. They do not replace educational, permission, disposition, or orchestration speech.

---

## 9. Closing

These patterns show the same constitutional truth in four shapes:

> **Single-member honesty · multi-coach coherence · post-disposition clarity · workflow-situated packaging — always with provenance intact and no invented tips.**

Use them to test narration. Do not treat them as a closed catalogue of product strings.
