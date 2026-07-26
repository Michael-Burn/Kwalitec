# Programme II — Unified Student Journey Architecture

**Milestones:** P2-MS001 (Journey Framework) · P2-MS002 (Journey Stage Integration) · P2-MS003 (Daily Mission Experience) · P2-MS004 (Guided Study Session) · **P2-MS005 (Guided Reflection Experience)**  
**Directive:** Engineering Directive 001 (Experience Layer — Guided Reflection Experience)  
**Status:** Guided Reflection Experience — Implemented  
**Package:** `app/application/unified_journey/`  
**Flag:** `KWALITEC_UNIFIED_JOURNEY` → `ENABLE_UNIFIED_JOURNEY` (default **OFF**)  
**Contract version:** `p2.ms005.1`

---

## 0. Purpose

Organise Programme I capabilities around a **single end-to-end student journey**.

When `ENABLE_UNIFIED_JOURNEY` is ON, Home answers one question immediately: **“What should I do next?”** — then guides the student through a structured study session and a lightweight optional reflection before concluding the learning day. Subsystem boundaries remain invisible.

| Milestone | Delivered |
|---|---|
| **P2-MS001** | Journey Coordinator, stages, contracts, navigation, Home placeholders |
| **P2-MS002** | `JourneyContext`, `JourneyContextAssembler`, stage→subsystem mapping, Home wired to Programme I outputs |
| **P2-MS003** | `DailyMission`, `DailyMissionAssembler`, `JourneyEvent`, Experience Timeline, mission-first Home |
| **P2-MS004** | `DayExperience`, `StudySession`, guided session phases / controls, Home continuous journey |
| **P2-MS005** | `SessionOutcome`, Guided Reflection prompts / states, Home reflection step |

**Non-goals (explicit):**

- Evidence writes / persistence of reflection responses
- AI-generated feedback / notifications / analytics
- Timers / Pomodoro
- Runtime A / Adaptive / Strategy / Digital Twin / Evidence modifications
- Educational logic or authority reassignment in the Experience Layer

---

## 1. Responsibilities

| Component | Responsibility | Non-responsibility |
|---|---|---|
| **Journey Coordinator** | Stage → Context → DailyMission → DayExperience → StudySession / SessionOutcome → ReflectionExperience | Educational decisions; inventing recommendations; mutating Programme I outputs |
| **JourneyContextAssembler** | Compose presentation-ready `JourneyContext` from opaque Programme I projections | Creating recommendations; overriding subsystem decisions; educational math |
| **DailyMissionAssembler** | Transform `JourneyContext` → student-facing `DailyMission` | Generating recommendations; modifying subsystem outputs |
| **DayExperienceAssembler** | Combine DailyMission + Timeline → canonical `DayExperience` (+ SessionOutcome / reflection state) | Persistence; educational calculations; engine calls |
| **StudySessionAssembler** | Transform `DayExperience` → student-facing `StudySession` | Timing calculations; educational recommendations |
| **SessionOutcomeAssembler** | Transform post-session `DayExperience` → `SessionOutcome` | Educational metrics; mastery; evidence |
| **ReflectionAssembler** | Transform `SessionOutcome` → presentation-ready `ReflectionExperience` | Educational interpretation; persistence; AI feedback |
| **Session controls** | Pure Start / Resume / Finish presentation transitions | Persistence; evidence writes; Runtime A / Strategy recalculation |
| **Reflection controls** | Pure Start / Complete / Skip presentation transitions | Persisting responses; Evidence Platform writes |
| **DailyMission** | Home mission briefing model | Persistence; educational calculations |
| **DayExperience** | **Canonical** daily presentation object | Educational authority |
| **SessionOutcome** | **Canonical** post-session presentation object | Educational metrics / mastery |
| **StudySession** | Guided session view model | Timers; educational writes |
| **ReflectionExperience** | Guided Reflection view model | Evidence; educational interpretation |
| **JourneyEvent** | Immutable Experience transition records | Triggering educational recalculation |
| **ExperienceTimeline** | Today's journey presentation aid | Educational authority; persistence |

---

## 2. Experience dependency graph

```
                    ┌─────────────────────────┐
                    │   Student Experience UI │
                    │  (Home continuous day)  │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   Journey Coordinator   │
                    │  Stage → … → Reflection │
                    └───────────┬─────────────┘
                                │
     ┌──────────┬───────────┬───┴────┬──────────┬──────────────┐
     ▼          ▼           ▼        ▼          ▼              ▼
 JourneyCtx  DailyMission  DayExp  StudySession SessionOutcome Reflection
 Assembler   Assembler     Assembler Assembler  Assembler      Assembler
     │            │           │
     └──────┬─────┴───────────┘
            │ consumes read-only
   ┌────────┼──────────┬──────────┬──────────┐
   ▼        ▼          ▼          ▼          ▼
 Runtime A  Twin    Adaptive  Strategy  Evidence
              Programme I authority (unchanged)
```

**Rules:**

