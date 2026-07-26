# MS-002 — Journey / History Interface Specification

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design (interfaces only — do not implement)  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Extends:** MS-001 `BRIDGE_INTERFACE_SPECIFICATION.md` §§5–6 (supersedes stub detail for Journey/History)

---

## 0. Conventions

### Layers

| Layer | Responsibility |
|---|---|
| Experience Port / Facade | `LearningJourneyPort`, `HistoryService`, Twin insights consumer |
| Bridge Adapter | Translates to Runtime A; owns empty authentic fallbacks + telemetry |
| Educational Service | Authoritative domain logic (read APIs only for MS-002) |
| Database | Existing SQLAlchemy models / Curriculum JSON |

### Shared types (logical)

| Type | Meaning |
|---|---|
| `StudentId` | Authenticated user id |
| `MissionId` | SQL `Mission.id` (stringified) |
| `AttemptId` | SQL `StudyAttempt.id` (stringified) |
| `EventId` | Stable timeline id (prefer SQL PK; else deterministic hash) |
| `OpaqueDict` | Projection document safe for Experience (no ORM) |
| `BridgeResult[T]` | `{ ok, value?, error_code?, message?, fallback_used }` |
| `TraceRef` | Traceability block (see §3) |

### Shared failure codes

Reuse MS-001 codes:

| Code | Meaning |
|---|---|
| `UNAVAILABLE` | Downstream service or DB unreachable |
| `NO_ACTIVE_PLAN` | No active StudyPlan (Journey empty) |
| `NOT_FOUND` | Mission / attempt / event missing |
| `FORBIDDEN` | Ownership failure |
| `INVALID_STATE` | Malformed filter / illegal inspect ref |
| `BEHAVIOUR_MISMATCH` | Parity / golden check (tests only) |

### Shared read-only rule

Journey and History bridges **must not**:

- Call Planning ensure/generate  
- Start / resume / complete sessions  
- Write TopicProgress or StudyAttempt  
- Recalculate recommendations as authority  
- Emit demo seeds when bridge flags are on  

---

## 1. `JourneyBridge`

**Purpose:** Journey page / Home journey card — syllabus position, milestones, timeline narrative.  
**Backs:** `LearningJourneyPort.get_journey_progress`, `get_topic_list` (+ Home snippet).  
**Ownership:** Infrastructure bridge adapter.  
**Educational owners (read):** `StudyPlanService`, `MissionService`, `ReadinessService`, `LearningLifecycleService`, TopicProgress reads / AdaptiveLearning read APIs, `CurriculumService`, optional `RecommendationService` for current focus alignment.

### 1.1 `project_journey`

**Inputs**

| Name | Type | Required | Notes |
|---|---|---|---|
| `student_id` | StudentId | Yes | Current user |
| `as_of_date` | date | No | Defaults to today (server) |
| `include_timeline` | bool | No | Default true for Journey page; false for tiny Home card |
| `timeline_limit` | int | No | Cap timeline events (e.g. 20) |

**Outputs** (`OpaqueDict` compatible with existing journey document + enrichments)

```
{
  student_id,
  has_journey: bool,
  progress: {
    overall_progress_ratio,      # from Readiness / plan coverage — not invented
    estimated_completion_label,  # from Runtime A labels if available else ""
    examination_label,
    current_topic_id,
    current_topic_title,
    lifecycle_stage             # learning | revision
  },
  topics: [                      # CurriculumService order
    {
      topic_id, title,
      status,                    # completed | current | upcoming
      status_label,
      prerequisite_note?,
      trace?
    }
  ],
  active_missions: [ ... ],      # today / in_progress projections
  completed_sessions_summary: {
    count, recent: [ { mission_id, topic_title, completed_at, study_minutes } ]
  },
  timeline: [ EducationalTimelineItem ],  # see JOURNEY_DATA_MODEL.md
  recommendation_focus: {        # aligned with Recommendation Read Bridge when available
    topic_title, reason_codes, mission_aligned, authority
  },
  authority: "journey_bridge",
  next_action_authority: false
}
```

**Failure modes**

| Condition | Code | Behaviour |
|---|---|---|
| No active plan | `NO_ACTIVE_PLAN` | Empty authentic (`has_journey=false`) |
| User mismatch | `FORBIDDEN` | Never return another user’s journey |
| Service/DB down | `UNAVAILABLE` | Empty authentic + `bridge.fallback` |
| Curriculum unloadable | `UNAVAILABLE` | Empty topics; do not invent order |

**Fallback behaviour**

1. Prefer partial authentic projection (plan + topics) if readiness unavailable.  
2. Never `seeded_demo_journey`.  
3. Emit `bridge.fallback`.

**Telemetry**

- `JOURNEY_BRIDGE_REQUESTED` / `SUCCESS` / `FAILURE` / `LATENCY`  
- `bridge.authority` = underlying services  

---

### 1.2 `get_recommendation_change`

**Purpose:** View Recommendation Change flow.  
**Inputs:** `student_id`, `event_id` (or `mission_id` + `occurred_at`).  
**Outputs:**

```
{
  event_id,
  what: "...",
  why: { reason_codes, summary },
  evidence_refs: [ AttemptId | MissionId ],
  recommendation_delta: {
    prior: { label, decision_id? } | null,
    next: { label, decision_id? } | null,
    mission_aligned_prior: bool | null,
    mission_aligned_next: bool | null
  } | null,
  unavailable_reason: null | "unavailable" | "not_applicable",
  authority: "journey_bridge"
}
```

