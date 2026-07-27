# EQ-001 — Journey Quality Rules

**Programme:** EQ-001  
**Status:** Active  
**Applies to:** Runtime C journey progression and explainable transitions

---

## Mandatory explainable transitions

For every student journey against a published subject, the system must always be able to answer:

| Question | Required field | Source |
|---|---|---|
| **Why was today’s topic selected?** | `why_today` | Current topic from progress model + syllabus order + satisfied prerequisites |
| **Why is the previous topic complete?** | `why_previous_complete` | Last `TOPIC_COMPLETED` / mission completion event; or “no previous topic” at start |
| **What unlocks next?** | `unlocks_next` | Next eligible topic after completing current, or syllabus-complete / revision posture |

---

## Transition rules

1. Today’s topic = `derive_progress().current_topic_id` (first incomplete topic with satisfied prerequisites).
2. Completing a mission for topic T emits `TOPIC_COMPLETED` then advances to the next eligible topic.
3. Journey explanations must use educational language only (no Twin / pipeline / entity-id theatre).
4. Syllabus complete: `why_today` states first-pass complete; `unlocks_next` states revision / readiness posture without inventing mastery.
5. Every `JOURNEY_ADVANCED` event payload must remain reconstructable into the three answers above.

---

## Certification ids

| Id | Check |
|---|---|
| EQ-J01 | Journey explanation present at enrolment start |
| EQ-J02 | `why_today` names current curriculum topic |
| EQ-J03 | After first completion, `why_previous_complete` cites completed topic |
| EQ-J04 | `unlocks_next` names next topic or syllabus-complete posture |
| EQ-J05 | Full journey maintains explainable transitions at each step |
