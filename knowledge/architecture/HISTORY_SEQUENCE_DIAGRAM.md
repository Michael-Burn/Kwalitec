# MS-002 — History Sequence Diagrams

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001 / 003  
**Status:** Architecture Design; **History Read Bridge (J2) — Implemented**  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Companion:** `JOURNEY_SEQUENCE_DIAGRAM.md`

---

## Conventions

Layer order in every diagram:

**UI → Experience Layer → Bridge → Educational Services → Database**

| Participant | Meaning |
|---|---|
| UI | History templates / Home history card |
| Exp | `HistoryService` / Twin insights consumer |
| Bridge | `HistoryAdapter` (`HistoryBridge`) |
| Services | Runtime A: Mission, StudyAttempt / Evidence, Readiness, Lifecycle |
| DB | SQLAlchemy models |

Bridges are **read-only**. History never surfaces raw event dumps (`events` / `raw_events` / `event_log`).

---

## 1. Load History

Student opens History page (or Home loads history card).

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as UI<br/>(history / home card)
    participant Exp as Experience Layer<br/>(HistoryService)
    participant Bridge as HistoryBridge
    participant Mission as MissionService / Mission queries
    participant Attempt as StudyAttempt reads
    participant Ready as ReadinessService
    participant Life as LearningLifecycleService
    participant Adaptive as AdaptiveLearningService<br/>(weak / mastered labels)
    participant DB as Database

    Student->>UI: GET /student/history
    UI->>Exp: history(student_id, page?)
    Exp->>Bridge: project_history(student_id,<br/>limit, offset, filters)

    Bridge->>Mission: list completed Missions<br/>(owned, ordered desc)
    Mission->>DB: SELECT missions<br/>WHERE user_id AND status=Completed
    Bridge->>Attempt: aggregate study minutes / attempts
    Attempt->>DB: SELECT study_attempts
    Bridge->>Ready: readiness progression samples
    Ready->>DB: aggregates / TopicProgress snapshots
    Bridge->>Adaptive: mastered topic labels
    Adaptive->>DB: TopicProgress mastery
    Bridge->>Life: revision-stage activity labels
    Life->>DB: lifecycle inputs

    Note over Bridge: Map to HistoryProjection shape.<br/>No mastery recomputation.<br/>Strip any raw event keys.

    alt Empty authentic
        Bridge-->>Exp: empty sessions, zero minutes,<br/>empty progression
        Exp-->>UI: History empty state
    else Has history
        Bridge-->>Exp: HistorySnapshot + trace hints
        Exp-->>UI: HistoryPageViewModel
        UI-->>Student: Authoritative accomplishment narrative
    end
```

### Pagination / filter application

```mermaid
sequenceDiagram
    autonumber
    participant Exp as Experience Layer
    participant Bridge as HistoryBridge
    participant DB as Database

    Exp->>Bridge: project_history(limit, offset,<br/>from_date, to_date, event_types, topic_code)
    Note over Bridge: Validate limit ≤ hard max<br/>Normalize dates / ownership scope
    Bridge->>DB: Filtered, ordered query
    DB-->>Bridge: Page of rows + optional total_count
    Bridge-->>Exp: items[], next_offset / cursor,<br/>has_more
```

### Notes

- When `ENABLE_HISTORY_BRIDGE` is off, HistoryService may still read Twin demo insights — not shown.  
- Home card uses `limit` small (e.g. 3–5 sessions) against the same Bridge.  
- Failure: empty authentic + telemetry; never fabricate sessions.

---

## 2. Inspect Evidence

Student opens a History item to see supporting educational evidence (attempt / acceptance), without dumping raw logs.

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as UI<br/>(history detail)
    participant Exp as Experience Layer
    participant Bridge as HistoryBridge
    participant Mission as MissionService
    participant Attempt as StudyAttempt / Learning reads
    participant Evidence as EducationalEvidenceAuthority<br/>(read / explain posture)
    participant DB as Database

    Student->>UI: Inspect session / evidence
    UI->>Exp: evidence_detail(student_id, mission_id|attempt_id)
    Exp->>Bridge: get_evidence_summary(student_id, ref)

    Bridge->>Mission: get_owned_mission(mission_id)
    Mission->>DB: SELECT mission + ownership
    alt Not owned / missing
        Bridge-->>Exp: FORBIDDEN / NOT_FOUND
        Exp-->>UI: 404-style safe empty
    else Owned
        Bridge->>Attempt: attempts for mission / topic / date
        Attempt->>DB: SELECT study_attempts
        Bridge->>Evidence: summarise acceptance posture<br/>(read-only)
        Evidence-->>Bridge: accepted / rejected / gated flags
        Note over Bridge: Project EvidenceSummary DTO:<br/>what was practised, outcome labels,<br/>whether mastery update was authorised.<br/>Never return raw event_log arrays.
        Bridge-->>Exp: evidence_summary + trace
        Exp-->>UI: Evidence panel
        UI-->>Student: What evidence supports this item
    end
```

### Notes

- Inspect is **read-only**. It must not re-run Evidence Authority writes or “repair” mastery.  
- If evidence cannot be summarised, return honest empty / `unavailable` — do not invent correctness scores.  
- Pair with Journey “View Recommendation Change” when the same `event_id` carries recommendation delta (see `JOURNEY_SEQUENCE_DIAGRAM.md` §2).

---

## 3. Cross-reference

| Flow | Location |
|---|---|
| Load Journey | `JOURNEY_SEQUENCE_DIAGRAM.md` §1 |
| View Recommendation Change | `JOURNEY_SEQUENCE_DIAGRAM.md` §2 |
| Load History | This file §1 |
| Inspect Evidence | This file §2 |

---

## Stop condition

Diagrams are design artefacts only. Do not implement adapters from this document alone.
