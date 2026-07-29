# PX-001 — Role Separation Report

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Authoritative for product behaviour / permissions / UX boundaries

---

## 1. Personas (authoritative)

### Persona 1 — Founder (Curriculum Authority)

The Founder is the **only** role permitted to create or modify curricula.

| Allowed | Forbidden for Founder-as-Authority (product framing) |
|---------|------------------------------------------------------|
| Create subjects | Treating students as co-authors of curriculum |
| Upload official CMP | Exposing unfinished extraction to students |
| Upload official syllabus | Publishing without review |
| Review extraction | Bypassing version / quality gates |
| Correct extraction | |
| Publish verified curriculum | |
| Version management | |
| Curriculum quality assurance | |

Founder **dogfooding** as a learner (same account holding `student` role) remains an Internal Alpha operational practice. It must not blur **chrome**: when acting as Founder, the Console / Studio; when acting as Student, the EOS shell with no authoring controls.

### Persona 2 — Student (Learner)

Students **never** upload learning material.

| Allowed | Forbidden |
|---------|-----------|
| Select an available exam (subject) | Upload CMP / syllabus |
| Enter exam date | Publish curriculum |
| Enter study availability | See Knowledge Graph / extraction / CIP |
| Begin studying published subjects | Browse Curriculum Editions as authoring artefacts |
| Consume Verified Curriculum via Study Plan / Home | Create or modify subjects |

Educational Intelligence personalises learning **after** enrolment (LP-001 → EI platform). Students do not configure intelligence systems.

---

## 2. Current enforcement vs target

| Boundary | Current | Target | Gap |
|----------|---------|--------|-----|
| HTTP upload / publish | `@founder_required` on `/console/studio` | Same | **None** (authority OK) |
| Student upload routes | None | None | **None** |
| Layout shells | Console vs EOS | Completely independent | **Mostly met** |
| Founder primary job framing | Broad ops Console | Curriculum management Studio | **Presentation gap** |
| Student subject entry | Wizard + “Published Curriculum” category | Subject Catalogue (Ready / Coming Soon) | **UX gap** |
| Role model | Multi-role users (`founder` + `student`) | Multi-role OK for dogfood; surfaces must not mix concepts | **Clarify policy** |
| Shared settings | Console topbar → `settings.index` | Account settings may be shared; never leak Studio into student nav | **Minor** |

---

## 3. Permission matrix (product law)

| Capability | Founder | Student | Notes |
|------------|---------|---------|-------|
| Create subject | ✓ | ✗ | `curriculum_studio.create_subject` |
| Upload official CMP / syllabus | ✓ | ✗ | Document upload services |
| Run / retry extraction pipeline | ✓ | ✗ | Founder Studio |
| Review / correct extraction | ✓ | ✗ | Review Queue |
| Publish verified curriculum | ✓ | ✗ | `PublicationService` |
| Assign / manage versions | ✓ | ✗ | Version history |
| Curriculum quality tools | ✓ | ✗ | Validation, QA views |
| View Subject Catalogue (student projection) | ✓ (ops) | ✓ | Students see Ready / Coming Soon only |
| Select Ready subject | — | ✓ | Enrolment path |
| Select Coming Soon / unavailable | — | ✗ | Message only |
| Enter exam date / availability | — | ✓ | Onboarding |
| Study sessions / Home / Journey | — | ✓ | After enrolment |
| Twin / Runtime diagnostics | ✓ | ✗ | Remain founder-only |
| Knowledge Graph UI | ✓ | ✗ | Never on student chrome |

Internal capabilities (`Permission.CURRICULUM_MANAGE`, `CONSOLE_ACCESS`) continue to back Founder access. PX-001 does not invent a parallel RBAC stack.

---

## 4. Separation rules

1. **Authoring surface = Console / Founder Studio only.**  
2. **Learning surface = EOS student shell only.**  
3. **No Founder nav items on student navigation** (DEP-003 EOS inventory remains the student tree).  
4. **No student-facing labels** for CMP upload, syllabus upload, publish, extraction, Knowledge Graph, Curriculum Intelligence Pipeline, or Curriculum Edition authoring.  
5. **Students interact with Subjects**, not Curriculum Editions. Edition identity may appear as Version / Release Date on catalogue cards only when Ready.  
6. **EI concepts stay hidden** on student path (SCI, Twin, Runtime, Educational Decision) — continue FV-001 Critical-term ban.  
7. **After enrolment only** may LP-001 / RI-001 drive personalisation; presentation must not call EI cores directly.

---

## 5. Dogfooding policy

| Practice | Allowed? | Rule |
|----------|----------|------|
| Founder account also has `student` role | Yes (Internal Alpha) | Login landing remains Console for founders |
| Founder manually opens `/student/*` | Yes | Student shell must not show Studio controls |
| Founder uses wizard to enrol into a published subject | Yes | Same student rules apply |
| Student account granted Studio access | No | Curriculum Authority is Founder-only |

---

## 6. Residual risks

| Risk | Mitigation |
|------|------------|
| “Published Curriculum” copy teaches students about founder pipeline | Replace with Subject Catalogue language |
| Console breadth implies Founder is ops engineer, not Curriculum Authority | Reshape primary nav per `NAVIGATION_CHANGES.md` |
| Multi-role accounts confuse UX testing | Document persona under test in FV sessions |
| Settings shared across shells | Keep account-only; no Studio deep links in student Settings |

---

## 7. Verdict

**Role separation at the permission boundary is already correct.**  
**Role separation at the product-experience boundary is incomplete.**  

PX-001’s remaining work is presentation, catalogue, navigation framing, and terminology — not a new Educational Intelligence design.

---

**End of Role Separation Report**
