# FSI-001 — Founder Knowledge Integration

**Document ID:** FSI-001  
**Title:** Founder Knowledge Integration  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure  
**Programme:** Founder System Integration

---

## Purpose

Replace placeholder/static Knowledge and Capability providers with **live
repository-backed** public query APIs.

This capability is **integration only**:

- No Dashboard changes
- No Recommendation Engine changes
- No Weekly Briefing changes
- No AI
- No database persistence
- No Operational State model changes

---

## Architecture

```text
KnowledgeQueryService          CapabilityArchiveQueryService
        │                                    │
        │ public query APIs only             │
        ▼                                    ▼
KnowledgeQueryProvider          CapabilityArchiveProvider
        │                                    │
        └──────────────┬─────────────────────┘
                       ▼
            FounderOperationalStateService
                       ▼
            FounderOperationalState (unchanged model)
```

### Packages

| Package | Capability | Public API |
|---------|------------|------------|
| `app/founder/knowledge_engine/` | FOS-001 | `KnowledgeQueryService` |
| `app/founder/capability_archive/` | FOS-002 | `CapabilityArchiveQueryService` |
| `app/founder/operational_state/` | FOS-005 | live providers (aggregation unchanged) |

Repository scanners stay **inside** their packages. Filesystem paths never
appear in public DTOs.

---

## Provider Flow

1. `KnowledgeQueryService` scans configured roots (`knowledge/`, `research/`,
   `docs/architecture/`, `docs/reviews/`), classifies artefacts into logical
   collections, and returns immutable DTOs.
2. `CapabilityArchiveQueryService` loads JSON entries under
   `research/capability_archive/entries/`, validates required fields, and
   returns immutable capability records plus inventory summary.
3. Operational State defaults to:
   - `KnowledgeQueryProvider` → wraps Knowledge Engine summary
   - `CapabilityArchiveProvider` → wraps Capability Archive summary
4. Aggregation / validation / snapshot shape remain FOS-005 behaviour.

Static sources (`StaticKnowledgeSource`, `StaticCapabilitySource`) remain
available for unit tests that must not touch the filesystem.

---

## Public Query Interfaces

### KnowledgeQueryService

| Method | Returns |
|--------|---------|
| `list_artefacts(collection=None)` | `tuple[KnowledgeArtefactDTO, ...]` |
| `get_summary()` | `KnowledgeIndexSummaryDTO` |
| `list_validation_issues()` | missing roots / scan issues |
| `refresh()` | re-scan repository |

Artefact fields: `artefact_id`, `title`, `collection`, `document_id`.

### CapabilityArchiveQueryService

| Method | Returns |
|--------|---------|
| `list_capabilities()` | `tuple[CapabilityRecordDTO, ...]` |
| `get_capability(id)` | one record or `None` |
| `get_summary()` | `CapabilityArchiveSummaryDTO` |
| `list_validation_issues()` | missing fields / duplicates |
| `refresh()` | re-scan archive |

Record fields: `capability_id`, `status`, `version`, `completion_date`,
`programme`, `subsystem`, `related_documents`, `title`.

Validation reports:

- missing archive root / entries directory
- missing required fields
- duplicate capability IDs

---

## Archive Layout

```text
research/capability_archive/
├── README.md
└── entries/
    ├── FOS-003.json
    ├── FOS-004.json
    └── …
```

---

## Future Extensions

- Dashboard live integration over Operational State / Recommendations /
  Weekly Brief (delivered in FSI-002)
- Expand Knowledge collections without changing Operational State models
- Add richer artefact metadata (owners, tags) behind the same query surface
- Optionally project Operational State summaries into briefing templates

---

## Related Paths

| Path | Role |
|------|------|
| `app/founder/knowledge_engine/` | FOS-001 implementation |
| `app/founder/capability_archive/` | FOS-002 implementation |
| `app/founder/operational_state/providers/knowledge_query.py` | Live Knowledge bridge |
| `app/founder/operational_state/providers/capability_archive.py` | Live Capability bridge |
| `research/capability_archive/` | Repository-backed archive entries |
| `knowledge/founder/FOS-005_OPERATIONAL_STATE.md` | Aggregation consumer |

---

## Owner

Founder Operating System

## Status

Active — Version 1.0
