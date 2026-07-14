# FOS-007 — Founder Weekly Briefing

**Document ID:** FOS-007  
**Title:** Founder Weekly Briefing  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure

---

## Purpose

The Founder Weekly Briefing converts the current
`FounderOperationalState` and `RecommendationSet` into a deterministic
executive report.

Version 1 allows the Founder to understand the state of Kwalitec in under
five minutes.

It performs **no** AI reasoning, LLM calls, machine learning, or free-form
natural language generation. Section wording comes only from predefined
templates with value interpolation from the two inputs.

The report is generated **only when requested**. Scheduling, email delivery,
and Dashboard integration are out of scope for Version 1.

---

## Architecture

Package root: `app/founder/briefing/`

```text
app/founder/briefing/
├── __init__.py              # Public exports
├── config.py                # Versions, section order, export filenames
├── models/                  # FounderWeeklyBrief, BriefSection, BriefMetadata
├── dto/                     # Validation + export result cargo
├── templates/               # Deterministic section template builders
├── builders/                # FounderWeeklyBriefBuilder
├── exporters/               # Markdown + JSON writers (no business logic)
├── providers/               # SectionTemplateProvider
├── validators/              # FounderWeeklyBriefValidator
├── services/                # FounderWeeklyBriefingService
└── tests/                   # Unit tests (mocked state + recommendations)
```

### Layering

```text
FounderWeeklyBriefingService
        ↓
FounderWeeklyBriefBuilder + FounderWeeklyBriefValidator
        ↓
SectionTemplateProvider → BriefSection[]
        ↓
Markdown / JSON exporters (optional)
        ↓
FounderOperationalState + RecommendationSet  (sole inputs)
```

No Flask routes. No HTML templates. No Dashboard modifications.
Pure application / service layer.

---

## Report Structure

Version 1 generates:

```text
# Founder Weekly Briefing

## Executive Summary
## Engineering Overview
## Internal Alpha
## Capability Progress
## Release Readiness
## Top Priorities
## Recommendations
## Risks
## Next Week Focus

---
## Metadata
```

Canonical model fields on `FounderWeeklyBrief`:

| Field | Source |
|---|---|
| `week` | `state.internal_alpha.current_week` |
| `generated_at` | injectable clock |
| `snapshot_version` | `state.snapshot_version` |
| `recommendation_version` | FOS-006 cargo contract (`1.0`) |
| section summaries | predefined templates |
| `metadata` | `generated_at`, `snapshot_version`, `report_version` |

---

## Template System

Nine deterministic template builders assemble `BriefSection` instances:

| Order | Title | Primary inputs |
|---|---|---|
| 1 | Executive Summary | status, counts, release |
| 2 | Engineering Overview | engineering + knowledge counts |
| 3 | Internal Alpha | feedback / duplicate / categories |
| 4 | Capability Progress | capability inventory |
| 5 | Release Readiness | release + engineering + status |
| 6 | Top Priorities | top N recommendations |
| 7 | Recommendations | full RecommendationSet |
| 8 | Risks | Critical / High recommendations |
| 9 | Next Week Focus | top priorities or healthy posture |

`FounderWeeklyBriefBuilder` performs construction only — no scoring and no
decision making. Advisory priorities come exclusively from the upstream
`RecommendationSet`.

---

## Export Formats

| Format | Filename | Notes |
|---|---|---|
| Markdown | `FOUNDER_WEEKLY_REPORT.md` | Human-readable executive report |
| JSON | `founder_weekly_report.json` | Machine-readable ordered sections + metadata |

Exporters contain **no** business logic. They render already-validated
`FounderWeeklyBrief` cargo. `render()` methods support in-memory tests
without filesystem writes; `export()` writes under a caller-supplied
directory when the service is asked to export.

---

## Validation

`FounderWeeklyBriefValidator` checks:

- Required sections present with non-empty content
- Section ordering matches the canonical Version 1 sequence
- Metadata completeness (`generated_at`, `snapshot_version`, `report_version`)
- Snapshot version alignment with the source `FounderOperationalState`
- Report version matches the expected `REPORT_VERSION`
- Recommendation section references every recommendation id

Failures raise `BriefingValidationError` with an explicit `ValidationReport`.

---

## Service Flow

```text
FounderOperationalState + RecommendationSet
        ↓
FounderWeeklyBriefingService.generate(...)
        ↓
FounderWeeklyBriefBuilder.build(...)
        ↓
FounderWeeklyBriefValidator.validate(...)
        ↓
WeeklyBriefExportBundle.export_all(...)   (optional)
        ↓
BriefingResult(brief, exports?)
```

---

## Dependencies

Consume **only**:

- `FounderOperationalState` (FOS-005)
- `RecommendationSet` (FOS-006)

Never call directly:

- Knowledge Engine
- Capability Archive
- Internal Alpha Pipeline
- Founder Dashboard

---

## Future Evolution

Version 1 intentionally excludes automation. A future FOS capability may:

- Schedule weekly generation
- Deliver the Markdown report by email
- Surface the briefing on the Founder Dashboard
- Add optional AI-assisted narrative **after** the deterministic core

Any future path must:

- Keep FOS-005 + FOS-006 as the factual/advisory inputs
- Preserve template-driven sections for Critical founder gates
- Label any generative text as non-authoritative
- Avoid mutating Operational State, Recommendations, or product subsystems

---

## Constraints

Version 1 intentionally does **not**:

- Implement AI, OpenAI, or LLMs
- Implement email delivery or scheduling
- Modify Dashboard, Recommendation Engine, Operational State, Internal Alpha,
  or Knowledge Engine
- Expose HTTP endpoints
- Persist briefings to a database

---

## Related Paths

| Path | Role |
|------|------|
| `app/founder/briefing/` | Implementation |
| `knowledge/founder/FOS-007_FOUNDER_WEEKLY_BRIEFING.md` | This specification |
| `knowledge/founder/FOS-005_OPERATIONAL_STATE.md` | Snapshot input |
| `knowledge/founder/FOS-006_RECOMMENDATION_ENGINE.md` | Advisory input |
| `app/founder/operational_state/` | Upstream aggregation |
| `app/founder/recommendations/` | Upstream recommendations |

---

## Owner

Founder Operating System

## Status

Active — Version 1.0
