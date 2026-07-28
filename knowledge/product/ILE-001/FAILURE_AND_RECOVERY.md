# Failure and Recovery — Adaptive Assessment

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design  
**Effective:** 2026-07-28  

---

## Purpose

Define how Adaptive Assessment behaves when study life is messy: interruptions, incomplete evidence, low confidence, conflicting signals, and long gaps.

Failure modes are **expected**. Recovery must protect trust and motivation while preserving educational honesty.

---

## Design stance

- Incomplete is not delinquency.  
- Uncertainty is not a product bug.  
- Recovery is a path, not a punishment loop.  
- The platform must not invent confidence to “smooth over” failure.

---

## 1. Interrupted sessions

**Examples:** Call, fatigue, browser close, device switch, accidental navigation away.

| Requirement | Behaviour |
|---|---|
| **Pause / resume** | Progress saved; student can return without restarting from zero when technically feasible |
| **Framing on return** | “Paused check — continue when ready” |
| **No shame** | No guilt copy, streak breaks, or “you abandoned your exam” |
| **Mission continuity** | Mission remains completable via lawful alternatives if the check cannot finish today |
| **Evidence** | Only committed responses become observations; uncommitted drafts do not invent outcomes |

**Student feeling to protect:** Life interrupts study; Kwalitec understands.

---

## 2. Incomplete evidence

**Examples:** Exit mid-check; only one item answered; hints on all items; time exhausted before intent met.

| Requirement | Behaviour |
|---|---|
| **Honesty** | Summary states evidence is partial |
| **Twin / Reasoning** | Partial observations only; no fabricated mastery fill-in |
| **Next action** | Prefer teaching/practice or a later short check — not immediate forced full retry |
| **UI** | Distinguish “check finished” from “check paused / partial” |

**Avoid:** Treating partial completion as full confirmation success to keep completion rates high.

---

## 3. Low confidence (student-felt)

**Examples:** Student marks “unsure” often; underconfidence pattern; anxiety before Readiness Check.

| Requirement | Behaviour |
|---|---|
| **Tone** | Encouraging, specific, non-patronising |
| **Interpretation** | Low confidence + strong evidence → fragility support, not fake celebration of mastery |
| **Interpretation** | Low confidence + weak evidence → normal learning state; offer recovery / study |
| **Controls** | Confidence prompts remain optional; never corner the student |
| **Tutor** | On request: normalise struggle; explain next recovery step already decided |

**Avoid:** “Just be more confident” coaching without evidence change.

---

## 4. Conflicting evidence

**Examples:** Recent success then miss on related item; assisted success vs later unassisted miss; Mission history disagrees with a new check.

| Requirement | Behaviour |
|---|---|
| **Surface conflict** | “Recent signals disagree — we won’t pretend this is settled.” |
| **Selection** | Prefer a narrow clarifying check or study/recovery over declaring a winner |
| **Language** | Keep both provisional; do not average into false precision |
| **Mission** | May schedule recovery or clarification; must not flip-flop daily without explanation |
| **Trust** | Explain why tomorrow’s plan changed |

**Avoid:** Hidden resolution that suddenly claims mastery or failure without narrative.

Detail also in `CONFIDENCE_AND_UNCERTAINTY_UX.md`.

---

## 5. Long study gaps

**Examples:** Weeks away; sitting pause; illness; work crunch.

| Requirement | Behaviour |
|---|---|
| **Welcome** | Recovery Check journey; dignity-first copy |
| **State honesty** | Evidence may be stale; uncertainty rises visibly |
| **Load** | Short, gentle instruments; avoid readiness batteries on day one back |
| **Mission** | Re-orientation over aggressive new content |
| **No punishment** | No streak debt, “catch up 40 checks,” or guilt dashboards |

**Student feeling to protect:** Returning is smart; the product helps restart accurately.

---

## 6. Low system confidence / thin Twin

**Examples:** New topic; new user; unsupported thin catalogue; Reasoning leaves high uncertainty after a check.

| Requirement | Behaviour |
|---|---|
| **Admit limits** | “We still don’t know enough to guide firmly on this.” |
| **Reduce uncertainty plan** | Concrete next evidence or study action |
| **Do not over-assess** | Thin state is not a licence for endless quizzes |
| **Curriculum honesty** | If content support is weak, do not fake adaptive depth |

---

## 7. Technical and delivery failures

**Examples:** Item failed to load; observation emission failed; session state corrupt.

| Requirement | Behaviour |
|---|---|
| **Student copy** | Direct and human; protect trust |
| **Safety** | Do not write Twin belief from broken sessions |
| **Retry** | Offer safe retry or skip to study activity |
| **Operator** | Founder diagnostics on evidence-path health — never student ranking |

Align with platform error-handling norms (AP-002D error boundaries conceptually): assessment observes; failures must not bypass Reasoning with guesswork.

---

## Recovery playbook (summary)

| Failure mode | Primary recovery | Session type bias |
|---|---|---|
| Interrupted | Resume or defer; partial honesty | Same type on resume |
| Incomplete evidence | Study/practice then optional short check | Quick / Recovery |
| Low student confidence | Calibration narrative + supportive next | Confidence / Recovery |
| Conflicting evidence | Clarify or rebuild; explain plan change | Quick clarifying / Recovery |
| Long gap | Welcome + gentle reorientation | Recovery Check |
| Thin system belief | Invite evidence without flood | Quick Check |
| Technical failure | Safe retry / skip; no fake results | N/A |

---

## Motivation protection checklist

After any failure path, verify:

1. No shame or delinquency language  
2. Uncertainty remains visible if evidence is weak  
3. One clear next action  
4. Home still has a single educational truth  
5. Student can continue studying today without “passing” a gate  

---

## Success criterion

A candidate who pauses, struggles, conflicts, or returns after weeks can say:

> “Kwalitec didn’t punish me — it helped me restart honestly.”

---

**End of FAILURE_AND_RECOVERY**
