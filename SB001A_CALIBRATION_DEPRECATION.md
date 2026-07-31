# SB-001A — Calibration Deprecation

**Programme:** SB-001A  
**Date:** 2026-07-31

---

## Decision 1A

Student-facing Calibration UI is **deprecated** and replaced by Baseline.

## Retained internals

These remain the Twin birth foundation and must not be duplicated:

- `StudentCalibrationContract`
- `StudentCalibrationBuilder`
- `CalibrationBirthPersister`
- `StudyPlanCalibrationCoordinator` (contract assembly helpers)
- `TwinRepository`

## Redirects

| Legacy route | Behaviour |
|--------------|-----------|
| `GET/POST /calibration/after-plan/<id>` | Redirect → `student_baseline.for_plan` |
| `GET /calibration/resume` | Redirect → Baseline for active plan |

Templates under `calibration/` are unused by live student routes.

## Compatibility

Existing application tests for Builder / Persister remain authoritative for Twin construction. Presentation tests now assert Baseline redirects instead of Calibration form POSTs.
