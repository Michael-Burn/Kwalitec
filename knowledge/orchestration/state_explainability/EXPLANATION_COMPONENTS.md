# Explanation Components

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS003 — Educational State Explainability  
**Classification:** Mandatory information set for educational state explanations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document catalogues the **information every material educational state explanation should contain**.

Subordinate to:

1. [`EDUCATIONAL_STATE_EXPLAINABILITY.md`](EDUCATIONAL_STATE_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`../state/STATE_TYPES.md`](../state/STATE_TYPES.md)
4. [`../state/STATE_BOUNDARIES.md`](../state/STATE_BOUNDARIES.md)
5. [`../state_transitions/TRANSITION_TYPES.md`](../state_transitions/TRANSITION_TYPES.md)
6. [`../state_transitions/TRANSITION_CONDITIONS.md`](../state_transitions/TRANSITION_CONDITIONS.md)
7. [`../state_transitions/TRANSITION_BOUNDARIES.md`](../state_transitions/TRANSITION_BOUNDARIES.md)
8. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
9. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

> **Explanations are complete only when required constitutional components are present.  
> Completeness of speech is not completeness of educational success.**

---

## 1. Purpose

Without a closed component set, context narration drifts: warm student copy without EST identity, or audit fields without succession continuity. This document names what must be reconstructible for every material educational-state explanation.

Components are **constitutional content obligations**, not database columns, API fields, or UI widgets. Persistence and rendering are out of scope for MS003.

---

## 2. Component Catalogue

| ID | Component | One-line definition |
|----|-----------|---------------------|
| **ESEC-01** | Current EST state | Live primary constitutional educational context (and parallel-read siblings if any) |
| **ESEC-02** | Preceding contextual states | Prior EST postures in the material succession window; else `initial` / `none` |
| **ESEC-03** | CST references | Named transition types for each material succession step; else `none` / `initial` |
| **ESEC-04** | Supporting contextual evidence | Context warrants (plan class, Programme VI, WS1 facts, WS2 dispositions, continuity) — not understanding Evidence |
| **ESEC-05** | Published rules applied | MS001 entry/exit, CST catalogue, condition families, SB/STB checks cited |
| **ESEC-06** | Continuity record | Explicit preservation that prior context history was not erased |
| **ESEC-07** | Workflow references | WS1 instances / stages / progression facts that observe or situate this context; else explicit none |
| **ESEC-08** | Authority references | WS2 permission / disposition narrations that consumed this context when material; else explicit none |
| **ESEC-09** | Recommendation references | WS3 tips / sets that cite this EST as context; else explicit none |
| **ESEC-10** | Non-claim honesty | Explicit pass of prohibited-interpretation checks (no mastery / success / completion / tip authorship / ownership transfer) |

Additional components may be added only by amending this document.

---

## 3. Mandatory vs Conditional

| Component | Initial posture | Single transition | Multi-step progression | Workflow-referenced |
|-----------|-----------------|-------------------|------------------------|---------------------|
| ESEC-01 Current EST | Mandatory | Mandatory | Mandatory | Mandatory |
| ESEC-02 Preceding states | Explicit `initial` | Mandatory (origin) | Mandatory (ordered chain) | Mandatory when succession; else as applicable |
| ESEC-03 CST references | Explicit `none` / `initial` | Mandatory | Mandatory (ordered) | Mandatory when succession used C-FLOW conditions |
| ESEC-04 Contextual evidence | Mandatory | Mandatory | Mandatory | Mandatory (+ C-FLOW facts as references) |
| ESEC-05 Rules applied | Mandatory | Mandatory | Mandatory | Mandatory |
| ESEC-06 Continuity | Explicit N/A or baseline | Mandatory | Mandatory | Mandatory |
| ESEC-07 Workflow refs | Explicit `none` or list | Same | Same | Mandatory when C-FLOW material |
| ESEC-08 Authority refs | Explicit `none` or list | Same | Same | Same |
| ESEC-09 Recommendation refs | Explicit `none` or list | Same | Same | Same |
| ESEC-10 Non-claim honesty | Mandatory | Mandatory | Mandatory | Mandatory |

**Material succession rule (ESEC-02 / ESEC-03):** A prior EST or CST step is *material* when a student or auditor could reasonably wonder how the live focus arrived, or whether an intermediate posture was erased.

