# PX-001 — Screen-by-Screen Mapping

**Programme:** PX-001 — Educational Experience Integration  
**Date:** 2026-07-27  
**Note:** Distinct from the earlier Premium Experience Audit under `knowledge/product/px001/`.

---

## Scope

Student-facing screens that present educational information. Premium redesign, Twin activation, and Runtime A cutover are out of scope.

| Screen | Route | Educational decision | Runtime C data | Previously shown | Gap closed |
|---|---|---|---|---|---|
| **Home** | `student.home` `/student/` | What to study today and why | `MissionInstanceSnapshot.quality`, curriculum position, journey explanation, pacing | Runtime A recommendation / empty when no StudyPlan | Mission rationale, LOs, duration, completion, position, journey, pacing, explainability |
| **Journey** | `student.journey` `/student/journey` | Where am I on the syllabus path? | `ProgressSnapshot`, `JourneyExplanationSnapshot`, topic lists | Runtime A TopicProgress titles only | why_today / previous / unlocks_next, progress %, exam pacing |
| **Revision** | `student.revision` | What to revise? | N/A (first-pass Runtime C path) | Runtime A Adaptive revision | Deferred — no Runtime C revision stage yet |
| **History** | `student.history` | What have I completed? | Event stream (available) | Runtime A sessions | Deferred — event narrative not required for acceptance |
| **Profile** | `student.profile` | Exam / preferences | Enrolment identity | Runtime A plan metadata | Deferred — Home/Journey carry examination label |
| **Study plan wizard** | `study_plan.*` | Enrol which subject? | Discovery + enrolment bridge | Already wired (PI-002A) | No change — enrolment remains the Runtime C entry point |
| **Legacy Dashboard / Mission** | `dashboard.*` / `mission.*` | Runtime A daily mission | Parallel only | Runtime A | Unchanged — coexistence preserved |

---

## Acceptance field → screen placement

| Acceptance criterion | Home | Journey | Source |
|---|---|---|---|
| Today's curriculum topic | ✓ hero + educational panel | ✓ current topic | `curriculum_position.topic_title` |
| Curriculum position | ✓ panel | ✓ progress + position | `position_label`, section title |
| Learning objectives | ✓ panel | ✓ panel | `mission.learning_objectives` |
| Mission rationale | ✓ hero Why + panel | ✓ panel | `quality.educational_rationale` / explanation |
| Estimated duration | ✓ hero duration + panel | ✓ panel | `estimated_duration_minutes` |
| Completion criteria | ✓ panel | ✓ panel | `completion_definition` |
| Journey explanation | ✓ panel | ✓ panel + topic notes | `get_journey_explanation()` |
| Progress | ✓ panel | ✓ progress card | `coverage_ratio` |
| Exam pacing | ✓ panel | ✓ panel | `project_pacing()` |
| Honest explanations | ✓ disclosure | ✓ disclosure | EQ-001 explanation schema |

---

## Non-goals confirmed

- No premium styling or layout redesign beyond clarity.
- No Twin activation.
- No Runtime A cutover; students without Runtime C enrolment keep the prior path.
- Session completion write-back to Runtime C remains a follow-up (visibility first).
