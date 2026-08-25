# EX-001 — Educational Experience Engine Architecture

**Programme:** EX-001 — Educational Experience Engine  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/educational_experience_engine/` · `app/application/educational_experience_engine/`  
**Depends on:** [EI-007 Educational Reasoning Engine](../../educational_intelligence/ei007_educational_reasoning_engine/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can communicate its educational intelligence consistently across the entire student experience.

Given an Educational Decision from EI-007, Kwalitec deterministically produces consistent, explainable, UI-independent experience models for Daily Mission, AI Coach, Dashboard, Revision Planner, and study session surfaces. The Experience Engine never decides what a student should study.

---

## 2. Experience Engine philosophy

| Principle | Meaning |
|-----------|---------|
| 1. Presentation ≠ reasoning | The engine communicates Educational Decisions; it never creates or re-ranks them. |
| 2. Consistency | The same decision yields aligned experiences across all student-facing surfaces. |
| 3. Separation | Wording, layout, and UX changes must never alter educational decisions. |
| 4. Explainability | Every experience preserves what / why / curriculum area / outcome / effort. |
| 5. UI-agnostic core | `ExperienceModel` is the canonical presentation object — surfaces project from it. |
| 6. Determinism | Same decision + presentation version → identical experience models. |
| 7. No generative AI | Fixed presentation catalogues only — no probabilistic LLM copy in the core path. |

```
Educational Decisions (EI-007)
        ↓
Experience Engine (EX-001)
        ↓
Experience Models (UI-agnostic)
        ↓
Surface projections (Mission / Coach / Dashboard / Revision / Session)
        ↓
Student Interfaces (consumers via contracts)
```

Package naming note: EX-001 lives under `educational_experience_engine` to remain distinct from PX-001 `app.application.educational_experience` (Runtime C snapshots) and EXP-001 `student_experience` packages.

---

## 3. Transformation pipeline

1. **Consume** — Accept an `EducationalDecision` (or EI-007 `DecisionView`) read-only.  
2. **Present** — `EducationalExperienceEngine.present` builds the canonical `ExperienceModel` using deterministic catalogues (`eee.v1.1`).  
3. **Project** — Surface helpers derive Daily Mission, Coach, Dashboard, Revision Planner, and Session briefing models from the same `ExperienceModel`.  
4. **Serve** — `ExperienceTransformationService` exposes the ExperienceEnginePort contract for orchestrators and future UI adapters.  
5. **Explain** — `explainable_presentation` returns a compact what/why/curriculum/outcome/effort payload with full decision trace.

Decisions are never written, deleted, or re-ranked by EX-001. Portfolio queries read persisted decisions via `DecisionQueryService` only.

---

## 4. Experience domain model

Canonical `ExperienceModel` fields:

| Field | Role |
|-------|------|
| `title` | Student-facing recommendation headline |
| `summary` | Short description of the recommended action |
| `educational_rationale` | Why — student-facing catalogue from decision type + area (never EI-007 `rationale_summary`) |
| `estimated_effort` | Minutes + human label |
| `expected_outcome` | Student-readable learning outcome |
| `urgency` | Presentation urgency band derived from priority/type |
| `prerequisite_explanation` | Prerequisite context in plain language |
| `motivational_framing` | Encouragement that does not change the action |
| `next_steps` | Ordered actionable steps for the surface |
| `curriculum_area` | Human curriculum area label |
| `trace` | Decision id, type, target, beliefs, evidence, rules, priority, rank |
| `experience_version` | Presentation pack id (`eee.v1.1`) |

Surface models (`DailyMissionExperience`, `CoachConversationContext`, `DashboardPriorityCard`, `RevisionPlannerEntry`, `StudySessionBriefing`) are projections of the same ExperienceModel.

---

## 5. Consumer contracts

Runtime integration contracts live in `app/application/educational_experience_engine/contracts.py`:

| Contract | Consumer |
|----------|----------|
| `ExperienceModelConsumer` | Any surface binding a canonical ExperienceModel |
| `DailyMissionExperiencePort` | Daily Mission presentation |
| `CoachExperiencePort` | AI Coach conversation grounding |
| `DashboardExperiencePort` | Dashboard priority cards |
| `RevisionPlannerExperiencePort` | Revision Planner entries |
| `StudySessionExperiencePort` | Study session briefings |
| `ExperienceEnginePort` | Full orchestrator / adapter contract |

**Invariant:** Controllers and templates must call these contracts (or `ExperienceTransformationService`). They must not duplicate educational ranking, prerequisite logic, or decision generation.

---

## 6. Presentation invariants

1. Student-facing educational rationale comes from EX-001 presentation catalogues keyed by decision type and curriculum area — EI-007 `rationale_summary` remains internal audit text and is never copied into experience outputs.  
2. Curriculum target and supporting belief / evidence / rule ids remain in `ExperienceTrace`.  
3. Urgency and motivational framing are presentation signals only — they do not mutate priority.  
4. All surfaces for one decision share the same `decision_id`, title family, and why text.  
5. Changing catalogue wording bumps `EXPERIENCE_VERSION`; it must not change EI-007 decisions.  
6. No Flask request/session coupling in experience services.

---

## 7. Separation from Educational Reasoning

| Concern | Owner |
|---------|-------|
| What to study next | EI-007 Educational Reasoning Engine |
| Why (educational) | EX-001 presentation catalogues (decision type + area); EI-007 rationale stays internal |
| Priority / rank | EI-007 prioritisation |
| How to say it | EX-001 presentation catalogues |
| How to shape per surface | EX-001 surface projections |
| Twin beliefs / evidence | EI-006 / EI-005 (untouched) |

EX-001 **must not**:

- modify Educational Decisions  
- modify Twin Beliefs or Learning Evidence  
- introduce new educational reasoning  
- bypass the Educational Reasoning Engine  

---

## 8. Explicit non-goals

- HTTP route / template wiring for student surfaces  
- Persisting experience models (regenerable from decisions)  
- Mission instance creation or Coach LLM responses  
- Mutating `ere_educational_decisions` or SCI state  
- Replacing PX-001 Runtime C educational experience snapshots  

---

## 9. Future extensibility

| Concern | Strategy |
|---------|----------|
| New surface | Add projection from `ExperienceModel`; extend `ExperienceEnginePort` |
| Copy refresh | Update presentation catalogues; bump `eee.v*` |
| UI wiring | Adapters implement contracts; no logic in templates |
| Locale | Catalogue layer only — decisions remain language-neutral codes + rationale |

```
Published CKG → SCI → Evidence → Twin Beliefs
        ↓
Educational Reasoning Engine (EI-007)  ← decisions + explanations
        ↓
Educational Experience Engine (EX-001) ← experience models
        ↓
Student Interfaces (Mission / Coach / Dashboard / Revision / Session)
```
