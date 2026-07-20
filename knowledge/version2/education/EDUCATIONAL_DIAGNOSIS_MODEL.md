# Educational Diagnosis Model

**Document ID:** V2-ERM-001  
**Classification:** Educational Architecture — Reasoning Foundation  
**Status:** Authoritative model of educational diagnosis  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  
**Companions:** [`EDUCATIONAL_HYPOTHESIS_MODEL.md`](EDUCATIONAL_HYPOTHESIS_MODEL.md) · [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md) · [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md) · [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md) · [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md)

---

## 1. Purpose

This document defines **Educational Diagnosis** for Kwalitec Version 2.

It answers four governing questions:

1. What is an educational diagnosis?  
2. What does diagnosis decide — and what must it refuse to decide?  
3. What categories of educational deficiency may lawfully be named?  
4. How does diagnosis relate to evidence, hypotheses, intentions, strategies, and episodes?

Educational Diagnosis is the permanent first interpretive act of tutoring: naming the educational problem that currently exists before any teaching move is chosen.

This is educational architecture. It is not an algorithm, scoring system, prompt library, database schema, or API contract.

---

## 2. Definition

**Educational Diagnosis:** the reasoned identification of the student’s current educational problem — what is deficient, distorted, fragile, missing, or miscalibrated relative to curriculum-grounded learning objectives — grounded in available evidence and stated with honest uncertainty.

A diagnosis answers:

> *What educational problem currently exists?*

A diagnosis does **not** answer:

> *How should we teach right now?*

That second question belongs to Teaching Intention and Teaching Strategy, which follow diagnosis (and, where useful, Educational Hypothesis).

---

## 3. Purpose of Diagnosis

Diagnosis exists so that teaching is contingent on the student’s actual educational state rather than on calendar position, content volume, or undifferentiated next-chapter logic.

Without diagnosis:

- teaching becomes broadcasting;  
- practice volume can reinforce wrong models;  
- recommendations lack educational justification;  
- Learning Episodes lose a lawful reason to exist.

With diagnosis:

- the tutor can name need in educational language;  
- competing needs can be prioritised;  
- hypotheses about *why* the need exists become possible;  
- teaching intentions become purposeful rather than opportunistic.

---

## 4. Governing Separation

```text
Educational Diagnosis  →  WHAT problem exists
Educational Hypothesis →  WHY the problem likely exists
Teaching Intention     →  WHAT change the next episode should achieve
Teaching Strategy      →  HOW instruction should pursue that change
Learning Episode       →  the bounded realisation of strategy + intention
```

**Governing sentence:** Diagnosis decides *what educational problem currently exists*. Diagnosis does not decide *how to teach*.

This specialises — and where necessary clarifies — the Domain Model’s statement that diagnosis precedes teaching strategy. Diagnosis constrains strategy by naming the deficit class; it does not itself select the instructional method.

---

## 5. Inputs

Lawful inputs to Educational Diagnosis include:

| Input | Role |
|-------|------|
| **Evidence** | Observed educational happenings (attempts, explanations, classifications, delayed performance, patterned errors) |
| **Reflection** | Soft metacognitive signal: felt difficulty, uncertainty, overconfidence, confusion maps |
| **Prior diagnoses** | Continuity of named needs across episodes (revisable, not sacred) |
| **Prior hypotheses** | Explanations previously held; useful context, never substitute for fresh evidence |
| **Student Digital Twin estimates** | Provisional learner-state belief and uncertainty — *context for interpretation*, never invented evidence |
| **Learning Objectives** | Curriculum-grounded aims against which deficiency is judged |
| **Curriculum position** | Syllabus sequence, prerequisites, legitimate exam demand |
| **Journey / session constraints** | Time, exam proximity, and lawful pacing — may constrain *priority*, not invent *need* |

Unlawful inputs:

- engagement metrics as proof of need;  
- completion status as proof of understanding or deficiency;  
- confidence alone as decisive diagnosis;  
- fabricated observations;  
- marketing urgency disguised as educational urgency.

---

## 6. Outputs

A complete Educational Diagnosis yields:

1. **Primary deficiency category** — the named class of educational problem (see §8).  
2. **Affected learning objective(s)** — curriculum-grounded aims implicated.  
3. **Primary learning dimension implicated** — Understanding, Application, Connection, Retention, and/or Transfer.  
4. **Scope statement** — what is wrong *here*, not a vague “student is weak.”  
5. **Evidential warrant** — which observations support the diagnosis, and how strong they are.  
6. **Uncertainty statement** — what remains thin, conflicting, or provisional.  
7. **Secondary deficiencies (optional)** — co-present problems noted but not primary for the next move.  
8. **Non-claims** — what the diagnosis explicitly does *not* assert (for example: “not a fluency deficit,” “not proven misconception”).

