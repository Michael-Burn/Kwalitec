# EP-008.1B — Student Surface Pack (post–EP-008.1A)

**Programme:** EP-008.1B — Recommendation Trust Validation (Tier B)  
**Date:** 2026-07-26  
**Purpose:** Student-visible recommendation trust experience judged by Tier B reviewers after Trust Contract T1–T11 delivery.  
**Constraint:** Evidence-only — no runtime / UI / educational reasoning changes in this programme.  
**Authority:** REVIEW_PROTOCOL — when package and live student experience diverge, judge the **live student-facing experience**.

---

## 1. What changed for students (EP-008.1A)

On the canonical Student Home (`/student/`), when Runtime A delivers a **schema-complete** recommendation:

| Element | Student-visible behaviour |
|---|---|
| L1 why | Authored `why_recommended` without expand |
| L1 why now | Authored `timeliness` line |
| L1 benefit | “You’ll work toward” + authored expected benefit |
| L1 next | Authored suggested next action |
| L1 coherence | Plan coherence label (e.g. “Supports today’s mission”) when not refusal |
| L2 disclosure | “Why this tip?” — evidence, confidence, full benefit, review point, ≤2 alternatives |
| Coach | Structured Why / Why now / Next / Benefit — same strings as Home |
| Refusal | “No recommendation yet”; Cannot yet be estimated; alternatives hidden; restorative next |
| Incomplete | Omit trust blocks; no invented confidence |

Ranking, Decision Framework, and Runtime A authorship are unchanged — presentation pass-through only.

---

## 2. Capture artefacts used by Tier B

| File | Content |
|---|---|
| [`_capture/home_schema_complete.txt`](_capture/home_schema_complete.txt) | Schema-complete trust + alternatives + structured Coach |
| [`_capture/home_honest_refusal.txt`](_capture/home_honest_refusal.txt) | Honest refusal / cannot-yet path |
| [`_capture/home_cold_start.txt`](_capture/home_cold_start.txt) | Incomplete recommendation; trust blocks absent |
| EP-008.1A TR-A0* tests | Automated structural proof |

### Representative schema-complete speech

> **Cash flow statements** — *25 minutes*  
> Why — *Your recent practice shows soft recall on cash flow statements, so a focused session will protect what you have already learned.*  
> Why now — *High educational return before the exam window.*  
> You’ll work toward — *Strengthen exam readiness on cash flow analysis.*  
> Next — *Start a 25-minute cash flow practice session.*  
> Coherence — *Supports today's mission*  
> L2 — evidence bullets; Confidence *Suggested — Based on recent practice outcomes*; After you complete this — *Reassess after tonight's practice set*; Other options — Working capital cycles; Inventory valuation.  
> Coach — same Why / Why now / Next / Benefit bullets.

### Representative honest-refusal speech

> **No recommendation yet**  
> Why — *There is not yet enough personal study evidence for a confident primary tip.*  
> Confidence — *Cannot yet be estimated*  
> Next — *Complete a short study session so guidance can be personalised.*  
> Alternatives — **absent**  
> Coach — humility Why / Next / Benefit (no fabricated tip).

### Representative cold-start speech

> Mission placeholder; Coach — *Your coach insight will appear after your next study session.*  
> No why / benefit / coherence / alternatives.

**Capture note:** Flask render without a live Start Session form shows the muted “A session will be ready…” line even when `can_start_session=True`. Reviewers treat **Start Session** as available on schema-complete nights when the product enables the primary CTA (contract TR-A05; same limitation as prior MES surface packs). Judge next-action speech from the authored *Next* line.

---

## 3. Known limitations reviewers must treat as current product

1. Cold-start / incomplete nights still lack trust speech.  
2. Why-now copy can still feel generic (“educational return”) when authored thinly.  
3. Benefit language must not be read as Exam Ready / guaranteed pass.  
4. Alternatives are informational only — no accept/dismiss controls (EP-008.3).  
5. Personalisation flags remain OFF.  
6. `V1_REVIEW_PACKAGE` may lag live Home — use this pack + live render.

---

## 4. Tier B cohort

Post-change re-reviews archived under [`tier_b_reviews/`](tier_b_reviews/) (baseline corpora **not** overwritten):

**SV-003, SV-005, SV-008, SV-010, SV-011, SV-012, SV-013, SV-014, SV-015** (N=9; meets methodology interview floor ≥8).

Focus: trust / explainability / decision support / calibration / educational feedback / adaptation — recommendation inspectability is in-scope for all.

---

**End of STUDENT_SURFACE_PACK**
