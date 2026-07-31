# SB-001A — Digital Twin Mapping

**Programme:** SB-001A  
**Date:** 2026-07-31

---

## Origin chain

```text
StudentBaseline (ORM)
    → BaselineDeclarations
    → AlphaCalibrationDeclarations / StudentCalibrationContract
    → StudentCalibrationBuilder
    → CalibrationBirthPersister / BaselineTwinBirth
    → TwinRepository (twin_snapshots)
```

Baseline is the durable educational origin. Twin birth reuses Capability 3.6–3.7 builders without a second authorship path.

## Field map

| Baseline field | StudyPlan | Calibration contract | Twin cargo |
|----------------|-----------|----------------------|------------|
| Experience | `current_stage` / position | `previously_studied`, posture | birth metadata posture |
| Position mode + topic | `curriculum_topic_code`, completed topics | `declared_completed_sections` | knowledge prior sections |
| Exam history | — | `previous_attempts` | performance prior |
| Optional mark | stored on Baseline only | not mapped to marks (no marks in contract) | Baseline provenance only |
| Objective continue | — | `finish_remaining` | `study_objective` |
| Objective restart / recommend | restart clears topics | `first_sit` | `study_objective` + Baseline objective token |
| Confidence | Baseline row | optional_notes + provenance | `confidence` self_declared cargo |
| Timestamp | `completed_at` | `emitted_at` | snapshot `persisted_at` |
| Runtime / subject | `runtime_authority`, subject keys | curriculum scope | TwinScope curriculum_id |

## Intentional unknowns preserved

Builder still does **not** invent mastery, readiness, Mid/High theatre, or diagnostic confidence. Confidence on Baseline is self-declared provenance only.