- Coordinator **orchestrates only** — never decides education.
- Assemblers **read / project** only — never recalculate recommendations.
- Session / reflection controls are **pure functions** — no side effects beyond returned DTOs / events.
- `JourneyEvent` records Experience transitions only — never trigger engines.
- Missing inputs yield explicit placeholders (`availability=placeholder`).

---

## 3. DayExperience lifecycle

`DayExperience` is the **canonical representation of today's student Experience**.

```
1. Resolve JourneyStage → assemble JourneyContext
2. DailyMissionAssembler.assemble(JourneyContext) → DailyMission
3. ExperienceTimeline from DailyMission completion / stage
4. DayExperienceAssembler.assemble(DailyMission, timeline=, phase=?, reflection_state=?)
   - Derive current_phase from completion (or explicit override)
   - Set session_status label (Ready / Studying / Wrapping Up / Complete)
   - When post-session: assemble SessionOutcome
   - When Complete: default reflection_state = Available
   - Set upcoming_transition + progress_summary (student wording)
5. Home / StudySessionAssembler / ReflectionAssembler consume DayExperience
```

`DayExperience` fields (presentation-only):

| Field | Role |
|---|---|
| `daily_mission` | Embedded mission briefing |
| `timeline` | Today's journey steps |
| `current_phase` | Guided session phase |
| `session_status` | Student-facing status label |
| `reflection_available` | Presentation flag |
| `upcoming_transition` | Next presentation step wording |
| `progress_summary` | Concise progress line |
| `session_outcome` | Post-session canonical object (or `None`) |
| `reflection_state` | Available / In Progress / Completed / Skipped (or `None`) |

---

## 4. SessionOutcome lifecycle

`SessionOutcome` is the **canonical presentation object after a study session**.

```
Guided session reaches Wrapping Up / Complete
        │
        ▼
SessionOutcomeAssembler.assemble(DayExperience)
        │
        ├─ mission_title (presentation)
        ├─ completion_status (UI vocabulary only)
        ├─ reflection_available
        ├─ summary_message / next_transition / upcoming_action
        └─ never mastery / readiness / evidence metrics
        │
        ▼
ReflectionAssembler.assemble(SessionOutcome) → ReflectionExperience
```

| Field | Role |
|---|---|
| `mission_title` | Student-facing title |
| `completion_status` | Presentation completion vocabulary |
| `reflection_available` | Whether Guided Reflection may present |
| `summary_message` | Concise post-session wording |
| `next_transition` | Next Experience step wording |
| `upcoming_action` | Short CTA-oriented label |

---

## 5. Guided Reflection flow

Reflection is **for the student**, lightweight, and **optional**. Responses are **not persisted** in this milestone.

### Experience states

```
(none) ──session Complete──► Available ──Start──► In Progress
                                │                      │
                                ├──────── Skip ────────┤
                                │                      │
                                ▼                      ▼
                             Skipped              Completed
                                    \              /
                                     \            /
                                      ▼          ▼
                               Day completion presentation
```

| State | Meaning (Experience only) |
|---|---|
| **Available** | Session finished; Home presents reflection before day completion |
| **In Progress** | Student has begun reflecting (presentation) |
| **Completed** | Student finished reflection (presentation) |
| **Skipped** | Student skipped reflection (presentation) |

Controls (`Start` / `Complete` / `Skip`) via `apply_reflection_control()`:

- No persistence of answers
- No Evidence Platform writes
- No educational authority changes

### Prompts (presentation-only)

Fixed copy from `default_reflection_prompts()`:

1. How did today's session feel? (`choice`)
2. Was today's mission manageable? (`choice`)
3. Would you like to add a note? (`note`)

---

## 6. Guided study session lifecycle

```
Ready ──Start──► Studying ──Finish──► Wrapping Up ──Finish──► Complete
  ▲                  │                                         │
  └──── Resume ──────┘                                         ▼
                                                         Reflection Available
```

| Phase | Meaning (Experience only) |
|---|---|
| **Ready** | Mission available; student has not entered studying presentation |
| **Studying** | Guided focus; one learning objective exposed |
| **Wrapping Up** | Presentation close-out; SessionOutcome assembled |
| **Complete** | Session presentation finished; Guided Reflection unlocks |

Controls (`Start` / `Resume` / `Finish`) update **presentation state only** via `apply_session_control()`.

---

## 7. Transition sequence (single continuous day)

```
Mission briefing
    → Guided Study Session (Ready → Studying → Wrapping Up → Complete)
    → SessionOutcome
    → Guided Reflection (Available → In Progress → Completed | Skipped)
    → Day complete presentation
```

Home remains one surface. After session completion it presents reflection **before** the day's completion state. Educational authority for live mission start remains with existing Home session gate / Runtime A paths.

---

## 8. JourneyEvent model

Immutable Experience transition contracts. They **never** trigger educational recalculation, persistence, or Programme I calls.

