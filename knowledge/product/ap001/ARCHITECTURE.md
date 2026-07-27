# AP-001 Architecture — Assessment & Learning Feedback Pipeline

Companion to `COMPLETION_REPORT.md`. Introduces the Assessment & Learning
Feedback Pipeline without redesigning CS-DOC-001, CIP-001 → CIP-003,
SDT-001 → SDT-003, or AME-001.

## Long-term principle

Kwalitec now closes the adaptive learning loop:

1. **Curriculum Intelligence** — WHAT should be learned
2. **Student Digital Twin** — WHO is learning
3. **Learning Graph** — HOW knowledge is interconnected
4. **Educational Reasoning** — WHY educational state changes
5. **Adaptive Mission Engine** — WHAT to do today
6. **Assessment Pipeline** — evidence from learner activity back into the Twin

The Assessment Pipeline must **never** perform educational reasoning itself.
It records educational evidence and delegates learner-state updates to
`StudentReasoningService` / the Educational Reasoning Engine.

```
Learner Activity
        │
        ▼
Validation
        │
        ▼
Assessment Event (immutable)
        │
        ▼
Observation Creation (SDT-001 fact)
        │
        ▼
StudentReasoningService → Educational Reasoning Engine
        │
        ▼
Student Digital Twin Update
        │
        ▼
Learning Feedback (educational, deterministic)
        │
        ▼
Mission Refresh Trigger (via Adaptive Mission Engine)
```

No LLM. No duplicated Twin mastery / gap / recommendation rows.

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/assessment_pipeline/` |
| Application | `app/application/assessment_pipeline/` |
| Persistence | `app/models/assessment_pipeline.py` |
| Founder diagnostics | `app/presentation/assessment_pipeline/` (`/founder/assessment/*`) |

## Assessment lifecycle

1. Capture learner activity (question, quiz, mission step/completion, revision, …)
2. Validate structural completeness (`feedback_validator`)
3. Persist immutable `AssessmentEvent`
4. Map event → SDT-001 `Observation` (existing ObservationKind values)
5. Persist `AssessmentResult` metadata linking event ↔ observation
6. Invoke `StudentReasoningService.reason` (only path that updates Twin inferences)
7. Persist deterministic `LearningFeedback`
8. Optionally trigger Adaptive Mission regeneration from updated Twin state

## Observation generation

Assessment events map to existing Twin observation kinds so SDT-001 remains
unchanged:

| Assessment event | ObservationKind |
|---|---|
| question_attempt | question_answered |
| quiz_submission | quiz_completed |
| mission_step_completion | study_session_completed |
| mission_completion | study_session_completed |
| revision_session | revision_completed |
| worked_example_completion | study_session_completed |
| formula_recall | formula_reviewed |
| reflection_submission | study_session_completed |
| study_session_completion | study_session_completed |

Provenance encodes `assessment_pipeline:<event_type>:<event_id>`.

## Mission integration

`AdaptiveMissionService.update_progress` and `.complete` emit assessment events
via `AssessmentPipelineService` (best-effort, opt-out with `emit_assessment=False`).

Mission success influences future missions **only** through Twin updates
produced by Educational Reasoning — never by the Assessment Pipeline inventing
priorities.

Links are stored in `mission_assessment_links`.

## Student Digital Twin integration

- Observations append via `ObservationService`
- Inferences update exclusively via `StudentReasoningService`
- Assessment tables store evidence metadata only

## Educational Reasoning integration

Triggered with `triggered_by=assessment_pipeline:<event_type>`. Curriculum
evidence continues to enter only through `CurriculumRetrievalService`.

## Founder diagnostics

| Endpoint | Purpose |
|---|---|
| `GET /founder/assessment/events` | List assessment events |
| `GET /founder/assessment/results` | List assessment results |
| `GET /founder/assessment/feedback` | List learning feedback |
| `GET/POST /founder/assessment/pipeline` | Describe / run pipeline |
| `GET /founder/assessment/diagnostics` | Twin-scoped diagnostics |

Not student-facing. Dashboard UX unchanged.

## Persistence

Alembic `202607270012` adds:

| Table | Purpose |
|---|---|
| `assessment_events` | Immutable activity events |
| `assessment_results` | Result ↔ observation metadata |
| `learning_feedback` | Deterministic educational feedback |
| `mission_assessment_links` | Mission ↔ event links |
| `activity_attempts` | Attempt records |
| `performance_summaries` | Evidence-only performance rollups |

## What AP-001 does not do

- Educational reasoning / mastery inference
- Dashboard redesign / student UX
- LLM scoring or motivational coaching copy
- Direct VectorStore access
- Duplication of Twin learner state
