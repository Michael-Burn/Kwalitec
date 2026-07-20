# Educational Hypothesis Model

**Document ID:** V2-ERM-002  
**Classification:** Educational Architecture — Reasoning Foundation  
**Status:** Authoritative model of educational hypotheses  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  
**Companions:** [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) · [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md) · [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md) · [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md)

---

## 1. Purpose

This document defines **Educational Hypotheses** for Kwalitec Version 2.

Diagnosis names *what* educational problem exists. An Educational Hypothesis proposes *why* that problem is occurring. Hypotheses turn tutoring from reactive content assignment into reasoned educational inquiry.

This is educational architecture. It is not statistical hypothesis testing as a software feature, not an algorithm, and not an AI prompt pattern.

---

## 2. Definition

**Educational Hypothesis:** the tutor’s current, revisable explanation for *why* the student is experiencing a diagnosed educational difficulty.

A hypothesis answers:

> *Why is this educational problem present?*

Examples (illustrative, actuarial):

- “I believe the student struggles with GLMs because exponential-family intuition is missing.”  
- “I believe repeated mistakes come from weak prerequisites rather than careless arithmetic.”  
- “I believe exam errors are caused by poor transfer rather than lack of knowledge.”  
- “I believe false confidence comes from success on textbook clones without varied stems.”  
- “I believe the student avoids reserves questions because of low confidence despite adequate conceptual evidence.”

Hypotheses are **explanations**, not labels of deficiency. The deficiency label belongs to diagnosis; the causal/educational reading belongs to hypothesis.

---

## 3. Purpose of Hypotheses

Hypotheses exist so that teaching can be designed as a **test of educational understanding of the learner**, not merely as delivery of more material.

Without hypotheses:

- every wrong answer invites the same response (“more practice”);  
- tutors cannot explain *why* a recommendation was chosen beyond the surface error;  
- competing interpretations of the same evidence remain invisible;  
- failure of teaching cannot revise belief about the learner.

With hypotheses:

- teaching intentions become discriminating;  
- success and failure of an episode update educational belief;  
- multiple readings can compete honestly;  
- recommendations gain deeper educational justification.

---

## 4. Relationship to Diagnosis and Intention

```text
Evidence + Reflection
        ↓
Educational Diagnosis   (WHAT problem)
        ↓
Educational Hypothesis  (WHY it likely exists)
        ↓
Teaching Intention      (WHAT change to seek next)
        ↓
Teaching Strategy       (HOW to seek it)
```

| Concept | Question | Example |
|---------|----------|---------|
| Diagnosis | What is wrong? | Prerequisite gap on exponential families for GLM objectives |
| Hypothesis | Why is it wrong / why does this pattern appear? | Because the student never built exponential-family intuition before GLM notation |
| Intention | What change do we seek next? | Strengthen the prerequisite |
| Strategy | How? | Concept introduction with contrastive examples, then a probe |

A diagnosis without a hypothesis may still allow crude teaching (“address the gap”). Mature tutoring prefers an explicit hypothesis so that episode outcomes can confirm or refute the tutor’s reading.

---

## 5. Characteristics of Educational Hypotheses

Educational Hypotheses are:

1. **Explanatory** — they propose a reason, not only a category.  
2. **Evidence-relative** — they cite supporting and contradicting observations.  
3. **Provisional** — held with confidence levels, never as dogma.  
4. **Testable by teaching** — a well-formed hypothesis implies what instructional move should change observable outcomes if the hypothesis is roughly right.  
5. **Replaceable** — when contradicted, they yield to better explanations.  
6. **Curriculum-grounded** — they refer to objectives, prerequisites, and legitimate exam demand.  
7. **Non-moral** — they explain educational state, not character.  
8. **Distinct from Twin estimates** — Twin holds standing belief; a hypothesis is an active explanatory commitment used to guide the next teaching move.

A statement fails as a hypothesis if it is:

- unfalsifiable by any educational outcome (“the student is just bad at maths”);  
- identical to the diagnosis with no added explanation;  
- a disguised teaching strategy (“we should drill more”);  
- an engagement claim (“they’re bored”) presented as educational cause without warrant.

---

## 6. Confidence

Every Educational Hypothesis carries an honest **confidence posture**:

| Posture | Meaning |
|---------|---------|
| **Tentative** | Thin or conflicting evidence; teach primarily to discriminate among readings |
| **Working** | Enough converging evidence to guide intention; still revisable |
| **Strong** | Repeated, multi-source support; still not infallible |
| **Suspended** | Temporarily held aside while a competing hypothesis is tested |

Confidence rules:

1. Confidence alone never creates a diagnosis or a hypothesis.  
2. High confidence does not freeze a hypothesis against new contradictory evidence.  
3. Low confidence should bias toward diagnostic or discriminating teaching intentions, not toward mastery claims.  
4. Reflection that merely asserts a cause (“I fail because I’m stupid”) is soft signal, not automatic adoption of that hypothesis.

---

## 7. Revision

Hypotheses are revised when:

- new evidence weakens the explanatory fit;  
- teaching designed to test the hypothesis produces outcomes better explained another way;  
- reflection reveals a metacognitive pattern that relocates the cause;  
- Twin-accumulated history shows the original reading was local or stale.

Revision is not failure. Refusal to revise is educational malpractice.

**Revision forms:**

