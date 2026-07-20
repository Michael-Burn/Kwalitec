# Learning Session Experience

**Document ID:** V2-019-LEARNING-SESSION-EXPERIENCE  
**Milestone:** V2-019 — Learning Session Experience  
**Status:** Authoritative domain + application + presentation specification  
**Authority:** Architectural — source of truth for the focused study workflow  
**Nature:** Framework-independent session workflow / projection layer + thin Flask UI  

**Packages:**
- `app/domain/session_experience/`
- `app/application/session_experience/`
- `app/presentation/session/` (thin UI)
- `app/templates/session/` · `app/static/css/session.css`

**Depends on:** injected ports only (Learning Session Runtime, Learning Activity Engine, Mission, Student Twin, Adaptive Decision). Does **not** import or modify those educational packages.

**Related:** [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md) · [`STUDENT_EXPERIENCE.md`](STUDENT_EXPERIENCE.md) · [`LEARNING_SESSION_RUNTIME.md`](LEARNING_SESSION_RUNTIME.md) · [`LEARNING_ACTIVITY_ENGINE.md`](LEARNING_ACTIVITY_ENGINE.md) · [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md) · [`VERSION2_ROADMAP.md`](VERSION2_ROADMAP.md)

---

## 1. Vision

A Learning Session is the primary interaction between a student and Kwalitec.

The student should feel they have entered a dedicated study environment. Every session answers:

| Question | Surface |
|----------|---------|
| What am I studying? | Overview objective / topics |
| Why am I studying it? | Overview rationale |
| How much remains? | Progress projection |
| What should I do next? | Single primary action |

One objective. One flow. No branching. No dashboard hopping.

---

## 2. Session Lifecycle

```text
Student Home
    → Start Today's Session
    → Session Overview
    → Learning Activities
    → Reflection
    → Session Summary
    → Complete → Student Home (updated projections)
```

Linear surfaces (`SessionSurface`):

1. `overview`
2. `activity`
3. `reflection`
4. `summary`
5. `complete`

Navigation may advance one step at a time only (`assert_linear_advance`). Skipping or sideways jumps raise `NavigationError`.

---

## 3. Workflow Ownership

| Layer | Owns |
|-------|------|
| Domain | Frozen projections, linear navigation vocabulary |
| Application | Port orchestration, session workspace registry, DTO snapshots |
| Presentation | Flask routes, view models, templates, one primary CTA |

Educational decisions remain in the educational kernel via ports.

---

## 4. Authority

### Session Experience owns

- Workflow
- Navigation (linear)
- Presentation
- Progress **projection** (display of port facts)
- Session **presentation** state (workspace / handle registry)

### Session Experience does **not** own

- Learning decisions
- Recommendations (ADR-005 — Adaptive Decision)
- Evidence storage or scoring
- Mission generation
- Readiness calculations (Student Twin)
- Journey calculations
- Educational algorithms of any kind

See [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md).

---

## 5. Ports

| Port | Role |
|------|------|
| `SessionRuntimePort` | Overview, begin, runtime snapshot, response hand-off, reflection, completion |
| `ActivityEnginePort` | Current activity, submit response, advance, activity progress |
| `MissionPort` | Resolve today's session identity |
| `StudentTwinPort` | Opaque readiness / insight facts for summary labels |
| `AdaptiveDecisionPort` | Next recommendation after completion |

All ports return opaque `dict` documents. Session Experience never imports Runtime / Activity / Twin / Adaptive / Mission packages.

---

## 6. Evidence Lifecycle (invisible to UI)

```text
Student Response
    → Learning Activity Engine (port)
    → Evidence Recording (Session Runtime port)
    → Learning Orchestrator (outside Session Experience)
    → Student Digital Twin
    → Adaptive Decision Engine
    → Updated Student Home projections
```

Presentation never owns evidence. The answer form only posts text to the application facade.

---

## 7. Surfaces

### Overview

Today's objective, estimated duration, activity count, topics, expected readiness improvement, learning goal, why studying, **Begin Session**.

### Activity

Question, context, supporting material, optional hints, answer area, progress bar, next action. No side navigation.

### Reflection

Key insight, concept confidence, suggested improvement, reflection prompt. **No scoring language.**

### Summary / Complete

Topics completed, time studied, activities completed, learning insights, exam readiness change label, next recommendation, estimated next session, **Return Home**.

On completion, Student Home must already display updated readiness, recommendation, and journey progress (produced by the educational loop — not by Session Experience).

---

## 8. UI Philosophy

Calm · Focused · Readable · Accessible · One primary action · Minimal navigation · Professional · Trustworthy

Design tokens reuse the Student Experience system (`DESIGN_SYSTEM.md`) via `session.css` aliases. Cards exist only as interaction/content containers inside the study flow — never as a dashboard collage.

Forbidden learner terms include Digital Twin, Adaptive Decision, Learning Orchestrator, Mission Engine, Curriculum Graph, evidence spine, mastery score.

---

## 9. Integration with Student Experience

`POST /student/session/start` (and revision begin) hand off into:

`/session/<session_id>/overview`

Student Experience remains the “what next / why” shell. Session Experience owns the in-session study environment.

---

## 10. Application Facade

`SessionExperienceService` (`facade.py`) is the sole public application entry point:

- `open_session` / `begin_session`
- `get_activity` / `submit_response` / `advance_activity`
- `get_progress` / `get_reflection` / `continue_from_reflection`
- `get_summary` / `complete_session`
- `navigate` / `get_flow` / `diagnostics`

---

## 11. Constraints (must not)

- Compute readiness
- Compute recommendations
- Compute missions
- Store evidence
- Calculate progress independently of ports
- Duplicate Twin / Adaptive / Journey logic
- Implement educational algorithms
- Branch the session flow

---

## 12. Success Criteria

- Complete learning session workflow  
- Focused study experience  
- Evidence captured through existing platform ports  
- Reflection integrated  
- Updated home projections after return  
- Educational kernel unchanged  
- Framework-independent application layer  
- Production-ready presentation under `/session`  
