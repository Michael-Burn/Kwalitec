# EQ-001 — Mission Quality Rules

**Programme:** EQ-001  
**Status:** Active  
**Applies to:** Derived mission templates (PI-001B) and Runtime C mission instances (PI-001C)

---

## Mandatory fields

Every mission template and every generated mission instance must expose:

| Field | Rule | Fail when |
|---|---|---|
| **Curriculum topic** | Non-empty `topic_id` and `topic_code` bound to the published package | Missing or unknown topic |
| **Learning objective references** | ≥1 `objective_id` from the topic’s published objectives | Empty objective list |
| **Estimated duration** | Positive `estimated_duration_minutes` derived from topic/objective minutes | ≤ 0 or missing |
| **Completion definition** | Explicit, student-readable definition of done | Empty or vague “done” without tasks |
| **Educational rationale** | Structured reason referencing syllabus position and objectives | Empty, Twin/pipeline jargon, or invented mastery claims |
| **Prerequisite validation** | Snapshot stating which prerequisites are required and whether they are satisfied for this mission | Missing validation; mission on topic with unsatisfied prerequisites |

---

## Derivation rules

1. One primary `learn_topic` mission template per published topic.
2. Title must include topic code and title (curriculum-bound — no generic “Study session”).
3. Task descriptions must reference the topic and at least one learning objective when objectives exist.
4. `estimated_duration_minutes` defaults to the topic’s `estimated_minutes` (sum of objective minutes when topic minutes absent).
5. `completion_definition` = all listed task descriptions acknowledged/completed for this mission day.
6. `educational_rationale` = syllabus-order learning of the current topic, citing objective codes — never mastery or Exam Ready claims.
7. Prerequisites are the topic’s published `prerequisite_ids`; generation must refuse or fail certification if the current progress model shows unmet prerequisites.

---

## Instance enrichment

When Runtime C generates a daily mission, the instance quality envelope must copy template fields and attach:

- `prerequisite_validation.required_ids`
- `prerequisite_validation.satisfied_ids`
- `prerequisite_validation.all_satisfied` (must be `true` for a lawful learning mission)
- `explanation` per [`EXPLAINABILITY_SPECIFICATION.md`](EXPLAINABILITY_SPECIFICATION.md)

---

## Certification ids

| Id | Check |
|---|---|
| EQ-M01 | Every mission template has curriculum topic binding |
| EQ-M02 | Every mission template has ≥1 learning objective reference |
| EQ-M03 | Every mission template has positive estimated duration |
| EQ-M04 | Every mission template has non-empty completion definition |
| EQ-M05 | Every mission template has non-empty educational rationale |
| EQ-M06 | Generated mission instance carries full quality envelope |
| EQ-M07 | Generated mission prerequisite validation reports all satisfied |
