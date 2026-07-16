# RIP-004 — Research Insight Engine

**Capability ID:** RIP-004  
**Programme:** Research Intelligence Programme  
**Title:** Research Insight Engine  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-16  
**Nature:** Objective aggregation and trend analysis for product research  

---

## Purpose

Convert structured research observations into objective, reproducible product
insights. The Founder requires trustworthy patterns rather than manually reading
every submission.

The Insight Engine performs **aggregation and trend analysis only**. It does
not use AI, does not make product decisions, and does not redesign Educational
Intelligence.

---

## Research succession

```
Research observations
        ↓
Evidence
        ↓
Insight
        ↓
Product Finding
        ↓
Founder Decision
        ↓
Release
        ↓
Verification
```

Insights sit between evidence and product findings. They describe patterns;
only the Founder decides what to act on.

---

## Research Insight Law

**Insights describe patterns. Insights never prescribe decisions. Only the
Founder decides.**

Summaries must not contain recommendations, roadmap suggestions, or imperative
language ("should", "must fix", etc.).

---

## Insight types

Six insight families are implemented:

| Family | Insights |
|--------|----------|
| **Experience** | Average experience, Average confidence, Would Open Tomorrow, Experience trend |
| **Behaviour** | Participation, Returning contributors, Completion rate, Contribution growth |
| **Friction** | Most confusing feature, Most reported friction, Most selected issue category, Fastest growing concern |
| **Trend** | Weekly movement, Version comparisons, Feature improvement, Declining issues |
| **Release** | Findings resolved, New findings, Verified findings, Issues introduced, Release comparison |
| **Research** | Most active feature, Contribution distribution, Implemented contributions, Badge distribution |

Every insight includes:

- Title
- Summary
- Supporting observations (count + submission ids)
- Time window
- Confidence level (Low / Medium / High)
- Affected feature
- Related findings
- Suggested review priority (Critical / High / Medium / Low)

Confidence reflects **amount of supporting evidence**, not correctness:

| Level | Threshold |
|-------|-----------|
| Low | 1–2 observations |
| Medium | 3–9 observations |
| High | 10+ observations |

No probabilities are used.

---

## Time windows

| Window | Description |
|--------|-------------|
| Today | Submissions on the selected date |
| 7 days | Rolling 7-day window (default) |
| 30 days | Rolling 30-day window |
| Current Release | Filter by current product version |
| Previous Release | Filter by prior product version |
| Custom | Founder-selected date range |

---

## Comparisons

Pure numeric comparison — no AI explanations:

| Comparison | Use |
|------------|-----|
| Previous day | Today vs yesterday |
| Previous week | Current window vs prior equal-length window |
| Previous release | Current vs prior product version |

---

## Filters

Insight generation respects the same filters as the research inbox:

- Feature
- Severity
- Version
- Badge
- Date (from / to)
- Classification
- Status
- Submission source

---

## Visualisation

Insight panels added to the Founder Research Command Centre:

- Top Trends
- Emerging Concerns
- Most Improved Areas
- Stable Areas
- Participation
- Release Comparison

The dashboard layout is additive — existing RIP-003 sections are preserved.

---

## Hard boundary

Research Intelligence observes **product experience**.  
Educational Intelligence observes **learning**.

This capability must never:

- write Educational Evidence, Estimated Knowledge/Mastery, Study Progress,
  readiness, mission authority, or Digital Twin educational state;
- modify research submissions, workflow history, or product findings;
- use AI or LLM summarisation;
- generate product decisions or roadmap automation.

---

## Architecture

```
Founder routes (/research/founder)
        ↓
FounderResearchService.build_dashboard_context()
        ↓
ResearchInsightService.generate_insights()
        ↓
Research models (read-only queries)
        ↓
founder_dashboard.html insight panels
```

Insights consume research. They never modify research or educational state.

---

## Files

| Path | Role |
|------|------|
| `app/services/research_insight_service.py` | Insight generation service |
| `app/services/founder_research_service.py` | Delegates to insight engine |
| `app/research/routes.py` | Time window query parameter |
| `app/templates/research/founder_dashboard.html` | Insight panels |
| `tests/test_rip004_research_insight_engine.py` | Capability tests |

---

## Dependencies

| Capability | Relationship |
|------------|--------------|
| RIP-001 | Consumes check-in submissions |
| RIP-002 | Reads badge awards (read-only) |
| RIP-003 | Host dashboard; delegates aggregation |

---

## Known limitations

- Release comparison requires at least two product versions in stored data.
- Stable-area detection uses a fixed experience delta threshold (0.25).
- Participation rate denominator uses distinct mission users, not total alpha cohort size.
- Custom time window requires explicit date parameters via query string.

---

## Verification

Run:

```bash
python -m pytest tests/test_rip004_research_insight_engine.py -v
python -m pytest tests/test_rip003_founder_command_centre.py -v
ruff check app/services/research_insight_service.py app/services/founder_research_service.py
```