---

## 4. Component Definitions

### 4.1 ESEC-01 — Current EST State

| Audience | Representation |
|----------|----------------|
| Student | Plain educational focus (“today’s priorities”, “recovery”, “waiting while options settle”, …) |
| Developer | `primary_est=EST-xx` (+ `parallel_read=[…]` if any) |

Must match [`../state/STATE_TYPES.md`](../state/STATE_TYPES.md). Fiction modes (“the algorithm mode”, unnamed “system”) are unlawful (ESEP-01 / SEXI-01). Article IV meaning-bearing states must not be aliased as EST-xx.

### 4.2 ESEC-02 — Preceding Contextual States

| Audience | Representation |
|----------|----------------|
| Student | “We were focusing on …; now …” / “This is where we start …” |
| Developer | `preceding_est=[EST-…, …] \| initial` |

For multi-step progression, preserve order. Do not collapse material intermediates.

### 4.3 ESEC-03 — CST References

| Audience | Representation |
|----------|----------------|
| Student | Plain succession story (“we shifted because…”, “we’re holding because…”) |
| Developer | `cst_path=[CST-xx, …] \| none \| initial` |

Must match [`../state_transitions/TRANSITION_TYPES.md`](../state_transitions/TRANSITION_TYPES.md). CST-13 refuse/remain is a first-class reference when no move occurred despite a proposed change.

### 4.4 ESEC-04 — Supporting Contextual Evidence

Context warrants — not EIP-002 Educational Evidence of understanding.

| Typical warrant families | When |
|--------------------------|------|
| Plan class / Active Canonical Study Plan | Presence, absence, or structural plan focus |
| Programme VI warrant | Coach / planner question that situates the EST type |
| WS1 progression / completion fact | Referenced as C-FLOW *fact*, never as State Engine execution |
| WS2 disposition | Conflict / escalation situation (EST-10 / EST-11) |
| Continuity hold | EST-12 / CST-12 / CST-13 remain |

Student speech paraphrases warrants honestly. Developer speech records warrant IDs / classes. Time-on-task, confidence alone, or UI mode must not be treated as understanding Evidence.

### 4.5 ESEC-05 — Published Rules Applied

The listed set of published rules that justified the live posture and any succession (ESEQ-04).

| Path | Minimum rule set |
|------|------------------|
| Initial posture | EST entry conditions + material SB checks |
| Single / multi transition | Origin exit + destination entry + CST type + condition families + STB checks |
| Refuse / remain | CST-13 + failed/ unmet condition citation |
| Workflow-referenced | Above + cited WT/completion rule IDs as *references* only |

Rules applied must be a subset of published law. Unpublished customs are forbidden (ESEP-05).

### 4.6 ESEC-06 — Continuity Record

| Student emphasis | Developer emphasis |
|------------------|--------------------|
| “We’re not forgetting where you were.” | `prior_est_recorded`, `eip005_pass`, `article_iv_mutated=false` |
| Holding / return speech that names prior focus when material | No history erasure; parallel-read siblings noted if observational |

For true initial posture with no prior EST in window: `continuity=baseline_initial`.

### 4.7 ESEC-07 — Workflow References

Where applicable: WS1 workflow instances, stages, or published progression/completion records that *observe* or *situate* this context.

| Lawful narration | Unlawful narration |
|------------------|--------------------|
| “Your study coordination is following this focus.” | “The workflow decided Topic X / ran because EST said so.” |
| `workflows_referencing=[…]` | `owner=workflow` for educational content |

If none: explicit `workflows_referencing=none`.

### 4.8 ESEC-08 — Authority References

Where applicable: WS2 permission / conflict narrations that consumed EST context as situation.

| Lawful narration | Unlawful narration |
|------------------|--------------------|
| Link authority explainability when ownership speech is material | “EST-07 transferred day ownership to Recovery.” |
| `authority_refs=[…] \| none` | Dual-owner fiction from context labels |

### 4.9 ESEC-09 — Recommendation References

Where applicable: WS3 recommendations / sets that cite EST-xx as *context reference*.

| Lawful narration | Unlawful narration |
|------------------|--------------------|
| “The guidance you’re seeing fits this recovery focus.” | “Recovery context created this tip.” |
| `recommendations_referencing=[…] \| none` | EST as tip author (SB-01 / STB-05) |

