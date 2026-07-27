# PI-001C — Test Evidence

**Date:** 2026-07-27  
**Raw log:** `knowledge/product/pi001c/TEST_EVIDENCE_RAW.txt`

## Commands

```bash
python3 -m ruff check \
  app/domain/educational_runtime_engine \
  app/application/educational_runtime_engine \
  app/models/educational_runtime_engine.py \
  app/models/__init__.py \
  tests/domain/educational_runtime_engine \
  tests/application/educational_runtime_engine

python3 -m pytest \
  tests/domain/educational_runtime_engine/test_lifecycle.py \
  tests/application/educational_runtime_engine/test_integration.py \
  tests/application/educational_engine_foundation/ \
  tests/application/curriculum_studio_foundation/test_integration.py \
  -v
```

## Results

| Suite | Outcome |
|---|---|
| Ruff (PI-001C paths) | All checks passed |
| Domain lifecycle unit tests (6) | Passed |
| Runtime engine integration / e2e (7) | Passed |
| PI-001B foundation regression (2) | Passed |
| PI-001A foundation integration (3) | Passed |
| **Total** | **18 passed** |

## Acceptance mapping

| Criterion | Evidence |
|---|---|
| Student can enrol | `test_enrol_instantiates_study_plan_from_template` |
| Study plan instance created automatically | same + e2e |
| Daily missions from derived templates | `test_daily_mission_from_derived_template_and_completion_advances` |
| Mission completion updates progress | same + e2e coverage assertions |
| Journey advances automatically | e2e topic advance + `syllabus_completed` event |
| Runtime outputs support Readiness + EK | `test_readiness_and_ek_inputs_without_duplicating_state` |
| No developer-authored subject content after publish | e2e uses founder-published `E2E1` only |
| JSON runtime non-regression | `test_json_runtime_unaffected_by_published_runtime_enrolment` |
