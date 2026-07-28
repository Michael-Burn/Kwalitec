# EI-004 — Student Curriculum Binding Architecture

**Programme:** EI-004 — Student Curriculum Binding  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/student_curriculum_binding/` · `app/application/student_curriculum_binding/` · `app/models/student_curriculum_binding.py`  
**Depends on:** [EI-001 Curriculum Knowledge Graph](../ei001_curriculum_knowledge_graph/ARCHITECTURE.md) · [EI-003 Founder Curriculum Publishing](../ei003_curriculum_publishing/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can represent a student's position within a trusted curriculum.

Given a Published Curriculum Edition and a student, Kwalitec creates and persists a Student Curriculum Instance containing educational state for every curriculum node. No recommendations, missions, mastery engines, or CKG mutations are introduced in EI-004.

---

## 2. Philosophy — Student Curriculum Instance

A **Student Curriculum Instance (SCI)** is the durable enrolment of one student into one Published Curriculum Edition for one subject.

| Field | Role |
|-------|------|
| `student_id` | Application user (learner) |
| `subject_code` | Subject scope (exactly one active SCI per student+subject) |
| `edition_id` | Published CKG edition (never Draft) |
| `enrolled_at` | Enrolment timestamp |
| `is_active` | Active binding flag |
| `is_completed` | Instance-level completion flag |

The SCI is the **only source of truth** for that student’s educational state relative to the trusted curriculum. Future Digital Twin, Reasoning, and Mission engines must consume this layer rather than studying against live CKG drafts or mutating curriculum structure.

---

## 3. Immutable curriculum vs mutable learner state

| Concern | Owner | Mutability |
|---------|-------|------------|
| Curriculum structure, LOs, objects, edges | CKG (`ckg_*`) | Immutable after Founder publish (EI-003) |
| Learner binding to an edition | `sci_student_curriculum_instances` | Mutable lifecycle (active/completed) |
| Per-node educational slots | `sci_curriculum_node_states` | Mutable learner state |

Node state **references** curriculum by `node_stable_id` and never updates CKG rows. Mastery/confidence/revision fields are **storage slots** initialised to defaults; EI-004 does not calculate mastery, run forgetting curves, or generate recommendations.

```
Published Curriculum Edition (immutable knowledge)
        ↑ reference only (edition_id, node_stable_id)
Student Curriculum Instance (mutable binding)
        ↓ owns
Curriculum Node State rows (mutable educational state)
```

---

## 4. Binding invariants

| # | Principle | Enforcement |
|---|-----------|-------------|
| 1 | Bind only to **Published** editions | `assert_published_edition` / `assert_can_bind` |
| 2 | Exactly one **active** binding per student+subject | Reject conflicting edition; idempotent same-edition rebind |
| 3 | Subject must match edition subject | `SUBJECT_MATCHES_EDITION` |
| 4 | Curriculum knowledge remains immutable | Binding services never write CKG tables |

Domain invariants live in `app/domain/student_curriculum_binding/invariants.py`.

---

## 5. Curriculum Node State

Every curriculum node in the published edition receives a state row at binding time:

| Slot | Default | Notes |
|------|---------|-------|
| mastery | `0.0` | Slot only — no mastery engine |
| confidence | `0.0` | Slot only |
| revision_status | `not_due` | `not_due` / `due` / `overdue` |
| attempts | `0` | Counter |
| total_study_time_minutes | `0` | Accumulator |
| last_interaction_at | `null` | Optional timestamp |
| completion_status | `not_started` | `not_started` / `in_progress` / `completed` |
| evidence_count | `0` | Counter |

Initialisation is idempotent: existing `(instance_id, node_stable_id)` pairs are skipped.

---

## 6. Aggregation model

Progress aggregation is a **deterministic read-side** derivation over node states.

### Levels

- subsection  
- section  
- topic  
- subject  

### Rules

1. Contributors are node states whose `node_stable_id` is the root or a descendant (`prefix.` rule via stable ids).  
2. Contributors are sorted by `node_stable_id` before aggregation (reproducible).  
3. Means (mastery, confidence) use arithmetic average rounded to **6 decimal places**.  
4. Attempts, study time, and evidence counts **sum**.  
5. Completion status is derived from completed / in-progress counts.  
6. Revision status takes the **worst** child status (`overdue` > `due` > `not_due`).  

Same inputs always yield the same `ProgressAggregate`. Aggregation does not write curriculum and does not invent mastery.

---

## 7. Educational state lifecycle

```
Published Edition (EI-003)
        ↓
StudentCurriculumBindingService.create_instance
        ↓
SCI row (active, not completed)
        ↓
initialise_node_states (one row per curriculum node)
        ↓
EducationalStateQueryService  — read current state
ProgressAggregationService    — roll-up subsection→subject
query_incomplete / query_completed
        ↓
(Future) Twin / Reasoning / Mission consumers
```

| Service | Responsibility |
|---------|----------------|
| `StudentCurriculumBindingService` | Create SCI; initialise node states |
| `EducationalStateQueryService` | Retrieve state; incomplete/completed filters |
| `ProgressAggregationService` | Deterministic upward aggregation |

---

## 8. Persistence (EI-004 additive)

Migration `202607280040`:

- `sci_student_curriculum_instances`  
- `sci_curriculum_node_states`  

Does not alter CKG node content, V1/V2 curriculum engine, Twin tables, missions, or recommendation schema.

---

## 9. Explicit non-goals

- Recommendations or study mission generation  
- Forgetting curves / mastery calculation engines  
- AI reasoning  
- Modifying published CKG content  
- Wiring SCI into student HTTP / CurriculumService runtime cutover  

---

## 10. Relationship to Student Digital Twin

EI-004 establishes the **curriculum-position substrate** for the Student Digital Twin: which trusted edition the student studies against, and a complete mutable state map keyed by curriculum node. Twin observation/inference pipelines remain out of scope; they must later consume SCI rather than invent a parallel educational SoT.
