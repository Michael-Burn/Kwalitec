# Teaching Intention Model

**Document ID:** V2-ERM-003  
**Classification:** Educational Architecture — Reasoning Foundation  
**Status:** Authoritative model of teaching intention  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_DOMAIN_MODEL.md`](EDUCATIONAL_DOMAIN_MODEL.md)  
**Companions:** [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) · [`EDUCATIONAL_HYPOTHESIS_MODEL.md`](EDUCATIONAL_HYPOTHESIS_MODEL.md) · [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md) · [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md) · [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md)

---

## 1. Purpose

This document defines **Teaching Intention** for Kwalitec Version 2.

Teaching Intention is the educational change the tutor wants to achieve during the next Learning Episode. It sits between Educational Hypothesis and Teaching Strategy: after the tutor knows *what* is wrong and *why* it likely is, intention states *what improvement to seek next*.

This is educational architecture. It does not specify UI flows, content files, or algorithms.

---

## 2. Definition

**Teaching Intention:** the deliberate educational change the tutor seeks to produce in the student through the next Learning Episode (or, exceptionally, the next micro-sequence of episodes under one governing intention decomposed atomically).

A Teaching Intention answers:

> *What educational improvement should the next episode achieve?*

Examples:

- Repair misconception  
- Build intuition  
- Strengthen prerequisite  
- Improve transfer  
- Increase procedural fluency  
- Consolidate understanding  
- Recover confidence  
- Prepare for examination  

Teaching Intention is **not**:

- a content title (“Chapter 7”);  
- a calendar block (“90 minutes”);  
- a Teaching Strategy (“use interleaved practice”);  
- a mastery declaration (“make them mastered”);  
- a bundle of unrelated improvements.

---

## 3. Relationship to Teaching Goal

In the Learning Episode Lifecycle, **Teaching Goal** is the episode-grain articulation of exactly one deliberate educational improvement under Educational Atomicity.

**Authority relationship:**

| Concept | Grain | Role |
|---------|-------|------|
| **Teaching Intention** | Reasoning architecture | Named class of educational change sought |
| **Teaching Goal** | Episode lifecycle | Atomic, objective-linked statement realising that intention for one episode |

Every lawful Teaching Goal expresses one Teaching Intention. Every Teaching Intention, when acted upon, must be realised as one or more atomic Teaching Goals (one per episode).

Example:

- Intention: *Strengthen prerequisite*  
- Teaching Goal: “Establish minimal correct explanation of exponential-family mean–variance relationship sufficient to enter GLM deepening”  
- Strategy: conceptual contrast + probe  
- Episode type: Concept Introduction / Prerequisite Repair

---

## 4. Governing Constraints

1. **One primary intention per episode** — Educational Atomicity. Secondary benefits may occur; they must not become co-equal aims.  
2. **Intention requires diagnosis** — no intention without a named educational problem (or lawful cold-start introduction under curriculum sequencing).  
3. **Intention is informed by hypothesis** — the intended change should be the change that would follow if the working hypothesis is roughly right, or that would discriminate among competitors.  
4. **Intention precedes strategy** — *what change* before *how*.  
5. **Intention must be evidentially evaluable** — success evidence must be imaginable in principle.  
6. **Intention never claims mastery as episode outcome.**

---

## 5. Catalogue of Teaching Intentions

For each intention: Educational goal · Success evidence · Typical episode types · Failure conditions.

Episode types refer to [`LEARNING_EPISODE_TYPES.md`](LEARNING_EPISODE_TYPES.md).

---

### 5.1 Repair Misconception

**Educational goal**  
Displace a stable wrong mental model with a corrected structure the student can use and explain.

**Success evidence**  
Correct discrimination on contrastive cases that previously triggered the wrong model; corrected own-words explanation; reduced patterned error on probes targeting the misconception.

**Typical episode types**  
Misconception Repair; Concept Deepening (when repair requires boundary sharpening); Error Analysis.

**Failure conditions**  
More undifferentiated practice without explicit contrast; treating slips as misconceptions; declaring repair from a single correct answer; ignoring persistent patterned error.

---

### 5.2 Build Intuition

**Educational goal**  
Establish meaningful first grasp or deepen felt sense of *why* a concept behaves as it does — recognition plus initial explanatory power, not fluency theatre.

**Success evidence**  
Own-words paraphrase; identification of the idea in simple probes; statement of basic conditions of validity; reduced “formula only” behaviour on introductory items.

**Typical episode types**  
Concept Introduction; Concept Deepening; Worked Example (intuition-first framing).

**Failure conditions**  
Jumping to independent timed practice; flooding with notation before meaning; equating watching an explanation with intuition gained.

---

### 5.3 Strengthen Prerequisite

**Educational goal**  
Restore or establish an upstream capability without which the current objective cannot be honestly pursued.

**Success evidence**  
Successful probes on the prerequisite objective; subsequent reduction of downstream failures that were prerequisite-caused; student can enter the dependent objective without scaffolded prerequisite crutches (or with planned fade).

**Typical episode types**  
Prerequisite Repair; Concept Introduction (on the upstream objective); Guided Practice (if procedural prerequisite).

**Failure conditions**  
Pushing advanced content while pretending the gap is “effort”; bundling prerequisite and advanced aims in one non-atomic episode; infinite delay of the dependent objective without a plan.

---

### 5.4 Improve Transfer

**Educational goal**  
Enable application under legitimate surface variation, novelty, or rewording within syllabus scope.

**Success evidence**  
Success on varied stems, parameters, or formats after teaching; correct mapping from new surface form to known structure; reduced keyword dependence.

**Typical episode types**  
Transfer; Exam Application; Interleaved Practice; Capstone (when synthesis transfer is the aim).

**Failure conditions**  
Only clone practice; declaring transfer from same-day identical items; attempting transfer theatre while misconception or prerequisite gap remains primary.

---

### 5.5 Increase Procedural Fluency

**Educational goal**  
Improve accurate, appropriately efficient execution of a legitimate method the student already conceptually warrants for the aim.

**Success evidence**  
Fewer execution errors; improved completion of multi-step procedures; maintained method choice quality; appropriate speed without collapse of accuracy.

**Typical episode types**  
Guided Practice; Independent Practice; Retrieval / Fluency; Spaced Retrieval (when fluency + retention combine lawfully across episodes).

**Failure conditions**  
Fluency drills on top of misconception or conceptual emptiness; speed goals that destroy accuracy; mistaking fluency for understanding or transfer.

---

### 5.6 Consolidate Understanding

**Educational goal**  
Stabilise and integrate partial grasp into a more complete, coherent understanding of the targeted objective facet — including conditions, boundaries, and relations.

**Success evidence**  
Richer explanations; correct handling of boundary cases previously missed; coherent links to neighbouring ideas *within the atomic aim*; fewer “I get it except when…” failures on the targeted facet.

**Typical episode types**  
Concept Deepening; Connection (when consolidation is relational within scope); Reflection (metacognitive consolidation); Mixed Review (as later consolidation across prior aims — distinct episode).

**Failure conditions**  
Re-teaching the entire chapter as one intention; consolidation claimed without new evidence; confusing consolidation with first introduction.

---

### 5.7 Recover Confidence

**Educational goal**  
Recalibrate self-appraisal upward toward evidence-supported capacity when low confidence is impairing learning or performance.

**Success evidence**  
Reflection and behaviour showing more accurate self-appraisal; willingness to attempt appropriately challenging tasks; reduced avoidance despite demonstrated capacity; performance under mild pressure without collapse *when capacity was already evidenced*.

**Typical episode types**  
Recovery; Confidence Calibration; Guided Practice with success-visible scaffolds; Reflection.

**Failure conditions**  
Empty praise without evidence; ignoring genuine conceptual deficits under the banner of “confidence”; inflating confidence into false confidence.

---

### 5.8 Prepare for Examination

**Educational goal**  
Improve exam-credible deployment of existing (or just-taught) capacity under examination-like constraints: timing, paper structure, presentation, and stem discipline — without sacrificing conceptual honesty.

**Success evidence**  
Improved timed performance relative to untimed baseline *when knowledge is adequate*; better time allocation; fewer misreads; stronger exam-condition transfer; calibrated readiness language.

**Typical episode types**  
Exam Application; Timed Practice; Mixed Review; Capstone; Confidence Calibration (when false or low confidence threatens exam behaviour).

**Failure conditions**  
Exam theatre that skips misconception repair; sacrificing conceptual understanding for short-term mark tricks; treating exam prep as a substitute for missing prerequisites; mastery language from one mock paper.

---

## 6. Additional Lawful Intentions (Specialised)

The eight intentions above are the primary catalogue. The following specialised intentions remain lawful when diagnosis warrants them; they must still obey atomicity.

| Specialised intention | Typical use | Typical episode types |
|-----------------------|-------------|------------------------|
| **Improve retention** | Address weak retention on a previously acquired objective | Spaced Retrieval; Retrieval; Mixed Review |
| **Calibrate confidence downward** | Address false confidence | Confidence Calibration; Transfer probes; Exam Application |
| **Connect fragmented knowledge** | Address knowledge fragmentation | Connection; Capstone; Mixed Review |
| **Strengthen application** | Address application weakness after concept is adequate | Guided Practice → Independent Practice |
| **Complete missing facets** | Address incomplete understanding | Concept Deepening targeting the missing facet |

These specialised forms may be treated as refinements of Consolidate Understanding, Improve Transfer, Prepare for Examination, or related primaries when governance prefers a shorter public catalogue. Educational reasoning may name them explicitly when precision helps.

---

## 7. Mapping Intentions to Deficiency Categories

Illustrative primary mappings (not exclusive):

| Diagnosis category | Typical primary intention |
|--------------------|---------------------------|
| Conceptual misunderstanding | Build intuition / Consolidate understanding |
| Procedural weakness | Increase procedural fluency |
| Weak retention | Improve retention |
| Knowledge fragmentation | Connect fragmented knowledge |
| Prerequisite gap | Strengthen prerequisite |
| Misconception | Repair misconception |
| Low confidence | Recover confidence |
| False confidence | Calibrate confidence downward |
| Exam technique weakness | Prepare for examination |
| Application weakness | Strengthen application |
| Transfer weakness | Improve transfer |
| Incomplete understanding | Consolidate understanding / Complete missing facets |

Priority among simultaneous diagnoses may override a “typical” mapping (see Priority Model).

---

## 8. Success, Failure, and Iteration

After an episode:

- **Intention succeeded (provisionally)** — evidence matches success profile; hypothesis gains support; Twin may update; next intention may advance or shift.  
- **Intention failed productively** — evidence contradicts hypothesis or reveals a better diagnosis; revise hypothesis; choose a new intention.  
- **Intention failed inconclusively** — thin evidence, noise, or interruption; do not over-update; consider a discriminating follow-up.  
- **Intention was wrong for the diagnosis** — strategy or intention mismatch; correct the reasoning chain, do not merely repeat volume.

---

## 9. Summary Propositions

1. Teaching Intention is the educational change sought in the next Learning Episode.  
2. Intention follows diagnosis and hypothesis; it precedes teaching strategy.  
3. One primary intention per episode (atomicity).  
4. Each intention defines educational goal, success evidence, typical episode types, and failure conditions.  
5. Teaching Goal is the atomic episode statement of an intention.  
6. Exam preparation is a lawful intention only when it does not erase conceptual honesty.
