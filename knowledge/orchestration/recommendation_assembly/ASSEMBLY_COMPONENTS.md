# Assembly Components

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS002 — Recommendation Assembly Framework  
**Classification:** Constitutional components of an assembled recommendation set  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional components** every assembled educational recommendation set must carry.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RECOMMENDATION_ASSEMBLY_FRAMEWORK.md`](RECOMMENDATION_ASSEMBLY_FRAMEWORK.md)
3. [`ASSEMBLY_OBJECTIVES.md`](ASSEMBLY_OBJECTIVES.md)
4. [`../recommendations/RECOMMENDATION_STRUCTURE.md`](../recommendations/RECOMMENDATION_STRUCTURE.md)
5. [`../recommendations/RECOMMENDATION_SOURCES.md`](../recommendations/RECOMMENDATION_SOURCES.md)
6. [`../authority/AUTHORITY_DOMAINS.md`](../authority/AUTHORITY_DOMAINS.md)
7. [`../conflict_resolution/RESOLUTION_OUTCOMES.md`](../conflict_resolution/RESOLUTION_OUTCOMES.md)
8. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)

> **Set structure makes multi-tip packaging auditable.  
> Incomplete packaging is not a constitutional recommendation set.**

---

## 1. Purpose

An expert tutor’s multi-part advice is not a naked list of slogans. It names which pieces of guidance belong together, who speaks for each, what warrants support them, under what orchestration they are live, and how conflict disposition (if any) situates their relationship.

This document closes the **set-component catalogue** so Runtime A and product surfaces cannot ship half-formed tip batches as constitutional recommendation sets.

---

## 2. Component Catalogue

| ID | Component | One-line definition |
|----|-----------|---------------------|
| **RAC-01** | Constituent recommendations | Lawful WS3 / MS001 artefacts that form the set |
| **RAC-02** | Contributing constitutional sources | Documented sources that contributed to the set and its members |
| **RAC-03** | Ownership references | Named constitutional owners for each constituent (and set-level index) |
| **RAC-04** | Workflow context | Orchestration situating facts for why this set is live now |
| **RAC-05** | Conflict disposition references | RO outcomes / disposition facts when concurrency applied |
| **RAC-06** | Supporting educational evidence | Honest warrants referenced at set and/or constituent grain |
| **RAC-07** | Set coherence & limit honesty | Consistency posture, membership honesty, and explicit limits |

Additional components may be added only by amending this document.

---

## 3. RAC-01 — Constituent Recommendations

**Definition.** The ordered or grouped collection of constitutional educational recommendations that are members of the set — each satisfying WS3 / MS001 structure completeness (C1–C7), or an explicit empty-set posture when no lawful member exists.

| Property | Requirement |
|----------|-------------|
| Source | WS3 / MS001 artefacts derived under ERS catalogue |
| Must | Admit only constitutionally complete recommendations (or explicit empty set) |
| Must | Preserve each member’s ERC-01…ERC-07 meaning intact |
| Must not | Invent members, average coaches into a synthetic member, or admit incomplete slogans |
| May | Contain a single member — single-member sets are lawful |
| Student form | Speakable list / grouping of guidance with clear primary when disposition applies |
| Developer form | Identities / references for each constituent artefact |

**Examples (illustrative):**

- Set of one: Daily Coach primary tip under Active Study Plan.
- Set of two: Recovery acted-upon primary + Daily deferred sibling after RO disposition.
- Empty set: no Programme VI warrant yet — “no recommendation set members.”

---

## 4. RAC-02 — Contributing Constitutional Sources

**Definition.** The closed catalogue of constitutional source classes (and underlying artefacts) that contributed to the set’s organisation and to its constituents — reconstructed without undocumented provenance.

| Property | Requirement |
|----------|-------------|
| Source | [`../recommendations/RECOMMENDATION_SOURCES.md`](../recommendations/RECOMMENDATION_SOURCES.md) (ERS-01…ERS-07) |
| Must | List contributing ERS classes for the set and map them to constituents |
| Must not | Cite engagement metrics, A/B winners, or unpublished heuristics as sources |
| Must | Distinguish meaning sources (ERS-01) from context / ownership / disposition / evidence sources |

**Typical contribution map:**

| ERS class | Set-level role |
|-----------|----------------|
| ERS-01 | Meaning of each constituent |
| ERS-02 | Why the set is live in this orchestration moment |
| ERS-03 | Ownership references for constituents |
| ERS-04 | Conflict disposition references when concurrency applied |
| ERS-05 | Supporting evidence referenced by constituents / set honesty |
| ERS-06 | Plan / profile envelope constraining the set |
| ERS-07 | Constitutional validity references for audit |

---

## 5. RAC-03 — Ownership References

**Definition.** Explicit references naming the constitutional owner of each constituent recommendation, plus a set-level ownership index that never invents a set owner that absorbs members.

| Property | Requirement |
|----------|-------------|
| Source | ERS-03 / ERC-02 / Authority Model domains |
| Must | Name exactly one owner per constituent’s primary educational decision |
| Must not | Attribute set ownership to Recommendation Engine, UI, Workflow Engine (for meaning), or “the system” |
| May | Present a set-level index of owners for explainability — index ≠ transfer of ownership |
| Distinct from | Acted-upon primary (disposition) — primary action ≠ new owner |

**Examples:**

- Constituent A owner: Recovery Coach  
- Constituent B owner: Daily Coach (deferred)  
- Set index: Recovery leading; Daily waiting — owners unchanged

---

## 6. RAC-04 — Workflow Context

**Definition.** Coordination facts that explain *why this recommendation set is live in this moment* without becoming educational meaning for any constituent.

| Property | Requirement |
|----------|-------------|
| Source | ERS-02 (and ERS-06 plan/profile envelope as consumed inputs) |
| Must | Include initiating/continuing educational situation at student-meaningful grain when the set is student-facing primary packaging |
| Must | Preserve authority: orchestration invited owners; it did not answer educational questions |
| Must not | Claim workflow completion as learning success; invent stages; substitute context for Programme VI meaning |

**Typical contextual elements:**

- Educational event class (student-facing reason the set is relevant)
- Primary authority / participation posture selected by workflow
- Handoff / refuse / escalate class when applicable
- Plan envelope (“inside your Study Plan”)

---

## 7. RAC-05 — Conflict Disposition References

**Definition.** When Conflict Resolution applied, explicit references to the lawful disposition of each material constituent and of the set’s primary-action posture (RO-01…RO-06).

| Property | Requirement |
|----------|-------------|
| Source | ERS-04 / ERC-06 / [`../conflict_resolution/RESOLUTION_OUTCOMES.md`](../conflict_resolution/RESOLUTION_OUTCOMES.md) |
| Required when | Concurrent valid recommendations competed for action |
| Optional when | Single valid recommendation with no concurrency |
| Must | Name acted-upon vs deferred / superseded / queued / merged / rejected-as-unlawful as applicable |
| Must not | Invent a new disposition; hide that a sibling tip remains valid but not primary; rank winners by assembly fiat |

**Assembly role:** *reference and organise*.  
**Conflict Resolution role:** *decide disposition*.  
Confusing these roles is an architectural defect.

---

## 8. RAC-06 — Supporting Educational Evidence

**Definition.** Observational evidence and permitted estimate inputs that warrant the educational claims of constituents (and any set-level honesty statements), with claim-type fidelity.

| Property | Requirement |
|----------|-------------|
| Source | ERS-05 / ERC-03 (and thin-evidence acknowledgements via ERC-07) |
| Must | Preserve observation vs estimate; coverage ≠ understanding ≠ mastery |
| Must not | Fabricate evidence at set scale; reinterpret evidence classes; mute contradictions silently across members |
| May | Present a set-level evidence index that points to constituent warrants — index ≠ new evidence |

---

## 9. RAC-07 — Set Coherence & Limit Honesty

**Definition.** Explicit statement of set coherence: membership honesty, primary-action posture, material sibling visibility, claim limits, and when the set refuses or waits.

| Property | Requirement |
|----------|-------------|
| Source | RAO-04 consistency + EIP-003 / EIP-006 honesty + owning Programme VI honesty rules |
| Must | Prevent dual-primary theatre and mastery minting from set packaging |
| Must | Allow empty set and single-member set as first-class structured outcomes |
| Must not | Use motivational language to invent educational certainty or invent missing members |

---

## 10. Completeness Rules

A package may be treated as a **constitutional educational recommendation set** only if:

| Rule | Requirement |
|------|-------------|
| **S1** | RAC-01 present (one or more complete constituents, or explicit empty-set posture) |
| **S2** | RAC-02 reconstructable (contributing sources mapped) |
| **S3** | RAC-03 present for every constituent member |
| **S4** | RAC-04 present for orchestrated student-facing primary sets |
| **S5** | RAC-05 present whenever concurrency was dispositioned |
| **S6** | RAC-06 present or RAC-07 explicitly records thin/absent evidence limits across material members |
| **S7** | RAC-07 present for every material student-facing set |

Failure of any required rule → **not** a constitutional recommendation set (may still be internal debug noise; must not be student-facing as coach packaging).

---

## 11. Structural Sketch (Non-Normative Shape)

The following sketch illustrates composition. It is **not** an API schema, database model, or serialisation contract (those remain out of scope).

```
ConstitutionalEducationalRecommendationSet
├── constituents            (RAC-01)  ← WS3 / MS001 artefacts (0..n)
│     └── each: guidance, owner, evidence, orchestration, refs, disposition, limits
├── contributing_sources    (RAC-02)  ← ERS-01…ERS-07 contribution map
├── ownership_references    (RAC-03)  ← per-constituent owners + set index
├── workflow_context        (RAC-04)  ← WS1 situating facts
├── conflict_disposition    (RAC-05)  ← WS2 / MS002 RO refs when concurrency
├── supporting_evidence     (RAC-06)  ← EIP-002 / EIP-006 honest warrants / index
└── coherence_limits        (RAC-07)  ← consistency · emptiness · honesty
```

Implementations may store or render these components differently. They may not drop required meaning.

---

## 12. Assembly vs Unification vs Invention

| Lawful assembly (MS002) | Lawful unification (MS001 ERO-03) | Unlawful invention |
|-------------------------|-----------------------------------|--------------------|
| Organise multiple complete tips into one set | Compose ERC components into one tip | Invent a tip with no ERS-01 warrant |
| Attach disposition refs after WS2 / MS002 | Attach ERC-06 on a single artefact | Average two coaches into a third tip without RO-03 |
| Index owners without absorbing them | Name ERC-02 on one artefact | Claim Recommendation Engine owns the set |
| Preserve each tip’s provenance | Preserve one tip’s provenance | Erase sources while “simplifying UX” |

**MS001 unifies components of one recommendation.**  
**MS002 assembles multiple recommendations into a set.**  
Neither creates educational meaning.

---

## 13. Closing

Set structure is how multi-recommendation packaging stays tutor-honest under product pressure.

When a surface wants to show only tip slogans, **add the missing set components or refuse**.  
When assembly would rewrite a constituent’s ERC-01 meaning, **stop** — amend Programme VI or apply Conflict Resolution, do not restructure by reinterpretation.

> **No lawful constituents, no ownership fidelity, no constitutional recommendation set.**
