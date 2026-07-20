# Subject Authoring Model

**Document ID:** V2-SAA-001  
**Classification:** Educational Architecture — Subject Authoring Foundation  
**Status:** Authoritative model of educational authoring  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Audience:** Product, educational governance, architecture, subject experts, curriculum designers, future implementers  

**Authority relationships**

| Document | Relationship |
|----------|--------------|
| [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md) | Defines *what* teachable knowledge is; this model defines *how experts author it* |
| [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) | Anatomy of a teachable concept — the primary authoring target |
| [`CONCEPT_DECOMPOSITION_MODEL.md`](CONCEPT_DECOMPOSITION_MODEL.md) | Syllabus-to-concept decomposition pipeline |
| [`MISCONCEPTION_AUTHORING_MODEL.md`](MISCONCEPTION_AUTHORING_MODEL.md) | How misconceptions are authored as repairable knowledge |
| [`REPRESENTATION_MODEL.md`](REPRESENTATION_MODEL.md) | Educational representations as authoring artefacts |
| [`APPLICATION_AND_TRANSFER_MODEL.md`](APPLICATION_AND_TRANSFER_MODEL.md) | Application and transfer contexts as authoring artefacts |
| [`AUTHORING_INVARIANTS.md`](AUTHORING_INVARIANTS.md) | Binding rules for lawful authoring |
| [`../CURRICULUM_MODEL.md`](../CURRICULUM_MODEL.md) | Syllabus packaging hierarchy; authoring fills knowledge under curriculum authority |
| [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md) | Strategies consume authored knowledge; they do not invent it |
| [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md) | Episodes enact teaching against authored objectives and concepts |
| [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md) | Parent educational vocabulary |

---

## 1. Purpose

This document defines **Subject Authoring** for Kwalitec Version 2: the educational architecture by which subject experts transform a professional syllabus into educational knowledge that the Educational Operating Model can teach.

It answers:

> **How does expert subject knowledge become teachable educational knowledge?**

Subject Authoring is the bridge between:

- **Official syllabus authority** — what may be examined  
- **Subject Knowledge Model** — what must be understood  
- **Educational Operating Model** — how the tutor diagnoses, intends, strategises, and teaches  

This is **not** curriculum implementation, content writing, database design, UI design, or AI prompting. It is the architecture of educational authoring.

---

## 2. Definition

**Subject Authoring:** the disciplined educational process by which a subject expert (or authorised authoring team) decomposes syllabus objectives into teachable concepts, dependencies, misconceptions, representations, applications, transfer opportunities, assessment opportunities, and learning objectives — producing educational knowledge artefacts that a tutor can teach against, diagnose against, and evaluate against.

### Governing sentence

> Subject Authoring produces educational knowledge, not software artefacts.  
> It fills the Subject Knowledge Model under Curriculum authority.  
> It does not write lessons, screens, prompts, or database schemas.  
> It makes the syllabus teachable.

### What Subject Authoring is not

| Not this | Why |
|----------|-----|
| Curriculum ingestion / JSON import | Ingestion structures syllabus containers; authoring creates teachable knowledge kinds |
| Writing textbook chapters or video scripts | Those are content production; authoring specifies educational structure |
| Lesson planning or episode scripting | Episode design consumes authored knowledge; it is a later act |
| Database schema or API design | Persistence is infrastructure; authoring is educational |
| Prompt engineering or LLM fine-tuning | Delivery mechanism is irrelevant to authoring architecture |
| Student Digital Twin configuration | The Twin interprets evidence about the learner; it does not invent subject knowledge |

---

## 3. Responsibilities

Subject Authoring is responsible for:

1. **Decomposing** syllabus objectives into teachable concepts and supporting knowledge entities.  
2. **Declaring** educational dependencies (required, helpful, bridge, remediation) among those entities.  
3. **Anticipating** high-frequency misconceptions with observable evidence and repair guidance.  
4. **Specifying** representations through which concepts become intelligible.  
5. **Encoding** authentic application and transfer contexts under syllabus-legitimate demand.  
6. **Deriving** learning objectives that are precise, evidence-amenable, and curriculum-grounded.  
7. **Identifying** assessment opportunities that elicit evidence relative to those objectives.  
8. **Handing off** a coherent knowledge package that Teaching Strategies and Learning Episodes may lawfully consume.

Subject Authoring is **not** responsible for:

