# PI-002A — Test Evidence

**Programme:** PI-002A — Platform Integration: Founder → Student Bridge  
**Date:** 2026-07-27  

---

## Commands

```bash
python3 -m pytest tests/application/platform_integration/ \
  tests/application/educational_runtime_engine/test_integration.py \
  tests/certification/test_cs12_coexistence.py -v --tb=short
```

**Result:** 28 passed (see `TEST_EVIDENCE_RAW.txt`).

---

## Acceptance mapping

| Criterion | Evidence |
|---|---|
| Founder-published subjects appear in discovery | `test_discovery_lists_published_when_flag_on` |
| Students can enrol in founder-published subjects | `test_bridge_enrols_runtime_c_with_audit` |
| Each enrolment is routed to the configured runtime | routing tests + e2e demo |
| Runtime selection is auditable | `RuntimeEnrolmentRoutingAudit` assertions |
| Existing Runtime A enrolments unchanged | `test_runtime_a_enrolment_unchanged_and_audited`, CS-12, PI-001C integration |
| Rollout controllable via flags | flag defaults / discovery-only / enrolment-disabled tests |

---

## End-to-end demonstration

`tests/application/platform_integration/test_e2e_demo.py` exercises:

1. Founder publish → discovery surface  
2. Student Runtime C enrolment + mission generation  
3. Same student Runtime A study plan  
4. Dual audit trail (`published_curriculum` + `json_bundled`)
