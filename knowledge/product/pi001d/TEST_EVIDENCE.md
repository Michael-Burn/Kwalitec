# PI-001D — Test Evidence

**Date:** 2026-07-27  
**Raw log:** `knowledge/product/pi001d/TEST_EVIDENCE_RAW.txt`

## Commands

```bash
python3 -m ruff check \
  tests/certification/pi001d_helpers.py \
  tests/certification/test_cs01_founder_onboarding.py \
  tests/certification/test_cs02_publication.py \
  tests/certification/test_cs03_derivation.py \
  tests/certification/test_cs04_to_cs08_runtime.py \
  tests/certification/test_cs09_journey_e2e.py \
  tests/certification/test_cs10_cs11_inputs.py \
  tests/certification/test_cs12_coexistence.py \
  tests/certification/test_runtime_parity.py

python3 -m pytest \
  tests/certification/test_cs01_founder_onboarding.py \
  tests/certification/test_cs02_publication.py \
  tests/certification/test_cs03_derivation.py \
  tests/certification/test_cs04_to_cs08_runtime.py \
  tests/certification/test_cs09_journey_e2e.py \
  tests/certification/test_cs10_cs11_inputs.py \
  tests/certification/test_cs12_coexistence.py \
  tests/certification/test_runtime_parity.py \
  -q
```

## Results

| Suite | Outcome |
|---|---|
| Ruff (PI-001D test paths) | All checks passed |
| CS-01 Founder onboarding (5) | Passed |
| CS-02 Curriculum publication (3) | Passed |
| CS-03 Educational derivation (4) | Passed |
| CS-04 to CS-08 Runtime lifecycle (15) | Passed |
| CS-09 End-to-end journey (4) | Passed |
| CS-10 / CS-11 Readiness + EK inputs (3) | Passed |
| CS-12 Runtime coexistence (4) | Passed |
| Runtime parity — CS1 structural (9) | Passed |
| **Total** | **47 passed** |

## Acceptance mapping

| Criterion | Evidence |
|---|---|
| Founder can onboard without developer intervention | `test_cs01_4_to_6_full_lifecycle_to_publish`, `test_cs01_7_subject_agnostic` |
| Published subject derives educational artefacts | `test_cs03_1_all_artefacts_derived` |
| Student completes end-to-end Runtime C cycle | `test_cs09_1_full_syllabus_traversal`, `test_cs09_2_final_state_correct` |
| Runtime C equivalent where expected | `test_runtime_parity.py` (9 tests) |
| Intentional differences documented | `BEHAVIOURAL_COMPARISON_REPORT.md` |
| Go/no-go recommendation produced | `MIGRATION_READINESS_ASSESSMENT.md` |
| Runtime A unaffected by Runtime C | `test_cs12_3_json_runtime_unaffected` |
| Prerequisite-aware journey ordering | `test_cs09_1_full_syllabus_traversal` topic sequence assertion |

## Coexistence with other certification suites

PI-001D helpers live in `tests/certification/pi001d_helpers.py` so they do not collide with the pre-existing FSI-005 operational certification helpers in `tests/certification/helpers.py`.
