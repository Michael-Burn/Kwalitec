# Resolution Principles

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS002 — Conflict Resolution Framework  
**Classification:** Binding constitutional principles for educational conflict resolution  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional principles** used to resolve educational conflicts among simultaneously valid recommendations.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONFLICT_RESOLUTION_FRAMEWORK.md`](CONFLICT_RESOLUTION_FRAMEWORK.md)
3. [`CONFLICT_TYPES.md`](CONFLICT_TYPES.md)
4. [`../authority/AUTHORITY_PRINCIPLES.md`](../authority/AUTHORITY_PRINCIPLES.md) — ownership principles this Framework must not violate
5. [`../authority/AUTHORITY_BOUNDARIES.md`](../authority/AUTHORITY_BOUNDARIES.md) — hard limits that constrain outcomes
6. Programme VI meaning corpora — meanings that resolution must not rewrite
7. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md) — orchestration must not invent winners’ meanings

> **Conflicts resolve through constitutional rules rather than runtime discretion.**

---

## 1. Purpose

Principles prevent conflict resolution from becoming a quiet empire: a “conflict engine” that picks winners by score, merges coaches into one voice, or transfers ownership “until things calm down.”

These principles bind every educational conflict path — documentation, design, and future Runtime A behaviour. They deliberately **do not** specify implementation algorithms, weights, or schedulers.

---

## 2. Principle Catalogue

| ID | Principle | One-line rule |
|----|-----------|---------------|
| **RP-01** | Ownership preserved | Resolution never transfers decision ownership |
| **RP-02** | Educational meaning unchanged | Resolution disposes action; it does not rewrite meaning |
| **RP-03** | Higher obligations precede concurrency | Explicit constitutional obligations outrank ordinary coach concurrency |
| **RP-04** | Rule-bound resolution | Published rules decide; runtime discretion does not |
| **RP-05** | Valid peers only | Only constitutionally valid artefacts enter peer resolution |
| **RP-06** | Single primary action | At most one primary acted-upon outcome per coordination moment (unless a published merge pathway applies) |
| **RP-07** | Non-acted artefacts remain lawful | Deferred, queued, or superseded artefacts keep owner and meaning |
| **RP-08** | Ownership disputes refuse | Competing ownership claims are not resolved here |
| **RP-09** | Orchestration non-education | Workflow timing may surface conflicts; it may not invent educational winners |
| **RP-10** | Explainable disposition | Material resolutions must cite conflict, rules, outcome, and preservation |

---

## 3. RP-01 — Ownership Is Preserved

**Rule:** Conflict resolution may change which recommendation is **acted upon**. It may **never** transfer, invent, or amend constitutional decision ownership.

| Lawful | Unlawful |
|--------|----------|
| Recovery’s recommendation is acted upon; Daily remains owner of day-priority decisions | Recovery “temporarily owns” Daily Coach’s domain |
| Revision informs day priority; Daily still owns today’s primary decision class | Conflict outcome reassigns AD domains |
| Temporary primary focus governs action; standing owners remain owners | AP-04 delegation treated as permanent transfer |

**Relationship to MS001:** RP-01 is the conflict-face of AP-04 / AP-06 / AP-07. Resolution implements *action selection*; Authority Model remains the ownership map.

---

## 4. RP-02 — Educational Meaning Is Unchanged

**Rule:** The resolution act does not reinterpret, rewrite, or silently edit Programme VI educational meanings or the substance of already-emitted recommendations.

| Lawful | Unlawful |
|--------|----------|
| Defer Topic A’s day recommendation while recovery leads | Rewrite Topic A’s warrant to “not really needed” so conflict disappears |
| Supersede *action* on an earlier tip; keep its meaning on record | Relabel Recovery as Revision to simplify the story |
| Queue a revision warrant for after recovery | Absorb revision meaning into a generic “study tip” |

**Meaning invariance tests:**

1. After resolution, can each artefact still be explained under its Programme VI owner’s explainability contract?
2. Did any coach meaning change *because of* the conflict step alone?
3. If yes to (2), the resolution violated RP-02 — refuse or amend Programme VI corpora first.

---

## 5. RP-03 — Higher Constitutional Obligations Take Precedence

**Rule:** Where the Educational Constitution, Evidence Model, Continuity Standard, Authority Boundaries, or other **explicitly defined** higher obligations constrain action, those obligations **precede** ordinary concurrency among coach recommendations.

| Higher obligation (examples) | Precedence effect |
|------------------------------|-------------------|
| Evidence honesty / non-reinterpretation (AB-03) | Cannot “resolve” by relabelling evidence |
| Plan non-mutation outside Master Planner / Scheduling (AB-02) | Cannot resolve by rewriting the Canonical Study Plan |
| Continuity (EIP-005) | Cannot erase history to make concurrency disappear |
| Domain non-overclaim (AB-04) / no independent tips (AB-05) | Cannot invent a meta-recommendation as the winner |
| Explicit temporary primary / handoff already authorised under MS001 | Temporary primary may lawfully precede standing day action (CT-03) without ownership transfer |

**Important:** RP-03 does **not** invent a free-form priority ladder among coaches (e.g. “Exam always beats Daily”). Precedence applies only where **explicitly defined** in constitutional corpora. Informal tribal precedence is not RP-03.

| Lawful | Unlawful |
|--------|----------|
| Apply AB-02: refuse plan rewrite as a conflict shortcut | Invent “Recovery always wins” without constitutional warrant |
| Apply temporary primary already published under Authority Principles | Invent a scoring hierarchy among AD-02…AD-06 in this document |
| Pause when evidence is missing (WS1 await) rather than fabricate | Rank coaches by optimiser confidence |

---

## 6. RP-04 — Conflicts Resolve Through Constitutional Rules, Not Runtime Discretion

**Rule:** The lawful outcome class is determined by **published** conflict types, these principles, and `RESOLUTION_OUTCOMES.md` — not by operator preference, UI proximity, performance, A/B whim, or undocumented “tutor instinct” in code.

| Lawful | Unlawful |
|--------|----------|
| Same CT-xx + same applicable RPs ⇒ same outcome *class* | Same situation yields different winners depending on which service ran last |
| Amend this corpus when a new rule is needed | Encode discretionary arbitration in Runtime A and call it “policy” |
| Refuse when rules do not yet cover the case | Invent an ad-hoc merge to ship a tip |

**Determinism of class, not of algorithm:** This principle requires **constitutional determinism of outcome class** (defer / supersede / queue / merge-where-permitted / reject). It does **not** authorise or describe scoring algorithms. Implementation may later encode these rules; it may not replace them with discretion.

---

## 7. RP-05 — Valid Peers Only

**Rule:** Peer resolution applies only among artefacts that are each constitutionally valid. Unlawful, out-of-domain, or ownerless claims are **rejected** (RO-05), not ranked against valid peers.

| Lawful | Unlawful |
|--------|----------|
| Exclude a Workflow Engine “independent tip” from peer set; reject it | Averaging an unlawful tip with Daily Coach’s recommendation |
| Require Programme VI warrant before an artefact enters CT-01 | Treating Version 2 Adaptive output as a Programme VI peer by proximity |

---

## 8. RP-06 — Single Primary Action

**Rule:** For a given coordination moment, at most **one** primary acted-upon educational outcome is presented as the student’s leading guidance — unless a **published constitutional merge pathway** explicitly permits a composite (see RO-03).

| Lawful | Unlawful |
|--------|----------|
| One primary; others deferred or queued | Two “equal primary” tips that leave the student to invent priority |
| Explicit permitted merge that names both owners and the composite’s warrant | Silent mega-tip that collapses Recovery + Revision + Daily into one unnamed voice (AB-08) |

**Single primary ≠ single owner forever.** Other domains remain owners of their deferred artefacts.

---

## 9. RP-07 — Non-Acted Artefacts Remain Lawful

**Rule:** Recommendations that are deferred, queued, or superseded for *action* remain constitutionally valid under their owners. Disposition of action is not invalidation of meaning or ownership.

| Lawful | Unlawful |
|--------|----------|
| “Revision warrant stands; recovery leads today” | “Revision was wrong because recovery won” |
| Queue for a later lawful window | Delete or rewrite the queued artefact’s educational substance |
| Record supersession of action with preservation | Treat supersession as erasure of the earlier owner |

---

## 10. RP-08 — Ownership Disputes Are Refused, Not Resolved Here

**Rule:** If two components claim the same decision class, the situation is **not** a CT-xx peer conflict. Refuse resolution-as-arbitration; name AP-01; consult / amend the Authority Model.

| Lawful | Unlawful |
|--------|----------|
| Refuse dual ownership of “what to do today” | “Resolve” by letting both own it equally |
| Amend `AUTHORITY_DOMAINS.md` if a new class is truly needed | Invent a conflict-engine owner of last resort |

---

## 11. RP-09 — Orchestration Non-Education

**Rule:** Workflow Engine timing, stage movement, and concurrency surfacing may create CT-05 situations. Orchestration may **not** invent educational meaning, modify coach recommendations, or claim ownership of the educational winner.

| Lawful | Unlawful |
|--------|----------|
| Surface concurrent valid outputs for MS002 disposition | Emit an independent “workflow tip” as the winner |
| Pause / await when outputs are missing | Advance stages by fabricating a recommendation to clear the conflict |

---

## 12. RP-10 — Explainable Disposition

**Rule:** Every material conflict resolution must be explainable per `RESOLUTION_EXPLAINABILITY.md`: why the conflict existed, which rules applied, why the outcome was lawful, and how ownership was preserved.

| Lawful | Unlawful |
|--------|----------|
| Student hears which guidance leads and what waits | Opaque “the system decided” |
| Developer trace cites CT-xx, RP-xx, RO-xx, owners preserved | Score vectors presented as educational law |

---

## 13. Application Order (Constitutional, Not Algorithmic)

When resolving a classified conflict, apply principles in this **constitutional order of consideration** (not a scoring pipeline):

1. **RP-08** — If ownership is disputed → refuse; stop.
2. **RP-05** — Remove / reject unlawful artefacts.
3. **RP-03** — Apply any explicit higher obligations that constrain action.
4. **RP-01 / RP-02** — Ensure candidate outcomes preserve ownership and meaning.
5. **RP-06 / RP-07** — Select a single primary acted-upon outcome (or permitted merge); disposition others lawfully.
6. **RP-04 / RP-09** — Confirm the selection is rule-bound and not orchestration invention.
7. **RP-10** — Record explainability.

This order is a **discipline of constitutional checks**. It is not an invitation to invent numeric priorities among coaches.

---

## 14. Closing

Resolution principles keep concurrency honest: **select action, preserve owners, leave meaning intact, obey published higher obligations, refuse discretion.**

> **Rules resolve conflicts. Ownership and meaning survive them.**