### 4.10 ESEC-10 — Non-Claim Honesty

Mandatory explicit (developer) or implicit-but-enforced (student) refusal of prohibited interpretations:

| Must not claim | Governing |
|----------------|-----------|
| Educational success | SB-06 / STB-02 / SEXI-04 |
| Learner mastery / Estimated Mastery | SB-07 / EIP-006 / STB-03 |
| Workflow completion from context/succession alone | SB-08 / STB-07 |
| Tip authorship by State Engine | SB-01 / STB-05 |
| Ownership transfer | SB-03 / STB-04 / ESEP-08 |
| Evidence / Article IV mutation by EST/CST | SB-02 / SB-09 / STB-08 / STB-09 |

Developer: `prohibited_interpretation_pass=true` with SB/STB checklist. Student: plain “focus, not mastery / finished” language when evaluative confusion is plausible.

---

## 5. Minimal Audit Record (Conceptual)

Documentation and future implementations should be able to reconstruct at least:

```
primary_est: EST-xx                         # ESEC-01
parallel_read: […] | none
preceding_est: [EST-…] | initial            # ESEC-02
cst_path: [CST-…] | none | initial          # ESEC-03
context_evidence:                           # ESEC-04
  warrants: [plan | programme_vi | ws1_fact | ws2_disposition | continuity]
  understanding_evidence_alias: false
rules_applied: […]                         # ESEC-05
continuity:                                 # ESEC-06
  prior_est_recorded: true | baseline_initial
  eip005_pass: true
  article_iv_mutated: false
workflows_referencing: […] | none           # ESEC-07
authority_refs: […] | none                  # ESEC-08
recommendations_referencing: […] | none     # ESEC-09
non_claim:                                  # ESEC-10
  boundary_pass: [SB-… / STB-…]
  prohibited_interpretation_pass: true
ms001_state_explainability_ref: …
ms002_transition_explainability_ref: null | …
programme_vi_explainability_ref: null | …
workflow_explainability_ref: null | …
authority_explainability_ref: null | …
recommendation_explainability_ref: null | …
```

This is a **constitutional audit shape**, not a database schema. Persistence design is out of scope for MS003.

---

## 6. Relationship to Sibling Contracts

| Sibling | How components relate |
|---------|------------------------|
| MS001 `STATE_EXPLAINABILITY.md` ESQ-01…ESQ-04 | Compatible; ESEC-01/04/07–09 generalise static-context fields; ESEC-02/03/06 add progression |
| MS002 `TRANSITION_EXPLAINABILITY.md` STQ-01…STQ-04 | When ESEC-03 is non-none, STQ-01…STQ-04 must also be satisfiable; ESEC-05/06 carry rules and continuity |
| Programme VI explainability | Linked via `programme_vi_explainability_ref`; not replaced by ESEC fields |
| WS1 workflow explainability | Optional ESEC-07 participation / C-FLOW reference; never substitutes for ESEC-01 |
| WS2 authority explainability | Optional ESEC-08; never transfers ownership via EST speech |
| WS3 set / tip explainability | Optional ESEC-09 context reference; never tip authorship |

---

## 7. Completeness Checklist

Before shipping student- or developer-facing educational-state narration, confirm:

- [ ] ESEQ-01…ESEQ-05 answered for the audience
- [ ] ESEC-01…ESEC-10 present (or explicit `none` / `initial` where allowed)
- [ ] Current EST matches MS001 catalogue
- [ ] CST path (if any) matches MS002 catalogue and conditions
- [ ] Continuity recorded when succession occurred
- [ ] No mastery / success / completion / ownership / tip-authorship overclaim
- [ ] Context warrants distinguished from understanding Evidence
- [ ] Workflow refs (if any) are references, not State Engine execution claims
- [ ] Programme VI / WS1 / WS2 / WS3 explainability linked when those layers applied
- [ ] No scoring / optimiser / job-queue jargon presented as constitutional context proof

---

## 8. Closing

Components make educational-state explanations auditable: **current EST, preceding states, CST path, warrants, rules, continuity, consumers, and non-claim honesty — with meaning and ownership intact.**

> **If a component is missing, the explanation is not yet constitutional.**
