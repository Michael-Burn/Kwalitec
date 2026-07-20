# Strategy Selection Model

**Document ID:** V2-TSA-004  
**Classification:** Educational Architecture — Teaching Strategy Foundation  
**Status:** Authoritative qualitative selection model  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md)  

**Related:** [`TEACHING_STRATEGY_CATALOGUE.md`](TEACHING_STRATEGY_CATALOGUE.md) · [`INSTRUCTIONAL_PRINCIPLES.md`](INSTRUCTIONAL_PRINCIPLES.md) · [`STRATEGY_COMPOSITION_MODEL.md`](STRATEGY_COMPOSITION_MODEL.md) · [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md) · [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md)

---

## 1. Purpose

This document defines **how Teaching Strategies are selected** in Kwalitec Version 2.

Selection is educational judgement under constraints. This model provides **qualitative decision rules only**. It does not specify algorithms, scores, machine-learning policies, or implementation heuristics.

---

## 2. Selection Stance

Strategy selection is lawful only when it:

1. **Serves** a named Teaching Intention (and atomic Teaching Goal for the next episode).  
2. **Fits** the Educational Diagnosis class and learning objective.  
3. **Respects** the working Educational Hypothesis (or deliberately discriminates among hypotheses).  
4. **Obeys** Instructional Principles and Strategy Invariants.  
5. **Remains** revisable when evidence warrants.

Strategy selection is **not**: choosing the most engaging activity; defaulting to more questions; matching UI templates; maximising content coverage; or reverse-fitting an intention to a favourite method.

---

## 3. Selection Inputs

| Consideration | What the tutor asks |
|---------------|---------------------|
| **Diagnosis** | What deficiency category and objective are primary? How strong is the warrant? |
| **Hypothesis** | What cause, if roughly right, should this strategy address or test? |
| **Teaching Intention** | What single educational change are we seeking next? |
| **Current understanding** | What can the student already explain, apply, or only recognise? |
| **Prerequisites** | What upstream gaps would make this strategy dishonest? |
| **Evidence history** | What patterns of error, success, retention, and transfer exist? |
| **Confidence calibration** | Is self-appraisal low, accurate, or falsely high relative to performance? |
| **Exam horizon** | Are examination constraints relevant *without* erasing conceptual duties? |
| **Cognitive load** | Can the student absorb this instructional demand now? |
| **Learning objective** | What syllabus-grounded aim must remain the accountability anchor? |

Thin inputs (cold start) do not waive selection; they narrow lawful strategies toward introduction-appropriate approaches under curriculum sequencing.

---

## 4. Qualitative Decision Rules

Rules are numbered for reference. They are not a flowchart that eliminates judgement.

---

### R-S1 — Intention gates the candidate set

Only strategies that can serve the stated Teaching Intention remain candidates. If no catalogue strategy fits, revise intention or diagnosis — do not force a mismatched method.

*Example:* Intention *Repair misconception* → Misconception Confrontation, Counterexample, Error-Led Teaching, Concept Comparison are primary candidates; Spaced Reinforcement alone is not.

---

### R-S2 — Diagnosis class constrains method family

Match strategy family to deficiency category:

| Diagnosis emphasis | Prefer method families |
|--------------------|------------------------|
| Misconception | Confrontation, counterexample, error-led, contrastive comparison |
| Conceptual absence / thin understanding | Direct explanation, analogy, guided discovery, dual representation |
| Prerequisite gap | Explanation/modelling on upstream objective; scaffolding; deliberate practice on upstream facet |
| Procedural / application weakness (concept adequate) | Worked example, progressive scaffolding, faded guidance, deliberate practice |
| Weak retention | Retrieval first/after instruction; spaced reinforcement |
| Fragmentation / discrimination failure | Concept comparison, concept mapping, interleaving |
| Transfer weakness | Interleaving, varied dual representation, guided discovery with variation |
| Exam technique (knowledge adequate) | Exam simulation, think-aloud modelling, interleaved mixed review |
| Low confidence (capacity evidenced) | Scaffolded success-visible practice; gentle Socratic; careful retrieval |
| False confidence | Discriminating probes, Socratic, counterexample, transfer variation |

---

### R-S3 — Hypothesis coherence or discrimination

- If a **working hypothesis** is clear, prefer a strategy that would succeed if that hypothesis is right.  
- If **competitors remain live**, prefer a strategy that produces discriminating evidence (often Socratic, counterexample, error-led, or contrastive comparison).  
- Do not pick a strategy that presupposes a hypothesis the evidence has already weakened.

---

### R-S4 — Understanding floor before memory and exam tactics

If current understanding is absent or misconception-dominated, do **not** select Exam Simulation, heavy Interleaving, or Spaced Reinforcement as the *primary* strategy for that contaminated objective. Apply P1 and P5 (understanding/repair before memorisation/extension).

---

### R-S5 — Modelling before independence for new procedures

When the student lacks a usable method schema, prefer Worked Example or Think-Aloud Modelling (then scaffolding) over Independent Practice or Deliberate Practice as the opening move (P6).

---

### R-S6 — Fade when evidence shows rising competence

