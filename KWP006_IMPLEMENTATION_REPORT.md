# KWP-006 — Exam Week Briefing & Home Experience

**Programme:** KWP-006 · Exam Week Briefing & Home Experience  
**Phase:** Commercialisation Phase 6  
**Date:** 2026-07-30  
**Nature:** Presentation / product experience — **no runtime authority redesign**  
**Authority:** KWP-005 · KWP-004 · KWP-003 · SR-001A · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-006 transforms Student Home from a navigation-first decision page into a calm daily **command centre**. The student opens Home and immediately sees today’s Session, syllabus position, Exam Week Briefing, Learning Insights, Study Health / Exam Readiness in stage language, streak and exam countdown — answering *where am I*, *what should I do today*, *am I on track*, *what changed*, and *what to focus on next* without searching or seeing internal architecture.

**Exam Week Briefing** is a new presentation projector over existing History, Journey, Revision, Profile streak, and readiness VMs. It never reproduces CMP content and never redesigns LearningSessionRuntime, Evidence Authority, Student Twin, Progress Engine, Mission Runtime, or the Commercial Loop.

**Verdict:** Missing weekly briefing and under-surfaced Home insights are now production-quality presentation consumers of authorities already built in KWP-002→005 / SR-001A.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | **Home Dashboard** | Exists (SOP-001) → enriched | **MODIFIED** | Mission-first shell retained; added position, briefing, insights. |
| 2 | **Daily Mission** | Exists | **EXISTING** | Mission panel + one Primary CTA unchanged. |
| 3 | **Today's Session** | Exists | **EXISTING** | Start / Continue / day-complete paths reused. |
| 4 | **Journey summary** | Partial on Home | **MODIFIED** | Syllabus position section from Journey / educational VMs. |
| 5 | **Exam countdown** | Exists | **EXISTING** | Remains in study-signals strip. |
| 6 | **Weekly briefing** | Missing for students | **NEW** | Founder briefing exists; student Exam Week Briefing added. Legacy adaptive daily briefing not reused (legacy StudyAttempt path). |
| 7 | **Study streaks** | Exists | **EXISTING** | Profile streak in signals; feeds briefing consistency. |
| 8 | **Notifications** | Flash-only | **EXISTING** | No new notification system — out of scope; flash stack retained. |
| 9 | **Readiness presentation** | Exists but %-led | **MODIFIED** | Stage language primary: Building → Ready for Assessment. |
| 10 | **Session entry** | Exists | **EXISTING** | Start/Continue forms and resume deep-link unchanged. |

### EXISTING (reused)

- `StudentHomeService` + `StudentHomePage` command-centre projection (SOP-001 / DX-006B)  
- Mission panel, study signals, Study Health, Quick Actions, Upcoming  
- Home loads journey / history / revision sibling snapshots (`include_all_surfaces`)  
- Journey Weak Topic Centre + Learning Insights (KWP-005)  
- History mastered topics, sessions, achievements, readiness trend  
- Revision primary / alternatives  
- Readiness card shell (KWP-002)  
- Product Language Guide + forbidden-term scrub  

### NEW

- `app/presentation/student/exam_week_briefing.py` — Exam Week Briefing + Home Insights projector  
- Home template sections: syllabus position, This Week briefing, Learning Insights  
- Design-system styles for briefing / insights / position  
- `tests/test_kwp006_home_exam_briefing.py`  

### MODIFIED

- `StudentHomePage` DTO — briefing, insights, syllabus_position, page question  
- `StudentHomeService` — wires briefing / insights from existing VMs  
- `home_vm` readiness label → stage language; `format_benefit` qualitative  
- `readiness_card.html` — stage hero, percent secondary  
- `home.html` — command-centre composition  
- Product language approved terms  

---

## 3. Home Experience

Home remains the primary post-login entry (PX-003 / SOP-001). Composition order:

1. **Header** — “Where you stand — and what to do today.”  
2. **Today’s Session** — one Primary (Start / Continue / day-complete)  
3. **Why this Session?** — existing explanation disclosure  
4. **Study signals** — subject, streak, progress, exam countdown  
5. **Where you are** — current syllabus position  
6. **This Week** — Exam Week Briefing  
7. **Learning Insights** — changed / weak / achievement / next / milestone  
8. **Study Health** + **Exam Readiness** (stage language)  
9. **Quick Actions** + **Upcoming** milestones  

Tone: calm, minimal, premium — no KPI wall, no engine names.

---

## 4. Exam Week Briefing

**Surface:** Home section titled **This Week** (`data-kwp-section="exam-week-briefing"`).

| Block | Source |
|---|---|
| Strengthened | History `mastered_topics` (fallback: recent session topics) |
| Needs reinforcement | Journey Needs Attention → Revision → History revision topics |
| Study consistency | Excellent / Steady / Building from streak + session count |
| Exam Readiness stage | Existing readiness VM → stage vocabulary |
| Recommended focus | Revision primary → Journey current → educational topic / section |

**Never:** CMP question stems, Twin / Evidence / Progress / Mission jargon, fabricated chapter–question ranges without real syllabus position detail.

---

## 5. Daily Command Centre

Home now answers the five daily questions:

| Question | Home answer |
|---|---|
| Where am I? | Syllabus position + signals |
| What should I do today? | Today’s Session Primary |
| Am I on track? | Study Health + readiness stage + consistency |
| What changed? | “Since last Session” insight / journey story |
| What to focus on next? | Briefing recommended focus + insight next |