- Selecting the next teaching move for a particular student  
- Estimating mastery, confidence, retention, or readiness  
- Rendering UI or choosing delivery media  
- Inventing syllabus scope beyond authorised curriculum  

---

## 4. Inputs

| Input | Nature | Role in authoring |
|-------|--------|-------------------|
| **Official syllabus** | Authoritative examinable scope, objectives, and (where provided) weightings | Bounds what may be authored; does not itself define teachable anatomy |
| **Curriculum Model containers** | Subject → Chapter → Topic packaging | Locates authored knowledge under navigable syllabus structure |
| **Subject-matter expertise** | Professional knowledge of meaning, methods, and typical student error | Primary intellectual source of decomposition quality |
| **Examination practice patterns** | Legitimate demand shapes (without copying proprietary items) | Informs application, transfer, and assessment opportunity design |
| **Educational Domain vocabulary** | Learning, Understanding, Evidence, Mastery, etc. | Constrains how objectives and evidence are framed |
| **Existing Subject Knowledge** | Prior authored concepts, dependencies, misconceptions | Enables reuse, consistency, and network coherence |

Authoring begins from syllabus authority and expert judgement. It does not begin from UI wireframes, analytics dashboards, or model prompts.

---

## 5. Outputs

Authoring produces **educational knowledge artefacts** — structured descriptions that fill the Subject Knowledge Model. Primary outputs include:

| Artefact | Educational role |
|----------|------------------|
| **Concepts** (and related skills, procedures, principles, rules, formulae) | Primary objects of understanding and teaching |
| **Dependencies / prerequisites** | Readiness structure for lawful teaching order |
| **Misconceptions** | Named wrong models with diagnosis and repair guidance |
| **Representations** | Legitimate modes of presenting concept structure |
| **Application contexts** | Situations of legitimate use |
| **Transfer contexts** | Controlled variation for flexible understanding |
| **Assessment opportunities** | Structured elicitation designs relative to objectives |
| **Learning objectives** | Precise educational aims grounded in curriculum |

Secondary supporting artefacts (definitions, examples, counterexamples, analogies, mastery indicators) enrich teachability and are governed by Concept Architecture completeness rules.

### Governing distinction

> Outputs are educational knowledge.  
> They may later be stored, versioned, rendered, or delivered by software.  
> The software representation is not the educational artefact.

---

## 6. Relationship to Adjacent Models

### 6.1 Subject Knowledge Model

The Subject Knowledge Model defines the **kinds** of teachable entities (Concept, Skill, Misconception, Representation, …).

Subject Authoring is the **process and discipline** that populates those kinds for a given syllabus pathway.

| Model | Question answered |
|-------|-------------------|
| Subject Knowledge | *What* is teachable knowledge? |
| Subject Authoring | *How* do experts produce it from a syllabus? |

Authoring must not invent entity kinds that contradict the Subject Knowledge Model without formal amendment.

### 6.2 Curriculum Model

The Curriculum Model defines **packaging and authority** (Curriculum → Subject → Chapter → Topic → Journey/Session).

Authoring attaches educational knowledge **under** that packaging. Topics organise; concepts teach. Completing a topic remains coverage, not mastery.

Syllabus *order* may guide authoring sequence; educational *dependency* may diverge and must be declared explicitly when it does.

### 6.3 Teaching Strategy

Teaching Strategies specify **how** a tutor pursues a Teaching Intention.

They consume authored concepts, misconceptions, representations, and objectives. They do not invent subject meaning. Weak authoring cannot be repaired by clever strategy selection.

### 6.4 Learning Episodes

Learning Episodes are the atomic units of teaching enactment.

Episodes require curriculum-grounded learning objectives and teachable concept anatomy. Authoring must therefore complete (at least to minimal completeness) the knowledge required by intended episode types **before** those episodes are treated as design-ready.

Episode design may reveal authoring gaps; that feedback loop improves authoring — it does not licence teaching without objectives or concepts.

### 6.5 Digital Twin

The Student Digital Twin maintains **learner-state estimates** from evidence (mastery, confidence, retention, readiness, recommendations).

Authoring supplies the **knowledge ontology** against which evidence is interpreted (which concept, which misconception, which objective). The Twin does not author subject knowledge; authoring does not estimate the student.

