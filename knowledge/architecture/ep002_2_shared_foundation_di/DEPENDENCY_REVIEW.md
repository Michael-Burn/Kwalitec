# EP-002.2 — Dependency Review

**Milestone:** EP-002.2  
**Review area:** Foundation DI dependency integrity  
**Date:** 2026-07-26  
**Based on:** [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md)

Legend: **O** · **E** · **C** · **R**

---

## 1. Intended dependency direction (unchanged)

```
Curriculum Engine
        ↓
Runtime A writes / facts
        ↓
MS-004 collectors → TwinRuntimeEvidence
        ↓
EP-001.1 CanonicalLearnerState (Foundation.assemble)
        ↓
   ┌────┴────┬────────────┐
   ↓         ↓            ↓
EP-001.2   EP-001.3     Insight inputs
Planner    Readiness
   ↓         ↓
   └────┬────┘
        ↓
     EP-001.4 Insight
```

**C:** EP-002.2 must not reverse Twin ownership or introduce cycles.

---

## 2. Current Runtime A resolve edges

| From | To | Edge type |
|---|---|---|
| Planning / Readiness / Recommendation `_resolve_twin_foundation` | `build_student_digital_twin_foundation` + `v2_flags` | Lazy construct |
| Readiness → Planning | `build_daily_study_plan(foundation=…)` | Nested compose |
| Insight → Planning | `build_daily_study_plan(foundation=…)` | Nested compose |
| Insight → Readiness | `build_readiness_intelligence(foundation=…, daily_plan=…)` | Nested compose |
| Experience composition | Shared Foundation for Authority | Separate DI root |

**O:** Nested edges already forward Foundation.  
**E:** Service source.  
**C:** Add forward of assembled CLS on the same edges; keep lazy imports.

---

## 3. Proposed DI edges (EP-002.2)

```
consumer_chain.foundation_di
  ├─ resolve_enabled_twin_foundation()     ← single Twin-ON resolve
  └─ assemble_shared_canonical_state()     ← inject-or-assemble + telemetry
           │
           ▼
Planning / Readiness / Recommendation build_* bodies
  (accept foundation= and canonical_state=)
```

| Check | Requirement |
|---|---|
| Twin packages import services? | **Forbidden** |
| Services import consumer_chain DI? | **Allowed** (ops/DI helper; EP-002.1 pattern) |
| Circular imports | Avoid — keep resolve lazy inside methods |
| Process-global Foundation | **Forbidden** |
| Process-global CLS cache | **Forbidden** |

---

## 4. MissionOptimizer dependency posture

```
MissionOptimizer.generate_balanced_mission
  ├─ (Twin ON) PlanningService.build_daily_study_plan  → Foundation assemble
  └─ (Twin OFF) AdaptiveLearningService / CurriculumService
```

**O:** No inbound production edges.  
**E:** Grep across `app/` finds definition only.  
**C:** Dependency is orphaned outbound only — safe to deprecate without breaking HTTP.

**R:** Do not add new production callers. Do not absorb into HTTP in this milestone.

---

## 5. Collector recursion invariant

**O:** Foundation assemble → collectors → `ReadinessService.get_overall_readiness` (legacy).  
**E:** EP-001.5 Dependency Review §3.  
**C:** Sharing CLS reduces how often that chain runs during Insight composition — good. Must still never wrap `get_overall_readiness` with Foundation.

---

## 6. Verdict

| Criterion | Result |
|---|---|
| Dependency direction intact after DI | **Yes (design)** |
| Circular risk | **Low** if helpers stay in `consumer_chain` |
| Ownership violation risk | **None** if CLS is pass-through only |
| Global state risk | **Avoided** by composition-local kwargs |
| MissionOptimizer wiring risk | **Avoided** by deprecate/quarantine decision |
