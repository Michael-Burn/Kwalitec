# Educational Continuity Standard

**Capability ID:** EIP-005  
**Programme:** Educational Integrity Programme  
**Classification:** Educational Persistence & Lifecycle Standard — subordinate specialised architecture  
**Status:** APPROVED — governing for Study Plan lifecycle implementation  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This Standard defines how educational history survives Study Plan lifecycle change.

It is subordinate to:

1. **KWALITEC_EDUCATIONAL_CONSTITUTION.md** (EGI-001) — especially Articles II §1.8, IV, VIII.15, IX §4  
2. **EDUCATIONAL_LOGIC_REGISTRY.md** (EGI-002) — especially EL-001, EL-011  
3. **EDUCATIONAL_STATE_AUTHORITY_MATRIX.md** (EIP-001) — ownership and lawful writers  
4. **EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md** (EIP-005-DESIGN) — lifetime, deletion, continuity  
5. **EDUCATIONAL_EVIDENCE_AUTHORITY.md** / **EDUCATIONAL_EVIDENCE_MODEL.md** (EIP-002) — evidence meaning  

Authority order for persistence:

> Constitution defines *that* the learning journey is continuous.  
> The Lifecycle Architecture defines *when* states may begin, end, or be disposed.  
> **This Standard defines the operational continuity contract for Study Plan change.**

This document:

- defines educational ownership and continuity / deletion / migration rules;
- does **not** redesign Digital Twin, Educational Intelligence, Learning Mode, Recommendation algorithms, Educational Evidence Authority, or Knowledge/Mastery semantics;
- does **not** introduce new educational scoring algorithms.

