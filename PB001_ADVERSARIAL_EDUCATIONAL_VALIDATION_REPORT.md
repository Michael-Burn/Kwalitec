# PB-001 — Adversarial Educational Validation (LIVE RC2)

**Programme:** PB-001 Adversarial Educational Validation  
**Authority:** EF-001 (Frozen Educational Law) · RC2 GO  
**Host:** https://kwalitec.onrender.com  
**LIVE commit:** `0d3fc72137ba0ea51d1baa522c52aa526cf04438` (fingerprint match verified)  
**Date:** 2026-08-01  
**Method:** Black-box LIVE simulation only — no implementation inspection during journeys; students obey missions; defects not fixed during simulation  

**Evidence:** `knowledge/evidence/releases/PB001_RC2/`

---

## Verdict on the educational claim

Claim under test:

> “A diligent student can safely entrust Kwalitec with all educational planning while using the CMP exactly as directed.”

# **REJECTED**

The claim is falsified on LIVE RC2. Diligent students who obey Kwalitec cannot use the CMP “exactly as directed” because **Kwalitec never directs CMP use**, and the prescribed Reading activity for Study 1.1 provides **no instructional body** to study in place of the CMP. Unresolved **S1** educational observations remain (by design of this programme: defects were not remediated during simulation).

This is an educational-trust / content-direction failure. It does **not** reopen EF-001 Educational Framework design. EF-001 sufficiency is **YES** for all recorded observations.

---

## Summary

Ten realistic actuarial student personas were provisioned on LIVE (`flask create-test-user` via Render one-off jobs) and walked through onboarding → Choose Exam (CS1) → baseline → Today’s Mission Study **1.1** → session start → activities → reflection → finish, then same-calendar-day return.

| Result | Detail |
|--------|--------|
| Fingerprint | LIVE commit matches RC2 tip |
| Enrolment | All 10 enrolled in `CS1:2026.1` (Runtime C) |
| Day-1 mission start | 10/10 started Study 1.1 |
| Day-1 mission finish | 9/10 finished faithfully; 1 simulator-artifact incomplete finish (excluded) |
| Interrupt/resume | Interrupted persona left mid-activity and resumed successfully |
| CMP direction | **0/10** missions directed any CMP / Core Reading / page-section use |
| Next-day journey | Same-day return correctly gates 1.2 until tomorrow (stop-honest copy present) |
| Complete exam-horizon journey | **Not exercisable** in one calendar day; volume continuity beyond authored day remains gated |

---

## Student population

| Persona | Behaviour | Day-1 outcome |
|---------|-----------|---------------|
| Strong math | Strong answers, high confidence | Finished 1.1 |
| Weak math | Weak answers, low confidence | Finished 1.1 |
| Working professional | Mixed answers (see artifact note) | Started; finish artifact excluded |
| Interrupted schedule | Mid-session leave + resume | Resumed + finished |
| Low confidence | Strong answers, low confidence | Finished 1.1 |
| Overconfident | Weak answers, high confidence | Finished 1.1; EK stayed honest 0% |
| High discipline | Full surfaces after session | Finished 1.1 |
| Average discipline | Mixed answers | Finished 1.1 |
| Revision-averse | Obeyed anyway; opened Revision | Finished 1.1; Revision reachable |
| Practice-averse | Obeyed practice activities | Finished 1.1 |

All personas **faithfully obeyed** Kwalitec (no compensating study outside the product).

---

## Material educational weaknesses (clustered)

### F1 — No CMP direction (S1 · EC) — claim-breaking

**Observation:** Session overview and activities for Study 1.1 never mention CMP, Core Reading, Institute materials, or page/section references. Students are told to begin practice / reading inside the product, not how to use the CMP.

**Classification:** EC  
**Severity:** S1  
**Evidence:** All 10 personas; overview/activity HTML (`html_samples/day1_start.html`, `day1_act_0.html`); `mentions_cmp=false` across cohort.  
**Smallest Effective Intervention:** Author explicit CMP-use instructions on every mission briefing (what to open, which pages/sections, what to do before in-app response).  
**EF-001 Check:** YES — content/authoring under existing Educational Law.

### F2 — Empty Reading activity (S1 · EC) — claim-breaking

