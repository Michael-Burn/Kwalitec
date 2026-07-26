# Learning Progression States

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS001 — Learning Progression Model  
**Classification:** Meaningful educational progression postures over time  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **meaningful educational progression states** — named postures describing how learning is advancing (or not) across sessions.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `LEARNING_PROGRESSION_MODEL.md`
3. `LEARNING_OBJECTIVES.md`
4. `LEARNING_EVIDENCE_MODEL.md`
5. `../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`
6. `../student_profile/PROFILE_STATES.md`
7. `../EDUCATIONAL_EVIDENCE_MODEL.md`

States are educational meanings — not database enums, UI badges, optimiser modes, or numeric bands. Implementations may map storage labels onto these meanings; they may not redefine the meanings in code.

> **States describe progression posture from accumulated evidence.  
> They do not schedule work and do not mint mastery from completion.**

---

## 1. Purpose

An expert IFoA tutor summarises growth in plain educational language: *emerging*, *developing*, *retrievable*, *applicable*, *holding*, *ready enough to claim preparation maturity* — or *too early / stalled / inconsistent*.

These states capture that summary so Learning Coach narration, Profile evolution consumers, and Daily Coach emphasis share one progression vocabulary.

Profile states (`PROFILE_STATES.md`) describe **journey diagnosis** (Beginning Study, Practising, Revising, …).  
Learning progression states describe **growth quality on educational objectives** for a scope of syllabus concern.

They often align; they are **not identical objects**.

---

## 2. State Principles (Educational Framework)

The catalogue below is developed from educational principles, not from product label fashion.

1. **Meaning before labels.** UI copy may vary; educational meaning must match this catalogue.
2. **Evidence-aware.** States that imply understanding, retrieval, application, or retention require warrant per `LEARNING_EVIDENCE_MODEL.md`.
3. **Objective-specific.** A student may be *Developing Competence* on Topic A and *Emerging Understanding* on Topic B. Global labels, if used, must not erase local unevenness.
4. **Non-punitive.** Stall and inconsistency are diagnostic — never shame categories.
5. **Reversible.** Students move among states as the evidence trail evolves.
6. **Silence over stretch.** Prefer a more cautious adjacent state — or explicit *Insufficient Warrant* — when history is thin.
7. **Not a score band.** Ordering is educational succession, not a points ladder.
8. **Completion never assigns advanced states.** Coverage-only trails stop at early postures.

---

## 3. Framework Logic (Before Labels)

Progression postures answer four tutor questions in order:

| Order | Tutor question | If “no” / thin |
|-------|----------------|----------------|
| 1 | Has contact / coverage begun honestly? | Insufficient Warrant or Coverage Emerging only |
| 2 | Is comprehension supported by more than familiarity? | Stay at Emerging Understanding or earlier |
| 3 | Can the student retrieve and apply across sessions? | Do not claim Reliable Retrieval / Confident Application |
| 4 | Does command survive spacing and support preparation maturity? | Do not claim Durable Knowledge / Exam-Ready Progression |

Examples such as “Emerging Understanding” or “Durable Knowledge” are **illustrative names** for postures produced by this logic — not a closed marketing set. The binding meanings are the state definitions below.

---

## 4. Primary Progression States

### LPS-0 — Insufficient Warrant

**Educational meaning:** Accumulated evidence is too thin to judge genuine learning progression. Activity may exist; understanding claims must stay silent or explicitly cautious.

**Tutor reading:** “Too early — or too empty — to say learning is progressing.”

**Typical trail:** Little or no EC-C/EC-E; possible EC-A/EC-B only; cold start.

**Must not claim:** Understanding growth, mastery, exam readiness.

**Adjacent:** Coverage Emerging (when LO-01 advances); Emerging Understanding (when first lawful comprehension signals appear).

---

### LPS-1 — Coverage Emerging

**Educational meaning:** Syllabus coverage (LO-01) is advancing honestly; familiarity (LO-02) may be starting. Performance evidence for understanding remains absent or negligible.

**Tutor reading:** “The journey is moving through the syllabus; we have not yet shown understanding growth.”

**Typical trail:** Confirming EC-A; thin EC-C.

**Must not claim:** Genuine understanding progression; application; durable knowledge.

