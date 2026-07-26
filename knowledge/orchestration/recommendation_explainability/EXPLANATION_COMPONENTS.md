# Explanation Components

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS003 — Recommendation Set Explainability  
**Classification:** Mandatory information set for recommendation set explanations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document catalogues the **information every material recommendation set explanation should contain**.

Subordinate to:

1. [`RECOMMENDATION_SET_EXPLAINABILITY.md`](RECOMMENDATION_SET_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`../recommendation_assembly/ASSEMBLY_COMPONENTS.md`](../recommendation_assembly/ASSEMBLY_COMPONENTS.md) — RAC-01…RAC-07 that explanations must faithfully describe
4. [`../recommendations/RECOMMENDATION_STRUCTURE.md`](../recommendations/RECOMMENDATION_STRUCTURE.md)
5. [`../recommendations/RECOMMENDATION_SOURCES.md`](../recommendations/RECOMMENDATION_SOURCES.md)
6. [`../conflict_resolution/`](../conflict_resolution/) — when concurrency applies
7. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)

> **Explanations are complete only when required constitutional components are present.  
> Completeness of speech is not completeness of educational success.**

---

## 1. Purpose

Without a closed component set, recommendation-set narration drifts: warm student copy without owners, or audit fields without disposition honesty. This document names what must be reconstructible for every material recommendation set explanation.

Components are **constitutional content obligations**, not database columns, API fields, or UI widgets. Persistence and rendering are out of scope for MS003.

These explanation components align with MS002 assembly components (RAC-01…RAC-07). RSEC fields narrate what RAC fields already require to exist for a constitutional set.

---

## 2. Component Catalogue

| ID | Component | One-line definition |
|----|-----------|---------------------|
| **RSEC-01** | Constituent recommendations | Lawful members of the set (or explicit empty-set posture) |
| **RSEC-02** | Contributing constitutional sources | Documented sources that contributed to the set and its members |
| **RSEC-03** | Recommendation owners | Named constitutional owners for each constituent (and set-level index) |
| **RSEC-04** | Workflow context | Orchestration situating facts for why this set is live now |
| **RSEC-05** | Conflict disposition references | RO outcomes / disposition facts when concurrency applied; else explicit none |
| **RSEC-06** | Constitutional evidence references | Honest Educational Evidence / warrant refs at set and/or constituent grain |
| **RSEC-07** | Assembly warrant | Why these members were organised together under MS002 |
| **RSEC-08** | Interpretation posture | How to read primary vs waiting, limits, and what the set does not mean |
| **RSEC-09** | Provenance preservation record | Confirmation that sources, owners, evidence, and constitutional refs survived packaging |
| **RSEC-10** | Tip-level explainability linkage | References that each material member also satisfies ERQ-01…ERQ-05 |

Additional components may be added only by amending this document.

---

## 3. Mandatory vs Conditional

| Component | Single-member set | Multi-coach set | Post-disposition set | Workflow-driven set |
|-----------|-------------------|-----------------|----------------------|---------------------|
| RSEC-01 Constituents | Mandatory (n=1) | Mandatory (n≥2) | Mandatory | Mandatory (or empty with warrant) |
| RSEC-02 Sources | Mandatory | Mandatory | Mandatory | Mandatory |
| RSEC-03 Owners | Mandatory | Mandatory (index all) | Mandatory (owners unchanged) | Mandatory |
| RSEC-04 Workflow context | Explicit `none` or situating ref | Same | Same | Mandatory situating ref |
| RSEC-05 Conflict dispositions | Explicit `none` | Explicit `none` unless concurrency | Mandatory RO set | Explicit `none` unless concurrency |
| RSEC-06 Evidence references | Mandatory (may be thin / none with honesty) | Same | Same | Same |
| RSEC-07 Assembly warrant | Mandatory | Mandatory | Mandatory | Mandatory |
| RSEC-08 Interpretation posture | Mandatory (identity + no fabricated siblings) | Mandatory (relation speech) | Mandatory (primary vs waiting) | Mandatory |
| RSEC-09 Provenance preservation | Mandatory | Mandatory | Mandatory | Mandatory |
| RSEC-10 Tip explainability links | Mandatory per member | Mandatory per member | Mandatory per member | Mandatory per member (or empty-set path) |

**Empty-set rule:** When RAC-01 is empty, RSEC-01 records explicit emptiness; RSEC-07 / RSEC-08 must explain non-invention; RSEC-10 may be `none` because no members exist.

---

