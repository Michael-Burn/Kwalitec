# FOS-004 — Founder Dashboard

**Document ID:** FOS-004  
**Title:** Founder Dashboard  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure

---

## Purpose

The Founder Dashboard is the executive control centre for Kwalitec.

Version 1 is a **presentation layer only**. It retrieves and displays information already produced by:

| Capability | Role |
|---|---|
| FOS-001 Knowledge Engine | Document / artefact counts and health signals |
| FOS-002 Capability Archive | Capability inventory, status, and release |
| FOS-003 Internal Alpha Pipeline | Weekly feedback summaries and duplicates |

The Dashboard performs **no** engineering analysis, AI inference, editing, uploads, release decisions, recommendations, or analytics.

---

## Architecture

Package root: `app/founder/dashboard/`

```text
app/founder/dashboard/
├── __init__.py              # Flask Blueprint (/founder)
├── routes.py                # GET /founder
├── access.py                # Founder / administrator gate
├── dto/                     # Immutable presentation DTOs
├── providers/               # Wrappers around subsystem read surfaces
├── services/                # FounderDashboardService aggregation
├── templates/               # Jinja2 executive layout
├── static/css|js/           # Bootstrap-aligned styling + table filter
└── tests/                   # Unit tests (mocked providers)
```

### Layering

```text
Templates / routes
        ↓
FounderDashboardService
        ↓
KnowledgeProvider | CapabilityProvider | InternalAlphaProvider
        ↓
Injected subsystem sources (static / future FOS public APIs)
```

Routes stay thin. Service aggregates DTOs. Providers never leak subsystem internals into templates.

---

## Subsystems

### Knowledge Engine (via KnowledgeProvider)

Surfaces counts only:

- Engineering Standards
- Architecture Documents
- Research Documents
- Capability Documents
- Indexed Artefacts

Plus deterministic Version 1 health placeholders from clean/failure signals.

### Capability Archive (via CapabilityProvider)

Surfaces:

- Recent capabilities (id, title, status, version, completion date)
- Completed / active counts
- Current release label

### Internal Alpha (via InternalAlphaProvider)

Read-only view of pipeline **outputs**:

- Current week
- Feedback count
- Category counts
- Duplicate count
- Latest summary filename
- Recent weeks

Does not run the FOS-003 pipeline.

---

## Provider Model

Each provider wraps one subsystem through an injectable **source**:

| Provider | Default source | Test strategy |
|---|---|---|
| `KnowledgeProvider` | `StaticKnowledgeSource` (empty) | Inject snapshot |
| `CapabilityProvider` | `StaticCapabilitySource` (empty) | Inject snapshot |
| `InternalAlphaProvider` | `StaticInternalAlphaSource` (empty) | Inject snapshot |

Dashboard tests **must not** depend on filesystem scanning. When FOS-001 / FOS-002 expose public query APIs, wire them behind the same provider constructors without changing routes or templates.

---

## Security

| Control | Behaviour |
|---|---|
| Authentication | `@login_required` via `founder_required` |
| Authorisation | Founder / administrator only |
| Founder identity | `ADMIN_EMAIL` and/or `FOUNDER_EMAILS` (env or app config) |
| Navigation | “Founder” sidebar link only when `show_founder_nav` is true |
| Ordinary users | HTTP 403 on `/founder` |

No Founder pages are exposed to ordinary authenticated students.

---

## Routes

| Method | Path | Access |
|---|---|---|
| GET | `/founder/` | Founder / administrator |

Blueprint name: `founder_dashboard`.

---

## Health Indicators (Version 1)

Placeholder health is deterministic and non-weighted:

- **100%** when tests pass, validation errors = 0, archive inconsistencies = 0
- **0%** otherwise

No complex scoring.

---

## Visual Design

- Bootstrap 5 + existing Kwalitec semantic tokens
- Cards and responsive grid
- No charts, no JS frameworks, no animations
- Capability table filter is vanilla JS only

---

## Future Roadmap

- Wire live FOS-001 / FOS-002 public query surfaces into providers
- Optional depth pages (document lists remain out of Version 1)
- Explicit `is_founder` role column if multi-admin grows
- FOS-005+ Founder Intelligence remains **out of scope** for this dashboard

---

## Owner

Founder Operating System

## Status

Active — Version 1.0
