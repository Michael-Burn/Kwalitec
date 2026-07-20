# Learning Episode Lifecycle

**Document ID:** V2-LEA-002  
**Classification:** Educational Architecture — Learning Episode Foundation  
**Status:** Authoritative lifecycle specification  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`LEARNING_EPISODE_ARCHITECTURE.md`](LEARNING_EPISODE_ARCHITECTURE.md)  

**Related:** [`TUTOR_MODEL.md`](TUTOR_MODEL.md) · [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) · [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) · [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md)

---

## 1. Purpose

This document defines the **complete educational lifecycle** of a Learning Episode — from the recognition of need to the next educational decision after the episode closes.

The lifecycle specialises the Tutor Model loop (Diagnose → Teach → Observe → Interpret → Adapt) into the episode grain. It is educational law for design, not a state-machine implementation.

---

## 2. Lifecycle Overview

```text
Educational Diagnosis
        ↓
   Teaching Goal
        ↓
 Teaching Strategy
        ↓
 Episode Selection
        ↓
    Instruction
        ↓
Student Interaction
        ↓
Evidence Collection
        ↓
    Reflection
        ↓
Episode Evaluation
        ↓
   Twin Update
        ↓
Next Educational Decision
```

Stages are **educationally ordered**. Some may be brief. None may be silently skipped when the episode claims to be tutoring. Diagnostic probes that discover need may precede Instruction; they are not a substitute for Instruction when the episode’s purpose is to teach a diagnosed aim.

---

## 3. Stage Catalogue

### 3.1 Educational Diagnosis

**Purpose**  
Interpret available evidence to identify the student’s current educational need relative to curriculum aims: gaps, misconceptions, weak learning dimensions, strengths, and readiness for challenge.

**Inputs**

- Accumulated evidence (performance, explanations, prior episode outcomes)  
- Prior reflections  
- Twin estimates and uncertainty (as context, not as invented evidence)  
- Curriculum position and learning objectives  
- Journey / session constraints  

**Outputs**

- Provisional diagnosis (need type, affected objective(s), primary dimension, misconception identity if any)  
- Honesty about thin or conflicting evidence  

**Success criteria**

- Need is named in educational language  
- Diagnosis is grounded in evidence or lawful curriculum sequencing (for cold-start introduction)  
- Diagnosis is revisable  

**Failure conditions**

- Assigning work solely because “it is next” when evidence demands repair  
- Inventing a misconception without patterned support  
- Treating coverage gaps as understanding gaps without distinction  
- Skipping diagnosis and broadcasting undifferentiated content  

---

### 3.2 Teaching Goal

**Purpose**  
Translate diagnosis into **exactly one** deliberate educational improvement — the episode’s teaching goal.

**Inputs**

- Educational diagnosis  
- Candidate learning objective(s)  
- Educational Atomicity constraint  

**Outputs**

- Single teaching goal statement  
- Primary learning dimension named  
- Linked learning objective  

**Success criteria**

- One goal, not a bundle  
- Goal is observable in principle (success can be evidenced)  
- Goal is atomic (see [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md))  

**Failure conditions**

- Goals such as “finish the chapter,” “do GLMs,” or “revise everything weak”  
- Multiple co-equal goals packed into one episode  
- Goals that declare mastery as the episode outcome  

---

### 3.3 Teaching Strategy

**Purpose**  
Select the instructional approach that best fits the diagnosis and teaching goal.

**Inputs**

- Teaching goal  
- Diagnosis (especially misconception vs gap vs fluency vs retention fade)  
- Episode-type affinities and student constraints  

**Outputs**

- Named teaching strategy (for example conceptual contrast, worked-example fading, error analysis, spaced retrieval)  
- Rationale linking strategy to diagnosis  

**Success criteria**

- Strategy matches deficit type  
- Strategy can be realised within available time and materials  
- Rationale is explainable to the student in plain language  

**Failure conditions**

- Defaulting to “more questions” for every diagnosis  
- Choosing strategy for engagement novelty rather than educational fit  
- Strategy incompatible with the teaching goal (for example pure retrieval when the need is conceptual repair)  

---

### 3.4 Episode Selection

**Purpose**  
Choose the Learning Episode type (and template/instance) that realises the teaching goal under the chosen strategy.

