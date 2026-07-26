# Explanation Components

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS003 — Authority Decision Explainability  
**Classification:** Mandatory information set for authority decision explanations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document catalogues the **information every material authority explanation should contain**.

Subordinate to:

1. [`AUTHORITY_DECISION_EXPLAINABILITY.md`](AUTHORITY_DECISION_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`../authority/AUTHORITY_DOMAINS.md`](../authority/AUTHORITY_DOMAINS.md)
4. [`../authority/AUTHORITY_PRINCIPLES.md`](../authority/AUTHORITY_PRINCIPLES.md)
5. [`../authority/AUTHORITY_BOUNDARIES.md`](../authority/AUTHORITY_BOUNDARIES.md)
6. [`../conflict_resolution/`](../conflict_resolution/) — when concurrency applies
7. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)

> **Explanations are complete only when required constitutional components are present.  
> Completeness of speech is not completeness of educational success.**

---

## 1. Purpose

Without a closed component set, authority narration drifts: warm student copy without owners, or audit fields without refusal reasons. This document names what must be reconstructible for every material authority decision explanation.

Components are **constitutional content obligations**, not database columns, API fields, or UI widgets. Persistence and rendering are out of scope for MS003.

---

## 2. Component Catalogue

| ID | Component | One-line definition |
|----|-----------|---------------------|
| **AEC-01** | Decision owner | Constitutional component accountable for the decision class |
| **AEC-02** | Decision class | Named class of educational decision at stake |
| **AEC-03** | Constitutional authority invoked | Published principles / domains / boundaries (and conflict rules if any) that authorised permission |
| **AEC-04** | Permission warrant | Why this owner (or AP-04 delegate) was permitted |
| **AEC-05** | Refused or non-primary alternatives | Why material alternative components were not permitted to decide |
| **AEC-06** | Consumed recommendations | Authorised peer outputs read as inputs without absorbing ownership |
| **AEC-07** | Conflicts identified | CT-xx and competing artefacts when concurrency arose; else explicit none |
| **AEC-08** | Constitutional rules applied | AP/AD/AB list and, when applicable, RP/RO (and higher EIP/Constitution obligations) |
| **AEC-09** | Delegation record | Owner → delegate → scope → restore_when when AP-04 applied; else none |
| **AEC-10** | Lawful outcome | Acted-upon / refused / dispositioned result with ownership and meaning preservation |

Additional components may be added only by amending this document.

---

## 3. Mandatory vs Conditional

| Component | Ordinary decision | Delegated exercise | Conflict disposition |
|-----------|-------------------|--------------------|----------------------|
| AEC-01 Decision owner | Mandatory | Mandatory (standing owner) | Mandatory (each peer’s owner unchanged) |
| AEC-02 Decision class | Mandatory | Mandatory | Mandatory (action class under coordination) |
| AEC-03 Authority invoked | Mandatory | Mandatory | Mandatory |
| AEC-04 Permission warrant | Mandatory | Mandatory (owner warrant + delegate scope) | Mandatory for acted-upon peer |
| AEC-05 Alternatives | Mandatory when material; recommended always for audits | Mandatory for out-of-scope claims | Mandatory for non-acted peers and unlawful exclusions |
| AEC-06 Consumed recommendations | Mandatory when any consumed; else explicit none | Same | Same (peers are not “consumed ownership”) |
| AEC-07 Conflicts identified | Explicit `none` | Explicit `none` unless concurrency also arose | Mandatory CT-xx + peers |
| AEC-08 Rules applied | Mandatory | Mandatory (+ AP-04 / AP-07) | Mandatory (+ RP/RO set) |
| AEC-09 Delegation record | Explicit `none` | Mandatory | Explicit `none` unless AP-04 also applied |
| AEC-10 Lawful outcome | Mandatory | Mandatory | Mandatory (RO set + preservation) |

**Material alternative rule (AEC-05):** An alternative is *material* when a student or auditor could reasonably wonder why that component did not decide (e.g. plan rewrite vs day priority; recovery vs ordinary study; revision meaning vs day ownership).

