# PX-002 — Implementation Report

**Programme:** PX-002 — Product Experience Implementation  
**Date:** 2026-07-28  
**Status:** Implementation complete  
**Authority:** PX-001 Operational Model Alignment design artefacts

---

## Summary

PX-002 implements the approved PX-001 operational model on the **visible product surface** only: Subject Catalogue, student onboarding without uploads, Founder Curriculum Authority navigation, Ready / Coming Soon availability messaging, domain terminology, Home / session completion framing, and regression coverage.

Educational Intelligence, CKG, Runtime Integration, LP-001 enrolment orchestration, VP-001 Preferred Authority, and PI-001 Studio spine were **not redesigned**. Presentation projects existing publication and support gates.

---

## What was delivered

| Scope item | Delivery |
|------------|----------|
| Subject Catalogue | `SubjectCatalogueService` read model + Choose Exam UI |
| Student onboarding | Welcome → Choose Exam → Exam Date → Study Availability → Begin Learning |
| Founder Studio nav | Primary curriculum workflow; ops demoted to secondary |
| Navigation separation | Founder Console vs EOS student shell preserved |
| Terminology | Ready / Coming Soon / Verified Curriculum / Today's Focus |
| Availability messaging | Consistent Ready / Coming Soon / Unavailable copy |
| Dashboard | Home hero framed as Today's Focus |
| Session completion | Stronger completed / why / tomorrow framing |

---

## Files Created

- `app/application/platform_integration/subject_catalogue.py`
- `app/templates/curriculum_studio/hub.html`
- `tests/test_px002_product_experience.py`
- `knowledge/product/px002_product_experience_implementation/PX002_IMPLEMENTATION_REPORT.md` (this file)
- `knowledge/product/px002_product_experience_implementation/SCREEN_CHANGE_REGISTER.md`
- `knowledge/product/px002_product_experience_implementation/TERMINOLOGY_IMPLEMENTATION_REPORT.md`
- `knowledge/product/px002_product_experience_implementation/NAVIGATION_IMPLEMENTATION_REPORT.md`
- `knowledge/product/px002_product_experience_implementation/SUBJECT_CATALOGUE_IMPLEMENTATION.md`
- `knowledge/product/px002_product_experience_implementation/REGRESSION_REPORT.md`

## Files Modified

- `app/services/subject_support_service.py` — student labels Ready / Coming Soon / Unavailable
- `app/application/platform_integration/discovery.py` — remove “Published Curriculum” student category branding
- `app/study_plan/routes.py` — PX-001 onboarding path + deferred defaults
- `app/study_plan/forms.py` — SubjectCatalogueForm; Begin Learning CTA
- `app/templates/study_plan/wizard_step_1.html` — Subject Catalogue cards
- `app/templates/study_plan/wizard_step_3.html`, `wizard_step_5.html`, `review.html`
- `app/templates/partials/subject_support_gate.html`
- `app/static/css/wizard/wizard.css` — Ready / Unavailable badge styles
- `app/founder/dashboard/nav.py` — Curriculum Authority primary nav
- `app/founder/dashboard/templates/founder_dashboard/_sidebar.html`
- `app/presentation/curriculum_studio/routes.py` — Subjects / Review / Publishing / Versions / Quality hubs
- `app/presentation/curriculum_studio/forms.py`, `view_models.py` — Publish Verified Curriculum
- `app/presentation/product_language.py`
- `app/services/alpha_onboarding_service.py`, `app/templates/alpha/onboarding.html`
- `app/templates/student/home.html`
- `app/application/unified_journey/session_outcome_assembler.py`
- Related regression tests under `tests/`

---

## Tests Executed

```bash
python3 -m pytest tests/test_px002_product_experience.py \
  tests/test_ptp001_supported_subject_integrity.py \
  tests/test_smoke.py::TestSmokeStudyPlanWizard \
  tests/test_smoke.py::TestFullEndToEnd \
  tests/presentation/curriculum_studio/test_navigation.py \
  tests/presentation/curriculum_studio/test_product_language.py \
  tests/test_console_001_kwalitec_console.py \
  tests/presentation/workflows/test_workflow_founder_nav.py \
  tests/test_routes.py::TestStudyPlanWizardPx002 -q
```

Outcome: focused PX-002 / PTP / smoke / founder-nav suites green after test updates.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved: blueprints → services / application projections → models.
- Curriculum V1/V2 loadable paths unchanged.
- LP-001 `onboard_after_enrolment` still invoked after Study Plan create.
- `FounderStudentEnrolmentBridge` remains enrolment write authority for published subjects.
- No EI / Twin / Runtime / CKG redesign.

---

## Technical Debt

- Deferred wizard fields (position / learning style / target) use calm defaults; progressive disclosure may return later without reintroducing uploads.
- Founder hub pages are thin framing over the existing Studio spine (intentional — no Studio fork).
- Legacy templates `wizard_step_2/4/6/7.html` remain on disk unused by the primary path.

---

## Known Limitations

- Does not improve extraction quality or publish success rates.
- Does not add new subjects to Ready beyond existing support / publication gates.
- Does not redesign Help / History residual jargon beyond Home / onboarding / catalogue / completion framing.

---

## Exit criteria checklist

| Criterion | Status |
|-----------|--------|
| Operational model faithfully implemented | Met |
| Founder workflow matches PX-001 | Met (nav + hubs) |
| Student workflow matches PX-001 | Met |
| Educational Intelligence unchanged | Met |
| No new architectural debt introduced | Met (presentation-only) |
| Regression tests pass | Met (focused suite) |

---

**End of PX-002 Implementation Report**
