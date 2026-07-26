# Explanation Boundaries

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS003 — Educational State Explainability  
**Classification:** Hard limits on what educational state explanations may and must not do  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **constitutional boundaries** for educational state explanations.

Subordinate to:

1. [`EDUCATIONAL_STATE_EXPLAINABILITY.md`](EDUCATIONAL_STATE_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md)
4. [`../state/STATE_BOUNDARIES.md`](../state/STATE_BOUNDARIES.md)
5. [`../state_transitions/TRANSITION_BOUNDARIES.md`](../state_transitions/TRANSITION_BOUNDARIES.md)
6. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
7. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md)
8. [`../authority/AUTHORITY_BOUNDARIES.md`](../authority/AUTHORITY_BOUNDARIES.md)

> **Educational state explanations may describe contextual state and lawful succession.  
> They must never invent meaning, mastery, ownership, tips, or unpublished law.**

---

## 1. Purpose

Boundaries prevent explanation from becoming a back door: narration that quietly implies mastery, transfers ownership, rewrites evidence, executes workflows in speech, or exposes runtime guts as if they were educational law.

These boundaries bind every educational-state explanation path. Crossing them makes the narration **unlawful** even if motivationally effective.

---

## 2. Boundary Catalogue

| ID | Boundary | One-line rule |
|----|----------|---------------|
| **ESEB-01** | Contextual state description | Explanations may describe published constitutional educational context |
| **ESEB-02** | Lawful succession description | Explanations may describe published contextual succession |
| **ESEB-03** | Constitutional evidence reference | Explanations may reference published context warrants and supporting facts |
| **ESEB-04** | Workflow progression as supporting context | Explanations may reference WS1 progression as context — never as State Engine execution |
| **ESEB-05** | No educational meaning rewrite | Explanations must not redefine Programme VI educational meaning |
| **ESEB-06** | No mastery or success implication | Explanations must not imply learner mastery or educational success from context/succession |
| **ESEB-07** | No authority transfer | Explanations must not imply transferred, absorbed, or dual ownership |
| **ESEB-08** | No evidence reinterpretation | Explanations must not reinterpret Educational Evidence or Twin estimates |
| **ESEB-09** | No tip invention | Explanations must not create recommendations or cast EST/CST as tip authors |
| **ESEB-10** | No runtime implementation exposure as law | Explanations must not present implementation details as constitutional justification |

---

## 3. What Educational State Explanations May Do

### ESEB-01 — Describe Contextual State

**Permitted:** Narrate the live EST posture — what constitutional educational focus is current — in audience-appropriate language.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “Right now the focus is recovering your study rhythm after a disruption.” | “You’re behind and failing — recovery mode proves it.” |
| Developer cites `primary_est=EST-07` | Developer cites “`RecoveryService` is running” as the EST |

### ESEB-02 — Describe Lawful Contextual Succession

**Permitted:** Narrate why and how context moved under published CST types, conditions, and continuity — including refuse/remain.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “We’re shifting from today’s priority to recovery because there’s been a meaningful break.” | “We flipped modes because engagement dropped 12%.” |
| “We’re not changing focus yet — conditions aren’t met.” | Silent UI tab switch with no succession honesty |

### ESEB-03 — Reference Constitutional Evidence

**Permitted:** Cite plan class, Programme VI warrants, WS2 dispositions, and continuity holds as *context warrants* supporting the live posture or move.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “Your active Study Plan and today’s coaching warrant this focus.” | “Opening the mission proves you understand Topic X.” |
| Distinguish warrants from understanding Evidence | Treat time-on-task as mastery Evidence inside context speech |

### ESEB-04 — Reference Workflow Progression as Supporting Context

**Permitted:** Mention that coordination started, handed off, progressed, or concluded — as *orchestration context* that situates focus — without attributing educational content decisions or workflow execution to the Educational State Engine.

| Lawful | Unlawful lookalike |
|--------|-------------------|
| “Your study coordination is following this recovery focus.” | “The State Engine completed your workflow / chose Topic X.” |
| Developer: `flow_references=[WT-…]; executed_by_state_engine=false` | Developer: `owner=AD-07` for educational tip content via EST citation |

---

## 4. What Educational State Explanations Must Not Do

### ESEB-05 — Must Not Redefine Educational Meaning

**Forbidden:** Using explanation to reinterpret, rewrite, or silently edit Programme VI meanings or the substance of authorised recommendations.

| Forbidden narration | Why |
|---------------------|-----|
| Relabel Recovery as Revision in speech to simplify the story | SB-02 / ESEP-07 / meaning non-invention |
| Rewrite a deferred tip’s warrant so succession “explains away” concurrency | Disposition ≠ meaning invalidation |
| Collapse Article IV Study Progress into EST-03 speech | Article IV orthogonality |

**Lawful alternative:** Preserve meaning; explain context and succession only; link Programme VI explainability for educational warrant.

### ESEB-06 — Must Not Imply Mastery or Educational Success

**Forbidden:** Speech that makes EST posture or CST succession sound like pass certainty, Estimated Mastery, educational success, or “you are done.”

| Forbidden narration | Why |
|---------------------|-----|
| “You’re in revision — so you’ve mastered the chapter.” | SB-07 / EIP-006 / ESEP-06 |
| “Leaving recovery means you succeeded.” | STB-02 / CST non-evaluative law |
| “Session context ended — you’ve completed learning.” | Session close ≠ mastery; WS1 completion ≠ educational success |