**Adjacent:** Insufficient Warrant; Emerging Understanding; Progression Stall (if sessions continue without any deeper warrant and expectations were for practice).

---

### LPS-2 — Emerging Understanding

**Educational meaning:** Early, provisional comprehension signals appear (LO-03). Familiarity is present; retrieval and application remain fragile or sparsely evidenced.

**Tutor reading:** “Understanding is beginning — still provisional, still easy to overstate.”

**Typical trail:** Sparse confirming EC-C; soft signals may accompany but do not author the state alone.

**Must not claim:** Reliable retrieval, confident application, durable retention, exam readiness.

**Adjacent:** Coverage Emerging; Developing Competence; Inconsistent Progression (if early signals conflict).

---

### LPS-3 — Developing Competence

**Educational meaning:** Application (LO-05) and/or retrieval (LO-04) are forming across more than one session, with provisional understanding support — but not yet stable or dense enough for “reliable” language.

**Tutor reading:** “Competence is developing; keep practising and testing under varied conditions.”

**Typical trail:** Multi-session EC-C confirming accumulation; spacing (EC-E) still thin or mixed.

**Must not claim:** Durable knowledge; exam readiness; mastery from mission completion.

**Adjacent:** Emerging Understanding; Reliable Retrieval; Confident Application; Progression Stall.

---

### LPS-4 — Reliable Retrieval

**Educational meaning:** The student can bring knowledge back with reduced prompting across sessions (LO-04), with enough confirming accumulation to treat retrieval as educationally meaningful — still provisional, still not full durability.

**Tutor reading:** “You can retrieve this more reliably now — next we stress application forms and spacing.”

**Typical trail:** Confirming retrieval-emphasised EC-C; some EC-E helpful but not required for this state’s core meaning.

**Must not claim:** That retrieval equals exam readiness; that all application forms are secure; lasting mastery.

**Adjacent:** Developing Competence; Confident Application; Durable Knowledge (when spacing confirms); Inconsistent Progression.

---

### LPS-5 — Confident Application

**Educational meaning:** Application under attributable practice/assessment conditions is consistently supported across sessions (LO-05), including varied question forms where evidenced — still not a pass prophecy.

**Tutor reading:** “Practice shows you can apply this with growing confidence.”

**Typical trail:** Confirming EC-C/EC-D accumulation; soft confidence optional and never sole basis.

**Must not claim:** Durable retention without EC-E; whole-syllabus exam readiness; mastery from streaks.

**Adjacent:** Developing Competence; Reliable Retrieval; Durable Knowledge; Exam-Ready Progression (synthesis only).

---

### LPS-6 — Durable Knowledge

**Educational meaning:** Command holds after spacing and return (LO-06). Prior application/understanding warrant survives interruption — Estimated Mastery territory may be *approached* educationally, but Twin Mastery labels remain governed by EIP-006 / Twin writers, not by this state name alone.

**Tutor reading:** “This is holding up over time — lasting command looks more credible.”

**Typical trail:** Confirming EC-E plus prior EC-C/EC-D density.

**Must not claim:** Guaranteed exam success; mastery of neighbouring unpractised topics; permanent immunity to rust.

**Adjacent:** Confident Application; Exam-Ready Progression; Decaying Progression (if later returns weaken).

---

### LPS-7 — Exam-Ready Progression

**Educational meaning:** Synthesis judgement that preparation maturity for the named sitting is becoming credible (LO-07) for the relevant scope — integrating coverage, application, retention, revision posture, and Profile feasibility — always provisional.

**Tutor reading:** “Preparation is looking exam-credible on the evidence we have — still provisional, still honest about remaining gaps.”

**Typical trail:** Dense multi-class accumulation; mocks/exam-like evidence where available; Profile not contradicting feasibility.

**Must not claim:** Pass/fail prophecy; that coverage % alone earned this state; that one strong mock permanently certifies readiness.

**Adjacent:** Durable Knowledge / Confident Application; Inconsistent Progression; Progression Stall (late gaps); Decaying Progression.

---

## 5. Cross-Cutting Progression Conditions

These may overlay or replace a primary LPS when the trail demands honesty.

### LPS-S — Progression Stall

**Educational meaning:** Sessions continue (or effort continues) without meaningful advancement on the targeted learning objective(s); or the same failure pattern repeats.