**Failure modes:** `NOT_FOUND`, `FORBIDDEN`, `UNAVAILABLE`.  
**Rule:** Prefer `recommendation_delta: null` + honest reason over fabrication.

---

## 2. `HistoryBridge`

**Purpose:** History page / Home history card — accomplished learning narrative.  
**Backs:** `HistoryService` (and Twin insights path used by History).  
**Ownership:** Infrastructure.  
**Educational owners (read):** Mission history queries / `MissionService`, `StudyAttempt` reads, `ReadinessService`, AdaptiveLearning mastered-topic reads, `LearningLifecycleService` (revision labels), Evidence Authority **read/summarise only**.

### 2.1 `project_history`

**Inputs**

| Name | Type | Required | Notes |
|---|---|---|---|
| `student_id` | StudentId | Yes | |
| `limit` | int | No | Default 20; hard max 100 |
| `offset` | int | No | Default 0 (or use cursor) |
| `cursor` | string | No | Alternative to offset (`before_date` encoded) |
| `from_date` | date | No | Inclusive |
| `to_date` | date | No | Inclusive |
| `event_types` | list[str] | No | Subset of timeline types |
| `lifecycle_stage` | str | No | `learning` \| `revision` |
| `topic_code` | str | No | Official topic code filter |

**Outputs** (maps to existing `HistoryProjection` / `HistorySnapshot`, plus pagination meta)

```
{
  student_id,
  completed_sessions: [
    {
      session_id,           # ExperienceSessionId == MissionId when bridged
      mission_id,
      topic_title,
      completed_at,
      study_minutes,
      lifecycle_stage?,
      trace?
    }
  ],
  total_study_minutes,
  readiness_progression: [
    { recorded_at, exam_readiness, label }
  ],
  mastered_topics: [ ... ],
  revision_history: [ ... ],   # labels from revision-stage activity
  recent_achievements: [ ... ], # progress milestones projected as cards
  session_count,
  mastered_count,
  page: { limit, offset, has_more, next_offset? },
  authority: "history_bridge"
}
```

**Ordering:** Reverse chronological by completion / study date; stable secondary key = mission/attempt id.

**Failure / fallback**

- Empty history on error/missing data — **not** fabricated sessions.  
- Strip `events` / `raw_events` / `event_log` if present in any upstream blob.  
- Emit `bridge.fallback` when degrading.

**Telemetry:** `HISTORY_BRIDGE_*` + `bridge.authority`.

---

### 2.2 `get_evidence_summary`

**Purpose:** Inspect Evidence flow.  
**Inputs:** `student_id`, `mission_id` and/or `attempt_id`.  
**Outputs:**

```
{
  student_id,
  mission_id?,
  attempt_ids: [...],
  summary: {
    topic_title,
    study_date,
    outcome_labels,          # student-safe; no raw dumps
    evidence_accepted: bool | null,
    mastery_updated: bool | null,
    questions_attempted?,
    duration_minutes?
  },
  why: { reason_codes, summary },
  recommendation_delta_ref?,  # event_id for optional follow-on
  authority: "history_bridge"
}
```

**Failure modes:** `NOT_FOUND`, `FORBIDDEN`, `UNAVAILABLE`, `INVALID_STATE`.  
**Rule:** Read-only; never re-commit evidence.

---

## 3. `TraceRef` (shared)

Attached to timeline items and optionally to History session cards:

```
{
  what: string,
  why: { reason_codes: [...], summary: string },
  evidence_refs: [ { kind: "attempt"|"mission"|"topic_progress", id: string } ],
  recommendation: {
    changed: bool | null,
    prior_label?: string,
    next_label?: string,
    decision_ids?: [...],
    unavailable_reason?: string
  }
}
```

Normative matrix: `JOURNEY_TRACEABILITY_MATRIX.md`.

---

## 4. Port → Bridge mapping

| Experience surface | Method | Bridge |
|---|---|---|
| `LearningJourneyPort.get_journey_progress` | progress blob | `JourneyBridge.project_journey` |
| `LearningJourneyPort.get_topic_list` | topics tuple | `JourneyBridge.project_journey` (topics slice) |
| Home journey card | snippet | `JourneyBridge.project_journey` (`include_timeline=false`) |
| `HistoryService.history` | HistorySnapshot | `HistoryBridge.project_history` |
| Home history card | limited insights | `HistoryBridge.project_history` (small `limit`) |
| Evidence inspect UI | detail | `HistoryBridge.get_evidence_summary` |
| Recommendation change UI | detail | `JourneyBridge.get_recommendation_change` |

Composition: existing `ExperienceJourneyAdapter` becomes a thin wrapper around `JourneyBridge` when flag on (same pattern as Mission Read). History may inject Bridge into Twin insights assembly or replace insights source behind `HistoryService` — implementation choice deferred; **contract above is binding**.

---

## 5. Feature flags

| Flag | Adapter |
|---|---|
| `KWALITEC_JOURNEY_BRIDGE` / `ENABLE_JOURNEY_BRIDGE` | JourneyBridge |
| `KWALITEC_HISTORY_BRIDGE` / `ENABLE_HISTORY_BRIDGE` | HistoryBridge |
| Umbrella `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE` | May enable both |

Default **off**. Independently releasable and reversible.

---

## 6. Compatibility with MS-001 stubs

This document **elaborates** `BRIDGE_INTERFACE_SPECIFICATION.md` §§5–6. Where conflict exists, **MS-002 this file wins** for Journey/History detail; MS-001 remains authoritative for Mission / Recommendation / Completion bridges.

---

## Stop condition

Interface design only. Do not implement adapters under this directive.
