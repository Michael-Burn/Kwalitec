# PX-002 — Navigation Implementation Report

**Programme:** PX-002  
**Date:** 2026-07-28  
**Authority:** `NAVIGATION_CHANGES.md` (PX-001)

---

## Principle

Founder and Student navigation remain completely independent. No Founder concepts on student chrome.

---

## Founder primary navigation (implemented)

Order:

```
Overview → Subjects → Curriculum Studio → Review Queue → Publishing → Versions → Quality → Students → Settings → Support
```

| Label | Endpoint |
|-------|----------|
| Subjects | `curriculum_studio.subjects_hub` |
| Curriculum Studio | `curriculum_studio.index` |
| Review Queue | `curriculum_studio.review_hub` |
| Publishing | `curriculum_studio.publishing_hub` |
| Versions | `curriculum_studio.versions_hub` |
| Quality | `curriculum_studio.quality_hub` |

Demoted to secondary (still reachable): Operations, Learning, Assessments, Analytics, Platform, Runtime Health, etc.

Sidebar tagline: **Curriculum Authority**.

---

## Student navigation (unchanged IA)

Home · Journey · Revision · History · Settings · Study Plan · Help  

Onboarding chrome remains wizard progress (logo + steps), not Console sidebar.

---

## Independence checks

| Rule | Status |
|------|--------|
| Student templates do not render `COMMAND_CENTRE_NAV` | Preserved |
| Console templates do not render EOS learning IA as authoring | Preserved |
| No student nav to `/console/studio` | Preserved |
| Studio routes remain `@founder_required` | Preserved |

---

## Acceptance

- [x] Founder primary nav reads as curriculum management  
- [x] Student nav contains zero authoring destinations  
- [x] Choosing a subject never requires Console  
- [x] Coming Soon subjects are not enrolment destinations  

---

**End of Navigation Implementation Report**
