# Daily Coach Explainability

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS001 — Daily Coaching Model  
**Classification:** Explainability contract for day-to-day coaching recommendations  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **today’s Daily Coach recommendations** in plain educational language.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `EDUCATIONAL_LOGIC_REGISTRY.md` (especially EL-008, EL-010)
4. `DAILY_COACH_MODEL.md`
5. `DAILY_COACH_DECISION_MODEL.md`
6. `DAILY_COACH_OUTPUTS.md`
7. `../study_plan/STUDY_PLAN_EXPLAINABILITY.md`
8. `../EDUCATIONAL_EVIDENCE_MODEL.md`

> **Every recommendation must reference the student’s current educational context and the broader Study Plan.  
> Explainability improves understanding of guidance already authorised. It never invents educational certainty.**

---

## 1. Purpose

Students should never have to guess why Kwalitec chose today’s priority.

Daily Coach explainability exists so that every material daily recommendation answers — in plain educational language — what is known, what is estimated, why this is today’s focus, and what to do next — while remaining faithful to the Canonical Study Plan.

Without Daily Coach explainability:

- today feels arbitrary;
- plan and mission stories conflict;
- recovery looks like laziness or failure;
- escalation feels like product breakage.

With Daily Coach explainability:

- the student trusts the tutor posture;
- long-term plan intent remains visible in daily speech;
- claim types stay honest;
- hard days (recovery, short windows, replan needed) remain dignified and clear.

---

## 2. Traceability Obligation (Architectural)

Every material Daily Coach recommendation must be traceable through:

| Trace link | Student-facing role |
|------------|---------------------|
| **Canonical Study Plan** | “Your Study Plan has you focused on…” |
| **Today’s authorised plan work** | “For today, that means…” |
| **Mode / topic authority** | “Under Learning Mode, today’s learning focus is…” / “Today is a revision / recovery day, so…” |
| **Student Educational Profile / current context** | “Given where you are now / what today allows…” |
| **Recent evidence / session history** | “Because recent study showed… / Because you completed / missed…” |
| **Daily Coach decision** | “So the most valuable thing today is…” |

Internal IDs (DCD-XX, DCO-XX, DCI-XX, SPC-XX, EL-XXX) may exist for algorithms and audits. They must not appear as student-facing jargon.

A recommendation with no plan / mode warrant (for plan-based coaching) is invalid — even if the explanation sounds motivating.

---

## 3. Explainability Principles

1. **Plan + today.** Every material recommendation cites both the broader Study Plan and the student’s current educational context.
2. **One primary reason.** Prefer a single clear educational purpose over multi-factor dumps.
3. **One clear next action.** Guidance reduces decision burden.
4. **Facts and estimates stay distinct.** Coverage and completion are not mastery.
5. **Protections are spoken as intentional.** Recovery and revision are coaching commitments, not apologies.
6. **Advice is labelled.** Optional secondaries never masquerade as Mission obligations.
7. **Escalation is plain.** When the plan needs rescheduling or replanning, say so without blame theatre.
8. **Internal machinery stays invisible.** No Twin facets, optimiser names, or registry IDs.
9. **Uncertainty is named** when evidence or capacity inputs are thin.
10. **No new algorithms in speech.** Copy narrates authorised decisions; it does not invent scores.

---

## 4. Four-Question Framework (Daily Specialisation)

Every material Daily Coach recommendation must answer EIP-003’s four questions, specialised for today:

### Q1 — What do we objectively know?

Examples:

- Today’s plan places a first-pass / practice / revision / recovery session.
- Available study time today is X.
- Recent planned sessions were completed or missed.
- Current Learning Topic is T (when Learning Mode applies).

### Q2 — What do we estimate?

Examples:

- Estimated Knowledge / readiness language only when Evidence Model warrants — clearly labelled.
- If estimation is not yet lawful: say it cannot yet be estimated.

### Q3 — Why are we recommending this?

One educational explanation tying **Study Plan intent** to **today’s context**.

Examples:

- “Your plan is in first-pass for this stretch, and today you have a focused evening — so continuing Topic T is the highest-value next step.”
- “Your plan reserved today for revision, so we are consolidating what you have already studied rather than opening new topics.”
- “You are in recovery after disruption, so today stays lighter on purpose.”

### Q4 — What should the student do next?

One clear educational action consistent with DCO-01 / DCO-02.

---

## 5. Narrative Patterns (Normative)

### 5.1 Ordinary learning day

> Your Study Plan keeps you in first-pass learning this week.  
> Today you have [time] available, and your next learning focus is [Topic].  
> The most valuable thing today is to complete that learning block.  
> Optional: if time remains, [secondary practice advice].

### 5.2 Practice / consolidation day

