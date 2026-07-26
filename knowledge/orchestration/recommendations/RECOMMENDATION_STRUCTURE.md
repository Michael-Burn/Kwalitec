# Recommendation Structure

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS001 — Educational Recommendation Model  
**Classification:** Constitutional components of an educational recommendation  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional components** every educational recommendation must carry.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`EDUCATIONAL_RECOMMENDATION_MODEL.md`](EDUCATIONAL_RECOMMENDATION_MODEL.md)
3. [`RECOMMENDATION_OBJECTIVES.md`](RECOMMENDATION_OBJECTIVES.md)
4. [`RECOMMENDATION_SOURCES.md`](RECOMMENDATION_SOURCES.md)
5. [`../authority/AUTHORITY_DOMAINS.md`](../authority/AUTHORITY_DOMAINS.md)
6. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)

> **Structure makes a tip auditable.  
> Incomplete packaging is not a constitutional recommendation.**

---

## 1. Purpose

An expert tutor’s advice is not a naked slogan. It names what to do, who is speaking educationally, what observations support the advice, under what situation it applies, and which rules make it valid.

This document closes the **component catalogue** so Runtime A and product surfaces cannot ship half-formed tips as constitutional guidance.

---

## 2. Component Catalogue

| ID | Component | One-line definition |
|----|-----------|---------------------|
| **ERC-01** | Educational guidance | Speakable lawful next-step or posture |
| **ERC-02** | Constitutional owner | Named accountable component for the decision |
| **ERC-03** | Supporting educational evidence | Honest warrants for asserted claims |
| **ERC-04** | Orchestration context | Workflow / coordination situating facts |
| **ERC-05** | Applicable constitutional references | Documented law establishing validity |
| **ERC-06** | Disposition status | Acted-upon / deferred / … when concurrency applies |
| **ERC-07** | Claim & limit honesty | Claim types and explicit limits / refusals |

Additional components may be added only by amending this document.

---

## 3. ERC-01 — Educational Guidance

**Definition.** The primary communicative content: what the student may lawfully treat as the recommended educational action or posture *now* (including refuse / wait / escalate postures).

| Property | Requirement |
|----------|-------------|
| Source | Primarily ERS-01; refuse/escalate may be WS1/WS2 outcomes with no new coach tip |
| Must | Be faithful to the owning Programme VI artefact’s meaning |
| Must not | Invent tips, average coaches, or overclaim outcomes |
| Student form | Plain educational speech |
| Developer form | Reference to the underlying Programme VI artefact / outcome class |

**Examples (illustrative):**

- “Today, prioritise consolidating Topic X under your Study Plan.”
- “Focus on restoring a sustainable study rhythm before ordinary daily load.”
- “We should adjust your Study Plan before inventing a new daily tip.”
- “No exam-style focus yet — first learning remains primary.”

---

## 4. ERC-02 — Constitutional Owner

**Definition.** The named constitutional component that owns the educational decision class for this guidance (Authority Model domain owner).

| Property | Requirement |
|----------|-------------|
| Source | ERS-03 |
| Must | Name exactly one owner for the primary educational decision |
| Must not | Attribute ownership to UI, Recommendation Engine, Workflow Engine (for meaning), or “the system” |
| Distinct from | Delegated *exercise* under owner warrant — delegation must still name the owner |

**Examples:**

- Owner: Daily Coach  
- Owner: Recovery Coach (Daily Coach consumes, does not own recovery warrant)  
- Owner: Master Planner (structural envelope)

---

## 5. ERC-03 — Supporting Educational Evidence

**Definition.** Observational evidence and permitted estimate inputs that warrant the guidance’s educational claims, with honest claim typing.

| Property | Requirement |
|----------|-------------|
| Source | ERS-05 (and thin-evidence acknowledgements when warrants are weak) |
| Must | Distinguish observation vs estimate; coverage ≠ understanding ≠ mastery |
| Must not | Fabricate evidence; reinterpret evidence classes; mute contradictions silently |
| May be empty of strong warrants | Only if guidance explicitly speaks thin-evidence / refuse / escalate limits |

---

## 6. ERC-04 — Orchestration Context

**Definition.** Coordination facts that explain *why this guidance is live in this moment* without becoming the educational meaning itself.

| Property | Requirement |
|----------|-------------|
| Source | ERS-02 (and ERS-06 plan/profile envelope as consumed inputs) |
| Must | Include initiating/continuing educational situation at student-meaningful grain |
| Must | Preserve authority: orchestration invited the owner; it did not answer the educational question |
| Must not | Claim workflow completion as learning success; invent stages |