Diagnosis outputs do **not** include:

- a chosen Teaching Strategy;  
- a chosen Learning Episode type;  
- a mastery certificate;  
- a numerical “severity score” as educational law (priority is a separate reasoning act).

---

## 7. Relationships

### 7.1 Evidence

Evidence is the observational ground of diagnosis. Diagnosis interprets evidence; it may not invent evidence. Thin evidence yields provisional diagnosis or lawful diagnostic probing — not confident labelling.

### 7.2 Reflection

Reflection is soft evidence. It can surface false confidence, low confidence, felt fragmentation, or metacognitive fog. It never alone proves conceptual misunderstanding or mastery. When reflection contradicts performance, diagnosis must name the conflict rather than silently preferring one source.

### 7.3 Learning Episodes

Diagnosis precedes episode selection. Episodes exist to address a diagnosed need (or a lawful cold-start introduction under curriculum sequencing). Episode outcomes generate new evidence that may confirm, revise, or replace the diagnosis.

### 7.4 Digital Twin

The Student Digital Twin holds provisional estimates of learner state. Diagnosis may consult Twin estimates as interpretive context. Diagnosis and Twin update remain distinct acts: diagnosis names current educational problem for teaching; Twin update revises standing belief after evidence and reflection are interpreted. Episodes and diagnoses supply inputs to the Twin; they do not overwrite Twin authority by administrative fiat.

### 7.5 Teaching Strategy

Teaching Strategy answers *how* to instruct. Diagnosis supplies the deficit class that strategies must fit. Selecting strategy without diagnosis is broadcasting. Selecting strategy *as if it were* diagnosis collapses the reasoning loop.

### 7.6 Learning Objectives

Deficiencies are meaningful only relative to objectives. “The student struggles” is incomplete. “Relative to the objective *explain select vs ultimate and compute from a select table*, the student holds a misconception about select period” is a diagnosis.

### 7.7 Educational Hypothesis and Teaching Intention

Diagnosis states the problem. Hypothesis proposes why. Intention states the educational change sought next. All three are required for mature tutoring; none replaces the others.

---

## 8. Categories of Educational Deficiency

The catalogue below is the authoritative deficiency vocabulary for Educational Diagnosis. Categories may co-occur. When they do, prioritisation follows [`EDUCATIONAL_PRIORITY_MODEL.md`](EDUCATIONAL_PRIORITY_MODEL.md).

Each category includes: Definition · Observable evidence · Typical causes · Educational consequences · Priority considerations.

---

### 8.1 Conceptual Misunderstanding

**Definition**  
The student lacks adequate grasp of meanings, principles, relationships, or conditions of validity. Distinct from a stable wrong model (misconception): here the structure is thin, confused, or incomplete rather than systematically false.

**Observable evidence**  
Fragile or empty explanations; inability to state conditions of use; correct answers without justification; collapse when “why” or “what if” is asked; confusion among near concepts without a patterned wrong belief.

**Typical causes**  
Rushed introduction; formula-first study; teaching that presented procedures without principles; insufficient contrast with neighbouring ideas.

**Educational consequences**  
Brittle application; false readiness after recognition success; inability to recover when stems change.

**Priority considerations**  
Usually precedes fluency and exam-technique work on the same objective. Often yields to Concept Deepening or Concept Introduction before Independent Practice.

---

### 8.2 Procedural Weakness

**Definition**  
The student understands (adequately for the current aim) what to do in principle, but cannot execute the legitimate method accurately or with appropriate efficiency.

**Observable evidence**  
Correct method choice with execution errors; slow or stalled multi-step work; arithmetic or table-lookup fragility; success on conceptual probes with failure on computation.

**Typical causes**  
Insufficient guided practice; skipped worked-example fading; anxiety under steps; weak intermediate skills (algebra, table reading) without conceptual absence.

**Educational consequences**  
Timed-exam failure despite “knowing the idea”; loss of confidence; avoidance of calculation-heavy topics.

**Priority considerations**  
Legitimate only when conceptual misunderstanding and misconception are not the better explanation. Do not drill procedures on top of a wrong model.

---

### 8.3 Weak Retention

**Definition**  
Capacity that once appeared present has faded after a meaningful interval; the student cannot reliably retrieve or apply what earlier evidence suggested was acquired.