---

## 4. Component Definitions

### 4.1 AEC-01 — Decision Owner

| Audience | Representation |
|----------|----------------|
| Student | Plain educational voice (“day coach”, “recovery coaching”, “planning review”, …) |
| Developer | `owner=AD-0x` (or named supporting authority when not an AD coach domain) |

Must match [`../authority/AUTHORITY_DOMAINS.md`](../authority/AUTHORITY_DOMAINS.md) for the decision class. Fiction owners (“the algorithm”, “the app”, unnamed “system”) are unlawful (AEP-01 / AEP-08).

### 4.2 AEC-02 — Decision Class

| Audience | Representation |
|----------|----------------|
| Student | Plain statement of what is being decided (“what to do today”, “how to recover”, …) |
| Developer | Named class from domain owned-decisions tables |

Decision class anchors AP-01 single-owner checks. Vague “guidance” without a class is incomplete.

### 4.3 AEC-03 — Constitutional Authority Invoked

The published law that made permission lawful — not a product preference.

| Typical citations | When |
|-------------------|------|
| AP-01, AP-03, AD-0x | Ordinary ownership match |
| AP-04, AP-07 | Delegation / restoration |
| AP-05 | Consumption of peer artefacts |
| AP-08, AB-xx | Refusal / boundary |
| CT-xx, RP-xx, RO-xx | Conflict disposition |
| EIP / Constitution obligations | Higher constraints (e.g. continuity, evidence honesty) |

Student speech paraphrases; developer speech cites IDs.

### 4.4 AEC-04 — Permission Warrant

Answers AEQ1: why *this* component was permitted.

| Student pattern | Developer pattern |
|-----------------|-------------------|
| “We’re focusing on **[domain]** because **[primary question]**.” | `permission=domain_match; owner=AD-0x; primary_question_match=true` |
| “Within today’s goal, your session may adjust how you work.” | `permission=AP-04; owner=AD-02; delegate=session; scope=…` |

Permission warrant must not claim educational certainty beyond Programme VI / EIP limits.

### 4.5 AEC-05 — Refused or Non-Primary Alternatives

Answers AEQ2: why alternatives were not permitted.

| Reason family | Examples |
|---------------|----------|
| Prohibited for caller | Domain prohibited list |
| Not primary question | Sibling domain not answering *this* question now |
| Boundary | AB-01…AB-10 |
| Ownership dispute refusal | RP-08 — not resolved by conflict engine |
| Unlawful artefact | RO-05 |
| Non-owner for class | AP-01 / AP-02 |

Student speech names the educational limit. Developer speech records `refused_or_non_primary=[{component, reason}]`.

### 4.6 AEC-06 — Consumed Recommendations

Authorised outputs of other owners read as inputs (AP-05). Consumption is **not** co-ownership.

| Lawful narration | Unlawful narration |
|------------------|--------------------|
| “Given your Study Plan and recent study…” | “The plan and the day coach jointly own today’s tip” |
| `consumed_owners=[AD-01, …]` | Treating consumed peers as co-deciders |

If nothing was consumed, record explicit `none` for audits.

### 4.7 AEC-07 — Conflicts Identified

When MS002 concurrency applied: conflict kind(s) and competing artefacts. When not: explicit `conflicts=none`.

| Student cue | Developer cue |
|-------------|----------------|
| “You had more than one good kind of guidance at once…” | `conflict=CT-xx; peers=[…]` |
| Ordinary single-owner path | `conflicts=none; conflict_prevention=AP-01` |

Do not invent conflicts for rhetorical drama. Do not hide real concurrency.

### 4.8 AEC-08 — Constitutional Rules Applied

The ordered or listed set of published rules that justified the path (AEQ3).

| Path | Minimum rule set |
|------|------------------|
| Ordinary | AP-01 + AD owner match + material AB checks |
| Delegation | Above + AP-04 (+ AP-07 when restoring) |
| Conflict | Above + CT classification + RP application + RO outcomes |
| Refusal | AP-08 + prohibited/boundary citation |

