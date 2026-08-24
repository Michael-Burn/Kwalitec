# HR-010 — Tutor Review (Campaign Mu / CS1-012)

**Programme:** HR-010 — Wave 10 Human Educational Review Cycle  
**Volume:** CS1-012 · Campaign Mu (`CS1-EP001-CAMPAIGN-MU` · `cs1012-1.0.0`)  
**Reviewer role:** Human Tutor Reviewer  
**Review recorded:** 2026-08-02 · 17:45  
**Decision:** **PASS**  
**Authority:** EP-010 Wave 10 Authoring Complete · EF-001 · EP-001 Governance · Alpha floor · Continuity Front Law · RO-009 PASS · PB-011 PASS  
**Desk companion:** Catalogue packages + `CS1012_TUTOR_REVIEW.md` (UNSIGNED desk pack — this human PASS is authoritative) · `EP010_WAVE10_PLAN.md`  
**Constraint:** Educational packages unmodified during review · reviewed independently · no LIVE deploy · Wave 11 not started · RO-010 not executed  

---

## 1. Scope reviewed

Six catalogue packages under `app/curriculum/data/educational_campaigns/cs1/campaign-mu-cs1012/packages/`:

| Block | Days | Mode | Focus |
|-------|------|------|-------|
| Hypothesis testing Learning | CM-D1…CM-D5 | Learning | 3.3.1–3.3.5 |
| Revision | CM-R1 | Revision | Return 3.3.1–3.3.5 |

**Independence confirmed:** YES — Tutor seat independent of sole Educational Author hat for this seal.

---

## 2. Intake

| # | Check | Result |
|---|-------|--------|
| T-IN-01 | Read / inspected all 6 package pages (mission · reading_guidance · AR/CP · reflection · tomorrow_preview) | ✓ |
| T-IN-02 | Skimmed package JSON Knowledge Checks for closed-book assessability | ✓ |
| T-IN-03 | CMP edition pin available for locus check (`IFoA CS1 Core Reading / CMP · 2026 syllabus alignment`) | ✓ |
| T-IN-04 | Confirm independence from sole Educational Author | ✓ |
| T-IN-05 | Confirm packages remain `campaign_member_certified` (not LIVE `publication_approved`) | ✓ |
| T-IN-06 | Confirm Wave 9 LIVE-complete prerequisite (RO-009 / PB-011) before Continuity Front into 3.3 | ✓ |

---

## 3. Tutor Voice (TR-01…TR-10) — Volume

| ID | Prompt | Catalogue observation | Human |
|----|--------|----------------------|-------|
| TR-01 | Would an IFoA tutor recognise the Sensei stance? | Refuse cookbook-test-as-concepts; refuse permutation-as-basic; refuse GOF-as-permutation; refuse independence-as-GOF; refuse Ch3 / spine / until-exam; retrieval-first Revision | **Yes** |
| TR-02 | Mission purpose student-usable? | Clear mission_purpose / LO / success criteria on each day | **Yes** |
| TR-03 | Honest stops present on every day? | Stop before neighbour LO / Ch3 trophy / remainder / until-exam | **Yes** |
| TR-04 | CMP partnership clear (guide ≠ textbook)? | Exit lines pin CMP as authoritative; guide≠textbook | **Yes** |
| TR-05 | Knowledge Checks assessable closed-book? | AR + Checkpoint with model answers / refuse warrants | **Yes** |
| TR-06 | Reflection harvests wobble not summary? | Stickiest / weakest-link prompts | **Yes** |
| TR-07 | Tomorrow previews natural / reciprocal? | CM-D1→…→D5→R1; R1 honest stop / remainder-spine successor | **Yes** |
| TR-08 | Revision is retrieval not re-teach? | “No new CMP open…”; targeted reopen only; five return targets | **Yes** |
| TR-09 | No chrome / gamification voice? | Sensei voice holds; light process note on CM-R1 preview accepted below | **Yes** |
| TR-10 | Alpha floor met (intent)? | Alpha reading_guidance shape + LO-per-day across 5 Learning | **Yes** |

---

## 4. CMP partnership — per package (Q1–Q6)

