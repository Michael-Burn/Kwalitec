# PX-001 — Implementation Summary

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Design complete (product behaviour / UX / navigation / permissions)  
**Precedence:** This programme’s Operational Model takes precedence over conflicting implementation habits.

---

## 1. Objective

Realign the **visible product** so Founder and Student experiences match the intended operational model:

| Persona | Role | Responsibilities |
|---------|------|------------------|
| **Founder** | Curriculum Authority | Create subjects, upload official CMP & syllabus, review/correct extraction, publish verified curriculum, version management, curriculum QA |
| **Student** | Learner | Select an available exam (subject), enter exam date & study availability, begin studying — consume **published** curricula only |

Educational Intelligence (Twin, Decisions, Runtime, Experience Models, Knowledge Graph) is **not** redesigned. It personalises learning **after enrolment**.

---

## 2. What already aligns (do not rebuild)

| Invariant | Current evidence | PX-001 stance |
|-----------|------------------|---------------|
| Founder-only curriculum upload / publish | All `/console/studio` routes use `@founder_required` | **Preserve** |
| Students never upload CMP / syllabus | No student upload endpoints | **Preserve** |
| Separate layout shells | Console sidebar vs EOS student topnav | **Preserve shells; reshape Founder nav** |
| Published-only student consumption | `PublishedCurriculumPackage` + `is_student_consumable()` | **Preserve** |
| EI starts after enrolment | LP-001 `onboard_after_enrolment` on wizard / bridge | **Preserve — do not bypass LP-001 or VP-001** |
| Domain foundation lifecycle | `CREATE_SUBJECT → … → PUBLISH` in `lifecycle.py` | **Preserve stage order; present as Founder Studio workflow** |

---

## 3. What must change (product surface)

| Change | Gap today | Target |
|--------|-----------|--------|
| **Subject Catalogue** | Exam selection buried in study-plan wizard steps 1–2; no first-class catalogue | First-class catalogue: Name, Status, Current Published Edition, Availability (Ready / Coming Soon), Version, Release Date |
| **Founder Studio navigation** | Console nav is a broad ops portal (Operations, Students, Learning, Assessments, Platform, …) with Content as one item | Curriculum-management primary nav: Subjects, Curriculum Studio, Review Queue, Publishing, Versions, Quality |
| **Student experience** | “Published Curriculum” category names founder pipeline; wizard is 7–8 steps including Learning Style / Target | Choose Exam → Exam Date → Study Availability → Begin Learning; no authoring concepts |
| **Availability labels** | PTP-001: Supported / Coming Soon / Not Supported | Student-facing: **Ready** / **Coming Soon**; unavailable not selectable; professional “under preparation” message |
| **Terminology** | Studio exposes CIP / Knowledge Graph / Evidence Explorer; student path still carries Study Sensei, Decision Journal, etc. | Domain terms: Subject, Study Plan, Today’s Focus, Verified Curriculum |
| **Navigation separation** | Shells separate; founders with student role can dogfood `/student/*`; shared account settings link | Keep shells independent; never expose Founder concepts on student chrome |

---

## 4. Explicit non-goals

- Do **not** redesign Educational Intelligence cores (EI-004…EI-007, Twin, CKG internals).
- Do **not** duplicate Runtime Integration behaviour (RI-001 / RI-002).
- Do **not** bypass LP-001 enrolment orchestration or VP-001 journey wiring.
- Do **not** invent speculative educational logic in presentation.
- Do **not** rename or collapse internal domain enums unless a later implementation programme scopes that work.

---

## 5. Implementation phases (recommended)

### Phase A — Documentation & contract (this delivery)

Produce the seven PX-001 artefacts. No application code change required for programme close on design scope.

### Phase B — Subject Catalogue + student onboarding (follow-on)

1. Introduce a Subject Catalogue read model projected from `StudioFoundationSubject` + active `PublishedCurriculumPackage`.
2. Student entry: Welcome → Choose Exam (catalogue) → Exam Date → Study Availability → Begin Learning.
3. Map catalogue **Ready** to existing support gate that allows enrolment; **Coming Soon** / unavailable block selection with preparation copy.
4. Remove student-visible “Published Curriculum” / Curriculum Studio language from wizard / catalogue copy.
5. Keep LP-001 onboard and `FounderStudentEnrolmentBridge` as write authority after enrolment.

### Phase C — Founder Studio navigation reshape (follow-on)

1. Primary Console nav becomes curriculum-authority workflows (see `NAVIGATION_CHANGES.md`).
2. Relabel Studio tabs to Founder-domain language where student-calm is not the issue but founder clarity is (`TERMINOLOGY_CHANGES.md`).
3. Keep CIP / Knowledge Graph APIs founder-only; optionally demote engineering tab labels behind “Advanced” or Quality tools.
4. Operational Console destinations (Platform, Runtime Health, etc.) move to secondary / Settings hubs — not removed from product.

### Phase D — Hardening

1. Regression tests: no student route can upload documents or publish.
2. Catalogue never lists draft / processing / failed editions as Ready.
3. Copy review against FV-001 terminology audit + this programme’s glossary.

---

## 6. Success criteria checklist

| Criterion | Design status | Code status |
|-----------|---------------|-------------|
| Founder creates subjects | Specified; already implemented | **Met** in Studio |
| Founder publishes verified curricula | Specified; already implemented | **Met** (publish path exists; quality of extraction is separate) |
| Students never upload learning material | Specified; already enforced | **Met** |
| Students study only published subjects | Specified; discovery + `is_student_consumable` | **Mostly met** — catalogue UX incomplete |
| Educational Intelligence begins only after enrolment | Specified; LP-001 / VP-001 | **Met** — preserve |
| Internal EI concepts remain hidden from students | Specified; residual jargon on Help / History | **Partial** — terminology programme |

---

## 7. Artefact index

| Deliverable | Path |
|-------------|------|
| Implementation Summary | `PX001_IMPLEMENTATION_SUMMARY.md` (this file) |
| Role Separation Report | `ROLE_SEPARATION_REPORT.md` |
| Subject Catalogue Design | `SUBJECT_CATALOGUE_DESIGN.md` |
| Navigation Changes | `NAVIGATION_CHANGES.md` |
| Terminology Changes | `TERMINOLOGY_CHANGES.md` |
| Updated Founder Flow | `UPDATED_FOUNDER_FLOW.md` |
| Updated Student Flow | `UPDATED_STUDENT_FLOW.md` |

---

## 8. Dependencies & constraints

| Upstream | Constraint |
|----------|------------|
| PI-001A–D | Curriculum Studio foundation spine — reuse, do not fork |
| PI-002A | Enrolment bridge — student still enrols via published package |
| LP-001 | Onboard / evidence orchestration — do not bypass |
| VP-001 | Preferred Authority chain after enrolment — do not duplicate |
| PTP-001 | Support gating — remap student labels Ready / Coming Soon |
| FV-001 | Terminology & journey evidence — inform copy changes |
| DEP-003 | EOS student navigation architecture — extend, do not revive dual-home |

---

## 9. Verdict

**Authority boundary (who may author curriculum) is already correct in code.**  
**Presentation boundary (what each persona sees and how they navigate) is the PX-001 gap.**

PX-001 closes that gap by defining Subject Catalogue, Founder Studio nav, student onboarding without uploads, availability messaging, and domain terminology — without touching Educational Intelligence architecture.

---

**End of Implementation Summary**
