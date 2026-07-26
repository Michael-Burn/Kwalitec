# MS-002 — Journey Sequence Diagrams

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Companion:** `HISTORY_SEQUENCE_DIAGRAM.md`

---

## Conventions

Layer order in every diagram:

**UI → Experience Layer → Bridge → Educational Services → Database**

| Participant | Meaning |
|---|---|
| UI | Journey templates / Home journey card |
| Exp | `JourneyService` / `StudentExperienceService` |
| Port | `LearningJourneyPort` |
| Bridge | `JourneyAdapter` (`JourneyBridge`) |
| Services | Runtime A: StudyPlan, Mission, TopicProgress/Readiness, Lifecycle, Recommendation |
| DB | SQLAlchemy models / Curriculum JSON |

Bridges are **read-only**. No educational writes appear in these flows.

---

## 1. Load Journey

Student opens Journey page (or Home loads journey card snippet).

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as UI<br/>(journey / home card)
    participant Exp as Experience Layer<br/>(JourneyService)
    participant Port as LearningJourneyPort
    participant Bridge as JourneyBridge
    participant Plan as StudyPlanService
    participant Mission as MissionService
    participant Ready as ReadinessService
    participant Life as LearningLifecycleService
    participant Progress as TopicProgress / Adaptive reads
    participant Curr as CurriculumService
    participant DB as Database

    Student->>UI: GET /student/journey
    UI->>Exp: journey(student_id)
    Exp->>Port: get_journey_progress / get_topic_list
    Port->>Bridge: project_journey(student_id)

    Bridge->>Plan: get active StudyPlan
    Plan->>DB: SELECT study_plans
    alt No active plan
        Bridge-->>Port: empty authentic journey<br/>(has_journey=false)
        Port-->>Exp: opaque empty progress
        Exp-->>UI: JourneyPage empty state
    else Active plan
        Bridge->>Life: resolve lifecycle stage
        Life->>DB: plan + leaf completion inputs
        Bridge->>Ready: coverage / readiness aggregates
        Ready->>DB: TopicProgress / plan aggregates
        Bridge->>Progress: topic status map (owned)
        Progress->>DB: TopicProgress rows
        Bridge->>Curr: ordered topic traversal (V1/V2)
        Curr-->>Bridge: official topic sequence
        Bridge->>Mission: get_today_mission / active In Progress
        Mission->>DB: SELECT missions
        Note over Bridge: Map only — no mastery math,<br/>no generate_today_mission
        Bridge-->>Port: Journey snapshot + timeline + trace
        Port-->>Exp: opaque progress + topics
        Exp-->>UI: JourneyPageViewModel
        UI-->>Student: Authoritative journey narrative
    end
```

### Notes

- When `ENABLE_JOURNEY_BRIDGE` is off, Port uses prior Experience projection path (demo/seed possible) — not shown.  
- Failure (`UNAVAILABLE`, `FORBIDDEN`): Bridge returns empty authentic + telemetry; never `seeded_demo_journey`.  
- Home card uses the same Bridge method with a snippet field subset (no second SoT).

---

## 2. View Recommendation Change

Student inspects a Journey (or History) timeline item that claims a recommendation delta — “what changed in my next focus because of this event?”

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as UI<br/>(journey / history detail)
    participant Exp as Experience Layer
    participant Bridge as JourneyBridge<br/>(or HistoryBridge)
    participant Rec as RecommendationService
    participant Mission as MissionService
    participant Explain as EducationalExplainabilityService
    participant DB as Database

    Student->>UI: Inspect timeline item<br/>(View recommendation change)
    UI->>Exp: recommendation_delta(student_id, event_id)
    Exp->>Bridge: get_recommendation_change(student_id, event_ref)

    Bridge->>Mission: load linked Mission (if any)
    Mission->>DB: SELECT mission by id + ownership
    alt Ownership failure
        Bridge-->>Exp: FORBIDDEN / NOT_FOUND
        Exp-->>UI: Safe error / hide detail
    else Owned event
        Bridge->>Rec: reconstruct recommendation<br/>before/after event context
        Rec->>DB: Learning state / progress reads
        opt Narrative enrichment
            Bridge->>Explain: student-safe explanation
        end
        alt Reconstructable
            Bridge-->>Exp: prior_label, next_label,<br/>reason_codes, evidence_refs,<br/>mission_aligned flags
            Exp-->>UI: Recommendation change panel
            UI-->>Student: Why next focus changed
        else Not reconstructable
            Bridge-->>Exp: recommendation_delta=null<br/>reason=unavailable
            Exp-->>UI: Honest “unavailable” copy
            UI-->>Student: No fabricated delta
        end
    end
```

### Notes

- Bridge **never recalculates** a new authoritative recommendation for “today” as a side effect of inspect (that remains Recommendation Read Bridge / RecommendationService on Home).  
- Reconstructability policy is ADR-MS002-003 territory: prefer explicit `unavailable` over invention.  
- Trace fields on the timeline item should already carry `prior_recommendation_id` / `next_recommendation_id` when known at projection time.

---

## 3. Cross-reference

| Flow | Location |
|---|---|
| Load History | `HISTORY_SEQUENCE_DIAGRAM.md` §1 |
| Inspect Evidence | `HISTORY_SEQUENCE_DIAGRAM.md` §2 |
| Load Journey | This file §1 |
| View Recommendation Change | This file §2 |

---

## Stop condition

Diagrams are design artefacts only. Do not implement adapters from this document alone.