Q1–Q6 confirmed on each package (open locus · purpose · attend · ignore · finished · next activity) via `open_point` / `focus_questions` / `exit_line` / `stop_condition` / `out_of_scope_today` / `return_cue` / `tomorrow_preview`.

| Package | Day | LO | Human |
|---------|-----|----|-------|
| HYPOTHESIS-CONCEPTS | CM-D1 | 3.3.1 | **PASS** |
| BASIC-TESTS | CM-D2 | 3.3.2 | **PASS** |
| PERMUTATION-TESTS | CM-D3 | 3.3.3 | **PASS** |
| CHI-SQUARE-GOF | CM-D4 | 3.3.4 | **PASS** |
| CONTINGENCY-INDEPENDENCE | CM-D5 | 3.3.5 | **PASS** |
| REV-HYPOTHESIS-TESTING | CM-R1 | Rev | **PASS** |

**Spot observations (role-appropriate):**

| Package | CMP / Voice note | Result |
|---------|------------------|--------|
| CM-D1 | Open 3.3.1; Continuity Front handoff from Lambda named; refuse applied-test-as-done; stop before 3.3.2 | **PASS** |
| CM-D2 | Basic one-/two-sample and paired tests; refuse permutation swallow; stop before 3.3.3 | **PASS** |
| CM-D3 | Permutation HT; misconception watch distinguishes bootstrap CI (3.2.8); refuse GOF swallow; stop before 3.3.4 | **PASS** |
| CM-D4 | Chi-square GOF incl. unknown parameters; refuse independence swallow; stop before 3.3.5 | **PASS** |
| CM-D5 | Contingency independence; refuse Ch3-complete / spine / until-exam; preview CM-R1 | **PASS** |
| CM-R1 | Retrieval-first open; five hinges + weakest-link; honest stop / remainder-spine successor | **PASS** |

---

## 5. Defects disposition

| ID | Note | Severity | EF-001 class | Tutor disposition |
|----|------|----------|--------------|-------------------|
| T-W10-01 | Confirm CMP locus wording vs edition pagination across 5 LOs | Medium | AW | **Accept** — syllabus-LO locus under 2026 edition pin sufficient; no pagination string edit (same bar as HR-001…HR-009) |
| T-W10-02 | Distinguish permutation HT from bootstrap CI (3.2.8) in voice | Medium | AW | **Accept** — CM-D3 misconception_watch / tutor grain explicitly distinguish; no content amendment |
| T-W10-03 | Confirm GOF vs independence separation is crisp in checks | Medium | AW | **Accept** — CM-D4 refuse independence; CM-D5 refuse GOF-as-done / Ch3 trophy; checks assessable; no content amendment |
| T-W10-04 | Actuarial sketches in checks — keep non-CS1B | Low | AW | **Accept** — checks stay inside CS1 HT/GOF warrants; no CS1B drift observed; no content amendment |
| T-W10-05 | CM-R1 `tomorrow_preview.student_facing` mentions Approver + LIVE process | Low | PI | **Accept** — mild process chrome; Continuity Front honesty (stop / remainder-spine successor) remains clear; no content amendment for Tutor PASS |

**Human-requested amendments:** **None.**

---

## 6. Decision block

```text
Tutor Reviewer name: HR-010 · Tutor seat
Date: 2026-08-02 · 17:45
Independence confirmed: YES
Decision: PASS
Conditions: None
Packages FAIL: None
Requested changes: None
Signature: SIGNED — HR-010 Tutor Review
```

---

### Summary

Tutor Voice and CMP partnership hold across the six-day Continuity Front arc into 3.3. Sensei stance recognisable; guide≠textbook on Learning days; honest stops before neighbour LOs and Chapter 3 trophy; closed-book AR assessable; Revision retrieval-first with honest handoff; permutation HT voice distinct from Lambda bootstrap CI; GOF vs independence separation crisp. Provisional items T-W10-01…T-W10-05 accepted without content change.

Educational packages under `campaign-mu-cs1012/packages/` — **untouched**.

Signed: HR-010 · Human Tutor Reviewer · CS1-012 · 2026-08-02 · 17:45
