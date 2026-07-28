# ILE-001A — Telemetry Guide

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001A  
**Status:** Active  
**Effective:** 2026-07-28  
**Implementation:** `app/application/adaptive_assessment/telemetry.py`

---

## Purpose

Operational product events for Adaptive Assessment UX behaviour. Telemetry is **behavioural only** — never educational answers or learner state.

---

## Allowlisted events

| Event | When |
|---|---|
| `AdaptiveAssessmentViewed` | AA chrome / entry frame shown |
| `QuickCheckStarted` | Learner starts a Quick Check |
| `QuickCheckDismissed` | Learner dismisses without completing |
| `QuickCheckCompleted` | Learner completes a Quick Check |
| `AssessmentDeferred` | Learner defers (“Not now”) |
| `AssessmentExplained` | Learner opens “Why am I seeing this?” |
| `ContextViewed` | Context Card viewed (ILE-001C) |
| `WhyRecommendationOpened` | “Why this recommendation?” opened |
| `ExplanationExpanded` | Other explanation expand |
| `RecommendationAccepted` | Learner accepts framed suggestion |
| `RecommendationDeferred` | Learner defers framed suggestion |
| `ReflectionCompleted` | Reflection step submitted |

Unknown event names are rejected.

---

## Allowed payload (examples)

- `surface` (e.g. `mission_step`, `home`)  
- `session_type_id`  
- `subject_code` (catalogue id, not Twin state)  
- UI timing metadata (e.g. `duration_ms` for chrome, not scoring)

---

## Forbidden payload keys

Never capture:

`answer`, `answers`, `response`, `responses`, `item_stem`, `question_text`, `score`, `mastery`, `readiness_score`, `twin_state`, `learner_state`, `correct`, `incorrect`, `grade`, `pass`, `fail`

Validation raises if these keys appear (including nested dicts).

---

## Privacy principles

1. No educational content in payloads.  
2. No Twin / mastery / readiness scores.  
3. Prefer opaque surface identifiers over free-text reflections.  
4. Future analytics bridge must retain these constraints.

Recorder: `ProductTelemetryRecorder` with pluggable sink (`InMemoryTelemetrySink` for tests).

---

**End of TELEMETRY_GUIDE**
