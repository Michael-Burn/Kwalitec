# EQ-001 — Study Plan Quality Rules

**Programme:** EQ-001  
**Status:** Active  
**Applies to:** Derived study-plan templates (PI-001B) and Runtime C plan pacing projections (PI-001C)

---

## Mandatory qualities

Each study plan derived from a published subject must demonstrate:

| Quality | Rule | Fail when |
|---|---|---|
| **Syllabus order** | Topic template order matches published topological order (prerequisites before dependents) | Order violates prerequisite edges |
| **Prerequisite integrity** | Every topic’s `prerequisite_ids` appear earlier in the plan; edges are acyclic | Unknown prereq, cycle, or forward reference |
| **Realistic pacing** | Total recommended minutes > 0; per-topic minutes positive; pacing projection yields feasible daily load given study budgets | Zero minutes; impossible compression without honesty flag |
| **Exam-date awareness** | When `exam_date` is set on enrolment, pacing projection reports days remaining, required average minutes/day, and feasibility | Exam date ignored when present |
| **Revision allocation** | Pacing projection reserves a revision share after first-pass coverage (default ≥ 15% of calendar or explicit revision block) | No revision allocation in projection |

---

## Template rules

1. One topic template row per published topic.
2. `recommended_minutes` = topic `estimated_minutes` (> 0).
3. Template order = derivation topological order.
4. Template does not invent week ORM rows (Runtime A ownership); quality is certified on the template + read-only pacing projection.

---

## Pacing projection rules

Given enrolment `exam_date`, weekday/weekend minute budgets (defaults: 90 / 120), and template minutes:

1. Sum first-pass recommended minutes.
2. Allocate revision minutes = `max(revision_floor, round(first_pass * revision_ratio))` with defaults `revision_ratio=0.20`, `revision_floor=60`.
3. Compute available study minutes from today → exam_date using weekday/weekend budgets.
4. Report `feasible` when available ≥ first_pass + revision; otherwise `feasible=false` with honest shortfall minutes (never silently compress).
5. Surface `required_average_minutes_per_study_day` for transparency.

---

## Certification ids

| Id | Check |
|---|---|
| EQ-P01 | Study plan template covers all published topics |
| EQ-P02 | Template order respects prerequisite integrity |
| EQ-P03 | All recommended_minutes are positive |
| EQ-P04 | Pacing projection is exam-date aware when exam_date set |
| EQ-P05 | Pacing projection includes revision allocation |
| EQ-P06 | Infeasible pacing is reported honestly (not silently compressed) |
