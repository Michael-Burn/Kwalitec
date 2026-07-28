# Explanation Patterns

**Programme:** ILE-001C0 — Study Sensei Communication Framework  
**Version:** 1.0  
**Status:** Active — permanent explanation structures  
**Effective:** 2026-07-28  
**Companion:** [`STUDY_SENSEI_COMMUNICATION_FRAMEWORK.md`](STUDY_SENSEI_COMMUNICATION_FRAMEWORK.md)  
**Related:** P-001.2 Explainability Standard; PTP-003 Product Communication Standard  

---

## Purpose

Standardise **how the Study Sensei explains** recommendations, checks, readiness signals, and recovery paths so learners always receive a traceable educational story — never opaque scores or implementation detail.

---

## Default arc

```
Observation
    ↓
Educational meaning
    ↓
Suggested action
    ↓
Expected benefit
```

When uncertainty matters (usually), append:

```
    ↓
What remains uncertain / what would strengthen evidence
```

This maps cleanly to P-001.2’s what / why / what next / what is uncertain without exposing internals.

---

## Layer definitions

| Layer | Student question answered | Rules |
|---|---|---|
| **Observation** | What did we see? | Concrete, learner-visible facts or labelled estimates; no Twin jargon |
| **Educational meaning** | What does that mean for learning? | Curriculum / plan / readiness interpretation in plain language |
| **Suggested action** | What should I do now? | One primary action when Reliable+; soft / optional when Emerging |
| **Expected benefit** | Why bother? | Learning benefit — clarity, reinforcement, unblock next step — not points or streaks |
| **Uncertainty** | What don’t we know? | Required when evidence is thin, mixed, or provisional |

---

## Canonical pattern — primary recommendation

**Structure**

1. Observation  
2. Educational meaning  
3. Suggested action  
4. Expected benefit  
5. Uncertainty (brief)

**Example**

> Recent practice on *Discounting* looks fragile after two short sessions.  
> That topic sits under a foundation idea you’ll need for later syllabus steps.  
> Today’s Mission focuses on reinforcing Discounting within your available time.  
> Strengthening it now reduces the chance of carrying a shaky base forward.  
> We still have limited evidence from Deep Checks — a careful check after practice would help.

---

## Pattern — Adaptive Assessment entry

**Structure**

1. Why this check now (educational purpose)  
2. What we’ll use the evidence for  
3. Effort / length honesty  
4. Non-guarantee / non-exam framing where required  

**Example**

> A Quick Check gathers a little evidence on today’s focus.  
> We’ll use it to guide practice — not to grade you.  
> About five minutes. You can pause if you need to.

---

## Pattern — post-check feedback

**Structure**

1. Observation (what this check showed — bounded)  
2. Educational meaning (provisional belief language)  
3. Suggested action (Continue Learning / Strengthen / Build Confidence — as warranted)  
4. Uncertainty remaining  

Never: FAILED stamps, rankings, or mastery declarations from a single formative check.

---

## Pattern — readiness / estimated values

**Structure**

1. Label the claim type honestly (Estimated / provisional — PTP-003)  
2. Basis in plain language (recorded practice, coverage, recent checks)  
3. What it is *not* (exam prediction, guarantee)  
4. Suggested study implication if Reliable  

**Example**

> Estimated readiness is provisional, based on recorded practice and syllabus progress.  
> It guides what to study next. It does not predict your result.

---

## Pattern — recovery / incomplete day

**Structure**

1. Neutral observation (incomplete / deferred — no guilt)  
2. Meaning (evidence partial; plan still holds)  
3. Soft recovery action  
4. Benefit (return to authorised loop)

---

## Pattern — conflicting evidence

**Structure**

1. Name the conflict plainly  
2. Meaning: we will not pretend precision  
3. Action: clarifying check, focused study, or wait  
4. Benefit: cleaner guidance afterward  

---

## Never reveal implementation details

Learner-facing explanations must **not** include:

| Forbidden | Why |
|---|---|
| Service / class / algorithm names | Implementation leakage |
| Raw scores, weights, ladder ranks | False precision / engineering chrome |
| Twin field names, warrant types, feature flags | Jargon breaks trust |
| “The model decided…” | Opaque authority |
| Database or migration concepts | Irrelevant and alarming |

Explain *educational* causes: thin evidence, mixed recent answers, time since last practice, plan focus, exam proximity (as pacing context — not fear).

---

## Length guidance

| Surface | Typical length |
|---|---|
| Inline tip / Mission reason | 2–4 short sentences covering the arc |
| “Why am I seeing this?” | Full arc; still scannable |
| Analytics / readiness callout | Label + basis + non-guarantee + optional action |
| Tutor narration | Arc only for *authorised* decisions; never invent new ranking |

---

## Quality checklist

1. Can a student restate observation → meaning → action → benefit?  
2. Is uncertainty present when claim strength is not High?  
3. Any implementation leak?  
4. Does claim taxonomy (PTP-003) match the wording?  
5. One primary action — not a tip storm?

---

**End of EXPLANATION_PATTERNS**
