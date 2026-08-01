# RC2_SPRINT_B_COMPLETION_REPORT.md

**Programme:** VERSION1-RC2 — Sprint B — Educational Trust Restoration  
**Date:** 2026-08-01  
**Commit:** *(filled after mandated commit)*  

---

## Summary

Sprint B closes the local **KI-C3 educational consistency** gap: Dashboard, Analytics, and Readiness now share Study Progress (`TopicProgress.completed`) coverage; practice-backed Estimated Knowledge no longer contradicts “Not Started” without explanation; imported learning objectives are surfaced on the Study Plan; Curriculum Map quarantines non-syllabus noise and inherits LO status from completed parents. No deploy, no push.

---

## Files Created

- `EV001_REMEDIATION_REPORT.md`
- `EDUCATIONAL_CONSISTENCY_REPORT.md`
- `READINESS_VALIDATION_REPORT.md`
- `RC2_SPRINT_B_COMPLETION_REPORT.md`
- `tests/test_rc2_educational_trust_consistency.py`

## Files Modified

- `app/services/readiness_service.py`
- `app/services/readiness_quality.py`
- `app/services/educational_explainability_service.py`
- `app/services/product_communication_service.py`
- `app/infrastructure/adapters/readiness_intelligence/consumer.py`
- `app/presentation/student/services/student_knowledge_graph_presentation_service.py`
- `app/application/student_baseline/topics.py`
- `app/templates/study_plan/view.html`
- `app/templates/analytics/index.html`
- `tests/test_ptp003_honest_product_communication.py`
- `KNOWN_ISSUES_RC2.md`
- `CHANGELOG.md`
- `VERSION1_RELEASE_MANIFEST.md`

## Tests Executed

```text
python3 -m pytest \
  tests/test_rc2_educational_trust_consistency.py \
  tests/test_ptp003_honest_product_communication.py \
  tests/services/test_readiness_quality_ep003_2.py \
  tests/test_services.py::TestReadinessService \
  tests/test_eip001_educational_state_ownership.py \
  tests/test_ia004_truthful_learning_progress.py \
  tests/infrastructure/adapters/consumer_chain/test_readiness_dual_run.py -q
```

**Outcome:** Focused RC2 consistency + readiness + ownership suites **PASS**.  
**Note:** Two pre-existing EIP-006 tests fail with FK IntegrityError (`topic_id=1` without Topic row) — reproduced without readiness edits; not Sprint B regressions.

`python3 tools/architecture_guardian.py` → **40/100** (unchanged pre-existing debt); Blueprint Separation **PASS**.

## Migration Impact

**None.**

## Architecture Compliance

- Layering preserved: readiness math in services; presentation adapters/templates only display.  
- Curriculum V1/V2: plan-scoped leaves via `CurriculumService.get_ordered_topics`; no new ordering fork.  
- EF-001 freeze respected: no new Educational Framework law.

## Technical Debt

- Global leaf fallback when no active plan remains (onboarding edge).  
- EIP-006 hard-coded `topic_id=1` tests remain brittle under FK enforcement.  
- Architecture Guardian 40/100 pre-existing.

## Known Limitations

- LIVE EV-001 pedagogy failures (placeholders / empty reading / stuck advance) require deploy + smoke (Sprint C).  
- Volume `released` / activation (KI-H1/H4) unchanged.  
- Full HTTP fresh-student workflow not re-run on LIVE (no deploy).

---

## Success criteria checklist

| Criterion | Local |
|-----------|-------|
| Dashboard / Analytics / Readiness coverage agree | ✓ |
| Topic Status consistent with Estimated Knowledge (or explained) | ✓ |
| Learning Objectives surfaced when imported | ✓ |
| Readiness components explainable / evidence-based | ✓ |
| Deploy / push | ✗ intentionally |

---

## Stop

Sprint B complete. **Do not deploy. Do not push.** Deployment belongs to Sprint C only.
