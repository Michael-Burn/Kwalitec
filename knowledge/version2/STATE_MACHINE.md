# Learning Journey State Machine

**Document ID:** V2-001-STATE  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Authoritative transition specification  
**Nature:** Architecture only — no runtime implementation  

**Parent domain:** [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md)

This document defines lawful and invalid state transitions for Learning Journeys, Learning Sessions, and related recommendation / reflection postures.

---

## 1. Design Rules

1. **Explicit transitions only.** No implied jumps.
2. **Terminal honesty.** `COMPLETED` requires completion criteria; `ABANDONED` requires explicit intent.
3. **Pause ≠ complete.** Pausing never advances coverage completion.
4. **Session complete ≠ journey complete.**
5. **Deterministic guards.** Same state + same event + same guard inputs → same next state.
6. **History.** Every successful transition appends to `JourneyHistory`.
7. **Constitution alignment.** Transitions must not mint Estimated Mastery or rewrite Evidence.

---

## 2. JourneyState Machine

### 2.1 States

| State | Terminal? | Student meaning |
|-------|-----------|-----------------|
| `NOT_STARTED` | No | Journey authorised; work not begun |
| `ACTIVE` | No | Journey in progress |
| `PAUSED` | No | Intentionally suspended |
| `RESUMED` | No | Just resumed from pause (implementation may immediately settle to `ACTIVE`) |
| `READY_FOR_COMPLETION` | No | Criteria met; confirmation pending |
| `COMPLETED` | Yes | Topic Complete outcome recorded |
| `DEFERRED` | No* | Postponed with intent to return |
| `ABANDONED` | Yes | Ended without Topic Complete |

\* `DEFERRED` is non-terminal educationally; it may later return to `ACTIVE` / `NOT_STARTED` reactivation rules.

### 2.2 Primary happy path

```
NOT_STARTED
    ↓  start_journey
ACTIVE
    ↓  pause_journey
PAUSED
    ↓  resume_journey
RESUMED
    ↓  settle_active   (automatic or explicit)
ACTIVE
    ↓  completion_criteria_met
READY_FOR_COMPLETION
    ↓  confirm_topic_complete
COMPLETED
```

Sessions and evidence accumulate while the journey is `ACTIVE` or `RESUMED` (and may be planned while `PAUSED`, but active session work should not run in `PAUSED` without resume).

### 2.3 Lawful transitions

| From | Event | To | Guards |
|------|-------|----|--------|
| `NOT_STARTED` | `start_journey` | `ACTIVE` | Journey bound to topic + learner; curriculum topic active |
| `NOT_STARTED` | `defer_journey` | `DEFERRED` | Explicit deferral |
| `NOT_STARTED` | `abandon_journey` | `ABANDONED` | Explicit abandonment |
| `ACTIVE` | `pause_journey` | `PAUSED` | No requirement that session is closed; open session must be paused or abandoned first in strict mode (recommended) |
| `ACTIVE` | `completion_criteria_met` | `READY_FOR_COMPLETION` | Criteria true (see Curriculum Model) |
| `ACTIVE` | `defer_journey` | `DEFERRED` | Explicit deferral |
| `ACTIVE` | `abandon_journey` | `ABANDONED` | Explicit abandonment |
| `PAUSED` | `resume_journey` | `RESUMED` | Learner resumes |
| `PAUSED` | `defer_journey` | `DEFERRED` | Explicit deferral |
| `PAUSED` | `abandon_journey` | `ABANDONED` | Explicit abandonment |
| `RESUMED` | `settle_active` | `ACTIVE` | Always allowed; may be implicit |
| `RESUMED` | `pause_journey` | `PAUSED` | Allowed |
| `RESUMED` | `completion_criteria_met` | `READY_FOR_COMPLETION` | Criteria true |
| `RESUMED` | `abandon_journey` | `ABANDONED` | Explicit |
| `READY_FOR_COMPLETION` | `confirm_topic_complete` | `COMPLETED` | Student or lawful coverage confirmation per Constitution |
| `READY_FOR_COMPLETION` | `continue_journey` | `ACTIVE` | Student chooses more work despite criteria |
| `READY_FOR_COMPLETION` | `pause_journey` | `PAUSED` | Allowed |
| `READY_FOR_COMPLETION` | `abandon_journey` | `ABANDONED` | Explicit; rare and disclosed |
| `DEFERRED` | `reactivate_journey` | `ACTIVE` | Or `NOT_STARTED` if no session history yet |
| `DEFERRED` | `abandon_journey` | `ABANDONED` | Explicit |

