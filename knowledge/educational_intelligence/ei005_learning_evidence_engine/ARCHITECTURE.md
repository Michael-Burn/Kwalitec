# EI-005 — Learning Evidence Engine Architecture

**Programme:** EI-005 — Learning Evidence Engine  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/learning_evidence/` · `app/application/learning_evidence/` · `app/models/learning_evidence.py`  
**Depends on:** [EI-004 Student Curriculum Binding](../ei004_student_curriculum_binding/ARCHITECTURE.md) · [EI-001 Curriculum Knowledge Graph](../ei001_curriculum_knowledge_graph/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can observe and record how a student learns.

Given a Student Curriculum Instance, Kwalitec persists a complete, chronological, explainable history of educational evidence for every curriculum node. No mastery inference, confidence updates, recommendations, or study missions are introduced in EI-005.

---

## 2. Evidence philosophy

Every belief held by the future Student Digital Twin must originate from **recorded educational evidence**. No educational belief may change without supporting observations.

| Principle | Meaning |
|-----------|---------|
| 1. Evidence origin | Twin beliefs require recorded observations |
| 2. Immutability | Evidence rows are append-only; corrections are new events |
| 3. Observation only | This programme records; it does not infer |

Evidence is linked to:

| Field | Role |
|-------|------|
| `instance_id` | Active Student Curriculum Instance (EI-004) |
| `node_stable_id` | Published curriculum node (string reference) |
| `occurred_at` | When the educational activity happened |
| `source` | Observation channel (`student_runtime`, `session_runtime`, …) |
| `evidence_type` | Catalogue / extensible type token |
| `metadata_json` | Observational payload (no mastery scores invented) |

---

## 3. Append-oriented design

```
Educational activity occurs
        ↓
EvidenceRecordingService.record_evidence
        ↓
Integrity gates (active SCI, node in instance, timestamp, type, payload)
        ↓
INSERT lee_evidence_events  (immutable row)
        ↓
Optional: increment SciCurriculumNodeState.evidence_count
          + last_interaction_at  (bookkeeping only)
        ↓
EvidenceQueryService — chronological / by-node / by-student / by-type / summarise
```

There is **no update or delete API**. A correction is a new event with `corrects_evidence_id` pointing at the prior observation. The prior row remains unchanged for audit and explainability.

---

## 4. Event lifecycle

1. **Record** — validate integrity → append event → optional SCI counter bump.  
2. **Retrieve** — by node, student, chronological instance history, or type filter.  
3. **Summarise** — deterministic counts by type (no weighted scores).  
4. **Correct** — append a new event referencing the prior `evidence_id`.  

Events never modify CKG curriculum content.

---

## 5. Initial evidence types

Stored as strings (not DB enums) so the catalogue can grow without schema redesign:

| Type | Token |
|------|-------|
| Reading Completed | `reading_completed` |
| Worked Example Completed | `worked_example_completed` |
| Practice Attempt | `practice_attempt` |
| Assessment Result | `assessment_result` |
| Study Session | `study_session` |
| Revision Session | `revision_session` |
| Manual Founder Override | `manual_founder_override` |

Additional snake_case tokens are accepted for future expansion. Known types may enforce light payload schemas (e.g. founder override requires `reason`).

---

## 6. Extensibility strategy

| Concern | Strategy |
|---------|----------|
| New evidence types | Add `EvidenceType` member + optional payload keys; column remains `String(64)` |
| New sources | Add `EvidenceSource` member |
| New payload fields | JSON metadata object — no migration |
| Corrections | `corrects_evidence_id` self-FK |
| Twin / inference consumers | Read via `EvidenceQueryService`; never write beliefs here |

Distinct from `app/domain/evidence/` (Twin extract/validate/transform vocabulary without SCI persistence). EI-005 is the **SCI-bound persistent observation store**.

---

## 7. Integrity gates

| # | Rule | Enforcement |
|---|------|-------------|
| 1 | Evidence belongs to an **active** SCI | `ACTIVE_INSTANCE_REQUIRED` |
| 2 | Node must exist in the SCI node-state map (published edition) | `NODE_IN_INSTANCE` |
| 3 | Timestamp required; not absurdly future | `VALID_TIMESTAMP` |
| 4 | Type is snake_case; source is catalogue | `VALID_EVIDENCE_TYPE` / `VALID_SOURCE` |
| 5 | Payload satisfies type schema | `PAYLOAD_SCHEMA` |

Domain gates live in `app/domain/learning_evidence/invariants.py` and `payload_schema.py`.

---

## 8. Persistence (EI-005 additive)

Migration `202607280050`:

- `lee_evidence_events`

Does not alter CKG node content, V1/V2 curriculum engine, Twin tables, missions, or recommendation schema. SCI node-state rows may have `evidence_count` / `last_interaction_at` updated as observation bookkeeping only — mastery and confidence remain untouched.

---

## 9. Explicit non-goals

- Mastery calculation or confidence updates  
- Forgetting curves  
- Recommendations or study mission generation  
- Modifying published CKG content  
- Wiring evidence into student HTTP / Coach surfaces  

---

## 10. Relationship to Digital Twin inference

EI-005 establishes the **evidence foundation** of the Student Digital Twin: a durable, chronological, explainable observation log keyed to curriculum nodes within a trusted SCI.

Future Twin inference engines must:

1. Consume evidence via query services (or projections thereof).  
2. Never invent observations.  
3. Treat corrections as additional events, not silent rewrites.  
4. Keep inference (mastery, confidence, recommendations) in a separate programme.

```
Published CKG Edition (immutable)
        ↑
Student Curriculum Instance (EI-004)
        ↑ instance_id / node_stable_id
Learning Evidence Events (EI-005)  ← observations only
        ↓
(Future) Twin inference / Reasoning / Missions
```