**Inputs**

- Teaching goal  
- Teaching strategy  
- Episode type catalogue ([`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md))  
- Prerequisites and duration constraints  

**Outputs**

- Selected episode type  
- Episode instance parameters (objective, misconception id, difficulty band, etc.)  
- Expected evidence profile  

**Success criteria**

- Type matches goal (for example Misconception Repair for a diagnosed wrong model)  
- Prerequisites satisfied or explicitly deferred with a Prerequisite Repair episode first  
- Scope remains atomic  

**Failure conditions**

- Selecting Capstone or Exam Application when introduction has not occurred  
- Selecting Independent Practice before Guided Practice when scaffolds are still required  
- Selecting an episode whose completion criteria cannot produce relevant evidence  

---

### 3.5 Instruction

**Purpose**  
Provide the instructional opportunity that addresses the teaching goal — explanation, contrast, worked example, scaffolded model, or other legitimate teach move.

**Inputs**

- Selected episode  
- Teaching strategy  
- Curriculum-grounded content for the learning objective  

**Outputs**

- Instructional experience delivered to the student  
- Clear target of what will be practised or checked next  

**Success criteria**

- Instruction addresses the diagnosed need  
- Teaching precedes post-instruction assessment of the same aim  
- Instruction remains within the single teaching goal  

**Failure conditions**

- Dumping undifferentiated chapter content  
- Assessing the taught aim with no instructional opportunity  
- Expanding instruction mid-stream into a second educational purpose without closing the episode  

**Note:** For episode types whose educational purpose *is* retrieval or independent practice after prior teaching, Instruction may be minimal (a brief cue or reminder). The lifecycle still requires that the student had a fair instructional opportunity on the aim in this or a prior linked episode.

---

### 3.6 Student Interaction

**Purpose**  
Engage the student in observable work that can evidence progress toward the teaching goal — solving, explaining, classifying, critiquing, retrieving, or reflecting-in-action.

**Inputs**

- Instructional setup  
- Tasks / probes matched to expected evidence  
- Time and difficulty constraints  

**Outputs**

- Student performances, attempts, explanations, timings, and choices  
- Partial products suitable for evidence  

**Success criteria**

- Interaction is active, not passive exposure alone  
- Tasks align with the teaching goal and expected evidence  
- Struggle is interpretable (not pure noise from broken prerequisites)  

**Failure conditions**

- Pure watching / highlighting treated as interaction  
- Tasks that only test a different objective  
- Interaction volume that replaces teaching when teaching was required  

---

### 3.7 Evidence Collection

**Purpose**  
Record lawful educational observations arising from instruction and interaction — without inventing observations from inference.

**Inputs**

- Student interaction artefacts  
- Episode expected-evidence profile  
- Timing and context metadata  

**Outputs**

- Evidence records attributable to the episode and learning objective  
- Separation of observation from later interpretation  

**Success criteria**

- At least one material evidence item exists for a completed episode  
- Evidence is relevant to the teaching goal  
- Soft and stronger signals are distinguishable  

**Failure conditions**

- Closing an episode with no evidence  
- Fabricating evidence from a score label alone presented as independent observation  
- Collecting only engagement metrics as if they were learning evidence  

---

### 3.8 Reflection

**Purpose**  
Capture the student’s structured consideration of difficulty, understanding, and uncertainty after the educational work — as soft evidence with consequence.

**Inputs**

- Episode work just performed  
- Teaching goal (so reflection can be targeted)  
- Reflection prompts appropriate to episode type  

**Outputs**

- Reflection artefact (soft evidence)  
- Signals available to Episode Evaluation and Next Educational Decision  

**Success criteria**

- Reflection is captured (or explicitly deferred under lawful session rules with consequence preserved)  
- Reflection can change subsequent diagnosis or strategy  
- Reflection is the student’s, not system-fabricated  

**Failure conditions**

- Decorative reflection that cannot influence the next move  
- Fabricated reflection presented as the student’s  
- Skipping reflection while claiming a full tutoring episode close  

---

### 3.9 Episode Evaluation

**Purpose**  
Interpret evidence and reflection modestly against the **single** teaching goal: advanced, partially advanced, not advanced, or inconclusive.

**Inputs**

- Evidence collected  
- Reflection  
- Teaching goal and success criteria for the episode type  
- Prior diagnosis (for comparison)  

**Outputs**

- Episode evaluation outcome  
- Updated provisional reading of the need (resolved, reduced, persists, newly discovered)  
- Named uncertainty where evidence is thin  

**Success criteria**

- Evaluation addresses the declared purpose only  
- Language is provisional and dimensional — not mastery theatre  
- Misconceptions are marked resolved or still recorded  

**Failure conditions**

- Declaring mastery from one episode  
- Declaring topic complete  
- Ignoring patterned failure  
- Inflating success from confidence alone  

---

### 3.10 Twin Update

**Purpose**  
Supply lawful inputs so the Student Digital Twin can interpret learner state from evidence — without the episode owning Twin belief.

**Inputs**

- Evidence package  
- Episode evaluation summary  
- Objective / misconception identifiers  
- Temporal context  

**Outputs**

- Twin-consumable update inputs (evidence events / evaluation facts)  
- No direct “mastery = true” write from the episode  

**Success criteria**

- Twin receives observations and evaluations, not invented certificates  
- Uncertainty is preserved where warrant is weak  
- Continuity of educational history is maintained  

**Failure conditions**

- Episode writing mastery badges into Twin  
- Silent erasure of prior evidence  
- Treating Twin estimates as if they were new raw evidence in a circular loop  

---

### 3.11 Next Educational Decision

**Purpose**  
Choose the next educational move: continue with a related episode, change strategy, repair a prerequisite, space for retention, introduce transfer, advance the objective, or pause — with educational justification.

**Inputs**

- Episode evaluation  
- Reflection  
- Twin-updated context  
- Journey / session remaining capacity  
- Curriculum sequencing norms  

**Outputs**

- Explainable next action  
- Optional next teaching goal / episode type  
- Continuity of tutoring memory across episodes  

**Success criteria**

- Decision cites educational interpretation  
- Decision respects Educational Atomicity for the next episode  
- Student can understand why this is next  

**Failure conditions**

- Random topic thrash  
- Endless identical drill after diagnosis has changed  
- Engagement-preserving moves that contradict educational need  
- Skipping interpretation and jumping to opaque ranking outputs  

---

## 4. Lifecycle Integrity Rules

1. **Diagnosis before strategy** — strategy without diagnosis is broadcasting.  
2. **One teaching goal per episode** — a new goal requires a new episode.  
3. **Instruction before post-teach assessment of the same aim** — diagnostic probes exempted; competence claims are not.  
4. **Evidence before evaluation success** — no evidence ⇒ inconclusive, not passed.  
5. **Reflection with consequence** — must be able to affect the next decision.  
6. **Evaluation before adaptation** — Adapt without Interpret is thrash.  
7. **Twin interprets; episodes evidence** — authority boundaries remain intact.  
8. **Abort is lawful** — an episode may end early for fatigue, error, or prerequisite failure; abort still yields evidence of what happened and feeds the next decision.

---

## 5. Mapping to the Tutor Loop

| Tutor loop stage | Episode lifecycle stages |
|------------------|--------------------------|
| Diagnose | Educational Diagnosis → Teaching Goal |
| Teach | Teaching Strategy → Episode Selection → Instruction |
| Observe | Student Interaction → Evidence Collection → Reflection |
| Interpret | Episode Evaluation |
| Adapt | Twin Update inputs → Next Educational Decision |

The tutor loop is continuous across episodes. A single episode is one turn (or a tightly bound cluster of turns) in that larger continuity.

---

## 6. Session-Level Compression

Within a Learning Session, multiple episodes may run sequentially. Lifecycle stages may be **compressed in presentation** (for example one reflection covering a micro-sequence) only if:

- each episode still has a distinct purpose and evidence;  
- reflection remains attributable enough to influence the next decision;  
- no episode is left without evidence.

Compression of UX is allowed. Compression that erases educational identity is not.

---

## 7. Summary Propositions

1. Every Learning Episode follows a diagnosable lifecycle from need to next decision.  
2. Each stage has purpose, inputs, outputs, success criteria, and failure conditions.  
3. The lifecycle specialises the Tutor Model at episode grain.  
4. Skipping stages silently produces false tutoring.  
5. Twin update and next decision close the loop without conferring mastery.
