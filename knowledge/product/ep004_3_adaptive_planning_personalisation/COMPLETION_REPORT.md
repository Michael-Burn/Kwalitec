# EP-004.3 — Programme Completion Report

**Programme:** EP-004.3 — Adaptive Planning Personalisation  
**Date:** 2026-07-26  
**Status:** Complete  
**Production activation:** Gated (`KWALITEC_PERSONAL_LEARNING_PROFILE` / `ENABLE_PERSONAL_LEARNING_PROFILE` default OFF)

---

## Summary

EP-004.3 enhances `PlanningService` so Personal Learning Profile attributes may lawfully influence session duration, workload pacing, recovery minute emphasis, revision timing, and equivalent repair-topic selection — without changing educational priorities or delegating planning authority. Personalisation is confidence-gated, fail-open, and explainable (`personalisation_factors` + supporting evidence). Educational slot order `review → recovery/weak → progression` is hard-preserved. Estimated weighted ΔKSI ≈ **+2.3** (K4/K1 primary), under-claimed pending live re-score. Constitutional ownership verified.

---

## Files Created

- `app/services/planning_personalisation.py`
- `tests/services/test_planning_personalisation_ep004_3.py`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/README.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/DISCOVERY_REPORT.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/CONSTITUTIONAL_IMPACT_ASSESSMENT.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/STUDENT_IMPACT_ASSESSMENT.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/PLANNING_PERSONALISATION_GAP_ANALYSIS.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/PERSONALISATION_RULES.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/RISK_ASSESSMENT.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/EXPLAINABILITY_REVIEW.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/KSI_IMPACT_ASSESSMENT.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/CONSTITUTIONAL_VERIFICATION.md`
- `knowledge/product/ep004_3_adaptive_planning_personalisation/COMPLETION_REPORT.md`

---

## Files Modified

- `app/services/planning_quality.py` — optional `profile_view`; apply personalisation after quality schema
- `app/services/planning_service.py` — consume profile and pass into quality for daily plan + dashboard surface
- `app/presentation/intelligence_surface/adapter.py` — pass-through documentation for planning personalisation fields
- `knowledge/architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md` — personalisation contract
- `knowledge/architecture/PERSONAL_LEARNING_PROFILE_ARCHITECTURE.md` — planning consumer closed-loop note
- `knowledge/subsystems/study-planning.md` — EP-004.3 pointer
- `knowledge/product/README.md` — programme index entry
- `knowledge/product/ep004_1_personal_learning_profile/LEARNING_PROFILE_GAP_ANALYSIS.md` — residual gap closure note

---

## Tests Executed

```bash
python3 -m pytest tests/services/test_planning_personalisation_ep004_3.py \
  tests/services/test_planning_quality_ep003_3.py -q
```

**Outcome:** Pass (EP-004.3: 13; EP-003.3 quality: 14).

```bash
python3 -m ruff check \
  app/services/planning_personalisation.py \
  app/services/planning_quality.py \
  app/presentation/intelligence_surface/adapter.py \
  tests/services/test_planning_personalisation_ep004_3.py
```

**Outcome:** Clean for EP-004.3 touched modules.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved: PlanningService remains sole Runtime A planning authority.
- Personal Learning Profile remains evidence-only via Port.
- Curriculum V1/V2 traversal/import compatibility untouched.
- RuntimeAPresentationAdapter remains presentation-only.
- Feature flags and fail-open behaviour preserved.
- Recommendation and Readiness authorities unchanged.
- EP-002.9 ownership baseline preserved (`CONSTITUTIONAL_VERIFICATION.md`).

---

## Technical Debt

- Process-local profile store (EP-004.1) limits multi-process personalisation stability.
- Equivalent repair-topic selection lacks per-topic behavioural rates.
- Preferred study windows remain unsupported.
- Declared session minutes require an upstream settings hand-off (not wired in this programme).

---

## Known Limitations

- Estimated KSI only — live cohort re-score pending.
- Flag OFF by default — no production behavioural change until explicitly enabled.
- Does not personalise readiness.
- Does not declare Twin Ready or production cutover changes.

---

## Student Impact Assessment

See [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md).

---

## Estimated KSI contribution

See [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md).

| Category | Δ |
|---|---:|
| K1 | +5 |
| K2 | 0 |
| K3 | 0 |
| K4 | +7 |
| K5 | 0 |
| K6 | +1 |
| K7 | +3 |
| K8 | +2 |
| **Weighted net ΔKSI** | **≈ +2.3** |

---

## Evidence collected

- Unit / integration tests: `tests/services/test_planning_personalisation_ep004_3.py`
- Rules: `PERSONALISATION_RULES.md`
- Architecture: `knowledge/architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md`, `PERSONAL_LEARNING_PROFILE_ARCHITECTURE.md`
- Reviews: `EXPLAINABILITY_REVIEW.md`
- Constitutional artefacts: `CONSTITUTIONAL_IMPACT_ASSESSMENT.md`, `CONSTITUTIONAL_VERIFICATION.md`

---

## Lessons learned for student value

A behavioural profile becomes planning-valuable when PlanningService consumes it with explicit confidence gates and discloses influence — without letting habits reorder educational priorities. Closing the loop inside PlanningService keeps personalisation trustworthy: students can see that pacing and repair emphasis reflected their habits while Today's Mission structure remains syllabus-coherent.

---

## Explainability Review

**Pass** — [`EXPLAINABILITY_REVIEW.md`](EXPLAINABILITY_REVIEW.md)

---

## Recommendation Quality Review

**N/A** — programme does not change student-facing recommendation ranking or selection (RecommendationService untouched; Planning does not use accept/dismiss).

---

## Constitutional Verification

**Pass** — [`CONSTITUTIONAL_VERIFICATION.md`](CONSTITUTIONAL_VERIFICATION.md)

---

## Completion criteria

| Criterion | Status |
|---|---|
| Evidence-based planning personalisation implemented | **Met** (when flag ON) |
| Planning authority preserved | **Met** |
| Personalised plans remain fully explainable | **Met** |
| Tests pass | **Met** |
| Estimated KSI contribution documented | **Met** |
| Student Impact Assessment completed | **Met** |
