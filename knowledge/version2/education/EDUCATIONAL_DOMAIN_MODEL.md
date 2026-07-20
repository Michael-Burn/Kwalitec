# Educational Domain Model

**Document ID:** V2-EDM-001  
**Classification:** Educational Domain Foundation  
**Status:** Authoritative educational vocabulary  
**Nature:** Documentation only — no runtime behaviour  
**Audience:** Product, educational governance, architecture, future implementers  

**Authority relationships**

| Document | Relationship |
|----------|--------------|
| [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) | Highest educational law; this Domain Model specialises vocabulary under it |
| [`LEARNING_MODEL.md`](LEARNING_MODEL.md) | Deepens the concept of Learning |
| [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md) | Deepens the concept of Understanding |
| [`TUTOR_MODEL.md`](TUTOR_MODEL.md) | Deepens the concept of Tutor |
| [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) | Binding rules derived from these concepts |
| [`EDUCATIONAL_GLOSSARY.md`](EDUCATIONAL_GLOSSARY.md) | Alphabetical vocabulary companion |

---

## 1. Purpose

This document defines the **Educational Domain Model (EDM)** for Kwalitec: the permanent set of educational concepts upon which all future educational design and implementation must rest.

The EDM is Kwalitec’s educational **ubiquitous language**. When product, pedagogy, and engineering speak of *learning*, *mastery*, *evidence*, or *tutor*, they must mean what this document defines — not colloquial substitutes, marketing shorthand, or accidental synonyms.

This model is intentionally technology-independent. It remains valid if the platform is rebuilt, rehosted, or reimplemented. It describes education, not software.

---

## 2. Educational Stance

Kwalitec prepares candidates for demanding professional examinations — especially actuarial and related quantitative disciplines — where syllabus volume is large, daily time is scarce, and false confidence is costly.

Under that stance:

1. **Learning is multi-dimensional.** Correct recall is necessary but never sufficient.
2. **Understanding is inferred, never declared into existence.**
3. **Teaching is purposeful intervention**, not mere content delivery.
4. **Evidence precedes educational claim.**
5. **Mastery is durable, exam-credible command** — estimated from accumulated evidence, never equated with completion.

These beliefs are consistent with the Educational Constitution. Where terminology here introduces new named concepts (for example *Learning Episode* or *Educational Diagnosis*), they specialise constitutional meaning; they do not replace it.

---

## 3. Concept Catalogue

Each concept below is defined with:

- **Definition** — precise meaning inside Kwalitec  
- **Purpose** — why the concept exists in the domain  
- **Why it matters** — educational risk if ignored  
- **Relationship to other concepts** — how it connects in the model  
- **Examples from actuarial education** — concrete syllabus-grounded illustrations  

---

### 3.1 Learning

**Definition**  
Learning is a durable, evidence-supported change in a student’s capacity to understand, apply, connect, retain, and transfer curriculum knowledge. Learning is not the mere expenditure of study time, the marking of a topic as done, or a single correct answer.

**Purpose**  
To name the educational outcome Kwalitec exists to produce — as distinct from coverage, completion, or engagement.

**Why it matters**  
Without a rigorous definition of learning, platforms reward activity that feels productive while leaving candidates unready for unseen exam conditions. Professional examinations punish shallow familiarity.

**Relationship to other concepts**  
Learning is the overarching process. It is realised through *Learning Episodes*, guided by *Teaching*, informed by *Evidence* and *Reflection*, aimed at *Learning Objectives*, and evaluated against dimensions of *Understanding*, *Procedural Fluency*, *Knowledge Retention*, and *Transfer*. *Mastery* is a high bar of learning durability, not a synonym for learning itself.

**Examples from actuarial education**  
A candidate who works through a chapter on survival models and can later derive a force of mortality from first principles under timed conditions has learned. A candidate who highlights the same chapter and marks it complete has covered material; that alone is not learning.

---

### 3.2 Understanding

**Definition**  
Understanding is the student’s ability to explain, relate, and reason with a concept — not merely to recognise it or reproduce a memorised procedure. Genuine understanding supports explanation in the student’s own words, correct use under variation, and detection of when a method does or does not apply.

**Purpose**  
To separate conceptual grasp from surface performance.

**Why it matters**  
Actuarial papers routinely rephrase familiar ideas. Recognition of a formula without knowing when it is valid produces brittle performance and false readiness.

