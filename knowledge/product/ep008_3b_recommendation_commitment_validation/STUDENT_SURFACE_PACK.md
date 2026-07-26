# EP-008.3B — Student Surface Pack (post–EP-008.3A)

**Programme:** EP-008.3B — Recommendation Commitment Validation (Tier B)  
**Date:** 2026-07-26  
**Purpose:** Student-visible commitment / defer / reflection / history experience judged by Tier B reviewers after EP-008.3A delivery.  
**Constraint:** Evidence-only — no runtime / UI / educational reasoning changes in this programme.  
**Authority:** REVIEW_PROTOCOL — when package and live student experience diverge, judge the **live student-facing experience**.

---

## 1. What changed for students (EP-008.3A)

On the canonical Student Home (`/student/`), when Runtime A delivers a **schema-complete** recommendation, Trust L1 remains, then:

| Element | Student-visible behaviour |
|---|---|
| Commitment helper (Pattern A) | “I’m doing this next.” + “Starting means you’re doing this next.” (`data-commitment="confirm"`) |
| Primary CTA | Single **Start Session** — POST also records preference commitment |
| Continuity | “This is part of your continuous study plan.” |
| Defer | Secondary “Not today” disclosure with calm reason catalogue |
| Committed chrome | “Committed for today: {title}” + continuity; Coach muted status only |
| Deferred chrome | “Deferred for today · {reason}” + “Your study plan continues…” |
| Reflection | What you did / changed / why / what we updated (humble) / what next + Got it |
| History | “Recent study choices” narrative (completed / deferred / committed incomplete) |
| Refusal nights | Commit / defer **hidden** |

Ranking, Decision Framework, and Runtime A authorship are unchanged — preference/intent only.

---

## 2. Capture artefacts used by Tier B

| File | Content |
|---|---|
| [`_capture/home_commitment_offered.txt`](_capture/home_commitment_offered.txt) | Schema-complete trust + Pattern A commit + defer catalogue |
| [`_capture/home_committed.txt`](_capture/home_committed.txt) | Committed chrome + Coach status |
| [`_capture/home_deferred.txt`](_capture/home_deferred.txt) | Honest defer ack + continuity |
| [`_capture/home_reflection.txt`](_capture/home_reflection.txt) | Completion reflection fields |
| [`_capture/home_refusal.txt`](_capture/home_refusal.txt) | Refusal — no commit/defer theatre |
| [`_capture/history_narrative.txt`](_capture/history_narrative.txt) | Recent study choices narrative |
| EP-008.3A CF-A0* tests | Automated structural proof |

### Representative offered speech

> **Cash flow statements** — *25 minutes*  
> Why / Why now / Benefit / Next / Coherence (Trust L1 unchanged)  
> **I’m doing this next.** *Starting means you’re doing this next.*  
> *This is part of your continuous study plan.*  
> **[ Start Session ]**  
> Not today ▸ What’s getting in the way? — Not enough time tonight / Too tired / Need a prerequisite first / Not today / Something else  

### Representative deferred speech

> Deferred for today · Not enough time tonight  
> Your study plan continues — we'll meet you when you're ready.  
> Tip remains inspectable; Start Session still available (intent ≠ lock).

### Representative reflection speech

> Session complete  
> What you did — *Completed: Cash flow statements*  
> What changed — *Reassess after tonight's practice set.*  
> Why it mattered — *Strengthen exam readiness on cash flow analysis.*  
> What we updated — *Tonight's practice updates the educational state that shapes tomorrow's tip.*  
> What happens next — *Return Home for the next tip.*  
> Continuity — *Tomorrow's tip will reflect tonight's work as part of the same plan.*  
> **[ Got it ]**

### Representative history speech

> Recent study choices  
> *Choices you've made inside one study plan.*  
> Completed · Cash flow statements · …  
> Deferred · Working capital cycles · Not enough time tonight · plan continues  
> Committed · not finished · Inventory valuation  

**Capture note:** Flask render may show muted secondary Start Session quick-action links; reviewers treat **one primary Start Session** on the commitment block as the DR-050 primary CTA (contract CF-A05). Judge Pattern A agency from helper copy + single primary button.

---

## 3. Known limitations reviewers must treat as current product

1. **Pattern A** combines start + commitment — no separate “I’m doing this next” button.  
2. Reflection “What changed” may reuse authored review-point language (can feel thin).  
3. Cold-start / refusal nights intentionally hide commit/defer.  
4. Behavioural acceptance / completion **rates** are not shown to students and are not claimed here.  
5. Personalisation flags remain OFF.  
6. `V1_REVIEW_PACKAGE` may lag live Home — use this pack + live render.

---

## 4. Tier B cohort

Post-change re-reviews archived under [`tier_b_reviews/`](tier_b_reviews/) (baseline corpora **not** overwritten):

**SV-004, SV-005, SV-008, SV-010, SV-011, SV-014, SV-015, SV-016, SV-020** (N=9; meets methodology interview floor ≥8).

Focus: motivation / trust / agency / recoverability / feedback / mental model / decision support / cognitive load / bounded commitment — commitment execution is in-scope for all.

---

## 5. Dogfood checklist (UI_SPEC §13) — facilitator

| Check | Result |
|---|---|
| Schema-complete: understand tip, then commit or defer without confusion | **Pass** (surface pack) |
| Single primary Start Session CTA | **Pass** (CF-A05 + capture) |
| Defer reasons calm; no punishment after save | **Pass** |
| Refusal night: no commit/defer theatre | **Pass** |
| Completion shows reflection without Twin theatre | **Pass** |
| History shows completed + deferred narrative | **Pass** |
| Continuity language on commit / defer / reflection | **Pass** |
| Coach does not add a second Commit button | **Pass** (muted status only) |
| No streak / points / gamification | **Pass** |
| Trust L1 fields still visible | **Pass** (CF-A11) |

---

**End of STUDENT_SURFACE_PACK**