| Layer | Owns |
|-------|------|
| Subject Authoring | What can be known / misunderstood / evidenced in the subject |
| Digital Twin | What this student currently appears to know, given evidence |

---

## 7. Authoring Stance

Under Kwalitec’s professional-examination stance, Subject Authoring:

1. **Privileges understanding over coverage.** Syllabus bullets become concepts with meaning, boundaries, and dependencies — not checklists.  
2. **Anticipates error.** Misconceptions are first-class authored objects, not footnotes.  
3. **Requires representational diversity.** One formula sheet is not a concept.  
4. **Encodes authentic use.** Application and transfer contexts reflect legitimate professional and examination demand.  
5. **Derives assessable aims.** Learning objectives and assessment opportunities are authored together enough that evidence can speak.  
6. **Remains technology-independent.** The same authored knowledge could be taught by human tutor, platform tutor, or blended means.

---

## 8. Authoring Pipeline (Overview)

The full decomposition pipeline is defined in [`CONCEPT_DECOMPOSITION_MODEL.md`](CONCEPT_DECOMPOSITION_MODEL.md). At overview grain:

```text
Syllabus Objective
        ↓
    Concepts
        ↓
    Dependencies
        ↓
    Misconceptions
        ↓
    Representations
        ↓
    Applications
        ↓
    Transfer Opportunities
        ↓
    Assessment Opportunities
        ↓
    Learning Objectives
```

Stages are educationally ordered. Later stages refine earlier ones; earlier stages must not be skipped. Learning Objectives appear last as the **precise aims** synthesised from the decomposition — not as a substitute for concept anatomy.

---

## 9. Quality of Authored Knowledge

Authored knowledge is adequate for teaching when:

- Concepts meet Concept Architecture **minimal completeness**  
- Dependencies are typed and syllabus-mapped where relevant  
- High-frequency misconceptions are named with observable evidence and repair intentions  
- At least one primary representation exists per concept; diversity is planned where the discipline requires it  
- Application contexts exist before transfer contexts for the same aim  
- Assessment opportunities derive from learning objectives  
- No orphan misconceptions, orphan procedures, or objectives without concept anchors  

Binding detail: [`AUTHORING_INVARIANTS.md`](AUTHORING_INVARIANTS.md).

---

## 10. Architectural Boundaries

| Boundary | Lawful | Unlawful |
|----------|--------|----------|
| Authoring ↔ Content production | Authoring specifies structure and educational roles of examples/representations | Treating a finished textbook chapter as “authored knowledge” without concept anatomy |
| Authoring ↔ Episode design | Episodes consume objectives, concepts, strategies | Episode scripts that invent undocumented concepts mid-flight |
| Authoring ↔ Twin | Authoring defines knowledge targets | Twin inventing concepts from telemetry alone |
| Authoring ↔ Curriculum ingestion | Ingestion loads containers and syllabus metadata | Ingestion claiming misconception or transfer architecture |
| Authoring ↔ Implementation | Future stores may persist authored artefacts | Equating table schemas with educational truth |

---

## 11. Architectural Ambiguities (Declared)

These ambiguities are acknowledged for governance; they are not licences to collapse distinctions:

1. **Depth vs breadth under time pressure** — How complete must authoring be before a pathway is teachable in alpha vs production? Minimal completeness (Concept Architecture §5) is the floor; richness is debt-tracked.  
2. **Syllabus objective grain** — Official objectives may be coarser or finer than teachable concepts. Decomposition may split or cluster; the mapping must remain traceable.  
3. **Assessment opportunity vs assessment item** — Authoring defines *what kind of evidence* to elicit; concrete items may be produced later by content production.  
4. **Transfer threshold** — Near vs far transfer is a design judgement guided by the learning objective (see Application and Transfer Model).  
5. **Multi-author consistency** — Network coherence across authors requires shared dependency and misconception conventions; process governance is out of scope here but required in practice.

---

## 12. Non-Goals

This model does not:

- Author any specific subject’s content  
- Define storage formats, APIs, or Curriculum Studio screens  
- Prescribe AI-assisted authoring workflows  
- Replace the Subject Knowledge Model or Concept Architecture  
- Define runtime tutoring behaviour  

---

## 13. Summary

Subject Authoring is how syllabus authority becomes teachable educational knowledge. It populates the Subject Knowledge Model so that Teaching Strategies, Learning Episodes, and the Digital Twin have stable targets. It produces educational knowledge — not software.
