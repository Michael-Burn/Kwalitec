# EA-003 — Mission Scoring Rubric

**Programme:** Educational Excellence Programme EA-003  
**Status:** Binding — Mission evaluation and publication threshold  
**Effective:** 2026-08-01  
**Parent:** `EA003_MISSION_BLUEPRINT.md` · `EA003_MISSION_CERTIFICATION.md`  
**Related:** EA-001 Mission Philosophy §8 · EV-001 Mission Quality Report · Gate MG  
**Nature:** Scoring law — not content generation, not application code  

---

## 1. Purpose

Provide an objective scoring system so different reviewers can evaluate Mission quality consistently — and so unfit Missions fail a numeric publication threshold, not only a vague taste test.

EV-001 scored live CS1 Mission quality **2/10**. This rubric is the permanent remedy specification for Mission evaluation.

**Hard gate:** Reject classes in `EA003_MISSION_CERTIFICATION.md` §5 cause **automatic FAIL** regardless of numeric score. Rubric scoring proceeds only when no automatic reject class fires (or after defects are fixed).

---

## 2. Scoring model

| Property | Value |
|----------|-------|
| Dimensions | 9 (equal weight unless Board amends) |
| Scale per dimension | **0–10** integers |
| Overall score | Mean of nine dimension scores, rounded to 1 decimal |
| Publication threshold | **Overall ≥ 8.0** and **no dimension < 6** |
| Tutor Intent override | If Tutor Intent fails TR-M01 → overall **FAIL** (treat as 0 for publication) |
| Reviewer | Human for Version 1 commercial certification; second reviewer recommended when overall 7.5–8.4 |

### Score bands (overall)

| Band | Range | Meaning |
|------|-------|---------|
| Unfit | 0.0–4.9 | Must not certify |
| Weak | 5.0–6.9 | Must not publish; major rewrite |
| Borderline | 7.0–7.9 | Must not publish; targeted rewrite |
| **Publishable** | **8.0–8.9** | Certify if gates PASS and no dimension < 6 |
| Exemplary | 9.0–10.0 | Model pack for author training |

---

## 3. Dimensions

### D1 — Educational coherence

**Question:** Do Purpose, Educational Intent, Concept Focus, Objective, and Success Criteria tell one deliberate learning story?

| Score | Anchor |
|------:|--------|
| 0–2 | Fields contradict or collapse to syllabus heading |
| 3–5 | Partial story; objective weak or success vague |
| 6–7 | Coherent but thin; some fields generic |
| 8–9 | Clear cognitive move; fields reinforce each other |
| 10 | Exemplary deliberate-study design; Head Tutor would adopt unchanged |

**Fail signals:** Educationally purposeless; syllabus restatement.  
**Principles:** EP-01, EP-03.

---

### D2 — Tutor quality

**Question:** Does Tutor Intent + student-facing prose pass the night-before IFoA tutor brief test?

| Score | Anchor |
|------:|--------|
| 0–2 | No Tutor Intent; chatbot/platform voice |
| 3–5 | Intent present but interchangeable; voice uneven |
| 6–7 | Acceptable tutor note; minor voice defects |
| 8–9 | Specific coaching move; calm professional Sensei |
| 10 | Indistinguishable from excellent human tutor brief |

**Fail signals:** Lacking Tutor Intent; platform meta hero copy.  
**Principles:** EP-09.  
**Hard rule:** Score ≤5 on D2 → cannot publish even if mean ≥ 8.0 (also covered by dimension floor < 6).

---

### D3 — CMP guidance

**Question:** Does the Mission multiply CMP value with precise locus and leverage — without becoming a second textbook?

| Score | Anchor |
|------:|--------|
| 0–2 | No locus; or CMP paste as body |
| 3–5 | Vague “read the material”; weak stop condition |
| 6–7 | Named open point; leverage thin |
| 8–9 | Open / stop / out-of-scope clear; strategy creates leverage |
| 10 | Precision a senior tutor uses when directing scarce hours |

**Fail signals:** CMP paraphrases; missing material locus.  
**Principles:** EP-01, EP-04. Guidance Over Content.

---

### D4 — Exam relevance

**Question:** Is why-now / weight / skill framing exam-serious and accurate?

| Score | Anchor |
|------:|--------|
| 0–2 | Engagement bait; false exam claims |
| 3–5 | Generic “exam readiness” only |
| 6–7 | Plausible exam cue; not specific |
| 8–9 | Specific skill/question type or weight-aware reason |
| 10 | Examiner-accurate cue tightly tied to today’s success check |

**Fail signals:** P12 engagement bait; opaque readiness ±% as sole benefit.  
**Principles:** EP-08.

---

### D5 — Continuity

**Question:** Is Educational Continuity built in — prior bridge, today centre, tomorrow bridge, truth alignment?

| Score | Anchor |
|------:|--------|
| 0–2 | Disconnected; no arc; contaminant next node |
| 3–5 | Token bridge; boilerplate tomorrow |
| 6–7 | Present bridges; somewhat formulaic |
| 8–9 | Felt arc; tomorrow is skill bridge not unlock theatre |
| 10 | Journey-grade continuity; residuals from prior Reflection used |

**Fail signals:** Lacking continuity; disconnected.  
**Principles:** EP-02, EP-10.

---

### D6 — Reflection quality

**Question:** Does Reflection Goal harvest topic-specific residual uncertainty useful for tomorrow and revision?