When guided performance is reliable, prefer Faded Guidance / Independent Practice over adding scaffolds (P7). If errors rise after fade, re-scaffold temporarily or revise diagnosis — do not immediately escalate to exam simulation.

---

### R-S7 — Prerequisites veto dishonest strategies

If critical prerequisites are unmet, select strategies that serve *Strengthen prerequisite* (or schedule Prerequisite Repair episodes) before strategies that pretend the dependent objective can be taught honestly.

---

### R-S8 — Evidence history breaks ties

When multiple strategies remain fit:

- repeated failure under Strategy A → do not merely repeat A at higher volume; revise;  
- prior success with partial fade → continue composition rather than restart explanation theatre;  
- retention fade after prior success → prefer retrieval/spacing over re-introduction unless understanding also collapsed;  
- patterned error → prefer confrontation/error-led over undifferentiated deliberate practice.

---

### R-S9 — Confidence calibration modulates intensity and order

| Calibration state | Selection implication |
|-------------------|------------------------|
| Appropriately calibrated | Proceed with intention-fit strategy at normal demand |
| Low confidence, capacity evidenced | Prefer Progressive Scaffolding, Think-Aloud Modelling, gentler Socratic; avoid early high-stakes Exam Simulation |
| False confidence | Prefer discriminating strategies (Counterexample, Transfer variation, Socratic) before blocked fluency praise |
| Confidence collapse with real gaps | Prefer Repair / explanation strategies; do not use “confidence” framing to skip diagnosis |

---

### R-S10 — Exam horizon shapes, never erases

Near examinations:

- lawful to prefer Exam Simulation, Interleaving, Spaced Reinforcement on **adequately warranted** objectives;  
- unlawful to skip Misconception Confrontation on a known blocking misconception because “there is no time” without acknowledging educational debt;  
- lawful to run parallel atomic episodes: repair on contaminated objective; simulation on clean objectives.

---

### R-S11 — Cognitive load caps strategy ambition

Prefer simpler, more scaffolded strategies when load is high (fatigue, novelty density, anxiety, multi-representation demands). Dual Representation, Interleaving, and Guided Discovery are powerful but load-intensive — introduce only when capacity allows or scaffolds reduce load.

---

### R-S12 — Learning objective remains the anchor

Reject strategies that optimise engagement or coverage while drifting from the objective named in the Teaching Goal. Method novelty is never justification for objective drift.

---

### R-S13 — Prefer composition over overloaded single episodes

If the educational path needs Analogy then Worked Example then Guided Practice, select the **first** strategy for the next episode and commit the sequence in composition — do not collapse all three into one non-atomic episode.

---

### R-S14 — Justify or do not select

Every selected strategy requires a brief educational rationale linking diagnosis → hypothesis → intention → strategy. Unjustified defaults (“more questions”) are unlawful.

---

### R-S15 — Revise mid-stream when evidence contradicts

If early interaction evidence falsifies the strategy’s expected profile, revise strategy (and possibly hypothesis/diagnosis) before episode theatre completes. Mid-session revision is a feature of tutoring, not a failure of planning (see Composition Model exit conditions).

---

## 5. Worked Qualitative Examples

### 5.1 Misconception on select vs ultimate mortality

- **Diagnosis:** Misconception on select vs ultimate.  
- **Hypothesis:** Student treats select as cosmetic labelling.  
- **Intention:** Repair misconception.  
- **Selection:** Misconception Confrontation + Counterexample as composition; opening strategy Misconception Confrontation.  
- **Rejected:** Deliberate Practice on more mortality calculations (would rehearse the wrong model).

### 5.2 Thin GLM intuition, exam in months

- **Diagnosis:** Incomplete conceptual understanding.  
- **Intention:** Build intuition.  
- **Selection:** Analogy or Direct Explanation → Dual Representation; Retrieval After Instruction later.  
- **Rejected:** Immediate Exam Simulation (horizon exists but foundation does not).

### 5.3 Fluent untimed, timed collapse, knowledge adequate

- **Diagnosis:** Exam technique weakness.  
- **Intention:** Prepare for examination.  
- **Selection:** Think-Aloud Modelling (planning) → Exam Simulation; Interleaving if category selection fails under time.  
- **Rejected:** Re-teaching the whole chapter as if knowledge were absent.

### 5.4 Prior success, delayed fade

- **Diagnosis:** Weak retention.  
- **Intention:** Improve retention.  
- **Selection:** Retrieval First; Spaced Reinforcement across sessions.  
- **Rejected:** Full Concept Introduction restart without checking residual retrieval.

---

## 6. What This Model Explicitly Excludes

- Weighted scoring formulae  
- Multi-armed bandits or reinforcement-learning policies  
- Prompt templates that “select” strategies  
- UI A/B engagement metrics as educational authority  
- Mandatory one-to-one maps from diagnosis label to a single strategy

---

## 7. Summary Propositions

1. Strategy selection is qualitative educational judgement under explicit inputs.  
2. Intention gates candidates; diagnosis constrains families; hypothesis demands coherence or discrimination.  
3. Principles of understanding, repair, modelling, fading, load, and exam honesty order preferences.  
4. Evidence history and confidence calibration break ties and modulate intensity.  
5. Justification is mandatory; mid-stream revision is lawful; algorithms are out of scope for this architecture.
