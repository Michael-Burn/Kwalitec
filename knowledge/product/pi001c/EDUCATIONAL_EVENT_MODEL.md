# PI-001C — Educational Event Model

Educational events are the durable student history for the curriculum-driven
runtime. They are **append-only**. Progress and journey position are derived
from the event stream plus the published progress model.

## Event kinds

| `event_type` | When emitted | Key payload |
|---|---|---|
| `student_enrolled` | Enrolment created | subject_code, version_label, published_package_id |
| `study_plan_instantiated` | Plan instance created from template | topic_template_count, current_topic_id |
| `mission_generated` | Daily mission created from template | template_id, mission_date, title |
| `mission_completed` | Mission marked complete | template_id, mission_date |
| `topic_completed` | Topic marked complete (study progress) | source=`mission_completion` |
| `journey_advanced` | Current topic / stage reconciled | from_topic_id, to_topic_id, journey_stage, coverage_ratio |
| `syllabus_completed` | All progress-model topics complete | completed_topic_count |

## Storage

Table: `runtime_educational_events`

| Column | Role |
|---|---|
| `event_id` | Stable unique id |
| `event_type` | Kind (above) |
| `user_id` | Student |
| `enrolment_id` / `plan_instance_id` / `mission_instance_id` | Runtime refs |
| `curriculum_identity` | `SUBJECT:version` |
| `topic_id` | Optional topic binding |
| `payload_json` | Structured facts |
| `occurred_at` | Event time |

No update/delete API is provided by the runtime service.

## Derivation rule

Only `topic_completed` events contribute to progress completion.  
`mission_completed` alone does **not** advance coverage — the engine always emits
a paired `topic_completed` when a learning mission completes a topic.

## Evidence policy for Estimated Knowledge

Mission / topic completion updates **study progress** only.  
`EstimatedKnowledgeRuntimeInputs` always reports
`has_estimated_knowledge=False` until a future evidence path records structured
question accuracy (same constitutional rule as Runtime A).
