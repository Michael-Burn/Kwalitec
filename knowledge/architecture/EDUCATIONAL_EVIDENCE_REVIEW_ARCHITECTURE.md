# Programme IV — Educational Evidence Review Workspace

**Milestone:** P4-MS003 — Educational Evidence Review Workspace  
**Directive:** Engineering Directive 001 (Educational Evidence Review Workspace)  
**Status:** Implemented (read-only review layer)  
**Package:** `app/infrastructure/adapters/evidence_review/`  
**Service:** `EvidenceQueryService`  
**Feature flag:** `KWALITEC_EVIDENCE_REVIEW` → `ENABLE_EVIDENCE_REVIEW` (**default OFF**)  
**Schema version:** `p4.ms003.1` (`EVIDENCE_REVIEW_SCHEMA_VERSION`)  
**Companions:** `LONGITUDINAL_EVIDENCE_ARCHITECTURE.md`, `EDUCATIONAL_TRIAL_ARCHITECTURE.md`, `ADVISORY_OUTCOME_MEASUREMENT.md`

---

## 0. Purpose

Build an **operational review layer** over the Longitudinal Learning Evidence Repository so humans can inspect accumulated educational evidence **before** algorithms act on it.

> Evidence should become understandable to people before it becomes actionable for algorithms.

This milestone is **read-only**. It must **not** influence Runtime A, Adaptive Engine, Recovery, recommendations, or educational policy.

| In scope | Out of scope |
|---|---|
| Evidence Query Service | Recommendation changes |
| Immutable timeline views | Runtime A integration |
| Filtering (policy / flag / advisory / trial / event) | Educational analytics models |
| Immutable JSON / CSV exports | Adaptive behaviour |
| `ENABLE_EVIDENCE_REVIEW` | Policy modification |
| Provenance-preserving inspection | Automatic optimisation |

**Stop condition:** Stop after the Educational Evidence Review Workspace. Await architecture review before introducing analytical models or allowing historical evidence to influence recommendation policy.

---

## 1. Review workflow

```
Longitudinal Learning Evidence Repository
        │
        │  (append-only; P4-MS002)
        ▼
ENABLE_EVIDENCE_REVIEW (default OFF)
        │
        ▼
EvidenceQueryService (read-only)
        │
        ├── query_by_time_window
        ├── query_by_event_type
        ├── query_by_policy_version
        ├── query_by_trial
        ├── query_by_advisory_field
        ├── filter (combined AND filters)
        ├── build_timeline (immutable view)
        └── export (JSON / CSV; reproducible)
```

Workflow rules:

1. Review never calls repository `append` / update / delete.
2. Disabling `KWALITEC_EVIDENCE_REVIEW` removes DI and rejects traffic (`UNAVAILABLE`).
3. Review with longitudinal repository missing or disabled returns `UNAVAILABLE` (flags remain independent).
4. Timeline and export artefacts are immutable DTOs with `read_only=True`.
5. The review service is **not** passed into Runtime A recommendation paths.

---

## 2. Query model

### 2.1 Single-dimension queries

| Method | Source | Constraint |
|---|---|---|
| `query_by_time_window` | Repository `get_by_time_window` | Inclusive `[start, end]` on `event_timestamp` |
| `query_by_event_type` | Repository `get_by_event_type` | Exact event type match |
| `query_by_policy_version` | Repository `get_by_policy_version` | Exact policy version match |
| `query_by_trial` | Repository `get_by_trial_id` | Exact trial id match |
| `query_by_advisory_field` | Repository `get_by_advisory_field` | Exact advisory field match |

### 2.2 Combined filter (`EvidenceReviewFilter`)

Empty string fields are unset. All set fields apply with **AND** semantics:

| Field | Meaning |
|---|---|
| `start_timestamp` / `end_timestamp` | Inclusive time window |
| `event_type` | Observation event type |
| `policy_version` | Policy / weighting version |
| `trial_id` | Educational trial identifier |
| `advisory_field` | Approved advisory field label |
| `feature_flag` | Flag name inside provenance `feature_flags` |
| `feature_flag_value` | Expected value (`True` → truthy; else equality) |

Combined filtering loads via repository `list_all()` then applies predicates in-process. No mutation. No scoring.

### 2.3 Result envelope

`EvidenceReviewResult` carries:

- `ok` / `error_code` / `message`
- `records` (immutable `LearningEvidenceRecord` snapshots)
- optional `timeline` / `export`
- `filter_snapshot` for audit reproducibility

Error codes: `UNAVAILABLE`, `INVALID_STATE`.

---

## 3. Timeline views