**Typical contextual elements:**

- Educational event class (student-facing reason)
- Primary authority selected
- Handoff / refuse / escalate class when applicable
- Plan envelope (“inside your Study Plan”)

---

## 7. ERC-05 — Applicable Constitutional References

**Definition.** Explicit references to governing documents and principles that make the artefact constitutionally valid.

| Property | Requirement |
|----------|-------------|
| Source | ERS-07 |
| Must | Be reconstructable for developers / auditors |
| May | Be omitted from student-facing copy while remaining faithful underneath |
| Must not | Cite unpublished heuristics as constitutional law |

**Minimum developer reference set (illustrative):**

- Owning Programme VI model document
- Authority domain / principle supporting the owner
- This Recommendation Model + applicable ERO/ERS/ERC IDs
- EIP-003 / EL-008 where speech claims are material

---

## 8. ERC-06 — Disposition Status

**Definition.** When Conflict Resolution applied, the lawful disposition of this artefact and of material siblings (RO-01…RO-06).

| Property | Requirement |
|----------|-------------|
| Source | ERS-04 |
| Required when | Concurrent valid recommendations competed for action |
| Optional when | Single valid recommendation with no concurrency |
| Must | Name acted-upon vs deferred / superseded / queued / merged / rejected-as-unlawful as applicable |
| Must not | Hide that a sibling tip remains valid but not primary |

---

## 9. ERC-07 — Claim & Limit Honesty

**Definition.** Explicit statement of claim types and limits: what is known, what is estimated, what is not claimed, and when guidance refuses or waits.

| Property | Requirement |
|----------|-------------|
| Source | EIP-003 / EIP-006 posture + owning Programme VI honesty rules |
| Must | Prevent certainty theatre and mastery minting from tip packaging |
| Must | Allow “no recommendation” as a first-class structured outcome |
| Must not | Use motivational language to invent educational certainty |

---

## 10. Completeness Rules

A tip may be treated as a **constitutional educational recommendation** only if:

| Rule | Requirement |
|------|-------------|
| **C1** | ERC-01 present (guidance or explicit no-recommendation posture) |
| **C2** | ERC-02 present (named owner) — except pure orchestration refuse/escalate with named escalation owner |
| **C3** | ERC-03 present or ERC-07 explicitly records thin/absent evidence limits |
| **C4** | ERC-04 present for orchestrated student-facing primary guidance |
| **C5** | ERC-05 reconstructable for audit |
| **C6** | ERC-06 present whenever concurrency was dispositioned |
| **C7** | ERC-07 present for every material student-facing recommendation |

Failure of any required rule → **not** a constitutional recommendation (may still be internal debug noise; must not be student-facing as coach advice).

---

## 11. Structural Sketch (Non-Normative Shape)

The following sketch illustrates composition. It is **not** an API schema, database model, or serialisation contract (those remain out of scope).

```
ConstitutionalEducationalRecommendation
├── guidance            (ERC-01)  ← Programme VI meaning (or refuse/escalate posture)
├── owner               (ERC-02)  ← Authority Model domain owner
├── evidence            (ERC-03)  ← EIP-002 / EIP-006 honest warrants
├── orchestration       (ERC-04)  ← WS1 context
├── constitutional_refs (ERC-05)  ← validity law
├── disposition         (ERC-06)  ← WS2 / MS002 when concurrency
└── claim_limits        (ERC-07)  ← honesty / refusal / thin evidence
```

Implementations may store or render these components differently. They may not drop required meaning.

---

## 12. Aggregation vs Invention

| Lawful aggregation | Unlawful invention |
|--------------------|--------------------|
| Attach WS1 context to a Daily Coach artefact | Invent a daily tip from context alone |
| Attach owner + evidence to Recovery guidance | Mint recovery advice from login streaks |
| Attach RO-06 disposition after conflict | Average two coaches into a third tip without RO-03 |
| Unify components into one speakable artefact | Merge meanings across domains to “simplify UX” |

Unification (ERO-03) operates on **components**. It does not create **meaning**.

---

## 13. Closing

Structure is how recommendations stay tutor-honest under product pressure.

When a surface wants to show only ERC-01, **add the missing components or refuse**.  
When aggregation would rewrite ERC-01 meaning, **stop** — amend Programme VI or apply Conflict Resolution, do not restructure by reinterpretation.

> **No owner, no evidence honesty, no constitutional recommendation.**
