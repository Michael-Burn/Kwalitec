# FV-001C — UX Findings Register

**Release Candidate:** RC-2026.07.29-01  
**Date:** 2026-07-29

---

## UX-S01 — Choose Exam catalogue density

| | |
|---|---|
| **Severity** | Major |
| **Classification** | Usability / Presentation |
| **Observation** | Many Coming Soon subjects listed with repeated preparation copy; Ready CS1V is present and selectable near the top but easy to lose in the list. |
| **Evidence** | `phase3_choose_exam.png` |
| **Impact** | Slows selection; does not block discovery of CS1V. |
| **Recommendation** | Group Ready first; collapse or paginate Coming Soon. |

---

## UX-S02 — Dual-role login lands on Console

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Usability |
| **Observation** | RC admin (Founder + student capability) lands on Console Home, not student onboarding. |
| **Evidence** | `phase1_after_login.png` |
| **Impact** | Extra navigation for a student-persona walk on this seed account. |
| **Recommendation** | Role-aware default landing for Alpha student validation accounts. |

---

## UX-S03 — Availability minutes validation

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Usability |
| **Observation** | Values outside 15–480 minutes are refused with clear copy. |
| **Evidence** | `followup.json` flashes |
| **Impact** | Correct safety; student must read unit (minutes). |
| **Recommendation** | Optional example values (e.g. 60 / 90) near fields. |

---

## Cleared engineering condition

| Prior | This RC |
|---|---|
| EV-001 Choose Exam HTTP 500 | **Cleared** — page renders Ready CS1V with date |
