# Session Transitions

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS002 — Learning Session Model  
**Classification:** Educational rules for moving between study-session phases  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **when a student should move between Learning Session phases**.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `LEARNING_SESSION_MODEL.md`
3. `SESSION_OBJECTIVES.md`
4. `SESSION_STRUCTURE.md`
5. `../daily_coach/DAILY_COACH_MODEL.md`
6. `EDUCATIONAL_EVIDENCE_MODEL.md`

> **Transitions depend on educational progress.  
> Elapsed time may constrain capacity; it must not be the sole authority for phase change.**

---

## 1. Purpose

An expert IFoA tutor does not say “twenty minutes are up, so we must practise now” regardless of understanding. The tutor watches for **educational readiness**: Has the idea landed? Is retrieval failing? Are misconceptions active? Is fatigue corrupting effort?

This document records that judgement so future session engines do not collapse learning into clocks.

Identifiers (LST-XX) exist for traceability. Educational meaning is binding; timer implementations are out of scope.

---

## 2. Transition Principles

1. **Progress before clock.** Primary transition warrants are educational signals.
2. **Time is a capacity constraint.** Running out of available study time may force a lawful early close — it does not prove the previous phase was educationally complete.
3. **One reason preferred.** Prefer a single clear educational warrant for moving on.
4. **Backward moves are lawful.** Returning to encoding or worked examples after failed retrieval is good tutoring — not “going backwards.”
5. **Skip only with purpose.** Omitting a phase requires today’s work type or local adaptation warrant — not convenience.
6. **Interrupts beat denial.** Misconception and fatigue signals may interrupt the planned order.
7. **Close with honesty.** Entering reflection/review should happen when the educational arc needs closing — including abbreviated closes under time pressure.
8. **No mastery gate theatre.** Transition readiness is not a claim that the student has mastered the topic.
9. **Deterministic posture.** Same signals → same transition class (advance / hold / regress / close / escalate).
10. **Objective fidelity.** Transitions never authorise a new Daily Coach job by stealth.

---

## 3. Educational Progress Signals

Transitions may cite the following **signal classes**. Signals are educational observations or cautious estimates — not Twin facet dumps.

| Signal class | Meaning | Typical claim posture |
|--------------|---------|------------------------|
| **Orientation clarity** | Student can restate today’s session objective and intended scope | Observed / soft check |
| **Encoding sense-check** | Short checks suggest the core idea/method is at least provisionally formed | Cautious estimate / check |
| **Retrieval success / failure** | Closed-book reconstruction succeeds, partially succeeds, or fails | Observed attempt outcomes |
| **Application fluency** | Worked or independent attempts show improving method legality | Observed / derived |
| **Systematic error** | Repeated wrong model / illegal step pattern | Derived from attempts |
| **False fluency** | Recognition or confidence high while retrieval/application fails | Derived contrast |
| **Cognitive overload / fatigue** | Effort quality collapsing; errors becoming careless rather than conceptual | Observed / student-reported |
| **Interruption** | External break that suspends the sitting | Observed fact |
| **Capacity remaining** | Declared remaining study time / intensity envelope | Observed / plan-derived |
| **Objective completion sense** | Today’s session aims for this sitting are as far advanced as honesty allows | Educational judgement — not mastery |

Thin evidence ⇒ prefer **hold** or **gentle advance** over confident claims.

---

## 4. Transition Catalogue

### LST-01 — Enter preparation → leave preparation

| Aspect | Rule |
|--------|------|
| **Advance when** | Student can state today’s objective and the sitting’s intended scope (orientation clarity) |
| **Hold when** | Objective is unclear, conflicting with day posture, or student cannot name what success would look like educationally |
| **Must not** | Skip preparation on dense first-pass/practice days solely to “save minutes” when confusion is likely |

---

### LST-02 — Focused learning → next phase

| Aspect | Rule |
|--------|------|
| **Advance when** | Encoding sense-checks pass for the chunk in scope **or** today’s job only required a brief refresh |
| **Regress / extend when** | Sense-checks fail; confusion remains high; misconceptions appear during encoding |
| **Advance to retrieval/examples when** | A coherent chunk exists to retrieve or exemplify |
| **Must not** | Advance solely because a reading timer ended |

---

### LST-03 — Worked examples → independent work

| Aspect | Rule |
|--------|------|
| **Advance when** | Student can follow and partially reconstruct the expert decisions; faded support becomes tolerable |
| **Hold / add example when** | Student can only copy final answers without grasping decision points |
| **Skip examples when** | Fluency already evidenced and today’s job is independent practice/revision |
| **Must not** | Keep showing solutions indefinitely to avoid productive struggle that today’s job requires |

---

### LST-04 — Enter / leave active retrieval

| Aspect | Rule |
|--------|------|
| **Enter when** | Enough encoding exists that retrieval is meaningful for today’s objective |
| **Advance after retrieval when** | Feedback has been given and either success warrants practice/next chunk, or failure warrants regress to encoding/examples/misconception repair |
| **Hold in retrieval cycle when** | False fluency is detected — more recognition would mislead |
| **Must not** | Treat one successful recall as licence to declare the topic done for the journey |

---

### LST-05 — Question practice transitions