**Lawful alternative:** Name focus change plainly; add “this is about where we are, not mastery or finished.”

### ESEB-07 — Must Not Transfer Authority

**Forbidden:** Speech that makes temporary focus, succession, conflict-await, or UI proximity sound like transferred or dual ownership.

| Forbidden narration | Why |
|---------------------|-----|
| “Recovery now owns your daily plan.” | SB-03 / STB-04 / ESEP-08 |
| “Conflict-await merged coaches into one owner.” | EST-10 is situation, not ownership rewrite |
| “The State Engine / workflow owns what you study.” | WS2 / WS1 boundaries |

**Lawful alternative:** Distinguish *live focus* from *standing owner*; link authority explainability when permission speech is material.

### ESEB-08 — Must Not Reinterpret Evidence

**Forbidden:** Treating explanation as a licence to reclassify Educational Evidence, invent observations, or mint Estimated Knowledge / Mastery from EST/CST labels or UI completion.

| Forbidden narration | Why |
|---------------------|-----|
| “Because you entered Session Context, we now know you understand…” | SB-02 / SB-09 / AB-03 adjacency |
| Context speech that rewrites Evidence Model classifications | Evidence Pipeline / EIP-002 owns meaning |
| Twin facet names in student copy as context proof | Wrong audience + wrong authority |

**Lawful alternative:** Consume Evidence / estimates as published inputs when they situate warrants; leave reclassification to rightful writers under EIP-001 / Evidence law.

### ESEB-09 — Must Not Invent Tips or Tip Authorship

**Forbidden:** Creating recommendations in speech, or casting EST/CST labels as authors of guidance.

| Forbidden narration | Why |
|---------------------|-----|
| “Because you’re in Day Priority Context, study Topic X.” (as tip creation) | SB-01 / STB-05 / WS3 ownership |
| “Succession assembled your tip set.” | Assembly owned by WS3 MS002 |
| Empty EST-01 / EST-11 narrated as inventing filler tips | Prefer no-recommendation honesty |

**Lawful alternative:** Reference existing WS3 artefacts that *cite* EST as context; defer tip substance to Programme VI / WS3 explainability.

### ESEB-10 — Must Not Expose Runtime Implementation as Law

**Forbidden:** Presenting queues, service names, feature flags, database rows, job IDs, stack traces, adapter paths, or Version 2 operational state-machine enums as the *constitutional reason* a context is live or succeeded.

| Forbidden as justification | Permitted as non-authoritative ops context (developer-only, clearly labelled) |
|----------------------------|-------------------------------------------------------------------------------|
| “Because `EducationalStateService` hashed first…” | Optional ops breadcrumbs *after* constitutional citations, never instead of them |
| “Flag `X` forced recovery mode” | Flag may gate delivery; it does not create EST-07 |
| “Row id 12345 is the current state” | Persistence identity ≠ context warrant |
| “V2 state machine `SESSION_ACTIVE` equals EST-04” | Version 2 operational machines do not replace EST catalogue |

**Architectural requirement:** Constitutional justification precedes any implementation breadcrumb. Implementation detail never substitutes for ESEC-04 / ESEC-05.

---

## 5. Boundary Interaction with MS001 / MS002

| MS001 / MS002 law | Explanation boundary effect |
|-------------------|----------------------------|
| EST catalogue closure | ESEB-01 forbids undocumented mode speech |
| SB-06…SB-08 non-claim | ESEB-06 binds evaluative speech |
| SB-01 / SB-03 tip & ownership | ESEB-07 / ESEB-09 bind consumer speech |
| CST catalogue / conditions | ESEB-02 forbids undocumented succession stories |
| STB-01…STB-06 representational only | ESEB-04 / ESEB-07 / ESEB-09 forbid execution, transfer, tip minting in speech |
| STB-08 / STB-09 Article IV / Evidence | ESEB-05 / ESEB-08 bind meaning and Evidence speech |
| EIP-005 continuity | ESEB-02 requires continuity-honest succession |

Explanation boundaries **do not amend** MS001/MS002. They constrain how those corpora are spoken.

---

## 6. Refusal Duty for Unlawful Narration

If a proposed explanation would require crossing ESEB-05…ESEB-10:

1. **Refuse** the narration path, or
2. **Amend** the owning constitutional corpus first (MS001 types, MS002 transitions, Programme VI meaning, EIP), then explain the amended law.

Silent “helpful” copy that crosses a boundary is an architectural defect, not a UX win.

---

## 7. Completeness vs Boundaries

Satisfying `EXPLANATION_COMPONENTS.md` does **not** authorise crossing these boundaries. A complete component set that implies mastery or invents tips remains unlawful.

Conversely, a boundary-respecting explanation that omits mandatory components remains incomplete (ESEP-02 / SEXI-11).

Both completeness and boundaries are required.

---

## 8. Closing

Educational state explanations are trustworthy only inside these limits:

> **May describe contextual state, lawful succession, constitutional warrants, and workflow progression as supporting context.  
> Must never redefine meaning, imply mastery or success, transfer authority, reinterpret evidence, invent tips, or treat runtime guts as educational law.**