## 4. Component Definitions

### 4.1 RSEC-01 — Constituent Recommendations

| Audience | Representation |
|----------|----------------|
| Student | Speakable list / grouping of guidance with clear primary when disposition applies |
| Developer | Identities / references for each MS001-complete constituent (or `constituents=[]`) |

Must match [`../recommendation_assembly/ASSEMBLY_COMPONENTS.md`](../recommendation_assembly/ASSEMBLY_COMPONENTS.md) RAC-01. Invented members and incomplete slogans are unlawful (RSEP-02 / RSEP-08).

### 4.2 RSEC-02 — Contributing Constitutional Sources

The closed catalogue of constitutional source classes (and underlying artefacts) that contributed — reconstructed without undocumented provenance.

| Typical citations | When |
|-------------------|------|
| ERS-01 Programme VI artefacts | Meaning contributors |
| ERS-02 workflow / event warrants | Orchestration situating |
| ERS-03 ownership artefacts | Authority refs |
| ERS-04 disposition artefacts | Conflict outcomes |
| ERS-05 evidence artefacts | Supporting warrants |
| ERS-06 / ERS-07 | Additional published source classes when applicable |

Student speech paraphrases (“Study Plan and today’s coaching”). Developer speech cites ERS classes and artefact refs. Recommendation Assembly / Recommendation Engine must **not** appear as a meaning contributor.

### 4.3 RSEC-03 — Recommendation Owners

| Audience | Representation |
|----------|----------------|
| Student | Plain educational voices (“day coach”, “recovery coaching”, …) |
| Developer | `owners=[AD-0x → constituent_id, …]` ownership index |

Must match Authority Model domains and RAC-03. Fiction owners (“the algorithm”, “the set”, unnamed “system”) are unlawful (RSEP-03).

**Hard rule:** There is no constitutional “set owner” that absorbs constituent domains.

### 4.4 RSEC-04 — Workflow Context

Coordination facts that explain *why this recommendation set is live in this moment* without becoming educational meaning for any constituent.

| Student cue | Developer cue |
|-------------|----------------|
| “You’ve returned to study…” / “We’re switching focus because…” | `workflow_context={event, stage, participation_ref}` or `none` |
| Escalate before set | `workflow_context=escalate_to_planning` |

When no orchestration situating applies, record explicit `workflow_context=none`. Do not invent workflow drama for rhetorical effect.

### 4.5 RSEC-05 — Conflict Disposition References

When concurrency applied: published RO outcomes (and CT/RP when material for audits). When not: explicit `conflict_dispositions=none`.

| Student cue | Developer cue |
|-------------|----------------|
| “Recovery leads; today’s ordinary priority waits.” | `dispositions={constituent → RO-xx}; conflict_types=[CT-…]` |
| Ordinary non-concurrent package | `conflict_dispositions=none` |

Do not invent dispositions for packaging convenience. Do not hide real concurrency.

### 4.6 RSEC-06 — Constitutional Evidence References

Honest Educational Evidence / warrant references at set and/or constituent grain — including explicit thin-evidence or none when true.

| Lawful narration | Unlawful narration |
|------------------|--------------------|
| “Given what your recent study showed…” | “Because you opened the card, we know you understand…” |
| `evidence_refs=[…]; thin_evidence=true` | Reclassify Evidence inside set speech |
| Explicit `evidence_refs=none` with limit honesty | Invent observations to fill the package |

Evidence meaning remains owned by the Evidence Model / Pipeline. Set speech references; it does not reinterpret.

### 4.7 RSEC-07 — Assembly Warrant

Answers RSEQ1 / RSEQ2: why this package exists and how members were organised under MS002.

| Student pattern | Developer pattern |
|-----------------|-------------------|
| “These tips already apply; we show them together so the priority is clear.” | `assembly_warrant=organise_lawful_members; rac_completeness=pass` |
| “There isn’t a recommendation set yet — we won’t invent filler.” | `assembly_warrant=empty_set_honesty; invention_refused=true` |

Assembly warrant must not claim educational certainty beyond constituents and EIP limits.

### 4.8 RSEC-08 — Interpretation Posture

Answers RSEQ3: how to read the set.

