# PI-001C — Educational Runtime Engine Architecture

**Programme:** PI-001C — Educational Runtime Engine  
**Status:** Authoritative for this milestone  
**Date:** 2026-07-27  

---

## 1. Purpose

Execute PI-001B derived educational artefacts for real students. The runtime
instantiates templates from the **published curriculum**, records immutable
educational events, and derives progress / journey / readiness inputs without
recreating subject-specific educational logic.

---

## 2. Authority chain

```text
PublishedCurriculumPackage (PI-001A SSOT)
        │
        ▼
EducationalEngineFoundationService (PI-001B)
  → study plan template
  → mission templates
  → journey structure
  → progress model
        │
        ▼
EducationalRuntimeEngineService (PI-001C)
  → enrol student
  → instantiate study plan instance
  → generate daily mission instance
  → complete mission → append events
  → derive progress / journey
  → project Readiness + Estimated Knowledge inputs
```

JSON Runtime A (`StudyPlanService` / `PlanningService` / `TopicProgress`) remains
the live default for bundled exams. PI-001C is additive and coexistence-safe.

---

## 3. Layering

| Layer | Package | Responsibility |
|---|---|---|
| Domain | `app/domain/educational_runtime_engine/` | Event types, state transitions, pure progress derivation |
| Application | `app/application/educational_runtime_engine/` | Orchestration, coexistence policy, DTOs |
| Models | `app/models/educational_runtime_engine.py` | Enrolment, plan/mission instances, append-only events |
| Existing | `app/services/` | Untouched JSON runtime until cutover evidence |

---

## 4. What is stored vs derived

### Stored (cannot be re-derived)

| Fact | Table |
|---|---|
| Student enrolment against a published identity | `runtime_enrolments` |
| Study-plan instance pointer + reconciled current topic | `runtime_study_plan_instances` |
| Daily mission instance (template binding + date) | `runtime_mission_instances` |
| Immutable educational events | `runtime_educational_events` |

### Derived (never a competing SSOT)

| Projection | Source |
|---|---|
| Completed topics / coverage | `TOPIC_COMPLETED` events + progress model |
| Current journey topic / stage | derived progress |
| Next mission template | current topic + mission templates |
| Readiness coverage inputs | derived progress |
| Estimated Knowledge placeholders | derived progress + evidence policy |

Curriculum titles, minutes, prerequisites, and mission task text remain in the
immutable published package / PI-001B artefacts — not re-authored in runtime rows.

---

## 5. Design decisions

1. **Published curriculum remains SSOT** — runtime never invents topics.
2. **Templates are instantiated, not rewritten** — mission titles/tasks come from derived templates.
3. **Events are append-only** — completion history is immutable.
4. **Mission completion ≠ Estimated Knowledge** — study progress only; EK still requires structured question evidence.
5. **Coexistence first** — JSON Runtime A unchanged; curriculum runtime activates only for founder-published subjects with an active package.

---

## 6. Explicit non-goals (this milestone)

- Cutover of existing CS1/JSON students onto published packages
- Rewriting `ReadinessService` / `AdaptiveLearningService` internals
- Twin / Daily Plan authority changes
- Student UI / wizard cutover to founder-published subjects
- Minting Estimated Knowledge from mission completion alone
