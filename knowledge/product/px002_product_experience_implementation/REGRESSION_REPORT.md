# PX-002 — Regression Report

**Programme:** PX-002  
**Date:** 2026-07-28

---

## Invariants maintained

| Invariant | Evidence |
|-----------|----------|
| Founder-only curriculum authoring | Studio routes remain `@founder_required`; hubs founder-only |
| Student-only learning workflow | EOS student shell unchanged; no upload routes for students |
| LP-001 enrolment | `onboard_after_enrolment` still called after Study Plan create |
| VP-001 Preferred Authority | Not modified; post-enrolment chain unchanged |
| PI-001 Studio spine | Hubs frame existing Studio; no fork |
| No EI regressions | No changes under educational intelligence cores / twin / decisions |

---

## Automated coverage

| Suite | Role |
|-------|------|
| `tests/test_px002_product_experience.py` | Catalogue Ready/Coming Soon; founder nav; no upload language; hubs |
| `tests/test_ptp001_supported_subject_integrity.py` | Ready labels; Coming Soon gate; hollow-plan refusal |
| `tests/test_smoke.py::TestSmokeStudyPlanWizard` | Full PX-002 onboarding → plan create |
| `tests/test_smoke.py::TestFullEndToEnd` | Journey through new wizard |
| `tests/presentation/curriculum_studio/test_navigation.py` | Curriculum Authority primary nav |
| `tests/test_console_001_kwalitec_console.py` | Console nav structure |
| `tests/presentation/workflows/test_workflow_founder_nav.py` | Founder workflow nav order |
| `tests/test_routes.py::TestStudyPlanWizardPx002` | Begin Learning redirects / Coming Soon block |

---

## Manual quality gates (per screen)

1. Who is this screen for? — Documented in Screen Change Register.  
2. What should they do next? — Documented.  
3. Is unnecessary implementation detail hidden? — Yes on student path.  
4. Does terminology match the approved glossary? — Ready / Coming Soon / Subject / Study Plan / Today's Focus / Verified Curriculum.

---

## Residual risk

- Broader CI matrix beyond focused suites should be run before release merge.  
- Residual Help / History jargon outside this programme’s touched surfaces may remain (PX-001 residual).  

---

**End of Regression Report**
