# Educational Glossary

**Document ID:** V2-EDM-006  
**Classification:** Educational Domain Foundation  
**Status:** Authoritative educational vocabulary  
**Nature:** Documentation only — no runtime behaviour  
**Parent:** [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  

---

## 1. Purpose

This glossary is the alphabetical companion to the Educational Domain Model: the educational equivalent of **ubiquitous language** in domain-driven design.

When Kwalitec documents, product copy, architecture, or future implementation speak educationally, they should use these terms with these meanings — or use plain-language equivalents that preserve the meaning without smuggling in false synonyms (for example, never using “mastered” to mean “completed”).

Entries follow a fixed pattern:

- **Definition**  
- **Related terms**  
- **Notes**  

For full conceptual treatment, see the Domain Model and its companion models.

---

## 2. Glossary Entries

### Adaptation

**Definition:** The tutor’s choice of the next educational move after interpreting evidence — continuing, changing strategy, repairing a misconception, spacing for retention, introducing transfer variation, or advancing objectives.

**Related terms:** Tutor loop; Interpretation; Teaching Strategy; Recommendation.

**Notes:** Adaptation without interpretation is thrash (Invariant I15).

---

### Application (learning dimension)

**Definition:** The student’s ability to use knowledge to perform legitimate syllabus tasks (calculate, classify, derive, decide).

**Related terms:** Learning dimensions; Procedural Fluency; Understanding; Transfer.

**Notes:** Application success on clones is weaker than application under variation.

---

### Assessment

**Definition:** Any structured elicitation of performance used to judge capacity relative to a learning objective.

**Related terms:** Evidence; Teaching; Learning Objective.

**Notes:** Diagnostic assessment discovers need; post-teaching assessment evaluates instructional effect. Teaching precedes assessment of a taught aim (Invariant I3).

---

### Competence

**Definition:** Reliable ability to apply knowledge when asked; stronger than momentary recognition, weaker than full mastery if retention and transfer are unproven.

**Related terms:** Knowledge; Mastery; Application; Understanding.

**Notes:** Aligns with the Knowledge & Mastery Educational Model ladder; do not equate with Study Progress.

---

### Conceptual Understanding

**Definition:** Grasp of meanings, relationships, principles, and conditions of validity — the “what” and “why.”

**Related terms:** Understanding; Procedural Fluency; Explanation (understanding level).

**Notes:** Necessary partner to procedural fluency for professional examinations.

---

### Connection (learning dimension)

**Definition:** The student’s ability to relate ideas across a topic and across related syllabus areas, seeing shared structure rather than isolated facts.

**Related terms:** Learning dimensions; Understanding; Curriculum; Transfer.

**Notes:** Combination exam questions heavily tax connection.

---

### Coverage

**Definition:** The extent to which syllabus material has been studied or marked studied; answers “what have I been through?”

**Related terms:** Study Progress; Completion; Understanding; Mastery.

**Notes:** Coverage is never proof of understanding or mastery (Invariant I8, I2).

---

### Curriculum

**Definition:** The official syllabus structure and content that organise legitimate study aims for a professional examination pathway.

**Related terms:** Learning Objective; Curriculum primacy; Topic.

**Notes:** Tutoring remains accountable to curriculum identity (Invariant I16).

---

### Diagnosis (Educational Diagnosis)

**Definition:** Reasoned identification of the student’s current educational problem — what is deficient, distorted, fragile, missing, or miscalibrated relative to learning objectives. Diagnosis answers *what problem exists*; it does not decide *how to teach*.

**Related terms:** Evidence; Educational Hypothesis; Teaching Intention; Misconception; Educational Priority; Tutor loop.

**Notes:** Provisional and revisable. Authoritative model: [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md).

---

### Educational Claim

**Definition:** Any assertion about what a student knows, understands, can do, retains, transfers, or has mastered.

**Related terms:** Evidence; Uncertainty; Mastery.

**Notes:** Claims require evidential warrant (Invariant I9).

---

### Educational Success

**Definition:** Honest, evidence-based advancement of capacity across learning dimensions toward exam-credible readiness — not the closing of tasks.

**Related terms:** Learning; Mastery; Learning dimensions.

**Notes:** Defined fully in the Learning Model.

---

### Educational Hypothesis

**Definition:** The tutor’s current, revisable explanation for *why* the student is experiencing a diagnosed educational difficulty.

**Related terms:** Educational Diagnosis; Teaching Intention; Evidence; Tutor loop.

**Notes:** Hypotheses are testable by teaching; competing hypotheses are lawful. Authoritative model: [`EDUCATIONAL_HYPOTHESIS_MODEL.md`](EDUCATIONAL_HYPOTHESIS_MODEL.md).

---

### Educational Priority

**Definition:** The reasoned selection of which diagnosed educational problem — and therefore which Teaching Intention — should govern the next Learning Episode when multiple lawful needs compete.

**Related terms:** Educational Diagnosis; Teaching Intention; Educational Reasoning Loop.

**Notes:** Priority orders needs; it does not invent them. Authoritative model: [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md).

---

### Educational Reasoning Loop

**Definition:** The permanent Version 2 tutor reasoning architecture: Observe → Interpret Evidence → Diagnosis → Hypothesis → Teaching Intention → Teaching Strategy → Learning Episode → Evidence → Reflection → Twin Update → Repeat.

**Related terms:** Tutor loop; Learning Episode Lifecycle; Educational Diagnosis; Teaching Intention.

**Notes:** Specialises the Tutor Model loop. Authoritative model: [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md).

---

### Educational Atomicity

**Definition:** The requirement that every Learning Episode improve one educational capability — one deliberate, nameable improvement — not a chapter, subject, or unrelated bundle.

**Related terms:** Learning Episode; Teaching Goal; Learning Objective.

**Notes:** Foundational doctrine in [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md); invariant E11.

---

### Episode (Learning Episode)

**Definition:** A bounded educational engagement with exactly one deliberate educational purpose — to produce one intentional capability improvement relative to a learning objective — during which teaching, practice, observation, and reflection occur.

**Related terms:** Learning Objective; Tutor; Evidence; Reflection; Educational Atomicity; Teaching Strategy.

**Notes:** Must improve at least one learning dimension (Invariant I1) and exactly one educational purpose (E1). Educational concept — not a UI screen, activity widget, database row, or mastery certificate. See [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md).

---

### Evidence

**Definition:** An observed educational happening that may lawfully support or weaken educational claims.

**Related terms:** Inference; Reflection; Assessment; Mastery.

**Notes:** Inference interprets evidence; it must not invent evidence (Invariant I10).

---

### Explanation (understanding level)

**Definition:** The level at which the student can say what a concept means and how its parts relate, preferably in their own words.

**Related terms:** Understanding levels; Recognition; Conceptual Understanding.

**Notes:** Verbal explanation without application remains incomplete for exam preparation.

---

### False Indicator

**Definition:** A signal that commonly looks like understanding or mastery but does not warrant that claim when used alone (e.g., single correct answer, speed, confidence, coverage).

**Related terms:** Understanding; Evidence; Mastery.

**Notes:** Catalogued in the Understanding Model.

---

### Inference

**Definition:** Educational interpretation drawn from evidence about a student’s state.

**Related terms:** Evidence; Educational Diagnosis; Estimate.

**Notes:** Must remain distinguishable from raw evidence.

---

### Knowledge (estimated)

**Definition:** Provisional estimate of how well the student currently understands a syllabus element.

**Related terms:** Understanding; Competence; Mastery; Study Progress.

**Notes:** Constitutional estimate — not a student self-certificate.

---

### Knowledge Retention

**Definition:** Persistence of understanding and skill over time after acquisition.

**Related terms:** Retention (learning dimension); Mastery; Spaced practice.

**Notes:** Retention claims need delayed evidence (Invariant I13).

---

### Learning

**Definition:** Durable, evidence-supported change in capacity across understanding, application, connection, retention, and transfer relative to curriculum aims.

**Related terms:** Learning dimensions; Learning Episode; Educational Success.

**Notes:** Not identical to time spent, completion, or engagement.

---

### Learning Dimensions

**Definition:** The five analytic facets of learning in Kwalitec: Understanding, Application, Connection, Retention, Transfer.

**Related terms:** Learning Model; Mastery; Teaching Strategy.

**Notes:** Journeys should attend to all five over time; each episode needs at least one.

---

### Learning Objective

**Definition:** A precise statement of what the student should know, explain, or do regarding a curriculum element.

**Related terms:** Curriculum; Episode; Assessment; Mastery.

**Notes:** “Chapter 4” is not an objective; “compute EPV of a term assurance under stated bases” can be.

---

### Mastery

**Definition:** Estimated lasting, exam-credible command of a curriculum element — understanding plus reliable application, retention over time, and transfer — never proved by completion or single success.

**Related terms:** Competence; Knowledge; Evidence; Learning dimensions.

**Notes:** Strong language is earned and provisional (Invariant I20, I2).

---

### Misconception

**Definition:** A stable incorrect mental model that systematically produces wrong reasoning; distinct from slips or mere gaps.

**Related terms:** Educational Diagnosis; Teaching Strategy; Understanding.

**Notes:** Must be addressed explicitly (Invariant I6).

---

### Observation

**Definition:** The tutor-loop stage of collecting new evidence after teaching and student activity.

**Related terms:** Evidence; Tutor loop; Interpretation.

**Notes:** Delivery of teaching is not observation of learning.

---

### Procedural Fluency

**Definition:** Accurate, appropriately efficient execution of legitimate methods, with awareness of when procedures apply.

**Related terms:** Application; Conceptual Understanding; Transfer.

**Notes:** Fluency without concept is brittle; concept without fluency is incomplete for timed exams.

---

### Recognition (understanding level)

**Definition:** The ability to identify familiar terms, symbols, and standard problem types.

**Related terms:** Understanding levels; False Indicator.

**Notes:** Floor of familiarity — not strong understanding.

---

### Recommendation

**Definition:** A proposed next educational action for the student.

**Related terms:** Adaptation; Educational Justification; Tutor.

**Notes:** Must carry educational justification (Invariant I5).

---

### Reflection

**Definition:** Structured student consideration of difficulty, understanding, and uncertainty after educational work; produces soft evidence and must influence future teaching.

**Related terms:** Evidence; Tutor loop; Adaptation.

**Notes:** Invariant I4 — reflection with consequence.

---

### Retention (learning dimension)

**Definition:** Persistence of capacity across time, including after gaps between study occasions.

**Related terms:** Knowledge Retention; Mastery; Spaced practice.

**Notes:** Same as Knowledge Retention in substance; named as a learning dimension in the Learning Model.

---

### Study Progress

**Definition:** Record of what the student has marked or earned as studied for a syllabus unit; answers coverage.

**Related terms:** Coverage; Knowledge; Mastery.

**Notes:** Must never be presented as mastery.

---

### Teaching

**Definition:** Intentional instructional action that moves a student from a diagnosed state toward a learning objective.

**Related terms:** Teaching Intention; Teaching Strategy; Tutor; Learning Episode.

**Notes:** Content delivery without diagnosis is not teaching in the EDM sense.

---

### Teaching Intention

**Definition:** The deliberate educational change the tutor seeks to produce through the next Learning Episode (for example repair misconception, strengthen prerequisite, improve transfer).

**Related terms:** Educational Diagnosis; Educational Hypothesis; Teaching Goal; Teaching Strategy; Learning Episode.

**Notes:** One primary intention per episode. Teaching Goal is the atomic episode statement of an intention. Authoritative model: [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md).

---

### Teaching Others (understanding level)

**Definition:** The level at which the student can structure an explanation so another learner could begin to understand and apply the idea.

**Related terms:** Understanding levels; Analysis; Conceptual Understanding.

**Notes:** May be elicited via “explain as if teaching” in solo study contexts.

---

### Teaching Strategy

**Definition:** A chosen instructional approach that serves a Teaching Intention for a diagnosed need (e.g., conceptual contrast, worked-example fading, interleaved practice, spaced retrieval, error analysis).

**Related terms:** Teaching Intention; Educational Diagnosis; Teaching; Learning Episode.

**Notes:** Strategies answer *how*; diagnosis answers *what problem*; intention answers *what change*. Different deficits require different strategies.

---

### Transfer

**Definition:** Ability to apply knowledge under legitimate novelty and surface variation within syllabus scope.

**Related terms:** Learning dimensions; Understanding; Mastery; Application.

**Notes:** Transfer claims require variation (Invariant I14).

---

### Tutor

**Definition:** Educational agent obligated to diagnose, teach, observe, interpret, and adapt continuously in service of the student’s learning.

**Related terms:** Tutor loop; Teaching; Educational Diagnosis; Recommendation.

**Notes:** Distinct from planner, question bank, and search engine (Tutor Model).

---

### Tutor Loop

**Definition:** The continuous cycle Diagnose → Teach → Observe → Interpret → Adapt.

**Related terms:** Tutor; Educational Reasoning Loop; Evidence; Reflection; Recommendation.

**Notes:** Core behavioural definition of tutoring in Kwalitec. Expanded reasoning architecture: [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md).

---

### Uncertainty

**Definition:** Honest expression that evidential warrant is thin, conflicting, or stale.

**Related terms:** Educational Claim; Evidence; Mastery.

**Notes:** Must be namable in communication (Invariant I17).

---

### Understanding

**Definition:** Explanatory, relational, conditional grasp of curriculum ideas — inferred from converging evidence, not proved by correct answers alone.

**Related terms:** Conceptual Understanding; Understanding levels; Learning dimensions; Evidence.

**Notes:** Central doctrine of the Understanding Model.

---

### Understanding Levels

**Definition:** Progressive ladder: Recognition → Explanation → Application → Analysis → Teaching Others.

**Related terms:** Understanding; False Indicator; Evidence.

**Notes:** Higher levels are not automatic rewards for completing lower tasks.

---

## 3. Forbidden Synonym Collapses

The following collapses are educationally unlawful in Kwalitec language:

| Do not use… | To mean… |
|-------------|----------|
| Completed / Done | Mastered |
| Studied | Understood |
| Confident | Ready in the mastery sense |
| Practised | Transferred |
| Time spent | Learned |
| Recommended | Observed as needed without justification |
| Explained to student | Learned by student |
| Score | Understanding |

---

## 4. Maintenance

1. New educational terms used repeatedly in Version 2 documentation should gain a glossary entry.  
2. Definitions here must stay consistent with the Domain Model; on conflict, amend deliberately.  
3. Student-facing microcopy may simplify wording but must not violate Forbidden Synonym Collapses.

---

## 5. Related Documents

- [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  
- [`LEARNING_MODEL.md`](LEARNING_MODEL.md)  
- [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md)  
- [`TUTOR_MODEL.md`](TUTOR_MODEL.md)  
- [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md)  
- [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md)  
- [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md)  
- [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)  
