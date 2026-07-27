# PI-002A — Integration Architecture

**Programme:** PI-002A — Platform Integration: Founder → Student Bridge  
**Status:** Authoritative for this milestone  
**Date:** 2026-07-27  

---

## 1. Purpose

Connect founder-published curriculum packages to student discovery and
enrolment **without** replacing Runtime A. Runtime C remains selectable only
through controlled, auditable routing gated by feature flags.

---

## 2. Authority chain

```text
Founder Curriculum Studio (PI-001A)
        │ publish
        ▼
PublishedCurriculumPackage  ← student-safe SSOT
        │
        ├─ PublishedSubjectDiscoveryService   (flag: discovery)
        │         │
        │         ▼
        │   Study Plan Wizard catalogue
        │   (virtual "Published" category)
        │
        └─ RuntimeRoutingService              (flag: Runtime C enrolment)
                  │
                  ├─ Runtime A (JSON)  ← default production path
                  │     StudyPlanService.create_study_plan
                  │
                  └─ Runtime C (published)
                        EducationalRuntimeEngineService.enrol_student
```

---

## 3. Layering

| Layer | Package | Responsibility |
|---|---|---|
| Application | `app/application/platform_integration/` | Flags, discovery, routing, enrolment bridge |
| Models | `app/models/platform_integration.py` | Routing audit rows |
| Services | `SubjectSupportService` | Support verdicts for Published category |
| Presentation | `app/study_plan/routes.py` | Wizard discovery + bridge enrolment |
| Existing | Runtime A / Runtime C engines | Unchanged educational logic |

---

## 4. Explicit non-goals

- Runtime cutover (Runtime A remains default)
- UI redesign of the study-plan wizard
- Removal of JSON catalogue / Runtime A paths
- Twin / Calibration cutover for Runtime C enrolments
- Student mission UI binding to Runtime C (engine-level only in this milestone)

---

## 5. Safety invariants

1. **Flags default OFF** — no discovery or Runtime C enrolment without env change.
2. **Legacy catalogue → Runtime A** — selecting IFoA CS1 (etc.) never silently
   switches to Runtime C unless the subject is on the allowlist.
3. **Published category → Runtime C** — only when enrolment flag is ON and an
   active package exists.
4. **Every enrolment decision is audited** — `runtime_enrolment_routing_audits`.
5. **Drafts never discoverable** — discovery reads only
   `PublishedCurriculumAuthority`.
