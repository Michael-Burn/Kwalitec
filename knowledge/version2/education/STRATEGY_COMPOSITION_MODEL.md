# Strategy Composition Model

**Document ID:** V2-TSA-005  
**Classification:** Educational Architecture — Teaching Strategy Foundation  
**Status:** Authoritative composition model  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md)  

**Related:** [`TEACHING_STRATEGY_CATALOGUE.md`](TEACHING_STRATEGY_CATALOGUE.md) · [`INSTRUCTIONAL_PRINCIPLES.md`](INSTRUCTIONAL_PRINCIPLES.md) · [`STRATEGY_SELECTION_MODEL.md`](STRATEGY_SELECTION_MODEL.md) · [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md) · [`EDUCATIONAL_ATOMICITY.md`](EDUCATIONAL_ATOMICITY.md)

---

## 1. Purpose

This document defines **how multiple Teaching Strategies combine**.

Teaching rarely uses a single strategy in isolation across a learning path. Composition is the educational art of sequencing strategies so that together they realise a Teaching Intention (or a lawful progression of intentions) without violating Educational Atomicity inside any one Learning Episode.

Composition is educational architecture. It is not a UI wizard, not a content playlist, and not an implementation pipeline.

---

## 2. Definition

**Strategy Composition:** a deliberate, ordered arrangement of Teaching Strategies across one or more Learning Episodes, such that each episode retains one primary strategy and one primary intention, while the sequence as a whole produces a coherent instructional arc.

### Governing distinction

| Concept | Grain | Rule |
|---------|-------|------|
| **Primary strategy** | Single episode | Exactly one governing instructional approach |
| **Supportive moves** | Within episode | May assist the primary strategy; must not become co-equal rival strategies |
| **Strategy sequence** | Micro-sequence / session arc | Ordered strategies across episodes under composition principles |

Packing Analogy + Worked Example + Guided Practice into one episode as three co-equal aims is **not** composition — it is atomicity failure. Composition places them in sequence.

---

## 3. Why Composition Is Required

Single strategies have characteristic limits:

- Analogy without formalisation leaves residue.  
- Worked Example without practice leaves copying.  
- Confrontation without reconstruction leaves a vacuum.  
- Retrieval without prior structure rehearses emptiness.  
- Exam Simulation without foundation trains panic.

Composition finishes what a single strategy rightly starts.

---

## 4. Composition Principles

### C1 — One primary strategy per episode

Each Learning Episode declares one primary Teaching Strategy. Secondary instructional moves are subordinate.

### C2 — Intention continuity or lawful intention progression

A composition either:

- pursues **one** Teaching Intention across multiple strategy stages, or  
- advances a **documented** intention progression (for example Repair misconception → Consolidate understanding) with explicit stage gates.

Silent intention drift mid-sequence is unlawful.

### C3 — Later strategies presuppose earlier success conditions

Each next strategy’s prerequisites must be satisfied by evidence from prior stages (or by independently established twin/evidence history).

### C4 — Guidance generally decreases across the arc

Unless diagnosis warrants re-scaffolding, compositions move from richer support toward independence (P7).

### C5 — Evidence gates transitions

Exit conditions are evidential, not merely temporal. “Time is up” does not complete a stage.

### C6 — Educational coherence over variety

Do not insert strategies for novelty. Every stage must answer *why this next?*

### C7 — Atomicity preserved at every node

Composition increases path richness, never episode scope. Chapter-sized “mega-strategies” remain forbidden.

### C8 — Revisability

Compositions are plans, not vows. Failed exit conditions may loop, branch to repair, or abandon the arc for a better diagnosis.

---

## 5. Ordering

Default educational orders (defeasible):

| Arc type | Typical order |
|----------|---------------|
| **Novice method acquisition** | Direct Explanation or Analogy → Worked Example / Think-Aloud Modelling → Progressive Scaffolding → Faded Guidance → Deliberate Practice / Retrieval After Instruction |
| **Misconception repair** | Misconception Confrontation → Counterexample → Error-Led Teaching or Guided Practice on contrastive cases → Reflection → Retrieval After Instruction (stabilisation) |
| **Intuition to form** | Analogy → Dual Representation → Direct Explanation (formalisation) → Concept Comparison (boundaries) |
| **Fragmentation to discrimination** | Concept Mapping or Concept Comparison → Interleaving → Transfer probes |
| **Retention arc** | Retrieval First (diagnose residual) → brief re-teach if needed → Spaced Reinforcement schedule |
| **Exam deployment** | Think-Aloud Modelling (exam strategy) → Interleaving → Exam Simulation → Reflection / Confidence Calibration |
| **Discovery deepening** | Guided Discovery → Socratic Questioning → Concept Mapping → Retrieval After Instruction |

Ordering obeys Instructional Principles: understanding before memorisation; examples before independence; repair before extension; simple before complex; known before unknown.

---

## 6. Canonical Composition Patterns

### 6.1 Analogy → Worked Example → Guided Practice

```text
Analogy
   ↓
Worked Example
   ↓
Guided Practice  (Progressive Scaffolding / Faded Guidance)
```

**Educational arc**  
Build felt sense → make method structure visible → practise under support.

**Typical intention**  
Build intuition advancing into Strengthen application (lawful progression with stage gate).

**Entry**  
Thin understanding; usable source domain for analogy; procedure will be required.

**Exit to next stage**  
Analogy: student states mapping and a break-point. Worked Example: student narrates decision points. Guided Practice: improving accuracy with decreasing hints.