| Score | Anchor |
|------:|--------|
| 0–2 | Generic “what is clearer…” / “Today’s topic” |
| 3–5 | Weakly topic-tied |
| 6–7 | Specific but shallow |
| 8–9 | Names likely sticky point; ties to misconceptions |
| 10 | Reflection would change tomorrow’s Tutor Intent |

**Fail signals:** Generic reflection; no goal.  
**Principles:** EP-07.

---

### D7 — Tomorrow preparation

**Question:** Does Tomorrow Bridge prepare the next lawful day without heavy post-Reflection teaching?

| Score | Anchor |
|------:|--------|
| 0–2 | Fabricated/contaminant next; contradicts handoff |
| 3–5 | Unlock-only copy; no educational bridge |
| 6–7 | Lawful next topic; thin continuity line |
| 8–9 | Skill bridge + light prep cue when appropriate |
| 10 | Candidate finishes calm and oriented for tomorrow |

**Fail signals:** Gate TP failures; disagreeing handoff.  
**Principles:** EP-02; Gate TP.

---

### D8 — Student confidence

**Question:** Does the brief reduce decision anxiety and build justified confidence — without mastery theatre?

| Score | Anchor |
|------:|--------|
| 0–2 | Confusing, guilt-inducing, or false mastery |
| 3–5 | Neutral checklist; little reassurance of *how* |
| 6–7 | Clear next action; limited emotional fitness |
| 8–9 | Calm authority; student knows what done means |
| 10 | Premium Sensei brief — decisive, honest, respectful |

**Fail signals:** Mastery-from-completion language; dual truth.  
**Principles:** EP-06, EP-09, EP-10.

---

### D9 — Overall educational value

**Question:** Taking the Mission as a whole, would primary-study reliance on this brief be educationally responsible?

| Score | Anchor |
|------:|--------|
| 0–2 | EV-001-class failure (checkbox / empty shell risk) |
| 3–5 | Partial value; not primary-study grade |
| 6–7 | Useful but not premium |
| 8–9 | Primary-study responsible; supports Session execution |
| 10 | Reference Mission for the subject package |

**Holistic check:** Reviewer may not score D9 more than 2 points above the lowest of D1–D8.

---

## 4. Scoring worksheet (minimum record)

```text
Mission ID:
Subject / package:
Reviewer:
Date:

D1 Educational coherence:     __ / 10
D2 Tutor quality:              __ / 10
D3 CMP guidance:               __ / 10
D4 Exam relevance:             __ / 10
D5 Continuity:                 __ / 10
D6 Reflection quality:         __ / 10
D7 Tomorrow preparation:       __ / 10
D8 Student confidence:         __ / 10
D9 Overall educational value:  __ / 10

Overall (mean):                __ / 10
Reject class fired?            Yes / No (IDs: ____)
Dimension floor < 6?           Yes / No
Tutor Intent PASS (TR-M01)?    Yes / No

Publication threshold met?     Yes / No
Gate MG + MX PASS?             Yes / No
CERTIFICATION RESULT:          PASS / FAIL / HOLD
Notes:
```

---

## 5. Minimum publication threshold

A Mission may be publication-approved only if **all** hold:

1. No reject class fired (`EA003_MISSION_CERTIFICATION.md` §5)  
2. Educational Review PASS  
3. Tutor Review PASS (including Tutor Intent)  
4. Gate MG PASS  
5. MX-01–MX-09 PASS  
6. **Overall rubric ≥ 8.0**  
7. **Every dimension ≥ 6**  
8. Joint Session/Episode rule satisfied (or honest unavailable)  
9. Universal preconditions U1–U7 PASS  

**Borderline overall 7.0–7.9:** FAIL for publication — rewrite required.  
**Any dimension ≤ 5:** FAIL for publication even if mean ≥ 8.0.

---

## 6. Calibration against EV-001

Illustrative calibration (not a live re-score of production):

| EV-001 pattern | Likely dimension hits | Expected overall |
|----------------|----------------------|------------------|
| Title = objective = syllabus heading | D1, D2, D9 → 0–2 | ~2/10 |
| “Highest-value next step” stamp | D2, D4, D5 → low | ≤4 |
| “Today’s topic” focus | D1, D6 → low | ≤4 |
| Platform meta narrative | D2, D8 → low | ≤3 |
| Empty stages behind structure | D3, D9 → fail reject / joint rule | FAIL |

EA-003 publishable band (≥8.0) is intentionally **above** EV-001 observed quality.

---

## 7. Multi-reviewer rules

| Situation | Rule |
|-----------|------|
| Commercial subject package | Prefer Author ≠ Tutor Reviewer ≠ Publication Approver |
| Overall 7.5–8.4 | Second reviewer scores independently; use mean of overalls; any reject class from either reviewer blocks |
| Dimension disagreement ≥ 3 points | Discuss; record resolution note; do not average away a reject class |
| Automation pre-score | Advisory only; cannot PASS Tutor quality alone in Version 1 |

---

## 8. Use in certification evidence

Rubric worksheet outcomes must be stored in `rubric_scores` and referenced from `certification_evidence_uri`.

Spot-check sample Missions (≥5 across journey positions per EA-001 §9) must each meet publication threshold before subject package educational publication.

---

## 9. Closing

> If you cannot score it, you cannot certify it.  
> If it scores below 8.0, it is not yet a Kwalitec Mission.

Objective review protects students from EV-001-class briefs returning under new packaging.