> Your Study Plan includes practice on recent material so coverage turns into usable skill.  
> Given [recent completion / evidence posture], today’s priority is focused practice on [focus].  
> This does not by itself prove mastery — it builds the evidence and habit your plan expects.

### 5.3 Protected revision day

> Your Study Plan protects revision time before the sitting.  
> Today that commitment comes first, so we revise [scope] rather than pushing into new first-pass topics.  
> New topics can wait so revision is not silently sacrificed.

### 5.4 Recovery day

> Your plan is in recovery after [illness / dense stretch / disruption].  
> Today’s priority is lighter, sustainable study — not catching up at full intensity.  
> Protecting recovery keeps the rest of the plan honest.

### 5.5 Short-capacity day

> Your plan expected a longer session, but today you only have [time].  
> We will complete a smaller, finishable piece of today’s planned job rather than starting something you cannot finish well.  
> If short days keep stacking up, we may need to reschedule remaining sessions.

### 5.6 Escalation day

> Recent missed sessions / capacity change means continuing “as if nothing changed” would break your Study Plan’s limits (for example, protected revision or sustainable weekly load).  
> Kwalitec will not silently rewrite your plan or invent overload for today.  
> Next step: [reschedule remaining sessions / request a replan].  
> Meanwhile today, do [interim lawful objective].

---

## 6. Language Rules

### 6.1 Required student language

- Prefer: Study Plan, today’s focus, learning, practice, revision, recovery, next step, estimated, recommended / optional.
- Prefer honest uncertainty: “we cannot yet estimate…”, “based on recent practice…”.

### 6.2 Forbidden student language

- Twin, facet, optimiser, score vector, registry IDs, “algorithm decided”.
- “Mastered” from completion alone.
- “Guaranteed pass if you follow today”.
- Shame framing as the educational reason (“you failed your plan”).
- Silent equivalence of advisory widgets with Today’s Mission.

### 6.3 Claim-type cues

| Claim type | Daily Coach cue |
|------------|-----------------|
| Observed / Derived Fact | “You completed…”, “Your plan places…”, “Coverage is…” |
| Evidence-backed Estimate | “Estimated…”, “Suggested readiness…” |
| Educational Advice | “Recommended…”, “Optional…”, “Most valuable today…” |

---

## 7. Surface Contract

Any student-facing surface that presents Daily Coach guidance must:

1. Show or narrate **DCO-01** as the primary objective.  
2. Provide **DCO-06** rationale answering Q1–Q4 (explicitly or as coherent equivalent narrative).  
3. Disclose **DCO-10** when today’s job is not ordinary Learning Mode first-pass.  
4. Keep secondaries visually/linguistically subordinate.  
5. Present **DCO-08** without burying it under motivational copy when escalation applies.  
6. Remain consistent with Canonical Study Plan narration (`STUDY_PLAN_EXPLAINABILITY.md`).

Surfaces may vary layout. They may not vary educational meaning.

---

## 8. Good and Bad Examples

### Good

> “Your Study Plan has you consolidating this week. Today’s most valuable work is revision on [topics], in the two hours you have this evening.”

### Bad

> “Do these five priority tasks to maximise your readiness score.”  
> (Multiple equal priorities; score theatre; no plan link.)

### Good

> “You missed two planned sessions. Today we continue with the next lawful learning focus rather than doubling intensity. If this keeps happening, we should reschedule so protected revision stays intact.”

### Bad

> “You are behind — study six hours tonight to catch up and keep your revision week free.”  
> (Punishment catch-up; silent threat to plan honesty.)

### Good

> “Estimated knowledge for this topic is still provisional. Today’s practice helps build evidence; completing the session does not mean the topic is mastered.”

### Bad

> “Great job — Topic mastered!” after a single completion tick.  
> (Mastery minting.)

---

## 9. Consistency with Broader Explainability Law

| Authority | Daily Coach duty |
|-----------|------------------|
| EIP-003 | Four questions; claim types; educational language |
| EL-010 | Messaging honesty; no engineering speech |
| EL-008 | Advice does not silently rewrite Mission |
| Study Plan explainability | Daily speech must not contradict plan commitments without disclosed adaptation / escalation |
| Evidence Model | No invented understanding claims in daily close |

---

## 10. Cross References

| Document | Relationship |
|----------|----------------|
| [`DAILY_COACH_MODEL.md`](DAILY_COACH_MODEL.md) | Tutor posture being explained |
| [`DAILY_COACH_OUTPUTS.md`](DAILY_COACH_OUTPUTS.md) | Outputs that require rationale |
| [`../EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) | Parent explainability standard |
| [`../study_plan/STUDY_PLAN_EXPLAINABILITY.md`](../study_plan/STUDY_PLAN_EXPLAINABILITY.md) | Long-term plan speech Daily Coach must remain consistent with |
