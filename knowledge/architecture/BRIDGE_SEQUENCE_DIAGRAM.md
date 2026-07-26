# MS-001 — Bridge Sequence Diagrams

**Milestone:** MS-001 — Foundational Trust  
**Directive:** Engineering Directive 002  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_RUNTIME_BRIDGE.md`  
**Interfaces:** `BRIDGE_INTERFACE_SPECIFICATION.md`

All flows show: **UI → Experience Layer → Bridge → Educational Services → Database**.

---

## 1. Start Study

Primary path: Student Home CTA → Session Overview.

```mermaid
sequenceDiagram
    actor Student
    participant UI as UI (Home CTA)
    participant Exp as Experience Layer<br/>(StudentExperienceService)
    participant Bridge as Bridge<br/>(Planning + MissionLifecycle)
    participant Edu as Educational Services<br/>(Planning / Mission / StudySession)
    participant DB as Database

    Student->>UI: Submit Start Session
    UI->>Exp: start_session(student_id)
    Exp->>Bridge: PlanningBridge.ensure_today(student_id)
    Bridge->>Edu: PlanningService.generate_today_mission
    Edu->>DB: Read StudyPlan, TopicProgress, Lifecycle
    DB-->>Edu: Plan + progress
    Edu->>DB: Upsert Mission + MissionTasks (idempotent)
    DB-->>Edu: Mission row
    Edu-->>Bridge: Mission
    Bridge-->>Exp: todays_session projection
    Exp->>Bridge: MissionLifecycleBridge.start_session(mission_id)
    Bridge->>Edu: StudySessionService.start_session
    Edu->>DB: Mission.status → In Progress
    DB-->>Edu: OK
    Edu-->>Bridge: started
    Bridge-->>Exp: session_id + mission_id
    Exp-->>UI: Redirect session.overview
    UI-->>Student: Overview (real mission topic)
```

**Notes**

- No `seeded_demo_mission`.  
- If ensure/start fails closed → flash + stay Home.  
- SessionWorkspace open happens in Experience after redirect (UX), keyed to bridged `session_id`.

---

## 2. Resume Study

Student returns with an in-progress mission / open workspace.

```mermaid
sequenceDiagram
    actor Student
    participant UI as UI (Home or Session URL)
    participant Exp as Experience Layer<br/>(SessionExperienceService)
    participant Bridge as Bridge<br/>(MissionLifecycle)
    participant Edu as Educational Services<br/>(Mission / StudySession)
    participant DB as Database

    Student->>UI: Open Home / deep-link Session
    UI->>Exp: load_page / resume_redirect_if_needed
    Exp->>Bridge: get_session_status(student_id, session_id)
    Bridge->>Edu: MissionService / StudySessionService.get_owned_mission
    Edu->>DB: SELECT Mission WHERE id + user_id
    DB-->>Edu: Mission (In Progress) or none
    Edu-->>Bridge: ownership + status
    alt Mission In Progress
        Bridge-->>Exp: status=in_progress
        Exp->>Exp: SessionWorkspace.active_surface
        Exp-->>UI: Redirect to active surface
        UI-->>Student: Resume at Overview/Activity/…
    else Missing or Completed
        Bridge-->>Exp: NOT_FOUND / completed
        Exp-->>UI: Redirect Home + flash
    else FORBIDDEN
        Bridge-->>Exp: FORBIDDEN
        Exp-->>UI: 403
    end
```

**Notes**

- Workspace cannot invent a mission if SQL Mission is missing.  
- Durable store required for multi-worker resume of `active_surface` (migration phase).

---

## 3. Load Dashboard (Student Home)

```mermaid
sequenceDiagram
    actor Student
    participant UI as UI (student.home)
    participant Exp as Experience Layer<br/>(HomeService / EducationalStateService)
    participant Bridge as Bridge<br/>(Planning / Recommendation / LearningState / Journey / History)
    participant Edu as Educational Services
    participant DB as Database

    Student->>UI: GET /student/
    UI->>Exp: get_dashboard / home
    par Mission projection
        Exp->>Bridge: PlanningBridge.get_todays_session
        Bridge->>Edu: Planning ensure/get + MissionService
        Edu->>DB: StudyPlan + Mission
        DB-->>Edu: rows
        Edu-->>Bridge: Mission
        Bridge-->>Exp: todays_session
    and Recommendation
        Exp->>Bridge: RecommendationBridge.get_todays_recommendation
        Bridge->>Edu: Align to mission + RecommendationService
        Edu->>DB: Readiness / TopicProgress (as needed)
        DB-->>Edu: aggregates
        Edu-->>Bridge: narrative
        Bridge-->>Exp: recommendation (mission_aligned)
    and Learning state
        Exp->>Bridge: LearningStateBridge.project
        Bridge->>Edu: Readiness + Lifecycle
        Edu->>DB: TopicProgress / plan fields
        DB-->>Edu: data
        Edu-->>Bridge: twin-like projection
        Bridge-->>Exp: readiness / stage
    and Journey / History cards
        Exp->>Bridge: JourneyBridge / HistoryBridge
        Bridge->>Edu: StudyPlan + history reads
        Edu->>DB: queries
        DB-->>Edu: data
        Edu-->>Bridge: snapshots
        Bridge-->>Exp: journey / history
    end
    Exp-->>UI: Home snapshot (no seeded_demo_*)
    UI-->>Student: Render Home