**Observation:** The prescribed Reading activity prompts “Study the reading, then note one key idea” but supplies essentially no readable instructional body (LO list + chrome only). A diligent student cannot obtain the learning content from Kwalitec and is not told where to find it in the CMP.

**Classification:** EC  
**Severity:** S1  
**Evidence:** LIVE Reading activity HTML (~36 words of chrome/LO text in the reading chunk); no CMP cue.  
**Smallest Effective Intervention:** Ship certified reading substance **or** replace with explicit open-CMP instructions with page/section refs before requiring a response.  
**EF-001 Check:** YES.

### F3 — Study Plan / LO surface unreachable after enrolment (S2 · RB)

**Observation:** After enrolment, `/study-plan/` returns Choose Exam wizard rather than the active plan / learning objectives the student is asked to trust.

**Classification:** RB  
**Severity:** S2  
**Evidence:** All personas `study_plan_lo` → `/study-plan/wizard/1`.  
**Smallest Effective Intervention:** Route enrolled Runtime C students to active plan LO view.  
**EF-001 Check:** YES.

### F4 — Same-day daily gate after completion (S2 · RB)

**Observation:** After finishing 1.1, Home states “Today's Session is finished. Return tomorrow to continue” and previews 1.2 locked until tomorrow. Stop-honest, but a diligent student with remaining study time has no authorised deepening/practice mission.

**Classification:** RB  
**Severity:** S2  
**Evidence:** `html_samples/day2_home.html`.  
**Smallest Effective Intervention:** Offer authorised same-day deepening/practice/revision when capacity remains, or state clearly that today’s plan is complete and any further CMP work is optional.  
**EF-001 Check:** YES.

### F5 — Progress/Coverage stay 0% after completed session (S2 · RB)

**Observation:** After finish (“Session complete…”), Home Progress and export Coverage / EK / Readiness remain 0%. Metrics do not acknowledge completed authorised study the same day (values agree with each other — no theatre — but silent).

**Classification:** RB  
**Severity:** S2  
**Evidence:** Post-finish surfaces across finished personas; PDF EK/Readiness/Coverage 0%.  
**Smallest Effective Intervention:** Move coverage/progress from completed authorised sessions, or explain why completed work does not yet move Progress.  
**EF-001 Check:** YES.

### Simulator artifact (not counted)

Working-professional run used an artificial short-session truncation that violated “follow every mission exactly,” then Finish correctly rejected incomplete completion. **Not a product S1.**

---

## EF-001 Operational Reviews (canonical forms)

### Review A — F1 No CMP direction

1. **Observation:** Mission briefing/activities never direct CMP use.  
2. **Classification:** EC  
3. **Severity:** S1  
4. **Evidence:** LIVE HTML cohort; zero CMP strings on overview/activities.  
5. **Smallest Effective Intervention:** Explicit CMP instructions per mission.  
6. **EF-001 Check:** YES

### Review B — F2 Empty Reading

1. **Observation:** Reading activity has no instructional body and no CMP redirect.  
2. **Classification:** EC  
3. **Severity:** S1  
4. **Evidence:** LIVE Reading activity HTML for Study 1.1.  
5. **Smallest Effective Intervention:** Certified reading substance or open-CMP page refs.  
6. **EF-001 Check:** YES

### Review C — F3 Plan LO unreachable

1. **Observation:** `/study-plan/` reopens Choose Exam after enrolment.  
2. **Classification:** RB  
3. **Severity:** S2  
4. **Evidence:** Cohort `study_plan_lo` finals.  
5. **Smallest Effective Intervention:** Enrolled-plan LO route.  
6. **EF-001 Check:** YES

### Review D — F4 Daily gate

1. **Observation:** Next syllabus mission locked until tomorrow after finish.  
2. **Classification:** RB  
3. **Severity:** S2  
4. **Evidence:** Day-2 home copy.  
5. **Smallest Effective Intervention:** Same-day authorised deepening or clearer complete-day policy.  
6. **EF-001 Check:** YES

### Review E — F5 Metric silence after completion

1. **Observation:** Progress/Coverage/EK remain 0% after finished mission.  
2. **Classification:** RB  
3. **Severity:** S2  
4. **Evidence:** Post-finish Home + PDF.  
5. **Smallest Effective Intervention:** Update metrics or explain non-movement.  
6. **EF-001 Check:** YES