`EvidenceTimeline` is an immutable inspection artefact:

| Field | Purpose |
|---|---|
| `timeline_id` | Deterministic id from record ids + filter snapshot |
| `observation_count` | Number of included records |
| `time_window` | Min / max `event_timestamp` among included records |
| `event_groups` | Per-event-type groups with ordered `record_ids` |
| `provenance_summary` | Distinct components, policies, trials, advisory fields, observed flags, schemas |
| `record_ids` | Append-order ids included in the view |
| `filter_snapshot` | Exact filter that produced the view |
| `read_only` | Always `True` |

Provenance summary preserves stored provenance facts only — no educational interpretation, ranking, or learning-depth claims.

---

## 4. Export format

Exports are immutable and **reproducible** for identical repository state + filter:

| Format | Body |
|---|---|
| `json` | Canonical sorted-key JSON with `records`, `record_count`, `schema_version`, `authority` |
| `csv` | Fixed `CSV_COLUMNS` header + one row per record (provenance nested fields JSON-encoded) |

Export metadata (`EvidenceReviewExport`):

| Field | Notes |
|---|---|
| `export_id` | Deterministic from format + content digest + filter |
| `content` | Exact export body |
| `content_digest` | SHA-256 of body |
| `record_count` | Included observations |
| `filter_snapshot` | Filter used |
| `reproducible` / `read_only` | Always `True` |

No wall-clock timestamp is embedded in export content, so identical inputs yield byte-identical exports.

---

## 5. Governance

| Rule | Enforcement |
|---|---|
| Review is inspection-only | No append / update / delete API on `EvidenceQueryService` |
| Runtime A isolation | Not wired into `RecommendationService` or Adaptive paths |
| Flag independence | `ENABLE_EVIDENCE_REVIEW` does not enable longitudinal storage, trials, policy weighting, or Adaptive |
| Schema compatibility | Review reads P4-MS002 records; review artefacts versioned `p4.ms003.1` |
| Privacy | Continues hashed student ids only (`student_id_hash`); no raw PII in exports |
| Rollback | Unset / `KWALITEC_EVIDENCE_REVIEW=0` removes DI; educational behaviour unchanged |

Dual-run ops field: `DualRunStatus.evidence_review`.

---

## 6. Security considerations

1. **Read-only surface** — review cannot alter educational evidence or policy.
2. **No Runtime A authority transfer** — authority labels remain `evidence_review` vs `runtime_a`.
3. **Hashed identifiers only** — exports retain repository privacy posture.
4. **Flag-gated DI** — default OFF; composition constructs service only when enabled.
5. **Independent from educational write paths** — enabling review never enables recommendation bridges, advisory activation, or policy weighting.
6. **Auditability** — filter snapshots, content digests, and deterministic ids support reproducible governance review.
7. **Future HTTP exposure** (not in this milestone) must remain authenticated / authorised ops surfaces; never student-facing mutation.

---

## 7. Feature flag & rollback

| Environment | Flag field | Default |
|---|---|---|
| `KWALITEC_EVIDENCE_REVIEW` | `ENABLE_EVIDENCE_REVIEW` | OFF |

### Immediate rollback

| Action | Effect |
|---|---|
| Unset / set `KWALITEC_EVIDENCE_REVIEW=0` | Review DI not constructed; queries unavailable |
| Leave flag OFF | Runtime A and all educational behaviour unchanged |

Practical inspection requires longitudinal repository data (`KWALITEC_LONGITUDINAL_EVIDENCE=1`). Flags remain independently controllable: review-only yields gated `UNAVAILABLE` until a repository is available.

---

## 8. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `EvidenceReviewFilter` | `contracts.py` | Immutable query constraints | Scoring / analytics |
| `EvidenceTimeline` | `contracts.py` | Immutable timeline DTO | Educational interpretation |
| `EvidenceReviewExport` | `contracts.py` | Immutable export DTO | Live mutation |
| `EvidenceQueryService` | `service.py` | Query / filter / timeline / export | Append / Runtime A |
| `build_evidence_query_service` | `service.py` | Flag-gated factory | Policy injection |

---

## 9. Acceptance mapping

| Criterion | How satisfied |
|---|---|
| Repository remains read-only | Review service never mutates; count unchanged after query/export |
| Runtime A remains isolated | Separate adapter; not wired into recommendation paths |
| Review exports are reproducible | Deterministic content + export id + digest tests |
| Timeline views preserve provenance | Provenance summary from stored provenance blocks |
| Feature isolation maintained | Independent env var; dual-run field; composition isolation tests |
| All tests pass | `tests/infrastructure/adapters/evidence_review/` + flag tests |