- **Narrowing** — same family of explanation, tighter scope.  
- **Broadening** — cause is more general than first thought.  
- **Shift** — different deficiency category becomes the better explanation.  
- **Layering** — primary cause plus contributing secondary cause.

---

## 8. Replacement

A hypothesis is **replaced** when another explanation better accounts for the total evidence — not when a single episode merely fails for incidental reasons (fatigue, misread stem, one slip).

Replacement discipline:

1. State what evidence the old hypothesis cannot absorb.  
2. State the new hypothesis and its warrant.  
3. Preserve useful partial insights (layering) when appropriate.  
4. Update teaching intention accordingly.  
5. Do not silently keep teaching as if the old hypothesis still governs.

---

## 9. Multiple Competing Hypotheses

Tutors may hold **more than one** competing hypothesis when evidence underdetermines explanation.

Example:

- H1: “Errors on with-profits valuation come from misconception about bonus structures.”  
- H2: “Errors come from procedural weakness in surplus distribution calculations.”  
- H3: “Errors come from transfer weakness; knowledge is present only on drilled stems.”

Rules for competition:

1. Competitors must be educationally distinct — not rewordings of one idea.  
2. Teaching Intention should prefer a move that **discriminates** among competitors when stakes are high or confidence is tentative.  
3. Do not average incompatible hypotheses into a vague “general weakness.”  
4. After discriminating evidence arrives, demote or retire losers explicitly.  
5. Priority among simultaneous *diagnoses* follows the Priority Model; competition among *hypotheses* for one diagnosis is resolved by evidential fit and discriminating teaching.

---

## 10. Evidence Supporting Hypotheses

Supporting evidence strengthens explanatory fit. Illustrative forms:

| Support type | Example |
|--------------|---------|
| Patterned performance | Same wrong model across varied items |
| Explanatory congruence | Student’s own-words explanation matches the suspected wrong model |
| Prerequisite probes | Upstream failure predicts downstream failure |
| Contrastive success | Performance recovers when the suspected factor is removed |
| Delayed probes | Fade pattern supports retention hypothesis over “never learned” |
| Transfer probes | Clone success + variant failure supports transfer hypothesis |
| Reflection alignment | Student reports “I freeze when wording changes” aligned with transfer reading |

Support must remain distinguishable from the hypothesis itself. Evidence is observation; hypothesis is interpretation.

---

## 11. Evidence Contradicting Hypotheses

Contradicting evidence weakens or defeats a hypothesis. Illustrative forms:

| Contradiction type | Example |
|--------------------|---------|
| Successful prerequisite probe | Upstream skill present → prerequisite-gap hypothesis weakens |
| Correct conceptual explanation with only execution errors | Misconception hypothesis weakens; procedural weakness strengthens |
| Failure on clones as well as variants | Pure transfer hypothesis weakens |
| Stable success after delay | Weak-retention hypothesis weakens for that objective |
| Pattern breaks under re-check | Suspected “stable misconception” may have been noise or incomplete understanding |
| Confidence–performance alignment | False-confidence hypothesis weakens if self-appraisal matches evidence |

Contradictions require response: revise, replace, suspend, or lower confidence. Ignoring contradictions preserves false tutoring.

---

## 12. Why Tutors Teach to Test Hypotheses

Expert tutors do not only teach to transmit content. They teach to **test whether their reading of the learner is right**.

Teaching to test a hypothesis means:

1. Choosing a Teaching Intention whose success would be expected if the hypothesis is roughly correct.  
2. Choosing a Teaching Strategy that makes the critical factor visible.  
3. Collecting evidence that could confirm *or* refute the reading.  
4. Interpreting outcomes as informational about the learner, not only as scores.

**Educational rationale:**

- Underdetermined evidence is common in exam preparation.  
- The cost of acting on the wrong explanation (drilling a misconception, extending past a prerequisite gap) is high.  
- Discriminating episodes convert uncertainty into warranted belief faster than undifferentiated volume.  
- Hypothesis-testing teaching preserves explainability: “We tried X because we believed Y; the outcome suggests Z.”

Teaching that never risks refuting the tutor’s belief is dogma, not tutoring.

**Actuarial illustration**  
Hypothesis: “GLM struggle is due to missing exponential-family intuition.”  
Intention: Strengthen prerequisite.  
Episode: short Concept Introduction on exponential families with probes.  
If probes succeed and GLM items then improve, hypothesis gains support.  
If probes succeed but GLM items still fail with a patterned wrong model, replace with a misconception or transfer hypothesis and change intention.

---

## 13. Hypotheses and the Student Digital Twin

- Hypotheses are **episodic reasoning commitments** used to choose the next move.  
- Twin estimates are **standing educational belief** about knowledge, mastery, confidence, retention, readiness.  
- Confirmed or revised hypotheses may lawfully influence how evidence is interpreted into Twin updates.  
- Twin fields must not silently freeze a hypothesis forever.  
- Students need not see the word “hypothesis”; they need explainable recommendations. Educational governance still requires the concept.

---

## 14. Summary Propositions

1. An Educational Hypothesis explains why a diagnosed difficulty exists.  
2. Hypotheses are provisional, evidence-relative, and revisable.  
3. Multiple competing hypotheses are lawful and often necessary.  
4. Teaching should often be designed to test hypotheses.  
5. Supporting and contradicting evidence must both be tracked.  
6. Hypotheses bridge Diagnosis and Teaching Intention without selecting Teaching Strategy themselves.