| Posture family | Student emphasis | Developer emphasis |
|----------------|------------------|--------------------|
| Single-member | “This is the live guidance right now.” | `interpretation=identity; fabricated_siblings=false` |
| Multi-coach coherent | “These support the same Study Plan — not competing guesses.” | `interpretation=coherent_siblings; dual_primary=false` |
| Post-disposition | “This leads; that waits.” | `interpretation=disposition_aware; primary=…; waiting=[…]` |
| Empty / escalate | “We shouldn’t invent tips yet.” | `interpretation=non_invention; escalate_or_refuse=…` |
| Limits | “We don’t claim more than this.” | `limits=[thin_evidence|plan_non_mutation|…]` |

Interpretation posture must never redefine meaning or transfer ownership.

### 4.9 RSEC-09 — Provenance Preservation Record

Answers RSEQ4: confirmation that packaging did not erase or rewrite constitutional history.

```
provenance_preservation:
  sources_intact: true
  owners_intact: true
  evidence_refs_intact: true
  constitutional_refs_intact: true
  dispositions_unmutated: true | n/a
  meaning_unrewritten: true
```

Student speech may be implicit honesty (“we’re not inventing a new tip by combining coaches”). Developer speech must make the record explicit.

### 4.10 RSEC-10 — Tip-Level Explainability Linkage

Each material constituent must remain explainable under WS3 / MS001 ERQ-01…ERQ-05. Set speech does not replace tip speech.

| Audience | Representation |
|----------|----------------|
| Student | Per-tip “why this guidance…” available when the tip is material |
| Developer | `tip_explainability_refs=[constituent → RECOMMENDATION_EXPLAINABILITY / Programme VI refs]` |

For empty sets: `tip_explainability_refs=none`.

---

## 5. Minimal Audit Record (Conceptual)

Documentation and future implementations should be able to reconstruct at least:

```
recommendation_set_id: …                    # conceptual identity only
constituents: […] | []                      # RSEC-01
contributing_sources: [ERS-… → artefacts]   # RSEC-02
owners: [AD-0x → constituent, …]            # RSEC-03
workflow_context: none | {…}                # RSEC-04
conflict_dispositions: none | {… → RO-xx}   # RSEC-05
evidence_references: […] | none             # RSEC-06
assembly_warrant: …                         # RSEC-07
interpretation_posture: …                   # RSEC-08
provenance_preservation: {…}                # RSEC-09
tip_explainability_refs: […] | none         # RSEC-10
rseq_answers:
  RSEQ1: …
  RSEQ2: …
  RSEQ3: …
  RSEQ4: …
assembly_ms002_ref: ASSEMBLY_EXPLAINABILITY.md#RAQ-01-RAQ-04
authority_explainability_ref: null | …
resolution_explainability_ref: null | …
workflow_explainability_ref: null | …
```

This is a **constitutional audit shape**, not a database schema. Persistence design is out of scope for MS003.

---

## 6. Relationship to Sibling Contracts

| Sibling | How components relate |
|---------|------------------------|
| MS002 RAC-01…RAC-07 | RSEC-01…RSEC-06 narrate the same constitutional facts RAC requires; RSEC-07…RSEC-10 specialise explanation obligations |
| MS002 RAQ-01…RAQ-04 | Satisfiable whenever RSEQ1…RSEQ4 are answered faithfully |
| MS001 ERQ-01…ERQ-05 | Required per member via RSEC-10 |
| WS2 Authority Decision Explainability | Optional permission speech when ownership narration is material; never substitutes for RSEC-03 |
| WS2 Resolution Explainability | When RSEC-05 is non-none, RQ1–RQ4 must also be satisfiable |
| WS1 workflow explainability | Feeds RSEC-04; never substitutes for tip owners |

---

## 7. Completeness Checklist

Before shipping student- or developer-facing recommendation-set narration, confirm:

- [ ] RSEQ1–RSEQ4 answered for the audience
- [ ] RSEC-01…RSEC-10 present (or explicit `none` where allowed)
- [ ] Constituents are MS001-complete (or explicit empty set)
- [ ] Owners match Authority Model; no set-owner absorption
- [ ] Sources and evidence refs reconstructable; no undocumented provenance
- [ ] Conflict dispositions (if any) cite published RO/CT/RP only
- [ ] Workflow context (if any) is situating, not tip ownership
- [ ] Each material tip also satisfies ERQ-01…ERQ-05
- [ ] No scoring / optimiser / job-queue jargon presented as constitutional set warrant

---

## 8. Closing

Components make recommendation-set explanations auditable: **constituents, sources, owners, workflow context, dispositions, evidence refs, assembly warrant, interpretation posture, provenance preservation, and tip-level links.**

> **If a component is missing, the explanation is not yet constitutional.**
