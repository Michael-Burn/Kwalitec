# MS-001 — Bridge Interface Specification

**Milestone:** MS-001 — Foundational Trust  
**Directive:** Engineering Directive 002  
**Status:** Architecture Design (interfaces only — do not implement)  
**Parent:** `EDUCATIONAL_RUNTIME_BRIDGE.md`

---

## 0. Conventions

### Layers

| Layer | Responsibility |
|---|---|
| Experience Port | Stable Protocol consumed by facades (`MissionPort`, …) |
| Bridge Adapter | Implements port; translates to Runtime A; owns fallbacks + telemetry |
| Educational Service | Authoritative domain logic (`PlanningService`, …) |
| Database | SQLAlchemy models / Curriculum JSON |

### Common types (logical — not implemented)

| Type | Meaning |
|---|---|
| `StudentId` | Authenticated user id string (matches `User.id` / learner id used by Experience) |
| `MissionId` | SQL `Mission.id` (stringified) — **canonical mission identity** |
| `ExperienceSessionId` | Stable UI session id; must map 1:1 to `MissionId` when bridged |
| `OpaqueDict` | Projection document safe for Experience (no ORM objects) |
| `BridgeResult[T]` | `{ ok, value?, error_code?, message?, fallback_used }` |

### Shared failure codes

| Code | Meaning |
|---|---|
| `UNAVAILABLE` | Downstream service or DB unreachable |
| `NO_ACTIVE_PLAN` | No active StudyPlan |
| `OUTSIDE_PLAN_WINDOW` | Date outside plan window |
| `NOT_FOUND` | Mission/session missing |
| `FORBIDDEN` | Ownership failure |
| `INVALID_STATE` | Illegal status transition |
| `EVIDENCE_REJECTED` | Evidence Authority refused mastery write |
| `BEHAVIOUR_MISMATCH` | Golden / parity check failed (test/diagnostics only) |

### Shared telemetry (all bridges)

Emit via existing `PresentationTelemetryService` / `AdapterDiagnostics` / EventRegistry patterns:

| Event | When |
|---|---|
| `bridge.call` | Every public bridge method (adapter_id, method, latency_ms, ok) |
| `bridge.fallback` | Fallback path used (code, adapter_id) |
| `bridge.authority` | Educational authority recorded (`planning`, `recommendation`, `evidence`, …) |

Ownership of telemetry payload shape: Bridge adapters (Infrastructure). Ownership of sink: existing telemetry services.

---

## 1. `PlanningBridge`

**Purpose:** Ensure and project today’s mission without Experience inventing topics.  
**Backs:** `MissionPort.get_todays_session` (read) and ensure-today used by Start.  
**Ownership:** Infrastructure bridge adapter. **Educational owner:** `PlanningService`.

### Inputs

| Name | Type | Required | Notes |
|---|---|---|---|
| `student_id` | StudentId | Yes | Current user |
| `as_of_date` | date | No | Defaults to today (server) |
| `ensure` | bool | No | If true, call `generate_today_mission` (idempotent) |

### Outputs

`OpaqueDict` today’s session projection, for example:

```
{
  student_id,
  mission_id,              # SQL Mission.id
  session_id,              # ExperienceSessionId (== mission_id or stable map)
  topic_code,
  topic_title,
  estimated_minutes,
  status,                  # pending | in_progress | completed (mapped)
  tasks: [...],
  lifecycle_stage,         # learning | revision
  authority: "planning_service",
  next_action_authority: false
}
```

### Failure modes

| Condition | Code | Behaviour |
|---|---|---|
| No active plan | `NO_ACTIVE_PLAN` | Return `None` or empty projection with CTA disabled |
| Outside window | `OUTSIDE_PLAN_WINDOW` | Same as no mission |
| Planning exception | `UNAVAILABLE` | See fallback |
| User mismatch | `FORBIDDEN` | Never return another user’s mission |

### Fallback behaviour

1. Prefer last successful SQL `MissionService.get_today_mission` without generate.  
2. If none: return `None` — **do not** seed demo mission.  
3. Emit `bridge.fallback`.

### Telemetry

- `bridge.call` (`planning.get_todays_session` / `planning.ensure_today`)  
- `bridge.authority` = `planning_service`  
- On ensure create: `mission_ensured` (new vs existing)

---

## 2. `MissionLifecycleBridge`

**Purpose:** Start, resume status, and complete sessions against SQL Mission.  
**Backs:** `MissionPort.start_session`, `get_session_status`, `complete_session` (and SessionExperience completion hooks).  
**Ownership:** Infrastructure. **Educational owners:** `StudySessionService`, `MissionService`.

