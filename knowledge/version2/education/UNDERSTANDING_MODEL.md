# Understanding Model

**Document ID:** V2-EDM-003  
**Classification:** Educational Domain Foundation  
**Status:** Authoritative model of understanding  
**Nature:** Documentation only — no runtime behaviour  
**Parent:** [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  
**Companion:** [`LEARNING_MODEL.md`](LEARNING_MODEL.md)  

---

## 1. Purpose

This document defines **understanding** for Kwalitec.

It establishes:

- how novices and experts typically think in professional quantitative domains;  
- what indicates genuine understanding;  
- what falsely appears to be understanding;  
- observable behaviours that tutors may seek;  
- a progressive ladder of understanding levels.

**Governing claim:** Correct answers alone do not prove understanding.

---

## 2. What Understanding Is

Understanding is the student’s grasp of meaning, structure, and justification within a curriculum domain: knowing what a concept is, how it relates to others, why methods work, and when they apply.

Understanding is:

- **Explanatory** — the student can make the idea intelligible;  
- **Relational** — the student connects the idea to principles and neighbours;  
- **Conditional** — the student knows limits and assumptions;  
- **Actionable** — the student can use the idea under variation;  
- **Inferred** — attributed from converging evidence, never from assertion alone.

Understanding is not identical to:

- familiarity (“I have seen this”);  
- recognition (“I pick the right option”);  
- fluency alone (“I can compute quickly”);  
- confidence (“I feel ready”).

---

## 3. How Novices Think

In actuarial and related professional study, novices commonly exhibit the following patterns. These are educational observations, not moral judgements.

### 3.1 Surface-feature attention

Novices classify problems by wording cues (“it says annuity”) rather than by underlying structure (payment timing, contingency, interest model).

### 3.2 Formula-first reasoning

Novices reach for a remembered expression before asking what quantity is required and under what assumptions.

### 3.3 Fragile procedures

Novices can execute a drilled sequence when prompts match practice, then stall when a step is reordered or an assumption changes.

### 3.4 Local coherence, global fragmentation

Novices may perform adequately inside one worked example while holding incompatible beliefs across examples (for instance, inconsistent treatment of timing).

### 3.5 Misplaced confidence

After recognising familiar notation, novices often overestimate readiness for exam-style novelty.

### 3.6 Error blindness to principle

Novices interpret wrong answers as arithmetic slips even when the method chosen was invalid.

**Tutor implication:** novice support must build conceptual structure and condition-of-use knowledge, not only more near-identical drills.

---

## 4. How Experts Think

Experts in the same domains typically show contrasting patterns.

### 4.1 Structure-first perception

Experts see deep structure quickly: cash-flow pattern, contingency, measurement basis, and required present-value relationship.

### 4.2 Principle-governed method choice

Experts select methods from principles (equivalence, consistency of bases, continuous vs discrete modelling) rather than from keyword matching.

### 4.3 Fluent recovery

Experts still err occasionally; they detect inconsistency faster and repair from principle.

### 4.4 Compression and elaboration

Experts can compress a topic into a small set of governing ideas and elaborate those ideas into procedures when needed.

### 4.5 Transfer readiness

Experts expect surface variation and treat it as normal rather than as a different subject.

### 4.6 Calibrated uncertainty

Experts more often know what they do not yet know, and can name the missing assumption or lemma.

**Tutor implication:** the path from novice to expert is not “more content.” It is restructuring perception, principle use, and transfer practice.

---

## 5. Indicators of Genuine Understanding

The following indicators, especially in combination, support an inference of understanding:

1. **Own-words explanation** of a concept without relying solely on memorised textbook phrasing  
2. **Justification** of why a method is appropriate for a given problem  
3. **Boundary knowledge** — stating when a method does *not* apply  
4. **Representation flexibility** — moving between formula, timeline, table, and narrative  
5. **Error diagnosis** — explaining what is wrong in an incorrect solution, not only supplying a correct one  
6. **Variation success** — maintaining performance when surface features change  
7. **Prerequisite use** — correctly invoking earlier ideas inside later tasks  
8. **Predictive thought** — anticipating how a result should behave if a parameter changes  
9. **Teaching attempt** — explaining the idea so that another learner could begin to use it (see levels below)  
10. **Stable revisit** — retaining explanatory power after delay  

No single indicator is absolute proof. Convergence across indicators strengthens the claim.

---

## 6. False Indicators

The following commonly mislead students and systems into believing understanding exists when it may not:

| False indicator | Why it misleads |
|-----------------|-----------------|
| Correct final numeric answer | May result from template match, cancelled errors, or recognition |
| High score on identical practice clones | Measures familiarity with a set, not flexible grasp |
| Speed | May reflect rote fluency without principle |
| “I get it” self-report | Confidence ≠ comprehension |
| Ability to recite a definition | Verbal memory ≠ relational understanding |
| Having studied the chapter | Coverage ≠ understanding |
| Watching a full explanation | Exposure ≠ uptake |
| One successful mock question on a topic | Insufficient temporal and transfer breadth |
| Matching worked-example steps while looking at the example | Scaffolded mimicry, not independent grasp |

**Hard rule:** a correct answer is evidence of *something* (possibly recognition or lucky procedure). It is never, by itself, sufficient evidence of understanding.

---

## 7. Observable Behaviours

Tutors and educational design should prefer behaviours that can be observed or elicited:

| Behaviour class | Examples |
|-----------------|----------|
| Explain | State meaning; paraphrase; give a non-example |
| Justify | Say why this method; cite the governing principle |
| Classify | Sort problems by structure, not keywords |
| Contrast | Distinguish related concepts (select vs ultimate; prospective vs retrospective) |
| Transform | Convert a word problem into a timeline or equation |
| Critique | Find the flaw in a plausible wrong solution |
| Vary | Solve a reparametrised or reworded sibling problem |
| Predict | Forecast direction of change when *i* or *μ* changes |
| Revisit | Explain again after an interval without notes |

Where only product-constrained observations are available (for example right/wrong marks), understanding claims must remain correspondingly modest.

---

## 8. Levels of Understanding

Understanding develops. Kwalitec recognises a progressive ladder. Higher levels presuppose lower ones educationally; assessment at a high level that skips lower probes may still be informative but must be interpreted carefully.

```text
Recognition
    ↓
Explanation
    ↓
Application
    ↓
Analysis
    ↓
Teaching Others
```

### 8.1 Recognition

**Description**  
The student identifies familiar terms, symbols, and standard problem types.

**Typical evidence**  
Correct identification; matching; selecting a named formula from a list.

**Limit**  
Recognition is the floor of familiarity, not understanding in the strong sense.

**Actuarial example**  
Recognising that “āₓ” denotes an annuity present value symbol.

---

### 8.2 Explanation

**Description**  
The student can say what a concept means and how its parts relate.

**Typical evidence**  
Own-words definition; description of cash-flow meaning; stating assumptions.

**Limit**  
Explanation without application may remain verbal.

**Actuarial example**  
Explaining that a whole life assurance pays on death, with EPV integrating discounted probability-weighted payments.

---

### 8.3 Application

**Description**  
The student uses the concept to solve legitimate tasks.

**Typical evidence**  
Correct method and result on standard and mildly varied problems.

**Limit**  
Application can still be template-bound; transfer probes are needed.

**Actuarial example**  
Computing an assurance EPV from a life table and effective interest rate.

---

### 8.4 Analysis

**Description**  
The student decomposes complex or mixed situations, selects among methods, and evaluates assumptions.

**Typical evidence**  
Multi-concept solutions; critique of methods; “which model is appropriate?” judgements.

**Limit**  
Strong analysis on one occasion still needs retention and transfer for mastery-level claims.

**Actuarial example**  
Given a hybrid benefit description, separating assurance and annuity components and justifying the valuation approach.

---

### 8.5 Teaching Others

**Description**  
The student can present the idea so another learner could begin to understand and apply it: clear structure, apt examples, anticipation of likely confusions.

**Typical evidence**  
Coherent mini-explanation; construction of a clarifying example; naming a common misconception and correcting it.

**Limit**  
In solo exam preparation, this level may be elicited through “explain as if teaching” prompts rather than literal peer tutoring. The educational meaning remains: generative, structured command of the idea.

**Actuarial example**  
Teaching the difference between contingent and deferred benefits with a timeline and one trap wording examiners use.

---

## 9. Progression Rules

1. **Higher is not automatic.** Completing application practice does not grant analysis-level understanding.  
2. **Lower supports higher.** Persistent recognition-only performance signals that explanation work is still required.  
3. **Regression is real.** Under time pressure or after delay, students may fall to a lower level; that is educationally informative.  
4. **Level labels are estimates.** They must be framed as inferred from evidence, not as certificates.  
5. **Exam readiness** typically requires solid application and emerging analysis/transfer on weighted objectives — not recognition alone.

---

## 10. Understanding and the Five Learning Dimensions

| Learning dimension | Role of understanding |
|--------------------|----------------------|
| Understanding | Directly this model’s subject |
| Application | Requires enough understanding to choose and execute methods |
| Connection | Is largely relational understanding across ideas |
| Retention | Includes retained explanatory structure, not only retained steps |
| Transfer | Strong practical test of understanding under novelty |

---

## 11. Summary Propositions

1. Understanding is explanatory, relational, conditional grasp — inferred from evidence.  
2. Novices attend to surfaces; experts attend to structure and principle.  
3. Genuine indicators emphasise explanation, justification, boundaries, variation, and critique.  
4. Correct answers, speed, confidence, and coverage are false indicators when used alone.  
5. Understanding develops through Recognition → Explanation → Application → Analysis → Teaching Others.  
6. **Correct answers alone do not prove understanding.**
