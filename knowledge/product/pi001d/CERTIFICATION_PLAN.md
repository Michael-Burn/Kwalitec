# PI-001D — Platform Certification Plan

**Programme:** PI-001D — Educational Platform Certification  
**Status:** Active  
**Date:** 2026-07-27  

---

## 1. Purpose

Certify that the complete educational platform — founder onboarding (PI-001A), educational derivation (PI-001B), and curriculum-driven runtime (PI-001C) — functions correctly as an integrated system before any runtime cutover decision.

This programme does not add functionality, redesign UI, or activate the Digital Twin. It produces evidence for a production cutover decision.

---

## 2. Certification scenarios

### CS-01: Founder onboarding

| Step | Description | Acceptance |
|---|---|---|
| CS-01.1 | Create a new subject via Curriculum Studio Foundation | Subject persisted with unique code |
| CS-01.2 | Upload CMP and syllabus documents | Documents stored as references |
| CS-01.3 | Process curriculum (extract + parse) | Processing state advances; parsed structure stored |
| CS-01.4 | Validate curriculum | Validation report passes |
| CS-01.5 | Founder review and approval | Version enters approved state |
| CS-01.6 | Publish curriculum version | Immutable published package created; prior active deactivated |
| CS-01.7 | Subject-agnostic verification | Second subject publishes without code changes |

### CS-02: Curriculum publication

| Step | Description | Acceptance |
|---|---|---|
| CS-02.1 | Published package contains complete structure | Sections, topics, objectives, prerequisites preserved |
| CS-02.2 | Published authority exposes only published packages | Draft/processing versions never returned |
| CS-02.3 | Version deactivation on new publish | Prior active package deactivated |

### CS-03: Educational derivation

| Step | Description | Acceptance |
|---|---|---|
| CS-03.1 | Derive artefacts from published package | Graph, study plan template, mission templates, journey, progress model all non-empty |
| CS-03.2 | Topic ordering matches published curriculum order | Topological order respects prerequisites |
| CS-03.3 | CS1 equivalence with JSON runtime | Section count, topic count, topic codes, topic titles match existing V2 engine |
| CS-03.4 | Mission template coverage | At least one template per topic |
| CS-03.5 | Progress model completeness | All topic IDs and objective IDs present |

### CS-04: Student enrolment

| Step | Description | Acceptance |
|---|---|---|
| CS-04.1 | Enrol against published curriculum | Enrolment created with correct identity |
| CS-04.2 | Auto-instantiate study plan | Study plan with correct topic count and first topic |
| CS-04.3 | Duplicate enrolment rejected | EnrolmentAlreadyExists raised |
| CS-04.4 | Enrolment without published curriculum rejected | PublishedCurriculumUnavailable raised |

### CS-05: Study plan instantiation

| Step | Description | Acceptance |
|---|---|---|
| CS-05.1 | Plan derives from template | Topic template IDs populated |
| CS-05.2 | Current topic initialised | First topic in curriculum order |
| CS-05.3 | Progress model initialised at zero | Coverage ratio 0.0 |

### CS-06: Mission generation

| Step | Description | Acceptance |
|---|---|---|
| CS-06.1 | Generate daily mission | Mission created with template, topic, tasks |
| CS-06.2 | Idempotent for same day | Same mission instance returned |
| CS-06.3 | Mission targets current topic | Topic ID matches plan's current topic |

### CS-07: Mission completion

| Step | Description | Acceptance |
|---|---|---|
| CS-07.1 | Complete mission | Status transitions to completed |
| CS-07.2 | Topic marked complete | Topic appears in completed set |
| CS-07.3 | Journey advances to next topic | Current topic changes |
| CS-07.4 | Duplicate completion rejected | MissionAlreadyCompleted raised |

### CS-08: Progress derivation

| Step | Description | Acceptance |
|---|---|---|
| CS-08.1 | Coverage ratio updates | Proportional to completed topics |
| CS-08.2 | Journey stage reflects progress | Progresses through learning stages |
| CS-08.3 | Syllabus completion detected | When all topics completed |

### CS-09: Journey progression (end-to-end)

