# EQ-001 — Test Evidence

**Programme:** EQ-001 — Educational Quality Certification  
**Date:** 2026-07-27  
**Raw log:** [`TEST_EVIDENCE_RAW.txt`](TEST_EVIDENCE_RAW.txt)

---

## Commands

```bash
python3 -m pytest tests/certification/test_eq001_educational_quality.py \
  tests/domain/educational_quality/ \
  tests/domain/educational_engine_foundation/test_derivation.py -v --tb=short

python3 -m ruff check app/domain/educational_quality \
  app/application/educational_quality \
  app/domain/educational_engine_foundation/derivation.py \
  app/application/educational_engine_foundation \
  app/application/educational_runtime_engine \
  tests/certification/test_eq001_educational_quality.py \
  tests/domain/educational_quality
```

**Outcome:** 12 passed; ruff clean on EQ-001 paths.  
**Regression (also green):** PI-001D CS-01, CS-03, CS-04–08, CS-09, CS-12, runtime parity; educational engine/runtime foundation suites.

---

## Scenario map

| Scenario | Test | Result |
|---|---|---|
| EQ-M01..M05 mission template quality | `test_eq_m_artefact_mission_quality_rules` | Pass |
| EQ-P01..P03 study plan order / minutes | `test_eq_p_study_plan_quality_rules` | Pass |
| EQ-M06/M07 + EQ-X* mission envelope | `test_eq_m06_m07_generated_mission_quality_envelope` | Pass |
| EQ-J* journey explainability | `test_eq_j_journey_explainability` | Pass |
| EQ-P04..P06 exam pacing + honest shortfall | `test_eq_p04_p06_exam_aware_pacing_and_revision` | Pass |
| End-to-end published subject quality | `test_eq_end_to_end_published_subject_quality` | Pass |
| Prerequisite gate refusal | `test_eq_prerequisite_gate_blocks_illegal_mission` | Pass |
| Domain rule units | `tests/domain/educational_quality/test_rules.py` | Pass (4) |

---

## Acceptance evidence

A newly published subject (`EQ1` via `publish_certified_subject`) automatically generates:

| Criterion | Evidence |
|---|---|
| Curriculum-bound study plans | Template order `topic-t1 → topic-t2 → topic-t3` with prerequisite edges |
| High-quality daily missions | Quality envelope: topic, LO refs, duration, completion definition, rationale, prereq validation |
| Explainable educational decisions | Mission `explanation` schema + journey why_today / why_previous_complete / unlocks_next |
| Correct prerequisite sequencing | Mission generation refuses unmet prerequisites |
| Realistic pacing | Exam-date projection with revision allocation; infeasible loads report shortfall |
| Transparent student guidance | Structured envelopes suitable for student display (no UI redesign in this programme) |