**Relationship to other concepts**  
Understanding is one primary dimension of *Learning* and the core concern of the *Understanding Model*. It is supported by *Conceptual Understanding*, evidenced through multiple *Evidence* sources, threatened by *Misconceptions*, and deepened through *Teaching* and *Reflection*. Correct answers are weak evidence of understanding unless accompanied by explanation, transfer, or diagnostic probes.

**Examples from actuarial education**  
A student who can state the formula for net premium but cannot explain why the equivalence principle is used, or when gross premium differs, has recognition without understanding.

---

### 3.3 Teaching

**Definition**  
Teaching is intentional instructional action that helps a student move from a diagnosed educational state toward a clearer *Learning Objective*. Teaching selects explanations, examples, contrasts, practice forms, and scaffolds according to need — it is not the undifferentiated presentation of content.

**Purpose**  
To define the active educational intervention that a *Tutor* performs.

**Why it matters**  
Content without teaching leaves the student alone with textbooks. Teaching without diagnosis becomes noise. Professional preparation requires targeted intervention where evidence shows the student is stuck, shallow, or misconceiving.

**Relationship to other concepts**  
Teaching follows *Educational Diagnosis*, employs a *Teaching Strategy*, targets one or more *Learning Objectives*, and produces new *Evidence* for observation. Teaching precedes assessment of the taught material within a coherent episode. *Reflection* after teaching informs the next teaching move.

**Examples from actuarial education**  
After diagnosing that a student confuses contingent and deferred annuities, teaching contrasts cash-flow timelines side by side, then asks the student to classify novel wordings — rather than assigning another undifferentiated problem set.

---

### 3.4 Tutor

**Definition**  
A Tutor is an educational agent whose standing obligation is to diagnose need, teach purposefully, observe outcomes, interpret evidence, and adapt the next educational move. In Kwalitec, the product itself accepts this obligation: it behaves as a tutor, not merely as a planner, repository, or search surface.

**Purpose**  
To fix the product’s educational identity and duties.

**Why it matters**  
Many study tools schedule work or supply questions. Few accept continuous responsibility for the student’s educational state. Without the tutor identity, recommendations drift toward convenience and engagement rather than learning.

**Relationship to other concepts**  
The Tutor executes the continuous loop of Diagnose → Teach → Observe → Interpret → Adapt (see [`TUTOR_MODEL.md`](TUTOR_MODEL.md)). It uses *Educational Diagnosis*, *Teaching Strategy*, *Evidence*, and *Reflection*. It never confuses *Learning Episode* completion with *Mastery*.

**Examples from actuarial education**  
A tutor notices repeated errors on “select and ultimate” mortality tables, teaches the select-period concept explicitly, then observes whether the student can interpret a new select table without prompting — adapting if the misconception persists.

---

### 3.5 Learning Episode

**Definition**  
A Learning Episode is a bounded educational engagement with **exactly one deliberate educational purpose** — to produce **one** intentional improvement in the student’s educational capability relative to a curriculum-grounded *Learning Objective* — during which teaching, practice, observation, and reflection occur under a *Teaching Strategy*. An episode produces evidence; it is not a calendar block, checklist item, UI screen, or mastery certificate.

**Purpose**  
To name the fundamental educational unit from which every tutoring interaction is composed.

**Why it matters**  
Without episodes as educational units, progress is narrated as time spent or tasks closed. Episodes force the question: *what single educational change was this engagement for?* See Educational Atomicity and the Learning Episode Architecture set.

**Relationship to other concepts**  
Episodes are guided by a *Tutor*, contain *Teaching*, generate *Evidence*, invite *Reflection*, and advance one primary dimension of *Learning*. Multiple episodes accumulate toward *Mastery*; no single episode proves it. Episodes align with, but are not identical to, product notions such as sessions or journey steps — the EDM concept is educational, not product-mechanical. Authoritative specialisation: [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md) · [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md).

**Examples from actuarial education**  
An episode whose purpose is “repair select-vs-ultimate confusion” may include contrastive teaching, discrimination probes, and reflection — one coherent educational unit. Introducing the concept, then practising lookups, then transferring to a new table are separate episodes (or a micro-sequence), not one fused purpose.

---

### 3.6 Evidence

