# Authoritative Student Intelligence Surface Architecture — Post EP-002

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Authority:** Binding baseline for all future architectural work on Runtime A student intelligence surfaces  
**Status:** Authoritative

This document answers: **What is the authoritative Student Intelligence Surface architecture after EP-002?**

---

## 1. One-sentence baseline

The student’s explainable daily intelligence surface is the Twin-gated EP-001 consumer chain — Foundation → Planner → Readiness → Insight — projected onto Runtime A HTTP through Consumer Chain dual-run / cutover gates and a single Runtime A presentation facade, with legacy Runtime A services remaining the fail-open authority under production defaults.

---

## 2. Constitutional chain (unchanged ownership)

```
Curriculum Engine (syllabus order)
        ↓
Runtime A writes / facts (SQL + services)     ← sole educational write authority
        ↓
MS-004 collectors → TwinRuntimeEvidence
        ↓
EP-001.1 CanonicalLearnerState (Foundation)   ← learner-state read model
        ↓
   ┌────┴────┬────────────┐
   ↓         ↓            ↓
EP-001.2   EP-001.3     (inputs)
Planner    Readiness
   ↓         ↓
   └────┬────┘
        ↓
     EP-001.4 Insight                         ← communication only
        ↓
Consumer Chain (observe / dual-run / cutover) ← orchestration / gates only
        ↓
RuntimeAPresentationAdapter                   ← presentation selection only
        ↓
Runtime A templates (Dashboard / Analytics / Mission)
```

**Hard rules**

1. Twin packages must not import planner / readiness / insight for authority.  
2. Insight must not invent readiness or plans when Twin is OFF (limitation codes only).  
3. Do not wrap `get_overall_readiness` with Foundation (collector recursion).  
4. Do not delete legacy HTTP paths before dual-run / cutover proof (legacy retained as fail-open).  
5. Do not introduce a fourth Twin stack for UX.  
6. Presentation must not invent evaluation or planning.

---

## 3. Surface map (post EP-002)

