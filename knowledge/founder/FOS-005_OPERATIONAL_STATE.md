# FOS-005 — Founder Operational State Service

**Document ID:** FOS-005  
**Title:** Founder Operational State Service  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure

---

## Purpose

The Founder Operational State Service aggregates information from existing
Founder subsystems into a **single immutable operational snapshot**.

It performs **aggregation only**.

It performs **no** AI reasoning, recommendations, scoring, or release decisions.

`FounderOperationalState` is the canonical source for all future Founder
Intelligence capabilities (FOS-006+). Downstream consumers must analyse a
named snapshot rather than querying subsystems ad hoc.

---

## Architecture

Package root: `app/founder/operational_state/`

```text
app/founder/operational_state/
├── __init__.py              # Public exports
├── models/                  # Immutable FounderOperationalState
├── dto/                     # Subsystem DTOs + validation cargo
├── providers/               # Knowledge / Capability / Internal Alpha
├── builders/                # OperationalStateBuilder
├── validators/              # OperationalStateValidator
├── services/                # FounderOperationalStateService
└── tests/                   # Unit tests (mocked providers)
```

### Layering

```text
FounderOperationalStateService
        ↓
OperationalStateBuilder + OperationalStateValidator
        ↓
KnowledgeProvider | CapabilityProvider | InternalAlphaProvider
        ↓
Injected subsystem sources (static / future FOS public APIs)
```

No Flask routes. No templates. Pure application / service layer.

---

## Aggregation Model

| Provider | Subsystem | Summary cargo |
|---|---|---|
| `KnowledgeProvider` | FOS-001 Knowledge Engine | Document counts + engineering signals |
| `CapabilityProvider` | FOS-002 Capability Archive | Inventory counts + release label |
| `InternalAlphaProvider` | FOS-003 Internal Alpha | Week counts + category totals |

Providers never access repository files directly. They wrap injectable
**sources** or public query services. Defaults (FSI-001) are live providers:

- `KnowledgeQueryProvider` → `KnowledgeQueryService`
- `CapabilityArchiveProvider` → `CapabilityArchiveQueryService`

Static sources (`source_version="unwired"`) remain available for isolated
unit tests. Builder and service aggregation logic are unchanged.

Engineering and Release sections are **derived summaries** of Knowledge and
Capability DTOs respectively — not separate subsystem calls.

---

## Snapshot Structure

Every generated state includes:

| Field | Role |
|---|---|
| `generated_at` | UTC timestamp of assembly |
| `snapshot_version` | Operational State schema version (`1.0`) |
| `source_versions` | Per-subsystem version labels |
| `engineering` | Standards count, tests_pass, validation_errors |
| `knowledge` | Document / artefact counts |
| `capability` | Archive inventory summary |
| `internal_alpha` | Week feedback / duplicate / category summary |
| `release` | Current release label + completed capability count |

Sections contain **summary information only**. No raw documents. No feedback
bodies. No archive file payloads.

The snapshot is a frozen dataclass — mutation raises `FrozenInstanceError`.

---

## Validation

`OperationalStateValidator` checks:

- Required sections exist and have correct types
- Snapshot metadata present (`generated_at`, `snapshot_version`)
- Source versions non-empty and free of duplicate non-`unwired` tokens
- Snapshot version matches the expected schema version
- Counts are non-negative
- Cross-section consistency (engineering ↔ knowledge standards;
  release ↔ capability completed count)

Failures raise `OperationalStateValidationError` with an explicit
`ValidationReport` of issue codes.

---

## Service Flow

`FounderOperationalStateService.get_state()`:

1. Query Knowledge, Capability, and Internal Alpha providers
2. Build `FounderOperationalState` via `OperationalStateBuilder`
3. Validate completeness
4. Return the immutable snapshot

Coordinator only — no interpretation beyond aggregation.

---

## Future Consumers

| Consumer | Expected use |
|---|---|
| FOS-006+ Founder Intelligence | Analyse a named snapshot; never re-query subsystems for truth |
| Future Dashboard read models | Optional projection of operational state (out of scope here) |
| Release advisory services | Read `release` / `capability` summaries only |

Consumers must record which `snapshot_version` and `source_versions` they
analysed.

---

## Constraints

Version 1 intentionally does **not**:

- Implement AI or LLM calls
- Produce recommendations or scores
- Make release decisions
- Modify Dashboard, Internal Alpha, or Knowledge Engine packages
- Add Flask routes or templates

---

## Related Paths

| Path | Role |
|------|------|
| `app/founder/operational_state/` | Implementation |
| `knowledge/founder/FOS-005_OPERATIONAL_STATE.md` | This specification |
| `knowledge/founder/FOS-003_INTERNAL_ALPHA_PIPELINE.md` | Upstream Internal Alpha |
| `knowledge/founder/FOS-004_FOUNDER_DASHBOARD.md` | Presentation layer (separate) |

---

## Owner

Founder Operating System

## Status

Active — Version 1.0
