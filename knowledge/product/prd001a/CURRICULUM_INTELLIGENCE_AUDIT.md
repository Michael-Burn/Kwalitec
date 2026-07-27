# PRD-001A — Curriculum Intelligence Audit

---

## 1. How curriculum is loaded

1. **On disk:** `app/curriculum/data/{org}/{paper}/{year}.json` (e.g. `ifoa/cs1/2026.json`).  
2. **Format detection:** `app/curriculum/schemas.py` — V2 if `sections` + `exam_code`; V1 if flat `topics` + `organisation`.  
3. **Engine load:** `CurriculumRepository` / `CurriculumEngineService.load_auto()`.  
4. **DB import:** `CurriculumService.import_curricula()` at startup (`StartupService`) — idempotent per `(exam_name, version)`.  
5. **Study plan binding:** Wizard resolves version from disk (CS1 → `"2026"`); `StudyPlan.curriculum_id` / `curriculum_version` set on create.

---

## 2. Syllabus representation

| Layer | Representation |
|---|---|
| JSON (CS1 V2) | `provider`, `exam_code`, `sections[]` |
| Engine dataclasses | `CurriculumDefinition` → `SectionDefinition` → `TopicDefinition` → `LearningObjectiveDefinition` |
| ORM | `Curriculum`, `Section`, `Topic` (`section_id`), `LearningObjective` |

V1 curricula remain loadable as flat topic trees (Blueprint / architecture invariant preserved).

---

## 3. Chapters / sections / topics

- **Sections** ≈ syllabus chapters / parts (V2 `Section`, `display_order`, exam weight).  
- **Topics** ≈ study units with official codes (e.g. `1.1`).  
- Canonical student ordering: `CurriculumService.get_all_topics_ordered` — section order then topic order (V2); parent tree (V1).

---

## 4. Learning objectives

- Represented in JSON as `learning_objectives[]` with `code`, cognitive level, estimated minutes.  
- Imported to `LearningObjective` rows via `_import_v2_topics`.  
- Available via `CurriculumService.get_learning_objectives_for_topic`.  
- **Student visibility:** Session may show a learning objective / focus line when guided session active; there is **no** student syllabus browser of all LOs.

---

## 5. Mission generation ↔ curriculum

| Step | Behaviour |
|---|---|
| Learning Mode selection | `get_next_incomplete_topic(user_id, curriculum)` — first leaf where `TopicProgress.completed` is false/missing |
| Title | Includes topic study label when topic resolved |
| Tasks | Deterministic templates using topic label + preference + minutes |
| Recommendations | Progression recs use coverage + next incomplete; weak recs use mastery |

**Conclusion:** Missions **originate from curriculum structure + completion flags**, not from a separate content bank. They do **not** currently originate from Twin Estimated Knowledge on the default production path.

---

## 6. Do recommendations originate from curriculum intelligence?

**Yes for progression and coverage.**  
**Yes for weak topics** (mastery on curriculum topics).  
**No for opaque AI.** No external LLM in recommendation path (`PROJECT_CONTEXT`).

Curriculum intelligence is the **ordering and identity** authority. Educational Intelligence packages explanations and additional rule buckets around that backbone.

---

## 7. Brand-new student creates a CS1 study plan — exact path

| Step | What happens |
|---|---|
| 1–3 | Wizard: IFoA → CS1 → future exam date |
| 4 | Position `not_started` → no `curriculum_current_topic` forced |
| 5–7 | Minutes, preference, target grade |
| Review POST | `StudyPlanService.create_study_plan` |
| Create | Deactivate prior plans; insert plan with `curriculum_version="2026"` |
| Progress init | One `TopicProgress` per CS1 topic: `completed=False`, `mastery_score=0.0`, stage not started |
| Week plans | Date grid (curriculum-paced weeks if topic code set; else date grid) |
| Mission | **Not** created inside `create_study_plan` |
| Calibration | Optional declared coverage sync — does **not** mint Estimated Knowledge |
| First Home/Dashboard visit | `generate_today_mission` → Learning stage → topic **1.1** (“Describe the purpose and function of data analysis” per CS1 JSON) |
| First recommendations | Likely progression / coverage-oriented; weak-topic empty until practice evidence |

---

## 8. Student-visible syllabus mapping

| Surface | Maps official syllabus? |
|---|---|
| Journey | Topic titles current/completed/upcoming — **yes, partial** |
| Study Plan roadmap | Topics + Estimated Knowledge % — **yes** |
| Home | Story line — **weak** |
| Dedicated syllabus / CMP map | **No** |

---

## Curriculum intelligence verdict

**Backend curriculum intelligence is real and production-grade for Version 1.**  
**Student-facing curriculum intelligence is under-exposed relative to the Blueprint’s “understand the syllabus” pillar.** The system understands the syllabus; the student often cannot see that the system does.