**Definition**  
Evidence is an observed educational happening that may lawfully support or weaken claims about learning, understanding, fluency, retention, or mastery. Evidence is recorded history of what the student did, produced, or disclosed in educational context — not an inference, score, or marketing claim.

**Purpose**  
To ground every material educational assertion in observation.

**Why it matters**  
Claims of mastery without evidence are theatre. Inference may interpret evidence; inference must not invent it. Thin evidence requires honest uncertainty.

**Relationship to other concepts**  
Evidence arises from *Learning Episodes*, informs *Educational Diagnosis*, constrains *Mastery* estimates, and is enriched by *Reflection* (as soft signal) and assessed performance (as stronger signal). *Understanding* and *Transfer* require converging evidence from multiple sources. See also the platform’s broader Educational Evidence doctrine under the Constitution.

**Examples from actuarial education**  
Successful derivation of a prospective reserve formula on an unseen variant is strong evidence of understanding. Marking a reserves chapter complete is coverage evidence only. Saying “I feel confident” is soft reflective evidence, never sufficient alone for mastery.

---

### 3.7 Reflection

**Definition**  
Reflection is the student’s structured consideration of what was attempted, what was difficult, what seems understood, and what remains uncertain after educational work. Reflection produces soft educational evidence and shapes future teaching; it is not optional decoration.

**Purpose**  
To capture metacognitive signal and close the educational loop inside an episode.

**Why it matters**  
Without reflection, tutors see performance but not the student’s own map of confusion. Professional learners who never surface uncertainty tend to over-estimate readiness.

**Relationship to other concepts**  
Reflection follows teaching and practice within a *Learning Episode*, contributes *Evidence* (soft), influences subsequent *Educational Diagnosis* and *Teaching Strategy*, and must affect future teaching when material. Fabricated reflection is educationally void.

**Examples from actuarial education**  
After practising commutation-function calculations, a student reflects: “I can compute when formulae are given, but I freeze when asked which commutation functions apply.” That reflection correctly steers the next episode toward selection-of-method teaching, not more arithmetic drill alone.

---

### 3.8 Mastery

**Definition**  
Mastery is estimated, lasting, exam-credible command of a curriculum element: understanding plus reliable application, retention over time, and transfer to unfamiliar but syllabus-valid presentations. Mastery is never self-certified by completion, and never proved by a single success.

**Purpose**  
To name the high educational attainment students and the platform aspire to estimate honestly.

**Why it matters**  
Collapsing mastery with “studied” or “finished today’s work” is the central educational integrity failure in exam preparation products.

**Relationship to other concepts**  
Mastery sits above episodic success. It depends on accumulated *Evidence* across *Understanding*, *Procedural Fluency*, *Knowledge Retention*, and *Transfer*. *Misconceptions* unresolved block mastery. *Teaching* and *Reflection* contribute to the path; they do not confer mastery by themselves.

**Examples from actuarial education**  
A candidate who correctly prices a standard annuity today, again after two weeks without notes, and also under a reworded exam-style stem, shows mastery-consistent evidence. Completing a mission labelled “Annuities” does not.

---

### 3.9 Misconception

**Definition**  
A Misconception is a stable, incorrect mental model that systematically produces wrong reasoning or wrong answers in a domain. It differs from a slip, a calculation error, or a gap of ignorance: it is a wrong structure the student treats as true.

**Purpose**  
To identify educational obstacles that mere practice volume will not remove.

**Why it matters**  
Drilling on top of a misconception strengthens the wrong model. Explicit diagnosis and corrective teaching are required.

**Relationship to other concepts**  
Misconceptions are targets of *Educational Diagnosis* and *Teaching Strategy*. They distort *Understanding* and block *Transfer*. Evidence of repeated patterned error supports diagnosing a misconception rather than random noise. Addressing misconceptions must be explicit — not hoped for through more of the same.

**Examples from actuarial education**  
Believing that “ultimate mortality always applies from age 0” regardless of select period; treating “independent lives” as identical to “identical lives”; assuming continuous and discrete payment models are interchangeable without adjustment.

---

### 3.10 Educational Diagnosis

**Definition**  
Educational Diagnosis is the reasoned interpretation of available evidence to identify the student’s current educational need: what is understood, what is missing, what is misconceived, and which learning dimension should be advanced next.

