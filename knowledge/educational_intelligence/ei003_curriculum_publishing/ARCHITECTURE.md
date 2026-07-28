# EI-003 — Founder Curriculum Publishing Architecture

**Programme:** EI-003 — Founder Curriculum Publishing Workflow  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/curriculum_publishing/` · `app/application/curriculum_publishing/`  
**Depends on:** [EI-001 Curriculum Knowledge Graph](../ei001_curriculum_knowledge_graph/ARCHITECTURE.md) · [EI-002 Curriculum Extraction Pipeline](../ei002_curriculum_extraction_pipeline/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can publish trusted educational knowledge.

Given a validated Draft Curriculum Knowledge Graph, the Founder publishing workflow supports inspection, editorial correction, explicit approval, and publication into a Founder-approved Published Curriculum Edition with complete auditability and edition history. Drafts are never student-visible. Student runtime is not integrated in EI-003.

---

## 2. Curriculum governance

Educational governance for CKG editions follows three principles:

| # | Principle | Enforcement |
|---|-----------|-------------|
| 1 | Only **Published** editions may be consumed by student-facing systems | `publication_state`; no student runtime wiring in EI-003 |
| 2 | Publishing is an **explicit Founder action** | `PublicationEngine.publish` requires review approval + publisher + rationale; validation alone never publishes |
| 3 | Every publication decision is **explainable and auditable** | Append-only `ckg_publication_records` + `ckg_editorial_audit_events` |

Domain invariants live in `app/domain/curriculum_publishing/invariants.py`.

---

## 3. Publication lifecycle

```
Draft Edition (EI-002)
    ↓ Inspection          FounderReviewService
    ↓ Validation Review   validation reports + confidence + provenance
    ↓ Educational Review  node approve / reject
    ↓ Corrections         edit metadata, resolve issues, revalidate
    ↓ Approval            approve_edition (review_status=approved)
    ↓ Publication         PublicationEngine.publish
    ↓ Edition History     snapshots + archived prior editions
```

| State | Meaning |
|-------|---------|
| `draft` | Extracted / under Founder review; never student-visible |
| `published` | Founder-approved authoritative edition for the subject |
| `archived` | Superseded published edition; history retained via snapshots + audit |

**Invariant:** at most one `published` edition per `subject_code`.

---

## 4. Edition management

### Live graph constraint

CKG node `stable_id` values are edition-stable and globally unique in live tables. Therefore **at most one live node graph may exist per subject** at a time.

### Successor editions

To extract a new draft while a published edition exists:

1. `PublicationEngine.prepare_successor_draft(subject_code, …)`  
   — snapshots the published edition, archives it, clears live nodes  
2. EI-002 extraction writes the new draft  
3. Founder review → approve → publish (links `previous_edition_id` to the archived predecessor)

### Snapshots

`ckg_edition_snapshots` stores immutable structural JSON (nodes + edges) for:

- publication capture  
- archive / successor prepare  
- edition comparison when live nodes are gone  

---

## 5. Founder review workflow (application services)

| Service | Responsibility |
|---------|----------------|
| `FounderReviewService` | List drafts, inspect hierarchy, validation reports, provenance, confidence, search, navigate |
| `EditorialOperationsService` | Approve/reject node, edit metadata, resolve validation issues, revalidate, approve/reject edition |
| `PublicationEngine` | Publish gates, archive previous, write publication record |
| `EditionComparisonService` | Structured diffs (hierarchy, LOs, prerequisites, objects, metadata) |
| `EditionSnapshotService` | Capture / load structural snapshots |
| `AuditTrailService` | Append-only editorial + publication audit |

No Founder HTTP UI is required in EI-003 — services are the deliverable for future Studio surfaces.

---

## 6. Audit strategy

| Artefact | Table | Retention |
|----------|-------|-----------|
| Editorial operations | `ckg_editorial_audit_events` | Append-only; never delete |
| Publication decisions | `ckg_publication_records` | Append-only; never delete |
| Structural history | `ckg_edition_snapshots` | Append-only captures |
| Node review dispositions | `ckg_node_review_states` | Mutable current state; changes audited |

Publication records always store:

- publication timestamp  
- publisher  
- previous edition id  
- publication rationale  
- validation status  
- review completion  

---

## 7. Publication invariants

1. **Draft-only editorial** — mutations refuse non-draft editions  
2. **Validation required** — approve/publish require `validation_status=passed`  
3. **Review approval required** — publish requires `review_status=approved`  
4. **No rejected nodes** — rejected nodes block edition approval and publish  
5. **Explicit publish** — only `PublicationEngine.publish` transitions to published  
6. **Single published per subject** — prior published archived before/at publish  
7. **Rationale + publisher required** — no anonymous or unexplained publications  

---

## 8. Persistence (EI-003 additive)

Migration `202607280030`:

- Review/publication columns on `ckg_graph_editions`  
- `ckg_node_review_states`  
- `ckg_editorial_audit_events`  
- `ckg_publication_records`  
- `ckg_edition_snapshots`  

Does not alter V1/V2 curriculum engine, CIP, Twin, or student runtime tables.

---

## 9. Explicit non-goals

- Student Digital Twin / missions / recommendations  
- Exposing drafts to students  
- Integrating published CKG into `CurriculumService` / student runtime  
- Founder HTTP UI redesign  
- CIP stage contract changes  
