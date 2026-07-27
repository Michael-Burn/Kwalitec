# PX-001 — Runtime C Integration Plan

**Programme:** PX-001 — Educational Experience Integration  
**Status:** Implemented  

---

## Architecture

```
RuntimeEnrolment (active)
    → EducationalExperienceService.load_for_user
         → EducationalRuntimeEngineService.generate_daily_mission (idempotent)
         → get_journey / get_journey_explanation / project_pacing
         → EducationalExperienceSnapshot (student-safe)
    → page_from_educational_experience
         → HomePageViewModel + JourneyPageViewModel + EducationalExperienceViewModel
    → templates/student/home.html + journey.html
         → components/educational_experience.html
```

Runtime A Student Experience (Twin / Adaptive / Mission ports) remains the default when no active Runtime C enrolment exists.

---

## Integration seams

| Layer | Component | Role |
|---|---|---|
| Application | `EducationalExperienceService` | Detect enrolment; project EQ-001 fields |
| Presentation | `educational_view_models.py` | Map snapshot → page VMs |
| HTTP | `views.load_page` | Prefer Runtime C for Home/Journey when enrolled |
| Template | `educational_experience.html` | Information panel (no new interactions) |

---

## Coexistence rules

1. **Runtime A default** — no Runtime C enrolment → existing Home/Journey path unchanged.
2. **Runtime C visibility** — active `RuntimeEnrolment` → Home/Journey project from Runtime C.
3. **Parallel plans** — a student may still hold a Runtime A `StudyPlan`; legacy dashboard/mission routes stay Runtime A.
4. **Fail-open** — Runtime C projection errors log and fall back to Runtime A path.
5. **No Twin** — Runtime C Home does not call Student Twin or Adaptive Decision ports.

---

## Explainability mapping

| EQ-001 field | UI placement |
|---|---|
| `why_this_mission` / rationale | Home hero Why + panel |
| `supporting_evidence` | `<details>` explainability |
| `confidence_level` | Explainability disclosure |
| `expected_benefit` | Hero + disclosure |
| `suggested_next_action` | Disclosure |
| `why_today` / `why_previous_complete` / `unlocks_next` | Journey panel |

---

## Mission / Journey integration

- Mission: auto-generate today's instance (idempotent) so duration/LOs/rationale are always available on Home.
- Journey: topic lists derived from progress model; explanation answers the three EQ-J questions.
- Pacing: exam-date-aware projection with honest shortfall language.

---

## Out of scope (explicit)

- Visual redesign / premium chrome
- Twin / Adaptive activation
- Runtime A production cutover
- Guided session write path into `complete_mission`
- Revision / History Runtime C event narratives
