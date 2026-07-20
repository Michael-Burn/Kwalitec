# Misconception Authoring Model

**Document ID:** V2-SAA-003  
**Classification:** Educational Architecture — Subject Authoring Foundation  
**Status:** Authoritative model of misconception authoring  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`SUBJECT_AUTHORING_MODEL.md`](SUBJECT_AUTHORING_MODEL.md)  

**Related:** [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md) · [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) · [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md) · [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md) · [`AUTHORING_INVARIANTS.md`](AUTHORING_INVARIANTS.md)

---

## 1. Purpose

This document defines how **misconceptions** are authored as first-class educational knowledge artefacts.

It answers:

> **What must an author capture so that a tutor can recognise, explain, and repair a stable wrong model?**

Misconception authoring is educational knowledge work. It is not writing “common mistakes” blog posts, not logging every student error, and not implementing a classifier.

---

## 2. Definition

**Misconception (authored):** a named, stable, incorrect mental model that systematically produces wrong reasoning or wrong answers with respect to one or more concepts — captured with observable evidence, causes, affected knowledge structure, typical incorrect reasoning, recommended teaching response, and criteria for repair.

### Governing distinctions

| This | Not this |
|------|----------|
| Stable wrong *model* | One-off slip or arithmetic error |
| Patterned across items/contexts | Single unexplained wrong answer |
| Attached to concept(s) | Free-floating “student is confused” |
| Repairable through teaching | Mere gap of never-having-seen the material (ignorance) |

Ignorance (“never taught”) and misconception (“wrongly constructed”) demand different Teaching Intentions. Authoring must not conflate them.

---

## 3. Why Misconceptions Are Authored

Without authored misconceptions:

- Diagnosis collapses into vague difficulty labels  
- Practice volume substitutes for contrastive repair  
- Strategies cannot be selected for *repair* vs *introduce* vs *fluency*  
- The Digital Twin cannot attribute patterned error to a knowledge target  

Anticipating misconceptions is part of making a concept teachable (Concept Architecture §4.5).

---

## 4. Authoring Schema

Every authored misconception captures the following fields. Fields may be thin in early drafts; permanent emptiness is authoring debt and may block treating the misconception as operational for diagnosis.

### 4.1 Description

**What to capture**  
A precise statement of the wrong model — what the student (implicitly) believes.

**Quality bar**  
Specific enough that two tutors would recognise the same pattern; not a vague “mixes up annuities.”

**Illustration**  
“Student treats continuous and discrete life-contingent formulae as freely interchangeable, believing the models differ only notationally.”

---

### 4.2 Observable Evidence

**What to capture**  
What performances, explanations, or classifications indicate the misconception is active — including characteristic error signatures and near-miss patterns.

**Quality bar**  
Evidence must be observable in principle (answers, explanations, classifications, representation translations). “Feels confused” is not evidence.

**Author obligations**

- Prefer converging indicators over a single MCQ miss  
- Note false positives (slips that mimic the pattern)  
- Separate strong indicators from weak ones  

**Illustration**  
Applies a continuous annuity formula to a clearly discrete payment schedule without adjustment; when asked, claims “the bar notation doesn’t matter.”

---

### 4.3 Likely Causes

**What to capture**  
Educational hypotheses about how the wrong model typically forms — prior teaching emphasis, notation overload, overgeneralisation from a narrow example set, missing prerequisite, etc.

**Quality bar**  
Causes are *likely*, not proven for every student. They inform Teaching Intention and Strategy; they do not replace diagnosis from evidence.

**Illustration**  
Over-exposure to continuous examples; notation introduced without payment-timing contrast; prerequisite gap on discrete vs continuous payment models.

---

### 4.4 Concept Affected

**What to capture**  
The concept(s) whose meaning is distorted. Required: at least one concept. Often also: related principles, rules, or formulae.

**Quality bar**  
Satisfies subject invariant K4 — every misconception belongs to one or more concepts.

**Illustration**  
Concepts: *annuity-due* / *annuity-immediate* timing; *continuous annuity*; principle: payment timing determines model class.

---

### 4.5 Dependencies Involved

**What to capture**  
Prerequisite or dependency failures that commonly co-occur with or enable the misconception — including whether foundation repair may be required before target-concept repair.

**Quality bar**  
Links to authored dependency structure where possible; avoids blaming “earlier chapters” without named entities.