**Educational Continuity preserves rightful history. It never invents equivalence.**

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Educational Ownership](#2-educational-ownership)
3. [Continuity Rules](#3-continuity-rules)
4. [Deletion Rules](#4-deletion-rules)
5. [Migration Rules](#5-migration-rules)
6. [Examples](#6-examples)
7. [Future Version 2 Considerations](#7-future-version-2-considerations)
8. [Cross References](#8-cross-references)

---

## 1. Purpose

A Study Plan is a disposable planning container and Learning Mode context.

Educational history — Study Progress, Study Attempts, Educational Evidence posture, Estimated Knowledge, Estimated Mastery, and Mission/Attempt ancestry — belongs to the **learner**.

Without Educational Continuity:

- deleting a plan silently erases “what I have completed studying”;
- recreating a plan forces false cold-start theatre;
- curriculum version change invents discontinuity or false equivalence.

With Educational Continuity:

- planning objects remain disposable;
- learner educational history remains persistent;
- Current Learning, Missions, and Recommendations regenerate from preserved inputs.

---

## 2. Educational Ownership

| Asset | Belongs to | Role of Study Plan |
|-------|------------|--------------------|
| **Study Progress** | Learner (User) + syllabus unit identity | Context for declaring / scoping coverage; never ontological delete-owner |
| **Study Attempts** | Learner | May have been produced under a plan-bound Mission; survive plan removal |
| **Educational Evidence posture** | Learner (via authorised evidence pathways) | Plan does not own evidence |
| **Estimated Knowledge / Mastery** | Twin / authorised estimator posture held for the learner | Plan deletion must not invent zeros by wiping history |
| **Mission history** | Learner | Plan pointer may clear; mission rows remain |
| **Decision Journal preference history** | Learner | Advisory preference; not deleted with plan |
| **Week plans / scheduling / active pointers** | Study Plan | Disposable planning metadata |
| **Temporary recommendation artefacts** | Application / advisory layer | May expire or regenerate freely |
| **Current Learning pointer** | Active Study Plan context | May clear or resynchronise; must not erase Study Progress |

Constitutional owner of *meaning* for Study Progress remains coverage truth under EL-001. Persistence owner for continuity is the **learner**, not the Study Plan row.

---

## 3. Continuity Rules

1. **Educational history belongs to the User, not the Study Plan.**
2. **Changing study context must not invent discontinuity** (Constitution II §1.8).
3. **Study Plan recreation continues existing history** for the same syllabus units.
4. **Current Learning is recalculated** from preserved Study Progress + syllabus order after a new active plan exists.
5. **Missions and Recommendations regenerate** from preserved inputs; they do not require the deleted plan row to reconstruct educational truth.
6. **Correct uncertainty beats false continuity** when syllabus unit identity cannot be mapped objectively.
7. **Future Revision Mode** (when constitutionally activated) must not erase first-pass Learning Mode history.

---

## 4. Deletion Rules

### 4.1 May be removed when a Study Plan is deleted

- Planning metadata (exam schedule settings on the plan row)
- Week schedules / temporary sequencing artefacts
- Active mission **pointers** (`Mission.study_plan_id`)
- Temporary advisory artefacts bound only to that plan context

### 4.2 Must not be silently removed

- Study Progress (`TopicProgress` coverage and stage history)
- Study Attempts
- Educational Evidence posture (authorised accuracy / evidence-bearing fields)
- Estimated Knowledge posture
- Estimated Mastery posture
- Mission rows that produced educational history
- Decision Journal preference history

### 4.3 Informed confirmation

Student-facing deletion confirms removal of **schedule and planning settings**, and states that **learning progress and study history are preserved**.

If a future path cannot preserve educational continuity, the application must **block deletion** or require **explicit informed authorisation** for an educational reset — never silent loss.

### 4.4 Account / privacy deletion

Legal privacy or full account deletion may remove educational history. That regime is outside ordinary Study Plan management and must not pretend empty estimates are mastered.

---

## 5. Migration Rules

Where curriculum identity changes (exam family same, syllabus version or structural identity differs):

1. **Attempt educational remapping** by objective official topic-code identity.
2. **If remapping cannot be determined objectively**, retain historical records on their original syllabus units without inventing equivalence.
3. **Never overwrite richer existing target progress** solely to force a remap.
4. **Estimate posture may fill gaps** on a mapped target unit when the target lacks evidence/estimate history and the source lawfully holds it — without rewriting Study Progress coverage the learner already holds.
5. **V1 and V2 curricula** both remain loadable; remapping must not break either traversal path.

---

## 6. Examples

### Good — plan delete preserves coverage

Student completes topics 1.1–1.3, deletes the Study Plan, creates a new plan for the same exam/version. Coverage on 1.1–1.3 remains; Current Learning advances past completed units; Mission regenerates for the next incomplete syllabus unit.

### Good — curriculum remap with objective codes

Syllabus 2024 topic code `A.1` maps to syllabus 2025 topic code `A.1`. Study Progress and estimate posture continue onto the new unit. Unmapped legacy code `LEGACY.9` remains historical without false relabelling.

### Bad — silent TopicProgress wipe on plan delete

Deleting a Study Plan hard-deletes curriculum-linked TopicProgress. This is educationally unlawful under Lifecycle Architecture §5 and this Standard.

### Bad — inventing equivalence

Copying progress from an unrelated topic title because codes are missing. Prefer retaining unmapped history as unknown continuity.

---

## 7. Future Version 2 Considerations

| Extension | Intent |
|-----------|--------|
| Explicit student-authorised educational reset | Clear consequence language if coverage must be wiped |
| Richer multi-plan continuity UI | Show preserved history across archived plans without dual mission authority |
| Dedicated Evidence store remapping | Attach observations to new unit ids without rewriting outcomes |
| Separated Knowledge / Mastery stores | Continuity rules apply to both sibling estimate postures |
| Revision Mode continuity productisation | Disclosed mode switch; retain first-pass history |
| Formal curriculum edition remap tables | Admin-governed maps when codes alone are insufficient |

Version 2 extensions amend specialised architecture; they must not contradict the Constitution without Article X amendment.

---

## 8. Cross References

| Document | Role |
|----------|------|
| `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Continuity belief; educational state meanings |
| `EDUCATIONAL_LOGIC_REGISTRY.md` | EL-001 Study Progress; EL-011 Study Plan |
| `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Mutation rights; learner persistence ownership clarification |
| `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md` | Lifetime / deletion / continuity architecture |
| `EDUCATIONAL_EVIDENCE_AUTHORITY.md` | What may authorise estimate writes |
| `EDUCATIONAL_CONTINUITY_STANDARD.md` | Operational continuity / deletion / migration contract (EIP-005) |
| Implementation | `app/services/educational_continuity_service.py`; `StudyPlanService.delete_study_plan` |

---

## Closing

If implementation would erase rightful learner educational history because a Study Plan container disappeared, the implementation is educationally unlawful — even if the database cascade is convenient.