**Purpose**  
To make teaching contingent on the student’s actual state rather than on a fixed content sequence alone.

**Why it matters**  
Teaching without diagnosis is broadcasting. Diagnosis without subsequent teaching is voyeurism. The tutor obligation binds them.

**Relationship to other concepts**  
Diagnosis uses *Evidence* and *Reflection*, identifies *Misconceptions* and gaps relative to *Learning Objectives*, and constrains subsequent *Teaching Intention* and *Teaching Strategy*. It precedes teaching of the diagnosed need. Diagnosis decides *what educational problem currently exists*; it does not by itself decide *how to teach*. Diagnosis is provisional and revisable as new evidence arrives. Authoritative specialisation: [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) · [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md).

**Examples from actuarial education**  
Patterned failures on “with-profits” valuation questions that vanish when surplus distribution is removed from the stem suggest a conceptual gap on bonus structures, not a general valuation deficit — diagnosis that changes what is taught next.

---

### 3.11 Teaching Strategy

**Definition**  
A Teaching Strategy is a chosen instructional approach for a diagnosed need — for example conceptual contrast, worked-example fading, interleaved practice, error analysis, or spaced retrieval — selected because it fits the diagnosis and the learning objective.

**Purpose**  
To connect diagnosis to concrete instructional action.

**Why it matters**  
Without named strategies, “teach more” remains vague. Different deficits (misconception vs forgetting vs lack of fluency) require different moves.

**Relationship to other concepts**  
Strategies implement *Teaching* after *Educational Diagnosis*, within a *Learning Episode*, aimed at *Learning Objectives* and specific learning dimensions. Outcomes become *Evidence* that may confirm or revise the diagnosis.

**Examples from actuarial education**  
For a fluency deficit on life-table look-ups: timed, varied retrieval practice. For a misconception on prospective vs retrospective reserves: contrastive examples with forced explanation. For retention fade: spaced revisiting of previously strong topics before an exam window.

---

### 3.12 Learning Objective

**Definition**  
A Learning Objective is a precise statement of what the student should be able to know, explain, or do with respect to a curriculum element. Objectives are educational aims; they are not topics themselves, not completion checkboxes, and not exam questions.

**Purpose**  
To give teaching and evidence a clear target.

**Why it matters**  
Vague aims (“study mortality”) produce vague episodes. Precise objectives (“explain select vs ultimate and compute a probability from a select table”) make diagnosis and success observable.

**Relationship to other concepts**  
Objectives orient *Learning Episodes*, *Teaching*, and *Assessment-worthy Evidence*. *Mastery* is estimated with respect to objectives (or coherent sets of them). Curriculum topics contain or imply objectives; the EDM treats the objective as the educational aim unit.

**Examples from actuarial education**  
“Given a constant force of mortality and a force of interest, derive and compute the EPV of a continuous whole life assurance” is an objective. “Chapter 4” is not.

---

### 3.13 Knowledge Retention

**Definition**  
Knowledge Retention is the persistence of understanding and skill over time after initial acquisition, including resistance to ordinary forgetting under realistic gaps between study occasions.

**Purpose**  
To recognise that professional examination success depends on what remains available weeks and months later, not only on end-of-chapter performance.

**Why it matters**  
Actuarial programmes span long calendars. Peak performance immediately after study is a false readiness signal if retention is ignored.

**Relationship to other concepts**  
Retention is a dimension of *Learning* and a necessary condition of *Mastery*. It is evidenced by successful performance after delay. *Teaching Strategies* such as spaced practice serve retention. *Reflection* may surface felt forgetting; delayed assessed performance is stronger evidence.

**Examples from actuarial education**  
Correctly computing net premiums in March and again in June without re-teaching from scratch indicates retention. Acing a same-day quiz after first exposure does not yet speak to retention.

---

### 3.14 Transfer

**Definition**  
Transfer is the ability to apply knowledge and skill in situations that differ in surface form from those practised — including novel wordings, altered parameters, combined topics, and exam-realistic constraints — while remaining within the syllabus’s legitimate demand.

**Purpose**  
To distinguish flexible competence from performance locked to familiar templates.

**Why it matters**  
Examiners redesign surface features. Students who only succeed on textbook clones fail under transfer demand.

