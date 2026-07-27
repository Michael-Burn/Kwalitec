# PI-001C — State Transition Model

## Enrolment

```text
active ──► completed
  │
  └──► withdrawn

completed / withdrawn are terminal
```

| From | To | Trigger |
|---|---|---|
| (none) | `active` | `enrol_student` |
| `active` | `completed` | syllabus fully completed via runtime |
| `active` | `withdrawn` | explicit withdrawal (reserved) |

## Study plan instance

```text
active ──► paused ──► active
  │           │
  └───────────┴──► completed
```

| From | To | Trigger |
|---|---|---|
| (none) | `active` | study plan instantiated from template |
| `active` | `completed` | all progress-model topics completed |
| `active` | `paused` | reserved |
| `paused` | `active` | reserved |

`current_topic_id` on the plan instance is a **reconciled projection** of
`derive_progress(...).current_topic_id`, not an independent educational truth.

## Mission instance

```text
generated ──► completed
```

| From | To | Trigger |
|---|---|---|
| (none) | `generated` | `generate_daily_mission` (idempotent per plan+date) |
| `generated` | `completed` | `complete_mission` |

Re-completing a completed mission is rejected.

## Journey stage (derived)

```text
not_started ──► learning ──► syllabus_complete
                                    │
                                    └──► revision (future; not persisted yet)
```

Resolved by `next_journey_stage(completed_count, total_count)` from the published
progress model + `TOPIC_COMPLETED` events.

## Illegal transitions

Domain helpers raise `IllegalRuntimeTransition` for illegal moves. Application
service maps these to `IllegalRuntimeState` / `MissionAlreadyCompleted` as
appropriate.
