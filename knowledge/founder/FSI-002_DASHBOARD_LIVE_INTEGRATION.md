# FSI-002 — Founder Dashboard Live Integration

**Document ID:** FSI-002  
**Title:** Founder Dashboard Live Integration  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure  
**Programme:** Founder System Integration

---

## Purpose

Replace static Founder Dashboard providers with **live Founder public
services** so the dashboard is a presentation layer over:

| Capability | Public service | Cargo |
|------------|----------------|-------|
| FOS-005 Operational State | `FounderOperationalStateService` | `FounderOperationalState` |
| FOS-006 Recommendation Engine | `FounderRecommendationService` | `RecommendationSet` |
| FOS-007 Weekly Briefing | `FounderWeeklyBriefingService` | `FounderWeeklyBrief` |

This capability is **integration only**:

- No Recommendation Engine changes
- No Weekly Brief generation changes
- No Operational State model changes
- No Knowledge Engine / Capability Archive / Internal Alpha Pipeline changes
- No AI, charts, analytics, editing, or uploads
- No repository scanning from the dashboard package

---

## Architecture

```text
FounderOperationalStateService
FounderRecommendationService
FounderWeeklyBriefingService
            │
            ▼
OperationalStateProvider | RecommendationProvider | WeeklyBriefProvider
            │
            ▼
    FounderDashboardService  (coordinator only)
            │
            ▼
     Dashboard DTOs → Templates
```

### Packages

| Package | Capability | Role in FSI-002 |
|---------|------------|-----------------|
| `app/founder/dashboard/` | FOS-004 | Live providers + DTO mapping + UI |
| `app/founder/operational_state/` | FOS-005 | Unchanged public `get_state()` |
| `app/founder/recommendations/` | FOS-006 | Unchanged public `recommend(state)` |
| `app/founder/briefing/` | FOS-007 | Unchanged public `generate_brief(...)` |

The dashboard never imports repository scanners. Filesystem access stays
inside FOS-001 / FOS-002 (and only via FOS-005’s existing live bridges).

---

## Provider Flow

1. `OperationalStateProvider.get_state()` calls
   `FounderOperationalStateService.get_state()`.
2. `RecommendationProvider.get_recommendations(state)` calls
   `FounderRecommendationService.recommend(state)`.
3. `WeeklyBriefProvider.get_brief(state, set)` calls
   `FounderWeeklyBriefingService.generate_brief(state, set)` **without**
   `output_dir` (in-memory metadata only — no export from the dashboard).
4. `FounderDashboardService` maps the three cargos into presentation DTOs
   and returns `DashboardPage`.

Static dashboard providers (`StaticKnowledgeSource`,
`StaticCapabilitySource`, `StaticInternalAlphaSource`) are removed.

---

## DTO Mapping

| Live cargo | Dashboard DTO |
|------------|---------------|
| `FounderOperationalState.engineering` + `.knowledge` | `KnowledgeSection` + overview health fields |
| `FounderOperationalState.capability` | `CapabilitySection` (counts + recent IDs) |
| `FounderOperationalState.internal_alpha` | `InternalAlphaSection` |
| `FounderOperationalState.snapshot_version` | `DashboardOverview.snapshot_version` |
| `RecommendationSet` (first 5) | `RecommendationsSection.top` |
| `FounderWeeklyBrief` metadata | `WeeklyBriefSection` |

Templates receive **DTOs only** — never raw `FounderOperationalState`,
`Recommendation`, or `FounderWeeklyBrief` objects.

Engineering / architecture health remain the Version 1 display projection
already used by FOS-004 (100 when tests pass and validation errors are
zero; otherwise 0). The dashboard does not invent new scoring.

Top recommendations are capped at **5**. Priority ordering comes from
FOS-006 (already sorted Critical → Low); the dashboard does not re-rank.

---

## Error Handling

| Failure | Behaviour |
|---------|-----------|
| Operational State unavailable | Empty page DTOs; dashboard still renders |
| RecommendationSet unavailable | State sections render; recommendations/brief empty |
| Weekly Brief unavailable | State + recommendations render; brief metadata empty |

Providers catch service exceptions, log them, and return `None`. The
service never raises to the route for missing Founder data.

---

## Access

Founder-only access is unchanged (`founder_required` /
`ADMIN_EMAIL` ∪ `FOUNDER_EMAILS`). No permission model changes.

---

## Testing

Dashboard unit tests inject stub public services through the three
providers. No filesystem, no Flask app, no repository scanning.

---

## Future Extensions

- Wire Internal Alpha into Operational State with a live provider (parity
  with FSI-001 Knowledge / Capability bridges)
- Optional read-only brief body preview section
- Capability Archive detail rows via a dedicated public query DTO (still
  not scanned from the dashboard)
- Cache snapshot / recommendation / brief results across requests (FSI-003+)

---

## Related Paths

| Path | Role |
|------|------|
| `app/founder/dashboard/providers/` | Live provider wrappers |
| `app/founder/dashboard/services/dashboard_service.py` | Coordinator |
| `app/founder/dashboard/dto/` | Presentation DTOs |
| `knowledge/founder/FOS-004_FOUNDER_DASHBOARD.md` | Dashboard capability doc |
| `knowledge/founder/FSI-001_KNOWLEDGE_INTEGRATION.md` | Prior live OS wiring |

---

## Owner

Founder Operating System

## Status

Active — Version 1.0
