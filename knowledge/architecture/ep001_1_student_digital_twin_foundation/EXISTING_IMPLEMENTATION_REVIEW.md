# EP-001.1 — Existing Implementation Review

**Milestone:** EP-001.1 — Student Digital Twin Foundation  
**Phase:** 2 — Existing Implementation Review

---

## Legend

| Status | Meaning |
|---|---|
| **Already Implemented** | Production-usable for that concern |
| **Partially Implemented** | Model / tests / wiring exist; not sole authority or incomplete coverage |
| **Missing** | No meaningful production path |

---

## Review matrix

| Concern | Status | Location / notes |
|---|---|---|
| Existing student state (ORM) | **Already Implemented** | `TopicProgress`, `StudyAttempt`, `Mission`, `StudyPlan` |
| Duplicated Twin stacks | **Partially Implemented** (risk) | Epic Twin + V2 student_twin + EOS + MS-004 + Experience demo projections |
| Progress tracking | **Already Implemented** | `TopicProgress` + lifecycle services |
| Performance tracking | **Already Implemented** | `StudyAttempt` accuracy; `TopicProgress.average_accuracy` |
| Learning evidence sources | **Partially Implemented** | Production writes attempts; domain Evidence + Twin pipeline exist but are not sole write path |
| Mission data | **Already Implemented** | `Mission` / `MissionTask` + MissionService |
| Dashboard dependencies | **Partially Implemented** | Mix of TwinProvider, ReadinessService, AnalyticsService, Experience ports |
| Analytics dependencies | **Already Implemented** (SQL-direct) | `AnalyticsService` reads ORM — not Twin-backed |
| Existing Twin APIs | **Partially Implemented** | No dedicated `/twin` REST; Experience via `StudentTwinPort` |
| Twin database tables | **Already Implemented** | `twin_snapshots`; EOS `eos_digital_twins` |
| MS-004 facet synthesis | **Already Implemented** (flag OFF) | Consistency, rhythm, habits, etc. from Runtime A |
| MS-004 Experience projection | **Already Implemented** (additive DI) | Does not cut over UX |
| Twin Authority flag | **Missing** (documented only) | `KWALITEC_DIGITAL_TWIN_AUTHORITY` in architecture docs; not in `v2_flags.py` |
| Canonical foundation read model | **Missing** | No single DTO exposing mastery + progress + evidence + streaks + missions together |
| Streaks in Twin | **Missing** | Computed in `ReadinessService`; not in Twin aggregate / foundation |
| Mock performance distinction | **Missing** | No mock-typed ORM; attempts are undifferentiated practice |
| Demo Twin theatre | **Already Implemented** (problem) | `ExperienceTwinAdapter` + `seeded_demo_twin` can surface non-Runtime-A state |

---

## Already Implemented (keep)

- Runtime A collectors feeding Twin / Adaptive
- Epic Twin domain + update strategies + repository
- MS-004 T0–T6 observational pipeline
- Feature flag `KWALITEC_DIGITAL_TWIN`

## Partially Implemented (extend)

- Experience TwinPort (needs Runtime-A-grounded authority path)
- Twin as consumer-facing learner-state SoT (architecture yes; wiring no)
- Evidence → Twin update loop (exists; not sole production path)

## Missing (Foundation scope)

- `CanonicalLearnerState` foundation contract
- Streak / mastery / progress / mission pass-through packaging for Twin consumers
- `ENABLE_DIGITAL_TWIN_AUTHORITY` implementation
- Consolidation documentation forbidding a fourth Twin stack