---

### 6.2 Misconception Confrontation → Counterexample → Reflection

```text
Misconception Confrontation
   ↓
Counterexample
   ↓
Reflection
```

**Educational arc**  
Name and displace wrong model → falsify residual rule → metacognitive consolidation of the corrected model.

**Typical intention**  
Repair misconception (single intention throughout).

**Entry**  
Warranted misconception diagnosis; elicitible wrong model.

**Exit**  
Correct discrimination on contrastive cases; corrected own-words explanation; reflection shows ownership of the change (soft). Follow with practice/retrieval episodes as needed — not stuffed into the reflection episode.

---

### 6.3 Worked Example → Progressive Scaffolding → Faded Guidance

```text
Worked Example
   ↓
Progressive Scaffolding
   ↓
Faded Guidance
```

**Educational arc**  
Classic modelling-to-independence path for procedural aims.

**Typical intention**  
Increase procedural fluency or Strengthen application.

**Entry**  
Concept floor present; new or fragile procedure.

**Exit**  
Reliable performance under reduced support; readiness for Independent Practice or Deliberate Practice — not mastery declaration.

---

### 6.4 Retrieval First → Brief Re-teach → Spaced Reinforcement

```text
Retrieval First
   ↓
Direct Explanation or Error-Led Teaching (only if retrieval reveals need)
   ↓
Spaced Reinforcement
```

**Educational arc**  
Activate and diagnose residual knowledge → repair thin spots → schedule durability.

**Typical intention**  
Improve retention.

**Entry**  
Prior teaching existed; fade suspected.

**Exit**  
Retrieval quality known; re-teach only if warranted; spacing commitments set from evidence, not calendar theatre.

---

### 6.5 Concept Comparison → Interleaving → Exam Simulation

```text
Concept Comparison
   ↓
Interleaving
   ↓
Exam Simulation
```

**Educational arc**  
Clarify discrimination → practise selection under mix → deploy under exam constraints.

**Typical intention**  
Improve transfer → Prepare for examination (lawful progression when knowledge base is adequate).

**Entry**  
Each node has introduction-level competence; mix-ups persist; exam horizon relevant.

**Exit**  
Explicit discrimination statements; mixed-practice selection accuracy; timed deployment improvements without conceptual sacrifice.

---

## 7. Entry Conditions

A composition (or next stage) may begin only when:

1. **Diagnosis and intention are named** for the arc or stage.  
2. **Prerequisites for the opening strategy** hold.  
3. **Cognitive load** permits the opening demand (or scaffolds reduce it).  
4. **Atomic Teaching Goal** for the first episode is defined.  
5. **Success evidence** for the first stage is imaginable in principle.

Opening a composition because a template playlist exists is unlawful.

---

## 8. Exit Conditions

A stage exits when **one** of the following holds:

| Exit type | Meaning | Typical next move |
|-----------|---------|-------------------|
| **Success exit** | Expected evidence profile met provisionally | Advance to next strategy in the arc |
| **Partial exit** | Some progress; residual weakness localised | Narrow Deliberate Practice / Socratic on residual facet; then continue |
| **Productive failure exit** | Evidence contradicts hypothesis or strategy fit | Revise hypothesis/diagnosis/strategy; possibly abandon arc |
| **Inconclusive exit** | Thin evidence, interruption, noise | Discriminating follow-up; do not over-update or fake completion |
| **Safety exit** | Load/affect collapse | Temporary Recovery / re-scaffold; defer high-demand stages |

Time expiry alone is **not** a success exit.

---

## 9. Educational Coherence

A composition is coherent when an expert educator can narrate:

1. **What single educational problem** opened the arc.  
2. **What change** each stage sought.  
3. **Why that order** respects instructional principles.  
4. **What evidence** authorised each transition.  
5. **What remains uncertain** at arc close.

Incoherence indicators:

- strategy variety without rationale;  
- intention drift;  
- return to full explanation after successful fade without new diagnosis;  
- exam simulation inserted mid-repair;  
- reflection episodes that never influence subsequent strategy.

---

## 10. Relationship to Learning Episode Sequences

Strategy Composition and [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md) are complementary:

| Model | Emphasises |
|-------|------------|
| Episode Sequence | How episodes chain as educational units (types, dependencies, micro-sequences) |
| Strategy Composition | How instructional approaches chain to realise intentions |

A lawful micro-sequence of episodes should exhibit a coherent strategy composition. A strategy composition must be realisable as lawful episode types under atomicity.

---

## 11. Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| **Kitchen-sink episode** | Multiple co-equal strategies in one episode |
| **Playlist teaching** | Fixed strategy order ignoring evidence gates |
| **Novelty hopping** | Changing strategy every few minutes without exit conditions |
| **Repair skip** | Jumping to interleaving/exam while misconception live |
| **Permanent scaffold arc** | Composition that never fades |
| **Reflection theatre** | Terminal reflection with no consequence for next strategy |

---

## 12. Summary Propositions

1. Teaching rarely uses one strategy across a full educational arc; composition is normal.  
2. Composition sequences strategies across episodes; it does not overload a single episode.  
3. Ordering follows instructional principles and evidence-gated exit conditions.  
4. Entry requires diagnosis, intention, prerequisites, and imaginable success evidence.  
5. Coherence means narratable problem → change → order → evidence → residual uncertainty.  
6. Compositions are revisable plans subordinate to learning objectives and atomicity.
