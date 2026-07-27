# PI-001C — Migration Strategy

## Goal

Move from JSON-backed Runtime A to curriculum-derived Runtime C **without**
regressing existing students.

## Current dual-path

| Path | Authority | Subjects |
|---|---|---|
| **Runtime A (JSON)** | Bundled syllabus JSON → DB import → `StudyPlan` / `Mission` / `TopicProgress` | Existing supported exams (CS1, …) |
| **Runtime C (Published)** | `PublishedCurriculumPackage` → PI-001B artefacts → Runtime Engine | Founder-published subjects with active package |

`RuntimeCoexistencePolicy`:

- If an active published package exists for a subject code → Runtime C **may** enrol.
- JSON Runtime A remains the **default** for existing wizard / mission / readiness paths.
- PI-001C does **not** redirect CS1 wizard traffic onto published packages.

## Phased cutover

### Phase 1 — Additive runtime (this milestone)

- Persist runtime enrolment / plan / mission / events.
- Prove end-to-end journey for a newly published subject.
- Keep Runtime A untouched.

### Phase 2 — Discovery bridge

- Allow study-plan discovery to list founder-published subjects alongside JSON exams.
- Feature-flag enrolment into Runtime C for selected subjects.

### Phase 3 — Service cutovers (evidence-gated)

For each surface, dual-run then cut over only with equivalence evidence:

1. Study plan instantiation
2. Daily mission generation
3. Mission completion → progress
4. Journey projection
5. Readiness denominator scoping
6. Estimated Knowledge input projection

Each cutover must be reversible until equivalence is demonstrated.

### Phase 4 — Decommission JSON path per subject

Only after that subject’s published package is the sole authority and Runtime A
imports are no longer required.

## Non-regression guarantee

Existing `StudyPlanService.create_study_plan` and `PlanningService.generate_today_mission`
continue to operate for bundled curricula. Tests assert a student can hold a
Runtime C enrolment **and** a Runtime A CS1 plan concurrently.
