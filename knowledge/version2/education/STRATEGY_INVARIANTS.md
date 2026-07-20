# Strategy Invariants

**Document ID:** V2-TSA-006  
**Classification:** Educational Architecture — Teaching Strategy Foundation  
**Status:** Binding educational invariants for Teaching Strategy  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural (binding for design and governance)  
**Parent:** [`TEACHING_STRATEGY_ARCHITECTURE.md`](TEACHING_STRATEGY_ARCHITECTURE.md)  

**Related:** [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md) · [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) · [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) · [`INSTRUCTIONAL_PRINCIPLES.md`](INSTRUCTIONAL_PRINCIPLES.md)

---

## 1. Purpose

This document states **binding invariants** for Teaching Strategies in Kwalitec Version 2.

Invariants specialise the Teaching Strategy Architecture into non-negotiable rules. They govern design, documentation, and future implementation. They are educational law for instructional method — not software assertions.

Numbering: **S1–S20**. Related reasoning invariants (R9–R11) remain in force; strategy invariants refine the method layer.

---

## 2. Invariant Catalogue

---

### S1 — Every strategy serves a Teaching Intention

**Statement:** A Teaching Strategy may be selected only as a means to a named Teaching Intention (and atomic Teaching Goal for the next episode).

**Rationale:** Methods exist for purposes; purposes do not exist for methods.

**Forbids:** Strategy-first teaching that reverse-fits an intention; method fashion without an educational change target.

**Requires:** Explicit intention → strategy link in educational reasoning.

---

### S2 — Strategies never replace diagnosis

**Statement:** Selecting or naming a Teaching Strategy does not constitute Educational Diagnosis and may not substitute for naming the educational problem.

**Rationale:** *How* is not *what is wrong*.

**Forbids:** Diagnosis statements that are merely method labels (“needs interleaving”); skipping diagnosis because a favourite strategy is ready.

**Requires:** Named deficiency category and objective before strategy commitment (including lawful cold-start introduction diagnosis).

---

### S3 — Strategies remain evidence-driven

**Statement:** Strategy choice, continuation, fade, and revision must be accountable to evidence (including honest thin evidence), not to preference, novelty, or engagement theatre.

**Rationale:** Tutoring without evidence is broadcasting.

**Forbids:** Persisting with a failing strategy solely because it was planned; switching strategies for entertainment; ignoring contradicting evidence.

**Requires:** Expected evidence profiles and evidential exit conditions.

---

### S4 — Strategy choice requires educational justification

**Statement:** Every material strategy selection must be justifiable in educational language linking diagnosis, hypothesis, intention, and instructional principles.

**Rationale:** Unjustified defaults recreate “more questions” tutoring.

**Forbids:** Opaque method assignment; UI-template-driven strategy labels without rationale.

**Requires:** Narratable rationale suitable for governance and explainability to the student at an appropriate grain.

---

### S5 — Guidance decreases as understanding increases

**Statement:** As evidence shows rising understanding and accurate performance, instructional guidance and scaffolding must decrease — unless new evidence warrants temporary re-scaffolding.

**Rationale:** Permanent dependence is not competence.

**Forbids:** Endless scaffolds after success; fading ignored for comfort; abrupt abandonment without readiness evidence labelled as “independence.”

**Requires:** Explicit fade stance in scaffolding compositions; monitoring after fade.

---

### S6 — Strategies respect Educational Atomicity

**Statement:** A strategy governing an episode may not expand the episode into multiple co-equal educational capabilities or multiple co-equal intentions.

**Rationale:** Atomicity makes evidence interpretable.

**Forbids:** Kitchen-sink episodes packing confrontation, interleaving, and exam simulation as one purpose; chapter-sized strategy scopes.

**Requires:** One primary intention and one primary strategy per episode; multi-strategy paths via composition across episodes.

---

### S7 — Strategies may be revised mid-session

