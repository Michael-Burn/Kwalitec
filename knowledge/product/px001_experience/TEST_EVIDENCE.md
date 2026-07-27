# PX-001 — Test Evidence

**Programme:** PX-001 — Educational Experience Integration  
**Date:** 2026-07-27  

## Command

```bash
python3 -m pytest tests/application/educational_experience/test_acceptance.py -v --tb=short
```

## Result

**5 passed.**

| Test | Proves |
|---|---|
| `test_educational_experience_surfaces_eq001_fields` | Snapshot carries topic, LOs, duration, completion, journey, pacing |
| `test_runtime_a_student_has_no_educational_experience` | Runtime A default preserved |
| `test_page_view_model_carries_educational_panel` | Presentation VMs populated |
| `test_home_and_journey_http_render_educational_fields` | HTML acceptance markers |
| `test_coexistence_runtime_a_home_unchanged_without_runtime_c` | No Runtime C panel without enrolment |

Raw log: [`TEST_EVIDENCE_RAW.txt`](TEST_EVIDENCE_RAW.txt).
