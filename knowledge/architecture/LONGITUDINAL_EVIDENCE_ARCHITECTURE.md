# Programme IV — Longitudinal Learning Evidence Repository

**Milestone:** P4-MS002 — Longitudinal Learning Evidence Repository  
**Directive:** Engineering Directive 001 (Longitudinal Learning Evidence Repository)  
**Status:** Implemented (evidence storage only)  
**Package:** `app/infrastructure/adapters/longitudinal_evidence/`  
**Repository:** `InMemoryLongitudinalEvidenceRepository` (implements `LongitudinalEvidenceRepository`)  
**Feature flag:** `KWALITEC_LONGITUDINAL_EVIDENCE` → `ENABLE_LONGITUDINAL_EVIDENCE` (**default OFF**)  
**Schema version:** `p4.ms002.1` (`LONGITUDINAL_EVIDENCE_SCHEMA_VERSION`)  
**Companions:** `EDUCATIONAL_TRIAL_ARCHITECTURE.md`, `ADVISORY_OUTCOME_MEASUREMENT.md`, `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`

---

## 0. Purpose

Create a durable repository for **longitudinal educational observations** collected across study sessions, missions, reflections, advisory activations, and educational trials.

> Educational optimisation should be based on accumulated evidence rather than isolated events.

This milestone stores evidence **only**. It must **not** influence Runtime A, Adaptive Engine, Recovery, or educational policy.

| In scope | Out of scope |
|---|---|
| Immutable `LearningEvidenceRecord` | Recommendation changes |
| Append-only repository interface | Additional advisory fields |
| In-memory persistence adapter | Adaptive Engine changes |
| Provenance preservation | Recovery optimisation |
| `ENABLE_LONGITUDINAL_EVIDENCE` | Policy weighting changes |
| Schema compatibility helpers | Automatic learning analytics |

**Stop condition:** Stop after the Longitudinal Learning Evidence Repository. Await architecture review before allowing longitudinal evidence to influence educational policy.

---

## 1. Repository lifecycle

```
Educational observation
  (session / mission / reflection / advisory / trial)
        │
        ▼
LearningEvidenceRecord (immutable; hashed student id)
        │
        ▼
ENABLE_LONGITUDINAL_EVIDENCE (default OFF)
        │
        ▼
LongitudinalEvidenceRepository.append
        │
        ├── reject when flag OFF (UNAVAILABLE)
        ├── reject invalid / unsupported schema
        ├── reject duplicate record_id (APPEND_ONLY_VIOLATION)
        └── store frozen snapshot
                │
                ├── get_by_time_window
                ├── get_by_event_type
                └── get_by_policy_version
```

Lifecycle rules:

1. Records are immutable once constructed (`LearningEvidenceRecord`).
2. Storage is append-only — never update or delete by `record_id`.
3. Duplicate `record_id` appends are rejected (append-only violation).
4. Disabling `KWALITEC_LONGITUDINAL_EVIDENCE` removes DI and rejects traffic.
5. The repository is **not** passed into Runtime A recommendation paths.

---

## 2. Schema evolution

| Property | Value |
|---|---|
| Current schema | `p4.ms002.1` |
| Supported readers | Exact match to `SUPPORTED_SCHEMA_VERSIONS` |
| Forward compatibility | Unknown `source_component` labels preserved; unknown event types rejected at write |
| Canonical form | Sorted-key JSON via `serialize()` / `to_canonical_dict()` |

Evolution rules for later milestones:

1. New optional fields may be added behind a new schema version.
2. Readers must declare supported versions explicitly.
3. Writers must set `schema_version` on every record.
4. Unsupported versions are rejected at append (`schema_version_unsupported`).

---

## 3. Provenance model

Every stored record carries a `LongitudinalEvidenceProvenance` block:

| Dimension | Purpose |
|---|---|
| `originating_component` | Which subsystem emitted the observation |
| `policy_version` | Policy / weighting version in force (if any) |
| `feature_flags` | Flag snapshot relevant to the observation |
| `trial_context` | Trial id / cohort / assignment context (if any) |
| `advisory_provenance` | Advisory field / activation explainability (if any) |
| `collected_at` | Collection timestamp |
| `notes` | Explicit non-claims / operational annotations |

Top-level record fields also mirror operational keys used for retrieval:

- `source_component`
- `policy_version`
- `advisory_field` (locked to approved surface when present)
- `trial_id`

Personal identifiers are **not** stored. Callers must supply `student_id_hash` (helper: `opaque_student_id_hash`).

---

## 4. Retention considerations

| Topic | Guidance (this milestone) |
|---|---|
| Durability | Process-local in-memory adapter; interface stable for SQL / object store later |
| Retention policy | Not enforced here — ops retention is a future governance decision |
| Deletion | Not supported on the repository interface (append-only) |
| Privacy | Hashed student ids only; no email / name / raw student id |
| Export | Canonical serialization supports audit export without analytics |

Future durable backends must preserve append-only semantics and provenance completeness.

---

## 5. Future integration points

After architecture review, publishers / consumers **may** be considered (not implemented here):

| Source | Observation |
|---|---|
| Unified Journey / Day Experience | Study session / mission / reflection completions |
| Controlled Advisory / Outcome Measurement | Advisory activation outcomes |
| Educational Trial | Cohort / metric observations |
| Evidence Platform | Factual evidence intake bridge (optional) |

| Consumer (future, gated) | Use |
|---|---|
| Educational review / ops | Time-window and policy-version inspection |
| Policy governance | Accumulated evidence before policy change |
| Analytics (later programme) | Separate analytical layer — not this repository |

**Forbidden until review:** feeding longitudinal evidence into Runtime A ranking, Adaptive decisions, Recovery optimisation, or automatic policy updates.

---

## 6. Feature flag & rollback

| Environment | Flag field | Default |
|---|---|---|
| `KWALITEC_LONGITUDINAL_EVIDENCE` | `ENABLE_LONGITUDINAL_EVIDENCE` | OFF |

### Immediate rollback

| Action | Effect |
|---|---|
| Unset / set `KWALITEC_LONGITUDINAL_EVIDENCE=0` | Repository DI not constructed; append / query unavailable |
| Leave flag OFF | Runtime A and all educational behaviour unchanged |

Dual-run ops field: `DualRunStatus.longitudinal_evidence`.

Independence: enabling longitudinal evidence does **not** enable educational trials, evidence platform, policy weighting, or Adaptive Engine.

---

## 7. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `LearningEvidenceRecord` | `contracts.py` | Immutable evidence DTO | Analytics / scoring |
| `LongitudinalEvidenceProvenance` | `contracts.py` | Required provenance block | Policy decisions |
| `LongitudinalEvidenceRepository` | `contracts.py` | Append / retrieve Protocol | Aggregation |
| `InMemoryLongitudinalEvidenceRepository` | `repository.py` | Process-local append-only store | Durable warehouse |
| `build_longitudinal_evidence_repository` | `repository.py` | Flag-gated factory | Runtime A injection |

---

## 8. Acceptance mapping

| Criterion | How satisfied |
|---|---|
| Evidence stored independently of Runtime A | Separate adapter package; not wired into `RecommendationService` |
| Repository is append-only | Duplicate `record_id` rejected; no update / delete API |
| Provenance is preserved | Required provenance fields validated and round-tripped |
| Runtime A behaviour unchanged | Flag default OFF; no recommendation path changes |
| Feature flag isolation | Independent env var; dual-run field; composition isolation tests |
| All tests pass | `tests/infrastructure/adapters/longitudinal_evidence/` + flag tests |