**Relationship to other concepts**  
Transfer is a dimension of *Learning* and a strong indicator of genuine *Understanding* and approaching *Mastery*. It is evidenced when students succeed on varied, unseen-but-valid tasks. *Misconceptions* often reveal themselves when transfer is required.

**Examples from actuarial education**  
A student practised only “calculate āₓ at i = 4%” who can also interpret a word problem requiring the same annuity under a different payment timing has transferred. One who fails whenever the interest rate is not 4% has not.

---

### 3.15 Conceptual Understanding

**Definition**  
Conceptual Understanding is grasp of meanings, relationships, principles, and conditions of validity — the “what” and “why” — as distinct from the ability to execute steps.

**Purpose**  
To name the conceptual half of professional competence.

**Why it matters**  
Actuarial work and examinations reward knowing why a method applies. Pure procedural mimicry collapses when assumptions change.

**Relationship to other concepts**  
Conceptual Understanding is a facet of *Understanding*. It complements *Procedural Fluency*. Teaching often alternates concept and procedure. Evidence includes explanation, classification, and justification — not only numeric correctness.

**Examples from actuarial education**  
Explaining why the equivalence principle equates present values of premiums and benefits, and what breaks if expenses are introduced, demonstrates conceptual understanding beyond computing a number from a formula sheet.

---

### 3.16 Procedural Fluency

**Definition**  
Procedural Fluency is accurate, appropriately efficient execution of legitimate methods and calculations, with awareness of when a procedure applies. Fluency without concept is brittle; concept without fluency is incomplete for timed examinations.

**Purpose**  
To name the skilled-performance half of professional competence.

**Why it matters**  
Exams are timed. Candidates need both sound reasoning and reliable execution.

**Relationship to other concepts**  
Procedural Fluency pairs with *Conceptual Understanding* under *Learning*. It is advanced by practice-oriented *Teaching Strategies*, evidenced by accurate performance under reasonable time pressure, and insufficient alone for *Mastery* without understanding, retention, and transfer.

**Examples from actuarial education**  
Consistently correct computation of assurance and annuity factors from life tables under time constraint shows fluency. Speed with frequent sign or timing errors shows neither fluency nor understanding.

---

## 4. Concept Map (Narrative)

At the centre of the EDM is **Learning**, pursued toward **Learning Objectives**.

A **Tutor** conducts **Learning Episodes** in which **Teaching** (via a **Teaching Strategy**) addresses needs identified by **Educational Diagnosis**. Diagnosis interprets **Evidence**, including **Reflection**, and must confront **Misconceptions** explicitly when present.

Within learning, Kwalitec attends to **Understanding** (including **Conceptual Understanding**), **Procedural Fluency**, **Knowledge Retention**, and **Transfer**. **Mastery** is the durable convergence of these under accumulated evidence — never the aftermath of completion alone.

---

## 5. Separation Rules (Domain Hygiene)

The following pairs must never be collapsed in language or design:

| Do not equate… | With… |
|----------------|-------|
| Study coverage / completion | Understanding or mastery |
| A correct answer | Understanding |
| Time spent | Learning |
| Feeling confident | Mastery |
| One successful episode | Mastery |
| Content delivery | Teaching |
| A question bank | A tutor |
| A study plan | Educational diagnosis |

---

## 6. Governance

1. New educational features must map onto EDM concepts or propose a formal amendment to this model.  
2. Student-facing language should prefer EDM terms or plain equivalents that preserve meaning (see glossary).  
3. Conflict with the Educational Constitution is resolved in favour of the Constitution until this model or the Constitution is formally amended.  
4. Implementation choices never redefine these meanings by accident of storage, scoring, or interface convenience.

---

## 7. Related Documents

- [`LEARNING_MODEL.md`](LEARNING_MODEL.md)  
- [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md)  
- [`TUTOR_MODEL.md`](TUTOR_MODEL.md)  
- [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md)  
- [`EDUCATIONAL_GLOSSARY.md`](EDUCATIONAL_GLOSSARY.md)  
- [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md)  
- [`LEARNING_EPISODE_LIFECYCLE.md`](LEARNING_EPISODE_LIFECYCLE.md)  
- [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md)  
- [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md)  
- [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md)  
- [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md)  
- [`../EDUCATIONAL_PRINCIPLES.md`](../EDUCATIONAL_PRINCIPLES.md)  
- [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)  
- [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md)  