**Observable evidence**  
Success soon after teaching followed by failure after delay; “I used to know this”; spaced probe collapse; re-learning from near-scratch on previously covered objectives.

**Typical causes**  
Massed practice without spacing; coverage-driven journeys; absence of retrieval episodes; long calendar gaps in actuarial programmes.

**Educational consequences**  
False exam readiness based on peak performance; last-minute panic; wasted earlier study.

**Priority considerations**  
Rises near exam windows and after long gaps. Must not be confused with never-having-learned. Retention repair differs from first teaching.

---

### 8.4 Knowledge Fragmentation

**Definition**  
The student holds locally coherent pieces that are not integrated: ideas, methods, or syllabus parts remain isolated rather than connected into usable structure.

**Observable evidence**  
Success inside one example family and failure when topics combine; inability to relate neighbouring objectives; contradictory treatments across contexts; “I know each bit separately.”

**Typical causes**  
Topic-silo study; absence of connection-focused episodes; teaching that never asked for structure across chapters.

**Educational consequences**  
Failure on combination questions; weak transfer; inability to choose methods from principle across a paper.

**Priority considerations**  
Often secondary until local conceptual clarity exists; becomes primary when exams demand synthesis and local pieces are already adequate.

---

### 8.5 Prerequisite Gap

**Definition**  
The student lacks an earlier curriculum capability required for legitimate progress on the current objective.

**Observable evidence**  
Repeated failure traceable to an upstream skill; success when the prerequisite is scaffolded; diagnosis that relocates the true deficit earlier in the syllabus graph.

**Typical causes**  
Skipped foundations; weak school mathematics; rushed journey sequencing; pretending coverage implies readiness.

**Educational consequences**  
Theatre of struggle on advanced topics; demoralisation; compounding gaps.

**Priority considerations**  
Generally highest educational priority when the gap blocks the current aim. Repair prerequisites before extension (see Priority Model).

---

### 8.6 Misconception

**Definition**  
A stable, incorrect mental model that systematically produces wrong reasoning. Distinct from slips, calculation noise, or mere ignorance: the student treats a wrong structure as true.

**Observable evidence**  
Patterned errors across items; confident wrong explanations; resistance to mere re-telling of the correct rule; discrimination failures on contrastive cases.

**Typical causes**  
Overgeneralisation from early examples; ambiguous teaching; analogy taken too far; unaddressed near-miss concepts.

**Educational consequences**  
Practice strengthens the wrong model; transfer collapses; mastery is blocked until repair is explicit.

**Priority considerations**  
High. Misconceptions must be addressed explicitly before undifferentiated practice on the same objective.

---

### 8.7 Low Confidence

**Definition**  
The student’s self-appraisal of capacity is materially below what evidence supports; affective under-estimation impairs engagement or exam performance.

**Observable evidence**  
Adequate or strong performance with self-reports of unreadiness; avoidance despite success; excessive checking; reflection that undervalues demonstrated capacity.

**Typical causes**  
Prior failure narratives; perfectionism; comparison with peers; punitive assessment history; incomplete feedback that only names errors.

**Educational consequences**  
Under-practice of transferable strengths; exam underperformance from anxiety; requests for unnecessary re-teaching.

**Priority considerations**  
Important but must not displace dangerous misconceptions or prerequisite gaps. Recovery episodes are lawful when evidence contradicts felt unreadiness.

---

### 8.8 False Confidence

**Definition**  
The student’s self-appraisal of capacity materially exceeds what evidence supports — especially dangerous before examinations.

**Observable evidence**  
High confidence with weak performance under variation; coverage treated as mastery; rejection of diagnostic challenge; reflection that claims readiness without delayed or transfer evidence.

**Typical causes**  
Recognition mistaken for understanding; success on clones; completion dashboards; social comparison; tutor or product language that overpraises.

**Educational consequences**  
Dangerous exam failure; refusal of needed repair; wasted late calendar on the wrong topics.

**Priority considerations**  
High when exam proximity and overconfidence co-occur. Addressing false confidence is protective of long-term outcomes and trust.

---

### 8.9 Exam Technique Weakness

**Definition**  
The student has adequate underlying knowledge for the aim, but fails to deploy it under examination conditions: timing, question selection, presentation, reading discipline, or mark-aware strategy.

**Observable evidence**  
Untimed success with timed collapse; incomplete answers despite knowing more; poor allocation of time; misreading stems; strong concept probes with weak paper simulation.

