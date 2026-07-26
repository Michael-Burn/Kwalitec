# EP-007.1 — Programme Completion Report

**Programme:** EP-007.1 — Student Journey Consolidation  
**Date:** 2026-07-26  
**Status:** Complete  
**Production activation:** Sole runtime already ON in `render.yaml`; entry / duration / CTA consolidation shipped  

---

## Summary

EP-007.1 designs and implements a single canonical student journey that removes the dual-home experience under `KWALITEC_V2_SOLE_RUNTIME`, unifies planned session duration across Home / Mission / bridges, and routes login, onboarding, calibration, and completion into Student Home — without changing Runtime A, RecommendationService, PlanningService, or ReadinessService educational reasoning. Regression tests cover canonical navigation, duration consistency, session-completion contract, and dual-run backwards compatibility. Estimated ΔKSI ≈ **+1.0** (prefer-lower; **not validated**). Ready for Tier B journey validation.

---

## Files Created

- `knowledge/product/ep007_1_student_journey_consolidation/README.md`
- `knowledge/product/ep007_1_student_journey_consolidation/STUDENT_JOURNEY_CONSOLIDATION.md`
- `knowledge/product/ep007_1_student_journey_consolidation/JOURNEY_TRACEABILITY.md`
- `knowledge/product/ep007_1_student_journey_consolidation/STUDENT_IMPACT_ASSESSMENT.md`
- `knowledge/product/ep007_1_student_journey_consolidation/COMPLETION_REPORT.md`
- `app/application/student_experience/session_duration.py`
- `tests/presentation/test_canonical_journey.py`

---

## Files Modified

- `app/presentation/consolidation.py` — canonical home / session-entry helpers
- `app/auth/routes.py` — login → canonical home
- `app/alpha/routes.py` — onboarding / feedback → canonical home
- `app/calibration/routes.py` — post-calibration → canonical home
- `app/study_plan/routes.py` — activate plan → canonical home
- `app/research/routes.py` — check-in dismiss / ineligible → canonical home
- `app/dashboard/routes.py` — welcome dismiss / revision ack → canonical home
- `app/presentation/student/routes.py` — welcome modal on Student Home
- `app/services/study_session_service.py` — duration via shared resolver
- `app/infrastructure/adapters/educational_runtime_bridge/mission_read_adapter.py`
- `app/infrastructure/adapters/educational_runtime_bridge/mission_start_adapter.py`
- `app/infrastructure/adapters/educational_runtime_bridge/mission_resume_adapter.py`
- `app/infrastructure/adapters/educational_runtime_bridge/recommendation_adapter.py`
- `app/infrastructure/adapters/educational_runtime_bridge/session_completion_adapter.py`
- `app/__init__.py` — template globals for canonical URLs
- `app/templates/partials/welcome_modal.html`
- `app/templates/student/home.html`
- `app/templates/mission/index.html` — preferred minutes first
- `app/templates/errors/403.html`, `404.html`, `500.html`
- `knowledge/product/README.md`
- `knowledge/GOVERNANCE.md`
- `knowledge/VERSION_1_READINESS.md`
- `.env.example` — sole-runtime comment notes EP-007.1 canonical journey

---

## Tests Executed

```bash
python3 -m pytest \
  tests/presentation/test_canonical_journey.py \
  tests/presentation/workflows/test_workflow_dual_run.py \
  -q
```

**Outcome:** Pass (15 new + 13 dual-run workflow tests).

```bash
python3 -m ruff check \
  app/presentation/consolidation.py \
  app/application/student_experience/session_duration.py \
  app/auth/routes.py \
  app/alpha/routes.py \
  app/calibration/routes.py \
  app/study_plan/routes.py \
  app/research/routes.py \
  app/dashboard/routes.py \
  app/presentation/student/routes.py \
  app/services/study_session_service.py \
  app/infrastructure/adapters/educational_runtime_bridge/mission_read_adapter.py \
  app/infrastructure/adapters/educational_runtime_bridge/mission_start_adapter.py \
  app/infrastructure/adapters/educational_runtime_bridge/mission_resume_adapter.py \
  app/infrastructure/adapters/educational_runtime_bridge/recommendation_adapter.py \
  app/infrastructure/adapters/educational_runtime_bridge/session_completion_adapter.py \
  tests/presentation/test_canonical_journey.py
```

**Outcome:** Pass (run at completion).

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved: routes → presentation helpers / services; no educational math in blueprints.
- Curriculum V1/V2: **N/A** (no curriculum engine changes).
- Runtime A / RecommendationService / PlanningService / ReadinessService ownership **preserved**.
- Dual-run rollback retained when `SOLE_RUNTIME` is OFF (Release Framework compatible).
- No Product Constitution amendments.

---

## Technical Debt

- Legacy blueprints remain registered as redirect shells — intentional until a retirement programme deletes them.
- `ENABLE_UNIFIED_JOURNEY` remains default OFF; guided DayExperience chrome is optional, not required for dual-home removal.
- Some secondary templates (study plan view link, research thank-you) may still mention Dashboard wording under dual-run; sole runtime users do not land there as Home.

---

## Known Limitations

- Validated K1 / dual-home perception lift **not claimed** — requires Tier B journey pack.
- Dual-home still exists when `SOLE_RUNTIME` is OFF (Internal Alpha / local soak).
- Does not change educational recommendation ranking, readiness scoring, or planning topic selection.
- Welcome dismiss POST remains on `dashboard.dismiss_welcome` endpoint (works under sole runtime; redirects to canonical home).

---

## Student Impact Assessment

See [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md).

---

## Estimated KSI contribution

| Category | Δ (est.) |
|---|---:|
| K1 | +4 |
| K5 | +3 |
| K8 | +1 |
| **Net ΔKSI** | **≈ +1.0** (prefer-lower; not validated) |

---

## Evidence collected

- `STUDENT_JOURNEY_CONSOLIDATION.md`
- `JOURNEY_TRACEABILITY.md`
- `STUDENT_IMPACT_ASSESSMENT.md`
- `tests/presentation/test_canonical_journey.py`
- Prior: EP-005.2 journey review; EP-006.3 / EP-006.5 dual-home residuals

---

## Lessons learned for student value

Dual-home is not cured by explainability delivery alone. Students need one entry, one clock, and one continue path before Tier B can clear REM-02 / REM-03. Estimated KSI must stay under-claimed until perception re-test.

---

## Explainability Review

N/A — presentation routing / duration display consolidation only; no change to recommendation, readiness, or planning explanation schema or Runtime A authored MES.

---

## Recommendation Quality Review

N/A — no ranking, selection, or Coach tip-authority changes.

---

## Version 1 readiness residual

Does **not** claim Version 1 production-ready. Residual open gates from P-002.1 remain (notably overall G1.1 KSI ≥ 80, G1.9 effectiveness). This programme advances REM-02 / REM-03 readiness for a Tier B journey pack; it does not clear Gate G1.

---

**End of COMPLETION_REPORT**