| Student concern | Twin-gated API | HTTP cutover gate | Legacy fail-open | Presentation |
|---|---|---|---|---|
| Today’s guidance (focus / risk / next / why) | `build_study_insights` | `KWALITEC_STUDY_INSIGHTS_CUTOVER` | `generate_recommendations` | Adapter pass-through (Twin) / EIP-003 enrich (legacy) |
| Readiness context | `build_readiness_intelligence` | `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | `get_overall_readiness` (+ surface getters) | Twin → `ReadinessNarrative` / legacy EIP-003 |
| Today’s mission / plan display | `build_daily_study_plan` | `KWALITEC_DAILY_PLAN_CUTOVER` | `generate_today_mission` (ORM persistence authority) | Twin → `MissionNarrative` / legacy EIP-003 |
| Experience TwinPort UX | Foundation Authority port | `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ExperienceTwinAdapter` | Out of Runtime A presentation facade scope |

**Production default:** all Twin / Authority / Cutover flags **OFF** → legacy Runtime A is student-visible authority.  
**Production hard gate:** all three HTTP cutovers are ineligible when `APP_ENV` / `FLASK_ENV` is `production` / `prod`, regardless of cutover flag values.

---

## 4. Ownership matrix (binding)

| Concern | Canonical owner | Must not |
|---|---|---|
| Curriculum / syllabus structure | Curriculum Engine + `CurriculumService` | Duplicate topic ordering in cutover / presentation |
| Educational facts / writes | Runtime A SQL + services | Twin / Insight / bridges writing educational state |
| Learner-state read model | MS-004 + EP-001.1 Foundation | Invent mastery; promote Epic / V2 / EOS Twin |
| Daily plan slots / workload | `PlanningService` + EP-001.2 | Insight or HTTP inventing plans; MissionOptimizer as second authority |
| Mission ORM persistence | `PlanningService.generate_today_mission` | Twin writing missions |
| Readiness score / drivers | `ReadinessService` + EP-001.3 | Intelligence wrapping legacy getters used by collectors |
| Student guidance copy (Twin path) | `RecommendationService` + EP-001.4 | Inventing evaluation or planning |
| Consumer-chain orchestration | `consumer_chain` adapters | Owning planning / readiness / insight maths |
| Presentation selection | `RuntimeAPresentationAdapter` | Becoming a third narrator or evaluation owner |
| Legacy presentation adapter | `EducationalExplainabilityService` (Outcome B) | Competing as peer SoT on Twin-served Runtime A concerns |
| Experience StudentTwinPort | `ExperienceTwinAdapter` (default) / Foundation Authority (gated) | Demo-seed theatre when Authority ON |

---

## 5. Twin stack quarantine (binding)

| Stack | Authoritative for Runtime A product? |
|---|---|
| MS-004 + EP-001.1 Foundation | **Yes** — extend this |
| ExperienceTwinAdapter | Default Experience UX until Authority soak + product decision |
| Foundation Authority port | Gated Experience TwinPort only |
| Epic / V2 / EOS Twin | **No** — reference / isolated; do not promote |

Full narrative: [`../TWIN_STACK_QUARANTINE.md`](../TWIN_STACK_QUARANTINE.md).

---

## 6. Feature-flag posture (code truth)

| Env var | Resolved field | Default | Role |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | Twin DI, Foundation, Shadow, Adaptive TwinInput, `build_*` availability |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF (requires Twin) | Experience TwinPort → Foundation |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | `ENABLE_STUDY_INSIGHTS_CUTOVER` | OFF (requires Twin) | Dashboard/home Insight cutover |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | `ENABLE_READINESS_INTELLIGENCE_CUTOVER` | OFF (requires Twin) | Dashboard/analytics readiness cutover |
| `KWALITEC_DAILY_PLAN_CUTOVER` | `ENABLE_DAILY_PLAN_CUTOVER` | OFF (requires Twin) | Dashboard/missions daily-plan display cutover |

Shadow Validation and Adaptive TwinInput remain **bundled under Twin ON** (no separate env flags).

---

## 7. Rollback model (authoritative)

| Intent | Action | Effect |
|---|---|---|
| Surface rollback | Cutover flag OFF + process restart | Legacy payload / narrative for that surface |
| Global Twin kill | `KWALITEC_DIGITAL_TWIN=0` | `build_*` → `None`; cutovers ineligible; Foundation DI absent |
| Authority rollback | `KWALITEC_DIGITAL_TWIN_AUTHORITY=0` | ExperienceTwinAdapter restored |
| Schema / data | Not required | No EP-002 Alembic; Twin is non-persistent |

---

## 8. What EP-002 completed vs deferred

### Completed (programme scope)

- Consumer-chain observability for all three `build_*` APIs  
- Shared Foundation / CLS DI across Planner → Readiness → Insight  
- MissionOptimizer soft-deprecate / quarantine  
- Non-production Twin + Authority soak harness + rollback verification  
- Study Insights dual-run → gated HTTP cutover  
- Readiness Intelligence dual-run → gated HTTP cutover  
- Daily Plan / mission dual-run → gated HTTP cutover (display projection; ORM remains legacy)  
- Runtime A presentation consolidation behind `RuntimeAPresentationAdapter`  
- Programme constitutional certification and this baseline  

### Explicitly deferred (not part of “architecture done”)

- Live staging soak evidence pack with real learner traffic (ops gate for pilot expansion)  
- Production-wide cutover activation  
- Twin Ready (T7) / MS-004 complete  
- Experience `/student` narrator consolidation under `SOLE_RUNTIME`  
- EI Stage A card narrator retirement (`TD-CO-02`)  
- MissionOptimizer hard-delete  
- Durable (non-process-local) cutover / dual-run metrics  
- Product effectiveness validation of guidance  

---

## 9. Successor constraint

Any future programme that changes student-visible intelligence must:

1. Cite this baseline as the starting architecture.  
2. Preserve the ownership matrix in §4 unless a superseding ADR + constitutional review says otherwise.  
3. Treat production Twin / Authority / Cutover ON as a separate go/no-go with staging evidence — not implied by EP-002 completion.  
4. Not declare Twin Ready (T7) from EP-002 exit alone.

---

## 10. Certification statement

**Certified:** The architecture described herein is the authoritative post-EP-002 Student Intelligence Surface baseline.

**Not certified by this document:** Twin Ready (T7), production GA, educational effectiveness of recommendations.
