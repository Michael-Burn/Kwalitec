# RI-001 — Educational Runtime Integration Architecture

**Programme:** RI-001 — Educational Runtime Integration (Preferred Authority)  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/application/runtime_integration/`  
**Depends on:** [EI-007](../../educational_intelligence/ei007_educational_reasoning_engine/ARCHITECTURE.md) · [EX-001](../../educational_experience/ex001_educational_experience_engine/ARCHITECTURE.md) · [EI-004 SCI](../../educational_intelligence/ei004_student_curriculum_binding/)

---

## 1. Capability statement

> Kwalitec's runtime preferentially delivers educational intelligence through a single authoritative pipeline while maintaining safe compatibility for unmigrated students.

---

## 2. Preferred authority philosophy

Educational Intelligence is the **preferred** educational authority whenever prerequisites exist:

```
Published Curriculum → SCI → Evidence → Twin Beliefs → EI-007 Decisions
        → EX-001 Experience Models → Surface adapters → UI
```

Runtime A (`RecommendationService`, Planning educational selection, PX-001 Runtime C) is **Temporary compatibility** only:

- Used only when no active SCI or no persisted Educational Decisions exist (or when `ENABLE_RUNTIME_INTEGRATION` is explicitly off)
- No new educational features may depend on it
- No new educational logic may be added to it
- Every fallback invocation is telemetered for RI-005 readiness

When SCI + decisions exist, Runtime A must never determine educational recommendations.

---

## 3. RuntimeIntegrationService

Orchestration only — **no educational reasoning**.

| Responsibility | Mechanism |
|----------------|-----------|
| Detect active SCI | `resolve_active_instance` (subject preference, else lowest id) |
| Detect decisions | `DecisionQueryService.highest_value_actions` (read-only) |
| Present experiences | `ExperienceTransformationService.present_decision_view` |
| Fallback | Injected Runtime A callable + telemetry |
| Peek without metrics | `has_educational_intelligence` (Runtime C fork) |

Flag: `ENABLE_RUNTIME_INTEGRATION` / `KWALITEC_RUNTIME_INTEGRATION` — **default ON**; set `0`/`false`/`off` to force compatibility.

---

## 4. Adapter architecture

| Adapter | Experience model | Consumer role |
|---------|------------------|---------------|
| Dashboard | `DashboardPriorityCard` | Home / Dashboard recommendation dicts |
| Mission | `DailyMissionExperience` | Mission framing / why overlay |
| Coach | `CoachConversationContext` | Tutor context metadata |
| Revision | `RevisionPlannerEntry` | Revision planner entries |
| Session | `StudySessionBriefing` | Session why / learning objective |

Adapters perform presentation mapping only. They must not re-rank, invent topics, or call Runtime A.

---

## 5. Runtime dependency graph

```
HTTP / blueprints / templates
        ↓ (no educational reasoning)
RuntimeIntegrationService
        ├─(SCI + decisions)→ DecisionQueryService → EX-001 → Surface adapters
        └─(else)→ Runtime A Temporary compatibility + Fallback telemetry
```

Wired consumers:

- Recommendation Bridge (`RecommendationAdapter`) — Home EducationalState path
- Legacy Dashboard (`dashboard/routes.py`)
- Mission / Session framing (`mission/routes.py`)
- Intelligent Tutor context metadata
- Student Home Runtime C fork — defers to Preferred Authority when available

---

## 6. Fallback lifecycle

| Reason | Missing prerequisite |
|--------|----------------------|
| `runtime_integration_disabled` | `ENABLE_RUNTIME_INTEGRATION` |
| `no_active_sci` | Active Student Curriculum Instance |
| `no_educational_decisions` | `ere_educational_decisions` rows |
| `subject_unresolved` | Subject hint (rare) |

Aggregation API (`RuntimeIntegrationTelemetry`):

- `fallback_rate()`
- `migrated_user_count()`
- `educational_intelligence_adoption_pct()`

These metrics determine **RI-005** readiness for hard removal of Runtime A recommendation authority.

---

## 7. Runtime A removal strategy

| Phase | Action |
|-------|--------|
| RI-001 (this programme) | Preferred Authority + Temporary compatibility + telemetry |
| Later SCI enrolment programmes | Bind students → evaluate EI-007 → drive adoption % up |
| RI-005 | Remove Runtime A recommendation authority when fallback rate → 0 for migrated cohort |

Mission ORM persistence (`PlanningService` / `MissionService`) may remain longer than recommendation authority — persistence is not educational selection.

---

## 8. Runtime C / PX-001 constraints

Runtime C is a Temporary compatibility consumer. RI-001 does not add educational logic to PX-001 packages. When Preferred Authority is available, Home/Journey skip the Runtime C educational page fork so Experience Models win via the Student Experience / Recommendation Bridge path.

---

## 9. Explicit non-goals

- Modifying EI-007 reasoning, Twin beliefs, Learning Evidence, or CKG
- Deleting `RecommendationService` / `PlanningService` in this programme
- Re-reasoning on student read paths (`evaluate_*` from RIS)
- Parallel recommendation engines
- Controllers performing educational ranking

---

## 10. Audit artefact

Full surface/engine classification: [`RUNTIME_AUDIT.md`](RUNTIME_AUDIT.md).
