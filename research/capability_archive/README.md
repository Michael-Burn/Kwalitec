# Capability Archive

## Purpose

Repository-backed capability inventory consumed by the Founder Capability
Archive query API (`CapabilityArchiveQueryService`, FOS-002 / FSI-001).

## Layout

```text
research/capability_archive/
├── README.md
└── entries/
    ├── FOS-003.json
    └── …
```

Each entry is a JSON object with:

| Field | Meaning |
|-------|---------|
| `capability_id` | Stable capability identifier |
| `title` | Human-readable title |
| `status` | Lifecycle status (`completed`, `active`, …) |
| `version` | Capability version label |
| `completion_date` | ISO date (`YYYY-MM-DD`) |
| `programme` | Owning programme |
| `subsystem` | Logical subsystem name |
| `related_documents` | Document identifiers (not filesystem paths) |

## Owner

Founder Operating System

## Status

Active — Version 1.0