Full per-persona finding records: `knowledge/evidence/releases/PB001_RC2/findings.json`.

---

## What did *not* falsify the claim (within exercised scope)

| Check | Result |
|-------|--------|
| LIVE fingerprint ≠ RC2 tip | Absent |
| Cannot enrol CS1 | Absent |
| Session start/advance after answer | Worked (Continue present) |
| Interrupt mid-activity resume | Worked |
| Metric disagreement theatre (Home vs export) | Absent (agree at 0%) |
| EK inflation after weak/overconfident answers | Absent (EK remained 0%) |
| Postal-address / non-syllabus topics on mission | Absent on enrolled path |
| Revision surface unreachable | Absent |

---

## End-condition assessment

| Criterion | Status |
|-----------|--------|
| Complete educational journey exercised | **Partial** — full day-1 arc exercised; exam-horizon continuity not exercisable same calendar day; volume beyond 1.1 gated by daily lock / release inventory |
| Every material educational weakness documented | **Met** for observed LIVE behaviour |
| No unresolved S1 educational observations | **Not met** — F1 and F2 remain open (unfixed by mandate) |
| Claim supported or rejected on evidence | **Rejected** |

PB-001 therefore concludes with **claim REJECTED** and **open S1s**, not with a PASS.

---

## Completion report sections

### Summary
Adversarial LIVE validation on RC2 tip rejected the trust claim: diligent obedience cannot include “use the CMP exactly as directed” when the product never directs CMP use and Reading activities lack substance.

### Files Created
- `PB001_ADVERSARIAL_EDUCATIONAL_VALIDATION_REPORT.md`
- `knowledge/evidence/releases/PB001_RC2/findings.json`
- `knowledge/evidence/releases/PB001_RC2/cohort_summary.json`
- `knowledge/evidence/releases/PB001_RC2/html_samples/*`

### Files Modified
None (application code intentionally untouched).

### Tests Executed
LIVE black-box cohort simulation (10 personas). Not a pytest suite.

### Migration Impact
None.

### Architecture Compliance
N/A for simulation; Runtime C enrolment + package session path exercised from the student surface only. V1/V2 curriculum engine not inspected.

### Technical Debt
Simulation could not advance wall-clock to exercise multi-day 1.2+ continuity; residual volume `released` inventory still limits exam-horizon proof.

### Known Limitations
- Same-day multi-mission horizon not fully walkable by product policy.  
- One persona finish failure was a simulator artifact and excluded.  
- Did not inspect internals (constraint).  

### Student Impact Assessment
- **Student problem:** Cannot safely outsource planning+CMP use — CMP never directed; Reading empty.  
- **Student benefit if fixed:** Restores the CMP partnership the claim assumes.  
- **Learning benefit:** Students would study official materials as instructed rather than inventing a study path.  
- **Success metrics:** 100% of missions include CMP direction; Reading activities have substance or CMP refs; S1 count = 0.  
- **Risks:** Shipping hollow Reading trains students to skip real CMP study.  
- **Assumptions:** CS1 CMP remains the authoritative external text.

### Estimated KSI contribution
ΔKSI = 0 (validation evidence only; no product change).

### Evidence collected
`knowledge/evidence/releases/PB001_RC2/`; LIVE HTML under `/tmp/pb001/html/` (operator workstation).

### Lessons learned for student value
Authored mission chrome and session plumbing can look complete while still failing the CMP partnership. Stop-honest daily gating is fine; undirected/empty Reading is not.

### Explainability Review
N/A — no recommendation/intelligence change.

### Recommendation Quality Review
N/A — no ranking change.

### Version 1 readiness residual
Open S1 educational content/direction gaps block any claim that LIVE RC2 is student-proof for CMP-entrusted planning. Aligns with FV-002 companion-rights FAIL and RC2 note that unconditional PB public cohort is not claimed.

### CRI domains / ΔCRI
ΔCRI = 0 (validation; board not updated).

---

## Stop

PB-001 adversarial validation complete. No defect fixes performed. Next work (outside this programme) should clear F1/F2 under existing Educational Law before re-testing the claim.