**Statement:** When interaction evidence contradicts the strategy’s expected profile, the tutor may revise strategy (and if needed hypothesis or diagnosis) before the planned arc completes.

**Rationale:** Adaptation is a tutor obligation; sacred plans are not.

**Forbids:** Completing a known-mismatched strategy for playlist purity; thrash without interpretation (revision requires reasons).

**Requires:** Evidential warrant for revision; preservation of educational memory of what was tried.

---

### S8 — Instruction remains subordinate to learning objectives

**Statement:** Strategies serve curriculum-grounded learning objectives; objectives are not redefined to fit convenient methods or available materials.

**Rationale:** Curriculum primacy and educational honesty.

**Forbids:** Objective drift toward whatever the strategy entertains; teaching off-syllabus content because a method is elegant.

**Requires:** Teaching Goal linkage to a precise learning objective.

---

### S9 — Intention precedes strategy

**Statement:** Teaching Intention is analytically prior to Teaching Strategy; strategy may not redefine the educational change sought.

**Rationale:** Preserves the reasoning loop order.

**Forbids:** Choosing interleaved practice then claiming the intention was whatever interleaving happens to do.

**Requires:** Named intention before strategy commitment.

---

### S10 — Hypothesis informs but does not select alone

**Statement:** Educational Hypothesis constrains and informs strategy; it does not by itself select strategy without intention, and it does not replace diagnosis.

**Rationale:** Explanation is not method assignment.

**Forbids:** “Because prerequisites” as a complete strategy decision without intention; hypothesis-as-strategy smuggling (“we should drill”).

**Requires:** Distinct stages: diagnosis → hypothesis → intention → strategy.

---

### S11 — One primary strategy per episode

**Statement:** Each Learning Episode has exactly one primary Teaching Strategy governing instructional decisions.

**Rationale:** Multiple co-equal strategies destroy attribution of evidence to method.

**Forbids:** Co-equal dual strategies in one episode; labelling a grab-bag of moves as one strategy without a governing approach.

**Requires:** Subordinate supportive moves clearly marked as non-governing.

---

### S12 — Strategies imply expected evidence

**Statement:** A selected strategy must make success, partial success, and productive failure imaginable in principle through an expected evidence profile.

**Rationale:** Unevaluable methods are educationally void.

**Forbids:** Strategies with no observable consequences; vibe-based “they’ll get it.”

**Requires:** Evidence expectations aligned with intention and episode type.

---

### S13 — Strategies do not declare mastery

**Statement:** No Teaching Strategy may claim mastery, completion-as-mastery, or permanent competence as its outcome.

**Rationale:** Mastery requires broader warrant than a method’s local success.

**Forbids:** “Mastered via worked examples”; exam simulation as mastery certificate.

**Requires:** Modest evaluation language: advanced, partially advanced, or not advanced relative to the Teaching Goal.

---

### S14 — Misconceptions require explicit strategies when diagnosed

**Statement:** When a stable misconception is the primary diagnosis, the primary strategy must confront or displace it explicitly — not bury it in undifferentiated practice or spacing.

**Rationale:** Educational ethics and diagnosis honesty.

**Forbids:** More drills on the contaminated procedure as sole response; spaced reinforcement of the wrong model.

**Requires:** Confrontation, counterexample, error-led, or contrastive strategies (alone or in composition) as governing response.

---

### S15 — Prerequisites constrain lawful strategies

**Statement:** Strategies that presuppose upstream capabilities are unlawful when critical prerequisites are unmet; prerequisite repair (or equivalent) must precede or replace them.

**Rationale:** Dishonest teaching on dependent objectives corrupts evidence and trust.

**Forbids:** Exam simulation or interleaving on objectives blocked by unmet critical prerequisites without repair plan.

**Requires:** Prerequisite check as part of strategy selection inputs.

---

### S16 — Composition preserves episode integrity

