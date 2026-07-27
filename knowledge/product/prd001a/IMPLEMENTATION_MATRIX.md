# PRD-001A — Implementation Matrix

**Method:** For each Blueprint capability, determine implementation status with evidence.  
**Production posture assumed:** `render.yaml` — `KWALITEC_V2_SOLE_RUNTIME=1`, Student Experience ON, **Digital Twin flags unset (default OFF)**, seed demo OFF.

Status vocabulary:

| Status | Meaning |
|---|---|
| Implemented | Works in production path and is wired end-to-end |
| Partially Implemented | Real code + some student/founder surface; incomplete loop |
| Placeholder | Stub, presentation-only, or empty contract |
| Missing | No meaningful implementation for the promised behaviour |
| Deprecated | Present but quarantined / must not drive production |
| Not yet connected | Backend exists; production flag or UI bridge off |

---

## Matrix

| ID | Capability | Status | Evidence |
|---|---|---|---|
| C01 | Curriculum Intelligence | **Implemented** | `app/curriculum/loader.py`, `schemas.py` V1/V2 detect; `CurriculumService.import_curricula` + `get_all_topics_ordered` / `get_next_incomplete_topic`; CS1 `app/curriculum/data/ifoa/cs1/2026.json` |
| C02 | Student Digital Twin | **Not yet connected** (foundation present) | Domain `app/domain/twin/`; flags `ENABLE_DIGITAL_TWIN` default False (`v2_flags.py`); **not** set in `render.yaml`; no student UI name “Digital Twin” |
| C03 | Educational State / EI stack | **Partially Implemented** | `EducationalStateService` assembles Home snapshot; Runtime A services coexist; Twin authority off → Experience twin adapter defaults |
| C04 | Evidence pillar | **Partially Implemented** | `StudyAttempt`, practice outcomes, Decision journal (`Decision` model, `RecommendationService.record_decision`); student rarely sees journal |
| C05 | Estimated Knowledge | **Partially Implemented** | `TopicProgress.mastery_score` + `has_estimated_knowledge`; shown on Study Plan roadmap; **absent** from EOS Home/Journey templates (grep: no EK strings under `app/templates/student/`) |
| C06 | Exam Readiness | **Implemented** (reporting) / **Partial** (decision influence) | `ReadinessService.get_overall_readiness`; Home readiness panel (`home.html`); influences recommendation packaging & weak-topic recs; **not** Learning Mode topic pick |
| C07 | Recommendation Engine | **Implemented** | `RecommendationService.generate_recommendations` rule buckets + `recommendation_quality.apply_quality_contract`; Home via Adaptive Decision port / Educational State |
| C08 | Explainability | **Implemented** (packaging) / **Partial** (clarity of true rule) | MES fields on Home (`why_recommended`, `timeliness_line`, `explanation_card`); schema `p001.2/v1` |
| C09 | Mission Engine | **Implemented** (legacy authority) | `PlanningService.generate_today_mission` → `_select_topic_for_today` → `get_next_incomplete_topic`; `MissionService.create_mission`. Twin `build_daily_study_plan` **Not yet connected** (`ENABLE_DAILY_PLAN_CUTOVER` off). `MissionOptimizer` **Deprecated** |
| C10 | Study Planning | **Implemented** | Wizard `app/study_plan/routes.py`; `StudyPlanService.create_study_plan` + week plans + topic progress init |
| C11 | Journey | **Implemented** | `/student/journey` → `journey.html` current/completed/upcoming; Home journey story panel |
| C12 | Coach | **Partially Implemented** | Home Coach panel; often defers to Mission card or cold-start placeholder (`view_models.py` default insight string) |
| C13 | Insights | **Partially Implemented** | Product language maps Twin → Learning Insights; no `/insights` route; content folded into Home/History |
| C14 | Reflection | **Partially Implemented** | Session reflection templates + commitment reflection on Home; hero reflection preview marked `data-presentation-only` / “nothing is saved yet” (`home.html`) |
| C15 | Progress Tracking | **Implemented** | Journey + History + Study Plan roadmap topic stages |
| C16 | Learning Analytics | **Partially Implemented** | Canonical `/student/history`; legacy `/analytics/` Chart.js **redirects** under sole runtime (`consolidation.py`) |
| C17 | Syllabus Management | **Partially Implemented** | Bundled JSON import at startup; Curriculum Studio services exist; founder upload UI incomplete |
| C18 | CMP Integration | **Placeholder / Missing** (student); **Partial** (founder) | `DocumentKind.CMP`; Studio validation requires `cmp_uploaded`; **no** student upload routes; Studio HTTP has validate/publish but **no** upload form |
| C19 | One Runtime / EOS | **Implemented** | `SOLE_RUNTIME=1` in `render.yaml`; DEP-003 layout router `layouts/base.html` → `eos_student.html` |
| C20 | Revision Intelligence | **Partially Implemented** | `/student/revision` with explanation_card; deeper optimisation deferred per Blueprint |
| C21 | Decision Journal | **Implemented** (backend) / **Not yet connected** (student UI) | `RecommendationService.get_decision_journal`; no primary EOS page for journal |
| C22 | Burnout / sustainable pace | **Partially Implemented** | `_burnout_recommendations` in RecommendationService; landing promise “Sustainable pace”; limited Home prominence |
| C23 | Confidence | **Partially Implemented** | Confidence labels on readiness/explanation; evidence-gated honesty |
| C24 | Providers / employers | **Missing** (deferred) | Blueprint Epic 4 — correctly not live |

---

## Dual-authority note (mission)

Production student session start still bridges to **legacy** `PlanningService.generate_today_mission` even when Experience shell is ON. Twin daily-plan projection is a gated HTTP cutover, not the default mission writer. Evidence: planning cutover flags; mission start adapter behaviour (explore audit).

---

## Status summary counts

| Status | Count (approx.) |
|---|---|
| Implemented | 8 |
| Partially Implemented | 11 |
| Not yet connected | 3 (Twin, Daily Plan cutover, Decision Journal UI) |
| Deprecated | 1 (`MissionOptimizer`) |
| Placeholder / Missing (in-scope expectation) | CMP student workflow; student syllabus/CMP map |
| Deferred (honest) | C24 + Twin-first cutover |

---

## Root integrity pattern

Most Blueprint nouns **exist in code**. Fewer are **connected as the student-facing decision system** the Blueprint describes. The implementation gap is concentrated in **authority cutover** (Twin / adaptive daily plan) and **visibility** (EK, syllabus map, decision rule honesty) — not in total absence of services.
