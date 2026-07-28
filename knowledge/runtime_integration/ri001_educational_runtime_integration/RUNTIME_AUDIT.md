# RI-001 Runtime Audit — Educational Decision Paths

**Programme:** RI-001 — Educational Runtime Integration (Preferred Authority)  
**Date:** 2026-07-28  
**Status:** Complete (audit artefact)

---

## 1. Purpose

Inventory every educational recommendation / prioritisation / mission-framing /
coach-context path in the live runtime. Classify each for Preferred Authority
migration. Detail always yields to this audit for RI-001 scope; later programmes
(RI-005+) own hard removal of Temporary compatibility.

---

## 2. Preferred authority target

```
Published Curriculum → SCI → Evidence → Twin Beliefs → EI-007 Decisions
        → EX-001 Experience Models → Surface adapters → UI
```

When an active SCI has persisted Educational Decisions, Runtime A must not
determine recommendations. Otherwise Runtime A remains Temporary compatibility.

---

## 3. Classification legend

| Class | Meaning |
|-------|---------|
| **Preferred authority** | EI-007 + EX-001 — keep and consume |
| **Adapt** | Wire to RIS / Experience Models; keep module shell |
| **Replace** | Selection logic superseded by EI-007; retire over time |
| **Remove** | Quarantined / no production callers — do not rewire |
| **Temporary compatibility** | Runtime A / PX-001 fallback until migration complete |

---

## 4. Surface inventory

| Surface | Authority today | RI-001 class | RI-001 status |
|---------|-----------------|--------------|---------------|
| Student Home (`/student`) | Runtime A via Recommendation Bridge / EducationalState; Runtime C fork when enrolled | Adapt + Temporary compatibility | RIS preferred via RecommendationAdapter |
| Legacy Dashboard (`/dashboard`) | Stage A orchestrator (flag) or `RecommendationService` | Adapt + Temporary compatibility | RIS preferred for recommendation card/lists |
| Daily Mission (`/missions`) | `PlanningService` / MissionService | Temporary compatibility (persistence); Adapt (copy) | RIS mission adapter for framing when EI available |
| Coach / Intelligent Tutor | AP-002 TutorExplanation / Twin context | Adapt | RIS coach adapter attached to context when EI available |
| Revision Planner | Adaptive / Runtime A revision lists | Adapt + Temporary compatibility | RIS revision adapter when EI available |
| Study Session | Mission + explainability narratives | Adapt + Temporary compatibility | RIS session adapter when EI available |
| Progress widgets | `ReadinessService` / CurriculumService (read models) | Temporary compatibility | Unchanged — not recommendation authority |
| Recommendation endpoints / bridge | `RecommendationService.generate_recommendations` | Temporary compatibility | RIS-first inside RecommendationAdapter |

---

## 5. Engine inventory

| Component | Path | Class |
|-----------|------|-------|
| EI-007 Educational Reasoning Engine | `app/domain/educational_reasoning_engine/` | Preferred authority |
| EX-001 Educational Experience Engine | `app/application/educational_experience_engine/` | Preferred authority |
| RuntimeIntegrationService | `app/application/runtime_integration/` | Preferred routing (orchestration only) |
| `RecommendationService` | `app/services/recommendation_service.py` | Temporary compatibility |
| Recommendation Bridge | `app/infrastructure/adapters/educational_runtime_bridge/recommendation_adapter.py` | Adapt (RIS-first) |
| `PlanningService` educational slots | `app/services/planning_service.py` | Temporary compatibility |
| Stage A `DecisionEngine` / Orchestrator | `app/domain/decision/`, `app/application/orchestration/` | Replace (selection) / Adapt (dashboard composer) |
| `MissionOptimizer` | `app/services/mission_optimizer.py` | Remove (quarantined) |
| AdaptiveLearningService / ReadinessService | `app/services/` | Temporary compatibility (inputs / read models) |
| SDT-002 `educational_reasoning` | `app/domain/educational_reasoning/` | Replace over time (distinct from EI-007) |
| AP-002 DecisionGenerator | `app/application/reasoning/decisions/` | Temporary compatibility (evidence→twin path) |
| Runtime C / PX-001 | `app/application/educational_experience/`, `educational_runtime_engine/` | Temporary compatibility consumer |
| EOS `src/` recommendation engines | `src/domain/education/recommendation_engine/` | Remove / out-of-scope for Runtime A |

---

## 6. Replacement strategy summary

1. **Read path:** Controllers → `RuntimeIntegrationService` → EX-001 adapters when SCI+decisions exist.  
2. **Fallback:** Injected Runtime A callables only when prerequisites missing; every invocation telemetered.  
3. **Persistence:** Mission ORM create/complete stays on PlanningService/MissionService until a later mission-persistence programme.  
4. **No new Runtime A features:** Compatibility infrastructure only.  
5. **Hard removal of Runtime A recommendation authority:** Deferred to RI-005 readiness (fallback rate → 0 for migrated cohort).

---

## 7. Missing prerequisites (fallback reasons)

| Reason code | Meaning |
|-------------|---------|
| `runtime_integration_disabled` | `ENABLE_RUNTIME_INTEGRATION` off |
| `no_active_sci` | No active Student Curriculum Instance |
| `no_educational_decisions` | Active SCI but empty EI-007 decision set |
| `subject_unresolved` | Could not resolve subject for SCI lookup (rare; uses any active SCI when subject missing) |

---

**End of Runtime Audit**
