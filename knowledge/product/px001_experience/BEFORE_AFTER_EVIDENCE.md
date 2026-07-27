# PX-001 — Before / After Evidence

**Programme:** PX-001 — Educational Experience Integration  
**Date:** 2026-07-27  

---

## Before

| Observation | Evidence |
|---|---|
| Runtime C produced EQ-001 mission quality, journey explanation, and pacing at the application layer | EQ-001 completion report; `EducationalRuntimeEngineService` |
| Student Home / Journey consumed Runtime A ports only (Twin / Adaptive / JourneyAdapter) | `HomeService`, `JourneyService`, composition adapters |
| Runtime C enrolment redirected to Home with **no** `StudyPlan`, so educational value was invisible | PI-002A enrolment bridge |
| No template referenced `MissionQualityEnvelope` or `JourneyExplanationSnapshot` | Grep across `app/templates` |

A Runtime C student could not answer:

1. What am I studying today?  
2. Where is that in my syllabus?  
3. Why this mission?  
4. How long / what counts as done?  
5. Am I on pace for the exam?

---

## After

| Observation | Evidence |
|---|---|
| `EducationalExperienceService` projects Runtime C → student-safe snapshot | `app/application/educational_experience/` |
| Home / Journey load Runtime C projection when enrolment is active | `views._try_runtime_c_page` |
| Educational panel renders all acceptance fields | `educational_experience.html` + HTTP acceptance test |
| Runtime A students unchanged (no panel) | `test_coexistence_runtime_a_home_unchanged_without_runtime_c` |

### Acceptance checklist (automated)

| Criterion | Marker / assertion | Status |
|---|---|---|
| Today's curriculum topic | `data-edu-field="today_topic"` | Pass |
| Curriculum position | `data-edu-field="curriculum_position"` | Pass |
| Learning objectives | `data-edu-field="learning_objectives"` | Pass |
| Mission rationale | `data-edu-field="mission_rationale"` | Pass |
| Estimated duration | `data-edu-field="estimated_duration"` | Pass |
| Completion criteria | `data-edu-field="completion_definition"` | Pass |
| Journey explanation | `data-edu-field="journey_explanation"` | Pass |
| Progress | `data-edu-field="progress"` | Pass |
| Exam pacing | `data-edu-field="exam_pacing"` | Pass |
| Honest explanations | `data-edu-field="explainability"` | Pass |

Raw pytest log: [`TEST_EVIDENCE_RAW.txt`](TEST_EVIDENCE_RAW.txt).

---

## Student independence test

A founding-cohort student enrolled via Published subject discovery can open Home and Journey and read syllabus position, mission rationale, objectives, duration, completion definition, journey explanation, progress, and exam pacing **without founder assistance**.
