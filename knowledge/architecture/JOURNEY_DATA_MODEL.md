# MS-002 — Journey / History Data Model

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Constraint:** No schema changes — logical projection model over existing SQL

---

## 1. Purpose

Define the **logical** data model for Educational Journey and History projections. Physical persistence remains Runtime A tables already in production. Bridges map SQL → opaque Experience DTOs.

---

## 2. Physical sources (unchanged)

| Entity | Role in narrative |
|---|---|
| `User` | Student identity / ownership |
| `StudyPlan` | Active plan window, exam labels, revision fields |
| `Mission` (+ `MissionTask`) | Session of record; status Pending / In Progress / Completed |
| `StudyAttempt` | Evidence-bearing practice records |
| `TopicProgress` | Mastery / coverage state per topic |
| Curriculum JSON via `CurriculumService` | Official topic order (V1 flat / V2 hierarchical) |
| Derived: Readiness aggregates | Coverage / readiness scores |
| Derived: Lifecycle stage | Learning vs Revision |

**Not authoritative for MS-002:** `ExperienceProjectionStore` journey/twin docs, `seeded_demo_*`, V2 `LearningJourney` aggregate (unwired relative to SQL Evidence).

---

## 3. Logical projection entities

### 3.1 `EducationalTimelineEvent`

Canonical timeline atom (Journey + History share).

| Field | Type | Source |
|---|---|---|
| `event_id` | string | Mission.id / Attempt.id / deterministic hash |
| `event_type` | enum | See architecture §5.1 |
| `student_id` | string | Ownership |
| `occurred_at` | datetime / date | `mission_date`, `study_date`, completion timestamp |
| `mission_id` | string? | When session-linked |
| `topic_code` / `topic_title` | string? | Mission / attempt / progress |
| `lifecycle_stage` | `learning` \| `revision` \| null | LifecycleService |
| `summary` | string | Student-safe what-happened |
| `authority` | string | Owning service tag |
| `trace` | TraceRef | Traceability block |

### 3.2 `JourneySnapshot` (projection)

Maps to existing Experience journey document shape.

| Field | Type | Source rule |
|---|---|---|
| `has_journey` | bool | Active StudyPlan exists |
| `progress.overall_progress_ratio` | float 0..1 | **ReadinessService / plan coverage** — adapter does not invent formula |
| `progress.estimated_completion_label` | string | Runtime A label or empty |
| `progress.examination_label` | string | StudyPlan / Twin exam label from plan |
| `progress.current_topic_id/title` | string | Active / today’s Mission topic, else next incomplete via Curriculum+Progress |
| `progress.lifecycle_stage` | string | LearningLifecycleService |
| `topics[]` | TopicCard | Curriculum order × TopicProgress status |
| `active_missions[]` | MissionCard | MissionService |
| `completed_sessions_summary` | object | Aggregated completed Missions |
| `timeline[]` | EducationalTimelineEvent | Recent events capped |
| `recommendation_focus` | object | Recommendation Read Bridge / RecommendationService (aligned) |
| `authority` | `"journey_bridge"` | Constant when bridged |

### 3.3 `TopicCard`

| Field | Values | Mapping |
|---|---|---|
| `status` | `completed` \| `current` \| `upcoming` | TopicProgress mastery/complete → completed; matches current mission topic → current; else upcoming |
| `status_label` | string | Presentation labels only |
| `prerequisite_note` | string? | Optional Curriculum / Planning helper text — not new educational law |

### 3.4 `HistorySnapshot` (projection)

Maps to existing `HistoryProjection` / `HistorySnapshot` DTOs.

| Field | Source |
|---|---|
| `completed_sessions[]` | Completed Missions (+ minutes from attempt/mission fields) |
| `total_study_minutes` | Sum of session minutes (Runtime A) |
| `readiness_progression[]` | Derived samples (ADR-MS002-002) |
| `mastered_topics[]` | TopicProgress mastered / complete labels |
| `revision_history[]` | Revision-stage mission / activity labels |
| `recent_achievements[]` | ProgressMilestone projections |
| `page` | Pagination meta |

### 3.5 `EvidenceSummary` (inspect)

| Field | Source |
|---|---|
| `attempt_ids` | StudyAttempt |
| `evidence_accepted` | Evidence Authority posture (read) |
| `mastery_updated` | Whether gated write occurred historically (if knowable) |
| `outcome_labels` | Student-safe summaries |
| Ban | `events`, `raw_events`, `event_log` arrays |

### 3.6 `RecommendationDelta` (inspect)

| Field | Source |
|---|---|
| `prior` / `next` labels | Reconstructable RecommendationService outputs / mission-aligned titles |
| `decision_ids` | If available from telemetry / decision surfaces |
| `unavailable_reason` | When reconstruction impossible |

---

## 4. Identity mapping

| Experience concept | Canonical identity |
|---|---|
| Journey “current topic” | Official topic code from Curriculum + Mission / next incomplete |
| History `session_id` | SQL `Mission.id` (same rule as MS-001 ExperienceSessionId ↔ MissionId) |
| Evidence inspect key | `mission_id` and/or `attempt_id` |
| Timeline `event_id` | Prefer SQL PK; document hash algorithm if composite |

---

## 5. Status mapping (Mission → UI)

| SQL `Mission.status` | Journey / History presentation |
|---|---|
| Pending | Active upcoming / not in completed_sessions |
| In Progress | `active_missions` |
| Completed | `completed_sessions` + timeline `SessionCompleted` |

---

## 6. Readiness progression (derived — no new table)

Without schema changes, readiness series is a **derived projection**:

| Strategy | Description | Preference |
|---|---|---|
| A. Point-in-time recompute | Sample dates (week boundaries / mission completion dates); call ReadinessService as-of if supported | Prefer if API exists |
| B. Completion-linked samples | On each completed Mission date, project readiness from TopicProgress state **as currently stored** (acknowledges limited historical fidelity) | Acceptable Interim |
| C. Empty series | Honest empty progression when not reconstructable | Required fallback |

**ADR-MS002-002** must lock A/B/C before History readiness series ships. Fabricating smooth demo curves is forbidden.

---

## 7. Continuity across plan changes

`EducationalContinuityService` preserves rightful TopicProgress / estimates across plan edits. Journey/History must:

- Continue to show owned attempts and completed missions for the learner  
- Not treat plan replacement as wiping history  
- Optionally emit `ContinuityPreserved` milestone when continuity copy ran (if detectable)

---

## 8. Entity relationship (logical)

```text
Student (User)
  └── StudyPlan (active)
        ├── Mission* (sessions)
        │     └── StudyAttempt* (evidence)
        ├── TopicProgress* (mastery)
        ├── Lifecycle stage (derived)
        └── Readiness aggregates (derived)

CurriculumService ──orders──> TopicCards on Journey
RecommendationService ──labels──> recommendation_focus / deltas
```

---

## 9. Non-goals

- New Alembic tables for timeline / recommendation audit (deferred; would be a later milestone if product requires durable deltas)  
- Changing Experience DTO field names required by templates (additive enrichment only)  
- Promoting V2 domain `LearningJourney` entity to SoT  

---

## Stop condition

Logical model only. No migrations. No ORM changes under this directive.
