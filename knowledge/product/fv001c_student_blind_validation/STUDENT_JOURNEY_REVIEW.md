# FV-001C — Student Journey Review

**Programme:** FV-001C  
**Release Candidate:** RC-2026.07.29-01  
**Date:** 2026-07-29  
**Ready subject:** CS1V  
**Evidence:** [`_evidence/`](_evidence/)

---

## Phase 1 — Login

Signed in successfully. RC seed admin lands on **Console Home** (dual Founder/student capability). Student surfaces remain reachable.

**Confidence:** 7/10  
**Evidence:** `phase1_login.png`, `phase1_after_login.png`

---

## Phase 2 — Onboarding

`/alpha/onboarding` explains Choose Exam, Ready vs Coming Soon, Today's Focus, and Session. Language is student-clear.

**Confidence:** 8/10  
**Evidence:** `phase2_onboarding.png`

---

## Phase 3 — Choose Exam (Subject Catalogue)

`/study-plan/wizard/1` loads without error.

Visible for **CS1V**:

- **Ready**
- **CS1V · 2026.1**
- **Version 2026.1 · Updated 28 Jul 2026**

Other exams show Coming Soon with clear non-selectable copy. CS1V is selectable; Next advances to exam date.

**Confidence:** 9/10 for discovery; 7/10 for catalogue density  
**Evidence:** `phase3_choose_exam.png`

---

## Phase 4 — Exam date

Wizard asks for exam sitting and exact exam date. Clear purpose.

**Confidence:** 8/10  
**Evidence:** follow-up / complete captures under `_evidence/screenshots/`

---

## Phase 5 — Availability

Asks for weekday/weekend minutes and preferred session length. Validation rejects out-of-range values with explicit “Study time must be between 15 and 480 minutes.”

**Confidence:** 8/10  
**Evidence:** follow-up captures

---

## Phase 6 — Home / Today's Focus

Until a Study Plan is completed, `/student/` and `/dashboard/` redirect to onboarding (expected gate). Onboarding itself describes Today's Focus honestly.

**Confidence:** 6/10 (gate understood; post-enrol Home not packaged as primary alias shot)  
**Evidence:** `phase7_student_home.png` (onboarding gate) / `complete.json`

---

## Overall

Student discovery of the Founder-published Ready curriculum **works on this RC**. The EV-001 Choose Exam failure mode is not present.
