# PX-001 — Navigation Changes

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Design (authoritative for persona navigation)

---

## 1. Principle

Founder and Student navigation must be **completely independent**.  
Avoid exposing Founder concepts to Students.  
Do not merge shells or revive legacy dual-home under sole runtime (DEP-003).

---

## 2. Current state (baseline)

| Persona | Shell | Primary nav today |
|---------|-------|-------------------|
| Founder | `layouts/console_base.html` | Overview · Operations · Students · Learning · Assessments · **Content** · Analytics · Platform · Settings · Support |
| Student | `layouts/eos_student.html` | Home · Journey · Revision · History · Settings · Study Plan · Help (feature mode) |

Curriculum Studio lives under `/console/studio` and is linked as **Content**.

---

## 3. Target — Founder navigation (Curriculum Authority)

Founder primary navigation becomes a **curriculum management experience**.

### Primary items (required framing)

| Nav label | Purpose | Maps to (existing or elevated) |
|-----------|---------|--------------------------------|
| **Subjects** | Create / list subjects | Studio subject dashboard / new Subjects hub |
| **Curriculum Studio** | Workspace: upload CMP & syllabus, advance workflow | `curriculum_studio` workspace |
| **Review Queue** | Review & correct extraction | Studio Review / CIP review queue (founder-facing) |
| **Publishing** | Approve & publish verified curriculum | Publish / approve actions & publication status |
| **Versions** | Edition & version management | Version history / assign version |
| **Quality** | Curriculum QA / validation outcomes | Validate / preview / quality metrics |

Optional secondary (not primary Curriculum Authority chrome):

| Nav label | Purpose |
|-----------|---------|
| Overview | Console home / attention summary |
| Students | Participant list (ops) |
| Platform / Operations | Health, observability — demoted from primary curriculum path |
| Settings / Support | Account & feedback |

### Founder workflow reflected in nav order

```
Subjects → Curriculum Studio → Review Queue → Publishing → Versions → Quality
```

This matches:

New Subject → Upload CMP → Upload Syllabus → Extraction → Review → Corrections → Publish → Available to Students.

### What to remove or demote from primary Founder nav

| Current item | Action |
|--------------|--------|
| Content (single catch-all) | Replace with the curriculum items above |
| Learning / Assessments as primary | Demote — not Curriculum Authority core |
| Platform / Analytics as primary | Demote to secondary hubs |
| “Curriculum Intelligence Pipeline” as a nav brand | Do not use as top-level student-visible or calm-founder label; keep under Studio / Quality tools |

Twin diagnostics (`/founder/twin`) remain founder-only and **out of student nav**; keep off primary curriculum strip unless needed under Quality / Advanced.

---

## 4. Target — Student navigation

### Keep (learning OS)

| Item | Notes |
|------|-------|
| Home (Today’s Focus / Mission framing per terminology plan) | Primary daily surface |
| Journey | Progress narrative |
| Revision | When in product scope |
| History | Past activity |
| Study Plan | Plan management — not authoring |
| Settings | Account preferences |
| Help | Student support — no Studio manuals |

### Remove / never introduce on student nav

| Concept | Rule |
|---------|------|
| Upload CMP / Syllabus | Forbidden |
| Publish Curriculum | Forbidden |
| Knowledge Graph | Forbidden |
| Extraction / Review Queue | Forbidden |
| Curriculum Studio / Console | Forbidden |
| Subjects (Founder management) | Forbidden — students see **catalogue selection**, not management |
| Versions (authoring) | Forbidden — version may appear as metadata on a Ready subject only |

### Onboarding chrome (pre-nav)

Before the full student nav is meaningful:

```
Welcome → Choose Exam → Exam Date → Study Availability → Begin Learning
```

During onboarding, prefer a minimal chrome (logo + progress) — not Console sidebar, not full learning IA.

---

## 5. Independence rules

1. Student templates must not render `COMMAND_CENTRE_NAV` or Studio sidebar fragments.  
2. Console templates must not render EOS learning IA as if Founders were students mid-authoring.  
3. Cross-links: Founder may open student dogfood via an explicit “View as student” or manual URL — never via student primary nav items that point at Studio.  
4. Shared `settings` pages: account-only; no “Open Curriculum Studio” for student-role-only users.  
5. Login landing: Founders → Console; Students → onboarding / catalogue / Home (existing auth law).

---

## 6. Implementation notes (follow-on)

| Change | Likely touchpoints |
|--------|--------------------|
| Founder primary nav reshape | `app/founder/dashboard/nav.py`, `_sidebar.html` |
| Subjects hub | Curriculum Studio dashboard elevation |
| Review / Publishing / Versions / Quality | Routes or deep-links into existing Studio tabs — prefer hub pages over raw CIP API names |
| Student catalogue entry | New route under `/student` or first wizard step rewrite; `presentation/student/navigation.py` unchanged for post-enrolment IA |
| Copy | Strip “Published Curriculum” / Studio language from student discovery |

Do not register Studio blueprints without `@founder_required`.

---

## 7. Acceptance checks

- [ ] Founder primary nav reads as curriculum management  
- [ ] Student nav contains zero authoring destinations  
- [ ] Choosing a subject never requires Console  
- [ ] Coming Soon subjects never appear as nav destinations that start enrolment  
- [ ] Sole-runtime EOS shell remains student-only chrome  

---

**End of Navigation Changes**