**Illustration**  
Missing required grasp of discrete payment timing before continuous models were introduced.

---

### 4.6 Typical Incorrect Reasoning

**What to capture**  
The chain of reasoning the misconception produces — the student’s (reconstructed) justification, not only the wrong final answer.

**Quality bar**  
Makes contrastive teaching possible: tutors know *which* inference to break.

**Illustration**  
“Both use force of interest / mortality symbols; therefore the formulae are the same idea with different letters — so substitution is valid.”

---

### 4.7 Recommended Teaching Intentions

**What to capture**  
What educational change to seek next when this misconception is diagnosed — e.g. restore boundary discrimination, repair principle application, rebuild prerequisite, then re-anchor the target concept.

**Quality bar**  
Intentions must be lawful relative to the Teaching Intention Model: one clear change direction, not a laundry list of activities.

**Illustration**  
Intention: restore discrimination between discrete and continuous payment models; secondary: verify prerequisite on payment timing if evidence suggests absence rather than confusion.

---

### 4.8 Recommended Strategies

**What to capture**  
Instructional approach classes suited to the intention — e.g. contrastive examples/counterexamples, representation shift, worked-example comparison, diagnostic questioning — referencing Teaching Strategy Architecture / Catalogue at the level of *strategy kinds*, not scripts.

**Quality bar**  
Strategies must fit intention and diagnosis class (repair vs introduce). Volume practice alone is not a recommended repair strategy for a stable wrong model.

**Illustration**  
Strategy: contrastive teaching with side-by-side timelines and a counterexample that breaks free substitution; follow with classification of novel wordings.

---

### 4.9 Evidence of Repair

**What to capture**  
What new evidence would support that the wrong model has been weakened or replaced — explanation of the distinction, correct classification under variation, spontaneous rejection of the old substitution rule, retention after delay.

**Quality bar**  
Repair evidence must be stronger than “got the next clone right.” Prefer indicators that the *model* changed.

**Illustration**  
Student correctly refuses to swap continuous/discrete formulae and explains payment timing as the reason; succeeds on a reworded classification task after spacing.

---

## 5. Authoring Rules

1. **Name the model, not the emotion.** Misconceptions are cognitive structures.  
2. **Attach to concepts.** No orphan misconceptions.  
3. **Prefer frequency and cost.** Author high-frequency or high-damage misconceptions first for central syllabus concepts.  
4. **Distinguish slip, gap, and misconception** in guidance notes where confusion is likely.  
5. **Pair with contrast.** Important misconceptions should point to examples/counterexamples or representation contrasts that expose the fault line.  
6. **Keep repair falsifiable.** If no evidence of repair can be stated, the misconception is not yet operational for tutoring closure.

---

## 6. Relationship to Runtime Reasoning

| Runtime artefact | Uses authored misconception how |
|------------------|--------------------------------|
| Educational Diagnosis | May identify patterned error consistent with a named misconception |
| Educational Hypothesis | May cite likely causes from the authored record |
| Teaching Intention | May adopt recommended intentions, constrained by current evidence |
| Teaching Strategy | May select from recommended strategy kinds |
| Learning Episode | Enacts repair; collects evidence of repair |
| Digital Twin | May track belief about misconception presence/absence from evidence — never invents the misconception object |

Authoring proposes; runtime confirms or revises belief from evidence.

---

## 7. Completeness Levels

| Level | Meaning |
|-------|---------|
| **Stub** | Description + concept affected only — design debt |
| **Diagnostic** | Stub + observable evidence + typical incorrect reasoning |
| **Instructional** | Diagnostic + intentions + strategies |
| **Operational** | Instructional + dependencies involved + evidence of repair + likely causes |

Pathways that claim misconception-aware tutoring should treat **Operational** as the target for high-frequency misconceptions on core concepts.

---

## 8. Non-Goals

This model does not:

- Provide a universal catalogue of actuarial misconceptions  
- Define ML detection thresholds  
- Script tutor dialogue  
- Equate every wrong answer with a misconception  

---

## 9. Summary

Misconception authoring captures wrong models as teachable, diagnosable, repairable educational knowledge — with description, evidence, causes, concept and dependency links, incorrect reasoning, teaching response, and repair criteria — so the Educational Operating Model can confront error intentionally rather than by volume alone.
