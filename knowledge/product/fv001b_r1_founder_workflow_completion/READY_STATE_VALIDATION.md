# FV-001B-R1 — Ready State Validation

**Programme:** FV-001B-R1  
**Date:** 2026-07-28

---

## Definition of Ready

A subject is **Ready** when:

1. Curriculum Management has published the Studio-linked version, and
2. Foundation has an active `PublishedCurriculumPackage` for that subject, and
3. Founder Subjects hub shows **Ready · Current Version · Published Date**, and
4. Student Subject Catalogue can discover the subject as Ready (bridge flags permitting).

---

## How Ready is produced

| Step | Authority |
|---|---|
| Studio Approve / Publish | Curriculum Management (unchanged safety) |
| Materialise student package | `PublicationBridgeService` → Foundation `founder_review` + `publish_curriculum` |
| Founder display | Subjects hub reads `PublishedCurriculumAuthority` |
| Student display | `SubjectCatalogueService` — active package → Ready label |

---

## Founder Subjects hub

For each workspace:

- **Ready** when an active Foundation package exists for the subject code  
  Display: `Ready · Current Version {label} · Published {YYYY-MM-DD}`
- **Draft** otherwise  
  Display: version label / workflow stage (unchanged draft behaviour)

---

## Student Subject Catalogue

- Active published package ⇒ availability **Ready** (even if enrolment is still gated)
- `selectable` remains tied to enrolment support (`allows_plan_creation`)
- Development default: when `APP_ENV=development` and no bridge env vars are set, discovery + enrolment flags enable so Ready is observable locally
- Explicit empty environ (tests) and production without flags keep safe defaults **off**

---

## Validation checklist for FV-001B re-run

- [ ] Publish a subject through Founder Studio only
- [ ] Return to **Subjects**
- [ ] Observe **Ready**, current version, and published date
- [ ] As student (or Choose Exam), discover the subject under Ready / Published subjects
- [ ] Confirm Studio counters no longer stuck at Published 0 after a successful walk

---

## Residual risk

- If extraction yields zero topics, preview/publish correctly block — Ready cannot be faked.
- If Foundation documents were never created for the workspace, Management may publish while Ready bridge skips with a warning (unit-test / incomplete upload path). Real Founder uploads create Foundation versions at document upload time.
