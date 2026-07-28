# VP-001 Architecture — Version 1 Product Wiring

**Programme:** VP-001 — Version 1 Product Completion  
**Date:** 2026-07-28

---

## 1. Intent

Complete the Version 1 student product by **consuming** the Educational
Intelligence Platform. No new educational architecture; no parallel
recommendation engines; no presentation-layer reasoning.

---

## 2. Write path (LP-001 hooks)

```
Study Plan Wizard / Enrolment Bridge
        │
        ▼
onboard_after_enrolment()          # infrastructure adapter
        │
        ▼
LearnerLifecycleOrchestrator.onboard_student
        │
        ├── EI-004 create SCI + node state
        ├── EI-006 initial beliefs
        ├── EI-007 initial decisions
        └── EX-001 experience models
```

```
Session answer / Session complete
        │
        ▼
record_session_evidence()          # infrastructure adapter
        │
        ▼
LearnerLifecycleOrchestrator.process_evidence
        │
        ├── EI-005 record evidence
        ├── EI-006 rebuild beliefs
        ├── EI-007 regenerate decisions
        └── EX-001 regenerate experience
```

Both hooks are **fail-open**: missing published edition or SCI never blocks
enrolment or session UX.

---

## 3. Read path (RI-001 Preferred Authority)

| Surface | IntegrationSurface | Adapter |
|---------|--------------------|---------|
| Home / Recommendation | `RECOMMENDATION` / dashboard | RecommendationAdapter |
| Daily Mission framing | `DAILY_MISSION` | `map_daily_mission` |
| Study Session overview | `STUDY_SESSION` | `map_session_briefing` |
| Revision Planner | `REVISION_PLANNER` | `map_revision_entry` |
| Coach | `COACH` | `map_coach_context` |

Controllers / services call `RuntimeIntegrationService.resolve_for_surface`.
They never import EI-007 rule engines.

---

## 4. Module map

| Module | Role |
|--------|------|
| `app/infrastructure/adapters/learner_lifecycle/` | Enrolment + evidence hooks |
| `app/application/platform_integration/enrolment_bridge.py` | Calls onboard after enrol |
| `app/study_plan/routes.py` | Calls onboard after Runtime A wizard |
| `app/application/student_experience/revision_service.py` | RIS-first revision |
| `app/presentation/session/views.py` | Session briefing + evidence |

---

## 5. Invariants preserved

- Curriculum V1/V2 loaders untouched  
- EI-007 / Twin / EX-001 cores untouched  
- Runtime Integration remains sole Preferred Authority read router  
- Runtime A Temporary compatibility retained  
- No secrets / new dependencies  

---

**End of Architecture**