### 2.1 `start_session`

**Inputs**

| Name | Type | Required |
|---|---|---|
| `student_id` | StudentId | Yes |
| `mission_id` | MissionId | No — default today’s mission via PlanningBridge |
| `session_id` | ExperienceSessionId | No — derived from mission |

**Outputs**

```
{
  student_id,
  mission_id,
  session_id / experience_session_id,
  status: "in_progress",
  topic_title,
  started_at,
  authority: "study_session_service"
}
```

**Failure modes**

| Condition | Code |
|---|---|
| Mission not owned | `FORBIDDEN` |
| Already completed | `INVALID_STATE` |
| No mission to start | `NOT_FOUND` / `NO_ACTIVE_PLAN` |
| Service error | `UNAVAILABLE` |

**Fallback**

- Do **not** create opaque-only sessions when Bridge flag is on.  
- On `UNAVAILABLE`: fail closed to Home with flash; optional read-only projection if previously in progress (no new start).

**Telemetry:** `learning_session_started` (existing event type) + `bridge.call`.

### 2.2 `get_session_status` / resume support

**Inputs:** `student_id`, `session_id` (mapped to MissionId).  
**Outputs:** status + resume hints (`active_surface` remains SessionWorkspace concern).  
**Failure:** `NOT_FOUND`, `FORBIDDEN`.  
**Fallback:** If workspace missing but Mission In Progress → open Overview (not fabricated activity).

### 2.3 `complete_session`

**Inputs**

| Name | Type | Required |
|---|---|---|
| `student_id` | StudentId | Yes |
| `session_id` / `mission_id` | ids | Yes |
| `outcome` | OpaqueDict | Conditional — practice outcome fields when Evidence parity phase on |

**Outputs:** completion projection + optional feedback summary.  
**Failure:** `INVALID_STATE`, `EVIDENCE_REJECTED`, `FORBIDDEN`.  
**Fallback:** Mark UX complete only if educational complete failed → **forbidden under Bridge Complete**; during transitional phase may complete UX with `bridge.fallback` and `educational_complete=false` telemetry (must be gated and temporary).

**Telemetry:** `learning_session_completed`, `mission_updated`, evidence accept/reject counters.

---

## 3. `RecommendationBridge`

**Purpose:** Single recommendation policy for Experience Home / Revision.  
**Backs:** `AdaptiveDecisionPort.get_todays_recommendation` / `decide`.  
**Ownership:** Infrastructure. **Educational owners:** Planning (topic) + `RecommendationService` (narrative).

### Inputs

| Name | Type | Required |
|---|---|---|
| `student_id` | StudentId | Yes |
| `mission_projection` | OpaqueDict | No — injected by facade/EducationalStateService |

### Outputs

```
{
  decision_id,
  recommendation_label,     # aligned to mission topic when present
  topic_code,
  topic_title,
  explanation: { summary, authority, … },
  alternatives: [...],      # optional from RecommendationService
  authority: "recommendation_bridge",
  mission_aligned: true|false
}
```

### Failure modes

| Condition | Code | Behaviour |
|---|---|---|
| No mission | — | Narrative-only from RecommendationService or “set up plan”; `mission_aligned=false` |
| RecommendationService empty | — | Label from mission only |
| Both empty | — | Empty recommendation; CTA disabled |
| Service error | `UNAVAILABLE` | Fallback to mission-only label if mission exists |

### Fallback behaviour

1. Mission topic title as label.  
2. Never `seeded_demo_adaptive`.  
3. Emit `bridge.fallback`.

### Telemetry

- `bridge.authority` recording `mission_aligned`  
- Existing adaptive recommendation read metrics

---

## 4. `LearningStateBridge` (Twin / readiness / lifecycle)

**Purpose:** Project learning state for TwinPort and EducationalStateService.  
**Ownership:** Infrastructure. **Educational owners:** `ReadinessService`, `AdaptiveLearningService` (read), `LearningLifecycleService`.

### Inputs

| Name | Type | Required |
|---|---|---|
| `student_id` | StudentId | Yes |

### Outputs

```
{
  student_id,
  readiness_label,
  readiness_score,          # from ReadinessService aggregates
  lifecycle_stage,
  weak_topics: [...],
  coverage_summary: {...},
  authority: "learning_state_bridge"
}
```

### Failure modes

| Condition | Code | Behaviour |
|---|---|---|
| No plan / empty progress | — | Neutral “not started” labels — not demo fabricated readiness ~0.58 |
| Service error | `UNAVAILABLE` | Cached last projection if Bridge cache allowed; else minimal empty state |

### Fallback

Empty authentic state preferred over demo. Emit `bridge.fallback`.

