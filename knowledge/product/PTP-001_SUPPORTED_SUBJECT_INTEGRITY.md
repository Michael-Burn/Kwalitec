# PTP-001 — Supported Subject Integrity

**Capability ID:** PTP-001  
**Programme:** Product Trust Programme  
**Title:** Supported Subject Integrity  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-15  
**Nature:** Product trust — examination support gating before study-plan creation  

---

## Purpose

Ensure students can never accidentally create a misleading study plan for an
unsupported examination.

This capability closes Blind Internal Alpha Review v2 Release Blocker 1 — the
**hollow-subject trap**: a student could complete onboarding for a paper that
produced a beautiful empty plan with no syllabus and no warning.

---

## Educational meaning

Support status answers one student question before any planning investment:

> “Does this paper actually work in Kwalitec?”

| State | Student meaning |
|-------|-----------------|
| **Supported** | Kwalitec has the official syllabus and can build a complete study plan. |
| **Coming Soon** | This paper is on the roadmap, but is not ready; creating a plan now would be incomplete. |
| **Not Supported** | This examination is outside Version 1; a full plan cannot be created. |

Support status is **product honesty**, not a new educational authority. It does
not change Estimated Knowledge, Evidence, Mission selection, or readiness maths.

---

## Support-state model

```
On-disk official syllabus present?
        │
        ├── Yes  →  Supported  →  plan creation allowed
        │
        └── No
                │
                ├── Announced as Coming Soon (IFoA roadmap papers)
                │         →  Coming Soon  →  explain + block
                │
                └── Otherwise
                          →  Not Supported  →  explain + stop + alternatives
```

### Version 1 Supported examinations

Discovery is **curriculum-driven** via `CurriculumEngineService.list_supported_exams`
(currently IFoA CS1, CM1, CB2). Adding a loadable syllabus promotes a paper to
Supported without a second hardcoded “supported” map of topics.

### Coming Soon

Product announcement list for IFoA papers without a syllabus yet
(e.g. CS2, CM2, CB1, CB3, CP1–CP3, SP, SA). Presence of an on-disk syllabus
overrides Coming Soon.

### Not Supported

All other catalogue selections, including free-text University / Other subjects
and non-IFoA examining bodies without a Version 1 syllabus.

### Ownership

| Concern | Owner |
|---------|--------|
| Support resolution + student messaging | `SubjectSupportService` |
| Catalogue listing (papers/sittings) | `examination_catalogue` |
| Syllabus truth | Curriculum engine / on-disk JSON |
| HTTP gating | Study Plan wizard routes (thin) |

---

## Student messaging

Plain educational language only. Forbidden in student copy:

- curriculum loading / JSON / loader / disk / engine terminology
- implementation version strings as product claims

### Surfaces

| Surface | Behaviour |
|---------|-----------|
| Wizard step 1 | Examining body cards show Supported / Partially Supported / Coming Soon / Not Supported with a short hint |
| Wizard step 2 | Each paper shows its badge; Next on non-Supported stays on step 2 with a gate explanation |
| Gate panel | Title, explanation, and Supported alternatives where appropriate |
| Steps 3–7 / Review | Fail-closed redirect to step 2 if selection is not Supported |
| Review POST | Refuses plan creation when support does not allow it; never creates a hollow shell |

### Example messages

**Coming Soon (CM2)**  
“IFoA CM2 is coming soon… Creating a plan now would produce an incomplete study plan…”

**Not Supported (CFA Level I)**  
“…is not available in Version 1… Please choose a supported paper instead.”

**Alternatives**  
Supported papers are listed by examination name and plain description (e.g. IFoA CS1 — Actuarial Statistics 1).

---

## Behaviour summary

| Selection | Plan creation | Student outcome |
|-----------|---------------|-----------------|
| Supported | Proceed normally | Full wizard → curriculum-bound study plan |
| Coming Soon | Blocked | Clear explanation; stay on / return to paper step |
| Not Supported | Blocked | Clear explanation + supported alternatives |

---

## Release implications

- Mandatory for Version 1 conditional GO (Blind Review v2 Release Blocker 1).
- Marketing / positioning must remain: adaptive study planner and honest practice tracker **for supported subjects**.
- Expanding Version 1 support means shipping a loadable official syllabus (and import), not widening the catalogue alone.
- Existing programmatic `StudyPlanService.create_study_plan` paths used in tests/internal tooling are unchanged; the **student wizard and review** path is fail-closed.

---

## Out of scope

- Redesign of Educational Constitution, Learning Experience Programme, curriculum engine internals, Digital Twin, or Educational Intelligence
- Building hollow “limited mode” plans for unsupported papers
- New examining-body content beyond labelling and gating

---

## Cross references

| Document | Relationship |
|----------|--------------|
| `PRODUCT_TRUST_PROGRAMME.md` | Programme parent; PTP-001 capability brief |
| `BLIND_INTERNAL_ALPHA_REVIEW_V2.md` | Hollow-subject trap evidence |
| `app/services/subject_support_service.py` | Implementation |

---

**End of PTP-001 Supported Subject Integrity.**  
**Stop. Return for Architecture Review.**
