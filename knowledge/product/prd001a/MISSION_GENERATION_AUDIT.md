# PRD-001A — Mission Generation Audit

## Trace

```
Student
  → Study Plan (active, curriculum-bound)
  → Mission Engine (PlanningService.generate_today_mission)
  → Recommendation Engine (parallel packaging for Home MES)
  → Dashboard / EOS Home
```

Production authority for **persisted** today’s mission: **Runtime A** `PlanningService.generate_today_mission` (not quarantined `MissionOptimizer`; not Twin daily-plan writer unless cutover flag ON).

---

## Why was today's mission selected?

**Learning Mode (typical new CS1 student):**

> Because it is the **first incomplete leaf topic** in the official curriculum order for the active plan.

Evidence — explicit product law:

```1279:1285:app/services/planning_service.py
        """Select today's mission topic under Learning Mode (IA-004).

        Version 1.0 Learning Mode: Today's Mission always follows the
        Current Learning Topic (first incomplete syllabus leaf in the
        active plan). Review / weak-topic interruption is deferred to
        Educational Intelligence Phase 1 and must never silently replace
        the planned learning sequence.
```

Selection call:

```1346:1350:app/services/planning_service.py
        # Current Learning Topic = first incomplete syllabus leaf.
        next_topic = CurriculumService.get_next_incomplete_topic(
            user_id=user_id,
            curriculum=curriculum,
        )
```

**Revision stage:** Deterministic rotation of revision mission kinds; weak-topic **label** may come from Twin or weakest completed topic — still not full Twin slot planner unless cutover enabled.

---

## What data produced it?

| Input | Used for topic selection? | Used for title/tasks/duration? |
|---|---|---|
| Active `StudyPlan` | Yes (curriculum binding, stage) | Yes (minutes, preference) |
| `TopicProgress.completed` | **Yes — sole Learning Mode selector** | Indirect |
| `mastery_score` (Estimated Knowledge) | **No** | No |
| Overall Readiness | **No** | Labels via planning quality only |
| Review schedules | **No** (docstring: deferred) | No |
| Weekday/weekend minutes | No | Yes — task minute splits |
| Study preference | No | Yes — Reading/Questions/Mixed templates |
| Exam date | Lifecycle/stage context | Copy / planning context |

---

## What evidence supports it?

**System evidence:** Curriculum leaf order + incomplete progress rows.  
**Learning evidence (attempts/accuracy):** Does **not** change Learning Mode topic.  
**Explainability evidence on Home:** Authored MES fields from recommendation/explanation pipeline — may describe benefit and timeliness even when selection was purely sequential.

---

## Can the student understand it?

| Layer | Understandable? |
|---|---|
| “I should study this topic title today” | Yes, if title bound |
| “Because it’s next in my CS1 syllabus” | **Only if copy says so** — often not explicit |
| “Because my Estimated Knowledge is low” | **Misleading if implied** — false for Learning Mode |
| “Because Readiness dropped” | **False** for topic selection |

---

## Recommendation Engine relationship

Mission selection and recommendation listing are **related but not identical**:

- Mission: syllabus progression (Learning Mode).  
- Recommendations: multiple rule buckets including weak topics (`mastery_score` thresholds), reviews, burnout, mocks — then quality/explainability contract.  
- Home often **presents** the mission through recommendation/explanation ports so the student sees Why/Why now — which can feel “smarter” than the underlying selector.

This dual presentation is a primary integrity risk: **explainability packaging can outrun selection intelligence.**

---

## Twin path (not default production)

When Digital Twin ON + `ENABLE_DAILY_PLAN_CUTOVER`:

- `DailyStudyPlanAssembler` can allocate review / weak (`mastery_score < 60`) / recovery / progression slots.  
- Still not the default writer for Experience session start in production `render.yaml`.

---

## Mission audit verdict

Today’s mission is **deterministically curriculum-sequential**, durable, and explainable only to the extent Home copy tells the truth about that rule. Founder perception of “generic” missions is consistent with template tasks + under-explained sequential selection — not with a missing Mission table.
