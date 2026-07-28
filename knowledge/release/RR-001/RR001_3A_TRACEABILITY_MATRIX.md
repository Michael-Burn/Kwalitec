# RR-001.3A — Traceability Matrix

**Programme:** RR-001 — Governance-driven Educational Remediation  
**Work Package:** RR-001.3A — Educational Identity & Narrator Consistency  
**Date:** 2026-07-28  
**Rule:** Every implementation references EGC NCR → governance clause → modified file → student impact.  
**Companion:** `RR001_3A_COMPLETION_REPORT.md`

---

## Traceability matrix

| EGC NCR | Governance clause(s) | Modified file(s) | Student impact |
|---------|----------------------|------------------|----------------|
| **NCR-001** | DG-001.1-D01; DG-001.2-D04; CI-05; CP-04; CP-10; T04 | `app/services/alpha_onboarding_service.py`; `app/templates/alpha/onboarding.html` | Learner meets Study Sensei before Home; no longer learns Kwalitec-as-tutor |
| **NCR-018** | DG-001.2-D04; CI-05; CP-04; CP-10; AC-01/04/05 | Same + `app/templates/partials/welcome_modal.html`; `app/templates/student/home.html` (`data-narrator`) | Explicit handoff + Home narrator signal; transitions no longer silent |
| **NCR-014** | DG-001.2-D07; DEP-04; Constitution §11; ED-11 | `app/templates/student/components/educational_experience.html` | If Runtime C enabled, disclosure is Mission-owned — not “the system” |
| **NCR-015** | DG-001.1-D02; DEP-01; DEP-02; CP-03; CI-01 | Onboarding copy; welcome modal; `mission/index.html`; `dashboard/index.html`; commitment continuity; explanation card; `product_language.py` | Mission = focus; Session = practice; tip retired as daily-focus noun |
| **NCR-020** | CP-03; CI-01; DG-001.1 lexicon; DEP-* | Same lexicon surfaces + Home Coach→Sensei labels; MI axis chrome | Live strings match Board vocabulary on in-scope path |
| **NCR-016** *(card)* | DEP-01; DG-001.2-D01; CP-07 | `app/templates/student/components/explanation_card.html` | Explainability disclosure owned as guidance, not tip slang |
| **NCR-004** *(continuity)* | DEP-01; DG-001.3-D07; ED-06 | `app/application/student_experience/recommendation_commitment.py` | Commitment close uses Mission vocabulary |
| **NCR-002** *(narrator portion)* | D01; D05; CP-04; CP-10; OQ-02 | `app/templates/student/home.html` | Sensei named on Home; Guidance panel replaces Coach chrome |

---

## Package mapping

| Remediation ID | Scope in RR-001.3A | Status |
|----------------|--------------------|--------|
| **EGC-R01** | Handoff, Sensei attribution, narrator transitions on educational core | **Implemented** (in-scope) |
| **EGC-R02** | Tip / Mission / Session lexicon on educational identity surfaces | **Implemented** (in-scope; OQ-01 PX docs residual noted) |
| EGC-R03 | Help map | Out of scope |
| EGC-R07 | Flag speech beyond Runtime C rename | Contained rename done; enablement still ops |
| EGC-R08 | Continuous Home naming density policy | Partial (Sensei named once); OQ-02 open |
| EGC-R12 | Journal/Timeline empty honesty | Out of scope |

---

## Authority transition IDs exercised

| Transition | Evidence |
|------------|----------|
| **T04** | Onboarding step `sensei` + welcome body handoff sentence |
| **T05** | Home `data-narrator="study-sensei"` |
| **T06–T08** | MI disclosure + explanation card Sensei/guidance ownership (composition unchanged) |
| **T09** | Session overview Sensei intro + Mission≠Session sentence |

---

## Explicit non-claims

| Item | Why not claimed |
|------|-----------------|
| Full product DG-001 compliance | Journal/Help/History/reflection map remain NC/PC |
| ED-01 closed product-wide | Help + memory introduction still lag (EGC-R03) |
| Recommendation behaviour change | Forbidden by WP constraints |
| MI composition change | Presentation chrome only |

---

**End of RR001_3A_TRACEABILITY_MATRIX**