### Telemetry

`bridge.call` (`learning_state.project`); readiness source tags.

---

## 5. `JourneyBridge`

**Purpose:** Journey page / Home journey card.  
**Ownership:** Infrastructure. **Educational owners:** `StudyPlanService`, TopicProgress/Readiness, Lifecycle.

### Inputs

`student_id`

### Outputs

Journey opaque snapshot: milestones, progress fraction, stage, next focus (from Planning mission if any).  
`authority: "journey_bridge"`

### Failure / fallback

No plan → empty journey (`has_journey=false`). No demo journey seed.

### Telemetry

`bridge.call` (`journey.project`)

---

## 6. `HistoryBridge`

**Purpose:** History page / Home history card.  
**Ownership:** Infrastructure. **Educational owners:** Mission history, StudyAttempt, Readiness progression.

### Inputs

`student_id`, optional `limit`

### Outputs

Activity entries, readiness progression series, revision history labels.  
`authority: "history_bridge"`

### Failure / fallback

Empty history on error/missing data — not fabricated sessions.

### Telemetry

`bridge.call` (`history.project`)

---

## 7. `EvidenceParityBridge`

**Purpose:** Map Session Experience completion / practice outcomes onto Evidence Authority path.  
**Ownership:** Infrastructure. **Educational owners:** `StudySessionService`, `EducationalEvidenceAuthority`, `AdaptiveLearningService`.

### Inputs

| Name | Type | Required |
|---|---|---|
| `student_id` | StudentId | Yes |
| `mission_id` | MissionId | Yes |
| `outcome_payload` | OpaqueDict | Yes when recording practice |

Logical fields mirror legacy finish/outcome forms (correctness, confidence, duration, task completion) without UI redesign — payload assembled by Session layer from available activity data.

### Outputs

```
{
  educational_complete: bool,
  evidence_accepted: bool,
  mastery_updated: bool,
  feedback_summary: {...},
  authority: "evidence_parity_bridge"
}
```

### Failure modes

| Condition | Code |
|---|---|
| Evidence rejected | `EVIDENCE_REJECTED` |
| Incomplete outcome when required | `INVALID_STATE` |
| Ownership | `FORBIDDEN` |

### Fallback behaviour

- **Bridge Complete:** no silent skip of evidence when outcome is required.  
- **Transitional phase:** allow UX complete with `educational_complete=false` + loud telemetry (feature-flagged).

### Telemetry

Evidence accept/reject; mastery delta counters; parity mismatch alarms.

---

## 8. Port → Bridge mapping

| Experience Port method | Bridge |
|---|---|
| `MissionPort.get_todays_session` | `PlanningBridge` |
| `MissionPort.start_session` | `MissionLifecycleBridge.start_session` |
| `MissionPort.get_session_status` | `MissionLifecycleBridge` |
| `MissionPort.complete_session` (if present) | `MissionLifecycleBridge` + `EvidenceParityBridge` |
| `AdaptiveDecisionPort.get_todays_recommendation` | `RecommendationBridge` |
| TwinPort learner summary / readiness | `LearningStateBridge` |
| JourneyPort projections | `JourneyBridge` |
| History/Orchestrator activity reads (as used by History) | `HistoryBridge` |

Existing `Experience*Adapter` classes either **become** thin wrappers around bridges or are **replaced** by bridge-backed adapters behind the same ports — implementation choice deferred; contract above is binding.

---

## 9. Composition / feature flags (design)

Logical flags (names illustrative; concrete env names chosen at implementation):

| Flag | Effect |
|---|---|
| `EDUCATIONAL_RUNTIME_BRIDGE` (or compose under existing V2 inject flags) | Enable bridge adapters |
| `SEED_DEMO_LEARNERS` | Must be false when Bridge on in Alpha/prod |
| Existing `ENABLE_DURABLE_STORE` | Persist projections/workspace — not educational SoT |

Composition rule: when Bridge on → adapters call bridges; `seeded_demo_*` path unreachable for authenticated learners.

---

## 10. Ownership summary

| Concern | Owner |
|---|---|
| Port Protocols | Application layer (`app/application/.../ports`) |
| Bridge adapters | Infrastructure (`app/infrastructure/adapters/...`) |
| Educational algorithms | `app/services/*` (Runtime A) |
| Curriculum order | `CurriculumService` |
| Mastery integrity | `EducationalEvidenceAuthority` |
| UX resume step | `SessionWorkspace` / SessionExperience |
| Chrome / sole runtime | `consolidation` + `v2_flags` |

---

## Stop condition

Interface specification complete. **Do not implement** these interfaces under Directive 002.