**Tutor reading:** “Effort is present; growth is not — change the educational approach.”

**Must not claim:** Laziness as fact; incompetence as character.

**Typical response:** Interventions (reinforcement, prerequisites, retrieval emphasis) — see `LEARNING_INTERVENTIONS.md`.

---

### LPS-I — Inconsistent Progression

**Educational meaning:** Evidence trail conflicts — e.g. strong immediate performance with weak return; high confidence with weak application; topic-level unevenness that forbids a single smooth success story.

**Tutor reading:** “Signals disagree — we will not pretend they don’t.”

**Must not claim:** Averaged mastery; selective quoting of only favourable sessions.

---

### LPS-D — Decaying Progression

**Educational meaning:** Earlier warrant has weakened after interruption, long gap, or failed spaced return. Coverage may remain; understanding/application posture must be spoken more cautiously.

**Tutor reading:** “What was strong may have rusted — rebuild before reclaiming the old claim strength.”

**Must not claim:** That coverage was erased; that the student “never knew it.”

---

### LPS-A — Accelerating Progression

**Educational meaning:** Confirming accumulation is advancing faster than the prior trajectory, with warrant (not soft-signal inflation). Educationally invites careful challenge increase.

**Tutor reading:** “Growth is accelerating on evidence — we can raise challenge without skipping foundations.”

**Must not claim:** Permission to skip prerequisites; instant LPS-7.

---

## 6. Transition Principles

1. **Advance only with warrant.** LPS-n → LPS-(n+1) requires the accumulation pattern for the higher state — never calendar time alone.
2. **Completion does not advance past LPS-1.** Coverage Emerging is the ceiling for coverage-only trails.
3. **Downgrade honestly.** Conflict, decay, or failed returns may move a student to LPS-I, LPS-D, LPS-S, or an earlier primary state.
4. **Acceleration is conditional.** LPS-A overlays; it does not skip evidence gates.
5. **Exam-Ready Progression is synthesis.** It is not an automatic next step after LPS-6 on a single topic.
6. **Deterministic meaning.** Same trail + same prior posture → same educational transition meaning (implementation determinism is out of scope; meaning stability is in scope).
7. **Profile consistency.** Material LPS changes that contradict Profile states require Profile re-consultation — Learning Coach does not silently win.

Illustrative succession (not mandatory path):

```
LPS-0 → LPS-1 → LPS-2 → LPS-3 → LPS-4 / LPS-5 → LPS-6 → LPS-7
                ↘ LPS-S / LPS-I / LPS-D may appear at any stage after contact begins
```

---

## 7. Relationship to Profile States and Knowledge Ladder

| Learning progression posture | Often relates to | Must not collapse into |
|------------------------------|------------------|------------------------|
| LPS-1 Coverage Emerging | Profile Building Foundation; Study Progress rising | Estimated Knowledge |
| LPS-2 Emerging Understanding | Early Estimated Knowledge | Estimated Mastery |
| LPS-3–5 Developing / Retrieval / Application | Profile Practising; Competence semantics | Exam Ready Profile state by itself |
| LPS-6 Durable Knowledge | Mastery-wardant territory | Checkbox “Mastered” |
| LPS-7 Exam-Ready Progression | Profile Exam Preparation / Exam Ready (when Profile agrees) | Pass guarantee |
| LPS-S / LPS-I / LPS-D | Profile Strengthening / At Risk / Recovering colouring | Shame labels |

---

## 8. Scope of Assignment

Progression states may be spoken:

- **per syllabus unit / topic** (preferred educational precision);
- **per domain / subject area** when evidence attributes at that grain;
- **globally** only with explicit honesty about unevenness.

A global “Accelerating Progression” claim that hides stalled prerequisites is unlawful educational speech.

---

## 9. Cross References

| Document | Relationship |
|----------|--------------|
| `LEARNING_EVIDENCE_MODEL.md` | Accumulation patterns that warrant states |
| `LEARNING_INTERVENTIONS.md` | Responses especially for LPS-S / LPS-I / LPS-D / LPS-A |
| `LEARNING_EXPLAINABILITY.md` | How states are explained |
| `../student_profile/PROFILE_STATES.md` | Journey diagnosis postures |
| `../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` | Coverage / knowledge / competence / mastery meanings |