| Event type | Typical stage | Meaning |
|---|---|---|
| `mission_started` | `daily_mission` | Student began today's mission (UI) |
| `mission_completed` | `daily_mission` | Student finished today's mission (UI) |
| `reflection_available` | `session_reflection` | Reflection surface is ready |
| `weekly_review_available` | `weekly_review` | Weekly review surface is ready |
| `session_started` | `study_session` | Guided session entered Studying |
| `session_resumed` | `study_session` | Guided session resumed Studying |
| `session_completed` | `study_session` | Guided session reached Complete |
| `wrap_up_started` | `study_session` | Guided session entered Wrapping Up |
| `reflection_started` | `session_reflection` | Guided Reflection entered In Progress |
| `reflection_completed` | `session_reflection` | Guided Reflection reached Completed |
| `reflection_skipped` | `session_reflection` | Guided Reflection skipped |

Helpers include `reflection_started()`, `reflection_completed()`, `reflection_skipped()`, `event_for_reflection_state()`.

---

## 9. Experience ownership

| Layer | Owns | Does not own |
|---|---|---|
| **Experience (Programme II)** | Presentation DTOs, journey transitions, Home wording, reflection UX | Educational truth, recommendations, mastery, evidence writes |
| **Programme I engines** | Runtime A / Twin / Adaptive / Strategy / Evidence authority | Home chrome / journey stage labels |

Guided Reflection is an Experience Layer concern. It does not alter educational authority.

---

## 10. Feature flag behaviour

`ENABLE_UNIFIED_JOURNEY` (env: `KWALITEC_UNIFIED_JOURNEY`) defaults **OFF**.

When OFF:

- Legacy Home / navigation unchanged
- Home continues to use existing recommendation projections (DayExperience / StudySession / Reflection fields blank)
- Composition does not wire `journey_coordinator`

When ON:

- Journey-stage navigation labels
- Home is a continuous day: mission → guided session → optional reflection → day complete
- Guided phases + session / reflection controls render as presentation aids
- Composition wires `JourneyCoordinator`

---

## 11. Contracts

Immutable DTOs (no persistence):

| DTO | Role |
|---|---|
| `JourneyContext` | Stage-level presentation object (P2-MS002) |
| `DailyMission` | Home mission briefing (P2-MS003) |
| `DayExperience` | **Canonical** daily Experience object (P2-MS004/005) |
| `StudySession` | Guided session view model (P2-MS004) |
| `SessionOutcome` | **Canonical** post-session object (P2-MS005) |
| `ReflectionPrompt` / `ReflectionExperience` | Guided Reflection presentation (P2-MS005) |
| `ReflectionState` / `ReflectionControl` | Reflection Experience vocabulary |
| `SessionPhase` / `SessionControl` | Presentation phase / control vocabulary |
| `JourneyEvent` | Experience transition record |
| `ExperienceTimeline` / `TimelineStep` | Today's journey presentation aid |
| `JourneyState` / `NextBestAction` / `JourneyProgress` | Orchestration snapshots |
| `HomePrimaryMission` | Compat Home projection |
| `JourneySubsystemInputs` | Frozen opaque projections |

---

## 12. Extension points for future Evidence integration

| Extension | Guidance |
|---|---|
| **Experience Observation Bridge (P2-MS006)** | Implemented — see `EXPERIENCE_OBSERVATION_ARCHITECTURE.md`. One-way factual `ExperienceObservation` publish via Evidence public intake; flag `ENABLE_EXPERIENCE_OBSERVATION` (default OFF) |
| Evidence writes | Wire optional capture **after** architecture review — keep Experience DTOs as the presentation boundary; do not invent educational meaning in assemblers |
| Persist reflection responses | Add an Evidence / Experience store adapter; `apply_reflection_control` stays pure — persistence belongs outside |
| Soft evidence interpretation | Programme I Evidence / Twin own interpretation — Experience only presents |
| Adaptive workflow from reflection | **Stop** — await architecture review |
| Notifications / analytics | Explicitly out of scope |

---

## 13. Tests

| Suite | Path |
|---|---|
| Contract tests | `tests/application/unified_journey/test_contracts.py` |
| JourneyContext assembler | `tests/application/unified_journey/test_assembler.py` |
| DailyMission assembler | `tests/application/unified_journey/test_daily_mission.py` |
| DayExperience assembler | `tests/application/unified_journey/test_day_experience.py` |
| StudySession assembler | `tests/application/unified_journey/test_study_session.py` |
| SessionOutcome assembler | `tests/application/unified_journey/test_session_outcome.py` |
| Reflection prompts / assembler | `tests/application/unified_journey/test_reflection.py` |
| Reflection controls / states | `tests/application/unified_journey/test_reflection_controls.py` |
| Session controls / phases | `tests/application/unified_journey/test_session_controls.py` |
| JourneyEvent contracts | `tests/application/unified_journey/test_events.py` |
| Experience Timeline | `tests/application/unified_journey/test_timeline.py` |
| Coordinator unit tests | `tests/application/unified_journey/test_coordinator.py` |
| Home integration | `tests/application/unified_journey/test_home_integration.py` |
| Navigation integration | `tests/application/unified_journey/test_navigation.py` |
| Feature flag isolation | `tests/application/unified_journey/test_feature_flags.py` |

---

## 14. Stop condition

Stop after the Guided Reflection Experience.

Await architecture review before integrating Reflection with the Learning Evidence Platform.