| Aspect | Rule |
|--------|------|
| **Enter when** | Encoding + examples (as needed) make practice educational rather than random flailing; DCO-03 / work type authorises practice |
| **Increase difficulty when** | Current level shows lawful method with stable success |
| **Decrease scaffolding slowly when** | Fluency grows |
| **Pause practice for repair when** | Systematic errors dominate attempts |
| **Leave practice when** | Target practice aim for the sitting is honestly met **or** capacity/fatigue requires close **or** escalation is needed |
| **Must not** | Keep assigning volume after fatigue destroys learning quality just to finish a count |

---

### LST-06 — Misconception interrupt

| Aspect | Rule |
|--------|------|
| **Interrupt current phase when** | Systematic error or false fluency is clear and continuing would entrench the wrong model |
| **Return to prior phase when** | Repair needs encoding or worked contrast |
| **Resume forward when** | The specific misconception is addressed enough for today’s objective to continue |
| **Escalate when** | Misconception repair would require changing today’s educational job or exploding scope beyond envelopes |

---

### LST-07 — Enter reflection and session review

| Aspect | Rule |
|--------|------|
| **Enter reflection when** | The main learning/practice arc for this sitting should close — including early close under capacity pressure |
| **Abbreviate when** | Time is nearly gone; prefer short honest reflection over skipping entirely on ordinary study days |
| **Enter session review when** | Reflection (even brief) has named residue **or** interruption forces administrative close with acknowledged debt |
| **Must not** | Delay reflection forever to chase one more question when capacity is gone; force mastery language in close |

---

### LST-08 — Early close / suspend

| Aspect | Rule |
|--------|------|
| **Early close when** | Capacity remaining hits zero; interruption ends the sitting; fatigue makes further effort counterproductive |
| **Educational duty** | Preserve LSO-00 narrative: what was served of today’s objective; what remains; no invented day rewrite |
| **Resume later** | Re-orientation (short LSP-01) before continuing the same day’s objective if the day still holds |

---

### LST-09 — Escalate instead of transitioning

| Aspect | Rule |
|--------|------|
| **Escalate to Daily Coach when** | No lawful phase transition can continue serving DCO-01 honestly (see `SESSION_ADAPTATION.md`) |
| **Examples** | Wrong-day objective discovered; recovery envelopes broken by needed intensity; topic authority conflict; sitting cannot proceed without redefining the job |
| **Must not** | “Transition” into a different educational job disguised as the next phase |

---

## 5. Transition Decision Posture

For any proposed phase change, classify as one of:

| Posture | Meaning |
|---------|---------|
| **Advance** | Move to the next planned phase in the composed arc |
| **Hold** | Remain; deepen or repeat with feedback |
| **Regress** | Return to an earlier phase (encoding, examples, misconception repair) |
| **Interrupt** | Insert misconception check or fatigue pause |
| **Skip (lawful)** | Omit a phase because today’s work type / readiness makes it unnecessary |
| **Close** | Enter reflection/review or suspend |
| **Escalate** | Stop local transition logic; return authority to Daily Coach |

Same inputs should yield the same posture class.

---

## 6. Time’s Lawful Role

| Lawful use of time | Unlawful use of time |
|--------------------|----------------------|
| Bound total session load to Daily Coach capacity envelopes | Force phase changes on fixed minute marks regardless of understanding |
| Trigger early close when remaining capacity is exhausted | Claim educational completion because the clock finished |
| Suggest sustainable chunking to protect focus (LSO-08) | Punish slow encoding with invented overload in the next phase |
| Inform abbreviated reflection under time pressure | Skip all reflection forever as default “efficiency” |

Timers may exist in product implementation later. They are **not educational authorities** in this model.

---

## 7. Examples (Tutor Reasoning)

**Example A — First-pass, sense-check fails**  
Student finishes a reading chunk but cannot restate the method’s triggering conditions.  
→ **Hold / extend LSP-02** or **regress from early LSP-04**; do not advance to heavy LSP-05.

**Example B — Practice reveals systematic error**  
Three attempts misuse the same formula condition.  
→ **Interrupt (LST-06)** → misconception repair → then resume practice or examples.

**Example C — Rapid fluency on revision day**  
Retrieval succeeds repeatedly; practice is clean.  
→ **Advance difficulty within revision job**; do **not** open undeclared new first-pass topics.

**Example D — Ten minutes left**  
Main practice incomplete.  
→ **Close path (LST-07/08)**: brief reflection + honest residue; do not fake “session complete = mastered.”

**Example E — Student realises today should be recovery**  
Declared capacity and fatigue contradict a dense practice arc, and envelopes cannot absorb it.  
→ **Escalate (LST-09)** — do not silently convert the day inside transition logic.

---

## 8. Cross References

| Document | Relationship |
|----------|----------------|
| [`SESSION_STRUCTURE.md`](SESSION_STRUCTURE.md) | Phases being transitioned |
| [`SESSION_ADAPTATION.md`](SESSION_ADAPTATION.md) | Broader adaptation and escalation rules |
| [`SESSION_OBJECTIVES.md`](SESSION_OBJECTIVES.md) | Aims that define “enough progress” |
| [`../daily_coach/DAILY_COACH_DECISION_MODEL.md`](../daily_coach/DAILY_COACH_DECISION_MODEL.md) | Day-level escalation sibling |
| [`../EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) | Lawful evidence for progress signals |
