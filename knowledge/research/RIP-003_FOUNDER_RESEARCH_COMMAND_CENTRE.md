# RIP-003 — Founder Research Command Centre

**Capability ID:** RIP-003  
**Programme:** Research Intelligence Programme  
**Title:** Founder Research Command Centre  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-16  
**Nature:** Founder operational workspace for product research  

---

## Purpose

Provide the Founder with one coherent operational environment to transform
Internal Alpha research into product decisions.

This is **not** an analytics dashboard. It is a Research Command Centre
designed to answer, on every visit:

1. How are students experiencing Kwalitec today?
2. What changed since yesterday?
3. What needs my attention first?
4. Which feedback deserves action?
5. What improvements are ready for the roadmap?

---

## Hard boundary

Research Intelligence observes **product experience**.  
Educational Intelligence observes **learning**.

This capability must never:

- write Educational Evidence, Estimated Knowledge/Mastery, Study Progress,
  readiness, mission authority, or Digital Twin educational state;
- redesign Educational Intelligence, Educational Truth, recommendations,
  or readiness;
- introduce AI summarisation (pure aggregation only).

---

## Architecture

```
Founder routes (/research/founder)
        ↓
FounderResearchService
        ↓
Research models (submissions, workflow, findings, notes)
        ↓
Templates (founder_dashboard.html, finding_detail.html)
```

Integrates with RIP-002 `ContributorRecognitionService` for Helpful,
Insightful, and Implemented marks (Product Shaper badge).

---

## Research lifecycle

Every feedback submission enters **New**. The Founder moves items through:

```
New → Under Review → Accepted → Planned → Implemented → Released → Verified
```

Additional states: **Rejected**, **Clarification Requested**.

Every transition appends a row to `research_feedback_status_transitions`
with timestamp, reviewer, and optional rationale. Historical decisions are
never overwritten.

---

## Founder workflow

| Action | Effect |
|--------|--------|
| Mark Helpful / Insightful | Updates `ResearchFeedbackReview` (RIP-002) |
| Accept / Reject / Clarify | Workflow transition |
| Plan / Implement / Release / Verify | Workflow transition |
| Implement | Also marks review implemented; may award Product Shaper |
| Add internal note | Appends `ResearchFounderNote` |

No student-facing comments in this capability.

---

## Product Findings

Founder may create **Product Finding** records with:

- Title, Summary, Severity, Feature Area
- Linked feedback (many submissions → one finding)
- Status (same lifecycle vocabulary)
- Target Release (e.g. 1.0.1, 1.1.0, Version 2)
- Internal notes

Status history stored in `research_product_finding_status_transitions`.

---

## Home overview

**Internal Alpha Summary:** active participants, completed check-ins,
participation rate, average product experience, would-open-tomorrow rate,
average confidence, outstanding reviews, implemented feedback, product
shapers, newest contributions.

**Product Health:** most loved/confusing feature, most mentioned friction,
fastest growing concern, recently improved areas, areas with no feedback.

**Insights:** most common feature, friction, suggestion category;
7-day participation and contribution trends; recently awarded badges.

---

## Filters and search

Filter by version, badge, feature, severity, status, classification, date
range, submission source.

Keyword search across free text, feature, friction, version. Student
search by email.

---

## Files

| Path | Role |
|------|------|
| `app/services/founder_research_service.py` | Aggregation, workflow, findings |
| `app/models/research_feedback.py` | Extended ORM models |
| `app/research/routes.py` | Founder HTTP surface |
| `app/research/forms.py` | Filter, note, finding forms |
| `app/templates/research/founder_dashboard.html` | Command centre UI |
| `app/templates/research/finding_detail.html` | Finding detail UI |
| `migrations/versions/202607160003_*.py` | Schema migration |
| `tests/test_rip003_founder_command_centre.py` | Capability tests |

---

## Known limitations

- Participation rate uses mission-active users as denominator (proxy for
  Internal Alpha cohort until explicit cohort membership exists).
- No public roadmap or student discussion system.
- Legacy filesystem research pipeline (`research/internal_alpha/`) remains
  separate from in-app DB research.
- Founder review legacy route (`/research/founder/review/<id>`) retained;
  redirects to Command Centre after save.

---

## Out of scope (this capability)

- AI summarisation
- Educational Intelligence changes
- Public roadmap
- Student discussion system

---

**Stop.** Return for Architecture Review.