**Statement:** Multi-strategy educational arcs must be realised as sequences of atomic episodes, each with one primary strategy — not as single overloaded episodes.

**Rationale:** Composition Model and Atomicity.

**Forbids:** Playlist collapse into one sitting-as-one-episode; “composite strategies” that are secretly multi-aim bundles.

**Requires:** Evidence-gated transitions between stages.

---

### S17 — Strategies are not implementation artefacts

**Statement:** Teaching Strategies are educational reasoning artefacts. They are not AI prompts, LLM templates, UI workflows, screen flows, lesson plan files, question sets, or database entities — though implementations may realise them.

**Rationale:** Long-term governance must keep method reasoning distinct from delivery technology.

**Forbids:** Equating a prompt library with the strategy catalogue; treating a screen flow as educational justification.

**Requires:** Documentation and design to speak in instructional-reasoning language first.

---

### S18 — Exam tactics never erase conceptual duties

**Statement:** Exam Simulation and related exam-horizon strategies may shape practice only when conceptual and prerequisite honesty for the targeted objectives is preserved.

**Rationale:** Professional education rejects mark-trick substitution for understanding.

**Forbids:** Skipping misconception repair for mock-paper volume; mastery language from one simulation.

**Requires:** Adequate knowledge warrant or explicit parallel repair on contaminated objectives.

---

### S19 — Reflection may influence strategy but not replace evidence

**Statement:** Student reflection may warrant strategy adaptation as soft evidence; it may not override strong performance patterns or excuse missing repair, nor be ignored when material.

**Rationale:** Reflection with consequence, without reflection sovereignty.

**Forbids:** Consequence-free reflection theatre; letting “I feel fine” cancel patterned error; discarding reflection that signals load collapse.

**Requires:** Integration of reflection into post-episode strategy decisions alongside performance evidence.

---

### S20 — Twin consults constrain; twin scores do not select

**Statement:** Lawful Digital Twin context may constrain strategy selection (history, uncertainty, prior outcomes); twin scores or dashboards may not by themselves select a Teaching Strategy or replace diagnosis and intention.

**Rationale:** Twin is educational memory, not an oracle method-picker.

**Forbids:** Strategy assignment from a single twin metric; ignoring twin uncertainty when choosing high-load strategies.

**Requires:** Human-educational (or future system) reasoning that cites twin state as background, not as substitute stages of the reasoning loop.

---

## 3. Invariant Dependence Map (Illustrative)

```text
S2 Diagnosis prior
   ↓
S10 Hypothesis informs
   ↓
S9 / S1 Intention then strategy service
   ↓
S4 Justification · S12 Evidence profile · S15 Prerequisites · S20 Twin constraint
   ↓
S11 / S6 Primary strategy + atomicity
   ↓
S3 Evidence-driven enactment
   ↓
S5 Fade · S7 Revision · S19 Reflection
   ↓
S13 No mastery · S18 Exam honesty · S14 Misconception duty
   ↓
S16 Composition integrity · S17 Non-implementation identity
```

---

## 4. Relationship to Other Invariant Families

| Family | Relationship |
|--------|--------------|
| [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) | Domain-wide educational law; strategy invariants must not contradict |
| [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md) | R9–R11 already bind strategy-to-intention and diagnosis/how separation; S-series refines |
| [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) | Episode enactment rules; strategy invariants constrain what episodes may embody |

Conflict resolution: Constitution and domain invariants prevail; then reasoning invariants; then strategy invariants specialise method governance.

---

## 5. Summary Propositions

1. Twenty invariants bind Teaching Strategy as educational reasoning.  
2. Strategy serves intention, never replaces diagnosis, and remains evidence-justified.  
3. Atomicity, one primary strategy per episode, and composition-across-episodes protect interpretable tutoring.  
4. Guidance fades, revision is lawful, mastery is never declared by method success alone.  
5. Strategies are not prompts, screens, or data entities; exam tactics never erase conceptual duties.