```

**Notes**

- Parallel reads are logical; implementation may sequentialize.  
- Empty authentic state beats demo fabrication.

---

## 4. Complete Session

```mermaid
sequenceDiagram
    actor Student
    participant UI as UI (session.complete POST)
    participant Exp as Experience Layer<br/>(SessionExperienceService)
    participant Bridge as Bridge<br/>(MissionLifecycle + EvidenceParity)
    participant Edu as Educational Services<br/>(StudySession + Evidence + Adaptive)
    participant DB as Database

    Student->>UI: Finish session
    UI->>Exp: complete_session(session_id, outcome?)
    Exp->>Bridge: MissionLifecycleBridge.complete_session
    Bridge->>Bridge: EvidenceParityBridge.map_outcome
    Bridge->>Edu: StudySessionService.finish_session / record_practice_outcome
    Edu->>Edu: EducationalEvidenceAuthority gate
    alt Evidence accepted
        Edu->>DB: Mission Completed + StudyAttempt + TopicProgress
        DB-->>Edu: OK
        Edu-->>Bridge: educational_complete=true
        Bridge-->>Exp: success projection
        Exp->>Exp: Close SessionWorkspace
        Exp-->>UI: Redirect student.home
    else Evidence rejected / invalid
        Edu-->>Bridge: EVIDENCE_REJECTED / INVALID_STATE
        Bridge-->>Exp: failure
        Exp-->>UI: Flash + stay / guided fix
    else Transitional flag (pre–Bridge Complete)
        Bridge-->>Exp: UX complete, educational_complete=false
        Note over Bridge: Telemetry alarm; not allowed at Bridge Complete
    end
```

**Notes**

- Mastery writes only through Evidence Authority.  
- Orchestrator must not become a second mastery writer.

---

## 5. Recommendation Request

Triggered on Home load or explicit Adaptive port refresh.

```mermaid
sequenceDiagram
    actor Student
    participant UI as UI (Home recommendation card)
    participant Exp as Experience Layer<br/>(HomeService / Adaptive port consumer)
    participant Bridge as Bridge<br/>(RecommendationBridge)
    participant Edu as Educational Services<br/>(Planning mission + RecommendationService)
    participant DB as Database

    Student->>UI: View Home (or refresh)
    UI->>Exp: get_todays_recommendation(student_id)
    Exp->>Bridge: RecommendationBridge.get_todays_recommendation
    Bridge->>Edu: MissionService.get_today_mission / PlanningBridge cache
    Edu->>DB: Mission for user/date/plan
    DB-->>Edu: Mission or none
    alt Mission exists
        Bridge->>Edu: RecommendationService.generate_today_recommendation
        Edu->>DB: Readiness / weak topics / lifecycle
        DB-->>Edu: aggregates
        Edu-->>Bridge: recommendations list
        Bridge->>Bridge: Align primary label to mission topic
        Bridge-->>Exp: mission_aligned=true DTO
    else No mission
        Bridge->>Edu: RecommendationService (optional narrative)
        Edu->>DB: reads
        DB-->>Edu: data
        Edu-->>Bridge: empty or setup guidance
        Bridge-->>Exp: mission_aligned=false; CTA disabled
    end
    Exp-->>UI: Recommendation + explanation
    UI-->>Student: Card (same topic as Start Session when mission exists)
```

**Invariant:** When a mission exists, recommendation primary topic **equals** mission topic (AC-2).

---

## 6. Cross-flow identity map

```
ExperienceSessionId  ←→  MissionId (SQL)
StudentId            ←→  User.id
StudyPlanId          ←→  active StudyPlan
TopicProgress        ←→  mastery SoT (via Evidence)
SessionWorkspace     ←→  UX step only (not topic SoT)
```

---

## Stop condition

Sequence diagrams complete for Start Study, Resume Study, Load Dashboard, Complete Session, and Recommendation Request. **No production code.**