**Typical causes**  
Insufficient exam-condition practice; perfectionism on early questions; unfamiliarity with paper structure; anxiety-specific behaviours.

**Educational consequences**  
Marks lost despite capacity; misleading diagnosis of conceptual failure when the true deficit is deployment under constraint.

**Priority considerations**  
Legitimate only after conceptual and major misconception issues are not the better explanation. Supports exam readiness without replacing conceptual work.

---

### 8.10 Application Weakness

**Definition**  
The student cannot reliably use knowledge to perform legitimate syllabus tasks (calculate, classify, derive, decide), even when some recognition or partial explanation is present.

**Observable evidence**  
Failure to start valid methods; incorrect method selection; incomplete solutions; success on recognition quizzes with failure on “do the task” items.

**Typical causes**  
Teaching that stopped at explanation; insufficient guided then independent practice; fear of calculation; unclear objective criteria.

**Educational consequences**  
Exam papers punish pure verbal familiarity; competence remains theoretical.

**Priority considerations**  
Distinguish from procedural weakness (execution after method choice) and from conceptual misunderstanding (no valid method available). Often follows conceptual repair.

---

### 8.11 Transfer Weakness

**Definition**  
The student succeeds on practised surface forms but fails when legitimate variation, novelty, or rewording appears within syllabus scope.

**Observable evidence**  
Clone success, variant failure; keyword dependence; collapse when parameters, timing, or wording shift; inability to map new stems to known structure.

**Typical causes**  
Narrow practice sets; teaching locked to templates; absence of Transfer / Exam Application episodes; misconception that surfaces only under variation.

**Educational consequences**  
False readiness for professional examinations; brittle competence; surprise failure on “unfair” papers that are actually syllabus-valid.

**Priority considerations**  
Critical for exam credibility once local application exists. Prefer foundational understanding before speeded transfer theatre.

---

### 8.12 Incomplete Understanding

**Definition**  
The student has partial, patchy grasp: some facets of an objective are present while necessary facets (conditions of validity, boundary cases, related principles) remain missing. Related to conceptual misunderstanding, but emphasises *partial acquisition* rather than global thinness or a single wrong model.

**Observable evidence**  
Correct work in a subset of cases; failure on boundary or assumption-change probes; explanations that omit critical constraints; “I get it except when…”

**Typical causes**  
Teaching that covered the central case only; early exit from Concept Deepening; objectives that were too coarse.

**Educational consequences**  
Intermittent success that feels like “careless mistakes”; blocked mastery; fragile transfer at boundaries.

**Priority considerations**  
Often addressed by Concept Deepening targeting the missing facet — not by more identical practice of the already-known facet.

---

## 9. Diagnostic Discipline

1. **Name the category** in educational language.  
2. **Anchor to an objective** — deficiency without aim is fog.  
3. **Cite warrant** — what evidence supports this reading.  
4. **Separate observation from interpretation.**  
5. **Prefer the most specific lawful category** that fits (misconception over generic “weak,” prerequisite gap over mysterious advanced failure).  
6. **Admit competition** — when categories compete, hold multiple provisional diagnoses and use hypothesis testing via teaching.  
7. **Remain revisable** — new evidence outranks loyalty to a prior label.  
8. **Refuse how-to smuggling** — do not encode a teaching strategy inside the diagnosis statement.

---

## 10. Actuarial Illustrations

| Observation pattern | Likely diagnosis (provisional) |
|---------------------|--------------------------------|
| Patterned errors treating ultimate mortality as applying from age 0 despite select tables | Misconception |
| Can explain equivalence principle but fails multi-step net premium calculations | Procedural weakness |
| Strong on annuities last month; blank after six weeks | Weak retention |
| Handles prospective and retrospective reserves separately; fails when asked to relate them | Knowledge fragmentation |
| Fails GLM questions because exponential-family basics are absent | Prerequisite gap |
| High confidence after completing a chapter; fails first varied exam stem | False confidence |
| Untimed reserves correct; timed paper unfinished | Exam technique weakness |

---

## 11. Summary Propositions

1. Educational Diagnosis names the current educational problem; it does not choose how to teach.  
2. Diagnosis is evidence-grounded, objective-relative, and revisable.  
3. Twelve deficiency categories form the authoritative vocabulary for Version 2 reasoning.  
4. Diagnosis constrains — but does not select — Teaching Strategy and Learning Episode.  
5. Twin estimates inform diagnosis; they do not replace evidence.  
6. Mature tutoring proceeds: Diagnosis → Hypothesis → Intention → Strategy → Episode.