Empty / quiet / day-complete states preserved; briefing and insights hide on empty.

---

## 6. Readiness Presentation

**Before:** Readiness card hero was a percentage (`62%`).  
**After:** Hero is stage language:

- Building  
- Developing  
- Strengthening  
- Ready for Revision  
- Ready for Assessment  

Percent retained as quiet secondary (“45% coverage signal”) when available. Study Health mirrors stage labels. Benefit copy uses qualitative lifts instead of “About N% readiness gain”.

---

## 7. Student Impact

| Dimension | Assessment |
|---|---|
| **Student problem** | Home answered “what next?” but not weekly posture, change-since-last, or readiness without searching Journey / History. |
| **Student benefit** | One morning open explains standings, today’s work, and weekly focus. |
| **Learning benefit** | Weak-topic and strengthened signals connect Sitting / History / Revision into a retention loop without overclaiming mastery. |
| **Success metrics** | Briefing non-empty when History/Revision exist; stage language on readiness; zero forbidden internal terms; one Primary CTA preserved. |
| **Risks** | Thin History → thin briefing; students may still want History drill-down to Sitting Reports (deferred). |
| **Assumptions** | Commercial Loop ON for rich sittings; sibling XP snapshots load on Home. |

---

## 8. Commercial Readiness

| Domain | Effect |
|---|---|
| **CR1 Student experience** | Improved — daily command centre |
| **CR2 Trust / honesty** | Improved — stage readiness + consistency honesty |
| **CR3 Personalisation perception** | Improved — weekly briefing from personal History / Revision |
| **CR4–CR9** | Unchanged or incidental |

**Estimated CRI delta:** Provisional **+1 to +2** on student-experience / retention perception (presentation only; not validated cohort measurement).

**Remaining blockers:** History → Sitting Report drill-down; denser CMP-backed syllabus refs for “Chapter / Questions” focus lines; validated KSI / dogfood for Version 1 declaration.

---

## 9. Architecture Compliance

| Constraint | Status |
|---|---|
| LearningSessionRuntime redesign | **No** |
| EducationalEvidenceAuthority | **Unchanged** |
| StudentTwinEngine | **Unchanged** |
| ProgressEngine | **Unchanged** |
| Mission Runtime / Commercial Loop / Session FSM | **Unchanged** |
| Curriculum traversal / CMP reproduction | **Unchanged** — topic titles / position labels only |
| Layering | Presentation projects briefing from existing Experience VMs |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |

---

## 10. Files Modified

### Created

- `app/presentation/student/exam_week_briefing.py`  
- `tests/test_kwp006_home_exam_briefing.py`  
- `KWP006_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/presentation/student/dto/student_home.py`  
- `app/presentation/student/services/student_home_service.py`  
- `app/presentation/student/view_models.py`  
- `app/presentation/product_language.py`  
- `app/templates/student/home.html`  
- `app/templates/student/components/readiness_card.html`  
- `app/static/css/design_system.css`  
- `tests/presentation/student/test_view_models.py`  
- `tests/presentation/student/test_templates.py`  
- `tests/test_dx006b_student_home.py`  

### Migration Impact

**None.**

---

## 11. Tests Added

```bash
python3 -m pytest tests/test_kwp006_home_exam_briefing.py -q
```

**Outcome:** 10 passed.

Also green with related suites: `tests/test_dx006b_student_home.py`, `tests/presentation/student/test_view_models.py`, `tests/presentation/student/test_templates.py`, `tests/test_kwp002_student_value_activation.py`, `tests/test_kwp005_sitting_reports.py` (133 passed combined).

Coverage includes readiness stage bands, briefing from History/Revision, Home service wiring, template markers, approved term, and Study Health stage (no `%` in status).

---

## 12. Known Limitations

1. Briefing richness depends on History / Revision density — cold-start students see a quieter Home.  
2. “Questions 3–6” style focus lines appear only when educational position / Revision detail exists — never invented.  
3. No push / in-app notification centre (flash messages remain the channel).  
4. History still does not open a stored Sitting Report per past Session (KWP-005 follow-up).  
5. Founder Weekly Briefing remains separate — not shared with the student surface.  

---

## 13. Recommendation for KWP-007

**Working title:** KWP-007 — Retention Loop & History Continuity

**Mandate:** Close the commercial retention loop after KWP-002→006 packaging:

1. History drill-down to stored Sitting Reports.  
2. Optional gentle re-engagement copy on Home after missed days (presentation only).  
3. Founder per-sitting inspector atop Evidence Packages.  
4. Dogfood / provisional KSI validation across the commercial Home → Session → Sitting Report → Home briefing loop.  

**Non-goals:** New evidence grades, Twin math, Progress Engine redesign, CMP content reproduction, notification infrastructure.

---

## Success Criteria Check

> The student should be able to open Kwalitec every morning and immediately know where they stand, what to do, and why it matters — without searching for information.

**Status:** Met for the commercial Home path when Journey / History / Revision signals exist. Empty and quiet states remain honest and calm rather than fabricated.

---

**Document status:** Complete — KWP-006 implementation deliverable  
**Next programme:** KWP-007 Retention Loop & History Continuity (recommended)  
**Architecture stance:** SR-001A authorities unchanged; presentation packaging only  
