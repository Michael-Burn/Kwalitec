# DX-006B Phase 5 — Choose Exam Completion Report

**Programme:** DX-006B — Founder & Student Surface Migration  
**Phase:** 5 — Choose Exam  
**Authority:** DX-005B Exam Commitment (Discovery First)  
**Status:** Implementation complete — awaiting independent review  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01`  
**Design freeze tag:** `v2.0.0-design-freeze`  
**Foundation Gate:** CERTIFIED  
**Founder OS:** CERTIFIED  
**Student Home:** CERTIFIED (programme authority for this phase entry)

---

## Executive Summary

Legacy Choose Exam / Study Plan wizard discovery (`wizard_step_1.html` option-card grid, Study Plan progress theatre, multi-section review with twin Yes/No confirm) was **replaced** with the DX-005B Exam Commitment architecture: one H1 (**Choose Exam**), L1 search/filters, L0 Ready catalogue (single-select), Selected Exam Summary, quiet Coming Soon band, exactly one discovery Primary (**Continue** → existing date/availability path), and confirm Primary (**Begin Learning**) with text Secondary **Change selection**. Presentation composes only `design_system/macros.html` and loads `design_system.css`. Catalogue projection, support gating, enrolment, and study-plan creation are unchanged.

**Recommendation: GO WITH CONDITIONS** — ready for independent Phase 5 review. Do not start Phase 6 (Study Session) until certified.

---

## Architecture Implemented

| Layer | Implementation |
|---|---|
| **H1** | `Choose Exam` via `ds-page-header` |
| **L1** | Search exams · Family (when ≥2 codes) · Status · Sort |
| **L0** | Ready to begin — selectable radio list (`ds_exam_ready_list`) |
| **Summary** | Selected exam panel (exam · stage · path · duration · next step) |
| **Primary (discovery)** | Continue — advances to quiet exam-date step |
| **Primary (confirm)** | Begin Learning — sole filled commitment CTA |
| **Secondary** | Back · Change selection · Coming Soon informational (Notify omitted — no backend) |
| **Coming Soon** | Secondary band below Ready — never Begin Learning |
| **Empty** | No Ready subjects yet → Return later |

One question answered: **Which exam am I committing to?** (DX-005B: which exam do I want to begin?)

---

## Legacy Removed

Deleted / replaced (not CSS-hidden):

- Study Plan eyebrow + step indicator + progress bar / dots theatre  
- Marketing helper essays on discovery  
- Decorative option-card grid with book icons + badge clusters  
- Multi-section review (Position / Learning Style / Target as decided theatre)  
- Twin Yes/No filled confirm radios  
- **Next** as peer Primary labels (→ Continue on intermediate; Begin Learning on confirm)  
- Orphan templates `wizard_step_2/4/6/7.html`  
- Unused wizard CSS (progress, review sections, option cards, KPI-like chrome)  
- Nav label **Study Plan** → **Choose Exam**

---

## Shared Components Used

| Component | Source |
|---|---|
| Exam Ready list | `ds_exam_ready_list` (new catalogue macro) |
| Coming Soon band | `ds_exam_coming_soon` |
| Selected / Confirm summary | `ds_selected_exam_summary` / `ds_exam_confirm_summary` |
| Search / Select / Toolbar | `ds_search_input` / `ds_select` / `ds_toolbar` |
| Empty operational | `ds_empty_operational` |
| Button / Primary strip | `ds_button` / `ds-primary-strip` / `ds-btn--primary` |
| Page / container | `ds-page`, `ds-container--content`, `ds-page-header` |

No page-specific primitives. Rejected KPI components unused. Founder `ds_subject_catalogue` not used (wrong link model).

---

## Foundation Imports

- Python: Choose Exam DTO via student presentation service; catalogue via existing `SubjectCatalogueService`.  
- Template: `{% from "design_system/macros.html" import … %}` only.  
- CSS: `design_system.css` (+ slim `wizard.css` for quiet intermediate field chrome only).  
- **No** imports from `presentation.design_system.components.*` on the Choose Exam path.

---

## Files Modified

- `app/templates/study_plan/wizard_step_1.html` — full DX-005B discovery replacement  
- `app/templates/study_plan/wizard_base.html` — quiet commitment chrome  
- `app/templates/study_plan/wizard_step_3.html` / `wizard_step_5.html` — Continue, quieter copy  
- `app/templates/study_plan/review.html` — Confirm + Begin Learning only  
- `app/templates/design_system/macros.html` — exam discovery macros  
- `app/templates/partials/subject_support_gate.html` — copy alignment  
- `app/static/css/design_system.css` — exam row / summary styles  
- `app/static/css/wizard/wizard.css` — slim to quiet field chrome only  
- `app/study_plan/routes.py` — discovery DTO wiring; quiet confirm payload  
- `app/study_plan/forms.py` — Continue / HiddenField confirm  
- `app/presentation/student/navigation.py` — Choose Exam nav label  
- Tests: navigation, terminology, premium chrome, PTP-001 surface, student routes  
- `knowledge/implementation/dx006b/PHASE_TRACKER.md`  
- `.cursor/rules/99-CURRENT_MILESTONE.md`

## Files Created

- `app/presentation/student/dto/choose_exam.py`  
- `app/presentation/student/services/choose_exam_service.py`  
- `tests/test_dx006b_choose_exam.py`  
- `knowledge/implementation/dx006b/DX006B_PHASE5_CHOOSE_EXAM_COMPLETION_REPORT.md`

## Files Deleted

- `app/templates/study_plan/wizard_step_2.html`  
- `app/templates/study_plan/wizard_step_4.html`  
- `app/templates/study_plan/wizard_step_6.html`  
- `app/templates/study_plan/wizard_step_7.html`

---

## Behaviour Changes

| Change | Notes |
|---|---|
| Discovery UI | Ready/Soon bands + search/filters; single-select list |
| Discovery Primary | Continue → existing exam date → availability → confirm |
| Confirm | Begin Learning only; Change selection returns to L0 |
| Nav | Study Plan → Choose Exam |
| Unchanged | Auth, support fail-closed gate, enrolment bridge, study-plan create, Calibration redirect, API/routing contracts, curriculum V1/V2 |

---

## Accessibility Result

**PASS**

- One H1 (`Choose Exam`) on discovery and confirm  
- Ready list as `radiogroup` with labelled radios  
- Primary has accessible name = Continue / Begin Learning  
- Search labelled; filters labelled  
- Status as text bands (not colour alone)  
- Keyboard: search → filters → radios → Primary → Back/Change selection  
- Focus-visible via DS tokens  

---

## Responsive Result

**PASS**

- Single column content container  
- DS Primary strip full-width &lt;768px  
- Toolbar stacks on mobile  
- Summary definition list collapses to single column on mobile  
- Ready selection remains first actionable region after heading  

---

## Guardian Result

| Rule | Status |
|---|---|
| G-1 One Primary | PASS (Continue on discovery; Begin Learning on confirm — not peers) |
| G-2 Hierarchy | PASS (L0→L2) |
| G-3/G-5 Tokens | PASS |
| G-4 No hard-coded colours | PASS |
| G-6 No KPI / vanity | PASS |
| G-7 No gamification | PASS |
| G-8 Decision clarity | PASS |
| G-9 Copy density | PASS |
| G-10 No duplicate nav | PASS |
| G-11 Catalogue only | PASS |
| G-12 Rejected unused | PASS |

**Guardian: PASS**

---

## Regression Result

| Suite | Outcome |
|---|---|
| `tests/test_dx006b_choose_exam.py` | PASS (5) |
| `tests/test_smoke.py::TestSmokeStudyPlanWizard` | PASS |
| `tests/test_ptp001_supported_subject_integrity.py` (wizard surface) | PASS |
| `tests/test_px002_product_experience.py` (Choose Exam language) | PASS |
| `tests/presentation/test_dep003_unification.py` | PASS |
| Navigation / terminology / premium chrome updates | PASS |
| `tests/test_dx006b_student_home.py` | PASS (no regression) |

---

## Decision Test Result

**PASS (provisional — structural)**

Within five seconds the learner sees:

1. **What exams are available** — Ready to begin list  
2. **Which exam is selected** — radio selection chrome + Selected exam summary  
3. **How to continue** — exactly one Primary Continue  

Live dogfood timing pending independent review.

---

## Architectural Fidelity

| Category | Score | Notes |
|---|---:|---|
| Matches DX Architecture | 29/30 | Multi-step date/availability retained with quiet Continue; Begin Learning on confirm per DX-005B intermediate-path law. Notify omitted (honesty). |
| Shared Components | 19/20 | New catalogue macros in shared macros.html; no page-local primitives |
| Token Compliance | 15/15 | DS tokens only |
| Guardian Compliance | 15/15 | G-1…G-12 |
| Accessibility | 10/10 | |
| Performance | 9/10 | Slim discovery DTO; live &lt;3s dogfood pending |
| **Total** | **97/100** | ≥95 PASS |

---

## Premium Score

| Dimension | Score |
|---|---:|
| Discovery Clarity | 10 |
| Decision Clarity | 10 |
| Commitment Honesty | 10 |
| Information Density | 9 |
| Professional Tone | 10 |
| Minimalism | 10 |
| Navigation Clarity | 9 |
| Handoff Continuity | 10 |
| Overall Premium Feel | 10 |

**All dimensions ≥9. Premium: PASS (provisional pending live review).**

---

## Known Issues

1. Intermediate exam-date and availability steps remain (quiet Continue) — not fully collapsed into Confirm; Alpha still requires those facts for Mission creation.  
2. Notify when available omitted (no backend) — Coming Soon is informational only.  
3. Shell still includes Journey / Revision alongside Choose Exam (DX-005A target ≤6 items) — deferred chrome pass.  
4. Plan list / view / edit retain “Study Plan” product nouns for active-plan management (not discovery L0).  
5. Live five-second dogfood and independent Premium certification pending.

---

## Technical Debt

- Legacy form classes for orphaned steps remain in `forms.py` (compat); templates deleted.  
- Small progressive-enhancement script on discovery for live summary / Continue enablement.  
- `wizard.css` retained only for quiet intermediate field chrome — further collapse into DS form primitives is optional follow-up.

---

## Recommendation

**GO WITH CONDITIONS**

Ready for independent Phase 5 review and certification.  
**Do not begin Phase 6 (Study Session) until Choose Exam is independently reviewed and CERTIFIED.**

Conditions:

1. Independent Architectural Fidelity + Premium review on live UI  
2. Confirm five-second decision clarity with a student walkthrough  
3. Accept quiet multi-step Continue path until a later collapse into Confirm  

---

## Summary

Choose Exam now matches DX-005B: discovery-first, single selection, Ready/Soon honesty, one Primary per step, no dashboard / KPI / marketing chrome, shared Foundation only.

Release Candidate: `RC-2026.07.29-01`