### 2.4 Invalid journey transitions

| From | To | Why invalid |
|------|----|-------------|
| `NOT_STARTED` | `COMPLETED` | No work / no criteria path |
| `NOT_STARTED` | `READY_FOR_COMPLETION` | Criteria cannot be met with zero journey work unless explicitly cold-started by prior continuity remap (special case must be named; default invalid) |
| `NOT_STARTED` | `RESUMED` | Nothing to resume |
| `ACTIVE` | `COMPLETED` | Must pass `READY_FOR_COMPLETION` + confirm |
| `PAUSED` | `COMPLETED` | Cannot complete while paused |
| `PAUSED` | `READY_FOR_COMPLETION` | Evaluate criteria only after resume or explicit evaluation event from `ACTIVE`/`RESUMED` |
| `COMPLETED` | any non-terminal | Journey is closed; new work requires a new journey or lawful reopen milestone (not defined in V2-001) |
| `ABANDONED` | `COMPLETED` | Abandonment is not completion |
| `ABANDONED` | `ACTIVE` | Requires explicit reopen policy (future); default invalid |
| Any | `COMPLETED` on `session_completed` alone | Session never completes journey |
| Any | `COMPLETED` because Estimated Mastery crossed a threshold | Forbidden by Constitution |
| Any | `COMPLETED` because a recommendation was accepted | Guidance ≠ completion |

### 2.5 Journey event catalogue (non-exhaustive)

| Event | Typical source |
|-------|----------------|
| `start_journey` | First learning session start for topic |
| `pause_journey` | Student pause / sustained inactivity policy (if disclosed) |
| `resume_journey` | Student resume |
| `settle_active` | Engine normalisation after resume |
| `session_completed` | Session engine (updates progress; may trigger criteria check) |
| `evidence_recorded` | Evidence pipeline |
| `reflection_captured` | Session close |
| `completion_criteria_met` | Journey Engine evaluation |
| `confirm_topic_complete` | Lawful coverage confirmation |
| `continue_journey` | Student declines early completion |
| `defer_journey` | Student / planner deferral |
| `abandon_journey` | Explicit abandonment |
| `reactivate_journey` | Return from deferral |

---

## 3. SessionState Machine

### 3.1 States

| State | Terminal? | Meaning |
|-------|-----------|---------|
| `NOT_STARTED` | No | Planned / recommended |
| `ACTIVE` | No | In progress |
| `PAUSED` | No | Suspended |
| `COMPLETED` | Yes | Finished; reflection flow engaged |
| `ABANDONED` | Yes | Ended without completion |

### 3.2 Happy path

```
NOT_STARTED
    ↓  start_session
ACTIVE
    ↓  pause_session
PAUSED
    ↓  resume_session
ACTIVE
    ↓  finish_session
COMPLETED
    ↓  capture_reflection
(educationally closed)
```

### 3.3 Lawful transitions

| From | Event | To | Guards |
|------|-------|----|--------|
| `NOT_STARTED` | `start_session` | `ACTIVE` | Parent journey in `ACTIVE` or `RESUMED` (or `NOT_STARTED` journey co-starts) |
| `ACTIVE` | `pause_session` | `PAUSED` | — |
| `PAUSED` | `resume_session` | `ACTIVE` | — |
| `ACTIVE` | `finish_session` | `COMPLETED` | — |
| `PAUSED` | `finish_session` | `COMPLETED` | Allowed if student finishes from pause |
| `ACTIVE` | `abandon_session` | `ABANDONED` | Explicit |
| `PAUSED` | `abandon_session` | `ABANDONED` | Explicit |
| `NOT_STARTED` | `abandon_session` | `ABANDONED` | Cancel planned session |
| `COMPLETED` | `capture_reflection` | `COMPLETED` | Reflection posture `CAPTURED`; session remains COMPLETED |