| Step | Description | Acceptance |
|---|---|---|
| CS-09.1 | Full syllabus traversal | All topics completed through mission cycle |
| CS-09.2 | Final state correct | Enrolment completed, plan completed, coverage 1.0 |
| CS-09.3 | Post-completion mission rejected | SyllabusAlreadyComplete raised |
| CS-09.4 | Event audit trail complete | All event types present in correct order |

### CS-10: Readiness inputs

| Step | Description | Acceptance |
|---|---|---|
| CS-10.1 | Readiness inputs derive from progress | Topic IDs, completed IDs, coverage ratio consistent |
| CS-10.2 | Denominator source is published model | Not duplicating state from another source |

### CS-11: Estimated Knowledge inputs

| Step | Description | Acceptance |
|---|---|---|
| CS-11.1 | EK inputs derive from progress | Per-topic completion status correct |
| CS-11.2 | No phantom knowledge claims | has_estimated_knowledge is False without actual data |

### CS-12: Runtime coexistence

| Step | Description | Acceptance |
|---|---|---|
| CS-12.1 | Unpublished subjects resolve to JSON runtime | RuntimeAuthority.JSON_BUNDLED |
| CS-12.2 | Published subjects resolve to curriculum runtime | RuntimeAuthority.PUBLISHED_CURRICULUM |
| CS-12.3 | JSON runtime study plan unaffected | StudyPlanService works independently of Runtime C enrolment |
| CS-12.4 | json_runtime_remains_default is True | Coexistence policy confirms A is default |

---

## 3. Test strategy

### Layer 1: Domain certification
Pure domain logic tests without database — progress derivation, state transitions, event types.

### Layer 2: Application certification
Service-level tests with database — full lifecycle through `EducationalRuntimeEngineService`.

### Layer 3: Cross-runtime parity
Compare Runtime A (JSON + StudyPlanService + PlanningService) and Runtime C (published + EducationalRuntimeEngineService) for CS1 subject.

### Layer 4: End-to-end certification
Full founder-to-student lifecycle: publish → enrol → plan → missions → complete syllabus.

### Layer 5: Coexistence certification
Both runtimes active simultaneously without interference.

---

## 4. Runtime parity dimensions

| Dimension | Runtime A source | Runtime C source | Comparison |
|---|---|---|---|
| Topic ordering | CurriculumService.get_all_topics_ordered | Topological ordering from published graph | Code sequence match |
| Topic count | Engine topic list length | Derived artefact topic count | Numeric equality |
| Section structure | Section model rows | Derived section artefacts | Count and code match |
| Mission generation | PlanningService.build_daily_study_plan | EducationalRuntimeEngineService.generate_daily_mission | Both produce missions per topic |
| Progress tracking | TopicProgress model | derive_progress from events | Coverage calculation comparison |
| Readiness denominator | Topic count from curriculum | topic_ids from progress model | Length equality |

---

## 5. Intentional differences (expected)

| Difference | Runtime A | Runtime C | Rationale |
|---|---|---|---|
| Data model | ORM-centric (StudyPlan, WeekPlan, TopicProgress, Mission) | Event-sourced (RuntimeEnrolment, events, derived progress) | Runtime C uses immutable event stream |
| Study plan shape | Weekly plans with time allocations | Flat topic template list | Runtime C does not model weekly scheduling yet |
| Mission generation | PlanningService with lifecycle, recovery, revision modes | Single template-per-topic generation | Runtime C implements minimal viable generation |
| Progress storage | TopicProgress rows with mastery scores | Derived from event stream | Runtime C has no mutable progress rows |
| Readiness | ReadinessService with weighted percentages | ReadinessRuntimeInputs with coverage ratio | Runtime C provides inputs, not full readiness |
| Recommendation | RecommendationService with personalisation | Not implemented | Out of scope for Runtime C |
| Exam timeline | Time engine integration | Not implemented | Runtime C does not model time budgets |

---

## 6. Constraints

- Runtime A remains production runtime
- Runtime C must not replace Runtime A
- All tests must be reproducible and automated
- No UI changes
- No Twin activation