Rules applied must be a subset of published law. Unpublished customs are forbidden (AEP-03).

### 4.9 AEC-09 — Delegation Record

When AP-04 applied:

```
delegation:
  owner: AD-0x
  delegate: <bounded actor>
  scope: <what may be exercised>
  restore_when: <constitutional return condition>
```

When not applied: `delegation=none`.

Student speech must not make the delegate sound like a new standing owner (AEP-05 / AEP-08).

### 4.10 AEC-10 — Lawful Outcome

Answers AEQ4: what resulted, with ownership and meaning intact.

| Outcome family | Student emphasis | Developer emphasis |
|----------------|------------------|--------------------|
| Ordinary acted decision | What guidance leads now | `outcome=acted; owner=…; preservation=pass` |
| Refusal | What will not be done; rightful path if known | `outcome=refused; rightful_owner=…` |
| Conflict dispositions | What leads; what waits / follows / was set aside | `outcomes={RO-06|RO-03, …}; ownership_preserved=true` |
| Delegation exercise | Bounded local adjustment under today’s goal | `outcome=delegated_exercise; owner_unchanged=true` |

Preservation of ownership and meaning is mandatory in every outcome family (AXI-03 / AXI-04).

---

## 5. Minimal Audit Record (Conceptual)

Documentation and future implementations should be able to reconstruct at least:

```
decision_class: …
owner: AD-0x                          # AEC-01 / AEC-02
authority_invoked: [AP-…, AD-…, AB-…] # AEC-03
permission_warrant: …                 # AEC-04
refused_or_non_primary: [… → reason]  # AEC-05
consumed_recommendations: […] | none  # AEC-06
conflicts: none | {CT-…, peers:[…]}   # AEC-07
rules_applied: […]                    # AEC-08
delegation: none | {owner, delegate, scope, restore_when}  # AEC-09
lawful_outcome:                       # AEC-10
  result: acted | refused | dispositioned
  dispositions: […]                   # RO-xx when conflict
  ownership_preserved: true
  meaning_preserved: true
programme_vi_explainability_ref: …
workflow_explainability_ref: null | …
authority_ms001_explainability_ref: …
resolution_ms002_explainability_ref: null | …
```

This is a **constitutional audit shape**, not a database schema. Persistence design is out of scope for MS003.

---

## 6. Relationship to Sibling Contracts

| Sibling | How components relate |
|---------|------------------------|
| MS001 `AUTHORITY_EXPLAINABILITY.md` minimal audit | Compatible; MS003 AEC set generalises permission/refusal/delegation/conflict fields |
| MS002 `RESOLUTION_EXPLAINABILITY.md` RQ1–RQ4 | When AEC-07 is non-none, RQ1–RQ4 must also be satisfiable; AEC-08/AEC-10 carry RP/RO |
| Programme VI explainability | Linked via `programme_vi_explainability_ref`; not replaced by AEC fields |
| WS1 workflow explainability | Optional participation reference; never substitutes for AEC-01 owner |

---

## 7. Completeness Checklist

Before shipping student- or developer-facing authority narration, confirm:

- [ ] AEQ1–AEQ4 answered for the audience
- [ ] AEC-01…AEC-10 present (or explicit `none` where allowed)
- [ ] Owner matches MS001 for the decision class
- [ ] Alternatives refused for published reasons only
- [ ] No ownership transfer or meaning rewrite in outcome speech
- [ ] Delegation (if any) has owner, scope, and restore condition
- [ ] Conflict (if any) cites CT/RP/RO only from MS002
- [ ] Programme VI explainability linked for educational warrant
- [ ] No scoring / optimiser / job-queue jargon presented as constitutional permission

---

## 8. Closing

Components make authority explanations auditable: **owner, warrant, alternatives, consumed peers, conflicts, rules, delegation, and lawful outcome — with ownership intact.**

> **If a component is missing, the explanation is not yet constitutional.**