### 3.4 Invalid session transitions

| From | To | Why invalid |
|------|----|-------------|
| `NOT_STARTED` | `COMPLETED` | Must start (or explicitly mark zero-length complete — not allowed) |
| `NOT_STARTED` | `PAUSED` | Cannot pause before start |
| `COMPLETED` | `ACTIVE` | Sessions are not restarted; open a new session |
| `COMPLETED` | `PAUSED` | Terminal |
| `ABANDONED` | `COMPLETED` | Abandonment is not completion |
| `ABANDONED` | `ACTIVE` | Default invalid |
| Any session event | Journey `COMPLETED` | Wrong aggregate |
| `finish_session` while parent journey `PAUSED` | — | Invalid unless journey resumes first (strict mode) |

### 3.5 Session vs journey coupling

| Session event | Journey effect |
|---------------|----------------|
| `start_session` | May `start_journey` if journey `NOT_STARTED`; else history entry |
| `finish_session` | Progress update; optional `completion_criteria_met` evaluation |
| `abandon_session` | History entry; journey remains `ACTIVE` unless student also pauses/defers |
| Reflection captured | Soft evidence; recommendation inputs refresh |

---

## 4. Reflection Posture

| State | Meaning |
|-------|---------|
| `NOT_REQUIRED` | Session not yet completed |
| `PENDING` | Session completed; reflection owed |
| `CAPTURED` | Reflection recorded |
| `DEFERRED_CAPTURE` | Explicit short deferral (policy TBD in implementation) |

### Transitions

```
NOT_REQUIRED → PENDING   (on session COMPLETED)
PENDING → CAPTURED       (on capture_reflection)
PENDING → DEFERRED_CAPTURE (explicit defer; must return to PENDING/CAPTURED)
DEFERRED_CAPTURE → CAPTURED
```

### Invalid

- Journey `confirm_topic_complete` while latest session reflection is `PENDING` (recommended hard guard)
- System-authored reflection text presented as student reflection

---

## 5. JourneyRecommendation Lifecycle

```
PROPOSED
    ↓ accept
ACCEPTED
    ↓ start_session
REALISED
```

Alternate terminals from `PROPOSED`: `DISMISSED`, `EXPIRED`, `SUPERSEDED`.

### Invalid

| Transition | Why |
|------------|-----|
| `PROPOSED` → Journey `COMPLETED` | Advice cannot complete topics |
| `ACCEPTED` → Session `COMPLETED` without start/finish | Skips work |
| `DISMISSED` treated as negative mastery evidence alone | Over-claim; may be behavioural evidence only at low weight |

---

## 6. Compatibility with Version 1 Session UX

LXP-002 already defines Start / Pause / Resume / Finish for Study Sessions. Version 2 SessionState is the domain generalisation of that UX:

| LXP-002 concept | SessionState |
|-----------------|--------------|
| Not started | `NOT_STARTED` |
| In session | `ACTIVE` |
| Paused timer | `PAUSED` |
| Finished | `COMPLETED` |

Version 2 adds mandatory reflection posture and journey attribution. Runtime mapping is deferred to V2-005.

---

## 7. Completion Criteria Gate

`completion_criteria_met` is true only when [`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md) criteria for the topic journey are satisfied. The state machine does not embed numeric mastery thresholds.

Required conceptual inputs:

- Minimum learning sessions or equivalent effort policy (topic-configurable)
- Required reflection closures
- Lawful coverage declaration readiness
- Evidence density floor for journeys that include practice objectives (without equating density to mastery)

Exact thresholds are implementation concerns for V2-003 / V2-005 / V2-008 — not V2-001.

---

## 8. Closing

If an implementation allows `session_completed` to set JourneyState `COMPLETED`, it violates this architecture regardless of UI convenience.
