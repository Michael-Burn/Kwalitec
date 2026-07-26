# SYSTEM_ARCHITECTURE — Education Operating System (V2-023)

**Status:** Binding runtime architecture after sole-runtime activation  
**Date:** 2026-07-23  
**Branch:** `feature/educational-architecture-consolidation`  
**Authority:** [PHASE_1_CANONICAL_DECLARATION.md](PHASE_1_CANONICAL_DECLARATION.md) · [CANONICAL_RUNTIME_VALIDATION.md](CANONICAL_RUNTIME_VALIDATION.md) · [V2_023_RELEASE_CANDIDATE.md](V2_023_RELEASE_CANDIDATE.md)

---

## One runtime

```
Browser
  │
  ▼
Flask create_app
  │
  ├─ /student/*   Student Experience (canonical Dashboard, Journey, Revision, Analytics, Settings)
  ├─ /session/*   Session Experience (overview → activity → reflection → summary)
  ├─ /study-plan  Study Plan wizard (shared blueprint)
  ├─ /settings    Account settings (linked from Experience Settings)
  └─ legacy shells (/dashboard, /analytics, /missions*) → redirect when SOLE_RUNTIME
```

Production flag: `KWALITEC_V2_SOLE_RUNTIME=1` (`render.yaml`).

---

## Educational state

```
EducationalStateService  (single snapshot cache per learner assembly)
        │
        ├── Twin ports          (learner, readiness, insights)
        ├── Adaptive Decision   (recommendation, revision options)
        ├── Mission port        (today's session handle)
        └── Learning Journey    (progress, topics)
                │
        ┌───────┴───────┬───────────┬───────────┬──────────┐
        ▼               ▼           ▼           ▼          ▼
     Dashboard       Journey    Revision   Analytics   Settings
     (+ Coach)                              (History)  (Profile)
```

Session / Reflection consume Session Runtime ports (no parallel mastery math).

Protected engines (never deleted): Student Digital Twin, Learning Evidence,
Recommendation / Adaptive Decision, IFoA curriculum, CMP, domain models,
Mission Engine / Adapter, `StudySessionService` (rollback evidence path).

---

## Navigation (canonical)

1. Dashboard → `student.home`  
2. Journey → `student.journey`  
3. Revision → `student.revision`  
4. Analytics → `student.history`  
5. Study Plan → `study_plan.index`  
6. Settings → `student.profile`  
7. Help → `alpha.help_centre`  

Coach and Today's Session live on Dashboard (not duplicate top-level products).

Under sole runtime, V1 sidebar chrome mirrors this tree when Study Plan / Help
pages still use `layouts/base.html`.

---

## Route map (student)

| Entry | Sole runtime destination |
|-------|--------------------------|
| `/` | `student.home` |
| `/dashboard/` | `student.home` |
| `/analytics/` | `student.history` |
| `/missions/` | `student.home` |
| `/missions/<id>/session*` | `student.home` |
| `/missions/review/<id>` | `student.home` |
| `/student/*` | Canonical Experience |
| `/session/<id>/*` | Canonical Session Experience |

---

## Service dependency graph (Experience)

```
presentation/student + presentation/session
        │
        ▼
StudentExperienceService / SessionExperienceService
        │
        ├── EducationalStateService
        ├── Home / Journey / Revision / History / Profile projections
        └── ports → infrastructure adapters → Twin / Adaptive / Journey / Mission engines
```

---

## Developer guide (orientation)

| Concern | Start here |
|---------|------------|
| Product context | `PROJECT_CONTEXT.md` |
| Layering | `ARCHITECTURE.md` · this document |
| Flags | `app/application/config/v2_flags.py` |
| Sole-runtime redirects | `app/presentation/consolidation.py` |
| Educational state | `app/application/educational_state/` |
| Student chrome | `app/presentation/student/navigation.py` |
| Retirement runbook | `knowledge/version2/V2_020_RETIREMENT_RUNBOOK.md` |
| RC-1 | `docs/architecture/V2_023_RELEASE_CANDIDATE.md` |

---

## Retired presentation (V2-023)

| Item | Disposition |
|------|-------------|
| Dual-run Version 2 CTAs | Removed |
| Dead `app/static/js/mission.js` | Deleted |
| Legacy list + nested LXP entry under sole | Redirect shells (templates retained for soak/rollback) |
| Competing V1 sidebar destinations under sole | Replaced with canonical nav labels |

Educational calculators (`ReadinessService`, `StudySessionService`, engines) are
**not** retired.
